# Stage 4: Rubric-Based Evaluation

Rubrics provide **structured, multi-dimensional scoring** for AI responses. Unlike binary pass/fail checks, rubrics grade responses across multiple criteria with weighted scores, giving you nuanced insights into agent quality.

## Why Rubrics?

Previous evaluation stages tell you **if** something passed or failed. Rubrics tell you **how well** the agent performed across different dimensions:

| Stage | What It Tells You |
|-------|-------------------|
| Golden Sets | "Did it contain the right answer?" |
| Labeled Scenarios | "Did it handle this category correctly?" |
| Replay Harnesses | "Were the tool calls and sources correct?" |
| **Rubrics** | "How helpful, accurate, and well-written was it?" |

## Rubric Dimensions

We evaluate responses across four key dimensions:

### 1. Relevance (0-5)
Does the response directly address the user's question?
- **5**: Perfectly on-topic, addresses all aspects of the query
- **3**: Mostly relevant with some tangential information
- **1**: Barely related to the question
- **0**: Completely off-topic or refuses to answer

### 2. Accuracy (0-5)
Is the information factually correct based on source data?
- **5**: All facts are correct and verifiable from sources
- **3**: Mostly correct with minor inaccuracies
- **1**: Significant errors or misleading information
- **0**: Completely incorrect or fabricated

### 3. Completeness (0-5)
Does the response fully answer the question?
- **5**: Comprehensive answer covering all aspects
- **3**: Covers main points but misses some details
- **1**: Minimal answer, major gaps
- **0**: Fails to provide any useful information

### 4. Clarity (0-5)
Is the response well-organized and easy to understand?
- **5**: Clear, well-structured, appropriate length
- **3**: Understandable but could be better organized
- **1**: Confusing or poorly structured
- **0**: Incomprehensible

## File Structure

```
stage_4_rubrics/
├── README.md           # This file
├── rubrics.yaml        # Rubric definitions and weights
├── scorer.py           # LLM-based rubric scoring
├── evaluator.py        # Run rubric evaluations
└── walkthrough.ipynb   # Interactive tutorial
```

## How It Works

### 1. Define Rubrics (`rubrics.yaml`)

```yaml
dimensions:
  relevance:
    weight: 0.3
    description: "Does the response address the question?"
    
  accuracy:
    weight: 0.4
    description: "Is the information factually correct?"
```

### 2. Score Responses (`scorer.py`)

We use an LLM as a judge to evaluate responses:

```python
from scorer import RubricScorer

scorer = RubricScorer()
scores = scorer.score(
    query="What's our refund policy?",
    response="We offer 30-day refunds for annual plans...",
    sources=["refund_policy.md"]
)
# Returns: {"relevance": 5, "accuracy": 4, "completeness": 4, "clarity": 5}
```

### 3. Aggregate Results (`evaluator.py`)

```python
from evaluator import run_rubric_evaluation

results = run_rubric_evaluation(test_cases)
# Weighted average: 4.3/5.0
# Breakdown by dimension, category, difficulty
```

## Running Evaluations

### Quick Start

```bash
# Score a single response
uv run python scorer.py "What's our PTO policy?"

# Run full evaluation suite
uv run python evaluator.py

# Filter by category
uv run python evaluator.py --category policy
```

### Integration with Previous Stages

Rubrics integrate seamlessly with golden sets and labeled scenarios:

```python
from evaluator import evaluate_golden_set_with_rubrics

# Get both pass/fail AND quality scores
results = evaluate_golden_set_with_rubrics("../stage_1_golden_sets/golden_data.yaml")
```

## Interpreting Results

### Score Thresholds

| Score | Quality Level | Action |
|-------|--------------|--------|
| 4.5-5.0 | Excellent | No action needed |
| 3.5-4.4 | Good | Minor improvements |
| 2.5-3.4 | Acceptable | Review and enhance |
| 1.5-2.4 | Poor | Significant work needed |
| 0-1.4 | Critical | Immediate attention |

### Dimension-Specific Insights

- **Low Relevance**: Agent may be misrouting queries or hallucinating
- **Low Accuracy**: Source retrieval or synthesis issues
- **Low Completeness**: May need better prompting or more sources
- **Low Clarity**: Response formatting or verbosity issues

## Best Practices

1. **Calibrate with humans first**: Score a sample manually, then compare LLM scores
2. **Use source grounding**: Always provide source documents for accuracy scoring
3. **Track trends over time**: Rubric scores show quality drift before failures
4. **Weight by priority**: Adjust weights based on your use case (e.g., accuracy > clarity for compliance)

## Next Step

Once rubrics are configured, run experiments to compare configurations:

```bash
cd ../stage_5_experiments
cat README.md
```
