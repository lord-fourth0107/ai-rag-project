# flask_app.py
from flask import Flask, request, jsonify
from rag.retriver import ContextRetriever
from feature_engineering.models.embedded_chunks import EmbeddedChunk
from ollama import Client
import requests
import ollama

app = Flask(__name__)

@app.route("/getAnswer", methods=['POST','PUT'])
def index():
    query = request.get_json().get('query')
    retriever = ContextRetriever(query)
    docs = retriever.search(query)
    context = EmbeddedChunk.to_context(docs)
    client = Client(
    host='http://localhost:11434',
    )
    response = ollama.chat(model='hf.co/nsh22/ROS-gguf', messages=[
        {
            'role': 'user',
            'content': query,
            'context': context
        },
        ])
    return jsonify({"response":response['message']['content']}) 



def run_flask():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5303)
