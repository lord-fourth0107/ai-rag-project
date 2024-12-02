from abc import ABC
from typing import Optional

from pydantic import UUID4, Field

from models.vectorBaseModel import BaseVectorDocument
from models.dataCategory import DataCategory


class Chunk(BaseVectorDocument, ABC):
    content: str
    platform: str
    document_id: UUID4
    # author_id: UUID4
    # author_full_name: str
    metadata: dict = Field(default_factory=dict)


class PostChunk(Chunk):
    image: Optional[str] = None

    class Config:
        category = DataCategory.POSTS


class ArticleChunk(Chunk):
    link: str

    class Config:
        category = DataCategory.ARTICLES


class RepositoryChunk(Chunk):
    name: str
    link: str

    class Config:
        category = DataCategory.REPOSITORIES