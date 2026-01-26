# Dockerfile for Ask Acme - Production Evals Cookbook
#
# This provides an alternative to local uv installation.
# Use with docker-compose.yml for the complete setup.

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files first for layer caching
# README.md is required by hatchling build backend (referenced in pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Install all dependencies (including dev and eval groups)
RUN uv sync --all-groups

# Copy the rest of the project
COPY . .

# Set Python path to include the project
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command: run Jupyter notebook server
CMD ["uv", "run", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]


