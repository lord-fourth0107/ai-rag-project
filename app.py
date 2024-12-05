from dataExtraction.crawlers import GitHubCrawler
from steps.crawl import crawl_links
from feature_engineering.query_datawarehouse import query_data_warehouse
from feature_engineering.load_to_vector_db import load_to_vector_db
from steps.feature import clean_documents, chunk_and_embed
from transformers import AutoTokenizer, AutoModelForCausalLM
from ollama import Client
import requests
import ollama
from feature_engineering.models.embedded_chunks import EmbeddedChunk
# model_name = "meta-llama/Llama-2-7b"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)
from rag.retriver import ContextRetriever
def openFile():
    file = open("urls.txt", "r")
    urls = file.readlines()
    file.close()    
    return urls
# def crawl(url):
#     visited_urls = []
#     crawled_urls = []
#     for url in openFile():
#         if url not in visited_urls:
#             url = url.strip()
#             response = requests.get(url)
#             soup = BeautifulSoup(response.content, "html.parser")
#             visited_urls.append(url)
#             crawled_urls.append(soup)
#             #print(soup.find("p"))   
#         else:
#             print("Already visited")
# #     return crawled_urls
# def split_user_full_name(user: str | None) -> tuple[str, str]:
#     if user is None:
#         raise Exception("User name is empty")

#     name_tokens = user.split(" ")
#     if len(name_tokens) == 0:
#         raise Exception("User name is empty")
#     elif len(name_tokens) == 1:
#         first_name, last_name = name_tokens[0], name_tokens[0]
#     else:
#         first_name, last_name = " ".join(name_tokens[:-1]), name_tokens[-1]

#     return first_name, last_name
# def get_or_create_user(user_full_name: str) -> Annotated[UserDocument, "user"]:
#     logger.info(f"Getting or creating user: {user_full_name}")

#     first_name, last_name = split_user_full_name(user_full_name)

#     user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)

#     # step_context = get_step_context()
#     # step_context.add_output_metadata(output_name="user", metadata=_get_metadata(user_full_name, user))

#     return user


if __name__ == "__main__":
    # githubCrawler = GitHubCrawler()
    # #user = get_or_create_user("John Doe")
    # urls=["https://github.com/ros2/ros2_documentation","https://medium.com/@Gabriel_Chollet/what-is-ros-c38493fe3eca","https://youtu.be/Gg25GfA456o?si=KEeyvdEIEC3tdYF5"]
    # #urls=["https://youtu.be/Gg25GfA456o?si=KEeyvdEIEC3tdYF5"]
    # # for url in openFile():
    # #    urls.append(url)
    # crawl_links(urls)
    # results = query_data_warehouse()
    # #print(results)
    # cleanded_documents = clean_documents(results)
    # chunked_documents = chunk_and_embed(cleanded_documents)
    # load_to_vector_db(chunked_documents)
    contextRetriver = ContextRetriever(mock=True)
    docs = contextRetriver.search("what is ros2")
    context = EmbeddedChunk.to_context(docs)
    
    client = Client(
    host='http://localhost:11434',
    )
    #print("Models are :",client.list())
    response = client.chat(model='llama3:latest', messages=[
  {
    'role': 'user',
    'content': 'Steps to install  ros2',
    # 'context': context
  },
])
    print(response)
# Send request to Ollama
    # try:
        
    #     response = requests.post('http://localhost:11434', json=payload)
    #     if response.status_code == 200:
    #         print("Request successful!")
    #         print("Response:", response.json()["content"])
    # except Exception as e:
    #     print("Error:", e)
    # #print(cleanded_documents)




