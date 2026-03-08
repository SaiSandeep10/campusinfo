# src/ingest.py
# Upgraded Track B - Loads PDF + CSV + JSON + Website content

import os
import sys
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_handbooks():
    """Load handbook text files from data/handbooks/"""
    content = ""
    handbooks_dir = os.path.join(BASE_DIR, "data/handbooks")
    
    if not os.path.exists(handbooks_dir):
        print("  ⚠️ No handbooks directory found")
        return ""
    
    # Load all .txt files in handbooks folder
    txt_files = [f for f in os.listdir(handbooks_dir) if f.endswith('.txt')]
    
    if not txt_files:
        print("  ⚠️ No handbook text files found")
        return ""
    
    for filename in txt_files:
        filepath = os.path.join(handbooks_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            file_content = f.read()
        content += f"\n\n=== {filename} ===\n{file_content}"
        print(f"  ✓ Loaded handbook: {filename} ({len(file_content)} characters)")
    
    return content

def load_pdf_chunks():
    """Load existing PDF chunks"""
    chunks_file = os.path.join(BASE_DIR, "data/scraped/chunks.txt")
    if os.path.exists(chunks_file):
        with open(chunks_file, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"  ✓ Loaded PDF chunks: {len(content)} characters")
        return content
    print("  ⚠️ No PDF chunks found")
    return ""

def load_website_content():
    """Load scraped website content"""
    website_file = os.path.join(BASE_DIR, "data/scraped/website.txt")
    if os.path.exists(website_file):
        with open(website_file, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"  ✓ Loaded website content: {len(content)} characters")
        return content
    print("  ⚠️ No website content found")
    return ""

def load_contacts():
    """Load faculty contacts from CSV"""
    contacts_file = os.path.join(BASE_DIR, "data/contacts/faculty_contacts.csv")
    if not os.path.exists(contacts_file):
        print("  ⚠️ No contacts file found")
        return ""

    df = pd.read_csv(contacts_file)
    text = "FACULTY CONTACTS AND DIRECTORY:\n"
    text += "=" * 40 + "\n"

    for _, row in df.iterrows():
        text += f"\nName: {row['Name']}\n"
        text += f"Department: {row['Department']}\n"
        text += f"Designation: {row['Designation']}\n"
        text += f"Email: {row['Email']}\n"
        text += f"Phone: {row['Phone']}\n"
        text += f"Cabin: {row['Cabin']}\n"
        text += "-" * 30 + "\n"

    print(f"  ✓ Loaded {len(df)} contacts: {len(text)} characters")
    return text

def load_events():
    """Load events from CSV"""
    events_file = os.path.join(BASE_DIR, "data/events/events.csv")
    if not os.path.exists(events_file):
        print("  ⚠️ No events file found")
        return ""

    df = pd.read_csv(events_file)
    text = "CAMPUS EVENTS AND ACTIVITIES:\n"
    text += "=" * 40 + "\n"

    for _, row in df.iterrows():
        text += f"\nEvent: {row['Event']}\n"
        text += f"Date: {row['Date']}\n"
        text += f"Venue: {row['Venue']}\n"
        text += f"Description: {row['Description']}\n"
        text += f"Registration: {row['Registration']}\n"
        text += "-" * 30 + "\n"

    print(f"  ✓ Loaded {len(df)} events: {len(text)} characters")
    return text

def load_locations():
    """Load campus locations from JSON"""
    locations_file = os.path.join(BASE_DIR, "data/locations/campus_map.json")
    if not os.path.exists(locations_file):
        print("  ⚠️ No locations file found")
        return ""

    with open(locations_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    text = "CAMPUS LOCATIONS AND MAP:\n"
    text += "=" * 40 + "\n"

    for location in data["campus_locations"]:
        text += f"\nCampus Location: {location['name']}\n"
        text += f"Description: {location['description']}\n"
        text += f"Block: {location['block']}\n"
        text += f"How to reach: {location['directions']}\n"
        text += "-" * 30 + "\n"

    print(f"  ✓ Loaded {len(data['campus_locations'])} locations: {len(text)} characters")
    return text

def main():
    print("📚 Loading all campus data sources...\n")
    
    all_content = ""
    
    # 1. Load PDF chunks
    print("📄 Loading PDF chunks...")
    all_content += load_pdf_chunks()
    
    # 2. Load handbooks and text files
    print("\n📖 Loading handbooks...")
    all_content += load_handbooks()
    
    # 3. Load website content
    print("\n🌐 Loading website content...")
    all_content += load_website_content()
    
    # 4. Load contacts
    print("\n👥 Loading faculty contacts...")
    all_content += load_contacts()
    
    # 5. Load events
    print("\n📅 Loading events...")
    all_content += load_events()
    
    # 6. Load locations
    print("\n🗺️ Loading campus locations...")
    all_content += load_locations()
    
    print(f"\n✅ Total content loaded: {len(all_content)} characters")
    return all_content

if __name__ == "__main__":
    main()
