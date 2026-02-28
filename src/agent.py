# src/agent.py

import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# ==========================================================
# 1️⃣ LOAD VECTOR STORE
# ==========================================================

def load_vector_store():
    """Load saved FAISS vector database"""

    save_path = "data/vector_store"

    if not os.path.exists(save_path):
        st.error("❌ Vector store not found! Run vector_store.py first.")
        return None

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    vector_store = FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


# ==========================================================
# 2️⃣ CREATE RAG RETRIEVAL CHAIN (Dual Track – PDF + Website)
# ==========================================================

def get_retriever():
    """Return retriever from FAISS"""

    vector_store = load_vector_store()

    if vector_store is None:
        return None

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    return retriever


# ==========================================================
# 3️⃣ BUILD CHATBOT ENGINE
# ==========================================================

def ask_question(question):
    """Retrieve relevant docs + Ask Gemini"""

    retriever = get_retriever()

    if retriever is None:
        return "Vector database not loaded."

    # Get relevant context from FAISS
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    # ======================================================
    # Gemini LLM (Your Brain 🧠)
    # ======================================================

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3
    )

    # Prompt Engineering (Very Important)
    prompt = f"""
You are an AI assistant for ANITS College.

Use the given context to answer the question.
If the answer is not in the context, say:
"Answer not found in provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content


# ==========================================================
# 4️⃣ STREAMLIT CHATBOT UI
# ==========================================================

def main():

    st.set_page_config(page_title="ANITS Campus AI Agent", layout="wide")

    st.title("🎓 ANITS Interactive Campus AI Agent")
    st.markdown("Dual Track Version – PDF + Website Knowledge Base")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask anything about campus...")

    if user_input:

        # Get AI Response
        answer = ask_question(user_input)

        # Save Conversation
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Bot", answer))

    # Display Chat
    for role, message in st.session_state.chat_history:
        if role == "User":
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)


# ==========================================================
# RUN APP
# ==========================================================

if __name__ == "__main__":
    main()