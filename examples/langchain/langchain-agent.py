"""LangChain Integration — Wrap a LangChain agent with FuseIQ.

Install: pip install fuseiq-agent langchain langchain-openai
Run:     export FUSEIQ_API_KEY="fk_live_..." && export OPENAI_API_KEY="sk-..." && python langchain-agent.py
"""
import os

from fuseiq_agent import FuseIQAgent

HEARTBEAT_EVERY_N_STEPS = 2

# Connect to FuseIQ dashboard
agent = FuseIQAgent(
    api_key=os.environ["FUSEIQ_API_KEY"],
    name="LangChain Researcher",
    framework="LangChain",
)

# Send heartbeat when agent starts
agent.heartbeat("online", task="LangChain agent initialized")

try:
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain_core.prompts import PromptTemplate
    from langchain_core.tools import Tool
    from langchain_openai import ChatOpenAI

    def word_count(text: str) -> str:
        return str(len(text.split()))

    tools = [
        Tool(
            name="WordCount",
            func=word_count,
            description="Counts the number of words in a piece of text.",
        )
    ]

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = PromptTemplate.from_template(
        "Answer the question as best you can. You have access to: {tools}\n"
        "Use the format:\nQuestion: {input}\n{agent_scratchpad}"
    )

    react_agent = create_react_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True)

    agent.heartbeat("busy", task="Running LangChain agent...")

    step = 0
    result = None
    for chunk in executor.stream({"input": "How many words are in 'FuseIQ connects agents to dashboards'?"}):
        step += 1
        if step % HEARTBEAT_EVERY_N_STEPS == 0:
            agent.heartbeat("busy", task=f"Step {step}")
        agent.log(f"Step {step}: {chunk}")
        result = chunk

    agent.heartbeat("idle", task="Research complete")
    print("✅ LangChain agent finished. Result:", result)

except ImportError:
    agent.heartbeat("offline", task="LangChain not installed")
    print("Install LangChain: pip install langchain langchain-openai")
