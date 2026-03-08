# backend/routes/search.py
# Advanced search with filters and multimedia support

from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.agent_manager import get_agent
from src.agent import get_response
from src.multimedia import search_multimedia
from src.recommendations import get_recommendations
from src.agent import build_agent, get_response
router = APIRouter()


# ----------------------------------------------------
# REQUEST MODEL
# ----------------------------------------------------
class SearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    session_id: str = "default"


# ----------------------------------------------------
# RESPONSE MODEL
# ----------------------------------------------------
class SearchResponse(BaseModel):
    answer: str
    query: str
    category: Optional[str]
    timestamp: str
    media: Optional[dict] = None
    recommendations: Optional[list] = None


# ----------------------------------------------------
# CATEGORY KEYWORDS
# ----------------------------------------------------
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


# ----------------------------------------------------
# CATEGORY DETECTION
# ----------------------------------------------------
def detect_category(query: str) -> str:

    query_lower = query.lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for word in keywords if word in query_lower)
        scores[category] = score

    best = max(scores, key=scores.get)

    return best if scores[best] > 0 else "general"


# ----------------------------------------------------
# PROMPT CONTEXT BUILDER
# ----------------------------------------------------
def build_filtered_prompt(query: str, category: str) -> str:

    context_map = {
        "academics": "Focus on academic information.",
        "facilities": "Focus on campus facilities.",
        "placements": "Focus on placement information.",
        "clubs": "Focus on clubs and events.",
        "contacts": "Focus on contact details.",
        "locations": "Focus on campus locations.",
        "general": "Provide general campus information."
    }

    context = context_map.get(category, context_map["general"])

    return f"{query} [{context}]"


# ----------------------------------------------------
# SEARCH ENDPOINT
# ----------------------------------------------------
@router.post("/search", response_model=SearchResponse)
async def advanced_search(request: Request, body: SearchRequest):

    print("\n🔎 Query:", body.query)

    # Detect category
    category = body.category or detect_category(body.query)

    print("📂 Category:", category)

    # Build prompt
    filtered_query = build_filtered_prompt(body.query, category)

    # Get AI agent
    chain = get_agent()

    # Generate answer
    answer = get_response(chain, filtered_query)

    # Multimedia search
    media = None
    try:
        media = search_multimedia(body.query)
    except Exception as e:
        print("Multimedia error:", e)

    # Recommendations
    recommendations = []
    try:
        recommendations = get_recommendations(category)
    except Exception as e:
        print("Recommendation error:", e)

    # Save chat history
    try:
        from backend.models.chat import save_message, update_session
        save_message(body.session_id, body.query, answer)
        update_session(body.session_id)
    except Exception as e:
        print("MongoDB save error:", e)

    return SearchResponse(
        answer=answer,
        query=body.query,
        category=category,
        timestamp=datetime.now().isoformat(),
        media=media,
        recommendations=recommendations
    )


# ----------------------------------------------------
# SUGGESTED QUESTIONS
# ----------------------------------------------------
@router.get("/search/suggestions")
async def get_suggestions(category: str = "general"):

    suggestions = {

        "academics": [
            "What departments are available in ANITS?",
            "Who is the HOD of CSE?",
            "What is the exam schedule?"
        ],

        "facilities": [
            "Where is the library located?",
            "What are canteen timings?",
            "Is hostel available?"
        ],

        "placements": [
            "What companies visit ANITS?",
            "What is the average package?",
            "Who is the placement officer?"
        ],

        "clubs": [
            "What clubs exist in ANITS?",
            "When is Tech Fest?",
            "How to join NSS?"
        ],

        "contacts": [
            "What is the principal email?",
            "How to contact placement cell?",
            "What is college phone number?"
        ],

        "locations": [
            "Where is the canteen?",
            "Where is the placement cell?",
            "Where is boys hostel?"
        ],

        "general": [
            "Tell me about ANITS",
            "What courses does ANITS offer?",
            "How to apply for admission?"
        ]
    }

    return {
        "category": category,
        "suggestions": suggestions.get(category, suggestions["general"])
    }