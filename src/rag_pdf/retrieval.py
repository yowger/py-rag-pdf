from pathlib import Path

from langchain_chroma import Chroma

from rag_pdf.indexing.embeddings import create_embeddings
from rag_pdf.path import CHROMA_DIR


def get_vector_store(persist_directory: Path = CHROMA_DIR) -> Chroma:
    return Chroma(
        collection_name="pro_git",
        embedding_function=create_embeddings(),
        persist_directory=str(persist_directory),
    )


def search_documents(
    query: str,
    persist_directory: Path,
    k: int = 4,
):
    vector_store = get_vector_store(persist_directory)

    # return vector_store.similarity_search(query, k=k)
    return vector_store.similarity_search_with_score(query, k=k)
