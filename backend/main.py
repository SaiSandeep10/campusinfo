import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Path setup
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

load_dotenv()

# ----------------------------------------------------
# LIFESPAN HANDLER
# ----------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 Starting ANITS Campus Assistant API...")
    
    # 1. MongoDB check (Low RAM usage)
    try:
        from backend.models.database import db
        if db is not None:
            db.command("ping")
            print("✓ MongoDB connected!")
    except Exception as e:
        print(f"MongoDB error: {e}")

    # 2. IMPORTANT: Skip heavy local processing on Render
    # auto_refresh_if_stale() often triggers a full re-embedding
    # which will CRASH a 512MB server. 
    # Only run this if we aren't in production or if memory allows.
    if os.getenv("RENDER"):
        print("⚠️ Running on Render: Skipping auto_refresh to save RAM.")
    else:
        try:
            from src.freshness import auto_refresh_if_stale
            auto_refresh_if_stale()
            print("✓ Content freshness checked!")
        except Exception as e:
            print(f"Freshness check skipped: {e}")

    yield 
    print("👋 Shutting down...")

app = FastAPI(
    title="ANITS Campus Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

# ----------------------------------------------------
# CORS - Prepare for Production
# ----------------------------------------------------
# Pro-tip: Use an env var for your Vercel URL
allowed_origins = [
    "http://localhost:3000",
    os.getenv("FRONTEND_URL", "*") # Add your Vercel URL to Render Env Vars
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# ROUTES & AGENT IMPORT
# ----------------------------------------------------
from backend.routes.chat import router as chat_router
from backend.routes.history import router as history_router
from backend.routes.search import router as search_router

app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(history_router, prefix="/api", tags=["History"])
app.include_router(search_router, prefix="/api", tags=["Search"])

@app.get("/")
async def root():
    return {"message": "ANITS Campus Assistant API is running!"}

@app.get("/health")
async def health():
    # We check if the HF_TOKEN is present as a proxy for 'ready'
    hf_ready = "configured" if os.getenv("HF_TOKEN") else "missing"
    return {
        "status": "healthy", 
        "embeddings": "HuggingFace-Inference-API",
        "token_status": hf_ready
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)