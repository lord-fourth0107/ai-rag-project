from abc import ABC

from pydantic import UUID4, Field

from models.dataCategory import DataCategory

from models.vectorBaseModel import BaseVectorDocument


class EmbeddedChunk(BaseVectorDocument, ABC):
    content: str
    embedding: list[float] | None
    platform: str
    document_id: UUID4
    # author_id: UUID4
    # author_full_name: str
    metadata: dict = Field(default_factory=dict)

    @classmethod
    def to_context(cls, chunks: list["EmbeddedChunk"]) -> str:
        context = ""
        for i, chunk in enumerate(chunks):
            context += f"""
            Chunk {i + 1}:
            Type: {chunk.__class__.__name__}
            Platform: {chunk.platform}
            Content: {chunk.content}\n
            """

        return context


class EmbeddedPostChunk(EmbeddedChunk):
    class Config:
        name = "embedded_posts"
        category = DataCategory.POSTS
        use_vector_index = True


class EmbeddedArticleChunk(EmbeddedChunk):
    link: str

    class Config:
        name = "embedded_articles"
        category = DataCategory.ARTICLES
        use_vector_index = True


class EmbeddedRepositoryChunk(EmbeddedChunk):
    name: str
    link: str

    class Config:
        name = "embedded_repositories"
        category = DataCategory.REPOSITORIES
        use_vector_index = True
class EmbeddedYoutubeChunk(EmbeddedChunk):
    link: str

    class Config:
        name = "embedded_youtube"
        category = DataCategory.YOUTUBE
        use_vector_index = True