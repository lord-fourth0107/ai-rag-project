from loguru import logger

from models.mongoBaseModel import BaseDataModel
from models.vectorBaseModel import BaseVectorDocument
from models.dataCategory import DataCategory

from .chunking_data_handler import (
    ArticleChunkingHandler,
    ChunkingDataHandler,
    PostChunkingHandler,
    RepositoryChunkingHandler,
    YoutubeChunkingHandler
)
from .cleaning_data_handler import (
    ArticleCleaningHandler,
    CleaningDataHandler,
    PostCleaningHandler,
    RepositoryCleaningHandler,
    YoutubeCleaningHandler
)
from .embedding_data_handler import (
    ArticleEmbeddingHandler,
    EmbeddingDataHandler,
    PostEmbeddingHandler,
    QueryEmbeddingHandler,
    RepositoryEmbeddingHandler,
    YoutubeEmbeddingHandler
)


class CleaningHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> CleaningDataHandler:
        if data_category == DataCategory.POSTS:
            return PostCleaningHandler()
        elif data_category == DataCategory.ARTICLES:
            return ArticleCleaningHandler()
        elif data_category == DataCategory.REPOSITORIES:
            return RepositoryCleaningHandler()
        elif data_category == DataCategory.YOUTUBE:
            return YoutubeCleaningHandler()
        else:
            raise ValueError("Unsupported data type")


class CleaningDispatcher:
    factory = CleaningHandlerFactory()

    @classmethod
    def dispatch(cls, data_model: BaseDataModel) -> BaseVectorDocument:
        data_category = DataCategory(data_model.get_collection_name())
        handler = cls.factory.create_handler(data_category)
        clean_model = handler.clean(data_model)

        logger.info(
            "Document cleaned successfully.",
            data_category=data_category,
            cleaned_content_len=len(clean_model.content),
        )

        return clean_model


class ChunkingHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> ChunkingDataHandler:
        if data_category == DataCategory.POSTS:
            return PostChunkingHandler()
        elif data_category == DataCategory.ARTICLES:
            return ArticleChunkingHandler()
        elif data_category == DataCategory.REPOSITORIES:
            return RepositoryChunkingHandler()
        elif data_category == DataCategory.YOUTUBE:
            return YoutubeChunkingHandler()
        else:
            raise ValueError("Unsupported data type")


class ChunkingDispatcher:
    factory = ChunkingHandlerFactory

    @classmethod
    def dispatch(cls, data_model: BaseVectorDocument) -> list[BaseVectorDocument]:
        data_category = data_model.get_category()
        handler = cls.factory.create_handler(data_category)
        chunk_models = handler.chunk(data_model)

        logger.info(
            "Document chunked successfully.",
            num=len(chunk_models),
            data_category=data_category,
        )

        return chunk_models


class EmbeddingHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> EmbeddingDataHandler:
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
    def dispatch(
        cls, data_model: BaseVectorDocument | list[BaseVectorDocument]
    ) -> BaseVectorDocument | list[BaseVectorDocument]:
        is_list = isinstance(data_model, list)
        if not is_list:
            data_model = [data_model]

        if len(data_model) == 0:
            return []
        print(data_model)
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
            data_category=data_category,
        )

        return embedded_chunk_model