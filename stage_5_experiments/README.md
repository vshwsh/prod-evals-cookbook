# Stage 5: Experiments & Configuration Comparison

Run the **same evaluation suite across different agent configurations** to find the best setup. This is how you make data-driven decisions about prompts, models, and parameters.

## Why Experiments?

When improving your agent, you'll ask questions like:
- "Is GPT-4o better than GPT-4o-mini for our use case?"
- "Does this new system prompt reduce hallucinations?"
- "What temperature gives the best quality/cost tradeoff?"

Experiments let you **answer these with data**, not intuition.

## How It Works

### 1. Define Variants (`variants.yaml`)

```yaml
variants:
  baseline:
    model: "gpt-4o-mini"
    temperature: 0.1
    system_prompt: "v1"
    
  gpt4o_upgrade:
    model: "gpt-4o"
    temperature: 0.1
    system_prompt: "v1"
    
  new_prompt:
    model: "gpt-4o-mini"
    temperature: 0.1
    system_prompt: "v2"
```

### 2. Run Experiments (`runner.py`)

```bash
# Run all variants against golden set
uv run python runner.py --test-source golden

# Run specific variants
uv run python runner.py --variants baseline,new_prompt

# Quick smoke test (3 cases per variant)
uv run python runner.py --limit 3
```

### 3. Compare Results (`reporter.py`)

```bash
# Generate comparison report
uv run python reporter.py results/

# Output:
# ┌─────────────┬─────────┬──────────┬───────────┬─────────┐
# │ Variant     │ Pass %  │ Rubric   │ Latency   │ Cost    │
# ├─────────────┼─────────┼──────────┼───────────┼─────────┤
# │ baseline    │ 87%     │ 4.1/5    │ 1.2s      │ $0.003  │
# │ gpt4o       │ 93%     │ 4.5/5    │ 2.1s      │ $0.015  │
# │ new_prompt  │ 91%     │ 4.3/5    │ 1.3s      │ $0.003  │
# └─────────────┴─────────┴──────────┴───────────┴─────────┘
```

## File Structure

```
stage_5_experiments/
├── README.md           # This file
├── variants.yaml       # Agent configuration variants
├── prompts/            # System prompt versions
│   ├── v1.txt
│   └── v2.txt
├── runner.py           # Run experiments
├── reporter.py         # Generate comparison reports
└── results/            # Experiment outputs (gitignored)
```

## Defining Variants

Each variant specifies agent configuration overrides:

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `model` | LLM model to use | `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo` |
| `temperature` | Sampling temperature | `0.0` - `1.0` |
| `system_prompt` | Prompt version | `v1`, `v2`, or inline text |
| `max_tokens` | Response length limit | `500`, `1000`, `2000` |
| `tools` | Which tools to enable | `["vector_search", "sql"]` |

## Experiment Workflow

```
1. Hypothesis: "New prompt will improve accuracy"
   │
2. Define variant in variants.yaml
   │
3. Run: python runner.py --variants baseline,new_prompt
   │
4. Compare: python reporter.py results/
   │
5. Decision: Keep new_prompt? Roll back? Iterate?
```

## Metrics Collected

For each variant, we track:

- **Pass Rate**: % of golden set cases passing
- **Rubric Scores**: Average across all dimensions
- **Latency**: Response time (p50, p95)
- **Token Usage**: Input/output tokens per query
- **Cost**: Estimated API cost per query
- **Tool Usage**: Which tools were called and how often

## Best Practices

1. **One change at a time**: Isolate variables to understand impact
2. **Use the same test set**: Compare apples to apples
3. **Run enough cases**: Statistical significance matters
4. **Track cost**: Better quality at 5x cost may not be worth it
5. **Version control prompts**: Store prompt versions as files

## Integration with Previous Stages

Experiments use all previous evaluation layers:

```python
# Run golden set evaluation for each variant
results = runner.run_experiment(
    variants=["baseline", "new_prompt"],
    test_source="golden",  # or "scenarios" or "rubrics"
    include_rubrics=True   # Also score with rubrics
)
```

## Example: Comparing Models

```bash
# Define experiment
cat >> variants.yaml << EOF
variants:
  mini:
    model: gpt-4o-mini
  full:
    model: gpt-4o
EOF

# Run
uv run python runner.py --test-source golden --limit 10

# Compare
uv run python reporter.py results/
```

## Next Steps

After finding the best configuration:
1. Update the production agent with winning settings
2. Set up regression tests to catch future degradation
3. Document the decision and rationale
