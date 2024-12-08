from models.vectorBaseModel import BaseVectorDocument
from feature_engineering.models.embedded_chunks import EmbeddedChunk
from models.dataCategory import DataCategory


class Prompt(BaseVectorDocument):
    template: str
    input_variables: dict
    content: str
    num_tokens: int | None = None

    class Config:
        category = DataCategory.PROMPT


class GenerateDatasetSamplesPrompt(Prompt):
    data_category: DataCategory
    document: EmbeddedChunk
