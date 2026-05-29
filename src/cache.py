# src/cache.py
# Response caching for faster repeated queries

import os
import sys
import json
import hashlib
from datetime import datetime, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# ══════════════════════════════════════════
# IN-MEMORY CACHE
# ══════════════════════════════════════════
# Stores: {query_hash: {answer, timestamp, hits}}
_cache = {}

# Cache settings
CACHE_TTL_MINUTES = 60      # Cache expires after 60 minutes
MAX_CACHE_SIZE = 100        # Max 100 cached responses


# ══════════════════════════════════════════
# GENERATE CACHE KEY
# ══════════════════════════════════════════
def get_cache_key(query: str, category: str = None) -> str:
    """Generate unique hash key for query + category"""
    raw = f"{query.lower().strip()}:{category or 'general'}"
    return hashlib.md5(raw.encode()).hexdigest()


# ══════════════════════════════════════════
# GET FROM CACHE
# ══════════════════════════════════════════
def get_cached_response(query: str, category: str = None) -> str:
    """
    Returns cached answer if exists and not expired.
    Returns None if cache miss.
    """
    key = get_cache_key(query, category)

    if key not in _cache:
        return None

    entry = _cache[key]
    cached_at = datetime.fromisoformat(entry["timestamp"])
    age_minutes = (datetime.now() - cached_at).seconds / 60

    # Check if expired
    if age_minutes > CACHE_TTL_MINUTES:
        del _cache[key]
        print(f"  [Cache] EXPIRED: {query[:40]}...")
        return None

    # Cache hit!
    _cache[key]["hits"] += 1
    print(f"  [Cache] HIT #{entry['hits']}: {query[:40]}...")
    return entry["answer"]


# ══════════════════════════════════════════
# SAVE TO CACHE
# ══════════════════════════════════════════
def save_to_cache(query: str, answer: str, category: str = None):
    """Saves answer to cache with timestamp"""
    # Don't cache error responses
    if "encountered an error" in answer or "Please try again" in answer:
        return

    # Evict oldest if cache is full
    if len(_cache) >= MAX_CACHE_SIZE:
        oldest_key = min(_cache, key=lambda k: _cache[k]["timestamp"])
        del _cache[oldest_key]
        print(f"  [Cache] Evicted oldest entry")

    key = get_cache_key(query, category)
    _cache[key] = {
        "query": query,
        "answer": answer,
        "category": category,
        "timestamp": datetime.now().isoformat(),
        "hits": 0
    }
    print(f"  [Cache] SAVED: {query[:40]}...")


# ══════════════════════════════════════════
# GET CACHE STATS
# ══════════════════════════════════════════
def get_cache_stats() -> dict:
    """Returns cache performance statistics"""
    if not _cache:
        return {
            "total_entries": 0,
            "total_hits": 0,
            "cache_size": 0,
            "hit_rate": "0%"
        }

    total_hits = sum(e["hits"] for e in _cache.values())
    total_requests = len(_cache) + total_hits

    return {
        "total_entries": len(_cache),
        "total_hits": total_hits,
        "max_size": MAX_CACHE_SIZE,
        "ttl_minutes": CACHE_TTL_MINUTES,
        "hit_rate": f"{round((total_hits/total_requests)*100, 1)}%" if total_requests > 0 else "0%",
        "top_queries": sorted(
            [{"query": v["query"], "hits": v["hits"]} for v in _cache.values()],
            key=lambda x: x["hits"],
            reverse=True
        )[:5]
    }


# ══════════════════════════════════════════
# CLEAR CACHE
# ══════════════════════════════════════════
def clear_cache():
    """Clears entire cache"""
    global _cache
    count = len(_cache)
    _cache = {}
    print(f"  [Cache] Cleared {count} entries")
    return count


# ══════════════════════════════════════════
# TEST
# ══════════════════════════════════════════
if __name__ == "__main__":
    print("⚡ Testing Cache System")
    print("=" * 40)

    # Test save
    save_to_cache("Where is canteen?", "Canteen is in center of campus.", "locations")
    save_to_cache("Who is TPO?", "Mr. K. Srinivas is the TPO.", "contacts")

    # Test hit
    result = get_cached_response("Where is canteen?", "locations")
    print(f"\nCache hit: {result}")

    # Test miss
    result = get_cached_response("What is NAAC grade?", "general")
    print(f"Cache miss: {result}")

    # Stats
    stats = get_cache_stats()
    print(f"\nCache stats: {json.dumps(stats, indent=2)}")

    print("\n✅ Cache working!")