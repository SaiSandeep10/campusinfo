# src/scraper.py
# Visits ANITS website pages and saves all text content

import requests
from bs4 import BeautifulSoup
import os
import time

# LIST OF ANITS PAGES TO SCRAPE
# Add more pages here anytime you want
PAGES_TO_SCRAPE = [
    "https://www.anits.edu.in/index.html",
    "https://www.anits.edu.in/aboutus.php",
    "https://www.anits.edu.in/depts.php",
    "https://www.anits.edu.in/admissions.php",
    "https://www.anits.edu.in/tpccontact.php",
    "https://www.anits.edu.in/facilities.php",
    "https://www.anits.edu.in/hostel.php",
    "https://www.anits.edu.in/clubs.php",
    "https://www.anits.edu.in/nss.php",
    "https://www.anits.edu.in/contacts.php",
    "https://library.anits.edu.in/",
    "https://cse.anits.edu.in/",
    "https://it.anits.edu.in/",
]


# FUNCTION 1 — Scrape a Single Page
def scrape_page(url):
    """
    Visit one URL and extract all useful text.
    Returns the cleaned text as a string.
    """
    print(f"  Scraping: {url}")

    try:
        # Send request like a real browser
        # (some websites block requests without a User-Agent)
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

        # Check if page loaded successfully
        # Status 200 = OK, anything else = problem
        if response.status_code != 200:
            print(f"  ✗ Could not load page. Status code: {response.status_code}")
            return ""

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # ── Remove unwanted elements ──
        # We don't want navigation menus, scripts, or styling
        for unwanted in soup(["script", "style", "nav","footer", "header", "iframe"]):
            unwanted.decompose()  # completely removes these tags

        # ── Extract useful text ──
        # We only want text from meaningful HTML tags
        useful_tags = ["h1", "h2", "h3", "h4", "p", "li", "td", "th", "span"]
        texts = []

        for tag in soup.find_all(useful_tags):
            text = tag.get_text(strip=True)  # get text, remove extra spaces

            # Only keep text that is long enough to be meaningful
            if len(text) > 25:
                texts.append(text)

        # Join all text pieces with newlines
        page_text = "\n".join(texts)

        print(f"  ✓ Got {len(page_text)} characters")
        return page_text

    except requests.exceptions.ConnectionError:
        print(f"  ✗ Cannot connect. Check your internet connection.")
        return ""

    except requests.exceptions.Timeout:
        print(f"  ✗ Page took too long to load. Skipping.")
        return ""

    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return ""


# FUNCTION 2 — Scrape All Pages
def scrape_all_pages(urls):
    """
    Go through every URL in the list,
    scrape each one, and combine all text.
    Returns one big string with all content.
    """
    print("=" * 50)
    print("  ANITS Website Scraper Starting...")
    print("=" * 50)

    all_text = ""
    success_count = 0

    for url in urls:
        # Add a label showing which page this text came from
        page_text = scrape_page(url)

        if page_text:
            all_text += f"\n\n{'=' * 30}\n"
            all_text += f"SOURCE: {url}\n"
            all_text += f"{'=' * 30}\n"
            all_text += page_text
            success_count += 1

        # Wait 1 second between requests
        # This is called "polite scraping"
        # It avoids overloading the college server
        time.sleep(1)

    print(f"\n  Pages scraped successfully: {success_count}/{len(urls)}")
    print(f"  Total characters collected: {len(all_text)}")
    return all_text


# FUNCTION 3 — Save Scraped Content
def save_scraped_content(text, output_file="data/scraped/website.txt"):
    """
    Save all scraped text to a .txt file
    so we can use it later in vector_store.py
    """
    # Create folder if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\n  Saved to: {output_file}")
    print(f"  File size: {os.path.getsize(output_file)} bytes")


# FUNCTION 4 — Load Saved Content
def load_scraped_content(file_path="data/scraped/website.txt"):
    """
    Load previously scraped content from file.
    Used by vector_store.py to read saved content.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"  Loaded {len(content)} characters from {file_path}")
        return content
    else:
        print(f"  No scraped file found at {file_path}")
        return ""

# TEST — Runs only when you run this file
# directly with: python src/scraper.py
if __name__ == "__main__":

    # Step 1: Scrape all pages
    all_text = scrape_all_pages(PAGES_TO_SCRAPE)

    if all_text:
        # Step 2: Save to file
        save_scraped_content(all_text)

        # Step 3: Show a preview of what was scraped
        print("\n========== PREVIEW (first 600 characters) ==========")
        print(all_text[:600])
        print("...")

        print("\n✅ scraper.py completed successfully!")
        print("Next step: Run vector_store.py to index this content.")

    else:
        print("\n✗ No content was scraped. Check your internet connection.")
        print("  Or the website URLs may have changed.")