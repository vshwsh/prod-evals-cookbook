# Stage 2: Labeled Scenarios

## What Are Labeled Scenarios?

Labeled scenarios extend golden sets by **categorizing test cases** by type, complexity, and expected behavior. This gives you coverage mapping - you can see at a glance which parts of your system are well-tested and which need more attention.

Think of it as organizing your test suite:
- **Golden Sets**: "Does it work?" (baseline correctness)
- **Labeled Scenarios**: "Does it work for all types of queries?" (coverage)

## Why Labeled Scenarios?

1. **Coverage visibility** - See which categories have gaps
2. **Targeted testing** - Run only SQL tests, or only multi-tool tests
3. **Regression tracking** - Know if a specific category degraded
4. **Prioritization** - Focus on categories that matter most

## Scenario Categories

### By Tool Type

| Category | Description | Example |
|----------|-------------|---------|
| `vector_only` | Queries that only need document search | "What's our PTO policy?" |
| `sql_only` | Queries that only need database access | "How many customers?" |
| `jira_only` | Queries that only need ticket search | "What P0 bugs are open?" |
| `slack_only` | Queries that only need message search | "What did eng decide?" |

### By Complexity

| Category | Description | Example |
|----------|-------------|---------|
| `single_tool` | Requires exactly one tool | "What's our refund policy?" |
| `multi_tool` | Requires 2+ tools working together | "Refund policy and refund count?" |
| `synthesis` | Requires reasoning across sources | "Compare policy to actual behavior" |

### By Difficulty

| Category | Description | Example |
|----------|-------------|---------|
| `straightforward` | Clear, direct questions | "How many customers?" |
| `ambiguous` | Could go multiple ways | "Tell me about refunds" |
| `edge_case` | Unusual or tricky inputs | Empty results, off-topic |

## What's in This Stage

| File | Purpose |
|------|---------|
| `scenarios.yaml` | 25+ scenarios organized by category |
| `evaluator.py` | Runs scenarios with category filtering |
| `walkthrough.ipynb` | Interactive tutorial |

## Scenario Structure

```yaml
scenarios:
  single_tool:
    vector_only:
      - id: "sc-v-001"
        query: "What is our remote work policy?"
        expected_tools: ["vector_search"]
        difficulty: "straightforward"
        
    sql_only:
      - id: "sc-s-001"
        query: "How many active customers do we have?"
        expected_tools: ["sql_query"]
        difficulty: "straightforward"
        
  multi_tool:
    vector_and_sql:
      - id: "sc-m-001"
        query: "What's our refund policy and how many refunds last quarter?"
        expected_tools: ["vector_search", "sql_query"]
        difficulty: "straightforward"
```

## Running Scenarios

```bash
cd stage_2_labeled_scenarios

# Run all scenarios
uv run python evaluator.py

# Run only single-tool scenarios
uv run python evaluator.py --category single_tool

# Run only SQL scenarios
uv run python evaluator.py --subcategory sql_only

# Run only straightforward difficulty
uv run python evaluator.py --difficulty straightforward
```

## Sample Output

```
Labeled Scenario Evaluation
========================================

Category: single_tool/vector_only
  ✓ sc-v-001: What is our remote work policy?
  ✓ sc-v-002: How much is the home office stipend?
  ✓ sc-v-003: What is our PTO policy?
  Results: 3/3 (100%)

Category: single_tool/sql_only
  ✓ sc-s-001: How many active customers?
  ✓ sc-s-002: What's our current MRR?
  ✗ sc-s-003: Revenue by quarter
  Results: 2/3 (67%)

Category: multi_tool/vector_and_sql
  ✓ sc-m-001: Refund policy and count
  Results: 1/1 (100%)

----------------------------------------
Overall: 6/7 passed (86%)

Coverage by Category:
  single_tool/vector_only: 100% ████████████████████
  single_tool/sql_only:     67% █████████████░░░░░░░
  multi_tool/vector_and_sql: 100% ████████████████████
```

## Coverage Matrix

The evaluator generates a coverage matrix:

```
                    | vector | sql | jira | slack | multi |
--------------------|--------|-----|------|-------|-------|
straightforward     |   3/3  | 2/3 |  2/2 |  2/2  |  1/1  |
ambiguous          |   1/1  | 1/2 |  0/1 |  1/1  |  0/1  |
edge_case          |   1/1  | 1/1 |  1/1 |  0/0  |  0/0  |
```

## Best Practices

1. **Balance coverage** - Don't over-test one category
2. **Label accurately** - Wrong labels hide problems
3. **Add scenarios from bugs** - Every production bug becomes a scenario
4. **Review quarterly** - Remove outdated, add new patterns
5. **Track trends** - Coverage should improve over time, not decline

## Relationship to Golden Sets

| Golden Sets | Labeled Scenarios |
|-------------|-------------------|
| Small (10-20) | Larger (30-100+) |
| Hand-curated | Can be generated |
| Must all pass | Some failure OK |
| Run on every change | Run on releases |
| Catch regressions | Map coverage |

## Next Step

Once you have good coverage, add deterministic replay for reproducibility:

```bash
cd ../stage_3_replay_harnesses
cat README.md
```
