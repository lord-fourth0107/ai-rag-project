import opik
from embedding.embeddings import CrossEncoderModelSingleton
from .base import RAGStep
from feature_engineering.models.embedded_chunks import EmbeddedChunk
from models.rag_base import Query


# The `Reranker` class is used for reranking a list of embedded chunks based on a query using a
# cross-encoder model.
class Reranker(RAGStep):
    def __init__(self, mock: bool = False) -> None:
        super().__init__(mock=mock)
        self.model = CrossEncoderModelSingleton()

    #@opik.track(name="Reranker.generate")
    def generate(self, query: Query, chunks: list[EmbeddedChunk], keep_top_k : int) -> list[EmbeddedChunk]:
        """
        This function takes a query, a list of embedded chunks, and a top-k value, predicts scores for
        each chunk based on the query, sorts the chunks by score in descending order, keeps the top-k
        chunks, and returns the reranked chunks.
        
        :param query: The `query` parameter is an object of type `Query`, which likely contains
        information about the search query that needs to be processed
        :type query: Query
        :param chunks: The `chunks` parameter in the `generate` method is a list of `EmbeddedChunk`
        objects. Each `EmbeddedChunk` object likely contains some content that needs to be processed or
        analyzed in relation to the given `query`. The method seems to be using these chunks to generate
        scores based on the
        :type chunks: list[EmbeddedChunk]
        :param keep_top_k: The `keep_top_k` parameter specifies the number of top-ranked documents that
        should be kept after the reranking process. It determines how many of the highest-scoring
        documents will be included in the final list of `EmbeddedChunk` objects returned by the
        `generate` method
        :type keep_top_k: int
        :return: the list of reranked documents after sorting and selecting the top k documents based on
        the scores predicted by the model.
        """
        if self._mock:
            return chunks

        query_doc_tuple=[(query.content,chunk.content) for chunk in chunks]
        scores = self.model.predict(query_doc_tuple)
        scored_query_doc_tuples = list(zip(scores,query_doc_tuple))
        scored_query_doc_tuples.sort(key=lambda x: x[0], reverse=True)
        scored_query_doc_tuples = scored_query_doc_tuples[:keep_top_k]
        reranked_docs = [doc for _,doc in reranked_docs]
        return reranked_docs