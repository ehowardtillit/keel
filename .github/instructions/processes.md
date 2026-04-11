# Processes

## Delegation Rules

- Main conversation thread is for reporting, discussing, deciding, and delegating
- Delegate implementation to sub-tasks when your agent supports it
- Different agents have different delegation models:

| Agent | How to delegate |
|-------|----------------|
| Claude Code | Use the Task tool for complex multi-step work |
| Cursor | Use explore, task, and general-purpose sub-agents |
| Codex | Use AGENTS.md-based orchestration |
| Other | Follow your agent's delegation patterns |

- Pre-gather raw data with bash, feed to agents as context

---

## API-First Development

- Build API endpoints first, test with OpenAPI / curl / httpie
- UI comes after API is stable, using mock data initially
- Every endpoint must have a Pydantic request/response model
- Iterate: API → contract tests → UI mockup → UI implementation

---

## Orchestration Scripts

For tasks with more than 10 steps, create a temporary orchestration script:

```bash
#!/bin/bash
# scripts/orchestrate-<task-name>.sh
# Orchestration script for: <description>
# Created: <date>
# Delete after task completion

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Step 1/N: <description> ==="
# ... commands ...

echo "=== Step 2/N: <description> ==="
# ... commands ...

echo "✅ Orchestration complete"
```

**Rules:**
- Place in `scripts/orchestrate-<name>.sh`
- Delete after task is complete -- these are temporary build scaffolding
- Each step should be idempotent (safe to re-run)
- Use `set -euo pipefail` for fail-fast behavior
- Print step numbers for progress tracking

---

## Documentation as Byproduct

Every workflow step naturally produces a document -- documentation is never a separate task:

| Workflow Step | Document Produced |
|--------------|-------------------|
| Analysis (Tier S) | `docs/analysis/NNN-<topic>.md` |
| Architecture decision | `docs/decisions/NNN-<title>.md` (ADR) |
| Planning (Tier S/A/B) | `docs/plans/NNN-<title>.md` |
| Implementation (Tier S/A/B) | `docs/implementations/NNN-<title>.md` |
| Testing | Coverage reports |
| Module changes | `.github/context/` files |
| Deployment | `CHANGELOG_RECENT.md` (auto from git log) |

**No standalone "write documentation" tasks.** If docs are stale, the workflow step that should have produced them was skipped.

### Plan documents (`docs/plans/`)

Created **before** implementation. Contents:
- What we're building and why
- Approach and affected files/modules
- Risks, open questions, dependencies
- Acceptance criteria

### Implementation records (`docs/implementations/`)

Created **after** implementation. Contents:
- What was actually built (may differ from plan)
- Files changed with brief rationale
- Decisions made during implementation
- Lessons learned, gotchas discovered
- Links to related plan/analysis/ADR

---

## Testing Requirements

- **Unit tests:** `tests/unit/test_<module>.py`, naming: `test_<function>_<scenario>`
- **Contract tests:** For external API integrations
- **Test markers:** `unit`, `integration`, `e2e`, `slow`
- **Coverage:** Define your targets in CI configuration (e.g., minimum % per module)
- **Workflow:** Run existing tests → make changes → add new tests → run all again
