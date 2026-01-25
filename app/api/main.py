from fastapi import FastAPI, Depends
from typing import List, Optional
from pydantic import BaseModel

from app.services.qa_service import QAService
from app.core.auth import verify_api_key

app = FastAPI(title="Internal Chatbot")

qa_service = QAService()


class QuestionRequest(BaseModel):
    question: str


class Source(BaseModel):
    document: Optional[str]

class AnswerResponse(BaseModel):
    answer: str
    sources: List[Source]


@app.post("/ask", response_model=AnswerResponse, dependencies=[Depends(verify_api_key)])
def ask_question(req: QuestionRequest):
    return qa_service.answer(req.question)

