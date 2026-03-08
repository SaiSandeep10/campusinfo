# src/freshness.py
# Content freshness detection and automatic updates

import os
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METADATA_FILE = os.path.join(BASE_DIR, "data/scraped/website_metadata.json")
FRESHNESS_FILE = os.path.join(BASE_DIR, "data/scraped/freshness.json")

# ══════════════════════════════════════════
# HOW OLD IS TOO OLD?
# ══════════════════════════════════════════
FRESHNESS_RULES = {
    "general":    7,   # Re-scrape every 7 days
    "academics":  14,  # Re-scrape every 14 days
    "placements": 3,   # Re-scrape every 3 days (changes often!)
    "events":     1,   # Re-scrape every 1 day (changes very often!)
    "facilities": 30,  # Re-scrape every 30 days
    "contacts":   30,  # Re-scrape every 30 days
    "clubs":      7,   # Re-scrape every 7 days
}


# ══════════════════════════════════════════
# SAVE FRESHNESS TIMESTAMP
# ══════════════════════════════════════════
def save_freshness_timestamp():
    """Save when data was last updated"""
    freshness_data = {
        "last_scraped": datetime.now().isoformat(),
        "last_ingested": datetime.now().isoformat(),
        "categories": {
            category: datetime.now().isoformat()
            for category in FRESHNESS_RULES.keys()
        }
    }

    os.makedirs(os.path.dirname(FRESHNESS_FILE), exist_ok=True)
    with open(FRESHNESS_FILE, "w") as f:
        json.dump(freshness_data, f, indent=2)

    print(f"  ✓ Freshness timestamp saved!")
    return freshness_data


# ══════════════════════════════════════════
# CHECK IF DATA IS STALE
# ══════════════════════════════════════════
def check_freshness():
    """
    Check if campus data needs updating.
    Returns dict of categories that need refresh.
    """
    print("\n🔍 Checking content freshness...")

    # If no freshness file exists, data is definitely stale!
    if not os.path.exists(FRESHNESS_FILE):
        print("  ⚠️ No freshness record found — data needs refresh!")
        return {cat: True for cat in FRESHNESS_RULES.keys()}

    with open(FRESHNESS_FILE, "r") as f:
        freshness_data = json.load(f)

    stale_categories = {}
    now = datetime.now()

    for category, max_age_days in FRESHNESS_RULES.items():
        if category in freshness_data.get("categories", {}):
            last_scraped = datetime.fromisoformat(
                freshness_data["categories"][category]
            )
            age_days = (now - last_scraped).days
            is_stale = age_days >= max_age_days

            stale_categories[category] = is_stale

            status = "⚠️ STALE" if is_stale else "✅ Fresh"
            print(f"  {status} — {category}: {age_days} days old (max {max_age_days} days)")
        else:
            stale_categories[category] = True
            print(f"  ⚠️ STALE — {category}: no record found")

    stale_count = sum(1 for v in stale_categories.values() if v)
    print(f"\n  📊 {stale_count}/{len(FRESHNESS_RULES)} categories need refresh")

    return stale_categories


# ══════════════════════════════════════════
# AUTO REFRESH STALE CONTENT
# ══════════════════════════════════════════
def auto_refresh_if_stale():
    """
    Automatically refresh stale content.
    Called on backend startup.
    """
    stale = check_freshness()
    stale_count = sum(1 for v in stale.values() if v)

    if stale_count == 0:
        print("  ✅ All content is fresh — no refresh needed!")
        return False

    print(f"\n  🔄 {stale_count} categories are stale — refreshing...")

    try:
        # Re-run scraper for stale categories
        import sys
        sys.path.append(BASE_DIR)
        from src.scraper import scrape_website
        scrape_website()
        print("  ✓ Website re-scraped!")

        # Save new freshness timestamp
        save_freshness_timestamp()
        print("  ✓ Freshness timestamp updated!")

        return True

    except Exception as e:
        print(f"  ✗ Auto refresh failed: {e}")
        return False


# ══════════════════════════════════════════
# GET FRESHNESS STATUS (for API)
# ══════════════════════════════════════════
def get_freshness_status():
    """Returns freshness status for API endpoint"""
    if not os.path.exists(FRESHNESS_FILE):
        return {
            "status": "unknown",
            "last_scraped": None,
            "categories": {}
        }

    with open(FRESHNESS_FILE, "r") as f:
        data = json.load(f)

    stale = check_freshness()
    stale_count = sum(1 for v in stale.values() if v)

    return {
        "status": "fresh" if stale_count == 0 else "stale",
        "last_scraped": data.get("last_scraped"),
        "stale_categories": [k for k, v in stale.items() if v],
        "fresh_categories": [k for k, v in stale.items() if not v]
    }


# ══════════════════════════════════════════
# TEST
# ══════════════════════════════════════════
if __name__ == "__main__":
    print("🕐 ANITS Content Freshness Checker")
    print("=" * 40)

    # Save initial timestamp
    save_freshness_timestamp()

    # Check freshness
    stale = check_freshness()

    # Get status
    status = get_freshness_status()
    print(f"\n📊 Overall Status: {status['status']}")