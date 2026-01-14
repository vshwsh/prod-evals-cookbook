"""
Session player for replay harnesses.

Replays recorded sessions for deterministic evaluation without LLM calls.
"""

import sys
from pathlib import Path
from typing import Any

from recorder import Session, load_session, list_sessions


def replay_session(session_id: str) -> Session:
    """
    Replay a recorded session.
    
    In replay mode, we use the cached response and tool calls
    instead of making new LLM/tool calls.
    
    Args:
        session_id: ID of session to replay
        
    Returns:
        The replayed session with cached data
    """
    session = load_session(session_id)
    
    print(f"Replaying session: {session_id}")
    print(f"Query: {session.query}")
    print(f"Tools called: {[tc.tool_name for tc in session.tool_calls]}")
    print(f"Response length: {len(session.response)} chars")
    
    return session


def compare_sessions(session_id_1: str, session_id_2: str) -> dict[str, Any]:
    """
    Compare two session recordings.
    
    Useful for checking if behavior changed between runs.
    
    Args:
        session_id_1: First session ID
        session_id_2: Second session ID
        
    Returns:
        Comparison results
    """
    s1 = load_session(session_id_1)
    s2 = load_session(session_id_2)
    
    # Compare queries
    same_query = s1.query == s2.query
    
    # Compare tools
    tools_1 = [tc.tool_name for tc in s1.tool_calls]
    tools_2 = [tc.tool_name for tc in s2.tool_calls]
    same_tools = tools_1 == tools_2
    
    # Compare response (fuzzy - check if similar length and key terms)
    len_diff = abs(len(s1.response) - len(s2.response))
    similar_length = len_diff < 100  # Within 100 chars
    
    # Check for key terms overlap
    words_1 = set(s1.response.lower().split())
    words_2 = set(s2.response.lower().split())
    overlap = len(words_1 & words_2) / max(len(words_1), len(words_2), 1)
    
    return {
        "same_query": same_query,
        "same_tools": same_tools,
        "tools_1": tools_1,
        "tools_2": tools_2,
        "similar_length": similar_length,
        "response_length_diff": len_diff,
        "word_overlap": overlap,
        "likely_same": same_query and same_tools and overlap > 0.7,
    }


def get_session_summary(session_id: str) -> dict[str, Any]:
    """
    Get a summary of a recorded session.
    
    Args:
        session_id: Session ID
        
    Returns:
        Summary dict
    """
    session = load_session(session_id)
    
    return {
        "session_id": session.session_id,
        "query": session.query,
        "response_length": len(session.response),
        "tool_calls": [tc.tool_name for tc in session.tool_calls],
        "retrieved_sources": session.retrieved_sources,
        "timestamp": session.timestamp,
        "has_annotations": bool(session.annotations),
        "annotations": session.annotations,
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Replay Ask Acme sessions")
    parser.add_argument("--session", "-s", type=str, help="Session ID to replay")
    parser.add_argument("--compare", nargs=2, help="Compare two sessions")
    parser.add_argument("--list", "-l", action="store_true", help="List all sessions")
    args = parser.parse_args()
    
    if args.list:
        sessions = list_sessions()
        print(f"Recorded sessions ({len(sessions)}):")
        for s in sessions:
            summary = get_session_summary(s)
            print(f"\n  {s}:")
            print(f"    Query: {summary['query'][:50]}...")
            print(f"    Tools: {summary['tool_calls']}")
            print(f"    Annotated: {summary['has_annotations']}")
        return 0
    
    if args.session:
        session = replay_session(args.session)
        print()
        print("Response:")
        print("-" * 40)
        print(session.response)
        return 0
    
    if args.compare:
        result = compare_sessions(args.compare[0], args.compare[1])
        print("Comparison:")
        print("-" * 40)
        for key, value in result.items():
            print(f"  {key}: {value}")
        return 0
    
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
