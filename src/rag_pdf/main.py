from fastapi import FastAPI
from pydantic import BaseModel

from rag_pdf.chain import answer_question

app = FastAPI(
    title="Pro Git RAG",
    description="A chatbot for retrieving information from Pro Git book epub file.",
)


class AskRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(request: AskRequest):
    answer = answer_question(request.question)

    return {
        "question": request.question,
        "answer": answer,
    }
