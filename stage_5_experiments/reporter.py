"""
Experiment Reporter - Generate comparison reports from experiment results.

Analyzes experiment outputs and produces formatted reports showing
how different variants compare across metrics.
"""

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class VariantSummary:
    """Summary metrics for a variant."""
    name: str
    pass_rate: float
    avg_rubric: float
    avg_latency_ms: float
    estimated_cost: float
    total_cases: int
    passed: int
    failed: int
    
    # Detailed breakdowns
    rubric_by_dimension: dict[str, float]
    latency_p50: float
    latency_p95: float
    tools_used: dict[str, int]
    failing_cases: list[str]


def load_results(results_dir: str) -> dict[str, VariantSummary]:
    """Load all experiment results from directory."""
    results_path = Path(results_dir)
    summaries = {}
    
    # Find all detail files (not summary files)
    for file_path in results_path.glob("*.json"):
        if file_path.name.startswith("summary_"):
            continue
        
        with open(file_path) as f:
            data = json.load(f)
        
        variant_name = data.get("variant", file_path.stem.split("_")[0])
        results = data.get("results", [])
        
        if not results:
            continue
        
        # Calculate metrics
        passed = sum(1 for r in results if r.get("passed", False))
        failed = len(results) - passed
        
        rubric_scores = [r["rubric_score"] for r in results if r.get("rubric_score") is not None]
        avg_rubric = sum(rubric_scores) / len(rubric_scores) if rubric_scores else 0
        
        latencies = sorted([r["latency_ms"] for r in results])
        p50_idx = len(latencies) // 2
        p95_idx = int(len(latencies) * 0.95)
        
        # Tool usage
        tools_count = defaultdict(int)
        for r in results:
            for tool in r.get("tools_used", []):
                tools_count[tool] += 1
        
        # Failing cases
        failing = [r["case_id"] for r in results if not r.get("passed", False)]
        
        summaries[variant_name] = VariantSummary(
            name=variant_name,
            pass_rate=passed / len(results) if results else 0,
            avg_rubric=avg_rubric,
            avg_latency_ms=sum(latencies) / len(latencies) if latencies else 0,
            estimated_cost=sum(r.get("input_tokens", 0) + r.get("output_tokens", 0) for r in results) * 0.000001,
            total_cases=len(results),
            passed=passed,
            failed=failed,
            rubric_by_dimension={},  # Would need dimension-level data
            latency_p50=latencies[p50_idx] if latencies else 0,
            latency_p95=latencies[p95_idx] if latencies else 0,
            tools_used=dict(tools_count),
            failing_cases=failing
        )
    
    return summaries


def print_comparison_table(summaries: dict[str, VariantSummary]):
    """Print formatted comparison table."""
    if not summaries:
        print("No results found.")
        return
    
    print("\n" + "=" * 80)
    print("EXPERIMENT COMPARISON REPORT")
    print("=" * 80)
    
    # Main metrics table
    print("\n## Overall Metrics\n")
    print(f"{'Variant':<15} {'Pass Rate':>10} {'Rubric':>8} {'Latency':>12} {'Cost':>10}")
    print("-" * 80)
    
    sorted_summaries = sorted(summaries.values(), key=lambda x: -x.pass_rate)
    
    for s in sorted_summaries:
        print(f"{s.name:<15} {s.pass_rate*100:>9.1f}% {s.avg_rubric:>7.2f} {s.avg_latency_ms:>10.0f}ms ${s.estimated_cost:>8.5f}")
    
    # Latency breakdown
    print("\n## Latency Distribution\n")
    print(f"{'Variant':<15} {'P50':>12} {'P95':>12} {'Avg':>12}")
    print("-" * 55)
    
    for s in sorted_summaries:
        print(f"{s.name:<15} {s.latency_p50:>10.0f}ms {s.latency_p95:>10.0f}ms {s.avg_latency_ms:>10.0f}ms")
    
    # Tool usage
    print("\n## Tool Usage\n")
    all_tools = set()
    for s in summaries.values():
        all_tools.update(s.tools_used.keys())
    
    if all_tools:
        header = f"{'Variant':<15}" + "".join(f"{t:>15}" for t in sorted(all_tools))
        print(header)
        print("-" * len(header))
        
        for s in sorted_summaries:
            row = f"{s.name:<15}"
            for tool in sorted(all_tools):
                count = s.tools_used.get(tool, 0)
                row += f"{count:>15}"
            print(row)
    
    # Failing cases comparison
    print("\n## Failing Cases\n")
    for s in sorted_summaries:
        if s.failing_cases:
            print(f"{s.name}: {', '.join(s.failing_cases[:5])}" + 
                  (f" (+{len(s.failing_cases)-5} more)" if len(s.failing_cases) > 5 else ""))
        else:
            print(f"{s.name}: All passed!")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    best_accuracy = max(sorted_summaries, key=lambda x: x.pass_rate)
    best_speed = min(sorted_summaries, key=lambda x: x.avg_latency_ms)
    best_cost = min(sorted_summaries, key=lambda x: x.estimated_cost)
    best_quality = max(sorted_summaries, key=lambda x: x.avg_rubric) if any(s.avg_rubric > 0 for s in sorted_summaries) else None
    
    print(f"\nBest Accuracy:  {best_accuracy.name} ({best_accuracy.pass_rate*100:.0f}% pass rate)")
    print(f"Fastest:        {best_speed.name} ({best_speed.avg_latency_ms:.0f}ms avg)")
    print(f"Cheapest:       {best_cost.name} (${best_cost.estimated_cost:.5f})")
    if best_quality:
        print(f"Best Quality:   {best_quality.name} ({best_quality.avg_rubric:.2f} rubric score)")
    
    # Overall recommendation
    print("\n## Overall Recommendation\n")
    
    # Simple scoring: normalize and weight metrics
    scores = {}
    for s in sorted_summaries:
        # Higher is better for pass_rate and rubric
        # Lower is better for latency and cost (invert)
        max_latency = max(x.avg_latency_ms for x in sorted_summaries)
        max_cost = max(x.estimated_cost for x in sorted_summaries) or 1
        
        score = (
            s.pass_rate * 0.4 +
            (s.avg_rubric / 5.0) * 0.3 +
            (1 - s.avg_latency_ms / max_latency) * 0.15 +
            (1 - s.estimated_cost / max_cost) * 0.15
        )
        scores[s.name] = score
    
    winner = max(scores.items(), key=lambda x: x[1])
    print(f"Recommended variant: {winner[0]}")
    print(f"(Weighted score: {winner[1]:.2f} based on 40% accuracy, 30% quality, 15% speed, 15% cost)")
    
    print("\n" + "=" * 80)


