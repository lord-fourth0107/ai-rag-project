from langchain.prompts import PromptTemplate

from .base import PromptTemplateFactory


# The `QueryExpansionTemplate` class is designed to generate multiple versions of a user question to
# enhance document retrieval from a vector database by providing alternative perspectives.
class QueryExpansionTemplate(PromptTemplateFactory):
    prompt: str = """You are an AI language model assistant. Your task is to generate {expand_to_n}
    different versions of the given user question to retrieve relevant documents from a vector
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search.
    Provide these alternative questions seperated by '{separator}'.
    Original question: {question}"""

    @property
    def separator(self) -> str:
        """
        The `separator` function returns the string "#next-question#"
        :return: The method `separator` is being called and it returns the string `#next-question#`.
        """
        return "#next-question#"

    def create_template(self, expand_to_n: int) -> PromptTemplate:
        """
        The function `create_template` creates a PromptTemplate object with specified input and partial
        variables.
        
        :param expand_to_n: The `expand_to_n` parameter is an integer value that specifies how many
        times a certain action should be expanded or repeated. In the context of the `create_template`
        method, it is used to determine the number of times a prompt template should be expanded or
        repeated
        :type expand_to_n: int
        :return: The `create_template` method creates a PromptTemplate object with the specified input
        variables and partial variables. The `template` attribute of the PromptTemplate object is set to
        `self.prompt`, the `input_variables` attribute is set to `["question"]`, and the
        `partial_variables` attribute includes the key-value pairs "separator" with the value of
        `self.separator` and "expand_to_n"
        """
        return PromptTemplate(
            template=self.prompt,
            input_variables=["question"],
            partial_variables={
                "separator": self.separator,
                "expand_to_n": expand_to_n,
            },
        )


# The `SelfQueryTemplate` class is designed to extract user names or user IDs from user questions and
# provide a response containing only the extracted information or "none" if no user name or ID is
# found.
class SelfQueryTemplate(PromptTemplateFactory):
    prompt: str = """You are an AI language model assistant. Your task is to extract information from a user question.
    The required information that needs to be extracted is the user name or user id. 
    Your response should consists of only the extracted user name (e.g., John Doe) or id (e.g. 1345256), nothing else.
    If the user question does not contain any user name or id, you should return the following token: none.
    
    For example:
    QUESTION 1:
    My name is Paul Iusztin and I want a post about...
    RESPONSE 1:
    Paul Iusztin
    
    QUESTION 2:
    I want to write a post about...
    RESPONSE 2:
    none
    
    QUESTION 3:
    My user id is 1345256 and I want to write a post about...
    RESPONSE 3:
    1345256
    
    User question: {question}"""

    def create_template(self) -> PromptTemplate:
        """
        The function `create_template` returns a `PromptTemplate` object with a specified template and
        input variables.
        :return: The function `create_template` returns a `PromptTemplate` object with the template set
        to `self.prompt` and input variables specified as `["question"]`.
        """
        return PromptTemplate(template=self.prompt, input_variables=["question"])