from abc import ABC, abstractmethod
from models.baseModel import BaseDataModel
from pydantic import UUID4, Field
from models.dataCategory import DataCategory
class UserDocument(BaseDataModel):
    first_name: str
    last_name: str

    class Settings:
        name = "users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Document(BaseDataModel, ABC):
    content: dict
    platform: str
    author_id: UUID4 = Field(alias="author_id")
    author_full_name: str = Field(alias="author_full_name")
class RepoDocument(Document,ABC):
    name: str
    link: str

    class Settings:
        name = str(DataCategory.REPOSITORIES)


# class PostDocument(ABC):

# class ArticleDocument(ABC):

# class VideoSubtitleDocument(ABC):
