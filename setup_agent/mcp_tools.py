"""
MCP tools for searching Jira tickets and Slack messages.

For this tutorial, we use JSON fixtures instead of actual MCP servers.
In production, these would connect to real Jira/Slack via MCP protocol.
"""

import json
from pathlib import Path
from typing import Any

from langchain_core.tools import tool


# Load fixtures
FIXTURES_PATH = Path(__file__).parent.parent / "setup_seed_data" / "mcp_fixtures"


def load_jira_data() -> dict[str, Any]:
    """Load Jira fixture data."""
    jira_path = FIXTURES_PATH / "jira_tickets.json"
    if jira_path.exists():
        with open(jira_path) as f:
            return json.load(f)
    return {"tickets": [], "projects": [], "sprints": []}


def load_slack_data() -> dict[str, Any]:
    """Load Slack fixture data."""
    slack_path = FIXTURES_PATH / "slack_messages.json"
    if slack_path.exists():
        with open(slack_path) as f:
            return json.load(f)
    return {"channels": [], "users": [], "messages": []}


@tool
def jira_search(query: str) -> str:
    """
    Search Jira tickets for bugs, features, and project work.
    
    Use this tool for questions about:
    - Open bugs and their status
    - Current sprint work
    - Specific tickets or issues
    - Engineering project status
    
    Args:
        query: Search terms or question about Jira tickets
        
    Returns:
        Matching tickets with key details
    """
    data = load_jira_data()
    tickets = data.get("tickets", [])
    
    if not tickets:
        return "No Jira data available."
    
    query_lower = query.lower()
    
    # Simple keyword matching for demo purposes
    # In production, this would use Jira's JQL search
    matched_tickets = []
    
    for ticket in tickets:
        # Check various fields for matches
        searchable = " ".join([
            ticket.get("summary", ""),
            ticket.get("description", ""),
            ticket.get("status", ""),
            ticket.get("priority", ""),
            ticket.get("type", ""),
            " ".join(ticket.get("labels", [])),
        ]).lower()
        
        # Priority filter
        if "p0" in query_lower and ticket.get("priority") == "P0":
            matched_tickets.append(ticket)
        elif "p1" in query_lower and ticket.get("priority") == "P1":
            matched_tickets.append(ticket)
        elif "open" in query_lower and ticket.get("status") in ["Open", "In Progress"]:
            matched_tickets.append(ticket)
        elif "bug" in query_lower and ticket.get("type") == "Bug":
            matched_tickets.append(ticket)
        # General keyword match
        elif any(word in searchable for word in query_lower.split() if len(word) > 3):
            matched_tickets.append(ticket)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tickets = []
    for t in matched_tickets:
        if t["key"] not in seen:
            seen.add(t["key"])
            unique_tickets.append(t)
    
    if not unique_tickets:
        return "No matching tickets found."
    
    # Format results (plain text, no markdown)
    formatted = []
    for ticket in unique_tickets[:5]:  # Limit to 5 results
        formatted.append(
            f"[{ticket['key']}] [{ticket.get('priority', 'N/A')}] [{ticket.get('status', 'Unknown')}]\n"
            f"Type: {ticket.get('type', 'Ticket')}\n"
            f"Summary: {ticket.get('summary', 'No summary')}\n"
            f"Assignee: {ticket.get('assignee') or 'Unassigned'}\n"
            f"Labels: {', '.join(ticket.get('labels', [])) or 'None'}"
        )
    
    return "\n\n".join(formatted)


@tool
def slack_search(query: str) -> str:
    """
    Search Slack messages for discussions and decisions.
    
    Use this tool for questions about:
    - Team discussions and decisions
    - Recent incidents and their resolution
    - Customer feedback shared internally
    - Product or engineering debates
    
    Args:
        query: Search terms or topic to find in Slack
        
    Returns:
        Relevant Slack conversations with context
    """
    data = load_slack_data()
    messages = data.get("messages", [])
    
    if not messages:
        return "No Slack data available."
    
    query_lower = query.lower()
    matched_threads = []
    
    for msg_group in messages:
        channel = msg_group.get("channel", "unknown")
        thread = msg_group.get("thread", [])
        
        # Search through all messages in the thread
        thread_text = " ".join([m.get("text", "") for m in thread]).lower()
        
        # Check for keyword matches
        if any(word in thread_text for word in query_lower.split() if len(word) > 3):
            matched_threads.append({
                "channel": channel,
                "thread": thread,
            })
    
    if not matched_threads:
        return "No matching Slack conversations found."
    
    # Format results (plain text, no markdown)
    formatted = []
    for match in matched_threads[:3]:  # Limit to 3 threads
        channel = match["channel"]
        thread = match["thread"]
        
        thread_lines = [f"#{channel}\n" + "-" * 40]
        for msg in thread:
            user = msg.get("user", "Unknown")
            text = msg.get("text", "").replace("*", "")  # Strip markdown
            ts = msg.get("ts", "")[:10]  # Just the date part
            thread_lines.append(f"{user} ({ts}):\n{text}\n")
        
        formatted.append("\n".join(thread_lines))
    
    return "\n\n".join(formatted)


# For direct testing
if __name__ == "__main__":
    print("Testing Jira Search:")
    print("="*60)
    result = jira_search.invoke({"query": "P0 P1 open bugs"})
    print(result)
    
    print("\n\nTesting Slack Search:")
    print("="*60)
    result = slack_search.invoke({"query": "notifications kafka"})
    print(result)
