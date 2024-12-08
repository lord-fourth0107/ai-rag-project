from steps.crawl import ingest
import threading
from settings import URL_FILE_PATH
from steps.feature import embed_and_load
from gradio_applet.gradio_app import launch_gradio_app
from flask_app.flaskApp import run_flask
from clearml.automation.controller import PipelineDecorator
from clearml import PipelineController
from clearml import TaskTypes

# @PipelineDecorator.component( cache=True, task_type=TaskTypes.data_processing)
def data_ingestion(filePath:str):
    ingest(filePath)
# @PipelineDecorator.component(name="featureExtraction",cache=True, task_type=TaskTypes.custom)
def feature_extraction():
   embed_and_load()

# @PipelineDecorator.component(name="launch_flask_app",task_type=TaskTypes.custom)
def launch_flask_app():
    run_flask()

# @PipelineDecorator.component(name="launch_gradio_app_call",task_type=TaskTypes.custom)
def launch_gradio_app_call():
    launch_gradio_app()

# app = Flask(__name__)

flask_thread = threading.Thread(target=launch_flask_app)
# @PipelineDecorator.pipeline(name="pipeline",project="ROS-RAG",version="1.0")
def pipeline(filePath:str):
    data_ingestion(filePath)
    feature_extraction()
    flask_thread.start()
    launch_gradio_app()
if __name__ == "__main__":
    # PipelineDecorator.set_default_execution_queue("default")
    # PipelineDecorator.debug_pipeline()
    # pipeline(URL_FILE_PATH)
    # rag_pipeline = PipelineController(
    #     project = "ROS-RAG",
    #     name = "RAG-Pipeline",
    #     version = "1.0",
    #     add_pipeline_tags=False,
    # )
    # rag_pipeline.set_default_execution_queue("default")
    # rag_pipeline.add_parameter(
    #     name="filePath",
    #     default=URL_FILE_PATH,
    # )
    # rag_pipeline.add_function_step(
    #     name="data_ingestion",
    #     function=data_ingestion,
    #     function_kwargs={
    #         "filePath": "{{filePath}}"
    #     }

    # )
    # rag_pipeline.add_function_step(
    #     name="feature_extraction",
    #     function=feature_extraction,
    #     parents=["data_ingestion"],
    # )
    # rag_pipeline.add_function_step(
    #     name="launch_flask_app",
    #     function=launch_flask_app,
    #     parents= ["feature_extraction"],
    # )
    # rag_pipeline.add_function_step(
    #     name="launch_gradio_app_call",
    #     function=launch_gradio_app_call,
    #     parents=["feature_extraction"],
    # )
    # rag_pipeline.start_locally()
    pipeline(URL_FILE_PATH)
    
    




