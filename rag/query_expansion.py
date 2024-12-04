import opik
from langchain_openai import ChatOpenAI
from loguru import logger
from models.rag_base import Query
from .base import RAGStep
from .prompt_template import QueryExpansionTemplate


class QueryExpansion(RAGStep):

    @opik.track(name="QueryExpansion.generate")
    def generate(self, query: Query, expand_to_n: int,*args, **kwargs) -> list[Query]:
        assert expand_to_n > 0, "expand_to_n must be greater than 0"
        if self._mock:
            return [query for _ in range(expand_to_n)]
        query_expansion_template = QueryExpansionTemplate()
        prompt = query_expansion_template.create_template(expand_to_n-1)
        model = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key="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",
            temperature=0
        )
        chain = prompt | model
        response = chain({"question": query})
        result = response.content
        queries_content = result.strip().split(query_expansion_template.separator)
        queries = [query]
        queries += [query.replace_content(query_content) for query_content in queries_content]
        return queries
    
if __name__ == "__main__":
    query = Query.from_str("What is the best way to learn Python?")
    query_expansion = QueryExpansion()
    queries = query_expansion.generate(query, expand_to_n=3)
    for expanded_query in queries:
        logger.info(expanded_query.content)