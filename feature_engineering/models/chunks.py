from abc import ABC
from typing import Optional

from pydantic import UUID4, Field

from models.vectorBaseModel import BaseVectorDocument
from models.dataCategory import DataCategory


# The `Chunk` class represents a document chunk with content, platform, document ID, and optional
# metadata.
class Chunk(BaseVectorDocument, ABC):
    content: str
    platform: str
    document_id: UUID4
    metadata: dict = Field(default_factory=dict)


# The `PostChunk` class represents a chunk of data with an optional image attribute, categorized under
# `DataCategory.POSTS`.
class PostChunk(Chunk):
    image: Optional[str] = None

    class Config:
        category = DataCategory.POSTS


# The `ArticleChunk` class represents a chunk of data related to articles and includes a link
# attribute.
class ArticleChunk(Chunk):
    link: str

    class Config:
        category = DataCategory.ARTICLES


class RepositoryChunk(Chunk):
    name: str
    link: str

    class Config:
        category = DataCategory.REPOSITORIES
class YoutubeChunk(Chunk):
    link: str

    class Config:
        category = DataCategory.YOUTUBE