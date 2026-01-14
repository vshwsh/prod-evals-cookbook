"""
Rubric Evaluator - Run comprehensive rubric-based evaluations

Integrates with golden sets and labeled scenarios to provide
multi-dimensional quality scores alongside pass/fail metrics.
"""

import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

from rubric_config import ask_acme

from scorer import RubricResult, RubricScorer, print_result


@dataclass
class EvaluationSummary:
    """Summary statistics for an evaluation run."""
    total_cases: int
    average_score: float
    quality_distribution: dict[str, int]
    dimension_averages: dict[str, float]
    category_scores: dict[str, float]
    lowest_scoring: list[tuple[str, float]]
    highest_scoring: list[tuple[str, float]]


def load_rubric_test_cases(rubrics_path: str) -> list[dict]:
    """Load test cases from rubrics.yaml."""
    with open(rubrics_path) as f:
        rubrics = yaml.safe_load(f)
    return rubrics.get("test_cases", [])


def load_golden_set_cases(golden_path: str) -> list[dict]:
    """Load and convert golden set cases for rubric evaluation."""
    with open(golden_path) as f:
        data = yaml.safe_load(f)
    
    cases = []
    for case in data.get("test_cases", []):
        cases.append({
            "id": case["id"],
            "query": case["query"],
            "category": case.get("category", "general"),
            "expected_sources": case.get("expected_tools", [])
        })
    return cases


def load_scenario_cases(scenarios_path: str, category: Optional[str] = None) -> list[dict]:
    """Load and convert scenario cases for rubric evaluation."""
    with open(scenarios_path) as f:
        data = yaml.safe_load(f)
    
    cases = []
    for scenario in data.get("scenarios", []):
        if category and scenario.get("category") != category:
            continue
        cases.append({
            "id": scenario["id"],
            "query": scenario["query"],
            "category": scenario.get("category", "general"),
            "difficulty": scenario.get("difficulty", "medium")
        })
    return cases


def run_rubric_evaluation(
    test_cases: list[dict],
    scorer: Optional[RubricScorer] = None,
    verbose: bool = True
) -> tuple[list[RubricResult], EvaluationSummary]:
    """Run rubric evaluation on test cases.
    
    Args:
        test_cases: List of test case dicts with 'query' and optional metadata
        scorer: Optional pre-configured scorer
        verbose: Print progress
        
    Returns:
        Tuple of (results list, summary statistics)
    """
    if scorer is None:
        scorer = RubricScorer()
    
    results = []
    dimension_scores = defaultdict(list)
    category_scores = defaultdict(list)
    quality_counts = defaultdict(int)
    
    for i, case in enumerate(test_cases):
        query = case["query"]
        case_id = case.get("id", f"case-{i+1}")
        category = case.get("category")
        
        if verbose:
            print(f"\n[{i+1}/{len(test_cases)}] {case_id}: {query[:50]}...")
        
        # Get agent response
        try:
            response = ask_acme(query)
        except Exception as e:
            if verbose:
                print(f"  ERROR: {e}")
            continue
        
        # Score the response
        result = scorer.score(
            query=query,
            response=response,
            sources=case.get("expected_sources"),
            category=category
        )
        results.append(result)
        
        # Track metrics
        for score in result.scores:
            dimension_scores[score.dimension].append(score.score)
        
        if category:
            category_scores[category].append(result.overall_score)
        
        quality_counts[result.quality_level] += 1
        
        if verbose:
            print(f"  -> {result.quality_level} ({result.overall_score:.2f}/5.0)")
    
    # Calculate summary statistics
    all_scores = [r.overall_score for r in results]
    
    # Find lowest and highest scoring
    scored_cases = [(test_cases[i].get("id", f"case-{i+1}"), results[i].overall_score) 
                    for i in range(len(results))]
    sorted_by_score = sorted(scored_cases, key=lambda x: x[1])
    
    summary = EvaluationSummary(
        total_cases=len(results),
        average_score=sum(all_scores) / len(all_scores) if all_scores else 0,
        quality_distribution=dict(quality_counts),
        dimension_averages={
            dim: sum(scores) / len(scores) 
            for dim, scores in dimension_scores.items()
        },
        category_scores={
            cat: sum(scores) / len(scores)
            for cat, scores in category_scores.items()
        },
        lowest_scoring=sorted_by_score[:3],
        highest_scoring=sorted_by_score[-3:][::-1]
    )
    
    return results, summary


