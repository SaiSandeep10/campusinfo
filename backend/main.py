# backend/main.py
# FastAPI Backend for ANITS Campus Assistant

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn


# ----------------------------------------------------
# Project Path Setup
# ----------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

load_dotenv()

# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------
app = FastAPI(
    title="ANITS Campus Assistant API",
    description="Backend API for ANITS Campus Chatbot",
    version="1.0.0"
)

# ----------------------------------------------------
# CORS (Allow frontend requests)
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# GLOBAL AGENT (Lazy Load)
# ----------------------------------------------------
agent_chain = None


def get_agent():
    """
    Loads AI agent only when first needed.
    Prevents slow startup on cloud platforms.
    """
    global agent_chain

    if agent_chain is None:
        print("⚡ Loading AI Agent...")
        from src.agent import build_agent
        agent_chain = build_agent()
        print("✅ AI Agent Loaded")

    return agent_chain


# ----------------------------------------------------
# STARTUP EVENT
# ----------------------------------------------------
@app.on_event("startup")
async def startup_event():

    print("\n🚀 Starting ANITS Campus Assistant API...")

    # MongoDB test
    try:
        from backend.models.database import db
        if db is not None:
            db.command("ping")
            print("✓ MongoDB connected!")
        else:
            print("✗ MongoDB not connected")
    except Exception as e:
        print("MongoDB error:", e)

    # Content freshness check
    try:
        from src.freshness import auto_refresh_if_stale, save_freshness_timestamp

        save_freshness_timestamp()
        auto_refresh_if_stale()

        print("✓ Content freshness checked!")
    except Exception as e:
        print("Freshness check skipped:", e)


# ----------------------------------------------------
# ROUTES
# ----------------------------------------------------
from backend.routes.chat import router as chat_router
from backend.routes.history import router as history_router
from backend.routes.search import router as search_router

app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(history_router, prefix="/api", tags=["History"])
app.include_router(search_router, prefix="/api", tags=["Search"])


# ----------------------------------------------------
# ROOT ENDPOINT
# ----------------------------------------------------
@app.get("/")
async def root():
    return {
        "message": "ANITS Campus Assistant API is running!",
        "version": "1.0.0",
        "status": "online"
    }


# ----------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------
@app.get("/health")
async def health():

    agent_status = "loaded" if agent_chain else "not_loaded"

    return {
        "status": "healthy",
        "agent": agent_status
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)