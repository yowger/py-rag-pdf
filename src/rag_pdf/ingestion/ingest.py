from dotenv import load_dotenv

from rag_pdf.ingestion.loader import load_epub
from rag_pdf.ingestion.chunker import chunk_documents
from rag_pdf.indexing.vector_store import create_vector_store
from rag_pdf.config import EPUB_PATH, CHROMA_DIR

load_dotenv()

documents = load_epub(EPUB_PATH)

chunks = chunk_documents(documents)

vector_store = create_vector_store(
    chunks=chunks,
    persist_directory=CHROMA_DIR,
)

print(f"Loaded elements: {len(documents)}")
print(f"Created chunks: {len(chunks)}")
print(f"Stored records: {vector_store._collection.count()}")
