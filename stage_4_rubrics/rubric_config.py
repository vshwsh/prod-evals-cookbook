"""
Local configuration for rubric evaluation.

Provides OpenAI client and agent access.
"""

import os
import sys
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI

# Load environment from setup_environment/.env
_env_path = Path(__file__).parent.parent / "setup_environment" / ".env"
if _env_path.exists():
    load_dotenv(_env_path)

# Add agent directory to path FIRST so it finds its own config.py
_agent_dir = Path(__file__).parent.parent / "setup_agent"
if str(_agent_dir) not in sys.path:
    sys.path.insert(0, str(_agent_dir))


@lru_cache()
def get_openai_client() -> OpenAI:
    """Get OpenAI client instance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    return OpenAI(api_key=api_key)


def ask_acme(query: str) -> str:
    """Run a query through the Ask Acme agent."""
    from orchestrator import ask_acme as _ask_acme
    return _ask_acme(query)
