#!/usr/bin/env python3
"""
Labeled Scenario Evaluator for Ask Acme.

Runs categorized test scenarios and provides coverage reporting.
"""

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "setup_agent"))
sys.path.insert(0, str(Path(__file__).parent.parent / "stage_1_golden_sets"))

from orchestrator import ask_acme_with_trace
from evaluator import check_tools, check_must_contain, check_must_not_contain


@dataclass
class ScenarioResult:
    """Result of a single scenario test."""
    id: str
    category: str
    subcategory: str
    query: str
    difficulty: str
    passed: bool
    tool_check: bool | None = None
    content_check: bool | None = None
    errors: list[str] = field(default_factory=list)
    tools_used: list[str] = field(default_factory=list)
    response: str = ""


def load_scenarios(path: str = "scenarios.yaml") -> dict[str, Any]:
    """Load scenarios from YAML file."""
    yaml_path = Path(__file__).parent / path
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return data.get("scenarios", {})


def flatten_scenarios(
    scenarios: dict[str, Any],
    category_filter: str | None = None,
    subcategory_filter: str | None = None,
    difficulty_filter: str | None = None,
) -> list[tuple[str, str, dict]]:
    """
    Flatten nested scenario structure into list of (category, subcategory, scenario).
    
    Optionally filter by category, subcategory, or difficulty.
    """
    flattened = []
    
    for category, subcategories in scenarios.items():
        if category_filter and category != category_filter:
            continue
            
        if isinstance(subcategories, dict):
            for subcategory, scenario_list in subcategories.items():
                if subcategory_filter and subcategory != subcategory_filter:
                    continue
                    
                if isinstance(scenario_list, list):
                    for scenario in scenario_list:
                        if difficulty_filter:
                            if scenario.get("difficulty") != difficulty_filter:
                                continue
                        flattened.append((category, subcategory, scenario))
    
    return flattened


def run_scenario(category: str, subcategory: str, scenario: dict) -> ScenarioResult:
    """Run a single scenario and return the result."""
    scenario_id = scenario.get("id", "unknown")
    query = scenario.get("query", "")
    difficulty = scenario.get("difficulty", "unknown")
    
    result = ScenarioResult(
        id=scenario_id,
        category=category,
        subcategory=subcategory,
        query=query,
        difficulty=difficulty,
        passed=False,
    )
    
    try:
        # Run the agent
        trace = ask_acme_with_trace(query)
        result.response = trace["response"]
        result.tools_used = [tc["tool"] for tc in trace["tool_calls"]]
        
        # Check tools
        expected_tools = scenario.get("expected_tools", [])
        tool_ok, tool_err = check_tools(expected_tools, result.tools_used)
        result.tool_check = tool_ok
        if not tool_ok:
            result.errors.append(tool_err)
        
        # Check must_contain
        must_contain = scenario.get("must_contain", [])
        if must_contain:
            content_ok, content_err = check_must_contain(must_contain, result.response)
            result.content_check = content_ok
            if not content_ok:
                result.errors.append(content_err)
        
        # Check must_not_contain
        must_not_contain = scenario.get("must_not_contain", [])
        if must_not_contain:
            negative_ok, negative_err = check_must_not_contain(must_not_contain, result.response)
            if not negative_ok:
                result.content_check = False
                result.errors.append(negative_err)
        
        # Overall pass/fail
        checks = [result.tool_check, result.content_check]
        result.passed = all(c for c in checks if c is not None)
        
    except Exception as e:
        result.errors.append(f"Exception: {str(e)}")
        result.passed = False
    
    return result


def run_all_scenarios(
    scenarios: dict[str, Any],
    category_filter: str | None = None,
    subcategory_filter: str | None = None,
    difficulty_filter: str | None = None,
    verbose: bool = False,
) -> list[ScenarioResult]:
    """Run all matching scenarios and return results."""
    flattened = flatten_scenarios(
        scenarios, category_filter, subcategory_filter, difficulty_filter
    )
    
    results = []
    total = len(flattened)
    
    current_category = ""
    
    for i, (category, subcategory, scenario) in enumerate(flattened, 1):
        # Print category header
        cat_key = f"{category}/{subcategory}"
        if cat_key != current_category:
            current_category = cat_key
            print(f"\n[{cat_key}]")
        
        scenario_id = scenario.get("id", "unknown")
        query = scenario.get("query", "")[:40]
        
        print(f"  ({i}/{total}) {scenario_id}: {query}...", end=" ")
        
        result = run_scenario(category, subcategory, scenario)
        results.append(result)
        
        # Print immediate result
        status = "✓" if result.passed else "✗"
        print(status)
        
        if verbose and not result.passed:
            for err in result.errors:
                print(f"       - {err}")
    
    return results


