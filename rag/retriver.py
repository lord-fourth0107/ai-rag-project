from loguru import logger
from feature_engineering.models import (
       EmbeddedArticleChunk,
       EmbeddedPostChunk,
       EmbeddedRepositoryChunk,
       EmbeddedYoutubeChunk
)
from models.rag_base import Query,EmbeddedQuery
from .query_expansion import QueryExpansion
from .reranking import Reranker
from .self_query import SelfQuery
import concurrent.futures
from feature_engineering.models.embedded_chunks import EmbeddedChunk
from qdrant_client.models import FieldCondition, Filter, MatchValue
from embedding.embeddings_dispatcher import EmbeddingDispatcher
from utils import misc

class ContextRetriever:
    def __init__(self,mock: bool = False) -> None:
        print(mock)
        self._query_expander=QueryExpansion(mock=mock)
        self._metadata_extractor=SelfQuery(mock=mock)
        self._reranker = Reranker(mock=mock)
    def search(self,query:str,k: int = 3,expand_to_n: int = 3)->list:
        query_model = Query.from_str(query)
        # query_model = self._metadata_extractor.generate(query_model)
        # n_generated_queries = self._query_expander.generate(query_model, expand_to_n)
        # logger.info(f"Generated {len(n_generated_queries)} queries")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            search_tasks = [executor.submit(self._search, query_model,k)]
            print(search_tasks)
            n_k_documents = [task.result() for task in concurrent.futures.as_completed(search_tasks)]
            n_k_documents = misc.flatten(n_k_documents)
            n_k_documents = list(set(n_k_documents))

        logger.info(f"{len(n_k_documents)} documents retrieved successfully")

        if len(n_k_documents) > 0:
            k_documents = self.rerank(query, chunks=n_k_documents, keep_top_k=k)
        else:
            k_documents = []

        return k_documents
    def _search(self, query: Query, k: int = 3) -> list[EmbeddedChunk]:
        assert k >= 3, "k should be >= 3"

        def _search_data_category(
            data_category_odm: type[EmbeddedChunk], embedded_query: EmbeddedQuery
        ) -> list[EmbeddedChunk]:
          
            query_filter = None

            return data_category_odm.search(
                query_vector=embedded_query.embedding,
                limit=k // 3,
                query_filter=query_filter,
            )

        embedded_query: EmbeddedQuery = EmbeddingDispatcher.dispatch(query)

        post_chunks = _search_data_category(EmbeddedYoutubeChunk, embedded_query)
        articles_chunks = _search_data_category(EmbeddedArticleChunk, embedded_query)
        repositories_chunks = _search_data_category(EmbeddedRepositoryChunk, embedded_query)

        retrieved_chunks = post_chunks + articles_chunks + repositories_chunks

        return retrieved_chunks

    def rerank(self, query: str | Query, chunks: list[EmbeddedChunk], keep_top_k: int) -> list[EmbeddedChunk]:
        if isinstance(query, str):
            query = Query.from_str(query)

        reranked_documents = self._reranker.generate(query=query, chunks=chunks, keep_top_k=keep_top_k)
        logger.info(f"{len(reranked_documents)} documents reranked successfully.")

        return reranked_documents
            


