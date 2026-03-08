# src/agent.py
# ANITS Campus Assistant using LCEL (works with LangChain v1.2+)

import os
import sys
import traceback
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from src.vector_store import load_vector_store

load_dotenv()

# ══════════════════════════════════════════
# CAMPUS ASSISTANT PROMPT
# ══════════════════════════════════════════
SYSTEM_PROMPT = """
You are a friendly and helpful campus assistant for ANITS
(Anil Neerukonda Institute of Technology and Sciences),
Visakhapatnam, Andhra Pradesh, India.

Your job is to help students, freshers, and visitors get
accurate information about the college.

Rules you must follow:
1. Only answer based on the context provided below
2. If answer is not in context say:
   "I don't have that information right now. Please visit
   anits.org or contact the college office directly."
3. Keep answers clear, friendly and to the point
4. Include specific details like timings, locations,
   contact numbers whenever available

Context:
{context}
"""


# ══════════════════════════════════════════
# FUNCTION 1 — Build the Agent
# ══════════════════════════════════════════
def build_agent():
    """
    Loads vector store + connects Groq LLM
    Returns a ready-to-use LCEL chain
    """
    print("\nInitializing ANITS Campus Assistant...")

    # Check for API Key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("  ✗ GROQ_API_KEY not found!")
        return None

    # Step 1: Load vector store
    vector_store = load_vector_store()
    if not vector_store:
        print("  ✗ Vector store not found!")
        return None
    print("  ✓ Vector store loaded")

    # Step 2: Create retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    print("  ✓ Retriever ready")

    # Step 3: Initialize Groq LLM
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key,
            temperature=0.3
        )
        print("  ✓ Groq LLM (Llama 3) connected")
    except Exception as e:
        print(f"  ✗ Failed to connect LLM: {e}")
        return None

    # Step 4: Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])

    # Step 5: Helper to format retrieved docs
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Step 6: Build LCEL chain
    chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print("  ✓ LCEL chain built!")
    print("\n  ✅ ANITS Campus Assistant is ready!")
    return chain


# ══════════════════════════════════════════
# FUNCTION 2 — Get Answer
# ══════════════════════════════════════════
def get_response(chain, question):
    """
    Takes a question and returns answer.
    Called by routes for every user message.
    """
    if not question or not question.strip():
        return "Please ask a question!"

    try:
        answer = chain.invoke(question)

        if not answer or len(answer.strip()) == 0:
            return "I don't have specific information about that. Please visit anits.org or contact the college office."

        print(f"\n[Agent] Q: {question}")
        print(f"[Agent] A: {answer[:100]}...")

        return answer

    except Exception as e:
        print(f"[Agent] Error type: {type(e).__name__}")
        print(f"[Agent] Error message: {str(e)}")
        traceback.print_exc()
        return (
            "Sorry, I encountered an error. "
            "Please try again or contact the college office."
        )


# ══════════════════════════════════════════
# FUNCTION 3 — Terminal Chat for Testing
# ══════════════════════════════════════════
def chat_loop(chain):
    """Simple terminal chat for testing"""
    print("\n" + "=" * 55)
    print("   ANITS Campus Assistant — Test Mode")
    print("   Type 'exit' to quit")
    print("=" * 55)

    while True:
        try:
            question = input("\n🎓 You: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break

        if question.lower() in ["exit", "quit", "bye", "q"]:
            print("\nGoodbye! 👋")
            break

        if not question:
            print("Please type a question!")
            continue

        print("\n🤖 Thinking...")
        answer = get_response(chain, question)
        print(f"\n🤖 Assistant: {answer}")
        print("-" * 55)


# ══════════════════════════════════════════
# TEST
# ══════════════════════════════════════════
if __name__ == "__main__":
    chain = build_agent()

    if not chain:
        print("\n✗ Agent failed. Fix errors above first.")
        exit()

    print("\n" + "=" * 55)
    print("   AUTOMATIC TEST QUESTIONS")
    print("=" * 55)

    test_questions = [
        "What departments are available in ANITS?",
        "Where is the placement cell?",
        "What facilities does ANITS have?",
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\nTest {i}: {question}")
        answer = get_response(chain, question)
        print(f"Answer: {answer}")
        print("-" * 55)

    chat_loop(chain)