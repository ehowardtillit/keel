# Workflow Details

## Tiered Workflow (S/A/B/C)

- ALL tiers run tests, lint, and security checks
- Tier determines human ceremony level
- Agent auto-classifies tier from the diff; user can override with explicit tier mention

### Tier S: Schema / Security / Infra

- **Touches:** Database migrations, auth middleware, deploy configs, `.env*`, CORS, security policies
- **Flow:** GitHub issue → branch → analysis doc → ADR → plan doc → orchestration script (if >10 steps) → implement → implementation record → test → PR
- **Review:** Human review required

### Tier A: Feature

- **Touches:** New endpoint, new service, new model, new external API integration
- **Flow:** GitHub issue → branch → plan doc → implement → implementation record → test → PR
- **Review:** Human review required

### Tier B: Enhancement

- **Touches:** Modify existing endpoint params, error messages, logging, filters
- **Flow:** Branch → implement → implementation record → test → PR
- **Review:** Auto-merge if CI green

### Tier C: Trivial

- **Touches:** Docstrings, comments, log text, typos in non-code files
- **Flow:** Branch → implement → test → PR
- **Review:** Auto-merge if CI green

### Creating Tickets

For Tier S and A changes, create a GitHub issue first:

```bash
# Tier S -- analysis ticket
gh issue create \
  --title "[Analysis] <topic>" \
  --label "analysis,tier-s" \
  --body "## Problem\n<description>\n\n## Scope\n- In: ...\n- Out: ...\n\n## Key Questions\n1. ..."

# Tier A -- feature ticket
gh issue create \
  --title "feat: <description>" \
  --label "enhancement" \
  --body "## Summary\n<description>\n\n## Acceptance Criteria\n- [ ] ..."
```

Tier B and C changes don't need a ticket -- the PR is the record.

---

## Mandatory Steps (ALL Tiers)

These run on EVERY commit regardless of tier -- mechanically enforced:

- **Pre-commit:** ruff (lint + format), bandit (security), semgrep (OWASP), detect-secrets
- **CI:** CodeQL (GitHub-native SAST), pytest with coverage, OpenAPI drift check
- **Tests must pass -- no exceptions**
- **Conventional commits:** `feat|fix|docs|refactor|test|chore|ci|perf: description`
