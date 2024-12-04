import loguru as logger
from feature_engineering.models import (
       EmbeddedArticleChunk,
       EmbeddedPostChunk,
       EmbeddedRepositoryChunk
)
from models.rag_base import Query,EmbeddedQuery
from .query_expansion import QueryExpansion
from .reranking import Reranker
from .self_query import SelfQuery
import concurrent.futures
import openai

class ContextRetriever:
    def __init__(self,mock: bool = False) -> None:
        self._query_expander=QueryExpansion(mock=mock)
        self._metadata_extractor=SelfQuery(mock=mock)
        self._reranker = Reranker(mock=mock)
    def search(self,query:str,k: int = 3,expand_to_n: int = 3)->list:
        query_model = Query.from_str(query)
        query_model = self._metadata_extractor.generate(query_model)
        n_generated_queries = self._query_expander.generate(query_model, expand_to_n)
        logger.info(f"Generated {len(n_generated_queries)} queries")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            search_tasks = [executor.submit(self._search, query,k) for query in n_generated_queries]
            


