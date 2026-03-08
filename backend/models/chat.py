# backend/models/chat.py
# Chat history model for MongoDB

from datetime import datetime
from backend.models.database import chat_collection, session_collection

# ══════════════════════════════════════════
# SAVE CHAT MESSAGE
# ══════════════════════════════════════════
def save_message(session_id, question, answer):
    """Save a chat message to MongoDB"""
    if chat_collection is None:
        return None

    message = {
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "timestamp": datetime.now(),
        "created_at": datetime.now().isoformat()
    }

    result = chat_collection.insert_one(message)
    print(f"  ✓ Message saved to MongoDB: {result.inserted_id}")
    return str(result.inserted_id)


# ══════════════════════════════════════════
# GET CHAT HISTORY
# ══════════════════════════════════════════
def get_chat_history(session_id, limit=20):
    """Get chat history for a session"""
    if chat_collection is None:
        return []

    messages = chat_collection.find(
        {"session_id": session_id},
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit)

    return list(messages)


# ══════════════════════════════════════════
# CREATE SESSION
# ══════════════════════════════════════════
def create_session(session_id):
    """Create a new user session"""
    if session_collection is None:
        return None

    session = {
        "session_id": session_id,
        "created_at": datetime.now(),
        "last_active": datetime.now(),
        "message_count": 0
    }

    # Only create if doesn't exist
    existing = session_collection.find_one({"session_id": session_id})
    if not existing:
        session_collection.insert_one(session)
        print(f"  ✓ New session created: {session_id}")

    return session_id


# ══════════════════════════════════════════
# UPDATE SESSION
# ══════════════════════════════════════════
def update_session(session_id):
    """Update session last active time"""
    if session_collection is None:
        return None

    session_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {"last_active": datetime.now()},
            "$inc": {"message_count": 1}
        }
    )