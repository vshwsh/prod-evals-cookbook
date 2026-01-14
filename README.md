# 🎯 Ask Acme - Production Evals Cookbook

> Learn how to build production-ready AI evaluations through 5 progressive stages, using a realistic knowledge base agent as the teaching example.

## What Is This?

This is a **hands-on tutorial** that teaches you how to evaluate AI systems properly. Instead of toy examples, you'll work with a realistic system: **Ask Acme** - an AI agent that answers questions about a company by searching across documents, databases, and collaboration tools.

**You'll learn:**
- How to build a multi-tool AI agent with LangGraph
- The 5 stages of production-ready evaluations
- Practical patterns you can apply to your own systems

## The Example System

```
         "What's our refund policy and how many refunds last quarter?"
                                    │
                                    ▼
                          ┌─────────────────┐
                          │    ASK ACME     │
                          │   (LangGraph)   │
                          └────────┬────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
       ┌────────────┐       ┌────────────┐       ┌────────────┐
       │   Vector   │       │    SQL     │       │    MCP     │
       │   Search   │       │   Agent    │       │   Tools    │
       │ (policies) │       │ (metrics)  │       │(Jira/Slack)│
       └────────────┘       └────────────┘       └────────────┘
```

## Quick Start

### 1. Clone and check prerequisites

```bash
git clone <repo-url>
cd prod-evals-cookbook

# Verify you have the required tools
python --version    # Need 3.11-3.13
docker --version    # Need Docker running
uv --version        # Need uv installed
```

### 2. Complete the setup steps (in order!)

```bash
# Step 1: Start databases and install dependencies
cd setup_environment
docker compose up -d
cd .. && uv sync
cp setup_environment/env.example setup_environment/.env
# Edit .env and add your OPENAI_API_KEY

# Step 2: Load company data
cd setup_seed_data
uv run python seed_all.py

# Step 3: Try the agent
cd ../setup_agent
uv run jupyter notebook demo.ipynb
```

### 3. Start the evaluation stages

```bash
cd stage_1_golden_sets
uv run python evaluator.py
```

## Course Structure

### Setup (Complete These First)

| Step | Folder | What To Do |
|------|--------|------------|
| 1 | `setup_environment/` | Start Docker, install deps, configure API keys |
| 2 | `setup_seed_data/` | Load Acme Corp data into databases |
| 3 | `setup_agent/` | Build and test the Ask Acme agent |

### Evaluation Stages

| Stage | Folder | What You'll Learn |
|-------|--------|-------------------|
| 1 | `stage_1_golden_sets/` | Curated input/output pairs - baseline correctness |
| 2 | `stage_2_labeled_scenarios/` | Categorized test cases - coverage mapping |
| 3 | `stage_3_replay_harnesses/` | Record/replay - reproducibility |
| 4 | `stage_4_rubrics/` | Multi-dimensional scoring with LLM-as-judge |
| 5 | `stage_5_experiments/` | Compare agent configurations with data |

## Prerequisites

- Python 3.11-3.13
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- Docker & Docker Compose
- OpenAI API key (for embeddings and LLM calls)
- ~2GB disk space for databases

## The Fictional Company

All data is synthetic but realistic. **Acme Corp** is a fictional B2B project management company with:

- 200 employees across Engineering, Product, Sales, CS, and People Ops
- 2,400+ customers and $18M ARR
- 3 years of business data, 8 internal documents, 75 Jira tickets, 200+ Slack messages

This gives you a rich, realistic dataset to query and evaluate against.

## Documentation

- See `START_HERE.md` for detailed setup instructions
- Each stage has its own README with theory and hands-on exercises

## License

MIT
