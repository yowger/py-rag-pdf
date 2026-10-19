from dotenv import load_dotenv

from rag_pdf.config import EPUB_PATH, CHROMA_DIR
from rag_pdf.ingestion.loader import load_epub
# from rag_pdf.ingestion.print_doc import print_documents
from rag_pdf.ingestion.chunker import chunk_documents
from rag_pdf.indexing.vector_store import create_vector_store

load_dotenv()

documents = load_epub(EPUB_PATH)


chunks = chunk_documents(documents)

# print_documents(
#     chunks,
#     title="Grouped Documents",
#     limit=20,
# )

vector_store = create_vector_store(
    chunks=chunks,
    persist_directory=CHROMA_DIR,
)

print(f"Loaded elements: {len(documents)}")
print(f"Created chunks: {len(chunks)}")
