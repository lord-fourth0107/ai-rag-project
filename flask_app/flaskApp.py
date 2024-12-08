# flask_app.py
from flask import Flask, request, jsonify
from rag.retriver import ContextRetriever
from feature_engineering.models.embedded_chunks import EmbeddedChunk
from ollama import Client
import requests
import ollama
from settings import OLLAMA_HOST_URL, MODEL_ID

app = Flask(__name__)

@app.route("/getAnswer", methods=['POST','PUT'])
def index():
    """
    The `index` function retrieves context based on a query, sends it to a chatbot model, and returns
    the response.
    :return: The `index` function returns a JSON response containing the content of the response message
    from the OLLAMA chat model. The content of the response message is extracted using
    `response['message']['content']`.
    """
    query = request.get_json().get('query')
    retriever = ContextRetriever(query)
    docs = retriever.search(query)
    context = EmbeddedChunk.to_context(docs)
    client = Client(
    host=OLLAMA_HOST_URL,
    )
    response = ollama.chat(model=MODEL_ID, messages=[
        {
            'role': 'user',
            'content': query,
            'context': context
        },
        ])
    return jsonify({"response":response['message']['content']}) 



    """
    The `run_flask` function starts a Flask application with debugging enabled, reloader disabled, and
    listening on host '0.0.0.0' at port 5303.
    """
def run_flask():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5303)
