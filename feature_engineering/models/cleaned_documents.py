from abc import ABC
from typing import Optional

from pydantic import UUID4

from models.vectorBaseModel import BaseVectorDocument
from models.dataCategory import DataCategory


class CleanedDocument(BaseVectorDocument, ABC):
    content: str
    platform: str
    # author_id: UUID4
    # author_full_name: str


class CleanedPostDocument(CleanedDocument):
    image: Optional[str] = None

    class Config:
        name = "cleaned_posts"
        category = DataCategory.POSTS
        use_vector_index = False


class CleanedArticleDocument(CleanedDocument):
    link: str

    class Config:
        name = "cleaned_articles"
        category = DataCategory.ARTICLES
        use_vector_index = False


class CleanedRepositoryDocument(CleanedDocument):
    name: str
    link: str

    class Config:
        name = "cleaned_repositories"
        category = DataCategory.REPOSITORIES
        use_vector_index = False
class CleanedYoutubeDocument(CleanedDocument):
    link: str

    class Config:
        name = "cleaned_youtube"
        category = DataCategory.YOUTUBE
        use_vector_index = False