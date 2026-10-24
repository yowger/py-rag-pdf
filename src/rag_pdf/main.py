from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_pdf.chain import answer_question, stream_answer

app = FastAPI(
    title="Pro Git RAG",
    description="A chatbot for retrieving information from Pro Git book epub file.",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.post("/chat/stream")
def chat_stream(request: AskRequest):
    return StreamingResponse(
        stream_answer(request.question),
        media_type="text/plain; charset=utf-8",
    )
