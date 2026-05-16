# src/personalization.py
# Advanced personalization based on user history

import os
import sys
from datetime import datetime
from collections import Counter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)


# ══════════════════════════════════════════
# BUILD USER PROFILE
# ══════════════════════════════════════════
def build_user_profile(session_id: str) -> dict:
    """
    Analyzes chat history to build
    a lightweight user interest profile
    """
    try:
        from backend.models.database import chat_collection

        if chat_collection is None:
            return {"interests": [], "top_category": "general", "message_count": 0}

        # Get all messages for this session
        messages = list(chat_collection.find(
            {"session_id": session_id},
            {"question": 1, "timestamp": 1, "_id": 0}
        ).sort("timestamp", -1).limit(20))

        if not messages:
            return {"interests": [], "top_category": "general", "message_count": 0}

        # Analyze interests
        category_counts = Counter()
        keywords_found = []

        KEYWORD_MAP = {
            "academics": ["department", "course", "exam", "hod", "faculty", "semester", "cbcs", "attendance"],
            "placements": ["placement", "company", "job", "tpo", "package", "internship", "recruit"],
            "clubs": ["club", "fest", "event", "society", "nss", "cultural", "technical"],
            "facilities": ["library", "canteen", "hostel", "sports", "medical", "wifi", "gym"],
            "locations": ["where", "location", "block", "building", "directions", "map"],
            "contacts": ["contact", "email", "phone", "number", "office", "reach"],
        }

        for msg in messages:
            question = msg.get("question", "").lower()
            for category, keywords in KEYWORD_MAP.items():
                matches = [kw for kw in keywords if kw in question]
                if matches:
                    category_counts[category] += len(matches)
                    keywords_found.extend(matches)

        # Determine top interests
        top_interests = [cat for cat, _ in category_counts.most_common(3)]
        top_category = top_interests[0] if top_interests else "general"

        profile = {
            "session_id": session_id,
            "message_count": len(messages),
            "top_category": top_category,
            "interests": top_interests,
            "category_counts": dict(category_counts),
            "keywords_found": list(set(keywords_found))[:10],
            "last_active": messages[0].get("timestamp", datetime.now()).isoformat() if messages else None
        }

        print(f"  [Profile] Session {session_id}: interests={top_interests}")
        return profile

    except Exception as e:
        print(f"  [Personalization] Error: {e}")
        return {"interests": [], "top_category": "general", "message_count": 0}


# ══════════════════════════════════════════
# GET PERSONALIZED GREETING
# ══════════════════════════════════════════
def get_personalized_greeting(session_id: str) -> str:
    """Returns personalized greeting based on user history"""
    try:
        profile = build_user_profile(session_id)
        count = profile.get("message_count", 0)
        top_category = profile.get("top_category", "general")

        if count == 0:
            return "Hi! 👋 I am your ANITS Campus Assistant. Ask me anything about departments, facilities, placements, events, and more!"

        greetings = {
            "placements": f"Welcome back! 👋 You seem interested in placements. Shall I tell you about recent company visits?",
            "academics": f"Welcome back! 👋 Looking for academic information? I can help with departments, exams, and more!",
            "clubs": f"Welcome back! 👋 Interested in campus activities? Check out our upcoming fests and club events!",
            "facilities": f"Welcome back! 👋 Need help finding campus facilities? I know every corner of ANITS!",
            "locations": f"Welcome back! 👋 Need directions? I can guide you anywhere on campus!",
            "contacts": f"Welcome back! 👋 Looking for someone? I have all faculty contacts ready!",
            "general": f"Welcome back! 👋 How can I help you today?"
        }

        return greetings.get(top_category, greetings["general"])

    except Exception as e:
        print(f"  [Personalization] Greeting error: {e}")
        return "Hi! 👋 I am your ANITS Campus Assistant!"


# ══════════════════════════════════════════
# GET PREDICTIVE SUGGESTIONS
# ══════════════════════════════════════════
def get_predictive_suggestions(session_id: str) -> list:
    """
    Predicts what user might ask next
    based on academic calendar and history
    """
    try:
        profile = build_user_profile(session_id)
        top_category = profile.get("top_category", "general")
        now = datetime.now()
        month = now.month
        suggestions = []

        # Academic calendar aware predictions
        if month in [7, 8]:
            # July-August: Semester start
            suggestions = [
                "When does the odd semester begin?",
                "What is the attendance requirement?",
                "How to get library membership?",
                "Where is the hostel located?"
            ]
        elif month in [9, 10]:
            # September-October: Mid semester
            suggestions = [
                "When are internal assessments?",
                "What is the CBCS grading system?",
                "When is Dasara holiday?",
                "What clubs can I join?"
            ]
        elif month in [11, 12]:
            # November-December: End semester
            suggestions = [
                "When do end semester exams start?",
                "How to apply for revaluation?",
                "When does even semester begin?",
                "What is the exam schedule?"
            ]
        elif month in [1, 2]:
            # January-February: Even semester start
            suggestions = [
                "When is Sports Day?",
                "When are internal assessments?",
                "What events are happening this semester?",
                "How to register for placement drives?"
            ]
        elif month in [3, 4]:
            # March-April: Placement season + Fests
            suggestions = [
                "When is TechNova fest?",
                "Which companies are visiting for placements?",
                "When is ANITS UTSAV?",
                "How to register for campus placements?"
            ]
        elif month in [5, 6]:
            # May-June: Exam + Vacation
            suggestions = [
                "When do even semester exams start?",
                "When is summer vacation?",
                "When is graduation day?",
                "How to apply for transcripts?"
            ]

        # Add category specific suggestions
        category_predictions = {
            "placements": [
                "What companies are visiting this month?",
                "How to prepare resume for placements?",
                "What is the placement eligibility criteria?"
            ],
            "academics": [
                "What is the exam timetable?",
                "How to apply for bonafide certificate?",
                "What is the minimum attendance required?"
            ],
            "clubs": [
                "How to register for TechNova?",
                "What are the upcoming fests?",
                "How to become club coordinator?"
            ]
        }

        if top_category in category_predictions:
            suggestions.extend(category_predictions[top_category])

        return suggestions[:4]

    except Exception as e:
        print(f"  [Personalization] Predictive error: {e}")
        return []


# ══════════════════════════════════════════
# TEST
# ══════════════════════════════════════════
if __name__ == "__main__":
    print("🎯 Testing Personalization Engine")
    print("=" * 40)

    print("\n1. User Profile (default session):")
    profile = build_user_profile("default")
    print(f"  Message count: {profile['message_count']}")
    print(f"  Top category: {profile['top_category']}")
    print(f"  Interests: {profile['interests']}")

    print("\n2. Personalized Greeting:")
    greeting = get_personalized_greeting("default")
    print(f"  {greeting}")

    print("\n3. Predictive Suggestions:")
    suggestions = get_predictive_suggestions("default")
    for s in suggestions:
        print(f"  - {s}")

    print("\n✅ Personalization engine working!")