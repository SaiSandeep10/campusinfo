# src/vector_store.py
# Uses HuggingFace embeddings (free, local, no API needed!)

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ── Base directory (works on both local and Streamlit Cloud) ──
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ══════════════════════════════════════════
# FUNCTION 1 — Load All Text Sources
# ══════════════════════════════════════════
def load_all_text():
    """Load text from all saved sources"""
    import pandas as pd
    import json

    print("\nLoading text from all sources...")
    all_text = ""

    # ── 1. Website content ──
    website_file = os.path.join(BASE_DIR, "data/scraped/website.txt")
    if os.path.exists(website_file):
        with open(website_file, "r", encoding="utf-8") as f:
            content = f.read()
            all_text += content
            print(f"  ✓ Loaded website content: {len(content)} characters")
    else:
        print("  ✗ No website.txt found. Run scraper.py first!")

    # ── 2. PDF chunks ──
    pdf_chunks_file = os.path.join(BASE_DIR, "data/scraped/chunks.txt")
    if os.path.exists(pdf_chunks_file):
        with open(pdf_chunks_file, "r", encoding="utf-8") as f:
            content = f.read()
            all_text += content
            print(f"  ✓ Loaded PDF chunks: {len(content)} characters")

    # ── 3. Faculty Contacts CSV ──
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
        print(f"  ✓ Loaded {len(df)} faculty contacts")
    else:
        print("  ✗ No faculty_contacts.csv found!")

    # ── 4. Events CSV ──
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
        print(f"  ✓ Loaded {len(df)} campus events")
    else:
        print("  ✗ No events.csv found!")

    # ── 5. Campus Locations JSON ──
    locations_file = os.path.join(BASE_DIR, "data/locations/campus_map.json")
    if os.path.exists(locations_file):
        with open(locations_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        locations_text = "\n\nCAMPUS LOCATIONS:\n"
        for loc in data["campus_locations"]:
            locations_text += (
                f"Campus Location: {loc['name']}. "
                f"Description: {loc['description']}. "
                f"Block: {loc['block']}. "
                f"How to reach: {loc['directions']}\n"
            )
        all_text += locations_text
        print(f"  ✓ Loaded {len(data['campus_locations'])} campus locations")
    else:
        print("  ✗ No campus_map.json found!")

    print(f"  Total text loaded: {len(all_text)} characters")
    return all_text

# ══════════════════════════════════════════
# FUNCTION 2 — Split Text into Chunks
# ══════════════════════════════════════════
def split_text(text):
    """Split big text into smaller chunks"""
    print("\nSplitting text into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = splitter.split_text(text)
    print(f"  Total chunks created: {len(chunks)}")
    return chunks


# ══════════════════════════════════════════
# FUNCTION 3 — Create and Save FAISS Index
# ══════════════════════════════════════════
def create_vector_store(chunks):
    """
    Convert chunks into embeddings using a
    free local HuggingFace model.
    No API key needed!
    """
    print("\nLoading embedding model...")
    print("  (Downloading model first time — ~90MB, takes 1-2 mins)")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    print("  ✓ Embedding model loaded!")
    print("\nBuilding FAISS index...")
    print("  This may take 2-3 minutes for 500+ chunks...")

    vector_store = FAISS.from_texts(chunks, embeddings)

    # ── Fixed path ──
    save_path = os.path.join(BASE_DIR, "data/vector_store")
    os.makedirs(save_path, exist_ok=True)
    vector_store.save_local(save_path)

    print(f"  ✓ Vector store saved to {save_path}")
    return vector_store


# ══════════════════════════════════════════
# FUNCTION 4 — Load Saved FAISS Index
# ══════════════════════════════════════════
def load_vector_store():
    """Load previously saved FAISS index"""

    # ── Fixed path ──
    save_path = os.path.join(BASE_DIR, "data/vector_store")

    if not os.path.exists(save_path):
        print("  ✗ No vector store found! Run vector_store.py first.")
        return None

    print("\nLoading saved vector store...")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    vector_store = FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("  ✓ Vector store loaded!")
    return vector_store


# ══════════════════════════════════════════
# FUNCTION 5 — Query the Vector Store
# ══════════════════════════════════════════
def query_vector_store(vector_store, question, top_k=3):
    """Search for most relevant chunks"""
    print(f"\nSearching for: '{question}'")

    results = vector_store.similarity_search(question, k=top_k)

    print(f"  Found {len(results)} relevant chunks:")
    for i, doc in enumerate(results):
        print(f"\n  --- Result {i+1} ---")
        print(f"  {doc.page_content[:200]}...")

    return results


# ══════════════════════════════════════════
# TEST
# ══════════════════════════════════════════
if __name__ == "__main__":

    text = load_all_text()

    if not text:
        print("\n✗ No text found! Make sure you ran:")
        print("  python src/scraper.py")
        print("  python src/ingest.py")
        exit()

    chunks = split_text(text)
    vector_store = create_vector_store(chunks)

    print("\n" + "=" * 50)
    print("  TESTING WITH SAMPLE QUESTIONS")
    print("=" * 50)

    test_questions = [
        "Where is the placement cell?",
        "What departments are available in ANITS?",
        "What facilities does ANITS have?"
    ]

    for question in test_questions:
        query_vector_store(vector_store, question)

    print("\n✅ vector_store.py working correctly!")
    print("Next step: Run agent.py")