# Production Evals Cookbook

Welcome to the **Production Evals Cookbook**! This hands-on tutorial teaches you how to build production-ready AI evaluations through progressive stages.

## What You'll Build

**Ask Acme** is an AI agent that answers questions about a company by intelligently routing queries to the right data sources:

- **Vector Search** → Company documents, policies, runbooks
- **SQL Agent** → Business metrics, customer data, analytics
- **MCP Tools** → Jira tickets, Slack conversations

By the end of this cookbook, you'll have:
1. A working multi-tool AI agent
2. A comprehensive evaluation framework
3. Practical patterns you can apply to your own systems

## Prerequisites

Before you begin, make sure you have:

### Required
- **Python 3.11-3.13** - We use modern Python features (not 3.14 due to Pydantic V1)
- **Docker & Docker Compose** - For running Postgres and MongoDB
- **uv** - For Python dependency management
- **OpenAI API Key** - For embeddings and LLM calls

### Quick Check

```bash
# Python version (need 3.11-3.13)
python --version

# Docker
docker --version
docker compose version

# uv (install with: curl -LsSf https://astral.sh/uv/install.sh | sh)
uv --version
```

## Getting Started: Setup (Do These First!)

Before running any evaluations, you must complete these three setup steps **in order**:

### Step 1: Environment Setup
Start Docker containers for Postgres and MongoDB, install Python dependencies, and configure your API keys.

```bash
cd setup_environment
cat README.md      # Read the instructions
docker compose up -d
cd .. && uv sync   # Install Python dependencies
```

### Step 2: Seed the Data
Load Acme Corp's fictional company data into the databases.

```bash
cd setup_seed_data
cat README.md      # Read the instructions
uv run python seed_all.py
```

### Step 3: Build the Agent
Explore the Ask Acme agent and verify it's working.

```bash
cd setup_agent
cat README.md      # Read the instructions
uv run jupyter notebook demo.ipynb
```

Once these three steps are complete, you're ready for the evaluation stages!

---

## Evaluation Stages

After setup is complete, work through these evaluation stages in order:

| Stage | Folder | What You'll Learn |
|-------|--------|-------------------|
| 1 | `stage_1_golden_sets/` | Curated input/output pairs - baseline correctness |
| 2 | `stage_2_labeled_scenarios/` | Categorized test cases - coverage mapping |
| 3 | `stage_3_replay_harnesses/` | Record/replay - reproducibility + rich metrics |
| 4 | `stage_4_rubrics/` | Multi-dimensional scoring with LLM-as-judge |
| 5 | `stage_5_experiments/` | Compare agent configurations with data |

---

## Full Directory Structure

```
START_HERE.md                    ← You are here

# Setup (do these first, in order)
setup_environment/               ← Step 1: Docker, dependencies, API keys
setup_seed_data/                 ← Step 2: Load company data
setup_agent/                     ← Step 3: Build and test the agent

# Evaluation stages (after setup is complete)
stage_1_golden_sets/             ← Start evaluations here
stage_2_labeled_scenarios/       ← Categorized testing
stage_3_replay_harnesses/        ← Deterministic testing
stage_4_rubrics/                 ← Quality scoring
stage_5_experiments/             ← Compare configurations
```

Each folder contains:
- **README.md** - Concepts and instructions
- **Code files** - Implementation
- **walkthrough.ipynb** - Interactive exercises (where applicable)

---

## The Fictional Company: Acme Corp

All data in this cookbook is **synthetic**. We've created a complete fictional company:

| Attribute | Value |
|-----------|-------|
| **Name** | Acme Corp |
| **Product** | "Acme Projects" - B2B project management platform |
| **Employees** | ~200 people |
| **Customers** | 2,400+ companies |
| **ARR** | $18M |

You'll query Acme Corp's:
- HR policies and engineering docs
- 3 years of business metrics
- Jira tickets and Slack conversations

---

## Ready?

Start with **Step 1: Environment Setup**:

```bash
cd setup_environment
cat README.md
```
