
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rag_pdf.ingestion.loader import load_epub

console = Console()

PROJECT_ROOT = next(
    p for p in Path(__file__).resolve().parents
    if (p / ".git").exists()
)

epub_file = PROJECT_ROOT / "data" / "documents" / "progit.epub"

documents = load_epub(epub_file)
documents = load_epub(epub_file)


console.print(
    f"\n[bold green]Elements loaded:[/bold green] {len(documents)}\n"
)

for index, document in enumerate(documents[:20], start=20):
    metadata_table = Table(
        title=f"Document {index} Metadata",
        show_header=True,
        header_style="bold cyan",
    )
    metadata_table.add_column("Key", style="yellow")
    metadata_table.add_column("Value", style="white")

    for key, value in document.metadata.items():
        metadata_table.add_row(str(key), str(value))

    console.print(metadata_table)

    content = document.page_content[:500]

    console.print(
        Panel(
            content or "[dim]Empty document[/dim]",
            title=f"[bold blue]Document {index} Content[/bold blue]",
            subtitle=f"{len(document.page_content)} characters total",
            border_style="blue",
            expand=False,
        )
    )

    console.print()
