import opik
from langchain_openai import ChatOpenAI
from loguru import logger
from models.rag_base import Query
from .base import RAGStep
from .prompt_template import SelfQueryTemplate
import openai
from transformers import AutoTokenizer, AutoModelForCausalLM

# model_name = "meta-llama/LLaMA-2-7b"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)
class SelfQuery(RAGStep):
    @opik.track(name="SelfQuery.generate")
    def generate(self, query: Query ) -> Query:
        if self._mock:
            return query
        prompt = SelfQueryTemplate().create_template()
        # input_text = "What is the LLaMA model?"
        # inputs = tokenizer(input_text, return_tensors="pt")

        # # Generate the output using the model
        # outputs = model.generate(inputs['input_ids'], max_length=50, num_return_sequences=1)
        # output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        chain = prompt | model
        response = chain.invoke({"question": query})
        return query ## should return response or query check again
if __name__ == "__main__":
    query = Query.from_str("What is the best way to learn Python?")
    self_query = SelfQuery()
    logger.info(self_query.generate(query))
    