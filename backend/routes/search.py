# backend/routes/search.py
# Advanced search with filters and faceted retrieval

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.multimedia import search_multimedia
from src.recommendations import get_recommendations

# import lazy loader
from backend.main import get_agent

router = APIRouter()


# ── Request model ──
class SearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    session_id: str = "default"


# ── Response model ──
class SearchResponse(BaseModel):
    answer: str
    query: str
    category: Optional[str]
    timestamp: str
    media: Optional[dict] = None
    recommendations: Optional[list] = None


# ══════════════════════════════════════════
# CATEGORY KEYWORDS
# ══════════════════════════════════════════
CATEGORY_KEYWORDS = {
    "academics": [
        "department", "course", "syllabus", "exam", "result",
        "semester", "attendance", "class", "lecture", "faculty",
        "professor", "hod", "branch", "engineering"
    ],
    "facilities": [
        "library", "canteen", "hostel", "sports", "gym",
        "medical", "wifi", "atm", "bus", "transport",
        "lab", "computer", "infrastructure"
    ],
    "placements": [
        "placement", "job", "company", "recruit", "salary",
        "package", "tpo", "internship", "campus drive",
        "tcs", "wipro", "infosys", "offer"
    ],
    "clubs": [
        "club", "society", "fest", "event", "cultural",
        "technical", "nss", "sports team", "committee",
        "competition", "hackathon", "ideathon"
    ],
    "contacts": [
        "contact", "email", "phone", "number", "address",
        "reach", "call", "office", "cabin", "who is"
    ],
    "locations": [
        "where", "location", "block", "building", "directions",
        "find", "map", "how to reach", "situated", "gate"
    ]
}


# ══════════════════════════════════════════
# AUTO DETECT CATEGORY
# ══════════════════════════════════════════
def detect_category(query: str) -> str:
    query_lower = query.lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        scores[category] = score

    best_category = max(scores, key=scores.get)
    return best_category if scores[best_category] > 0 else "general"


# ══════════════════════════════════════════
# BUILD FILTERED PROMPT
# ══════════════════════════════════════════
def build_filtered_prompt(query: str, category: str) -> str:

    category_context = {
        "academics": "Focus on academic information, departments, courses, faculty.",
        "facilities": "Focus on campus facilities, infrastructure, services.",
        "placements": "Focus on placement cell, companies, packages, TPO.",
        "clubs": "Focus on clubs, societies, events, fests, activities.",
        "contacts": "Focus on contact information, emails, phone numbers.",
        "locations": "Focus on campus locations, directions, buildings.",
        "general": "Provide general campus information."
    }

    context = category_context.get(category, category_context["general"])
    return f"{query} [{context}]"


# ══════════════════════════════════════════
# POST /api/search
# ══════════════════════════════════════════
@router.post("/search", response_model=SearchResponse)
async def advanced_search(body: SearchRequest):

    print(f"\n[SEARCH] Query: {body.query}")

    # detect category
    category = body.category or detect_category(body.query)
    print(f"[SEARCH] Category: {category}")

    filtered_query = build_filtered_prompt(body.query, category)

    # get AI agent (lazy loading)
    chain = get_agent()

    if not chain:
        return SearchResponse(
            answer="AI agent is not available.",
            query=body.query,
            category=category,
            timestamp=datetime.now().isoformat()
        )

    from src.agent import get_response
    answer = get_response(chain, filtered_query)

    # multimedia
    media = None
    try:
        media = search_multimedia(body.query)
    except Exception as e:
        print("Multimedia error:", e)

    # recommendations
    recommendations = get_recommendations(category)

    # save chat
    try:
        from backend.models.chat import save_message, update_session
        save_message(body.session_id, body.query, answer)
        update_session(body.session_id)
    except Exception as e:
        print("MongoDB save failed:", e)

    return SearchResponse(
        answer=answer,
        query=body.query,
        category=category,
        timestamp=datetime.now().isoformat(),
        media=media,
        recommendations=recommendations
    )