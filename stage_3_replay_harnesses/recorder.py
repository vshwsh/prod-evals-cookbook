"""
Session recorder for replay harnesses.

Records agent sessions with full tool call history for reproducible evaluation.
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "setup_agent"))

from orchestrator import ask_acme_with_trace


@dataclass
class ToolCall:
    """A recorded tool call."""
    tool_name: str
    arguments: dict[str, Any]
    result: str = ""


@dataclass  
class Session:
    """A recorded agent session."""
    session_id: str
    query: str
    response: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    retrieved_sources: list[str] = field(default_factory=list)
    source_contents: list[str] = field(default_factory=list)
    timestamp: str = ""
    
    # Annotations (added manually for ground truth)
    annotations: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        """Create from dictionary."""
        tool_calls = [
            ToolCall(**tc) if isinstance(tc, dict) else tc
            for tc in data.get("tool_calls", [])
        ]
        return cls(
            session_id=data.get("session_id", ""),
            query=data.get("query", ""),
            response=data.get("response", ""),
            tool_calls=tool_calls,
            retrieved_sources=data.get("retrieved_sources", []),
            source_contents=data.get("source_contents", []),
            timestamp=data.get("timestamp", ""),
            annotations=data.get("annotations", {}),
        )


def extract_sources_from_response(response: str) -> list[str]:
    """Extract source document names mentioned in response."""
    sources = []
    
    # Look for common patterns like [Source: filename.md] or filename.md
    import re
    
    # Pattern: [Source X: filename.md]
    pattern1 = r"\[Source \d+: ([^\]]+)\]"
    matches1 = re.findall(pattern1, response)
    sources.extend(matches1)
    
    # Pattern: filename.md mentioned
    pattern2 = r"(\w+_\w+\.md)"
    matches2 = re.findall(pattern2, response)
    sources.extend(matches2)
    
    return list(set(sources))


def record_session(
    query: str,
    session_id: str | None = None,
    save: bool = True,
) -> Session:
    """
    Record an agent session.
    
    Args:
        query: The query to run
        session_id: Optional ID for the session (auto-generated if not provided)
        save: Whether to save to fixtures directory
        
    Returns:
        Recorded session
    """
    # Generate session ID if not provided
    if not session_id:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create short ID from query
        short_query = "".join(c for c in query[:20] if c.isalnum())
        session_id = f"{short_query}_{timestamp}"
    
    print(f"Recording session: {session_id}")
    print(f"Query: {query}")
    print()
    
    # Run the agent
    trace = ask_acme_with_trace(query)
    
    # Extract tool calls
    tool_calls = []
    for tc in trace.get("tool_calls", []):
        tool_calls.append(ToolCall(
            tool_name=tc["tool"],
            arguments=tc["args"],
            result="",  # We could capture this with more instrumentation
        ))
    
    # Extract sources from response
    retrieved_sources = extract_sources_from_response(trace["response"])
    
    # Create session
    session = Session(
        session_id=session_id,
        query=query,
        response=trace["response"],
        tool_calls=tool_calls,
        retrieved_sources=retrieved_sources,
        source_contents=[],  # Would need deeper instrumentation to capture
        timestamp=datetime.now().isoformat(),
        annotations={},
    )
    
    if save:
        save_session(session)
    
    print(f"Recorded {len(tool_calls)} tool calls")
    print(f"Found {len(retrieved_sources)} source references")
    
    return session


def save_session(session: Session, directory: str = "fixtures") -> Path:
    """Save session to JSON file."""
    fixtures_dir = Path(__file__).parent / directory
    fixtures_dir.mkdir(exist_ok=True)
    
    filepath = fixtures_dir / f"{session.session_id}.json"
    
    with open(filepath, "w") as f:
        json.dump(session.to_dict(), f, indent=2)
    
    print(f"Saved to: {filepath}")
    return filepath


def load_session(session_id: str, directory: str = "fixtures") -> Session:
    """Load session from JSON file."""
    fixtures_dir = Path(__file__).parent / directory
    filepath = fixtures_dir / f"{session_id}.json"
    
    if not filepath.exists():
        raise FileNotFoundError(f"Session not found: {filepath}")
    
    with open(filepath) as f:
        data = json.load(f)
    
    return Session.from_dict(data)


def list_sessions(directory: str = "fixtures") -> list[str]:
    """List all recorded sessions."""
    fixtures_dir = Path(__file__).parent / directory
    
    if not fixtures_dir.exists():
        return []
    
    sessions = []
    for f in fixtures_dir.glob("*.json"):
        sessions.append(f.stem)
    
    return sorted(sessions)


def annotate_session(
    session_id: str,
    relevant_sources: list[str] | None = None,
    expected_tools: list[str] | None = None,
    expected_facts: list[str] | None = None,
) -> Session:
    """
    Add ground truth annotations to a session.
    
    Args:
        session_id: ID of session to annotate
        relevant_sources: Ground truth relevant source documents
        expected_tools: Expected tools that should be called
        expected_facts: Key facts that should appear in response
        
    Returns:
        Updated session
    """
    session = load_session(session_id)
    
    if relevant_sources is not None:
        session.annotations["relevant_sources"] = relevant_sources
    
    if expected_tools is not None:
        session.annotations["expected_tools"] = expected_tools
    
    if expected_facts is not None:
        session.annotations["expected_facts"] = expected_facts
    
    save_session(session)
    print(f"Annotated session: {session_id}")
    
    return session


def main():
    parser = argparse.ArgumentParser(description="Record Ask Acme sessions")
    parser.add_argument("--query", "-q", type=str, help="Query to record")
    parser.add_argument("--id", type=str, help="Session ID")
    parser.add_argument("--list", "-l", action="store_true", help="List recorded sessions")
    args = parser.parse_args()
    
    if args.list:
        sessions = list_sessions()
        print(f"Recorded sessions ({len(sessions)}):")
        for s in sessions:
            print(f"  - {s}")
        return 0
    
    if args.query:
        session = record_session(args.query, session_id=args.id)
        print()
        print(f"Session ID: {session.session_id}")
        print(f"Tools used: {[tc.tool_name for tc in session.tool_calls]}")
        return 0
    
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
