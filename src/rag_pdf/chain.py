from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from rag_pdf.config import get_settings
from rag_pdf.retrieval import get_vector_store

settings = get_settings()

SYSTEM_PROMPT = """
You answer questions about Git using the supplied context.

- Use only information supported by the context.
- If the context does not contain enough information, say so.
- Do not invent facts.
- Cite the source numbers used, such as [Source 1].
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            "Context:\n{context}\n\n"
            "Question: {question}",
        ),
    ]
)


def format_docs(docs: list[Document]) -> str:
    """Format retrieved Document"""
    context_parts: list[str] = []

    for index, document in enumerate(docs, start=1):
        section = document.metadata.get("section_path")
        source = f"[Source {index}]"

        if section:
            source += f"\nSection: {section}"

        context_parts.append(
            f"{source}\n{document.page_content}"
        )

    return "\n\n".join(context_parts)


llm = ChatOpenAI(
    model=settings.answer_model,
    temperature=0,
    api_key=settings.openai_api_key,
)

retriever = get_vector_store().as_retriever(
    search_kwargs={"k": 4},
)

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)


def answer_question(question: str) -> str:
    return rag_chain.invoke(question)


answer = answer_question(
    "What is the difference between git stash apply and git stash pop?"
)

print(answer)
