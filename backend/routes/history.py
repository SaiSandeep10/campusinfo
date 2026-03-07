# backend/routes/history.py
# Chat history endpoint

from fastapi import APIRouter

router = APIRouter()

# ══════════════════════════════════════════
# GET /api/history
# ══════════════════════════════════════════
@router.get("/history")
async def get_history(session_id: str = "default"):
    """
    Returns chat history for a session.
    Will be connected to MongoDB later!
    """
    # Placeholder for now
    # Will be replaced with MongoDB query
    return {
        "session_id": session_id,
        "messages": [],
        "message": "History feature coming soon with MongoDB!"
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

