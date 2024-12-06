from loguru import logger
from typing_extensions import Annotated
# from zenml import step

from utils import misc
from models.vectorBaseModel import BaseVectorDocument


# @step
def load_to_vector_db(
    documents: Annotated[list, "documents"],
) -> Annotated[bool, "successful"]:
    logger.info(f"Loading {len(documents)} documents into the vector database.")

    grouped_documents = BaseVectorDocument.group_by_class(documents)
    for document_class, documents in grouped_documents.items():
        logger.info(f"Loading documents into {document_class.get_collection_name()}")
        for documents_batch in misc.batch(documents, size=4):
            try:
                print(documents_batch)
                document_class.bulk_insert(documents_batch)
            except Exception as e:
                logger.error(f"Failed to insert documents into {document_class.get_collection_name() }due to {e}")

                return False

    return True