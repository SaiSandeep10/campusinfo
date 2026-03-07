# backend/routes/chat.py
# Chat endpoint - handles questions from React frontend

from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# ── Request model ──
class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default"

# ── Response model ──
class AnswerResponse(BaseModel):
    answer: str
    question: str
    timestamp: str
    session_id: str

# ══════════════════════════════════════════
# POST /api/ask
# ══════════════════════════════════════════
@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: Request, body: QuestionRequest):
    """
    Main endpoint - receives question from React,
    sends to AI agent, returns answer
    """
    print(f"\n[API] Question: {body.question}")

    # Get AI chain from app state
    chain = request.app.state.chain

    if not chain:
        return AnswerResponse(
            answer="Sorry, AI agent is not available. Please try again later.",
            question=body.question,
            timestamp=datetime.now().isoformat(),
            session_id=body.session_id
        )

    # Import get_response from agent
    from src.agent import get_response

    # Get answer from AI
    answer = get_response(chain, body.question)

    print(f"[API] Answer: {answer[:100]}...")

    # Save to MongoDB (we'll add this later)
    # await save_to_db(body.question, answer, body.session_id)

    return AnswerResponse(
        answer=answer,
        question=body.question,
        timestamp=datetime.now().isoformat(),
        session_id=body.session_id
    )