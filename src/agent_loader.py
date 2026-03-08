# src/agent_loader.py
# Lazy loader for AI agent

agent_chain = None

def get_agent():
    global agent_chain

    if agent_chain is None:
        print("⚡ Loading AI Agent...")
        from src.agent import build_agent
        agent_chain = build_agent()
        print("✅ AI Agent loaded!")

    return agent_chain