def print_summary(summary: EvaluationSummary):
    """Pretty print evaluation summary."""
    print("\n" + "=" * 60)
    print("RUBRIC EVALUATION SUMMARY")
    print("=" * 60)
    
    print(f"\nTotal Cases: {summary.total_cases}")
    print(f"Average Score: {summary.average_score:.2f}/5.0")
    
    print("\nQuality Distribution:")
    quality_order = ["Excellent", "Good", "Acceptable", "Poor", "Critical"]
    for level in quality_order:
        count = summary.quality_distribution.get(level, 0)
        pct = (count / summary.total_cases * 100) if summary.total_cases > 0 else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  {level:12} [{bar}] {count} ({pct:.0f}%)")
    
    print("\nDimension Averages:")
    for dim, avg in sorted(summary.dimension_averages.items()):
        bar = "█" * int(avg) + "░" * (5 - int(avg))
        print(f"  {dim.capitalize():12} [{bar}] {avg:.2f}/5.0")
    
    if summary.category_scores:
        print("\nScores by Category:")
        for cat, avg in sorted(summary.category_scores.items(), key=lambda x: -x[1]):
            bar = "█" * int(avg) + "░" * (5 - int(avg))
            print(f"  {cat:12} [{bar}] {avg:.2f}/5.0")
    
    print("\nLowest Scoring Cases:")
    for case_id, score in summary.lowest_scoring:
        print(f"  {case_id}: {score:.2f}")
    
    print("\nHighest Scoring Cases:")
    for case_id, score in summary.highest_scoring:
        print(f"  {case_id}: {score:.2f}")
    
    print("=" * 60)


def evaluate_with_golden_set(golden_path: str, verbose: bool = True) -> tuple[list[RubricResult], EvaluationSummary]:
    """Run rubric evaluation using golden set test cases."""
    cases = load_golden_set_cases(golden_path)
    return run_rubric_evaluation(cases, verbose=verbose)


def evaluate_with_scenarios(
    scenarios_path: str, 
    category: Optional[str] = None,
    verbose: bool = True
) -> tuple[list[RubricResult], EvaluationSummary]:
    """Run rubric evaluation using labeled scenario test cases."""
    cases = load_scenario_cases(scenarios_path, category=category)
    return run_rubric_evaluation(cases, verbose=verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run rubric-based evaluation")
    parser.add_argument("--source", "-s", 
                       choices=["rubrics", "golden", "scenarios"],
                       default="rubrics",
                       help="Source of test cases")
    parser.add_argument("--category", "-c",
                       help="Filter by category (for scenarios)")
    parser.add_argument("--limit", "-l", type=int,
                       help="Limit number of cases to run")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Minimal output")
    parser.add_argument("--detailed", "-d", action="store_true",
                       help="Show detailed results for each case")
    args = parser.parse_args()
    
    verbose = not args.quiet
    
    # Load test cases based on source
    if args.source == "rubrics":
        rubrics_path = Path(__file__).parent / "rubrics.yaml"
        cases = load_rubric_test_cases(str(rubrics_path))
        print("Running rubric evaluation with built-in test cases...")
    elif args.source == "golden":
        golden_path = Path(__file__).parent.parent / "stage_1_golden_sets" / "golden_data.yaml"
        cases = load_golden_set_cases(str(golden_path))
        print("Running rubric evaluation with golden set cases...")
    else:  # scenarios
        scenarios_path = Path(__file__).parent.parent / "stage_2_labeled_scenarios" / "scenarios.yaml"
        cases = load_scenario_cases(str(scenarios_path), category=args.category)
        print(f"Running rubric evaluation with scenario cases{f' (category: {args.category})' if args.category else ''}...")
    
    # Apply limit if specified
    if args.limit:
        cases = cases[:args.limit]
    
    print(f"Evaluating {len(cases)} test cases...")
    
    # Run evaluation
    results, summary = run_rubric_evaluation(cases, verbose=verbose)
    
    # Print detailed results if requested
    if args.detailed:
        print("\n" + "=" * 60)
        print("DETAILED RESULTS")
        print("=" * 60)
        for result in results:
            print_result(result)
    
    # Print summary
    print_summary(summary)
