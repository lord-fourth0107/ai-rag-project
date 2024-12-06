from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from loguru import logger

from feature_engineering.models.cleaned_documents import (
    CleanedArticleDocument,
    CleanedDocument,
    CleanedPostDocument,
    CleanedRepositoryDocument,
    CleanedYoutubeDocument,
)
from models.documentModels import (
    ArticleDocument,
    Document,
    PostDocument,
    RepoDocument,
    YoutubeDocument,
)

from .operations.cleaning import clean_text

DocumentT = TypeVar("DocumentT", bound=Document)
CleanedDocumentT = TypeVar("CleanedDocumentT", bound=CleanedDocument)


class CleaningDataHandler(ABC, Generic[DocumentT, CleanedDocumentT]):
    """
    Abstract class for all cleaning data handlers.
    All data transformations logic for the cleaning step is done here
    """

    @abstractmethod
    def clean(self, data_model: DocumentT) -> CleanedDocumentT:
        pass


class PostCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: PostDocument) -> CleanedPostDocument:
        return CleanedPostDocument(
            id=data_model.id,
            content=clean_text(" #### ".join(data_model.content.values())),
            platform=data_model.platform,
            # author_id=data_model.author_id,
            # author_full_name=data_model.author_full_name,
            image=data_model.image if data_model.image else None,
        )


class ArticleCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: ArticleDocument) -> CleanedArticleDocument:
        valid_content = [content for content in data_model.content.values() if content]

        instance = CleanedArticleDocument(
            id=data_model.id,
            content=clean_text(" #### ".join(valid_content)),
            platform=data_model.platform,
            link=data_model.link,
            # author_id=data_model.author_id,
            # author_full_name=data_model.author_full_name,
        )
        logger.debug(f"Cleaned article: {instance.__dict__}")
        return instance


class RepositoryCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: RepoDocument) -> CleanedRepositoryDocument:
        return CleanedRepositoryDocument(
            id=data_model.id,
            content=clean_text(" #### ".join(data_model.content.values())),
            platform=data_model.platform,
            name=data_model.name,
            link=data_model.link,
            # author_id=data_model.author_id,
            # author_full_name=data_model.author_full_name,
        )
class YoutubeCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: YoutubeDocument) -> CleanedYoutubeDocument:
        valid_content = [content for content in data_model.content.values() if content]
        return CleanedYoutubeDocument(

            id=data_model.id,
            content=clean_text(" #### ".join(valid_content)),
            platform=data_model.platform,
            #name=data_model.name,
            link=data_model.link,
        )