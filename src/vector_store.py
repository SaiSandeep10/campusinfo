import os
from dotenv import load_dotenv
# CHANGED: Use Inference API instead of local HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# ── Base directory ──
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ══════════════════════════════════════════
# NEW: Shared Embedding Instance
# ══════════════════════════════════════════
def get_embeddings():
    """Returns the API-based embedding instance to save RAM."""
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("⚠️ WARNING: HF_TOKEN not found in environment variables!")
    
    return HuggingFaceInferenceAPIEmbeddings(
        api_key=hf_token,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# ... (load_all_text and split_text functions remain exactly the same) ...

# ══════════════════════════════════════════
# FUNCTION 3 — Create and Save FAISS Index
# ══════════════════════════════════════════
def create_vector_store(chunks):
    """
    Now uses CLOUD embeddings. RAM usage: ~10MB 
    instead of 800MB+.
    """
    print("\nConnecting to Hugging Face Inference API...")
    embeddings = get_embeddings()

    print("  ✓ Connected! Sending chunks to cloud for embedding...")
    # This now happens on HF servers, not your Render CPU
    vector_store = FAISS.from_texts(chunks, embeddings)

    save_path = os.path.join(BASE_DIR, "data/vector_store")
    os.makedirs(save_path, exist_ok=True)
    vector_store.save_local(save_path)

    print(f"  ✓ Vector store saved to {save_path}")
    return vector_store

# ══════════════════════════════════════════
# FUNCTION 4 — Load Saved FAISS Index
# ══════════════════════════════════════════
def load_vector_store():
    """Load FAISS index using API-based embeddings"""
    save_path = os.path.join(BASE_DIR, "data/vector_store")

    if not os.path.exists(save_path):
        print("  ✗ No vector store found!")
        return None

    print("\nLoading vector store (Cloud API Mode)...")
    embeddings = get_embeddings()

    # Note: FAISS still loads the 'index' locally, but uses 
    # the API whenever it needs to turn a new question into numbers.
    vector_store = FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("  ✓ Vector store loaded!")
    return vector_store

# ... (rest of the file remains the same) ...