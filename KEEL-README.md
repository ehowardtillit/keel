# ⚓ KEEL

**KEEL Enforces Engineering Layouts**

An opinionated engineering scaffold for projects. Initially it supports Python projects.

Drop it into any repo and get tiered workflows, mechanical guardrails, AI-agent context management, and documentation-as-byproduct -- all pre-configured.

Born from the real-world pain of "vibe coding", then needing to retroactively impose discipline. 

KEEL is a framework to fix that.

---

## Why KEEL

Most project templates give you boilerplate **code**. KEEL gives you boilerplate **engineering process**:

- 🔒 **Security scanning** runs on every commit and not when someone remembers or when you get pwned
- 🏗️ **Tiered workflow** that bounds heavy ceremony for risky changes and gives you zero-ish friction for safe ones
- 🤖 **AI-agent aware** context files that make Copilot/Claude/GPT productive immediately
- 📝 **Docs happen automatically** at every workflow step produces an artifact
- 🚫 **Hard guardrails** for things that should never happen or we wish can't happen

---

## Quick Start

### New project

```bash
pip install copier
copier copy gh:ehowardtillit/keel my-project
cd my-project
git init && git add -A && git commit -m "feat: init from KEEL scaffold"
./bootstrap.sh
```

### Existing project

```bash
pip install copier
copier copy gh:ehowardtillit/keel .
./bootstrap.sh
```

### Pull KEEL updates

When KEEL evolves (new hooks, updated CI, improved guardrails):

```bash
copier update
```

Copier diffs what changed in KEEL since your last apply and merges cleanly. Your customizations are preserved.

### Manual setup (without Copier)

```bash
git clone https://github.com/ehowardtillit/keel.git /tmp/keel
cp -r /tmp/keel/.github /tmp/keel/.pre-commit-config.yaml /tmp/keel/.gitignore \
      /tmp/keel/CONTRIBUTING.md /tmp/keel/bootstrap.sh .
cp -r /tmp/keel/docs .
cp /tmp/keel/Makefile.jinja Makefile   # Rename: replace {{ source_dirs }} with your paths
chmod +x bootstrap.sh && ./bootstrap.sh
rm -rf /tmp/keel
```

Note: manual setup doesn't support `copier update`. You'll need to re-copy manually when KEEL changes. Edit the copied Makefile to replace `{{ source_dirs }}` with your actual source directories (e.g. `src/`).

### Customize for your project

Copier fills in basic variables (project name, GitHub owner, Python version, source dirs). These files need **manual** customization with your project-specific details:

| File | What to add |
|------|-------------|
| `.github/copilot-instructions.md` | Project overview, directory map, domain-specific rules |
| `.github/context/ARCHITECTURE.md` | System design, module boundaries, data flow |
| `.github/context/API_SURFACE.md` | Your API endpoints |
| `.github/context/MODULE_MAP.md` | File locations (auto-generated via CI) |
| `.github/context/CONVENTIONS.md` | Project-specific coding patterns |
| `.github/dependabot.yml` | Your package directories |

---

## What's Inside

