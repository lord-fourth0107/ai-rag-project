import uuid
from abc import ABC
from typing import Generic, Type, TypeVar

from loguru import logger
from pydantic import UUID4, BaseModel, Field
from pymongo import errors
from db.mongClient import connection

_databaseConnection = connection.get_database("rag")
T = TypeVar("T", bound="BaseDataModel")
# The `BaseDataModel` class provides methods for converting data between Python objects and MongoDB
# documents, as well as for saving, retrieving, and bulk operations on MongoDB collections.


class BaseDataModel(BaseModel, ABC, Generic[T]):
    id: UUID4 = Field(default_factory=uuid.uuid4, alias="_id")
    def __eq__(self, value: object) -> bool:
        """
        This function checks if two objects are of the same class and have the same id attribute.
        
        :param value: The `value` parameter in the `__eq__` method represents the object that you are
        comparing with the current object for equality. The method checks if the `value` is an instance
        of the same class as the current object and then compares the `id` attribute of both objects to
        determine if
        :type value: object
        :return: The `__eq__` method is being defined to compare two objects for equality based on their
        `id` attribute. If the `value` object is not an instance of the same class as `self`, it will
        return `False`. Otherwise, it will return the result of comparing the `id` attribute of both
        objects for equality.
        """
        if not isinstance(value, self.__class__):
            return False
        return self.id == value.id
    def __hash__(self) -> int:
        """
        This function returns the hash value of the 'id' attribute of an object.
        :return: The `hash` value of the `id` attribute of the object is being returned.
        """
        return hash(self.id)

    @classmethod
    def from_mongo(cls: Type[T], data: dict) -> T:
        """Convert "_id" (str object) into "id" (UUID object)."""

        if not data:
            raise ValueError("Data is empty.")

        id = data.pop("_id")

        return cls(**dict(data, id=id))

    def to_mongo(self: T, **kwargs) -> dict:
        """Convert "id" (UUID object) into "_id" (str object)."""
        exclude_unset = kwargs.pop("exclude_unset", False)
        by_alias = kwargs.pop("by_alias", True)

        parsed = self.model_dump(exclude_unset=exclude_unset, by_alias=by_alias, **kwargs)

        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = str(parsed.pop("id"))

        for key, value in parsed.items():
            if isinstance(value, uuid.UUID):
                parsed[key] = str(value)

        return parsed

    def model_dump(self: T, **kwargs) -> dict:
        """
        The `model_dump` function converts any UUID values in the dictionary returned by the superclass
        method to strings.
        
        :param self: The `self` parameter in the `model_dump` method refers to the instance of the class
        on which the method is being called. It is a reference to the current object, allowing you to
        access and modify its attributes and methods within the method implementation
        :type self: T
        :return: A dictionary is being returned. The `model_dump` method takes keyword arguments,
        converts the UUID values in the dictionary to strings, and then returns the modified dictionary.
        """
        dict_ = super().model_dump(**kwargs)

        for key, value in dict_.items():
            if isinstance(value, uuid.UUID):
                dict_[key] = str(value)

        return dict_

    def save(self: T, **kwargs) -> T | None:
        """
        The `save` function inserts a document into a collection and returns the document if successful,
        otherwise logs an exception and returns None.
        
        :param self: The `self` parameter in the `save` method refers to the instance of the class on
        which the method is being called. In this context, `self` is of type `T`, which means it can be
        any type. The method is designed to save the instance data to a database collection
        :type self: T
        :return: The `save` method is returning an instance of the class `T` if the document insertion
        is successful. If there is a `WriteError` during the insertion process, it will return `None`.
        """
        collection = _databaseConnection[self.get_collection_name()]
        try:
            collection.insert_one(self.to_mongo(**kwargs))

            return self
        except errors.WriteError:
            logger.exception("Failed to insert document.")

            return None

    @classmethod
    def get_or_create(cls: Type[T], **filter_options) -> T:
        """
        The function `get_or_create` retrieves an instance from a database collection based on filter
        options or creates a new instance if not found.
        
        :param cls: The `cls` parameter in the `get_or_create` function is expected to be a type hint
        representing a class. It is used to specify the type of the object that the function will
        operate on. In this context, it is used to determine the collection name associated with the
        class and to create
        :type cls: Type[T]
        :return: The `get_or_create` function returns an instance of the class `T`. If an instance
        matching the filter options is found in the collection, it is returned after converting it using
        the `from_mongo` method. If no instance is found, a new instance is created using the filter
        options, saved to the collection, and then returned.
        """
        collection = _databaseConnection[cls.get_collection_name()]
        logger.info(collection)
        try:
            instance = collection.find_one(filter_options)
            if instance:
                return cls.from_mongo(instance)

            new_instance = cls(**filter_options)
            new_instance = new_instance.save()

            return new_instance
        except errors.OperationFailure:
            logger.exception(f"Failed to retrieve document with filter options: {filter_options}")

            raise

    @classmethod
    def bulk_insert(cls: Type[T], documents: list[T], **kwargs) -> bool:
        """
        The function `bulk_insert` inserts multiple documents into a MongoDB collection and returns a
        boolean indicating success or failure.
        
        :param cls: The `cls` parameter in the `bulk_insert` function is expected to be a type hint
        representing a class. It is used to specify the type of documents that will be inserted into the
        database collection
        :type cls: Type[T]
        :param documents: The `documents` parameter in the `bulk_insert` function is a list of objects
        of type `T`. These objects represent the documents that you want to insert into a MongoDB
        collection. Each document should have a method `to_mongo(**kwargs)` that converts the document
        object into a format suitable for
        :type documents: list[T]
        :return: The function `bulk_insert` returns a boolean value. It returns `True` if the insertion
        of documents is successful, and `False` if there is an error during the insertion process.
        """
        collection = _databaseConnection[cls.get_collection_name()]
        try:
            collection.insert_many(doc.to_mongo(**kwargs) for doc in documents)

            return True
        except (errors.WriteError, errors.BulkWriteError):
            logger.error(f"Failed to insert documents of type {cls.__name__}")

            return False

    @classmethod
    def find(cls: Type[T], **filter_options) -> T | None:
        """
        The `find` function retrieves a single document from a MongoDB collection based on specified
        filter options.
        
        :param cls: The `cls` parameter in the `find` function is expected to be a type hint
        representing a class. It is used to specify the type of the class whose instances are being
        searched for in the database
        :type cls: Type[T]
        :return: The `find` function is returning an instance of type `T` if a document matching the
        `filter_options` is found in the database collection. If no matching document is found, it
        returns `None`.
        """
        collection = _databaseConnection[cls.get_collection_name()]
        collectionList = _databaseConnection.list_collection_names()
        print("this is +",collectionList)
        try:
            instance = collection.find_one(filter_options)
            #print(instance)
            if instance:
                return cls.from_mongo(instance)
            return None
        except errors.OperationFailure:
            logger.error("Failed to retrieve document")
            return None

    @classmethod
    def bulk_find(cls: Type[T], **filter_options) -> list[T]:
        """
        The function `bulk_find` retrieves documents from a MongoDB collection based on specified filter
        options and returns a list of instances of a specified class.
        
        :param cls: The `cls` parameter in the `bulk_find` function is expected to be a type hint
        representing a class. It is used to specify the type of objects that will be retrieved from the
        database collection
        :type cls: Type[T]
        :return: The function `bulk_find` returns a list of instances of type `T` that match the
        provided filter options from the database collection associated with the class `cls`. If an
        error occurs during the database operation, an empty list is returned.
        """
        collection = _databaseConnection[cls.get_collection_name()]
        try:
            instances = collection.find(filter_options)
            return [document for instance in instances if (document := cls.from_mongo(instance)) is not None]
        except errors.OperationFailure:
            logger.error("Failed to retrieve documents")

            return []

    @classmethod
    def get_collection_name(cls: Type[T]) -> str:
        """
        The function `get_collection_name` retrieves the name of a collection from a class's `Settings`
        configuration.
        
        :param cls: The `cls` parameter in the `get_collection_name` function is expected to be a class
        type (Type[T]). The function checks if the class has a nested class `Settings` and if that
        `Settings` class has an attribute `name`. If these conditions are met, it returns the value
        :type cls: Type[T]
        :return: The function `get_collection_name` is returning the name of the collection specified in
        the `Settings` configuration class of the input class `cls`.
        """
        if not hasattr(cls, "Settings") or not hasattr(cls.Settings, "name"):
            raise Exception(
                "Document should define an Settings configuration class with the name of the collection."
            )
        logger.info(cls.Settings.name)
        return cls.Settings.name

