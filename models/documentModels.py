from abc import ABC, abstractmethod
from models.mongoBaseModel import BaseDataModel
from pydantic import UUID4, Field
from models.dataCategory import DataCategory
from typing import Optional
# class UserDocument(BaseDataModel):
#     first_name: str
#     last_name: str

#     class Settings:
#         name = "users"

#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}"

# The `Document` class represents a document with content stored as a dictionary and associated with a
# platform.
class Document(BaseDataModel, ABC):
    content: dict
    platform: str
    # author_id: UUID4 = Field(alias="author_id")
    # author_full_name: str = Field(alias="author_full_name")
# The class `RepoDocument` represents a document with `name` and `link` attributes, categorized under
# `DataCategory.REPOSITORIES`.
class RepoDocument(Document,ABC):
    name: str
    link: str

    class Settings:
        name = DataCategory.REPOSITORIES


# This Python class `PostDocument` represents a document for posts with optional image and link
# attributes.
class PostDocument(Document,ABC):
    image: Optional[str] = None
    link: str | None = None

    class Settings:
        name = DataCategory.POSTS


# The `ArticleDocument` class represents a document for articles with a link attribute and belongs to
# the `ARTICLES` data category.
class ArticleDocument(Document,ABC):
    link: str
    class Settings:
        name = DataCategory.ARTICLES


# The `YoutubeDocument` class represents a document with a YouTube link and belongs to the `YOUTUBE`
# data category.
class YoutubeDocument(Document,ABC):
    link: str
    class Settings:
        name = DataCategory.YOUTUBE