```
keel/
├── .github/
│   ├── copilot-instructions.md       # AI agent playbook (compact core)
│   ├── instructions/                 # Detailed playbooks (loaded on demand)
│   │   ├── workflow.md               # Tier ceremonies, ticket creation
│   │   ├── guardrails.md             # NEVER/ALWAYS rules, LLM verification
│   │   ├── prompts.md                # /analyze, /plan, /implement commands
│   │   └── processes.md              # Delegation, orchestration, testing, docs
│   ├── CODEOWNERS                    # Auto-assign PR reviewers
│   ├── PULL_REQUEST_TEMPLATE.md      # Tier selection + checklist
│   ├── dependabot.yml                # Dependency update automation
│   ├── ISSUE_TEMPLATE/
│   │   ├── analysis.yml              # Tier S analysis task template
│   │   ├── bug.yml                   # Bug report (KEEL only)
│   │   ├── feature.yml               # Feature request (KEEL only)
│   │   └── config.yml                # Issue chooser (KEEL only)
│   ├── context/                      # AI agent orientation layer
│   │   ├── ARCHITECTURE.md
│   │   ├── API_SURFACE.md
│   │   ├── MODULE_MAP.md
│   │   ├── CONVENTIONS.md
│   │   └── CHANGELOG_RECENT.md
│   └── workflows/
│       ├── ci.yml                    # Lint, scan, CodeQL, test, audit
│       ├── pr-validation.yml         # Title format + tier detection
│       └── keel-ci.yml               # Template validation (KEEL only)
├── docs/
│   ├── analysis/
│   │   ├── README.md                 # Analysis index
│   │   └── 000-template.md           # Analysis template
│   ├── decisions/
│   │   ├── README.md                 # ADR index
│   │   └── 000-template.md           # ADR template
│   ├── plans/
│   │   ├── README.md                 # Plans index
│   │   └── 000-template.md           # Plan template
│   └── implementations/
│       ├── README.md                 # Implementation records index
│       └── 000-template.md           # Implementation record template
├── tests/
│   ├── __init__.py
│   └── conftest.py                   # Shared test fixtures
├── .pre-commit-config.yaml           # ruff + bandit + semgrep + detect-secrets + LLM guards
├── .gitignore
├── bootstrap.sh                      # One-shot project setup
├── Makefile                          # lint, test, context-refresh, secrets
├── CONTRIBUTING.md                   # Workflow, branching, testing, style
├── LICENSE.jinja                     # Templated license (MIT/Apache/AGPL)
├── README.md.jinja                   # Consumer project README
├── KEEL-README.md                    # KEEL template documentation (you are here)
└── KEEL-LICENSE                      # KEEL's own AGPL-3.0 license
```

> Files marked *(KEEL only)* are used by the KEEL repository itself and are not copied to consumer projects.

---

## Tiered Workflow (S/A/B/C)

Every change from database migrations to typo fixes go through a branch and PR. What varies is the **ceremony**.

The tiers follow a ranking system :

- **S** = **S**chema / **S**ecurity / infra is for the highest-risk changes that can break data, auth, or deploys. Full ceremony: analysis doc, ADR, human review.
- **A** = **A**ddition is for new functionality (endpoints, services, models). Needs a ticket and human review, but no analysis doc.
- **B** = **B**etter is for improvements to existing code (refactors, logging, filters). Branch + PR, auto-merge if CI is green.
- **C** = **C**osmetic is for zero-risk changes (docs, comments, typos). Branch + PR, auto-merge if CI is green.

| Tier | What triggers it | Ceremony | Review |
|------|-----------------|----------|--------|
| **S** | Schema, security, infra, auth, deploy | Issue → analysis doc → ADR → PR | Human required |
| **A** | New endpoint, service, model, integration | Issue → PR | Human required |
| **B** | Enhancement, refactor, logging, filters | PR | Auto-merge if green |
| **C** | Docs, comments, typos, log text | PR | Auto-merge if green |

**What's constant across ALL tiers:**
- Pre-commit hooks run (lint, security, secrets)
- CI pipeline runs (CodeQL, tests, audit)
- Conventional commit format enforced
- Branch + PR required (no direct pushes to main)

Tier is auto-detected by CI from the changed file paths. Override in the PR description if needed.

---

## Guardrails

### Pre-commit (local, every commit)

| Hook | What it catches |
|------|----------------|
| **ruff** | Lint errors, import sorting, code formatting |
| **bandit** | Python security anti-patterns (SQL injection, exec, etc.) |
| **semgrep** | OWASP Top 10 patterns, insecure defaults |
| **detect-secrets** | API keys, passwords, tokens in source code |
| **no-todo-fixme** | Blocks `TODO`, `FIXME`, `HACK`, `PLACEHOLDER` in Python files |
| **no-silenced-exceptions** | Blocks bare `except:` and `except...pass` patterns |
| **check-yaml/json** | Syntax errors in config files |
| **no-commit-to-branch** | Blocks direct commits to main/master |

### CI (GitHub Actions, every push/PR)

