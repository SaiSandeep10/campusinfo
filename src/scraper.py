# src/scraper.py
# Advanced ANITS Website Scraper with Metadata & Categorization

import requests
from bs4 import BeautifulSoup
import os
import time
import json
from datetime import datetime

# ══════════════════════════════════════════
# PAGES TO SCRAPE WITH CATEGORIES
# Each page has a category and description
# ══════════════════════════════════════════
PAGES_TO_SCRAPE = [
    {
        "url": "https://www.anits.edu.in/index.html",
        "category": "general",
        "label": "ANITS Home Page"
    },
    {
        "url": "https://www.anits.edu.in/aboutus.php",
        "category": "general",
        "label": "About ANITS"
    },
    {
        "url": "https://www.anits.edu.in/depts.php",
        "category": "academics",
        "label": "Departments"
    },
    {
        "url": "https://www.anits.edu.in/admissions.php",
        "category": "admissions",
        "label": "Admissions"
    },
    {
        "url": "https://www.anits.edu.in/tpccontact.php",
        "category": "placements",
        "label": "Training and Placement Cell"
    },
    {
        "url": "https://www.anits.edu.in/facilities.php",
        "category": "facilities",
        "label": "Campus Facilities"
    },
    {
        "url": "https://www.anits.edu.in/hostel.php",
        "category": "facilities",
        "label": "Hostel Information"
    },
    {
        "url": "https://www.anits.edu.in/clubs.php",
        "category": "clubs",
        "label": "Clubs and Societies"
    },
    {
        "url": "https://www.anits.edu.in/nss.php",
        "category": "clubs",
        "label": "NSS Activities"
    },
    {
        "url": "https://www.anits.edu.in/contacts.php",
        "category": "contacts",
        "label": "Contact Directory"
    },
    {
        "url": "https://library.anits.edu.in/",
        "category": "facilities",
        "label": "Library"
    },
    {
        "url": "https://cse.anits.edu.in/",
        "category": "academics",
        "label": "CSE Department"
    },
    {
        "url": "https://it.anits.edu.in/",
        "category": "academics",
        "label": "IT Department"
    },
]


# ══════════════════════════════════════════
# FUNCTION 1 — Scrape a Single Page
# ══════════════════════════════════════════
def scrape_page(page_info):
    """
    Visit one URL and extract all useful text with metadata.
    Returns dict with text, category, label, timestamp.
    """
    url = page_info["url"]
    category = page_info["category"]
    label = page_info["label"]

    print(f"  [{category.upper()}] Scraping: {label}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url, timeout=10)

        if response.status_code != 200:
            print(f"  ✗ Failed. Status: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for unwanted in soup(["script", "style", "nav", "footer", "header", "iframe"]):
            unwanted.decompose()

        # Extract useful text
        useful_tags = ["h1", "h2", "h3", "h4", "p", "li", "td", "th", "span"]
        texts = []

        for tag in soup.find_all(useful_tags):
            text = tag.get_text(strip=True)
            if len(text) > 25:
                texts.append(text)

        page_text = "\n".join(texts)

        print(f"  ✓ Got {len(page_text)} characters")

        return {
            "url": url,
            "category": category,
            "label": label,
            "text": page_text,
            "scraped_at": datetime.now().isoformat(),
            "char_count": len(page_text)
        }

    except requests.exceptions.ConnectionError:
        print(f"  ✗ Cannot connect. Check internet.")
        return None

    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout. Skipping.")
        return None

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


# ══════════════════════════════════════════
# FUNCTION 2 — Scrape All Pages
# ══════════════════════════════════════════
def scrape_all_pages(pages):
    """
    Scrape all pages and return structured results
    with metadata for each page.
    """
    print("=" * 50)
    print("  ANITS Advanced Scraper Starting...")
    print(f"  Total pages: {len(pages)}")
    print("=" * 50)

    results = []
    success_count = 0

    for page_info in pages:
        result = scrape_page(page_info)

        if result and result["text"]:
            results.append(result)
            success_count += 1

        time.sleep(1)  # polite scraping

    print(f"\n  ✓ Pages scraped: {success_count}/{len(pages)}")
    print(f"  ✓ Total characters: {sum(r['char_count'] for r in results)}")

    return results


# ══════════════════════════════════════════
# FUNCTION 3 — Save Results
# ══════════════════════════════════════════
def save_scraped_content(results, 
                          txt_file="data/scraped/website.txt",
                          json_file="data/scraped/website_metadata.json"):
    """
    Save scraped content in two formats:
    1. Plain TXT for vector store (combined text)
    2. JSON with metadata for advanced search
    """
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)

    # ── Save plain TXT (for vector store) ──
    all_text = ""
    for result in results:
        all_text += f"\n\n{'=' * 30}\n"
        all_text += f"PAGE: {result['label']}\n"
        all_text += f"CATEGORY: {result['category']}\n"
        all_text += f"SOURCE: {result['url']}\n"
        all_text += f"{'=' * 30}\n"
        all_text += result["text"]

    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(all_text)
    print(f"\n  ✓ Saved TXT: {txt_file} ({len(all_text)} chars)")

    # ── Save JSON with metadata ──
    metadata = {
        "scraped_at": datetime.now().isoformat(),
        "total_pages": len(results),
        "categories": list(set(r["category"] for r in results)),
        "pages": results
    }

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Saved JSON: {json_file}")


# ══════════════════════════════════════════
# FUNCTION 4 — Load Saved Content
# ══════════════════════════════════════════
def load_scraped_content(file_path="data/scraped/website.txt"):
    """Load previously scraped content from TXT file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"  ✓ Loaded {len(content)} characters from {file_path}")
        return content
    else:
        print(f"  ✗ No scraped file at {file_path}")
        return ""


# ══════════════════════════════════════════
# FUNCTION 5 — Check Content Freshness
# ══════════════════════════════════════════
def check_freshness(json_file="data/scraped/website_metadata.json"):
    """
    Check when content was last scraped.
    Returns True if content is older than 7 days (needs update).
    """
    if not os.path.exists(json_file):
        print("  ⚠️ No metadata found. Content needs scraping!")
        return True

    with open(json_file, "r") as f:
        metadata = json.load(f)

    scraped_at = datetime.fromisoformat(metadata["scraped_at"])
    age_days = (datetime.now() - scraped_at).days

    print(f"  ℹ️ Content last scraped: {scraped_at.strftime('%Y-%m-%d %H:%M')}")
    print(f"  ℹ️ Content age: {age_days} days")

    if age_days >= 7:
        print("  ⚠️ Content is older than 7 days. Consider re-scraping!")
        return True
    else:
        print("  ✓ Content is fresh!")
        return False


# ══════════════════════════════════════════
# MAIN — Run when called directly
# ══════════════════════════════════════════
if __name__ == "__main__":

    print("\n🌐 ANITS Advanced Web Scraper")
    print("================================\n")

    # Step 1: Check if content needs updating
    needs_update = check_freshness()

    if needs_update:
        # Step 2: Scrape all pages
        results = scrape_all_pages(PAGES_TO_SCRAPE)

        if results:
            # Step 3: Save content
            save_scraped_content(results)

            # Step 4: Preview
            print("\n========== PREVIEW ==========")
            print(results[0]["text"][:400])
            print("...")
            print("\n✅ Scraper completed!")
            print("Next: Run python src/vector_store.py")
        else:
            print("\n✗ No content scraped. Check internet connection.")
    else:
        print("\n✅ Content is fresh! No need to re-scrape.")
        print("   Delete data/scraped/website_metadata.json to force re-scrape.")