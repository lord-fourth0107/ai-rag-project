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

# The `ContextRetriever` class in Python is designed to retrieve and rerank documents based on a given
# query using various search methods.
class ContextRetriever:
    def __init__(self,mock: bool = False) -> None:
        print(mock)
        self._query_expander=QueryExpansion(mock=mock)
        self._metadata_extractor=SelfQuery(mock=mock)
        self._reranker = Reranker(mock=mock)
    def search(self,query:str,k: int = 3,expand_to_n: int = 3)->list:
        """
        The `search` function retrieves and ranks documents based on a given query using multithreading
        in Python.
        
        :param query: The `query` parameter is a string that represents the search query that you want
        to use to retrieve relevant documents. It is the input text that you want to search for in the
        documents
        :type query: str
        :param k: The `k` parameter in the `search` method specifies the number of top documents to
        retrieve and return as results. By default, it is set to 3, meaning that the method will return
        the top 3 documents that match the search query. However, you can adjust this parameter to
        retrieve, defaults to 3
        :type k: int (optional)
        :param expand_to_n: The `expand_to_n` parameter in the `search` method specifies the number of
        queries to generate from the original query for further searching. This parameter determines how
        many additional queries will be created based on the initial query to potentially broaden the
        search scope and improve search results, defaults to 3
        :type expand_to_n: int (optional)
        :return: The `search` method returns a list of top-k documents that are retrieved and reranked
        based on the given query.
        """
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
        """
        The function `_search` retrieves embedded chunks from different data categories based on a query
        using a specified limit.
        
        :param query: The `query` parameter is an object of type `Query`, which is used to represent a
        search query that will be used to search for relevant data chunks
        :type query: Query
        :param k: The parameter `k` in the `_search` method represents the number of results to retrieve
        for each data category during the search process. The method ensures that `k` is at least 3 by
        including an assertion `assert k >= 3, "k should be >= 3"`. This, defaults to 3
        :type k: int (optional)
        :return: The function `_search` returns a list of `EmbeddedChunk` objects that are retrieved by
        searching for a given query using different data categories such as `EmbeddedYoutubeChunk`,
        `EmbeddedArticleChunk`, and `EmbeddedRepositoryChunk`.
        """
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
        """
        The `rerank` function takes a query, a list of embedded chunks, and a top-k value, reranks the
        documents based on the query, and returns the reranked documents.
        
        :param query: The `query` parameter in the `rerank` method can be either a string or an instance
        of the `Query` class. If it is a string, it will be converted to a `Query` object using the
        `Query.from_str` method before reranking the documents
        :type query: str | Query
        :param chunks: The `chunks` parameter in the `rerank` method is a list of `EmbeddedChunk`
        objects. These objects likely contain information or data that needs to be reranked based on a
        given query. The method takes this list of chunks, along with a query and a parameter
        `keep_top_k
        :type chunks: list[EmbeddedChunk]
        :param keep_top_k: The `keep_top_k` parameter specifies the number of top documents to keep
        after reranking. It determines how many of the reranked documents will be retained based on
        their ranking scores
        :type keep_top_k: int
        :return: The function `rerank` returns a list of `EmbeddedChunk` objects after reranking them
        based on the provided query and keeping the top k results specified by the `keep_top_k`
        parameter.
        """
        if isinstance(query, str):
            query = Query.from_str(query)

        reranked_documents = self._reranker.generate(query=query, chunks=chunks, keep_top_k=keep_top_k)
        logger.info(f"{len(reranked_documents)} documents reranked successfully.")

        return reranked_documents
            


