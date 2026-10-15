
from pathlib import Path

from rag_pdf.ingestion.loader import load_epub

PROJECT_ROOT = next(p for p in Path(
    __file__).resolve().parents if (p / '.git').exists())
epub_file = PROJECT_ROOT / "data" / "documents" / "progit.epub"

documents = load_epub(epub_file)

print(f"Elements loaded: {len(documents)}")

for document in documents[:5]:
    print("\n--- DOCUMENT ---")
    print(document.page_content[:500])
    print(document.metadata)
