from typing_extensions import Annotated
from feature_engineering.preprocessing.dispatcher import CleaningDispatcher, ChunkingDispatcher
from models.documentModels import Document, RepoDocument, PostDocument
from embedding.embeddings_dispatcher import EmbeddingDispatcher
from utils import misc
def clean_documents(
    documents: Annotated[list, "raw_documents"],
) -> Annotated[list, "cleaned_documents"]:
    cleaned_documents = []
    for document_str in documents:
        
        #document = PostDocument(content=document_str.content, platform=document_str.platform, name=document_str.name, link=document_str.link)
        cleaned_document = CleaningDispatcher.dispatch(document_str)
        cleaned_documents.append(cleaned_document)

    # step_context = get_step_context()
    # step_context.add_output_metadata(output_name="cleaned_documents", metadata=_get_metadata(cleaned_documents))

    return cleaned_documents
def chunk_and_embed(
    cleaned_documents: Annotated[list, "cleaned_documents"],
) -> Annotated[list, "embedded_documents"]:
    metadata = {"chunking": {}, "embedding": {}, "num_documents": len(cleaned_documents)}

    embedded_chunks = []
    for document in cleaned_documents:
        chunks = ChunkingDispatcher.dispatch(document)
       #metadata["chunking"] = _add_chunks_metadata(chunks, metadata["chunking"])

        for batched_chunks in misc.batch(chunks, 10):
            batched_embedded_chunks = EmbeddingDispatcher.dispatch(batched_chunks)
            embedded_chunks.extend(batched_embedded_chunks)

    # metadata["embedding"] = _add_embeddings_metadata(embedded_chunks, metadata["embedding"])
    # metadata["num_chunks"] = len(embedded_chunks)
    # metadata["num_embedded_chunks"] = len(embedded_chunks)

    # step_context = get_step_context()
    # step_context.add_output_metadata(output_name="embedded_documents", metadata=metadata)

    return embedded_chunks
