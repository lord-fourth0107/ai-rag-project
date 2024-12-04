import opik
from langchain_openai import ChatOpenAI
from loguru import logger
from models.rag_base import Query
from .base import RAGStep
from .prompt_template import SelfQueryTemplate
import openai

class SelfQuery(RAGStep):
    @opik.track(name="SelfQuery.generate")
    def generate(self, query: Query ) -> Query:
        if self._mock:
            return query
        prompt = SelfQueryTemplate().create_template()
       
        model = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key="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",
            temperature=0
        )
        chain = prompt | model
        response = chain.invoke({"question": query})
        return query ## should return response or query check again
if __name__ == "__main__":
    query = Query.from_str("What is the best way to learn Python?")
    self_query = SelfQuery()
    logger.info(self_query.generate(query))
    