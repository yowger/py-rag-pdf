from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rag_pdf.retrieval import search_documents
from rag_pdf.config import CHROMA_DIR

console = Console()

query = "What is Git and why was it created?"

results = search_documents(
    query=query,
    persist_directory=CHROMA_DIR,
    k=4,
)

console.print(
    Panel(
        query,
        title="[bold cyan]Search Query[/bold cyan]",
        border_style="cyan",
    )
)

console.print(f"\n[bold green]Results found:[/bold green] {len(results)}")

for index, document in enumerate(results, start=1):
    console.print(
        Panel(
            document.page_content,
            title=f"[bold blue]Result {index}[/bold blue]",
            subtitle=f"{len(document.page_content)} characters",
            border_style="blue",
        )
    )

    metadata_table = Table(
        title=f"Result {index} Metadata",
        show_header=True,
        header_style="bold magenta",
    )

    metadata_table.add_column("Key", style="cyan", no_wrap=True)
    metadata_table.add_column("Value", style="white", overflow="fold")

    for key, value in document.metadata.items():
        metadata_table.add_row(str(key), str(value))

    console.print(metadata_table)
    console.print()
