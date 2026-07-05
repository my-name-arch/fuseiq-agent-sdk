# LangChain + FuseIQ Example

Wraps a simple LangChain ReAct agent with FuseIQ monitoring so its status
shows up live in your FuseIQ dashboard.

## Prerequisites

- Python 3.9+
- A FuseIQ API key — get one at [fuseiq.io/quick-start](https://fuseiq.io/quick-start)
- An OpenAI API key (or swap `ChatOpenAI` for another LangChain-supported model)

## Install

```bash
pip install fuseiq-agent langchain langchain-openai
```

## Run

```bash
export FUSEIQ_API_KEY="fk_live_your_key"
export OPENAI_API_KEY="sk-your_key"
python langchain-agent.py
```

## What it does

1. Creates a `FuseIQAgent` and sends an `"online"` heartbeat.
2. Builds a minimal LangChain ReAct agent with one tool.
3. Streams the agent's steps, sending a `"busy"` heartbeat every
   `HEARTBEAT_EVERY_N_STEPS` steps and logging each step via `agent.log(...)`.
4. Sends an `"idle"` heartbeat when done and prints the result.

View live status at [fuseiq.io/dashboard](https://fuseiq.io/dashboard).
