# backend/routes/history.py
# Chat history + freshness endpoints

from fastapi import APIRouter

router = APIRouter()


# ══════════════════════════════════════════
# GET /api/history
# ══════════════════════════════════════════
@router.get("/history")
async def get_history(session_id: str = "default"):
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
    return {
        "categories": [
            {"id": "academics",  "label": "Academics",  "icon": "📚"},
            {"id": "facilities", "label": "Facilities", "icon": "🏢"},
            {"id": "placements", "label": "Placements", "icon": "💼"},
            {"id": "clubs",      "label": "Clubs",      "icon": "🎭"},
            {"id": "contacts",   "label": "Contacts",   "icon": "📞"},
            {"id": "locations",  "label": "Locations",  "icon": "🗺️"},
        ]
    }


# ══════════════════════════════════════════
# GET /api/freshness
# ══════════════════════════════════════════
@router.get("/freshness")
async def get_freshness():
    try:
        from src.freshness import get_freshness_status
        return get_freshness_status()
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# ══════════════════════════════════════════
# GET /api/analytics
# ══════════════════════════════════════════
@router.get("/analytics")
async def get_analytics():
    """Returns comprehensive analytics report"""
    try:
        from src.analytics import get_full_analytics
        return get_full_analytics()
    except Exception as e:
        return {"error": str(e)}


# ══════════════════════════════════════════
# GET /api/analytics/popular
# ══════════════════════════════════════════
@router.get("/analytics/popular")
async def get_popular():
    """Returns most popular questions"""
    try:
        from src.analytics import get_popular_queries
        return {"popular_queries": get_popular_queries(10)}
    except Exception as e:
        return {"error": str(e)}


# ══════════════════════════════════════════
# GET /api/analytics/gaps
# ══════════════════════════════════════════
@router.get("/analytics/gaps")
async def get_gaps():
    """Returns information gaps"""
    try:
        from src.analytics import get_information_gaps
        return {"information_gaps": get_information_gaps(10)}
    except Exception as e:
        return {"error": str(e)}