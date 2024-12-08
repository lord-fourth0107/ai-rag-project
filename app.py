from dataExtraction.crawlers import GitHubCrawler
from steps.crawl import ingest
from feature_engineering.query_datawarehouse import query_data_warehouse
from feature_engineering.load_to_vector_db import load_to_vector_db
import threading
from settings import URL_FILE_PATH
from steps.feature import embed_and_load
from gradio_applet.gradio_app import launch_gradio_app
from flask_app.flaskApp import run_flask


def data_ingestion():
    ingest(URL_FILE_PATH)
def feature_extraction():
   embed_and_load()

def launch_flask_app():
    run_flask()

def launch_gradio_app_call():
    launch_gradio_app()

# app = Flask(__name__)

flask_thread = threading.Thread(target=launch_flask_app)


if __name__ == "__main__":
    data_ingestion()
    feature_extraction()
    flask_thread.start()
    launch_gradio_app()
    




