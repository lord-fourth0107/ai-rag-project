from loguru import logger

from feature_engineering.preprocessing.embedding_data_handler import (
    ArticleEmbeddingHandler,
    EmbeddingDataHandler,
    PostEmbeddingHandler,
    #QueryEmbeddingHandler,
    RepositoryEmbeddingHandler,
)
from models.dataCategory import DataCategory
from models.vectorBaseModel import BaseVectorDocument

class EmbeddingHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> EmbeddingDataHandler:
        # if data_category == DataCategory.QUERIES:
        #     return QueryEmbeddingHandler()
        if data_category == DataCategory.POSTS:
            return PostEmbeddingHandler()
        elif data_category == DataCategory.ARTICLES:
            return ArticleEmbeddingHandler()
        elif data_category == DataCategory.REPOSITORIES:
            return RepositoryEmbeddingHandler()
        else:
            raise ValueError("Unsupported data type")
        


class EmbeddingDispatcher:
    factory = EmbeddingHandlerFactory

    @classmethod
    def dispatch(
        cls, data_model: BaseVectorDocument | list[BaseVectorDocument]
    ) -> BaseVectorDocument | list[BaseVectorDocument]:
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