def generate_markdown_report(summaries: dict[str, VariantSummary], output_path: str):
    """Generate a markdown report file."""
    lines = [
        "# Experiment Results Report",
        "",
        f"Generated from {len(summaries)} variants",
        "",
        "## Summary Table",
        "",
        "| Variant | Pass Rate | Rubric | Avg Latency | Cost |",
        "|---------|-----------|--------|-------------|------|",
    ]
    
    for s in sorted(summaries.values(), key=lambda x: -x.pass_rate):
        lines.append(f"| {s.name} | {s.pass_rate*100:.1f}% | {s.avg_rubric:.2f} | {s.avg_latency_ms:.0f}ms | ${s.estimated_cost:.5f} |")
    
    lines.extend([
        "",
        "## Detailed Results",
        ""
    ])
    
    for s in sorted(summaries.values(), key=lambda x: -x.pass_rate):
        lines.extend([
            f"### {s.name}",
            "",
            f"- **Pass Rate**: {s.pass_rate*100:.1f}% ({s.passed}/{s.total_cases})",
            f"- **Rubric Score**: {s.avg_rubric:.2f}/5.0",
            f"- **Latency**: P50={s.latency_p50:.0f}ms, P95={s.latency_p95:.0f}ms",
            f"- **Estimated Cost**: ${s.estimated_cost:.5f}",
            ""
        ])
        
        if s.failing_cases:
            lines.append(f"**Failing Cases**: {', '.join(s.failing_cases)}")
            lines.append("")
    
    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    
    print(f"Markdown report saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate experiment comparison report")
    parser.add_argument("results_dir", nargs="?", default="results",
                       help="Directory containing experiment results")
    parser.add_argument("--markdown", "-m",
                       help="Output markdown report to file")
    parser.add_argument("--json", "-j",
                       help="Output JSON summary to file")
    args = parser.parse_args()
    
    results_path = Path(__file__).parent / args.results_dir
    
    if not results_path.exists():
        print(f"Results directory not found: {results_path}")
        print("Run experiments first with: python runner.py")
        exit(1)
    
    summaries = load_results(str(results_path))
    
    if not summaries:
        print("No experiment results found in directory.")
        exit(1)
    
    # Print comparison
    print_comparison_table(summaries)
    
    # Generate markdown if requested
    if args.markdown:
        generate_markdown_report(summaries, args.markdown)
    
    # Output JSON if requested
    if args.json:
        output = {
            name: {
                "pass_rate": s.pass_rate,
                "avg_rubric": s.avg_rubric,
                "avg_latency_ms": s.avg_latency_ms,
                "estimated_cost": s.estimated_cost,
                "total_cases": s.total_cases,
                "passed": s.passed,
                "failed": s.failed
            }
            for name, s in summaries.items()
        }
        with open(args.json, "w") as f:
            json.dump(output, f, indent=2)
        print(f"JSON summary saved to: {args.json}")
