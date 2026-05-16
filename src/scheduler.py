# src/scheduler.py
# Automated scheduling for content freshness

import os
import sys
import threading
import time
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)


# ══════════════════════════════════════════
# SCHEDULER CONFIG
# ══════════════════════════════════════════
SCHEDULE_CONFIG = {
    "scraper":    24,   # Run scraper every 24 hours
    "freshness":  1,    # Check freshness every 1 hour
    "analytics":  6,    # Update analytics every 6 hours
}


# ══════════════════════════════════════════
# RUN SCRAPER
# ══════════════════════════════════════════
def run_scraper():
    """Runs web scraper to refresh campus content"""
    try:
        print(f"\n[Scheduler] 🔄 Running scraper at {datetime.now().strftime('%H:%M:%S')}")
        from src.scraper import scrape_website
        scrape_website()
        print(f"[Scheduler] ✓ Scraper completed!")

        # Save freshness timestamp
        from src.freshness import save_freshness_timestamp
        save_freshness_timestamp()
        print(f"[Scheduler] ✓ Freshness timestamp updated!")

    except Exception as e:
        print(f"[Scheduler] ✗ Scraper failed: {e}")


# ══════════════════════════════════════════
# CHECK FRESHNESS
# ══════════════════════════════════════════
def check_and_refresh():
    """Checks freshness and refreshes if stale"""
    try:
        print(f"\n[Scheduler] 🔍 Checking freshness at {datetime.now().strftime('%H:%M:%S')}")
        from src.freshness import check_freshness
        stale = check_freshness()
        stale_count = sum(1 for v in stale.values() if v)

        if stale_count > 0:
            print(f"[Scheduler] ⚠️ {stale_count} categories stale — refreshing!")
            run_scraper()
        else:
            print(f"[Scheduler] ✅ All content is fresh!")

    except Exception as e:
        print(f"[Scheduler] ✗ Freshness check failed: {e}")


# ══════════════════════════════════════════
# SCHEDULER LOOP
# ══════════════════════════════════════════
def scheduler_loop():
    """
    Runs in background thread.
    Checks freshness every hour.
    Runs full scrape every 24 hours.
    """
    print("\n[Scheduler] 🚀 Background scheduler started!")

    scraper_counter = 0
    freshness_counter = 0

    while True:
        try:
            # Sleep 1 hour between checks
            time.sleep(3600)

            scraper_counter += 1
            freshness_counter += 1

            # Check freshness every hour
            if freshness_counter >= SCHEDULE_CONFIG["freshness"]:
                check_and_refresh()
                freshness_counter = 0

            # Full scrape every 24 hours
            if scraper_counter >= SCHEDULE_CONFIG["scraper"]:
                run_scraper()
                scraper_counter = 0

        except Exception as e:
            print(f"[Scheduler] ✗ Loop error: {e}")
            time.sleep(60)  # Wait 1 minute before retrying


# ══════════════════════════════════════════
# START SCHEDULER
# ══════════════════════════════════════════
def start_scheduler():
    """
    Starts scheduler in background thread.
    Called from backend/main.py on startup.
    Non-blocking — runs alongside FastAPI!
    """
    thread = threading.Thread(
        target=scheduler_loop,
        daemon=True,        # Dies when main app dies
        name="ContentScheduler"
    )
    thread.start()
    print("  ✓ Background scheduler started!")
    return thread


# ══════════════════════════════════════════
# TEST
# ══════════════════════════════════════════
if __name__ == "__main__":
    print("⏰ Testing Scheduler")
    print("=" * 40)
    print("\nRunning immediate freshness check...")
    check_and_refresh()
    print("\n✅ Scheduler test complete!")