# src/analytics.py
# Comprehensive campus analytics dashboard

import os
import sys
from datetime import datetime, timedelta
from collections import Counter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)


# ══════════════════════════════════════════
# GET OVERALL STATS
# ══════════════════════════════════════════
def get_overall_stats() -> dict:
    """Returns overall usage statistics"""
    try:
        from backend.models.database import chat_collection, session_collection

        if chat_collection is None:
            return {}

        # Total messages
        total_messages = chat_collection.count_documents({})

        # Total sessions
        total_sessions = session_collection.count_documents({}) if session_collection else 0

        # Messages today — use created_at string instead of timestamp
        today_str = datetime.now().strftime("%Y-%m-%d")
        messages_today = chat_collection.count_documents({
            "created_at": {"$regex": f"^{today_str}"}
        })

        # Messages this week — count last 7 days
        messages_week = 0
        for i in range(7):
            day = datetime.now() - timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            count = chat_collection.count_documents({
                "created_at": {"$regex": f"^{day_str}"}
            })
            messages_week += count

        print(f"  [Analytics] Total: {total_messages}, Today: {messages_today}, Week: {messages_week}")

        return {
            "total_messages": total_messages,
            "total_sessions": total_sessions,
            "messages_today": messages_today,
            "messages_this_week": messages_week,
            "generated_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"  [Analytics] Stats error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "total_messages": 0,
            "total_sessions": 0,
            "messages_today": 0,
            "messages_this_week": 0,
            "generated_at": datetime.now().isoformat()
        }

# ══════════════════════════════════════════
# GET POPULAR QUERIES
# ══════════════════════════════════════════
def get_popular_queries(limit: int = 10) -> list:
    """Returns most asked questions"""
    try:
        from backend.models.database import chat_collection

        if chat_collection is None:
            return []

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
        print(f"  [Analytics] Popular queries error: {e}")
        return []


# ══════════════════════════════════════════
# GET CATEGORY DISTRIBUTION
# ══════════════════════════════════════════
def get_category_distribution() -> dict:
    """Returns how many questions per category"""
    try:
        from backend.models.database import chat_collection

        if chat_collection is None:
            return {}

        messages = list(chat_collection.find(
            {},
            {"question": 1, "_id": 0}
        ))

        category_counts = Counter()

        for msg in messages:
            question = msg.get("question", "").lower()

            if any(w in question for w in ["department", "course", "exam", "hod", "faculty", "semester"]):
                category_counts["academics"] += 1
            elif any(w in question for w in ["placement", "company", "job", "tpo", "package", "internship"]):
                category_counts["placements"] += 1
            elif any(w in question for w in ["club", "fest", "event", "society", "nss"]):
                category_counts["clubs"] += 1
            elif any(w in question for w in ["library", "canteen", "hostel", "sports", "medical", "wifi"]):
                category_counts["facilities"] += 1
            elif any(w in question for w in ["where", "location", "block", "building", "directions"]):
                category_counts["locations"] += 1
            elif any(w in question for w in ["contact", "email", "phone", "number", "office"]):
                category_counts["contacts"] += 1
            else:
                category_counts["general"] += 1

        total = sum(category_counts.values()) or 1

        return {
            cat: {
                "count": count,
                "percentage": round((count / total) * 100, 1)
            }
            for cat, count in category_counts.most_common()
        }

    except Exception as e:
        print(f"  [Analytics] Category distribution error: {e}")
        return {}


# ══════════════════════════════════════════
# GET DAILY ACTIVITY
# ══════════════════════════════════════════
def get_daily_activity(days: int = 7) -> list:
    """Returns message count per day for last N days"""
    try:
        from backend.models.database import chat_collection

        if chat_collection is None:
            return []

        activity = []
        for i in range(days - 1, -1, -1):
            day = datetime.now() - timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")

            # Use created_at string field instead of timestamp
            count = chat_collection.count_documents({
                "created_at": {"$regex": f"^{day_str}"}
            })

            activity.append({
                "date": day.strftime("%b %d"),
                "count": count
            })

        return activity

    except Exception as e:
        print(f"  [Analytics] Daily activity error: {e}")
        return []

# ══════════════════════════════════════════
# GET INFORMATION GAPS
# ══════════════════════════════════════════
def get_information_gaps(limit: int = 5) -> list:
    """
    Detects questions where chatbot gave
    fallback/error responses - information gaps!
    """
    try:
        from backend.models.database import chat_collection

        if chat_collection is None:
            return []

        # Find answers that contain fallback phrases
        fallback_phrases = [
            "I don't have that information",
            "Please visit anits.org",
            "contact the college office",
            "encountered an error"
        ]

        gaps = []
        for phrase in fallback_phrases:
            messages = list(chat_collection.find(
                {"answer": {"$regex": phrase, "$options": "i"}},
                {"question": 1, "_id": 0}
            ).limit(limit))

            for msg in messages:
                question = msg.get("question", "")
                if question and question not in gaps:
                    gaps.append(question)

        return gaps[:limit]

    except Exception as e:
        print(f"  [Analytics] Information gaps error: {e}")
        return []


# ══════════════════════════════════════════
# GET FULL ANALYTICS REPORT
# ══════════════════════════════════════════
def get_full_analytics() -> dict:
    """Returns complete analytics report"""
    print("\n📊 Generating analytics report...")

    return {
        "overall_stats": get_overall_stats(),
        "popular_queries": get_popular_queries(10),
        "category_distribution": get_category_distribution(),
        "daily_activity": get_daily_activity(7),
        "information_gaps": get_information_gaps(5),
        "generated_at": datetime.now().isoformat()
    }


# ══════════════════════════════════════════
# TEST
# ══════════════════════════════════════════
if __name__ == "__main__":
    print("📊 ANITS Campus Analytics Dashboard")
    print("=" * 40)

    stats = get_overall_stats()
    print(f"\n Overall Stats:")
    print(f"  Total messages: {stats.get('total_messages', 0)}")
    print(f"  Total sessions: {stats.get('total_sessions', 0)}")
    print(f"  Messages today: {stats.get('messages_today', 0)}")
    print(f"  Messages this week: {stats.get('messages_this_week', 0)}")

    print(f"\n Popular Queries:")
    for q in get_popular_queries(5):
        print(f"  - {q['question']} ({q['count']} times)")

    print(f"\n Category Distribution:")
    for cat, data in get_category_distribution().items():
        print(f"  - {cat}: {data['count']} ({data['percentage']}%)")

    print(f"\n Information Gaps:")
    for gap in get_information_gaps():
        print(f"  - {gap}")

    print(f"\n Daily Activity (last 7 days):")
    for day in get_daily_activity():
        print(f"  - {day['date']}: {day['count']} messages")

    print("\n✅ Analytics working!")