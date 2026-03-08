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
# LIFESPAN HANDLER (Replaces @app.on_event("startup"))
# ----------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs ON STARTUP
    print("\n🚀 Starting ANITS Campus Assistant API...")
    
    # MongoDB check
    try:
        from backend.models.database import db
        if db is not None:
            db.command("ping")
            print("✓ MongoDB connected!")
    except Exception as e:
        print(f"MongoDB error: {e}")

    # Freshness check
    try:
        from src.freshness import auto_refresh_if_stale, save_freshness_timestamp
        save_freshness_timestamp()
        auto_refresh_if_stale()
        print("✓ Content freshness checked!")
    except Exception as e:
        print(f"Freshness check skipped: {e}")

    yield # --- App is running ---

    # This runs ON SHUTDOWN
    print("👋 Shutting down...")

# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------
app = FastAPI(
    title="ANITS Campus Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS (Fixed: origins cannot be "*" if allow_credentials is True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Add your Vercel URL here
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

# Safely import agent_chain for the health check
try:
    from src.agent_manager import get_agent
    # Assuming get_agent() or similar initializes your chain
except ImportError:
    pass

app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(history_router, prefix="/api", tags=["History"])
app.include_router(search_router, prefix="/api", tags=["Search"])

@app.get("/")
async def root():
    return {"message": "ANITS Campus Assistant API is running!"}

@app.get("/health")
async def health():
    # 'agent_chain' isn't defined in the scope of this function 
    # unless it's imported or declared global.
    agent_status = "loaded" if 'agent_chain' in globals() else "not_loaded"
    return {"status": "healthy", "agent": agent_status}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)