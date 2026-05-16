# src/recommendations.py
# Intelligent recommendation engine based on MongoDB chat history

import os
import sys
from datetime import datetime
from collections import Counter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)


# ══════════════════════════════════════════
# CATEGORY SUGGESTIONS
# ══════════════════════════════════════════
CATEGORY_SUGGESTIONS = {
    "academics": [
        "What departments are available in ANITS?",
        "Who is the HOD of CSE department?",
        "What is the exam schedule?",
        "What courses are offered at ANITS?",
        "What is the CBCS grading system?",
        "When do internal assessments happen?",
        "What is the attendance requirement?",
    ],
    "facilities": [
        "Where is the library located?",
        "What are canteen timings?",
        "Is there a hostel facility?",
        "Where is the medical centre?",
        "Is there WiFi on campus?",
        "Where is the ATM on campus?",
        "What sports facilities are available?",
    ],
    "placements": [
        "What companies visit ANITS for placements?",
        "What is the average placement package?",
        "Who is the TPO of ANITS?",
        "What is the highest placement package?",
        "How to register for placement drives?",
        "What is the placement percentage?",
        "When do campus placements start?",
    ],
    "clubs": [
        "What clubs are available in ANITS?",
        "When is TechNova fest?",
        "How to join NSS?",
        "What is the CodeZen club?",
        "How to join the Robotics club?",
        "When is ANITS UTSAV?",
        "What technical clubs are there?",
    ],
    "contacts": [
        "What is the principal email?",
        "How to contact the placement cell?",
        "What is the college phone number?",
        "Who is the dean of academics?",
        "What is the exam cell contact?",
        "How to contact the hostel warden?",
        "What is the library contact?",
    ],
    "locations": [
        "Where is the placement cell?",
        "How to reach the canteen?",
        "Where is the boys hostel?",
        "Where is the library?",
        "Where is the admin block?",
        "Where is the sports ground?",
        "Where is the medical centre?",
    ],
    "general": [
        "Tell me about ANITS college",
        "What is ANITS known for?",
        "How to apply for admission?",
        "What is the college ranking?",
        "What is NAAC grade of ANITS?",
        "Who founded ANITS?",
        "Where is ANITS located?",
    ]
}


# ══════════════════════════════════════════
# RELATED QUESTIONS MAP
# ══════════════════════════════════════════
RELATED_QUESTIONS = {
    "placement": [
        "What is the average placement package?",
        "Which companies visited ANITS recently?",
        "How to prepare for campus placements?"
    ],
    "hostel": [
        "What are hostel fees?",
        "What facilities are in the hostel?",
        "How to apply for hostel admission?"
    ],
    "library": [
        "What are library timings?",
        "How to get library membership?",
        "How many books does the library have?"
    ],
    "exam": [
        "When are internal assessments?",
        "What is the passing criteria?",
        "How to apply for revaluation?"
    ],
    "club": [
        "How to join a club?",
        "When do clubs meet?",
        "What are the benefits of joining clubs?"
    ],
    "canteen": [
        "What are canteen timings?",
        "Where is the canteen located?",
        "What food is available in canteen?"
    ],
    "fee": [
        "How to pay college fees?",
        "What is the fee structure?",
        "Are scholarships available?"
    ],
    "admission": [
        "What is the admission process?",
        "What documents are needed for admission?",
        "What is the eligibility criteria?"
    ]
}


# ══════════════════════════════════════════
# GET RECOMMENDATIONS BY CATEGORY
# ══════════════════════════════════════════
def get_recommendations(category: str, limit: int = 3) -> list:
    """Returns recommended questions for a category"""
    suggestions = CATEGORY_SUGGESTIONS.get(
        category,
        CATEGORY_SUGGESTIONS["general"]
    )
    return suggestions[:limit]


