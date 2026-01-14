# Code Review Standards

**Effective Date:** January 1, 2024  
**Last Updated:** November 15, 2024  
**Owner:** Engineering

## Overview

Code reviews are essential for maintaining code quality, sharing knowledge, and catching bugs before they reach production. This document outlines our standards and expectations.

## Pull Request Guidelines

### Before Opening a PR

1. **Self-review first** - Read through your own diff before requesting review
2. **Run tests locally** - All tests must pass before opening PR
3. **Keep PRs small** - Aim for under 400 lines changed. Split large changes into multiple PRs
4. **Write a good description** - Explain what, why, and how

### PR Description Template
```markdown
## What
[One-line summary of the change]

## Why
[Context and motivation]

## How
[Implementation approach, if not obvious]

## Testing
[How you tested this, what to test in review]

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated (if needed)
- [ ] No console.log or debug code
- [ ] Migrations are reversible (if applicable)
```

## Review SLAs

| PR Size | First Review Within |
|---------|---------------------|
| Small (<100 lines) | 4 hours |
| Medium (100-400 lines) | 8 hours |
| Large (>400 lines) | 24 hours (but try to avoid) |

**Note:** These are business hours. Weekend PRs will be reviewed Monday.

## Approval Requirements

| Change Type | Required Approvals |
|-------------|-------------------|
| Standard feature/fix | 1 approval from team member |
| Database migrations | 2 approvals (including DBA or lead) |
| Security-sensitive code | 2 approvals (including security review) |
| API contract changes | 2 approvals (including API owner) |
| Infrastructure/config | 1 approval from platform team |

## What Reviewers Look For

### Must Fix (Block Merge)
- Bugs or logic errors
- Security vulnerabilities
- Missing error handling
- Breaking changes without migration path
- Missing tests for new functionality
- Performance issues (N+1 queries, memory leaks)

### Should Fix (Strong Suggestion)
- Code clarity and readability
- Better abstractions or patterns
- Missing edge case handling
- Incomplete documentation

### Nitpicks (Optional)
- Style preferences (beyond linter rules)
- Variable naming suggestions
- Minor refactoring ideas

**Label nitpicks as `nit:` so authors know they're optional.**

## Review Etiquette

### For Reviewers
- Be kind and constructive
- Explain *why*, not just what
- Ask questions instead of making demands
- Acknowledge good code, not just problems
- Respond promptly to author questions

### For Authors
- Don't take feedback personally
- Respond to all comments (even just "done")
- Ask for clarification if needed
- Be open to alternative approaches

## Automated Checks

All PRs must pass these automated checks before merge:
- **CI Tests** - Unit and integration tests
- **Linting** - Ruff for Python, ESLint for TypeScript
- **Type checking** - mypy for Python, tsc for TypeScript
- **Security scan** - Snyk for dependency vulnerabilities

## Merging

- Use **Squash and Merge** for feature branches
- Use **Merge Commit** for release branches
- Delete the branch after merging
- Deploy to staging automatically; production deploy requires manual trigger

## Questions

Ask in #engineering or reach out to your tech lead.
