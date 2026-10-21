from rag_pdf.path import EPUB_PATH
from rag_pdf.ingestion.loader import load_epub
from rag_pdf.ingestion.print_doc import print_documents, print_document_stats, print_short_documents


documents = load_epub(EPUB_PATH)

# for index, document in enumerate(documents):
#     if document.page_content.strip() == "Speed":
#         start = max(0, index - 2)
#         end = min(len(documents), index + 5)

#         for i in range(start, end):
#             item = documents[i]

#             print(f"\n--- Document {i} ---")
#             print("Text:", repr(item.page_content[:300]))
#             print("Category:", item.metadata.get("category"))
#             print("Element ID:", item.metadata.get("element_id"))
#             print("Parent ID:", item.metadata.get("parent_id"))

#         break


# print("---")


# for index, document in enumerate(documents):
#     if document.metadata.get("category") == "Title":
#         print(
#             index,
#             repr(document.page_content[:100]),
#             document.metadata.get("element_id"),
#             document.metadata.get("parent_id"),
#         )

element_by_id = {
    document.metadata.get("element_id"): document
    for document in documents
}

for index in range(50, 66):
    document = documents[index]

    parent_id = document.metadata.get("parent_id")
    parent = element_by_id.get(parent_id)

    print(f"\n--- Element {index} ---")
    print("Category:", document.metadata.get("category"))
    print("Text:", repr(document.page_content[:150]))
    print(
        "Parent heading:",
        repr(parent.page_content if parent else None),
    )

# print_document_stats(documents)
# print_short_documents(documents)
# print_documents(
#     documents=documents,
#     limit=5,
#     title="Git book"
# )
