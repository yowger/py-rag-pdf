
from langchain_core.documents import Document


ALLOWED_METADATA_KEYS = {
    "source",
    "filename",
    "category",
    "element_id",
    "parent_id",
    "start_index",
    # "chapter",
    # "section",
}


def filter_metadata(
    documents: list[Document],
) -> list[Document]:
    filtered_documents = []

    for document in documents:
        metadata = {
            key: value
            for key, value in document.metadata.items()
            if key in ALLOWED_METADATA_KEYS
        }

        filtered_documents.append(
            Document(
                page_content=document.page_content,
                metadata=metadata,
            )
        )

    return filtered_documents
