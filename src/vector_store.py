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
    print("\nLoading text from all sources...")
    all_text = ""

    # Load scraped website content
    website_file = os.path.join(BASE_DIR, "data/scraped/website.txt")
    if os.path.exists(website_file):
        with open(website_file, "r", encoding="utf-8") as f:
            content = f.read()
            all_text += content
            print(f"  ✓ Loaded website content: {len(content)} characters")
    else:
        print("  ✗ No website.txt found. Run scraper.py first!")

    # Load PDF chunks
    pdf_chunks_file = os.path.join(BASE_DIR, "data/scraped/chunks.txt")
    if os.path.exists(pdf_chunks_file):
        with open(pdf_chunks_file, "r", encoding="utf-8") as f:
            content = f.read()
            all_text += content
            print(f"  ✓ Loaded PDF chunks: {len(content)} characters")

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