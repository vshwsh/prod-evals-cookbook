#!/usr/bin/env python3
"""
Golden Set Evaluator for Ask Acme.

Runs curated test cases and reports pass/fail results.
"""

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "setup_agent"))

from orchestrator import ask_acme_with_trace


@dataclass
class TestResult:
    """Result of a single test case."""
    id: str
    query: str
    passed: bool
    tool_check: bool | None = None
    source_check: bool | None = None
    content_check: bool | None = None
    negative_check: bool | None = None
    errors: list[str] = field(default_factory=list)
    response: str = ""
    tools_used: list[str] = field(default_factory=list)


def load_golden_set(path: str = "golden_data.yaml") -> list[dict[str, Any]]:
    """Load golden set from YAML file."""
    yaml_path = Path(__file__).parent / path
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return data.get("test_cases", [])


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


def run_test_case(test_case: dict[str, Any], verbose: bool = False) -> TestResult:
    """Run a single test case and return the result."""
    test_id = test_case.get("id", "unknown")
    query = test_case.get("query", "")
    
    result = TestResult(id=test_id, query=query, passed=False)
    
    try:
        # Run the agent
        trace = ask_acme_with_trace(query)
        result.response = trace["response"]
        result.tools_used = [tc["tool"] for tc in trace["tool_calls"]]
        
        # Check tools
        expected_tools = test_case.get("expected_tools", [])
        tool_ok, tool_err = check_tools(expected_tools, result.tools_used)
        result.tool_check = tool_ok
        if not tool_ok:
            result.errors.append(tool_err)
        
        # Check sources
        expected_sources = test_case.get("expected_sources", [])
        if expected_sources:
            source_ok, source_err = check_sources(expected_sources, result.response)
            result.source_check = source_ok
            if not source_ok:
                result.errors.append(source_err)
        
        # Check must_contain
        must_contain = test_case.get("must_contain", [])
        if must_contain:
            content_ok, content_err = check_must_contain(must_contain, result.response)
            result.content_check = content_ok
            if not content_ok:
                result.errors.append(content_err)
        
        # Check must_not_contain
        must_not_contain = test_case.get("must_not_contain", [])
        if must_not_contain:
            negative_ok, negative_err = check_must_not_contain(must_not_contain, result.response)
            result.negative_check = negative_ok
            if not negative_ok:
                result.errors.append(negative_err)
        
        # Overall pass/fail
        checks = [
            result.tool_check,
            result.source_check,
            result.content_check,
            result.negative_check,
        ]
        # Pass if all non-None checks are True
        result.passed = all(c for c in checks if c is not None)
        
    except Exception as e:
        result.errors.append(f"Exception: {str(e)}")
        result.passed = False
    
    return result


def run_golden_set(
    test_cases: list[dict[str, Any]],
    verbose: bool = False,
    test_id: str | None = None,
) -> list[TestResult]:
    """Run all test cases and return results."""
    results = []
    
    # Filter to specific test if requested
    if test_id:
        test_cases = [tc for tc in test_cases if tc.get("id") == test_id]
        if not test_cases:
            print(f"No test case found with id: {test_id}")
            return []
    
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        tc_id = test_case.get("id", "unknown")
        query = test_case.get("query", "")[:50]
        
        print(f"[{i}/{total}] Running {tc_id}: {query}...")
        
        result = run_test_case(test_case, verbose)
        results.append(result)
        
        # Print immediate result
        status = "✓" if result.passed else "✗"
        print(f"       {status} {'PASS' if result.passed else 'FAIL'}")
        
        if verbose and not result.passed:
            for err in result.errors:
                print(f"         - {err}")
    
    return results


def print_summary(results: list[TestResult]) -> None:
    """Print summary of results."""
    print("\n" + "=" * 60)
    print("GOLDEN SET RESULTS")
    print("=" * 60 + "\n")
    
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    pct = (passed / total * 100) if total > 0 else 0
    
    # Group by category
    by_category: dict[str, list[TestResult]] = {}
    for r in results:
        # Extract category from test ID or use default
        cat = r.id.split("-")[0] if "-" in r.id else "other"
        by_category.setdefault(cat, []).append(r)
    
    # Print each result
    for result in results:
        status = "✓" if result.passed else "✗"
        print(f"{status} {result.id}: {result.query[:50]}...")
        
        # Show check details
        checks = []
        if result.tool_check is not None:
            checks.append(f"Tools: {'✓' if result.tool_check else '✗'}")
        if result.source_check is not None:
            checks.append(f"Sources: {'✓' if result.source_check else '✗'}")
        if result.content_check is not None:
            checks.append(f"Content: {'✓' if result.content_check else '✗'}")
        if result.negative_check is not None:
            checks.append(f"Negative: {'✓' if result.negative_check else '✗'}")
        
        if checks:
            print(f"    {' | '.join(checks)}")
        
        if not result.passed and result.errors:
            for err in result.errors:
                print(f"    ERROR: {err}")
        
        print()
    
    # Print totals
    print("-" * 60)
    print(f"Total: {passed}/{total} passed ({pct:.1f}%)")
    
    if passed == total:
        print("\n✓ All golden set tests passed!")
    else:
        print(f"\n✗ {total - passed} test(s) failed")


def main():
    parser = argparse.ArgumentParser(description="Run Ask Acme golden set evaluation")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--id", type=str, help="Run only a specific test case by ID")
    parser.add_argument("--file", type=str, default="golden_data.yaml", help="Golden set YAML file")
    args = parser.parse_args()
    
    print("Ask Acme - Golden Set Evaluation")
    print("=" * 60)
    print()
    
    # Load golden set
    test_cases = load_golden_set(args.file)
    print(f"Loaded {len(test_cases)} test cases\n")
    
    # Run tests
    results = run_golden_set(test_cases, verbose=args.verbose, test_id=args.id)
    
    # Print summary
    print_summary(results)
    
    # Exit with error code if any failed
    passed = sum(1 for r in results if r.passed)
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