| Job | Purpose |
|-----|---------|
| **Lint** | ruff across all source dirs |
| **Security Scan** | bandit deep scan |
| **CodeQL** | GitHub-native SAST (semantic analysis) |
| **Test** | pytest with coverage reporting |
| **Dependency Audit** | pip-audit for known CVEs |
| **Template Validation** | Copier render test, Jinja syntax, YAML lint, structure check |
| **Context Staleness** | Warns if `.github/context/` files are >30 days old |

### PR Validation

| Check | Enforcement |
|-------|-------------|
| Conventional commit title | Blocks merge |
| Description ≥ 50 chars | Blocks merge |
| Tier S detection | Warns if analysis/ADR may be needed |

### Behavioral Guardrails (NEVER / ALWAYS)

Defined in `copilot-instructions.md` and enforced by convention:

**NEVER:**
- Drop a database or schema
- Delete infrastructure files (Makefile, CI, deploy scripts)
- Push directly to main
- Skip tests to save time
- Store secrets in code or commit `.env` with real credentials
- Use `allow_origins=["*"]` in CORS
- Add dependencies without checking for CVEs

**ALWAYS:**
- Run tests before AND after changes
- Update `.github/context/` if architecture/API/modules change
- Use parameterized SQL: Never allow for string interpolation in queries
- Validate user input at the boundary layer
- Follow OWASP Top 10 best practices

### LLM / AI-Generated Code Guardrails

AI assistants produce specific failure modes that humans don't. These are enforced both mechanically (pre-commit hooks) and by convention (copilot-instructions):

**Mechanically blocked (pre-commit):**
- `TODO` / `FIXME` / `HACK` / `PLACEHOLDER` in Python files
- Bare `except:` and `except...pass` (silenced exceptions)

**Enforced by convention (copilot-instructions):**
- No ghost implementations: Every function must be called and tested
- No phantom imports: Verify every import resolves
- No aspirational code: Only build what was asked for
- No over-abstraction: No base class with one subclass, no factory for one type
- No bloated functions: Limit to 50 line max, split if longer
- No placeholder stubs: If it's not implemented, don't create it
- No hallucinated endpoints, columns, or config keys
- Tests must assert real behavior, not just `assert True`

See the full **Verification Protocol** in `.github/instructions/guardrails.md`.

---

## AI Agent Context Layer

The `.github/context/` directory gives AI assistants (Copilot, Claude, GPT) instant orientation:

```
.github/context/
├── ARCHITECTURE.md      # System design, module boundaries
├── API_SURFACE.md       # All endpoints grouped by domain
├── MODULE_MAP.md        # What lives where, file counts
├── CONVENTIONS.md       # Coding style, naming, patterns
└── CHANGELOG_RECENT.md  # Last N changes from git log
```

**How it works:** The `copilot-instructions.md` gives AI agents the critical rules and orientation. Detailed playbooks live in `.github/instructions/` and are loaded on demand. This keeps the always-loaded context small while making everything accessible.

**Keeping it fresh:** CI warns when files are >30 days stale. Refresh manually or automate:

```bash
# Add to your Makefile:
context-refresh:
	@echo "# Module Map" > .github/context/MODULE_MAP.md
	@find src/ -name "*.py" | head -100 >> .github/context/MODULE_MAP.md
	@git log --oneline -50 > .github/context/CHANGELOG_RECENT.md
```

---

## Architecture Decision Records (ADRs)

Tier S changes require an ADR **before** implementation. The template lives at `docs/decisions/000-template.md`:

```markdown
# ADR-NNN: Title

> Status: Proposed | Accepted | Deprecated | Superseded by ADR-NNN
> Date: YYYY-MM-DD
> Tier: S

## Context       -- What's the problem?
## Decision      -- What did we choose?
## Consequences  -- What are the trade-offs?
## Alternatives  -- What else did we consider?
```

Create one: `cp docs/decisions/000-template.md docs/decisions/004-my-decision.md`

---

## Documentation as Byproduct

KEEL doesn't have "write docs" tasks. Instead, every workflow step naturally produces a document:

