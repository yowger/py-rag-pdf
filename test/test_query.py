from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rag_pdf.retrieval import search_documents
from rag_pdf.config import CHROMA_DIR

console = Console()

# query = "Whats Git"
# query = "Whats is version control"
# query = "How does distributed version control differ from centralized version control?"
# query = "What are the disadvantages of centralized version control?"

TEST_QUESTIONS = [
    {
        "question": "What is version control, and why is it useful?",
        "expected_topic": "About Version Control",
    },
    {
        "question": "What are the disadvantages of centralized version control?",
        "expected_topic": "Centralized Version Control Systems",
    },
    {
        "question": "How does distributed version control differ from centralized version control?",
        "expected_topic": "Distributed",
    },
    {
        "question": "What is a single point of failure in version control?",
        "expected_topic": "Centralized Version Control Systems",
    },
    {
        "question": "What is the difference between local and centralized version control?",
        "expected_topic": "Version Control",
    },
]

for item in TEST_QUESTIONS:
    question = item["question"]
    expected_topic = item["expected_topic"]

    results = search_documents(
        query=question,
        persist_directory=CHROMA_DIR,
        k=4,
        # k=2,
    )

    console.print(
        Panel(
            question,
            title="[bold cyan]Search Query[/bold cyan]",
            border_style="cyan",
        )
    )

    console.print(f"\n[/bold green]expected answer:[/bold green] {expected_topic}")
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
