# src/agent_manager.py

from src.agent import build_agent

agent_chain = None


def get_agent():
    global agent_chain

    if agent_chain is None:
        print("⚡ Loading AI agent...")
        agent_chain = build_agent()

    return agent_chain