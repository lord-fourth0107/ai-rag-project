# from clearml.automation import PipelineController
# from steps.crawl import get_links, crawl_links
# from steps.feature import clean_documents, chunk_and_embed
# from feature_engineering.load_to_vector_db import load_to_vector_db
# from feature_engineering.query_datawarehouse import query_data_warehouse
# from settings import URL_FILE_PATH

# feature_pipeline = PipelineController(
#     name="Feature Engineering",
#     project="ROS-RAG",
#     version="1.0",
#     add_pipeline_tags=["data_sourcing","raw_data_crawling_and_ingestion" ,"clean_chunk_and_embed","app_launch"]
# )


# feature_pipeline.add_function_step(
#     name="getlinks",
#     function=get_links,
#     function_return=['links'],
#     function_kwargs={
#         "filePath": URL_FILE_PATH
#     }
    
# )
# feature_pipeline.add_function_step(
#     name="crawlAndIngest",
#     function=crawl_links,
#     function_kwargs={
#         "links": '${getlinks.links}'
#     }
   
# )
# feature_pipeline.add_function_step(
#     name="queryDataWarehouse",
#     function=query_data_warehouse,
#     parents=['crawlAndIngest'] ,
#     function_return = ['raw_documents']
# )
# feature_pipeline.add_function_step(
#     name="cleanDocuments",
#     function=clean_documents,
#     function_return=['cleaned_documents'],
#     function_kwargs={
#         "crawled_links": '${queryDataWarehouse.raw_documents}'
#     }
   
# )

# feature_pipeline.add_function_step(
#     name="chunkAndEmbed",
#     function=chunk_and_embed,
#     function_return=['embedded_documents'],
#     function_kwargs={
#         "cleaned_documents": '${cleanDocuments.cleaned_documents}'
#     }
   
# )
# feature_pipeline.add_function_step(
#     name="loadToVectorDB",
#     function=load_to_vector_db,
#     function_kwargs={
#         "embedded_documents": '${chunkAndEmbed.embedded_documents}'
#     }
   
# )
# feature_pipeline.set_default_execution_queue("default")
# feature_pipeline.start_locally()



