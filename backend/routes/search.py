# backend/routes/search.py
# Advanced search with filters and faceted retrieval

from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.multimedia import search_multimedia
from src.recommendations import get_recommendations

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
    """Auto detect category from query keywords"""
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
    """Add category context to query for better results"""
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
async def advanced_search(request: Request, body: SearchRequest):

    print(f"\n[SEARCH] Query: {body.query}")

    # Detect category
    category = body.category or detect_category(body.query)
    print(f"[SEARCH] Category: {category}")

    # Build prompt
    filtered_query = build_filtered_prompt(body.query, category)

    chain = request.app.state.chain
    if not chain:
        return SearchResponse(
            answer="Sorry, AI agent is not available.",
            query=body.query,
            category=category,
            timestamp=datetime.now().isoformat()
        )

    from src.agent import get_response
    answer = get_response(chain, filtered_query)

    # Multimedia
    media = None
    try:
        media = search_multimedia(body.query)
    except Exception as e:
        print("Multimedia error:", e)

    # Recommendations
    recommendations = get_recommendations(category)

    # Save chat
    try:
        from backend.models.chat import save_message, update_session
        save_message(body.session_id, body.query, answer)
        update_session(body.session_id)
    except Exception as e:
        print(f"⚠ MongoDB save failed: {e}")

    return SearchResponse(
        answer=answer,
        query=body.query,
        category=category,
        timestamp=datetime.now().isoformat(),
        media=media,
        recommendations=recommendations
    )

# ══════════════════════════════════════════
# GET /api/search/suggestions
# ══════════════════════════════════════════
@router.get("/search/suggestions")
async def get_suggestions(category: str = "general"):
    """Returns suggested questions per category"""
    suggestions = {
        "academics": [
            "What departments are available in ANITS?",
            "Who is the HOD of CSE department?",
            "What is the exam schedule?"
        ],
        "facilities": [
            "Where is the library located?",
            "What are canteen timings?",
            "Is there a hostel facility?"
        ],
        "placements": [
            "What companies visit ANITS for placements?",
            "What is the average placement package?",
            "Who is the TPO of ANITS?"
        ],
        "clubs": [
            "What clubs are available in ANITS?",
            "When is TechNova fest?",
            "How to join NSS?"
        ],
        "contacts": [
            "What is the principal email?",
            "How to contact the placement cell?",
            "What is the college phone number?"
        ],
        "locations": [
            "Where is the placement cell?",
            "How to reach the canteen?",
            "Where is the boys hostel?"
        ],
        "general": [
            "Tell me about ANITS college",
            "What is ANITS known for?",
            "How to apply for admission?"
        ]
    }

    return {
        "category": category,
        "suggestions": suggestions.get(category, suggestions["general"])
    }