
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def build_headings_map(
    documents: list[Document],
) -> dict[str, Document]:
    """Index title elements by their element IDs."""
    return {
        doc.metadata["element_id"]: doc
        for doc in documents
        if doc.metadata.get("category") == "Title"
        and doc.metadata.get("element_id")
    }


def get_heading_path(
    heading_id: str | None,
    headings_by_id: dict[str, Document],
) -> list[str]:
    """Return the heading hierarchy from top level to section."""
    path = []
    visited = set()
    current_id = heading_id

    while current_id and current_id not in visited:
        visited.add(current_id)
        heading = headings_by_id.get(current_id)

        if heading is None:
            break

        path.append(heading.page_content.strip())
        current_id = heading.metadata.get("parent_id")

    path.reverse()
    return path


def format_heading_path(path: list[str]) -> str:
    """Format headings with readable labels."""
    labels = ["Chapter", "Section", "Subsection"]
    lines = []

    for index, heading in enumerate(path):
        if index < len(labels):
            label = labels[index]
        else:
            label = f"Subsection {index - 1}"

        lines.append(f"{label}: {heading}")

    return "\n".join(lines)


def build_section_text(elements: list[Document]) -> str:
    """Combine section elements into readable text."""
    text_parts = []

    for element in elements:
        content = element.page_content.strip()

        if not content:
            continue

        if element.metadata.get("category") == "ListItem":
            content = f"- {content}"

        text_parts.append(content)

    return "\n\n".join(text_parts)


def build_sections(
    documents: list[Document],
    headings_by_id: dict[str, Document],
) -> list[Document]:
    """Group consecutive elements that share a parent heading."""
    sections = []
    current_elements = []
    current_parent_id = None

    def save_section():
        if not current_elements:
            return

        heading_path = get_heading_path(
            current_parent_id,
            headings_by_id,
        )
        section_text = build_section_text(current_elements)

        if not section_text:
            return

        sections.append(
            Document(
                page_content=section_text,
                metadata={
                    "source": current_elements[0].metadata.get(
                        "source", ""
                    ),
                    "section_heading": (
                        heading_path[-1]
                        if heading_path
                        else "Unsectioned"
                    ),
                    "section_path": " > ".join(heading_path),
                    "heading_text": format_heading_path(heading_path),
                },
            )
        )

    for doc in documents:
        if doc.metadata.get("category") == "Title":
            continue

        if not doc.page_content.strip():
            continue

        parent_id = doc.metadata.get("parent_id")

        if current_elements and parent_id != current_parent_id:
            save_section()
            current_elements = []

        current_parent_id = parent_id
        current_elements.append(doc)

    save_section()
    return sections


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[Document]:
    """Build sections, split them, and add heading context."""
    headings_by_id = build_headings_map(documents)
    sections = build_sections(documents, headings_by_id)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )

    chunks = splitter.split_documents(sections)

    for chunk in chunks:
        heading_text = chunk.metadata.get("heading_text", "")

        if heading_text:
            chunk.page_content = (
                f"{heading_text}\n\n{chunk.page_content}"
            )

    return chunks
