# backend/main.py
# FastAPI Backend for ANITS Campus Assistant

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

load_dotenv()

from src.agent import build_agent, get_response
from backend.routes.chat import router as chat_router
from backend.routes.history import router as history_router
from backend.routes.search import router as search_router

# ══════════════════════════════════════════
# CREATE FASTAPI APP
# ══════════════════════════════════════════
app = FastAPI(
    title="ANITS Campus Assistant API",
    description="Backend API for ANITS Campus Chatbot",
    version="1.0.0"
)

# ══════════════════════════════════════════
# CORS MIDDLEWARE
# ══════════════════════════════════════════
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ══════════════════════════════════════════
# LOAD AI AGENT ON STARTUP
# ══════════════════════════════════════════
@app.on_event("startup")
async def startup_event():
    print("\n🚀 Starting ANITS Campus Assistant API...")

    # Test MongoDB connection
    try:
        from backend.models.database import db
        if db is not None:
            db.command("ping")
            print("  ✓ MongoDB connected!")
        else:
            print("  ✗ MongoDB connection failed!")
    except Exception as e:
        print(f"  ✗ MongoDB error: {e}")

    # Check content freshness
    try:
        from src.freshness import auto_refresh_if_stale, save_freshness_timestamp
        save_freshness_timestamp()
        auto_refresh_if_stale()
        print("  ✓ Content freshness checked!")
    except Exception as e:
        print(f"  ⚠️ Freshness check skipped: {e}")

    # Load AI agent
    app.state.chain = build_agent()
    
    if app.state.chain:
        print("  ✅ AI Agent loaded successfully!")
    else:
        print("  ✗ AI Agent failed to load!")

# ══════════════════════════════════════════
# INCLUDE ROUTES
# ══════════════════════════════════════════
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(history_router, prefix="/api", tags=["History"])
app.include_router(search_router, prefix="/api", tags=["Search"])

# ══════════════════════════════════════════
# ROOT ENDPOINT
# ══════════════════════════════════════════
@app.get("/")
async def root():
    return {
        "message": "ANITS Campus Assistant API is running!",
        "version": "1.0.0",
        "status": "online"
    }

# ══════════════════════════════════════════
# HEALTH CHECK
# ══════════════════════════════════════════
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "agent": "loaded" if app.state.chain else "failed"
    }
