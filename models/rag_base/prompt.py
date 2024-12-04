from models.vectorBaseModel import BaseVectorDocument
from models.dataCategory import DataCategory
from feature_engineering.models.cleaned_documents import CleanedDocument
from pydantic import UUID4, Field

class Prompt(BaseVectorDocument):
    template: str
    input_variables: dict
    content: str
    num_tokens: int | None  = None

    class Config:
        category = DataCategory.PROMPTS
    
class GenerateDatasetSamplesPrompt(Prompt):
    data_category : DataCategory
    document: CleanedDocument