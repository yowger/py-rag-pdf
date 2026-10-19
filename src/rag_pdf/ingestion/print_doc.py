from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich import box
from langchain_core.documents import Document
from collections import Counter, defaultdict

console = Console()


def print_documents(
    documents: list[Document],
    title: str = "Documents",
    limit: int = 5,
    show_content: bool = True,
) -> None:
    if limit < 0:
        raise ValueError("limit must be zero or greater")

    console.print()
    console.rule(f"[bold cyan]{title}[/bold cyan]")

    displayed_count = min(limit, len(documents))

    console.print(
        f"[dim]Showing {displayed_count} of "
        f"{len(documents)} documents[/dim]\n"
    )

    for index, document in enumerate(documents[:limit], start=1):
        content = document.page_content or "Empty content"

        if show_content:
            console.print(
                Panel(
                    content,
                    title=f"[bold green]Document {index}[/bold green]",
                    subtitle=f"{len(document.page_content)} characters",
                    border_style="green",
                    box=box.ROUNDED,
                )
            )

        metadata_table = Table(
            title=f"Document {index} Metadata",
            box=box.ROUNDED,
            show_lines=True,
        )

        metadata_table.add_column("Key", style="cyan", no_wrap=True)
        metadata_table.add_column("Value", style="white", overflow="fold")

        if document.metadata:
            for key, value in document.metadata.items():
                metadata_table.add_row(str(key), str(value))
        else:
            metadata_table.add_row("Metadata", "[dim]No metadata[/dim]")

        console.print(metadata_table)
        console.print()

    console.print(f"[bold]Total documents:[/bold] {len(documents)}")


def print_document_stats(documents: list[Document]) -> None:
    lengths = [len(doc.page_content) for doc in documents]

    console.print("\n[bold cyan]Document Statistics[/bold cyan]")
    console.print(f"Total documents: {len(documents)}")
    console.print(f"Empty documents: {sum(n == 0 for n in lengths)}")
    console.print(f"Under 50 characters: {sum(n < 50 for n in lengths)}")
    console.print(f"Under 200 characters: {sum(n < 200 for n in lengths)}")
    console.print(f"Over 1000 characters: {sum(n > 1000 for n in lengths)}")

    categories = Counter(
        doc.metadata.get("category", "Unknown")
        for doc in documents
    )

    console.print("\n[bold cyan]Categories[/bold cyan]")

    for category, count in categories.most_common():
        console.print(f"{category}: {count}")


def print_short_documents(
    documents: list[Document],
    max_length: int = 50,
    limit_per_category: int = 10,
) -> None:
    if max_length < 0:
        raise ValueError("max_length must be zero or greater")

    if limit_per_category < 0:
        raise ValueError("limit_per_category must be zero or greater")

    short_documents = defaultdict(list)

    for document in documents:
        content = document.page_content.strip()

        if len(content) < max_length:
            category = document.metadata.get("category", "Unknown")
            short_documents[category].append(document)

    console.print("\n[bold cyan]Short Documents[/bold cyan]")

    for category, category_documents in sorted(short_documents.items()):
        console.print(
            f"\n[bold yellow]--- {category}: "
            f"{len(category_documents)} ---[/bold yellow]"
        )

        for document in category_documents[:limit_per_category]:
            console.print(
                Panel(
                    repr(document.page_content.strip()),
                    subtitle=f"{len(document.page_content.strip())} characters",
                    box=box.ROUNDED,
                )
            )
