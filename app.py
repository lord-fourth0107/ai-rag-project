from steps.crawl import ingest
import importlib
import threading
from settings import URL_FILE_PATH
from steps.feature import embed_and_load
from gradio_applet.gradio_app import launch_gradio_app
from flask_app.flaskApp import run_flask
from clearml.automation.controller import PipelineDecorator
from clearml import PipelineController
from clearml import Task
pipelinetask = Task.init(
            project_name='ROS-RAG', 
            task_name='RAG-Pipeline',
        )
# @PipelineDecorator.component( cache=True, task_type=TaskTypes.data_processing)
def data_ingestion(filePath:str):
    extraction_task = Task.create(
            project_name='ROS-RAG',
            task_name='Data Extraction',
            # parent=pipelinetask,
    )
    ingest_module = importlib.import_module('steps.crawl')
    ingest_module.ingest(filePath)
# @PipelineDecorator.component(name="featureExtraction",cache=True, task_type=TaskTypes.custom)
def feature_extraction():
   feature_extraction_task = Task.create(
            project_name='ROS-RAG',
            task_name='Feature Extraction',
            # parent=pipelinetask,        
   )
   feature_extraction_module = importlib.import_module('steps.feature')
   feature_extraction_module.embed_and_load()

# @PipelineDecorator.component(name="launch_flask_app",task_type=TaskTypes.custom)
def launch_flask_app():
    launch_flask_app_task = Task.create(
            project_name='ROS-RAG',
            task_name='Flask App',
            # parent=pipelinetask,
    )
    launch_flask_app_module = importlib.import_module('flask_app')
    launch_flask_app_module.run_flask()

# @PipelineDecorator.component(name="launch_gradio_app_call",task_type=TaskTypes.custom)
def launch_gradio_app_call():
    launch_gradio_app_task = Task.create(
            project_name='ROS-RAG',
            task_name='Gradio App',
            # parent=pipelinetask,    
    )
    launch_gradio_app_module = importlib.import_module('gradio_applet') 
    launch_gradio_app_module.gradio_app()

# app = Flask(__name__)

flask_thread = threading.Thread(target=launch_flask_app)
# @PipelineDecorator.pipeline(name="pipeline",project="ROS-RAG",version="1.0")
def pipeline(filePath:str):
    data_ingestion(filePath)
    feature_extraction()
    flask_thread.start()
    launch_gradio_app()
if __name__ == "__main__":
    PipelineDecorator.set_default_execution_queue("default")
    PipelineDecorator.debug_pipeline()
    pipeline(URL_FILE_PATH)
    rag_pipeline = PipelineController(
        project = "ROS-RAG",
        name = "RAG-Pipeline",
        version = "1.0",
        add_pipeline_tags=False,
    )
    rag_pipeline.set_default_execution_queue("default")
    rag_pipeline.add_parameter(
        name="filePath",
        default=URL_FILE_PATH,
    )
    rag_pipeline.add_function_step(
        name="data_ingestion",
        function=data_ingestion,
        function_kwargs={
            "filePath": "{{filePath}}"
        }

    )
    rag_pipeline.add_function_step(
        name="feature_extraction",
        function=feature_extraction,
        parents=["data_ingestion"],
    )
    rag_pipeline.add_function_step(
        name="launch_flask_app",
        function=launch_flask_app,
        parents= ["feature_extraction"],
    )
    rag_pipeline.add_function_step(
        name="launch_gradio_app_call",
        function=launch_gradio_app_call,
        parents=["feature_extraction"],
    )
    rag_pipeline.start_locally()
    #pipeline(URL_FILE_PATH)
    
    




