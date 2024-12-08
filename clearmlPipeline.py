# from clearml.automation import PipelineController
# from steps.crawl import get_links, crawl_links
# from steps.feature import clean_documents, chunk_and_embed
# from feature_engineering.query_datawarehouse import fetch_all_data
# from feature_engineering.load_to_vector_db import load_to_vector_db

# # Define the pipeline
# data_pipeline = PipelineController(
#     name="Data Pipeline",
#     project="ROS-RAG",
#     version="1.0",
#     add_pipeline_tags=["data_sourcing","raw_data_crawling_and_ingestion" ,"clean_chunk_and_embed","app_launch"]
# )

# # Add tasks to the pipeline
# data_pipeline.add_function_step(
#     name="get_links",
#     function=get_links,
#     function_kwargs={
#         "filePath": "urls.txt"
#     }
# )

# data_pipeline.add_function_step(
#     name="crawlAndIngest",
#     function=crawl_links,
#     function_kwargs={
#         "links": "{{get_links.output.links}}"
#     }
# )

# # data_pipeline.add_function_step(
# #     name="load_to_mongodb",
# #     function=load_to_mongodb,
# #     function_kwargs={
# #         "documents": "{{crawlAndIngest.output.documents}}"
# #     }
# # )

# data_pipeline.add_function_step(
#     name="load_from_mongodb",
#     function=fetch_all_data,
#     # function_kwargs={
#     #     "collection_name": "your_collection_name"
#     # }
# )

# data_pipeline.add_function_step(
#     name="clean_documents",
#     function=clean_documents,
#     function_kwargs={
#         "documents": "{{load_from_mongodb.output.documents}}"
#     }
# )

# data_pipeline.add_function_step(
#     name="chunk_and_embed",
#     function=chunk_and_embed,
#     function_kwargs={
#         "cleaned_documents": "{{clean_documents.output.cleaned_documents}}"
#     }
# )

# data_pipeline.add_function_step(
#     name="load_to_vector_db",
#     function=load_to_vector_db,
#     function_kwargs={
#         "embedded_documents": "{{chunk_and_embed.output.embedded_documents}}"
#     }
# )

# # Run the pipeline
# data_pipeline.set_default_execution_queue("default")
# data_pipeline.start_locally()