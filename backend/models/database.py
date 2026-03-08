# backend/models/database.py
# MongoDB connection and collections

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ══════════════════════════════════════════
# CONNECT TO MONGODB
# ══════════════════════════════════════════
def get_database():
    """Connect to MongoDB Atlas and return database"""
    try:
        client = MongoClient(os.getenv("MONGODB_URL"))
        db = client["anits_campus"]
        print("  ✓ MongoDB connected!")
        return db
    except Exception as e:
        print(f"  ✗ MongoDB connection failed: {e}")
        return None

# Initialize database
db = get_database()

# Collections
chat_collection = db["chat_history"] if db is not None else None
session_collection = db["sessions"] if db is not None else None
content_collection = db["campus_content"] if db is not None else None