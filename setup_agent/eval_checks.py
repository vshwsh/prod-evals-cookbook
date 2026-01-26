#!/usr/bin/env python3
"""
Shared evaluation check functions for Ask Acme evaluators.

These functions are used by both golden set and labeled scenario evaluators.
"""


def check_tools(expected: list[str], actual: list[str]) -> tuple[bool, str]:
    """Check if the correct tools were used."""
    if not expected:
        # No tools expected - pass if no tools were used
        if not actual:
            return True, ""
        return False, f"Expected no tools, but used: {actual}"
    
    expected_set = set(expected)
    actual_set = set(actual)
    
    missing = expected_set - actual_set
    
    if missing:
        return False, f"Missing tools: {list(missing)}"
    
    return True, ""


def check_sources(expected: list[str], response: str) -> tuple[bool, str]:
    """Check if expected sources are mentioned in response."""
    if not expected:
        return True, ""
    
    response_lower = response.lower()
    missing = []
    
    for source in expected:
        # Check if source filename is mentioned
        source_lower = source.lower().replace(".md", "").replace("_", " ")
        if source_lower not in response_lower and source.lower() not in response_lower:
            missing.append(source)
    
    if missing:
        return False, f"Missing sources: {missing}"
    
    return True, ""


def check_must_contain(keywords: list[str], response: str) -> tuple[bool, str]:
    """Check if response contains required keywords."""
    if not keywords:
        return True, ""
    
    response_lower = response.lower()
    missing = []
    
    for keyword in keywords:
        if keyword.lower() not in response_lower:
            missing.append(keyword)
    
    if missing:
        return False, f"Missing keywords: {missing}"
    
    return True, ""


def check_must_not_contain(forbidden: list[str], response: str) -> tuple[bool, str]:
    """Check that response does not contain forbidden phrases."""
    if not forbidden:
        return True, ""
    
    response_lower = response.lower()
    found = []
    
    for phrase in forbidden:
        if phrase.lower() in response_lower:
            found.append(phrase)
    
    if found:
        return False, f"Found forbidden phrases: {found}"
    
    return True, ""

