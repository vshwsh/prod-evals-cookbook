# Environment Setup

This lesson gets your development environment ready with all the infrastructure Ask Acme needs.

## What We're Setting Up

| Component | Purpose | How |
|-----------|---------|-----|
| **PostgreSQL** | Analytics database (customer data, metrics) | Docker |
| **MongoDB** | Vector search (documents with embeddings) | Docker |
| **Python Environment** | Dependencies, LangChain, LangGraph | uv |

## Step 1: Start the Databases

Make sure Docker is running, then:

```bash
# From this directory (setup_environment)
docker compose up -d
```

This starts:
- **PostgreSQL** on port `5432` (user: `acme`, password: `acme`, database: `acme`)
- **MongoDB** on port `27017` (no auth for local dev)

Verify they're running:

```bash
docker compose ps
```

You should see both containers with status "running".

### Connecting to the Databases

**PostgreSQL:**
```bash
# Using psql
docker compose exec postgres psql -U acme -d acme

# Or with any Postgres client
# Host: localhost, Port: 5432, User: acme, Password: acme, Database: acme
```

**MongoDB:**
```bash
# Using mongosh
docker compose exec mongodb mongosh

# Or with any MongoDB client
# Connection string: mongodb://localhost:27017
```

## Step 2: Set Up Python Environment

```bash
# Go to project root (if not already there)
cd /path/to/prod-evals-cookbook

# Install dependencies with uv (creates .venv automatically)
uv sync

# Activate the virtual environment
source .venv/bin/activate

# Or run commands directly without activating
uv run python my_script.py
```

> **Note:** The `pyproject.toml` is in the project root, so always run `uv sync` from there.

## Step 3: Configure Environment Variables

Copy the example environment file:

```bash
cp env.example .env
```

Edit `.env` and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-key-here
```

## Step 4: Verify Everything Works

Run the verification script:

```bash
# From this directory (setup_environment)
uv run python verify_setup.py
```

You should see:
```
✓ PostgreSQL connection successful
✓ MongoDB connection successful
✓ OpenAI API key configured
✓ All dependencies installed

Ready to proceed to seed data setup!
```

## Troubleshooting

### Docker Issues

**"Cannot connect to Docker daemon"**
- Make sure Docker Desktop is running

**"Port already in use"**
- Another service is using port 5432 or 27017
- Either stop that service or modify the ports in `docker-compose.yml`

### uv Issues

**"Command not found: uv"**
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Or with Homebrew: `brew install uv`

**"Python version not found"**
- uv can install Python for you: `uv python install 3.11`

### OpenAI API Key

**"Invalid API key"**
- Double-check your key at https://platform.openai.com/api-keys
- Make sure there are no extra spaces in your `.env` file

## Stopping the Databases

When you're done working:

```bash
docker compose down
```

To also remove the data volumes (start fresh):

```bash
docker compose down -v
```

## Next Step

Once everything is verified, proceed to load the seed data:

```bash
cd ../setup_seed_data
cat README.md
```
