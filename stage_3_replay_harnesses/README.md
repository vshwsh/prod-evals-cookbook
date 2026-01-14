# Stage 3: Replay Harnesses

## What Are Replay Harnesses?

Replay harnesses provide **deterministic, reproducible evaluation** by:
1. **Recording** agent sessions (query, tool calls, responses)
2. **Replaying** with cached responses for consistent testing
3. **Measuring** with proper ML metrics (precision, recall, groundedness)

This builds on golden sets and labeled scenarios by adding:
- Reproducibility (same inputs = same outputs)
- Richer metrics beyond pass/fail
- Cost savings (no LLM calls during replay)

## The Eval Metrics

### Retrieval Metrics

| Metric | What It Measures | Formula |
|--------|-----------------|---------|
| **Precision** | How many retrieved docs are relevant? | relevant_retrieved / total_retrieved |
| **Recall** | How many relevant docs were retrieved? | relevant_retrieved / total_relevant |
| **MRR** | How high is the first relevant result? | 1 / rank_of_first_relevant |

### Generation Metrics

| Metric | What It Measures | How It's Computed |
|--------|-----------------|-------------------|
| **Groundedness** | Is the response grounded in sources? | LLM judge checks claims vs sources |
| **Faithfulness** | Does it stay true to sources (no hallucination)? | LLM judge checks for made-up facts |
| **Relevance** | Does it answer the question? | LLM judge scores relevance 1-5 |
| **Completeness** | Does it fully answer the question? | LLM judge checks all parts addressed |

### Tool Metrics

| Metric | What It Measures |
|--------|-----------------|
| **Tool Accuracy** | Did it use the correct tools? |
| **Tool Efficiency** | Did it avoid unnecessary tool calls? |

## How It Works

### 1. Record a Session

```python
from recorder import record_session

# Records all tool calls and responses
session = record_session(
    query="What's our refund policy and how many refunds in Q4?",
    session_id="refund-001"
)
# Saves to fixtures/refund-001.json
```

### 2. Annotate Ground Truth

```python
# Add ground truth annotations
session.annotations = {
    "relevant_sources": ["refund_policy.md"],
    "expected_facts": ["30-day refund window", "8 refunds in Q4"],
    "expected_tools": ["vector_search", "sql_query"],
}
```

### 3. Replay and Evaluate

```python
from player import replay_session
from metrics import evaluate_session

# Replay with cached responses (no LLM calls)
replayed = replay_session("refund-001")

# Compute all metrics
scores = evaluate_session(replayed)
print(scores)
# {
#   "retrieval_precision": 1.0,
#   "retrieval_recall": 1.0,
#   "groundedness": 0.95,
#   "faithfulness": 1.0,
#   "relevance": 5,
#   "tool_accuracy": 1.0,
# }
```

## What's in This Stage

| File | Purpose |
|------|---------|
| `metrics.py` | Precision, recall, groundedness, faithfulness scoring |
| `recorder.py` | Captures sessions with tool calls |
| `player.py` | Replays sessions with mocked responses |
| `evaluator.py` | Full evaluation harness |
| `fixtures/` | Recorded session files |

## Building on Previous Layers

```
Layer 1: Golden Sets
  └── Basic correctness (must_contain, expected_tools)
  
Layer 2: Labeled Scenarios  
  └── Coverage mapping by category
  
Layer 3: Replay Harnesses (this lesson)
  └── Reproducibility + rich metrics
      ├── Retrieval: precision, recall, MRR
      └── Generation: groundedness, faithfulness, relevance
```

## Running the Harness

```bash
cd stage_3_replay_harnesses

# Record new sessions
uv run python recorder.py --query "What's our refund policy?"

# Evaluate all fixtures
uv run python evaluator.py

# Evaluate specific session
uv run python evaluator.py --session refund-001
```

## Sample Output

```
Replay Harness Evaluation
========================================

Session: refund-001
Query: What's our refund policy and how many refunds in Q4?

Retrieval Metrics:
  Precision:  1.00  (1/1 relevant)
  Recall:     1.00  (1/1 found)
  
Generation Metrics:
  Groundedness:   0.95  (19/20 claims grounded)
  Faithfulness:   1.00  (no hallucinations)
  Relevance:      5/5   (fully answers question)
  Completeness:   1.00  (all parts addressed)

Tool Metrics:
  Accuracy:    1.00  (correct tools used)
  Efficiency:  1.00  (no unnecessary calls)

Overall Score: 0.98
```

## When to Use Each Layer

| Layer | Run When | Purpose |
|-------|----------|---------|
| Golden Sets | Every commit | Catch regressions fast |
| Labeled Scenarios | Every release | Verify coverage |
| Replay Harnesses | Weekly/on-demand | Deep quality analysis |

## Best Practices

1. **Record production examples** - Real queries make the best test cases
2. **Annotate carefully** - Ground truth quality determines metric quality
3. **Version fixtures** - Commit recorded sessions to git
4. **Track trends** - Metrics should improve over time
5. **Investigate drops** - A 5% drop in groundedness is a red flag

## Next Step

Add structured rubrics for multi-dimensional scoring:

```bash
cd ../stage_4_rubrics
cat README.md
```
