import opik
from embedding.embeddings import CrossEncoderModelSingleton
from .base import RAGStep
from feature_engineering.models.embedded_chunks import EmbeddedChunk
from models.rag_base import Query
class Reranker(RAGStep):
    def __init__(self, mock: bool = False) -> None:
        super().__init__(mock=mock)
        self.model = CrossEncoderModelSingleton()

    #@opik.track(name="Reranker.generate")
    def generate(self, query: Query, chunks: list[EmbeddedChunk], keep_top_k : int) -> list[EmbeddedChunk]:
        if self._mock:
            return chunks

        query_doc_tuple=[(query.content,chunk.content) for chunk in chunks]
        scores = self.model.predict(query_doc_tuple)
        scored_query_doc_tuples = list(zip(scores,query_doc_tuple))
        scored_query_doc_tuples.sort(key=lambda x: x[0], reverse=True)
        scored_query_doc_tuples = scored_query_doc_tuples[:keep_top_k]
        reranked_docs = [doc for _,doc in reranked_docs]
        return reranked_docs