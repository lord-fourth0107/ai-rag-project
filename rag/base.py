from abc import ABC, abstractmethod
from typing import Any

from langchain.prompts import PromptTemplate
from pydantic import BaseModel

from models.rag_base.query import Query


# This class is an abstract factory for creating prompt templates.
class PromptTemplateFactory(ABC, BaseModel):
    @abstractmethod
    def create_template(self) -> PromptTemplate:
        """
        This function is intended to create a template and should return a PromptTemplate object.
        """
        pass


# The `RAGStep` class is an abstract base class with an abstract method `generate` that takes a
# `Query` object as input.
class RAGStep(ABC):
    def __init__(self, mock: bool = False) -> None:
        self._mock = mock

    @abstractmethod
        
    def generate(self, query: Query, *args, **kwargs) -> Any:

        """
        The `generate` function is an abstract method that takes a `Query` object and additional
        arguments to generate a result.
        
        :param query: The `query` parameter in the `generate` method represents a query object that is
        being passed to the method. It is of type `Query`
        :type query: Query
        """

        pass