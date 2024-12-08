from concurrent.futures import ThreadPoolExecutor, as_completed

# from loguru import logger
# from typing_extensions import Annotated
# from zenml import get_step_context, step

# from llm_engineering.application import utils
from models.mongoBaseModel import BaseDataModel
from models.documentModels import ArticleDocument, Document, PostDocument, RepoDocument, YoutubeDocument
from clearml import PipelineDecorator, Task


# task = Task.create(
#     project_name="ROS-RAG",
#     task_name="Query Data Warehouse",
#     task_type=Task.TaskTypes.data_processing
# )
def query_data_warehouse():
    results = fetch_all_data()

    # step_context = get_step_context()
    # step_context.add_output_metadata(output_name="raw_documents", metadata=_get_metadata(results))

    return results
#     author_full_names: list[str],
# ) -> Annotated[list, "raw_documents"]:
#     documents = []
#     authors = []
    # for author_full_name in author_full_names:
    #     logger.info(f"Querying data warehouse for user: {author_full_name}")

    #     first_name, last_name = utils.split_user_full_name(author_full_name)
    #     logger.info(f"First name: {first_name}, Last name: {last_name}")
    #     user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)
    #     authors.append(user)

    #     results = fetch_all_data(user)
    #     user_documents = [doc for query_result in results.values() for doc in query_result]

    #     documents.extend(user_documents)

    # step_context = get_step_context()
    # step_context.add_output_metadata(output_name="raw_documents", metadata=_get_metadata(documents))

    # return documents


def fetch_all_data() -> dict[list[BaseDataModel]]:
    #user_id = str(user.id
    docs = []
    with ThreadPoolExecutor() as executor:
        future_to_query = {
            executor.submit(__fetch_articles): "articles",
            # executor.submit(__fetch_posts): "posts",
            executor.submit(__fetch_repositories): "repositories",
            executor.submit(__fetch_youtube): "youtube",

        }

        # In the code snippet provided, `results = {}` is initializing an empty dictionary named
        # `results`. This dictionary will be used to store the results of different queries that are
        # being executed concurrently using a `ThreadPoolExecutor`. Each query result will be stored
        # in this dictionary with a specific key associated with the type of query being executed.
        results = {}
        for future in as_completed(future_to_query):
            query_name = future_to_query[future]
            try:
                results[query_name] = future.result()
                docs.append(results[query_name])
            except Exception:
                #logger.exception(f"'{query_name}' request failed.")

                results[query_name] = []
    return docs


def __fetch_articles() -> list[BaseDataModel]:
    return ArticleDocument.bulk_find()


# def __fetch_posts() -> list[BaseDataModel]:
#     return PostDocument.bulk_find()


def __fetch_repositories() -> list[BaseDataModel]:
    return RepoDocument.bulk_find()
def __fetch_youtube() -> list[BaseDataModel]:
    return YoutubeDocument.bulk_find()


def _get_metadata(documents: list[Document]) -> dict:
    metadata = {
        "num_documents": len(documents),
    }
    for document in documents:
        collection = document.get_collection_name()
        if collection not in metadata:
            metadata[collection] = {}
        # if "authors" not in metadata[collection]:
        #     metadata[collection]["authors"] = list()

        metadata[collection]["num_documents"] = metadata[collection].get("num_documents", 0) + 1
        #metadata[collection]["authors"].append(document.author_full_name)

    # for value in metadata.values():
    #     if isinstance(value, dict) and "authors" in value:
    #         value["authors"] = list(set(value["authors"]))

    return metadata