# Stage 1: Golden Sets

**Your first line of defense for AI quality.**

## What Are Golden Sets?

Golden sets are **curated input/output pairs** that define what "correct" looks like for your AI system. They serve as your baseline for correctness - if the agent fails on these, something is fundamentally broken.

Think of them like unit tests for your AI:
- **Input**: A specific question
- **Expected**: What the answer should contain or which tools should be used
- **Actual**: What the agent actually produces
- **Pass/Fail**: Does the actual meet expectations?

## Why Golden Sets First?

Golden sets are the foundation because they:

1. **Establish ground truth** - You manually verify these are correct
2. **Catch regressions** - Run after every change to catch breakages
3. **Are fast to run** - Small set (10-50 cases) runs in minutes
4. **Are easy to debug** - When one fails, you know exactly what went wrong

## What's in This Stage

| File | Purpose |
|------|---------|
| `golden_data.yaml` | 15 curated test cases with expected behaviors |
| `evaluator.py` | Runs the golden set and reports results |
| `walkthrough.ipynb` | Jupyter notebook version |

## Quick Start

Run the evaluator to see golden sets in action:

```bash
uv run python evaluator.py
```

Or explore the walkthrough notebook for an interactive experience:

```bash
uv run jupyter notebook walkthrough.ipynb
```

## The Golden Set Structure

Each test case has:

```yaml
- id: "gs-001"
  query: "What is our remote work policy?"
  
  # Which tools should be called?
  expected_tools:
    - vector_search
    
  # What sources should be cited?
  expected_sources:
    - remote_work_policy.md
    
  # What keywords must appear in the response?
  must_contain:
    - "remote"
    - "core hours"
    
  # What must NOT appear?
  must_not_contain:
    - "I don't know"
    - "no information"
```

## Types of Checks

### 1. Tool Selection
Did the agent use the right tools?

```python
# Expected: ["vector_search"]
# Actual: ["vector_search"]  ✓ Pass
# Actual: ["sql_query"]      ✗ Fail - wrong tool
# Actual: []                 ✗ Fail - no tools used
```

### 2. Source Citation
Did the agent cite the right sources?

```python
# Expected sources: ["refund_policy.md"]
# Response mentions "refund_policy.md"  ✓ Pass
# Response mentions "pto_policy.md"     ✗ Fail - wrong source
```

### 3. Content Validation
Does the response contain expected information?

```python
# must_contain: ["$500", "annual", "stipend"]
# Response: "...receive a $500 annual stipend..."  ✓ Pass
# Response: "...office supplies provided..."       ✗ Fail - missing key info
```

### 4. Negative Validation
Does the response avoid hallucination markers?

```python
# must_not_contain: ["I don't know", "I cannot"]
# Response: "The policy states..."   ✓ Pass
# Response: "I don't know about..."  ✗ Fail - gave up when answer exists
```

## Running the Golden Set

```bash
cd stage_1_golden_sets

# Run all golden set tests
uv run python evaluator.py

# Run with verbose output
uv run python evaluator.py --verbose

# Run a specific test
uv run python evaluator.py --id gs-001
```

## Sample Output

```
Golden Set Evaluation Results
========================================

✓ gs-001: What is our remote work policy?
  Tools: ✓  Sources: ✓  Content: ✓

✓ gs-002: How many active customers do we have?
  Tools: ✓  Sources: N/A  Content: ✓

✗ gs-003: What P0 bugs are open?
  Tools: ✓  Sources: ✓  Content: ✗
  Missing: "PLAT-1247"

----------------------------------------
Results: 14/15 passed (93.3%)
```

## When to Update Golden Sets

- **Add cases** when you find bugs in production
- **Update expected** when behavior intentionally changes
- **Remove cases** when they test deprecated features
- **Never** change expected just to make tests pass

## Best Practices

1. **Start small** - 10-20 high-quality cases beats 100 sloppy ones
2. **Cover the basics** - Each tool should have at least 2-3 golden cases
3. **Include edge cases** - Empty results, multi-tool queries, etc.
4. **Review regularly** - Golden sets should reflect current expectations
5. **Keep them fast** - Golden sets should run in < 5 minutes

## Next Step

Once golden sets pass consistently, add more coverage with labeled scenarios:

```bash
cd ../stage_2_labeled_scenarios
cat README.md
```