# ══════════════════════════════════════════
# GET RELATED QUESTIONS FROM QUERY
# ══════════════════════════════════════════
def get_related_questions(query: str, limit: int = 3) -> list:
    """Returns related questions based on keywords in query"""
    query_lower = query.lower()
    related = []

    for keyword, questions in RELATED_QUESTIONS.items():
        if keyword in query_lower:
            related.extend(questions)

    # Remove duplicates
    seen = set()
    unique = []
    for q in related:
        if q not in seen:
            seen.add(q)
            unique.append(q)

    return unique[:limit] if unique else get_recommendations("general", limit)


# ══════════════════════════════════════════
# GET PERSONALIZED RECOMMENDATIONS
# ══════════════════════════════════════════
def get_personalized_recommendations(session_id: str, limit: int = 3) -> list:
    """
    Analyzes MongoDB chat history for a session
    and returns personalized recommendations
    """
    try:
        from backend.models.database import chat_collection

        if chat_collection is None:
            return get_recommendations("general", limit)

        # Get last 10 messages for this session
        messages = list(chat_collection.find(
            {"session_id": session_id},
            {"question": 1, "_id": 0}
        ).sort("timestamp", -1).limit(10))

        if not messages:
            return get_recommendations("general", limit)

        # Count category occurrences in history
        category_counts = Counter()

        for msg in messages:
            question = msg.get("question", "").lower()

            # Check which category this question belongs to
            if any(w in question for w in ["department", "course", "exam", "hod", "faculty"]):
                category_counts["academics"] += 1
            elif any(w in question for w in ["placement", "company", "job", "tpo", "package"]):
                category_counts["placements"] += 1
            elif any(w in question for w in ["club", "fest", "event", "society"]):
                category_counts["clubs"] += 1
            elif any(w in question for w in ["library", "canteen", "hostel", "sports", "medical"]):
                category_counts["facilities"] += 1
            elif any(w in question for w in ["where", "location", "block", "building"]):
                category_counts["locations"] += 1
            elif any(w in question for w in ["contact", "email", "phone", "number"]):
                category_counts["contacts"] += 1
            else:
                category_counts["general"] += 1

        # Get most interested category
        if category_counts:
            top_category = category_counts.most_common(1)[0][0]
        else:
            top_category = "general"

        print(f"  [Recommendations] User interest: {top_category}")

        # Get suggestions for top category
        suggestions = CATEGORY_SUGGESTIONS.get(top_category, CATEGORY_SUGGESTIONS["general"])

        # Filter out questions already asked
        asked = {msg.get("question", "") for msg in messages}
        fresh = [s for s in suggestions if s not in asked]

        return fresh[:limit] if fresh else suggestions[:limit]

    except Exception as e:
        print(f"  [Recommendations] Error: {e}")
        return get_recommendations("general", limit)


# ══════════════════════════════════════════
# GET POPULAR QUESTIONS (for analytics)
# ══════════════════════════════════════════
def get_popular_questions(limit: int = 10) -> list:
    """Returns most asked questions across all sessions"""
    try:
        from backend.models.database import chat_collection

        if chat_collection is None:
            return []

        # Aggregate most common questions
        pipeline = [
            {"$group": {
                "_id": "$question",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]

        results = list(chat_collection.aggregate(pipeline))
        return [{"question": r["_id"], "count": r["count"]} for r in results]

    except Exception as e:
        print(f"  [Popular Questions] Error: {e}")
        return []


# ══════════════════════════════════════════
# TEST
# ══════════════════════════════════════════
if __name__ == "__main__":
    print("🤖 Testing Recommendation Engine")
    print("=" * 40)

    print("\n1. Category recommendations (placements):")
    recs = get_recommendations("placements")
    for r in recs:
        print(f"  - {r}")

    print("\n2. Related questions for 'Where is the library?':")
    related = get_related_questions("Where is the library?")
    for r in related:
        print(f"  - {r}")

    print("\n3. Popular questions:")
    popular = get_popular_questions()
    if popular:
        for p in popular:
            print(f"  - {p['question']} ({p['count']} times)")
    else:
        print("  No data yet!")

    print("\n✅ Recommendation engine working!")