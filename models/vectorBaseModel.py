# from db.vectorDBdriver import vectorDBClient
# from typing import Any
# from uuid import UUID
# from pydantic import BaseModel
# import numpy as np 
# from qdrant_client.models import CollectionInfo, PointStruct, Record


# class BaseVectorDocument(BaseModel):
#     def _uuid_to_str(self, item: Any) -> Any:
#         if isinstance(item, dict):
#             for key, value in item.items():
#                 if isinstance(value, UUID):
#                     item[key] = str(value)
#                 elif isinstance(value, list):
#                     item[key] = [self._uuid_to_str(v) for v in value]
#                 elif isinstance(value, dict):
#                     item[key] = {k: self._uuid_to_str(v) for k, v in value.items()}

#         return item
    

#     def batch_upsert(self,embedded_chunks):
#         if not isinstance(embedded_chunks,list):
#             embedded_chunks = [embedded_chunks]
#         for embedded_chunk in embedded_chunks:
#             payload = self._uuid_to_str(embedded_chunk.__dict__)
#             vector = payload.pop("embedding", {})
#             uuid = str(payload.pop("uuid"))
#             if vector and isinstance(vector, np.ndarray):
#                 vector = vector.tolist()
#             annotated = PointStruct(id=uuid, vector=vector, payload=payload)
#             vectorDBClient.upsert(annotated)

    
#     def similarity_search(self,query,rank=10):
        
#         search_result = vectorDBClient.search(
#             collection_name="ai_rag",
#             query_vector=query.tolist(),
#             limit=rank,  # Number of similar items to retrieve
#             with_payload=True
#         )
#         metadata = []
#         for result in search_result:
#             metadata.append(result.payload)
#         return metadata
import uuid
from abc import ABC
from typing import Any, Callable, Dict, Generic, Type, TypeVar
from uuid import UUID

import numpy as np
from loguru import logger
from pydantic import UUID4, BaseModel, Field
from qdrant_client.http import exceptions
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.models import CollectionInfo, PointStruct, Record

from embedding.embeddings import EmbeddingModelSingleton
#from llm_engineering.domain.exceptions import ImproperlyConfigured
from models.dataCategory import DataCategory
from db.vectorDBdriver import vectorDBClient

T = TypeVar("T", bound="BaseVectorDocument")


