from pathlib import Path
from langchain_community.document_loaders import UnstructuredEPubLoader
from langchain_core.documents import Document


def load_epub(epub_path: Path) -> list[Document]:
    if not epub_path.is_file():
        raise FileNotFoundError(f"EPUB not found: {epub_path}")

    loader = UnstructuredEPubLoader(
        str(epub_path),
        mode="elements",
    )

    documents = loader.load()

    return documents
