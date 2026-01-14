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

## The Evaluation Stages

| Stage | What You'll Learn |
|-------|-------------------|
| **1. Golden Sets** | Curated input/output pairs - your baseline for correctness |
| **2. Labeled Scenarios** | Categorized test cases by complexity and expected behavior |
| **3. Replay Harnesses** | Record and replay for deterministic, reproducible tests |
| **4. Rubrics** | Multi-dimensional scoring with LLM-as-judge |
| **5. Experiments** | Compare agent configurations with data-driven decisions |

## Course Structure

Work through the stages in order. Start with `START_HERE.md` in the root.

```
START_HERE.md                    # Start here - prerequisites and concepts
setup_environment/               # Get Docker, databases, and dependencies running
setup_seed_data/                 # Load the fictional Acme Corp company data
setup_agent/                     # Build Ask Acme step by step
stage_1_golden_sets/             # Baseline correctness
stage_2_labeled_scenarios/       # Coverage mapping
stage_3_replay_harnesses/        # Reproducibility
stage_4_rubrics/                 # Structured scoring
stage_5_experiments/             # Configuration comparison
```

## Quick Start

```bash
# Clone the repo
git clone <repo-url>
cd prod-evals-cookbook

# Read the start guide
cat START_HERE.md

# Then begin with environment setup
cd setup_environment
cat README.md
```

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- Docker & Docker Compose
- OpenAI API key (for embeddings and LLM calls)
- ~2GB disk space for databases

## The Fictional Company

All data is synthetic but realistic. **Acme Corp** is a fictional B2B project management company with:

- 200 employees across Engineering, Product, Sales, CS, and People Ops
- 2,400+ customers and $18M ARR
- 3 years of business data, 45 internal documents, 75 Jira tickets, 200+ Slack messages

This gives you a rich, realistic dataset to query and evaluate against.

## Documentation

- Each stage has its own README with theory and hands-on exercises

## License

MIT
