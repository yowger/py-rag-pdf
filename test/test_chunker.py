
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rag_pdf.ingestion.loader import load_epub
from rag_pdf.ingestion.chunker import chunk_documents
from rag_pdf.path import EPUB_PATH

console = Console()

documents = load_epub(EPUB_PATH)
chunks = chunk_documents(documents)

console.print(f"[green]Original elements:[/green] {len(documents)}")
console.print(f"[cyan]Chunks created:[/cyan] {len(chunks)}")

for index, chunk in enumerate(chunks[:5], start=1):
    console.print(
        Panel(
            chunk.page_content,
            title=f"Chunk {index}",
            subtitle=f"{len(chunk.page_content)} characters",
            border_style="blue",
        )
    )

    metadata_table = Table(
        title=f"Chunk {index} Metadata",
        show_header=True,
        header_style="bold magenta",
    )

    metadata_table.add_column("Key", style="cyan", no_wrap=True)
    metadata_table.add_column("Value", style="white", overflow="fold")

    for key, value in chunk.metadata.items():
        metadata_table.add_row(str(key), str(value))

    console.print(metadata_table)
    console.print()
