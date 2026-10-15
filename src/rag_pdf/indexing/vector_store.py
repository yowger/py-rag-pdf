
from pathlib import Path
from langchain_chroma import Chroma
from langchain_core.documents import Document

from rag_pdf.indexing.embeddings import create_embeddings


def create_vector_store(
    chunks: list[Document],
    persist_directory: Path,
) -> Chroma:
    embeddings = create_embeddings()

    vector_store = Chroma(
        collection_name="pro_git",
        embedding_function=embeddings,
        persist_directory=str(persist_directory),
    )

    vector_store.add_documents(chunks)

    return vector_store
