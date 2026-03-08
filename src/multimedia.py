# src/multimedia.py

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MULTIMEDIA_FILE = os.path.join(BASE_DIR, "data", "multimedia.json")


def load_multimedia():
    """Load multimedia database safely"""
    if not os.path.exists(MULTIMEDIA_FILE):
        print("⚠ multimedia.json not found")
        return {}

    try:
        with open(MULTIMEDIA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading multimedia: {e}")
        return {}


def search_multimedia(query: str):
    """Find multimedia related to query"""

    query = query.lower()
    db = load_multimedia()

    for key, value in db.items():
        if key in query:
            return value

    return None


# test block
if __name__ == "__main__":
    print("Testing multimedia search...")
    result = search_multimedia("library")
    print(result)