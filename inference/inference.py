
from rag.retriver import ContextRetriever
from flask import Flask
import requests

app = Flask(__name__)



@app.route("/")
def index():
    query = requests.args.get('query')
    retriever = ContextRetriever(query) 
if __name__ == "__main__":
    app.run(debug=True)
     

