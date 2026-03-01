# app.py
# Streamlit Interface for ANITS Campus Assistant

import streamlit as st
import os
import sys

# Ensure project root is accessible
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from src.agent import build_agent, get_response

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ANITS Campus Assistant",
    page_icon="🎓",
    layout="centered"
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🎓 ANITS Campus Assistant")
st.markdown(
    "Welcome to the AI-powered campus assistant for **ANITS**.\n"
    "Ask me anything about departments, facilities, admissions, placements, etc."
)

# ─────────────────────────────────────────────
# LOAD API KEY (Streamlit Cloud Compatible)
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# LOAD API KEY (Works both locally and on Streamlit Cloud)
# ─────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()  # loads from .env file locally

# If running on Streamlit Cloud, load from st.secrets
try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass  # running locally, .env file is used instead

# ─────────────────────────────────────────────
# LOAD AGENT (Only Once)
# ─────────────────────────────────────────────
@st.cache_resource
def load_chain():
    return build_agent()

chain = load_chain()

if not chain:
    st.error("⚠️ Agent failed to initialize.")
    
    # Show debug info
    st.write("**Debug Info:**")
    st.write(f"GROQ_API_KEY exists: {bool(os.getenv('GROQ_API_KEY'))}")
    st.write(f"Vector store exists: {os.path.exists('data/vector_store')}")
    st.write(f"Current directory: {os.getcwd()}")
    st.stop()

# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─────────────────────────────────────────────
# USER INPUT
# ─────────────────────────────────────────────
if prompt := st.chat_input("Ask your question about ANITS..."):

    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):
            response = get_response(chain, prompt)
            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )