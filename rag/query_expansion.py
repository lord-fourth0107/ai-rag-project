import opik
from langchain_openai import ChatOpenAI
from loguru import logger
from models.rag_base import Query
from .base import RAGStep
from .prompt_template import QueryExpansionTemplate


# The `QueryExpansion` class defines a method `generate` that expands a given query using a template
# and a language model.
class QueryExpansion(RAGStep):

    @opik.track(name="QueryExpansion.generate")
       
    def generate(self, query: Query, expand_to_n: int,*args, **kwargs) -> list[Query]:
        """
        The `generate` function takes a query and expands it into multiple related queries using a
        language model, returning a list of Query objects.
        
        :param query: The `query` parameter is the input query for which you want to generate query
        expansions. It is of type `Query`, which is likely a data structure representing a search query
        :type query: Query
        :param expand_to_n: The `expand_to_n` parameter in the `generate` method specifies the number of
        queries to generate as expansions of the input query. It determines how many additional queries
        will be created based on the input query. The method will generate a list of `expand_to_n`
        queries, including the original input
        :type expand_to_n: int
        :return: The `generate` method returns a list of Query objects. The method takes a Query object
        as input, along with an integer `expand_to_n` specifying how many expanded queries to generate.
        It then generates additional queries based on the input query using a model and template, and
        returns a list containing the original query and the expanded queries.
        """

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