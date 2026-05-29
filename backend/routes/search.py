# backend/routes/search.py
# Advanced search with filters

from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.agent import get_response
from src.cache import get_cached_response, save_to_cache
from src.recommendations import get_personalized_recommendations, get_related_questions

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
        "department", "course", "syllabus", "exam",
        "result", "semester", "faculty", "hod"
    ],
    "facilities": [
        "library", "canteen", "hostel", "wifi",
        "sports", "gym", "medical"
    ],
    "placements": [
        "placement", "package", "company",
        "job", "internship", "tpo"
    ],
    "clubs": [
        "club", "event", "fest",
        "competition", "hackathon"
    ],
    "contacts": [
        "contact", "email", "phone",
        "number", "office"
    ],
    "locations": [
        "where", "location", "map",
        "block", "building", "gate"
    ]
}


# ══════════════════════════════════════════
# CATEGORY DETECTION
# ══════════════════════════════════════════
def detect_category(query: str) -> str:
    query_lower = query.lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for word in keywords if word in query_lower)
        scores[category] = score
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"


# ══════════════════════════════════════════
# FILTERED QUERY BUILDER
# ══════════════════════════════════════════
def build_filtered_query(query: str, category: str) -> str:
    context_map = {
        "academics": "Focus on academic information, departments, courses and faculty.",
        "facilities": "Focus on campus facilities like library, canteen, hostel and sports.",
        "placements": "Focus on placement cell, companies visiting, packages and TPO.",
        "clubs": "Focus on clubs, societies, events and fests.",
        "contacts": "Focus on contact details, emails and phone numbers.",
        "locations": "Focus on campus locations, directions and buildings.",
        "general": "Provide general campus information about ANITS."
    }
    context = context_map.get(category, context_map["general"])
    return f"{query}. {context}"


# ══════════════════════════════════════════
# MEDIA HELPER
# ══════════════════════════════════════════
def get_media(category: str) -> dict:
    media_map = {
        "locations": {
            "map": "https://maps.google.com/?q=ANITS+Visakhapatnam"
        },
        "facilities": {
            "images": ["https://www.anits.edu.in/images/library.jpg"]
        },
    }
    return media_map.get(category, {})


# ══════════════════════════════════════════
# RECOMMENDATIONS HELPER
# ══════════════════════════════════════════
def get_recommendations(category: str) -> list:
    suggestions = {
        "academics": [
            "Who is the HOD of CSE department?",
            "What courses are offered at ANITS?",
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
            "What departments are available?",
            "How to apply for admission?"
        ]
    }
    return suggestions.get(category, suggestions["general"])


# ══════════════════════════════════════════
# POST /api/search
# ══════════════════════════════════════════
@router.post("/search", response_model=SearchResponse)
async def advanced_search(request: Request, body: SearchRequest):
    print(f"\n🔎 Query: {body.query}")

    # Rate limiting
    try:
        from src.rate_limiter import is_rate_limited
        client_ip = request.client.host
        if is_rate_limited(client_ip):
            from fastapi import HTTPException
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please wait a moment!"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"  [RateLimit] Error: {e}")

    category = body.category or detect_category(body.query)
    print(f"📂 Category: {category}")

    filtered_query = build_filtered_query(body.query, category)
    print(f"📝 Filtered: {filtered_query}")

    chain = request.app.state.chain

    if not chain:
        return SearchResponse(
            answer="AI agent is not available. Please try again later.",
            query=body.query,
            category=category,
            timestamp=datetime.now().isoformat(),
            recommendations=get_recommendations(category)
        )

    # Check cache first
    cached = get_cached_response(body.query, category)
    if cached:
        print(f"  ⚡ Returning cached response!")
        return SearchResponse(
            answer=cached,
            query=body.query,
            category=category,
            timestamp=datetime.now().isoformat(),
            media=get_media(category),
            recommendations=get_recommendations(category)
        )

    # Generate answer from AI
    answer = get_response(chain, filtered_query)

    # Save to cache for next time
    save_to_cache(body.query, answer, category)

    try:
        from backend.models.chat import save_message, create_session, update_session
        create_session(body.session_id)
        save_message(body.session_id, body.query, answer)
        update_session(body.session_id)
        print(f"  ✓ Saved to MongoDB")
    except Exception as e:
        print(f"  ⚠️ MongoDB save failed: {e}")

    # Build recommendations: prefer personalized, fall back to related questions
    recommendations = get_personalized_recommendations(body.session_id)
    if not recommendations:
        recommendations = get_related_questions(body.query)

    return SearchResponse(
        answer=answer,
        query=body.query,
        category=category,
        timestamp=datetime.now().isoformat(),
        media=get_media(category),
        recommendations=recommendations,
    )


# ══════════════════════════════════════════
# GET /api/search/suggestions
# ══════════════════════════════════════════
@router.get("/search/suggestions")
async def get_suggestions(category: str = "general"):
    return {
        "category": category,
        "suggestions": get_recommendations(category)
    }


# ══════════════════════════════════════════
# GET /api/debug
# ══════════════════════════════════════════
@router.get("/debug")
async def debug(request: Request):
    chain = request.app.state.chain
    if not chain:
        return {"status": "ERROR - chain is None!"}
    try:
        test_answer = get_response(chain, "What is ANITS?")
        return {
            "status": "working",
            "test_answer": test_answer[:300]
        }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }