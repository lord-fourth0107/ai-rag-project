# from clearml import PipelineController
# from steps.crawl import get_links, crawl_links
# from settings import URL_FILE_PATH

# pipeline = PipelineController(
#     name="ClearML Pipeline",
#     project="ROS-RAG",
#     version="1.0",
#     add_pipeline_tags=["data_sourcing","raw_data_crawling_and_ingestion" ,"clean_chunk_and_embed","app_launch"]
# )

# pipeline.add_function_step(
#     name="Step 1: Data sourcing",
#     function=get_links,
#     function_kwargs={
#         "filePath": URL_FILE_PATH
#     }
# )

# pipeline.add_function_step(
#     name="Step 2: Raw data crawling and ingestion",
#     function=crawl_links,
#     function_kwargs={
#         "links": "{{step1.outputs.links}}"
#     }
# )



