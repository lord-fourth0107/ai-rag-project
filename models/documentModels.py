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

class Document(BaseDataModel, ABC):
    content: dict
    platform: str
    # author_id: UUID4 = Field(alias="author_id")
    # author_full_name: str = Field(alias="author_full_name")
class RepoDocument(Document,ABC):
    name: str
    link: str

    class Settings:
        name = DataCategory.REPOSITORIES


class PostDocument(Document,ABC):
    image: Optional[str] = None
    link: str | None = None

    class Settings:
        name = DataCategory.POSTS


class ArticleDocument(Document,ABC):
    link: str
    class Settings:
        name = DataCategory.ARTICLES
class YoutubeDocument(Document,ABC):
    link: str
    class Settings:
        name = DataCategory.YOUTUBE