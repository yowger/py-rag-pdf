import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from rag_pdf.chain import answer_question, stream_answer

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


@app.post("/chat/stream")
def chat_stream(request: AskRequest):
    def generate():
        for chunk in stream_answer(request.question):
            event = json.dumps({"text": chunk})
            yield f"data: {event}\n\n"

        yield 'data: {"done": true}\n\n'

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )
