# Contributing to this project

## Getting Started

```bash
./bootstrap.sh              # Or manually:
python3 -m venv .venv && source .venv/bin/activate
pip install pre-commit && pre-commit install
```

## Common Commands

```bash
make help                   # Show all targets
make lint                   # Lint with ruff
make test                   # Run tests
make test-coverage          # Tests + coverage report
make security-scan          # Bandit scan
make secrets-baseline       # Regenerate secrets baseline
make context-refresh        # Update .github/context/ files
make hooks-run              # Run all pre-commit hooks
```

## Development Workflow

Changes are classified into four tiers (see `.github/instructions/workflow.md` for full details):

| Tier | Scope | Flow |
|------|-------|------|
| **S** | Schema, security, infra, deploy | Issue → branch → analysis doc → ADR → implement → test → PR (human review) |
| **A** | New endpoint, service, model, integration | Issue → branch → implement → test → PR (human review) |
| **B** | Modify existing endpoint, logging, filters | Branch → implement → test → PR (auto-merge if CI green) |
| **C** | Docs, comments, log text, typos | Branch → implement → test → PR (auto-merge if CI green) |

All tiers require: branch, tests, passing CI, and a PR.

## Branching Policy

- `main` -- protected, requires PR + green CI
- `feat/<ticket>-<short-description>` -- feature branches
- `fix/<ticket>-<short-description>` -- bug fixes
- `chore/<description>` -- maintenance
- `docs/<description>` -- documentation

```bash
git checkout main && git pull
git checkout -b feat/42-add-scoring-endpoint
```

## Commit Messages

[Conventional Commits](https://www.conventionalcommits.org/) required. Valid prefixes:

```
feat|fix|docs|refactor|test|chore|ci|perf: description
```

Examples:
```
feat: add prospect scoring endpoint
fix: handle null values in enrichment
ci: add bandit to pre-commit hooks
```

AI-assisted commits must include the Co-authored-by trailer:
```
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

## Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

Hooks that run on every commit:
- **ruff** -- linting + formatting (E501/F401 ignored)
- **bandit** -- security scanning (B101 skipped)
- **semgrep** -- static analysis
- **detect-secrets** -- prevent credential leaks
- **no-todo-fixme** -- blocks TODO/FIXME/HACK/PLACEHOLDER in Python files
- **no-silenced-exceptions** -- blocks bare `except:`
- **no-pass-except** -- blocks `except...pass` patterns

Run manually: `pre-commit run --all-files`

## AI-Generated Code

This project uses AI assistants for code generation, with specific guardrails to ensure code quality and maintainability.

**Key Rules for LLM-Generated Code:**
- **No TODOs** -- implement the feature or delete the code. TODOs are blocks for merge and indicate incomplete work.
- **No ghost implementations** -- every function must have a call site. Dead code adds maintenance burden.
- **No phantom imports** -- all imports must be used. Remove unused imports or delete the code that would use them.
- **No aspirational code** -- only implement what is needed now. Future requirements may change.
- **Functions under 50 lines** -- easier to test, review, and maintain.
- **Match existing patterns** -- follow the codebase conventions, structure, and style.

See [`.github/instructions/guardrails.md`](.github/instructions/guardrails.md) for the full ruleset.

**Quick Verification Checklist:**
- Grep for stray markers: `grep -rn "TODO\|FIXME\|HACK\|PLACEHOLDER" <files>`
- Verify imports resolve and are used: `python -c "import <module>"` or check call sites
- Confirm new functions have call sites: search codebase for function name
- Run changed code paths to ensure they execute cleanly

## Testing

```bash
pytest tests/ -v                                    # All tests
pytest tests/unit/ -v                               # Unit tests only
pytest tests/ --cov --cov-report=term-missing       # With coverage
```

Check CI configuration for coverage thresholds.

**Naming convention:** `tests/unit/test_<module>.py` → `test_<function>_<scenario>`

**Workflow:** Run existing tests → make changes → add new tests → run all again.

## Code Style

- **ruff** handles all formatting and linting -- do not configure other formatters
- **Pydantic v2** for all data models
- **Type hints** required on all function signatures
- **Parameterized SQL only** -- no string interpolation in queries
- Python 3.11+

## PR Checklist

See the [PR template](.github/PULL_REQUEST_TEMPLATE.md) for the full checklist. Key points:
- Conventional commit title
- All tests pass
- Pre-commit hooks pass
- No secrets committed
- `.github/context/` files updated if architecture/API/module changes
- ADR created for Tier S changes

## Architecture Decisions

Tier S changes require an Architecture Decision Record (ADR) before implementation.

- Template: [`docs/decisions/000-template.md`](docs/decisions/000-template.md)
- Store ADRs in `docs/decisions/NNN-<short-title>.md`
- Link the ADR in the PR description

## Versioning

[Semantic Versioning](https://semver.org/) with the `VERSION` file as the single source of truth.

Release workflow:
1. Update `VERSION` file
2. Commit: `git commit -am "chore: bump version to X.Y.Z"`
3. Tag: `git tag vX.Y.Z`
4. Push: `git push origin main --tags`

## Questions?

Open an issue with the `question` label.
