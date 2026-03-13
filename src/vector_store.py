# src/vector_store.py
# Local embedding + FAISS storage (Render compatible)

import os
import json
import pandas as pd
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ═══════════════════════════════════════
# EMBEDDING MODEL
# ═══════════════════════════════════════

def get_embeddings():
    """Local HuggingFace embedding model"""

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ═══════════════════════════════════════
# LOAD ALL TEXT SOURCES
# ═══════════════════════════════════════

def load_all_text():

    print("\nLoading text from sources...")
    all_text = ""

    # Website text
    website_file = os.path.join(BASE_DIR, "data/scraped/website.txt")

    if os.path.exists(website_file):
        with open(website_file, "r", encoding="utf-8") as f:
            content = f.read()
            all_text += content
            print(f"✓ Loaded website content: {len(content)} chars")

    # PDF chunks
    pdf_chunks_file = os.path.join(BASE_DIR, "data/scraped/chunks.txt")

    if os.path.exists(pdf_chunks_file):
        with open(pdf_chunks_file, "r", encoding="utf-8") as f:
            content = f.read()
            all_text += content
            print(f"✓ Loaded PDF chunks: {len(content)} chars")

    # Faculty contacts
    contacts_file = os.path.join(BASE_DIR, "data/contacts/faculty_contacts.csv")

    if os.path.exists(contacts_file):

        df = pd.read_csv(contacts_file)

        contact_text = "\n\nFACULTY CONTACTS:\n"

        for _, row in df.iterrows():

            contact_text += (
                f"Name: {row['Name']} | "
                f"Department: {row['Department']} | "
                f"Designation: {row['Designation']} | "
                f"Email: {row['Email']} | "
                f"Phone: {row['Phone']} | "
                f"Cabin: {row['Cabin']}\n"
            )

        all_text += contact_text

        print(f"✓ Loaded {len(df)} faculty contacts")

    # Events
    events_file = os.path.join(BASE_DIR, "data/events/events.csv")

    if os.path.exists(events_file):

        df = pd.read_csv(events_file)

        events_text = "\n\nCAMPUS EVENTS:\n"

        for _, row in df.iterrows():

            events_text += (
                f"Event: {row['Event']} | "
                f"Date: {row['Date']} | "
                f"Venue: {row['Venue']} | "
                f"Description: {row['Description']} | "
                f"Registration: {row['Registration']}\n"
            )

        all_text += events_text

        print(f"✓ Loaded {len(df)} campus events")

    # Campus locations
    locations_file = os.path.join(BASE_DIR, "data/locations/campus_map.json")

    if os.path.exists(locations_file):

        with open(locations_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        locations_text = "\n\nCAMPUS LOCATIONS:\n"

        for loc in data["campus_locations"]:

            locations_text += (
                f"Location: {loc['name']} | "
                f"Description: {loc['description']} | "
                f"Block: {loc['block']} | "
                f"Directions: {loc['directions']}\n"
            )

        all_text += locations_text

        print(f"✓ Loaded {len(data['campus_locations'])} campus locations")

    print(f"\nTotal text loaded: {len(all_text)} characters")

    return all_text


# ═══════════════════════════════════════
# SPLIT TEXT INTO CHUNKS
# ═══════════════════════════════════════

def split_text(text):

    print("\nSplitting text into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120
    )

    chunks = splitter.split_text(text)

    print(f"Total chunks created: {len(chunks)}")

    return chunks


# ═══════════════════════════════════════
# CREATE VECTOR STORE
# ═══════════════════════════════════════

def create_vector_store(chunks):

    print("\nCreating embeddings locally...")

    embeddings = get_embeddings()

    vector_store = FAISS.from_texts(
        chunks,
        embeddings
    )

    save_path = os.path.join(BASE_DIR, "data/vector_store")

    os.makedirs(save_path, exist_ok=True)

    vector_store.save_local(save_path)

    print(f"✓ Vector store saved to {save_path}")

    return vector_store


# ═══════════════════════════════════════
# LOAD VECTOR STORE (USED IN API)
# ═══════════════════════════════════════

def load_vector_store():

    save_path = os.path.join(BASE_DIR, "data/vector_store")

    if not os.path.exists(save_path):

        print("✗ Vector store not found!")
        return None

    print("\nLoading FAISS vector store...")

    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("✓ Vector store loaded!")

    return vector_store


# ═══════════════════════════════════════
# TEST
# ═══════════════════════════════════════

if __name__ == "__main__":

    text = load_all_text()

    if not text:
        print("✗ No data found!")
        exit()

    chunks = split_text(text)

    vector_store = create_vector_store(chunks)

    print("\nTesting search...")

    results = vector_store.similarity_search(
        "Where is the placement cell?",
        k=3
    )

    for i, r in enumerate(results):
        print(f"\nResult {i+1}:")
        print(r.page_content[:200])