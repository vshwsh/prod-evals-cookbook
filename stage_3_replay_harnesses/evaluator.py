#!/usr/bin/env python3
"""
Replay Harness Evaluator.

Runs comprehensive evaluation on recorded sessions using retrieval and generation metrics.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from recorder import Session, load_session, list_sessions
from player import replay_session
from metrics import (
    precision, recall, f1_score, mrr,
    groundedness, faithfulness, relevance,
    tool_accuracy, tool_efficiency,
)


def evaluate_session(session: Session, verbose: bool = False) -> dict[str, Any]:
    """
    Run full evaluation on a session.
    
    Args:
        session: The session to evaluate
        verbose: Whether to print detailed output
        
    Returns:
        Dict with all metric scores
    """
    results = {
        "session_id": session.session_id,
        "query": session.query,
        "metrics": {},
    }
    
    # Get annotations (ground truth)
    annotations = session.annotations
    relevant_sources = annotations.get("relevant_sources", [])
    expected_tools = annotations.get("expected_tools", [])
    
    # Actual values from recording
    retrieved_sources = session.retrieved_sources
    actual_tools = [tc.tool_name for tc in session.tool_calls]
    
    # ==========================================================================
    # Retrieval Metrics
    # ==========================================================================
    
    if relevant_sources:
        results["metrics"]["retrieval"] = {
            "precision": precision(retrieved_sources, relevant_sources),
            "recall": recall(retrieved_sources, relevant_sources),
            "f1": f1_score(retrieved_sources, relevant_sources),
            "mrr": mrr(retrieved_sources, relevant_sources),
        }
        
        if verbose:
            print("Retrieval Metrics:")
            print(f"  Precision: {results['metrics']['retrieval']['precision']:.2f}")
            print(f"  Recall:    {results['metrics']['retrieval']['recall']:.2f}")
            print(f"  F1:        {results['metrics']['retrieval']['f1']:.2f}")
            print(f"  MRR:       {results['metrics']['retrieval']['mrr']:.2f}")
    else:
        results["metrics"]["retrieval"] = None
        if verbose:
            print("Retrieval Metrics: N/A (no ground truth sources)")
    
    # ==========================================================================
    # Generation Metrics (LLM-as-Judge)
    # ==========================================================================
    
    if verbose:
        print("\nGeneration Metrics:")
        print("  (Running LLM judges...)")
    
    # Only run LLM judges if we have sources
    if session.source_contents or retrieved_sources:
        # Use source contents if available, otherwise use placeholder
        source_text = session.source_contents or [f"Source: {s}" for s in retrieved_sources]
        
        # Groundedness
        ground_result = groundedness(session.response, source_text)
        results["metrics"]["groundedness"] = ground_result["score"]
        
        # Faithfulness
        faith_result = faithfulness(session.response, source_text)
        results["metrics"]["faithfulness"] = faith_result["score"]
        
        if verbose:
            print(f"  Groundedness: {ground_result['score']:.2f}")
            print(f"  Faithfulness: {faith_result['score']:.2f}")
    else:
        results["metrics"]["groundedness"] = None
        results["metrics"]["faithfulness"] = None
    
    # Relevance (always run - doesn't need sources)
    rel_result = relevance(session.query, session.response)
    results["metrics"]["relevance"] = rel_result["score"]
    
    if verbose:
        print(f"  Relevance:    {rel_result['score']}/5")
    
    # ==========================================================================
    # Tool Metrics
    # ==========================================================================
    
    if expected_tools:
        results["metrics"]["tools"] = {
            "accuracy": tool_accuracy(expected_tools, actual_tools),
            "efficiency": tool_efficiency(expected_tools, actual_tools),
        }
        
        if verbose:
            print("\nTool Metrics:")
            print(f"  Accuracy:   {results['metrics']['tools']['accuracy']:.2f}")
            print(f"  Efficiency: {results['metrics']['tools']['efficiency']:.2f}")
    else:
        results["metrics"]["tools"] = None
        if verbose:
            print("\nTool Metrics: N/A (no expected tools annotated)")
    
    # ==========================================================================
    # Overall Score
    # ==========================================================================
    
    scores = []
    
    if results["metrics"].get("retrieval"):
        scores.append(results["metrics"]["retrieval"]["f1"])
    
    if results["metrics"].get("groundedness") is not None:
        scores.append(results["metrics"]["groundedness"])
    
    if results["metrics"].get("faithfulness") is not None:
        scores.append(results["metrics"]["faithfulness"])
    
    if results["metrics"].get("relevance"):
        scores.append(results["metrics"]["relevance"] / 5)  # Normalize to 0-1
    
    if results["metrics"].get("tools"):
        scores.append(results["metrics"]["tools"]["accuracy"])
    
    results["overall"] = sum(scores) / len(scores) if scores else 0.0
    
    if verbose:
        print(f"\nOverall Score: {results['overall']:.2f}")
    
    return results


def evaluate_all_sessions(verbose: bool = False) -> list[dict[str, Any]]:
    """
    Evaluate all recorded sessions.
    
    Returns:
        List of evaluation results
    """
    sessions = list_sessions()
    
    if not sessions:
        print("No recorded sessions found.")
        print("Record some sessions first: uv run python recorder.py --query 'Your query'")
        return []
    
    results = []
    
    print(f"Evaluating {len(sessions)} sessions...")
    print("=" * 60)
    
    for session_id in sessions:
        print(f"\nSession: {session_id}")
        print("-" * 40)
        
        session = load_session(session_id)
        result = evaluate_session(session, verbose=verbose)
        results.append(result)
    
    return results


def print_summary(results: list[dict[str, Any]]) -> None:
    """Print summary of all evaluation results."""
    if not results:
        return
    
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    
    # Aggregate scores
    overall_scores = [r["overall"] for r in results]
    avg_overall = sum(overall_scores) / len(overall_scores)
    
    print(f"\nSessions evaluated: {len(results)}")
    print(f"Average overall score: {avg_overall:.2f}")
    
    # Breakdown by metric
    metric_sums = {
        "retrieval_f1": [],
        "groundedness": [],
        "faithfulness": [],
        "relevance": [],
        "tool_accuracy": [],
    }
    
    for r in results:
        m = r.get("metrics", {})
        
        if m.get("retrieval"):
            metric_sums["retrieval_f1"].append(m["retrieval"]["f1"])
        
        if m.get("groundedness") is not None:
            metric_sums["groundedness"].append(m["groundedness"])
        
        if m.get("faithfulness") is not None:
            metric_sums["faithfulness"].append(m["faithfulness"])
        
        if m.get("relevance"):
            metric_sums["relevance"].append(m["relevance"] / 5)
        
        if m.get("tools"):
            metric_sums["tool_accuracy"].append(m["tools"]["accuracy"])
    
    print("\nMetric Averages:")
    print("-" * 40)
    
    for metric, values in metric_sums.items():
        if values:
            avg = sum(values) / len(values)
            print(f"  {metric:20} {avg:.2f} (n={len(values)})")
    
    # List any low-scoring sessions
    low_scores = [(r["session_id"], r["overall"]) for r in results if r["overall"] < 0.7]
    
    if low_scores:
        print("\nLow-scoring sessions (< 0.7):")
        for session_id, score in low_scores:
            print(f"  - {session_id}: {score:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate Ask Acme sessions")
    parser.add_argument("--session", "-s", type=str, help="Evaluate specific session")
    parser.add_argument("--all", "-a", action="store_true", help="Evaluate all sessions")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    if args.session:
        session = load_session(args.session)
        result = evaluate_session(session, verbose=not args.json)
        
        if args.json:
            print(json.dumps(result, indent=2))
        
        return 0
    
    if args.all or not args.session:
        results = evaluate_all_sessions(verbose=args.verbose)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_summary(results)
        
        return 0
    
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
