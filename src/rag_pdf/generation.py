
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


SYSTEM_PROMPT = """
You answer questions about Git using the supplied context.

- Use only information supported by the context.
- If the context does not contain enough information, say so.
- Do not invent facts.
- Cite the source numbers used, such as [Source 1].
"""


def generate_answer(question: str, context: str) -> str:
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

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    chain = prompt | model | StrOutputParser()

    return chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )
