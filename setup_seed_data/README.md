# Seed Data Setup

This lesson loads the fictional Acme Corp data into your databases. By the end, you'll have realistic data to query across all three sources.

## What Gets Loaded

| Source | Data | Purpose |
|--------|------|---------|
| **MongoDB** | 8 documents with embeddings | Vector search for policies & docs |
| **PostgreSQL** | 3 years of business data | SQL queries for metrics |
| **MCP Fixtures** | Jira tickets + Slack messages | Collaboration tool searches |

## The Documents (8 total)

We've created a focused set of documents that demonstrate key use cases:

### Policies (3)
- `remote_work_policy.md` - Work from home guidelines
- `pto_policy.md` - Time off policy
- `refund_policy.md` - Customer refund terms

### Engineering (3)
- `incident_runbook.md` - How to handle production incidents
- `code_review_standards.md` - PR review guidelines
- `oncall_handbook.md` - On-call rotation procedures

### Product (2)
- `roadmap_2025.md` - Product direction and priorities
- `pricing_strategy.md` - Pricing tiers and discounts

## Loading the Data

```bash
# Make sure databases are running
cd ../setup_environment
docker compose up -d

# Load all seed data
cd ../setup_seed_data
uv run python seed_all.py
```

## What the Script Does

1. **Creates PostgreSQL tables** and loads sample business data
2. **Generates embeddings** for each document using OpenAI
3. **Stores documents in MongoDB** with their embeddings
4. **Loads MCP fixtures** for Jira and Slack mock servers

## Verifying the Data

After running the seed script, you can verify:

```bash
# Check MongoDB documents
uv run python -c "
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client.acme
print(f'Documents loaded: {db.documents.count_documents({})}')
"

# Check PostgreSQL tables
docker compose -f ../setup_environment/docker-compose.yml exec postgres \
  psql -U acme -c "SELECT COUNT(*) FROM customers;"
```

## Example Queries These Enable

**Single-tool queries:**
- "What's our remote work policy?" → Vector search
- "How many customers do we have?" → SQL
- "What P0 bugs are open?" → Jira MCP

**Multi-tool queries:**
- "What's our refund policy and how many refunds last quarter?" → Vector + SQL
- "Are there incidents related to auth and what does the runbook say?" → Jira + Vector

## Next Step

Once data is loaded, proceed to build the agent:

```bash
cd ../setup_agent
cat README.md
```
