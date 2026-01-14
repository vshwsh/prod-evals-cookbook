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

## The Stages

### Setup (Get the project running)

| Setup | Folder | What It Does |
|-------|--------|--------------|
| Environment | `setup_environment/` | Docker, dependencies, configuration |
| Seed Data | `setup_seed_data/` | Load fictional company data |
| Agent | `setup_agent/` | Build the Ask Acme agent |

### Evaluation Stages

| Stage | Folder | What It Does |
|-------|--------|--------------|
| 1 | `stage_1_golden_sets/` | Curated input/output pairs |
| 2 | `stage_2_labeled_scenarios/` | Categorized test cases |
| 3 | `stage_3_replay_harnesses/` | Record/replay for deterministic tests |
| 4 | `stage_4_rubrics/` | Multi-dimensional scoring |
| 5 | `stage_5_experiments/` | Compare agent configurations |

## Prerequisites

### Required
- **Python 3.11-3.13** - We use modern Python features (not 3.14 due to Pydantic V1)
- **Docker & Docker Compose** - For running Postgres and MongoDB
- **uv** - For Python dependency management
- **OpenAI API Key** - For embeddings and LLM calls

### Optional but Recommended
- **VS Code or Cursor** - With Python extension
- **Jupyter** - For interactive notebooks

## Quick Setup Check

```bash
# Python version (need 3.11-3.13)
python --version

# Docker
docker --version
docker compose version

# uv
uv --version
```

### Installing uv (if needed)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

## How to Use This Cookbook

Work through the stages **in order**. Each builds on the previous:

```
START_HERE.md                    ← You are here
setup_environment/               ← Next: Get infrastructure running
setup_seed_data/                 ← Load the fictional company data
setup_agent/                     ← Build Ask Acme
stage_1_golden_sets/             ← Start evaluations
stage_2_labeled_scenarios/       ← Categorized testing
stage_3_replay_harnesses/        ← Deterministic testing
stage_4_rubrics/                 ← Quality scoring
stage_5_experiments/             ← Compare configurations
```

Each stage contains:
- **README.md** - Concepts and instructions
- **Code files** - Implementation
- **walkthrough.ipynb** - Interactive exercises (where applicable)

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

## Ready?

Start with environment setup:

```bash
cd setup_environment
cat README.md
```
