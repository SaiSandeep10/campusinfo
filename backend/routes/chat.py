# backend/routes/chat.py
# Chat endpoint with MongoDB integration

from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime
import uuid

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
    sends to AI agent, saves to MongoDB, returns answer
    """
    print(f"\n[API] Question: {body.question}")

    # Get AI chain from app state
    chain = request.app.state.chain

    if not chain:
        return AnswerResponse(
            answer="Sorry AI agent is not available. Please try again later.",
            question=body.question,
            timestamp=datetime.now().isoformat(),
            session_id=body.session_id
        )

    # Get answer from AI
    from src.agent import get_response
    answer = get_response(chain, body.question)

    # Save to MongoDB
    try:
        from backend.models.chat import save_message, create_session, update_session
        create_session(body.session_id)
        save_message(body.session_id, body.question, answer)
        update_session(body.session_id)
        print(f"  ✓ Saved to MongoDB")
    except Exception as e:
        print(f"  ⚠️ MongoDB save failed: {e}")

    print(f"[API] Answer: {answer[:100]}...")

    return AnswerResponse(
        answer=answer,
        question=body.question,
        timestamp=datetime.now().isoformat(),
        session_id=body.session_id
    )