# The `BaseVectorDocument` class provides functionality for handling vector-based documents with
# methods for conversion, bulk operations, searching, and grouping.
class BaseVectorDocument(BaseModel, Generic[T], ABC):
    id: UUID4 = Field(default_factory=uuid.uuid4)

    def __eq__(self, value: object) -> bool:
        """
        The function checks if the given object is an instance of the same class and compares their 'id'
        attributes for equality.
        
        :param value: The `value` parameter in the `__eq__` method represents the object that you are
        comparing with the current object for equality. The method checks if the `value` is an instance
        of the same class as the current object and then compares the `id` attribute of both objects to
        determine if
        :type value: object
        :return: The `__eq__` method is being defined to compare two objects for equality based on their
        `id` attribute. If the `value` being compared is not an instance of the same class as `self`, it
        will return `False`. Otherwise, it will return the result of comparing the `id` attribute of
        both objects for equality.
        """
        if not isinstance(value, self.__class__):
            return False

        return self.id == value.id

    def __hash__(self) -> int:
        """
        The function returns the hash value of the 'id' attribute of the object.
        :return: The `hash` value of the `id` attribute of the object is being returned.
        """
        return hash(self.id)

    @classmethod
    def from_record(cls: Type[T], point: Record) -> T:
        """
        The function `from_record` converts a record into an instance of a specified class by mapping
        attributes and handling special cases like embedding.
        
        :param cls: `cls` is a type hint representing a class. In this context, it is used to specify
        the type of the object that will be created and returned by the `from_record` method
        :type cls: Type[T]
        :param point: `point` is a Record object containing information such as an id, payload, and
        possibly a vector
        :type point: Record
        :return: An instance of the class `cls` with attributes set based on the `point` record
        provided, including an ID generated from the `point.id`, payload attributes, and potentially an
        "embedding" attribute if the class has a class attribute named "embedding".
        """
        _id = UUID(point.id, version=4)
        payload = point.payload or {}

        attributes = {
            "id": _id,
            **payload,
        }
        if cls._has_class_attribute("embedding"):
            attributes["embedding"] = point.vector or None

        return cls(**attributes)

    def to_point(self: T, **kwargs) -> PointStruct:
        """
        The function `to_point` converts a data model into a `PointStruct` object by extracting specific
        fields and formatting them accordingly.
        
        :param self: The `self` parameter refers to the instance of the class on which this method is
        being called. In this context, it is a generic type `T`
        :type self: T
        :return: The function `to_point` returns a `PointStruct` object with the following attributes:
        - `id`: The ID converted to a string
        - `vector`: The embedding vector converted to a list if it is a numpy array
        - `payload`: The remaining payload data after extracting `id` and `embedding` from the input
        data.
        """
        exclude_unset = kwargs.pop("exclude_unset", False)
        by_alias = kwargs.pop("by_alias", True)

        payload = self.model_dump(exclude_unset=exclude_unset, by_alias=by_alias, **kwargs)

        _id = str(payload.pop("id"))
        vector = payload.pop("embedding", {})
        if vector and isinstance(vector, np.ndarray):
            vector = vector.tolist()

        return PointStruct(id=_id, vector=vector, payload=payload)

    def model_dump(self: T, **kwargs) -> dict:
        """
        The function `model_dump` converts the UUID values in a dictionary to strings.
        
        :param self: The `self` parameter in the `model_dump` method refers to the instance of the class
        on which the method is being called. It is a reference to the current object, allowing the
        method to access and manipulate the object's attributes and methods
        :type self: T
        :return: A dictionary is being returned.
        """
        dict_ = super().model_dump(**kwargs)

        dict_ = self._uuid_to_str(dict_)

        return dict_

    def _uuid_to_str(self, item: Any) -> Any:
        """
        The function `_uuid_to_str` recursively converts UUID objects to strings within dictionaries and
        lists.
        
        :param item: The `_uuid_to_str` method takes an input `item` of type `Any`, which can be a
        dictionary or any other data type. The method recursively iterates through the dictionary and
        converts any UUID objects found into their string representation. If the value associated with a
        key is a list, it
        :type item: Any
        :return: The function `_uuid_to_str` is returning the modified `item` after converting any UUID
        values to strings recursively within dictionaries and lists.
        """
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, UUID):
                    item[key] = str(value)
                elif isinstance(value, list):
                    item[key] = [self._uuid_to_str(v) for v in value]
                elif isinstance(value, dict):
                    item[key] = {k: self._uuid_to_str(v) for k, v in value.items()}

        return item

    @classmethod
    def bulk_insert(cls: Type[T], documents: list["BaseVectorDocument"]) -> bool:
        """
        The function `bulk_insert` attempts to insert a list of documents into a collection, creating
        the collection if it does not exist.
        
        :param cls: The `cls` parameter in the `bulk_insert` function is expected to be a class type
        (Type[T]) that inherits from a base class, and it is used to perform bulk insertion of documents
        into a collection associated with that class
        :type cls: Type[T]
        :param documents: A list of documents that you want to bulk insert into a collection
        :type documents: list["BaseVectorDocument"]
        :return: The function `bulk_insert` returns a boolean value. It returns `True` if the bulk
        insertion of documents was successful, and `False` if there was an error during the insertion
        process.
        """
        try:
            cls._bulk_insert(documents)
        except exceptions.UnexpectedResponse:
            logger.info(
                f"Collection '{cls.get_collection_name()}' does not exist. Trying to create the collection and reinsert the documents."
            )

            cls.create_collection()

            try:
                cls._bulk_insert(documents)
            except exceptions.UnexpectedResponse:
                logger.error(f"Failed to insert documents in '{cls.get_collection_name()}'.")

                return False

        return True

    @classmethod
    def _bulk_insert(cls: Type[T], documents: list["BaseVectorDocument"]) -> None:
        """
        The function `_bulk_insert` takes a class and a list of documents, converts the documents to
        points, and upserts them into a collection using a vector database client.
        
        :param cls: The `cls` parameter in the `_bulk_insert` function is expected to be a type hint for
        a class, specifically a subclass of `T`. It is used to determine the collection name for the
        documents being inserted
        :type cls: Type[T]
        :param documents: A list of "BaseVectorDocument" objects that contain data to be inserted into
        the database
        :type documents: list["BaseVectorDocument"]
        """
        points = [doc.to_point() for doc in documents]

        vectorDBClient.upsert(collection_name=cls.get_collection_name(), points=points)

    @classmethod
    def bulk_find(cls: Type[T], limit: int = 10, **kwargs) -> tuple[list[T], UUID | None]:
        """
        The function `bulk_find` retrieves a list of documents and a next offset value based on the
        provided class and search criteria.
        
        :param cls: The `cls` parameter in the `bulk_find` function represents the class type of the
        documents you want to search for. It is used to specify the type of documents you are querying
        in the database
        :type cls: Type[T]
        :param limit: The `limit` parameter specifies the maximum number of documents to retrieve in a
        single query. In this case, it is set to a default value of 10, meaning that by default, the
        function will attempt to retrieve up to 10 documents, defaults to 10
        :type limit: int (optional)
        :return: The function `bulk_find` returns a tuple containing a list of documents of type `T` and
        a UUID or `None`.
        """
        try:
            documents, next_offset = cls._bulk_find(limit=limit, **kwargs)
        except exceptions.UnexpectedResponse:
            logger.error(f"Failed to search documents in '{cls.get_collection_name()}'.")

            documents, next_offset = [], None

        return documents, next_offset

    @classmethod
    def _bulk_find(cls: Type[T], limit: int = 10, **kwargs) -> tuple[list[T], UUID | None]:
        """
        The function `_bulk_find` retrieves a list of documents from a collection with optional
        filtering and pagination using vectorDBClient.
        
        :param cls: The `cls` parameter in the `_bulk_find` function represents the class type `T` that
        is being used for the bulk find operation. It is used to determine the collection name
        associated with the class and to create instances of the class from the retrieved records
        :type cls: Type[T]
        :param limit: The `limit` parameter in the `_bulk_find` function specifies the maximum number of
        records to retrieve from the database in a single query. In this case, the default value for
        `limit` is set to 10, meaning that by default, the function will retrieve up to 10 records
        unless, defaults to 10
        :type limit: int (optional)
        :return: The function `_bulk_find` returns a tuple containing a list of documents (instances of
        the class `T`) and a UUID or `None`.
        """
        collection_name = cls.get_collection_name()

        offset = kwargs.pop("offset", None)
        offset = str(offset) if offset else None

        records, next_offset = vectorDBClient.scroll(
            collection_name=collection_name,
            limit=limit,
            with_payload=kwargs.pop("with_payload", True),
            with_vectors=kwargs.pop("with_vectors", False),
            offset=offset,
            **kwargs,
        )
        documents = [cls.from_record(record) for record in records]
        if next_offset is not None:
            next_offset = UUID(next_offset, version=4)

        return documents, next_offset

    @classmethod
    def search(cls: Type[T], query_vector: list, limit: int = 10, **kwargs) -> list[T]:
        """
        The function `search` takes a query vector and optional parameters to search for documents of a
        specified class and returns a list of matching documents.
        
        :param cls: The `cls` parameter in the `search` function represents the class type (Type[T])
        that you want to search for documents in. It is used to specify the type of objects you are
        searching for, and the function will search for documents of this type
        :type cls: Type[T]
        :param query_vector: The `query_vector` parameter is a list that represents the vector used for
        searching documents in a specific collection. It contains the information or features that are
        used to match and retrieve relevant documents from the collection based on the search query
        :type query_vector: list
        :param limit: The `limit` parameter in the `search` function specifies the maximum number of
        documents to retrieve from the search operation. By default, if the `limit` parameter is not
        provided when calling the function, it is set to 10. This means that the function will return up
        to 10 documents, defaults to 10
        :type limit: int (optional)
        :return: The function `search` is returning a list of documents of type `T` that match the given
        query vector. If an unexpected response error occurs during the search, an empty list will be
        returned.
        """
        try:
            documents = cls._search(query_vector=query_vector, limit=limit, **kwargs)
        except exceptions.UnexpectedResponse:
            logger.error(f"Failed to search documents in '{cls.get_collection_name()}'.")

            documents = []

        return documents

    @classmethod
    def _search(cls: Type[T], query_vector: list, limit: int = 10, **kwargs) -> list[T]:
        """
        The function `_search` retrieves documents from a database based on a query vector and returns
        them as a list.
        
        :param cls: The `cls` parameter in the `_search` function is expected to be a Type variable
        representing a class. It is used to access class methods and attributes within the function
        :type cls: Type[T]
        :param query_vector: The `query_vector` parameter in the `_search` function is a list that
        represents the vector used for searching in the database. It is typically a numerical
        representation of a query or document that is used to find similar items in the database based
        on similarity metrics
        :type query_vector: list
        :param limit: The `limit` parameter in the `_search` function specifies the maximum number of
        records/documents to retrieve from the database. By default, it is set to 10, meaning that the
        function will return up to 10 documents that match the search criteria. However, you can adjust
        this limit by providing, defaults to 10
        :type limit: int (optional)
        :return: A list of documents of type T is being returned.
        """
        collection_name = cls.get_collection_name()
        records = vectorDBClient.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=kwargs.pop("with_payload", True),
            with_vectors=kwargs.pop("with_vectors", False),
            **kwargs,
        )
        documents = [cls.from_record(record) for record in records]

        return documents

    @classmethod
    def get_or_create_collection(cls: Type[T]) -> CollectionInfo:
        """
        The function `get_or_create_collection` retrieves an existing collection from a vector database
        client or creates a new collection if it does not exist.
        
        :param cls: The `cls` parameter in the `get_or_create_collection` function is expected to be a
        class type (Type[T])
        :type cls: Type[T]
        :return: The function `get_or_create_collection` returns a `CollectionInfo` object.
        """
        collection_name = cls.get_collection_name()

        try:
            return vectorDBClient.get_collection(collection_name=collection_name)
        except exceptions.UnexpectedResponse:
            use_vector_index = cls.get_use_vector_index()

            collection_created = cls._create_collection(
                collection_name=collection_name, use_vector_index=use_vector_index
            )
            if collection_created is False:
                raise RuntimeError(f"Couldn't create collection {collection_name}") from None

            return vectorDBClient.get_collection(collection_name=collection_name)

    @classmethod
    def create_collection(cls: Type[T]) -> bool:
        """
        This function takes a class as input, retrieves the collection name and vector index information
        from the class, and then calls a method to create a collection using this information.
        
        :param cls: The `cls` parameter in the `create_collection` function is expected to be a class
        type. It is used to access class methods `get_collection_name()`, `get_use_vector_index()`, and
        `_create_collection()`
        :type cls: Type[T]
        :return: The function `create_collection` is returning a boolean value.
        """
        collection_name = cls.get_collection_name()
        use_vector_index = cls.get_use_vector_index()

        return cls._create_collection(collection_name=collection_name, use_vector_index=use_vector_index)

    @classmethod
    def _create_collection(cls, collection_name: str, use_vector_index: bool = True) -> bool:
        """
        The function `_create_collection` creates a collection with vector indexing based on the
        provided parameters.
        
        :param cls: The `cls` parameter in the `_create_collection` method is a conventional name used
        to represent the class itself within a class method. It is used to access class variables or
        methods within the method
        :param collection_name: The `collection_name` parameter is a string that represents the name of
        the collection that you want to create in the database. It is the name under which the
        collection will be stored and accessed
        :type collection_name: str
        :param use_vector_index: The `use_vector_index` parameter is a boolean flag that determines
        whether a vector index should be used for the collection. If `use_vector_index` is set to
        `True`, a vector index will be created with specific configuration settings. If it is set to
        `False`, no vector index will be, defaults to True
        :type use_vector_index: bool (optional)
        :return: The function `_create_collection` returns a boolean value indicating whether the
        collection creation was successful or not.
        """
        if use_vector_index is True:
            vectors_config = VectorParams(size=EmbeddingModelSingleton().embedding_size, distance=Distance.COSINE)
        else:
            vectors_config = {}

        return vectorDBClient.create_collection(collection_name=collection_name, vectors_config=vectors_config)

    @classmethod
    def get_category(cls: Type[T]) -> DataCategory:
        """
        This function retrieves the data category of a class by checking if it has a Config class with a
        'category' property.
        
        :param cls: The `cls` parameter in the `get_category` function is expected to be a class type
        (Type[T]) that should have a `Config` class attribute with a `category` property. The function
        retrieves the `category` property from the `Config` class of the provided class and returns it
        :type cls: Type[T]
        :return: The function `get_category` returns the `category` property defined in the `Config`
        class of the input class `cls`.
        """
        if not hasattr(cls, "Config") or not hasattr(cls.Config, "category"):
            raise ImproperlyConfigured(
                "The class should define a Config class with"
                "the 'category' property that reflects the collection's data category."
            )

        return cls.Config.category

    @classmethod
    def get_collection_name(cls: Type[T]) -> str:
        """
        This function retrieves the name of a collection by checking if the class has a Config class
        with a 'name' property.
        
        :param cls: The `cls` parameter in the `get_collection_name` function is expected to be a class
        type (Type[T]). The function checks if the class has a nested `Config` class with a `name`
        property that reflects the collection's name. If the class does not have the required
        configuration,
        :type cls: Type[T]
        :return: The function `get_collection_name` returns the name of the collection as specified in
        the `name` property of the `Config` class within the provided class `cls`.
        """
        if not hasattr(cls, "Config") or not hasattr(cls.Config, "name"):
            raise ImproperlyConfigured(
                "The class should define a Config class with" "the 'name' property that reflects the collection's name."
            )

        return cls.Config.name

    @classmethod
    def get_use_vector_index(cls: Type[T]) -> bool:
        """
        This function checks if a class has a Config attribute with a use_vector_index attribute and
        returns its value.
        
        :param cls: The `cls` parameter in the provided function `get_use_vector_index` is expected to
        be a type hint of a generic class `T`. The function checks if the class `cls` has an attribute
        `Config` and if that `Config` attribute has a sub-attribute `use_vector_index
        :type cls: Type[T]
        :return: The function `get_use_vector_index` returns a boolean value. If the class `cls` does
        not have a `Config` attribute or if the `Config` attribute does not have a `use_vector_index`
        attribute, it returns `True`. Otherwise, it returns the value of `cls.Config.use_vector_index`.
        """
        if not hasattr(cls, "Config") or not hasattr(cls.Config, "use_vector_index"):
            return True

        return cls.Config.use_vector_index

    @classmethod
    def group_by_class(
        cls: Type["BaseVectorDocument"], documents: list["BaseVectorDocument"]
    ) -> Dict["BaseVectorDocument", list["BaseVectorDocument"]]:
        
        """
        The function `group_by_class` groups a list of documents by their class type.
        
        :param cls: The `cls` parameter in the `group_by_class` function is expected to be a type hint
        for a class that inherits from the `BaseVectorDocument` class
        :type cls: Type["BaseVectorDocument"]
        :param documents: The `documents` parameter is a list of objects that are instances of the
        `BaseVectorDocument` class or its subclasses
        :type documents: list["BaseVectorDocument"]
        :return: The function `group_by_class` is returning a dictionary where the keys are instances of
        the class `BaseVectorDocument` and the values are lists of `BaseVectorDocument` instances that
        belong to the same class as the key.
        """

        return cls._group_by(documents, selector=lambda doc: doc.__class__)

    @classmethod
    def group_by_category(cls: Type[T], documents: list[T]) -> Dict[DataCategory, list[T]]:
        """
        The function `group_by_category` groups a list of documents by their category using a specified
        selector function.
        
        :param cls: The `cls` parameter in the `group_by_category` function is expected to be a type
        hint representing a class type. It is used to specify the type of objects that are contained in
        the `documents` list parameter
        :type cls: Type[T]
        :param documents: A list of documents that you want to group by category
        :type documents: list[T]
        :return: The function `group_by_category` is returning a dictionary where the keys are instances
        of `DataCategory` and the values are lists of objects of type `T`. The objects in the lists are
        grouped based on their category, which is obtained by calling the `get_category()` method on
        each object in the `documents` list.
        """
        return cls._group_by(documents, selector=lambda doc: doc.get_category())

    @classmethod
    def _group_by(cls: Type[T], documents: list[T], selector: Callable[[T], Any]) -> Dict[Any, list[T]]:
        """
        The function `_group_by` groups a list of documents by a specified key selector function.
        
        :param cls: The `cls` parameter in the `_group_by` function is of type `Type[T]`, which means it
        expects a class as input. This parameter is not used within the function implementation provided
        :type cls: Type[T]
        :param documents: A list of documents of type T that you want to group based on a specific
        selector function
        :type documents: list[T]
        :param selector: The `selector` parameter in the `_group_by` function is a callable that takes
        an element of the input `documents` list as its argument and returns a value based on which the
        elements will be grouped together. This value will be used as the key in the resulting
        dictionary that groups the elements
        :type selector: Callable[[T], Any]
        :return: A dictionary where the keys are the result of applying the `selector` function to the
        elements in the `documents` list, and the values are lists of elements from `documents` that
        have the same key.
        """
        grouped = {}
        for doc in documents:
            key = selector(doc)

            if key not in grouped:
                grouped[key] = []
            grouped[key].append(doc)

        return grouped

    @classmethod
    def collection_name_to_class(cls: Type["BaseVectorDocument"], collection_name: str) -> type["BaseVectorDocument"]:
        """
        The function `collection_name_to_class` takes a base class and a collection name, and returns
        the subclass that corresponds to the given collection name.
        
        :param cls: The `cls` parameter in the `collection_name_to_class` function is expected to be a
        type hint for a class that inherits from `BaseVectorDocument`. This parameter is used to iterate
        over the subclasses of the provided class to find a subclass that matches the given
        `collection_name`
        :type cls: Type["BaseVectorDocument"]
        :param collection_name: The `collection_name` parameter is a string that represents the name of
        a collection
        :type collection_name: str
        :return: a subclass of the input class `cls` that has a collection name matching the input
        `collection_name`. If no subclass is found with a matching collection name, it raises a
        `ValueError` with a message indicating that no subclass was found for the given collection name.
        """
        for subclass in cls.__subclasses__():
            try:
                if subclass.get_collection_name() == collection_name:
                    return subclass
            except ImproperlyConfigured:
                pass

            try:
                return subclass.collection_name_to_class(collection_name)
            except ValueError:
                continue

        raise ValueError(f"No subclass found for collection name: {collection_name}")

    @classmethod
    def _has_class_attribute(cls: Type[T], attribute_name: str) -> bool:
        """
        The function `_has_class_attribute` checks if a class or its base classes have a specified
        attribute.
        
        :param cls: The `cls` parameter in the `_has_class_attribute` function represents a class type
        (Type[T]) for which we want to check if it has a specific class attribute with the given name
        :type cls: Type[T]
        :param attribute_name: The `attribute_name` parameter in the `_has_class_attribute` function
        refers to the name of the class attribute that you want to check for existence within the class
        or its base classes
        :type attribute_name: str
        :return: a boolean value - `True` if the class `cls` or any of its base classes have the
        attribute with the name `attribute_name`, otherwise it returns `False`.
        """
        if attribute_name in cls.__annotations__:
            return True

        for base in cls.__bases__:
            if hasattr(base, "_has_class_attribute") and base._has_class_attribute(attribute_name):
                return True

        return False