def print_summary(results: list[ScenarioResult]) -> None:
    """Print summary with coverage matrix."""
    print("\n" + "=" * 60)
    print("LABELED SCENARIO RESULTS")
    print("=" * 60)
    
    # Group by category/subcategory
    by_category: dict[str, list[ScenarioResult]] = {}
    for r in results:
        key = f"{r.category}/{r.subcategory}"
        by_category.setdefault(key, []).append(r)
    
    # Print per-category results
    print("\nResults by Category:")
    print("-" * 40)
    
    for cat_key in sorted(by_category.keys()):
        cat_results = by_category[cat_key]
        passed = sum(1 for r in cat_results if r.passed)
        total = len(cat_results)
        pct = (passed / total * 100) if total > 0 else 0
        
        # Visual bar
        bar_len = 20
        filled = int(pct / 100 * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        
        print(f"  {cat_key:30} {passed}/{total} ({pct:5.1f}%) {bar}")
    
    # Print by difficulty
    by_difficulty: dict[str, list[ScenarioResult]] = {}
    for r in results:
        by_difficulty.setdefault(r.difficulty, []).append(r)
    
    print("\nResults by Difficulty:")
    print("-" * 40)
    
    for diff in ["straightforward", "ambiguous", "edge_case"]:
        if diff in by_difficulty:
            diff_results = by_difficulty[diff]
            passed = sum(1 for r in diff_results if r.passed)
            total = len(diff_results)
            pct = (passed / total * 100) if total > 0 else 0
            print(f"  {diff:20} {passed}/{total} ({pct:5.1f}%)")
    
    # Overall summary
    total_passed = sum(1 for r in results if r.passed)
    total_count = len(results)
    overall_pct = (total_passed / total_count * 100) if total_count > 0 else 0
    
    print("\n" + "-" * 40)
    print(f"Overall: {total_passed}/{total_count} passed ({overall_pct:.1f}%)")
    
    # List failures
    failures = [r for r in results if not r.passed]
    if failures:
        print(f"\nFailed Scenarios ({len(failures)}):")
        for r in failures:
            print(f"  ✗ {r.id}: {r.query[:50]}...")
            for err in r.errors:
                print(f"      {err}")


def main():
    parser = argparse.ArgumentParser(description="Run Ask Acme labeled scenario evaluation")
    parser.add_argument("--category", "-c", type=str, help="Filter by category (e.g., single_tool)")
    parser.add_argument("--subcategory", "-s", type=str, help="Filter by subcategory (e.g., sql_only)")
    parser.add_argument("--difficulty", "-d", type=str, help="Filter by difficulty")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--file", type=str, default="scenarios.yaml", help="Scenarios YAML file")
    args = parser.parse_args()
    
    print("Ask Acme - Labeled Scenario Evaluation")
    print("=" * 60)
    
    # Load scenarios
    scenarios = load_scenarios(args.file)
    
    # Count total scenarios
    flattened = flatten_scenarios(
        scenarios, args.category, args.subcategory, args.difficulty
    )
    print(f"Found {len(flattened)} matching scenarios")
    
    # Run tests
    results = run_all_scenarios(
        scenarios,
        category_filter=args.category,
        subcategory_filter=args.subcategory,
        difficulty_filter=args.difficulty,
        verbose=args.verbose,
    )
    
    # Print summary
    print_summary(results)
    
    # Exit with error code if significant failures
    passed = sum(1 for r in results if r.passed)
    pass_rate = (passed / len(results) * 100) if results else 0
    
    # For scenarios, we allow some failures (80% threshold)
    return 0 if pass_rate >= 80 else 1


if __name__ == "__main__":
    sys.exit(main())
