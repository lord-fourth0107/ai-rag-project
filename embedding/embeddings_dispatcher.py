# The above code defines a factory class for creating embedding data handlers based on data categories
# and a dispatcher class for embedding data models using the appropriate handler.
from loguru import logger

from feature_engineering.preprocessing.embedding_data_handler import (
    ArticleEmbeddingHandler,
    EmbeddingDataHandler,
    PostEmbeddingHandler,
    QueryEmbeddingHandler,
    RepositoryEmbeddingHandler,
    YoutubeEmbeddingHandler,
)
from models.dataCategory import DataCategory
from models.vectorBaseModel import BaseVectorDocument

class EmbeddingHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> EmbeddingDataHandler:
        """
        The function `create_handler` returns an `EmbeddingDataHandler` based on the `data_category`
        provided.
        
        :param data_category: The `data_category` parameter in the `create_handler` function is of type
        `DataCategory`, which is an enumeration representing different categories of data such as
        QUERIES, POSTS, ARTICLES, REPOSITORIES, and YOUTUBE. The function returns an
        `EmbeddingDataHandler`
        :type data_category: DataCategory
        :return: The function `create_handler` returns an instance of a specific `EmbeddingDataHandler`
        subclass based on the `data_category` provided. The specific subclass returned depends on the
        value of `data_category`:
        """
        if data_category == DataCategory.QUERIES:
            return QueryEmbeddingHandler()
        if data_category == DataCategory.POSTS:
            return PostEmbeddingHandler()
        elif data_category == DataCategory.ARTICLES:
            return ArticleEmbeddingHandler()
        elif data_category == DataCategory.REPOSITORIES:
            return RepositoryEmbeddingHandler()
        elif data_category == DataCategory.YOUTUBE:
            return YoutubeEmbeddingHandler()
        else:
            raise ValueError("Unsupported data type")
        


class EmbeddingDispatcher:
    factory = EmbeddingHandlerFactory

    @classmethod
    
    def dispatch(cls, data_model: BaseVectorDocument | list[BaseVectorDocument]
       
    ) -> BaseVectorDocument | list[BaseVectorDocument]:
        """
        The function `dispatch` takes a single `BaseVectorDocument` object or a list of
        `BaseVectorDocument` objects, ensures they are of the same category, processes them using a
        handler, and returns the embedded result.
        
        :param cls: In the provided code snippet, `cls` is likely a class object that contains a method
        `factory` with a `create_handler` method. The `create_handler` method is used to create a
        handler based on the data category obtained from the input `data_model`. The handler is then
        used to
        :param data_model: The `data_model` parameter in the `dispatch` function is expected to be
        either an instance of `BaseVectorDocument` or a list of `BaseVectorDocument` instances. The
        function first checks if the input is a list, and if not, it converts the input into a list with
        a
        :type data_model: BaseVectorDocument | list[BaseVectorDocument]
        :return: The function `dispatch` is returning the embedded chunk model. If `data_model` is a
        single instance of `BaseVectorDocument`, then the embedded chunk model will also be a single
        instance of `BaseVectorDocument`. If `data_model` is a list of `BaseVectorDocument` instances,
        then the embedded chunk model will be a list of embedded `BaseVectorDocument` instances.
        """
        is_list = isinstance(data_model, list)
        if not is_list:
            data_model = [data_model]

        if len(data_model) == 0:
            return []

        data_category = data_model[0].get_category()
        assert all(
            data_model.get_category() == data_category for data_model in data_model
        ), "Data models must be of the same category."
        handler = cls.factory.create_handler(data_category)

        embedded_chunk_model = handler.embed_batch(data_model)

        if not is_list:
            embedded_chunk_model = embedded_chunk_model[0]

        logger.info(
            "Data embedded successfully.",
        )

        return embedded_chunk_model