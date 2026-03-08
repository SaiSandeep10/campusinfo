# backend/routes/chat.py
# Main chat endpoint

from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime

from src.agent_manager import get_agent
from src.agent import get_response

router = APIRouter()


# --------------------------------------------------
# Request Model
# --------------------------------------------------
class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


# --------------------------------------------------
# Response Model
# --------------------------------------------------
class ChatResponse(BaseModel):
    answer: str
    question: str
    timestamp: str
    session_id: str


# --------------------------------------------------
# POST /api/ask
# --------------------------------------------------
@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: Request, body: ChatRequest):

    print("\n[API] Question:", body.question)

    # Load AI agent (lazy loading)
    chain = get_agent()

    # Generate response from AI
    answer = get_response(chain, body.question)

    # Save chat history to MongoDB
    try:
        from backend.models.chat import save_message, update_session

        save_message(body.session_id, body.question, answer)
        update_session(body.session_id)

    except Exception as e:
        print("⚠ MongoDB save failed:", e)

    return ChatResponse(
        answer=answer,
        question=body.question,
        timestamp=datetime.now().isoformat(),
        session_id=body.session_id
    )