"""
Rubric Scorer - LLM-based multi-dimensional response evaluation

Uses an LLM as a judge to score responses across relevance, accuracy,
completeness, and clarity dimensions.
"""

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml
from openai import OpenAI

from rubric_config import get_openai_client, ask_acme


@dataclass
class RubricScore:
    """Individual dimension score with justification."""
    dimension: str
    score: int
    justification: str
    weight: float
    
    @property
    def weighted_score(self) -> float:
        return self.score * self.weight


@dataclass 
class RubricResult:
    """Complete rubric evaluation result."""
    query: str
    response: str
    scores: list[RubricScore]
    overall_score: float
    quality_level: str
    
    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "response": self.response[:200] + "..." if len(self.response) > 200 else self.response,
            "scores": {s.dimension: {"score": s.score, "justification": s.justification} for s in self.scores},
            "overall_score": round(self.overall_score, 2),
            "quality_level": self.quality_level
        }


class RubricScorer:
    """Scores AI responses using LLM-as-judge with structured rubrics."""
    
    def __init__(self, rubrics_path: Optional[str] = None):
        self.client = get_openai_client()
        
        # Load rubrics
        if rubrics_path is None:
            rubrics_path = Path(__file__).parent / "rubrics.yaml"
        with open(rubrics_path) as f:
            self.rubrics = yaml.safe_load(f)
        
        self.dimensions = self.rubrics["dimensions"]
        self.thresholds = self.rubrics["thresholds"]
        self.category_weights = self.rubrics.get("category_weights", {})
    
    def get_weights(self, category: Optional[str] = None) -> dict[str, float]:
        """Get dimension weights, optionally adjusted for category."""
        if category and category in self.category_weights:
            return self.category_weights[category]
        return {dim: info["weight"] for dim, info in self.dimensions.items()}
    
    def get_quality_level(self, score: float) -> str:
        """Map overall score to quality level."""
        if score >= self.thresholds["excellent"]:
            return "Excellent"
        elif score >= self.thresholds["good"]:
            return "Good"
        elif score >= self.thresholds["acceptable"]:
            return "Acceptable"
        elif score >= self.thresholds["poor"]:
            return "Poor"
        else:
            return "Critical"
    
    def build_scoring_prompt(self, query: str, response: str, sources: Optional[list[str]] = None) -> str:
        """Build the prompt for LLM-based scoring."""
        
        # Build dimension descriptions
        dim_descriptions = []
        for dim_name, dim_info in self.dimensions.items():
            criteria_text = "\n".join([f"    {score}: {desc}" for score, desc in dim_info["criteria"].items()])
            dim_descriptions.append(f"""
{dim_info['name']} (0-5):
  Description: {dim_info['description']}
  Scoring Guide:
{criteria_text}""")
        
        dimensions_text = "\n".join(dim_descriptions)
        
        sources_text = ""
        if sources:
            sources_text = f"\n\nSource documents used:\n" + "\n".join(f"- {s}" for s in sources)
        
        return f"""You are an expert evaluator assessing AI assistant responses.

Evaluate the following response across these dimensions, scoring each from 0-5:

{dimensions_text}

USER QUERY:
{query}

AI RESPONSE:
{response}
{sources_text}

Provide your evaluation as a JSON object with this exact structure:
{{
  "relevance": {{"score": <0-5>, "justification": "<brief explanation>"}},
  "accuracy": {{"score": <0-5>, "justification": "<brief explanation>"}},
  "completeness": {{"score": <0-5>, "justification": "<brief explanation>"}},
  "clarity": {{"score": <0-5>, "justification": "<brief explanation>"}}
}}

Be critical but fair. Only give 5s for truly excellent responses.
Respond ONLY with the JSON object, no other text."""

    def score(
        self, 
        query: str, 
        response: str, 
        sources: Optional[list[str]] = None,
        category: Optional[str] = None
    ) -> RubricResult:
        """Score a response using the rubric.
        
        Args:
            query: The user's original question
            response: The AI's response to evaluate
            sources: Optional list of source documents used
            category: Optional category for weight adjustments
            
        Returns:
            RubricResult with dimension scores and overall assessment
        """
        prompt = self.build_scoring_prompt(query, response, sources)
        
        # Call LLM for scoring
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective for evaluation
            messages=[
                {"role": "system", "content": "You are a precise evaluator. Output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Low temperature for consistency
            max_tokens=500
        )
        
        # Parse response
        raw_response = completion.choices[0].message.content.strip()
        
        # Handle potential markdown code blocks
        if raw_response.startswith("```"):
            raw_response = raw_response.split("```")[1]
            if raw_response.startswith("json"):
                raw_response = raw_response[4:]
        
        try:
            scores_dict = json.loads(raw_response)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                scores_dict = json.loads(json_match.group())
            else:
                raise ValueError(f"Could not parse LLM response as JSON: {raw_response}")
        
        # Get weights for this evaluation
        weights = self.get_weights(category)
        
        # Build RubricScore objects
        scores = []
        for dim_name in self.dimensions.keys():
            dim_result = scores_dict.get(dim_name, {"score": 0, "justification": "Not evaluated"})
            scores.append(RubricScore(
                dimension=dim_name,
                score=dim_result["score"],
                justification=dim_result["justification"],
                weight=weights[dim_name]
            ))
        
        # Calculate overall weighted score
        overall_score = sum(s.weighted_score for s in scores)
        quality_level = self.get_quality_level(overall_score)
        
        return RubricResult(
            query=query,
            response=response,
            scores=scores,
            overall_score=overall_score,
            quality_level=quality_level
        )
    
    def score_batch(
        self,
        items: list[dict],
        verbose: bool = True
    ) -> list[RubricResult]:
        """Score multiple query/response pairs.
        
        Args:
            items: List of dicts with 'query', 'response', optional 'sources', 'category'
            verbose: Print progress
            
        Returns:
            List of RubricResult objects
        """
        results = []
        for i, item in enumerate(items):
            if verbose:
                print(f"Scoring {i+1}/{len(items)}: {item['query'][:50]}...")
            
            result = self.score(
                query=item["query"],
                response=item["response"],
                sources=item.get("sources"),
                category=item.get("category")
            )
            results.append(result)
            
            if verbose:
                print(f"  -> {result.quality_level} ({result.overall_score:.2f})")
        
        return results


def print_result(result: RubricResult):
    """Pretty print a rubric result."""
    print("\n" + "=" * 60)
    print(f"Query: {result.query}")
    print("-" * 60)
    print(f"Response: {result.response[:150]}...")
    print("-" * 60)
    print("Dimension Scores:")
    for score in result.scores:
        bar = "█" * score.score + "░" * (5 - score.score)
        print(f"  {score.dimension.capitalize():12} [{bar}] {score.score}/5 (weight: {score.weight:.0%})")
        print(f"    {score.justification}")
    print("-" * 60)
    print(f"Overall: {result.overall_score:.2f}/5.0 - {result.quality_level}")
    print("=" * 60)


if __name__ == "__main__":
    # Demo: Score a single query through the agent
    import argparse
    
    parser = argparse.ArgumentParser(description="Score a query through the Ask Acme agent")
    parser.add_argument("query", nargs="?", default="What is our remote work policy?",
                       help="Query to evaluate")
    parser.add_argument("--category", "-c", help="Category for weight adjustments")
    args = parser.parse_args()
    
    # Agent is imported from local config
    
    print(f"Running query: {args.query}")
    print("-" * 40)
    
    # Get agent response
    response = ask_acme(args.query)
    print(f"Agent response:\n{response}\n")
    
    # Score the response
    scorer = RubricScorer()
    result = scorer.score(
        query=args.query,
        response=response,
        category=args.category
    )
    
    print_result(result)