| Workflow Step | Artifact |
|--------------|----------|
| Analysis | `docs/analysis/NNN-topic.md` |
| Architecture decision | `docs/decisions/NNN-title.md` |
| Planning | `docs/plans/NNN-title.md` |
| Implementation | `docs/implementations/NNN-title.md` |
| Testing | Coverage reports |
| API changes | OpenAPI spec |
| Module changes | `.github/context/` updates |

Plans and implementation records are automatically surfaced in `CHANGELOG_RECENT.md` via `make context-refresh`, giving AI agents immediate access to recent work context.

If docs are stale, the workflow step that should have produced them was skipped.

---

## Prompt Patterns (/ Commands)

KEEL defines shortcut commands that trigger specific agent workflows. Use these in conversation with AI assistants:

| Command | When to use | What happens |
|---------|-------------|-------------|
| `/analyze` | Before building anything risky (Tier S) | Creates issue, branch, writes `docs/analysis/NNN-*.md` |
| `/plan` | Before implementation (Tier S/A/B) | Writes `docs/plans/NNN-*.md` with approach, affected files, risks |
| `/implement` | Build from a plan or issue | Code + tests + `docs/implementations/NNN-*.md` + context update |
| `/test` | Add or fix tests | Coverage gaps → new tests → full suite run |
| `/review` | Before opening PR | Lint, tests, LLM verification checklist, context freshness check |
| `/status` | Check where things stand | Git log, project status, todo state |

**Example flow for a Tier A feature:**
```
You: /plan Add rate limiting to enrichment endpoints
      (agent writes docs/plans/005-rate-limiting.md)

You: /implement
      (agent reads the plan, builds it, writes docs/implementations/005-rate-limiting.md)

You: /review
      (agent runs checks, verifies context files are current)
```

**Example flow for a Tier S change (schema/security):**
```
You: /analyze Impact of adding row-level security
      (agent creates issue, writes docs/analysis/003-rls-impact.md)

You: /plan
      (agent writes docs/plans/003-rls-implementation.md, creates ADR)

You: /implement
      (agent reads analysis + plan + ADR, builds it)

You: /review
      (agent runs full verification)
```

Full details for each command are in `.github/instructions/prompts.md`.

---

## Philosophy

KEEL is built on these four basic ideas:

1. **Guardrails beat guidelines.** A pre-commit hook that blocks secrets is worth more than a wiki page saying "don't commit secrets." that no one reads.

2. **Ceremony should scale with risk.** A database migration deserves an ADR and human review. A typo fix doesn't.

3. **AI agents need context, not conversation.** A well-maintained `.github/context/` directory beats re-explaining your architecture in every prompt.

4. **Documentation is a side effect, not a task.** If your workflow doesn't produce docs naturally, your workflow is wrong and it sucks.

---

## Versioning

KEEL follows [Semantic Versioning](https://semver.org/). The `VERSION` file is the source of truth.

- **Patch** (`0.1.1`) -- hook version bumps, typo fixes, minor CI tweaks
- **Minor** (`0.2.0`) -- new guardrails, new CI jobs, new context files, workflow refinements
- **Major** (`1.0.0`) -- breaking changes to template variables or file structure

### Pinning a version

```bash
# Copy a specific version
copier copy gh:ehowardtillit/keel.git --vcs-ref=v0.1.0 my-project

# Update to a specific version (not latest)
copier update --vcs-ref=v0.2.0

# Update to latest
copier update
```

Copier records the version in `.copier-answers.yml` in your project. Each `copier update` diffs from your pinned version to the target.

### Releasing a new version

1. Update the `VERSION` file
2. Commit: `git commit -am "chore: bump version to X.Y.Z"`
3. Tag: `git tag vX.Y.Z`
4. Push: `git push origin main --tags`

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. The short version:

1. Branch from main (`feat/`, `fix/`, `chore/`, `docs/`)
2. Make changes, pre-commit hooks run automatically
3. Open a PR with a conventional commit title
4. CI runs, tier is auto-detected
5. Merge when green (B/C) or after review (S/A)

---

## License

AGPL-3.0 -- see [KEEL-LICENSE](KEEL-LICENSE)
