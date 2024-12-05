from dataExtraction.crawlers import GitHubCrawler
from steps.crawl import crawl_links
from feature_engineering.query_datawarehouse import query_data_warehouse
from feature_engineering.load_to_vector_db import load_to_vector_db
from steps.feature import clean_documents, chunk_and_embed
from transformers import AutoTokenizer, AutoModelForCausalLM
from ollama import Client
from flask import Flask,jsonify,request
import requests
import ollama
from feature_engineering.models.embedded_chunks import EmbeddedChunk
# from clearml import Task
# task = Task.init(project_name="ROS-RAG", task_name="RAG-App")
# model_name = "meta-llama/Llama-2-7b"

from rag.retriver import ContextRetriever
app = Flask(__name__)
def openFile():
    file = open("urls.txt", "r")
    urls = file.readlines()
    file.close()    
    return urls
@app.route("/getAnswer", methods=['POST','PUT'])
def index():
    query = request.get_json().get('query')
    retriever = ContextRetriever(query)
    docs = retriever.search(query)
    context = EmbeddedChunk.to_context(docs)
    client = Client(
    host='http://localhost:11434',
    )
    response = client.chat(model='llama3:latest', messages=[
        {
            'role': 'user',
            'content': query,
            'context': context
        },
        ])
    print(response['message']['content'])
    #print(response.to_dict())
    return jsonify({"response":response['message']['content']}) 


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
    # contextRetriver = ContextRetriever(mock=True)
    # docs = contextRetriver.search("what is ros2")
    # context = EmbeddedChunk.to_context(docs)
    
    
    # print(response)
    app.run(debug=True)





