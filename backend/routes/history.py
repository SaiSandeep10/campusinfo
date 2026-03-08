# backend/routes/history.py
# Chat history endpoint with MongoDB

from fastapi import APIRouter

router = APIRouter()

# ══════════════════════════════════════════
# GET /api/history
# ══════════════════════════════════════════
@router.get("/history")
async def get_history(session_id: str = "default"):
    """Returns chat history from MongoDB"""
    try:
        from backend.models.chat import get_chat_history
        messages = get_chat_history(session_id)
        return {
            "session_id": session_id,
            "messages": messages,
            "count": len(messages)
        }
    except Exception as e:
        return {
            "session_id": session_id,
            "messages": [],
            "error": str(e)
        }

# ══════════════════════════════════════════
# GET /api/categories
# ══════════════════════════════════════════
@router.get("/categories")
async def get_categories():
    """Returns list of campus information categories"""
    return {
        "categories": [
            {"id": "academics", "label": "Academics", "icon": "📚"},
            {"id": "facilities", "label": "Facilities", "icon": "🏢"},
            {"id": "placements", "label": "Placements", "icon": "💼"},
            {"id": "clubs", "label": "Clubs & Events", "icon": "🎭"},
            {"id": "contacts", "label": "Contacts", "icon": "📞"},
            {"id": "locations", "label": "Campus Map", "icon": "🗺️"},
        ]
    }

# ══════════════════════════════════════════
# GET /api/freshness
# ══════════════════════════════════════════
@router.get("/freshness")
async def get_freshness():
    """Returns content freshness status"""
    try:
        from src.freshness import get_freshness_status
        return get_freshness_status()
    except Exception as e:
        return {"status": "error", "message": str(e)}

