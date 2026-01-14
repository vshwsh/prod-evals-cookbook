# Agent Setup

In this lesson, you'll build **Ask Acme** - a LangGraph agent that answers questions by routing to the right data sources.

## Architecture

```
                          User Query
                               │
                               ▼
                    ┌──────────────────┐
                    │     ROUTER       │
                    │  (decides which  │
                    │   tools to use)  │
                    └────────┬─────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │   Vector    │   │    SQL      │   │    MCP      │
    │   Search    │   │   Agent     │   │   Tools     │
    │  (MongoDB)  │   │ (Postgres)  │   │(Jira/Slack) │
    └─────────────┘   └─────────────┘   └─────────────┘
           │                 │                 │
           └─────────────────┼─────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   SYNTHESIZER    │
                    │ (combines results│
                    │  into response)  │
                    └──────────────────┘
```

## Files in This Lesson

| File | Purpose |
|------|---------|
| `vector_search.py` | Search documents in MongoDB using embeddings |
| `sql_agent.py` | Convert natural language to SQL and execute |
| `mcp_tools.py` | Search Jira tickets and Slack messages |
| `orchestrator.py` | LangGraph agent that coordinates everything |
| `config.py` | Configuration and environment loading |
| `demo.ipynb` | Interactive notebook to try the agent |

## How It Works

### 1. Router (Query Classification)

The router LLM decides which tools are needed based on the query:

```python
# Example routing decisions:
"What's our PTO policy?" → ["vector_search"]
"How many customers last month?" → ["sql_agent"]
"What P0 bugs are open?" → ["jira_search"]
"Refund policy and count?" → ["vector_search", "sql_agent"]
```

### 2. Tool Execution

Tools run in parallel when possible:

- **Vector Search**: Embeds the query, finds similar documents in MongoDB
- **SQL Agent**: Converts question to SQL, executes against Postgres
- **MCP Tools**: Searches Jira/Slack fixtures for relevant information

### 3. Synthesis

The synthesizer LLM combines all tool results into a coherent response, citing sources appropriately.

## Running the Agent

### Interactive Demo

```bash
# Make sure databases are running and seeded
cd ../setup_environment && docker compose up -d
cd ../setup_seed_data && uv run python seed_all.py

# Run the demo
cd ../setup_agent
uv run jupyter notebook demo.ipynb
```

### Command Line

```python
from orchestrator import ask_acme

response = ask_acme("What's our remote work policy?")
print(response)
```

## LangSmith Integration

This agent is instrumented with LangSmith for observability. To enable:

1. Get a LangSmith API key from https://smith.langchain.com
2. Add to your `.env`:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-key-here
LANGCHAIN_PROJECT=ask-acme
```

3. Run queries and view traces in the LangSmith dashboard

## Example Queries

Try these queries to test different tools:

**Vector Search (documents)**
- "What's our remote work policy?"
- "How do I handle a production incident?"
- "What are the code review requirements?"

**SQL Agent (metrics)**
- "How many active customers do we have?"
- "What's our MRR?"
- "How many refunds were processed in Q4 2024?"

**MCP Tools (collaboration)**
- "What P0 or P1 bugs are open?"
- "What did engineering decide about notifications?"
- "Any customer feedback about mobile performance?"

**Multi-tool (orchestration)**
- "What's our refund policy and how many refunds did we process last quarter?"
- "Are there open bugs related to auth and what does the incident runbook say?"

## Next Step

Once the agent is working, proceed to evaluations:

```bash
cd ../stage_1_golden_sets
cat README.md
```
