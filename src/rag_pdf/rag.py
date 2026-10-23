# from pathlib import Path

# from rag_pdf.path import CHROMA_DIR
# from rag_pdf.retrieval import search_documents


# def answer_question(
#     question: str,
#     persist_directory: Path = CHROMA_DIR,
#     k: int = 4,
# ) -> dict:
#     results = search_documents(
#         query=question,
#         persist_directory=persist_directory,
#         k=k,
#     )

#     documents = [document for document, score in results]

#     if not documents:
#         return {
#             "question": question,
#             "answer": "I couldn't find relevant information.",
#             "sources": [],
#         }

#     context_parts = []

#     for index, document in enumerate(documents, start=1):
#         section = document.metadata.get(
#             "section_path",
#             "Unknown section",
#         )

#         context_parts.append(
#             f"[Source {index}]\n"
#             f"Section: {section}\n"
#             f"{document.page_content}"
#         )

#     context = "\n\n".join(context_parts)

#     answer = generate_answer(
#         question=question,
#         context=context,
#     )

#     return {
#         "question": question,
#         "answer": answer,
#         "sources": [
#             {
#                 "section": document.metadata.get(
#                     "section_path",
#                 ),
#             }
#         ],
#     }
