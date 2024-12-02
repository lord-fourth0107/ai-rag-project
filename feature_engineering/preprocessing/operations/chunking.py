import re

from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from langchain.text_splitter import TokenTextSplitter
from embedding.embeddings import EmbeddingModelSingleton
from transformers import AutoTokenizer

embedding_model = EmbeddingModelSingleton()
     


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    character_splitter = RecursiveCharacterTextSplitter(separators=["\n"], chunk_size=chunk_size, chunk_overlap=0)
    text_split_by_characters = character_splitter.split_text(text)
    text_splitter = TokenTextSplitter( chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # token_splitter = SentenceTransformersTokenTextSplitter(
    #     chunk_overlap=chunk_overlap,
    #     tokens_per_chunk=embedding_model.max_input_length,
    #     model_name=embedding_model.model_id,
    # )
    chunks_by_tokens = []
    for section in text_split_by_characters:
        chunks_by_tokens.extend(text_splitter.split_text(section))

    return chunks_by_tokens


def chunk_document(text: str, min_length: int, max_length: int) -> list[str]:
    """Alias for chunk_article()."""

    return chunk_article(text, min_length, max_length)


def chunk_article(text: str, min_length: int, max_length: int) -> list[str]:
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", text)

    extracts = []
    current_chunk = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + " "
        else:
            if len(current_chunk) >= min_length:
                extracts.append(current_chunk.strip())
            current_chunk = sentence + " "

    if len(current_chunk) >= min_length:
        extracts.append(current_chunk.strip())

    return extracts
class CustomTokenTextSplitter(SentenceTransformersTokenTextSplitter):
    def __init__(self, tokenizer, chunk_overlap=0, tokens_per_chunk=500, **kwargs):
        # Handle tokenizer locally
        self.tokenizer = tokenizer
        # Pass only supported arguments to the parent class
        super().__init__(chunk_overlap=chunk_overlap, tokens_per_chunk=tokens_per_chunk, **kwargs)
