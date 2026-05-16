import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_database():
    try:
        MONGODB_URL = os.getenv("MONGODB_URL")
        print(f"  Connecting with URL: {MONGODB_URL[:30]}...")
        client = MongoClient(MONGODB_URL)
        db = client["anits_campus"]
        db.command("ping")
        print("  ✓ MongoDB connected!")
        return db
    except Exception as e:
        print(f"  ✗ MongoDB connection failed: {e}")
        return None

db = get_database()
chat_collection    = db["chat_history"]   if db is not None else None
session_collection = db["sessions"]       if db is not None else None
content_collection = db["campus_content"] if db is not None else None