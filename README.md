# KEEL

**KEEL Enforces Engineering Layouts**

Engineering infrastructure-as-code. Drop it into any repo and get CI pipelines, mechanical guardrails, risk-scaled ceremony, and a documentation architecture -- all pre-configured. Then wire in the tools you already use.

KEEL is the foundation layer -- the docker-compose of the AI engineering stack. It configures and connects your memory system, workflow tools, runtime enforcement, and merge gates on a shared foundation of CI, hooks, ceremony, and documentation.

---

## Why KEEL

Most project templates give you boilerplate **code**. KEEL gives you boilerplate **engineering process**:

- **Mechanical guardrails** that run on every commit -- not when someone remembers
- **Risk-scaled ceremony** (S/A/B/C tiers) that bounds heavy process for risky changes and gives zero friction for safe ones
- **Multi-agent aware** -- generates instruction files for Claude Code, Cursor, GitHub Copilot, and OpenAI Codex from a single source
- **Documentation happens automatically** -- every workflow step produces an artifact
- **Stack orchestration** -- configure MemPalace, gstack, Caliper, AgentSteer, agent-guardrails, roborev, and CodeGuard in one place

---

## The Stack

KEEL sits at the infrastructure layer and orchestrates everything above it:

| Layer | Tool | What KEEL does |
|-------|------|---------------|
| **Memory** | MemPalace | MCP config, context sync, `./keel memory mine` |
| **Workflow** | gstack | Tier-to-sprint mapping, PR template references |
| **Runtime** | Caliper / AgentSteer | Hook installation, convention export |
| **Merge Gates** | agent-guardrails / roborev | Protected paths from tier system |
| **Security** | CodeGuard | Rule installation, CI deduplication |

KEEL does not replace these tools. It gives them a foundation to stand on and makes them work together.

---

## Quick Start

### New project

```bash
curl -sL https://raw.githubusercontent.com/ehowardtillit/keel/main/install.sh | sh -s my-project
cd my-project
```

### Existing project

```bash
curl -sL https://raw.githubusercontent.com/ehowardtillit/keel/main/install.sh | sh
```

The installer handles Copier, scaffolding, git init, and `./keel install` in one shot. If you prefer manual control:

```bash
pip install copier
copier copy gh:ehowardtillit/keel my-project
cd my-project && ./keel install
```

### Pull KEEL updates

```bash
./keel regenerate
```

Reads your `keel.yml` and re-runs Copier with the current config. Your customizations are preserved.

---

## keel.yml -- The Stack Manifest

After setup, your project has a `keel.yml` file. This is the single source of truth for your engineering infrastructure -- like `docker-compose.yml` is for your containers.

```yaml
# keel.yml
version: 1

project:
  name: "My API"
  owner: "my-org"
  source_dirs: "src/"

methodology:
  type: "keel"           # "keel" for built-in tiers, "custom" to bring your own
  branching: "simple"    # "simple", "gitflow", or "trunk"
  skip_agent_instructions: false

languages:
  python:
    enabled: true
    version: "3.12"
  typescript:
    enabled: true

agents:
  claude_code: true
  cursor: true
  github_copilot: true

stack:
  memory:
    mempalace: true
  workflow:
    gstack: false
  enforcement:
    runtime: "none"
    merge_gate: "none"
  security:
    codeguard: false
  dependencies:
    updater: "dependabot"

ci_extra_jobs:
  - name: "e2e-tests"
    run: "npx playwright test"
  - name: "performance"
    run: "k6 run tests/smoke.js"
```

Edit `keel.yml`, run `./keel regenerate`, and KEEL regenerates your CI pipelines, pre-commit hooks, agent instructions, and tool configs to match.

```bash
./keel status          # What's configured
./keel validate        # Check config consistency
./keel diff            # Preview changes
./keel regenerate      # Apply changes
```

The CLI is also the primary interface for daily development:

```bash
./keel lint            # Run all linters (or ./keel lint --lang python)
./keel test            # Run all tests (or ./keel test --lang go)
./keel format          # Auto-format code
./keel security-scan   # Run security scanners
./keel hooks install   # Install pre-commit hooks
./keel context refresh # Update AI context files
./keel memory status   # MemPalace status (when enabled)
./keel memory search "auth flow"  # Search MemPalace
```

---

## Bring Your Own Methodology

KEEL ships with a default workflow (S/A/B/C tiers). If your organization already has an engineering methodology — playbooks, runbooks, compliance frameworks, agent instructions, branching policies — point KEEL at it:

```yaml
methodology:
  type: "custom"
  branching: "gitflow"
  skip_agent_instructions: true
  source: "git@github.com:org/your-methodology.git"
  path: ".methodology"
  init: "setup/init.sh"
  version: "v2.0.0"
```

Then `./keel install` handles everything:

1. Bootstraps language toolchains
2. Clones your methodology as a git submodule, pins to the version tag, runs its init script
3. Installs pre-commit hooks
4. Sets up stack tools (MemPalace, gstack, etc.)
5. Generates context files

When `methodology.type` is `"custom"`, KEEL strips its own workflow content — tiers, commit conventions, PR template checkboxes, agent instructions — and keeps only infrastructure. Your methodology provides the process; KEEL provides the plumbing.

This works with any methodology that ships as a git repo: enterprise engineering foundations, compliance frameworks, team playbooks, or org-wide standards. KEEL doesn't compete with your process — it gives it CI, hooks, a CLI, and tool wiring for free.

---

## What You Configure

KEEL asks these questions during `copier copy` (and stores them in `keel.yml`):

**Project:** name, GitHub owner, source directories, license

**Methodology:** built-in S/A/B/C tiers or custom (bring your own), branching model (simple/gitflow/trunk), agent instruction generation (on/off)

**Languages:** Python, TypeScript, Go, Rust, PHP, Elixir/Erlang (multi-select -- each enables language-specific CI jobs, pre-commit hooks, and CLI commands)

**Agent targets:** Claude Code (CLAUDE.md), Cursor (.cursor/rules/keel.mdc), GitHub Copilot (copilot-instructions.md), OpenAI Codex (AGENTS.md) -- all generated from the same guardrails, each in its native format

**Stack:**
- MemPalace -- local semantic memory + knowledge graph via MCP
- gstack -- sprint workflow (/office-hours, /review, /ship)
- Caliper or AgentSteer -- runtime enforcement
- agent-guardrails or roborev -- merge-time validation
- CodeGuard -- OWASP security rules for AI agents
- Dependabot or Renovate -- dependency updates

**CI extensions:** custom pipeline stages beyond KEEL's defaults (contract validation, E2E tests, performance tests, compliance gates)

---

## What's Inside

```
keel/
├── .github/
│   ├── copilot-instructions.md    # GitHub Copilot playbook
│   ├── instructions/              # Detailed playbooks (loaded on demand)
│   │   ├── workflow.md            # Tier ceremonies, ticket creation
│   │   ├── guardrails.md          # NEVER/ALWAYS rules, LLM verification
│   │   ├── prompts.md             # /analyze, /plan, /implement commands
│   │   └── processes.md           # Delegation, testing, docs
│   ├── CODEOWNERS                 # Auto-assign PR reviewers
│   ├── PULL_REQUEST_TEMPLATE.md   # Tier selection + stack verification
│   ├── dependabot.yml             # Dependency updates (or renovate.json)
│   ├── context/                   # AI agent orientation layer
│   │   ├── ARCHITECTURE.md
│   │   ├── API_SURFACE.md
│   │   ├── MODULE_MAP.md
│   │   ├── CONVENTIONS.md
│   │   └── CHANGELOG_RECENT.md
│   └── workflows/
│       ├── ci.yml                 # Multi-language CI pipeline
│       └── pr-validation.yml      # Title format + tier detection
├── .cursor/rules/keel.mdc         # Cursor rules (if selected)
├── CLAUDE.md                      # Claude Code playbook (if selected)
├── AGENTS.md                      # OpenAI Codex playbook (if selected)
├── .mcp.json                      # MCP servers (MemPalace, agent-guardrails)
├── docs/
│   ├── analysis/                  # Pre-implementation investigation
│   ├── decisions/                 # Architecture Decision Records
│   ├── plans/                     # Implementation plans
│   └── implementations/           # Post-implementation records
├── .pre-commit-config.yaml        # Multi-language guardrails
├── keel                           # Engineering Stack CLI
├── bootstrap.sh                   # One-shot stack setup
├── CONTRIBUTING.md                # Multi-tool workflow guide
└── renovate.json                  # Renovate config (if selected)
```

---

## Tiered Workflow (S/A/B/C)

Every change goes through a branch and PR. What varies is the **ceremony**.

| Tier | What triggers it | Ceremony | Review |
|------|-----------------|----------|--------|
| **S** | Schema, security, infra, auth, deploy | Issue > analysis > ADR > PR | Human required |
| **A** | New endpoint, service, model, integration | Issue > PR | Human required |
| **B** | Enhancement, refactor, logging, filters | PR | Auto-merge if green |
| **C** | Docs, comments, typos, log text | PR | Auto-merge if green |

Tier is auto-detected by CI from changed file paths. Override in the PR description.

If gstack is configured, KEEL maps tiers to gstack skills: Tier S triggers `/office-hours` + `/plan-ceo-review` guidance. Standard changes get `/review` guidance.

---

## Guardrails

### Pre-commit (local, every commit)

| Hook | What it catches | Languages |
|------|----------------|-----------|
| **ruff** | Lint errors, formatting | Python |
| **bandit** | Security anti-patterns | Python |
| **semgrep** | OWASP Top 10 patterns | Python |
| **detect-secrets** | API keys, passwords, tokens | All |
| **no-todo-fixme** | Blocks TODO/FIXME/HACK/PLACEHOLDER | All configured |
| **no-silenced-exceptions** | Blocks bare except: | Python |
| **eslint** | Lint errors | TypeScript (via project config) |
| **golangci-lint** | Lint errors | Go (via project config) |
| **clippy** | Lint errors | Rust (via project config) |
| **phpcs** | PSR-12 violations | PHP (via project config) |
| **credo** | Style and consistency | Elixir (via project config) |

### CI (GitHub Actions, every push/PR)

Jobs are generated per language. Python gets ruff + bandit + pytest + pip-audit + CodeQL. TypeScript gets eslint + vitest + CodeQL. Go gets golangci-lint + go test + CodeQL. Rust gets clippy + cargo test. PHP gets phpcs + phpunit + composer audit. Elixir gets credo + mix test + sobelow + deps.audit.

Context staleness checks warn when `.github/context/` files are >30 days old. If MemPalace is enabled, a context-sync job keeps the palace current on merges to main.

---

## MemPalace Integration

When `mempalace_enabled` is true, KEEL configures:

- **MCP server** wired to Claude Code via `.mcp.json`
- **bootstrap.sh** installs MemPalace, initializes the palace, mines the project
- **CLI** gains `./keel context live` (syncs MemPalace to flat files), `./keel memory status`, `./keel memory mine`
- **Agent instructions** include the MemPalace memory protocol (search before assuming, write diary after sessions)
- **CI** runs `mempalace mine` on merges to main

The flat files in `.github/context/` remain the version-controlled baseline. MemPalace is the live engine that keeps them current.

---

## Documentation as Byproduct

Every workflow step produces a document:

| Step | Artifact |
|------|----------|
| Analysis | `docs/analysis/NNN-topic.md` |
| Decision | `docs/decisions/NNN-title.md` |
| Planning | `docs/plans/NNN-title.md` |
| Implementation | `docs/implementations/NNN-title.md` |
| Testing | Coverage reports |
| Module changes | `.github/context/` updates |

If docs are stale, the workflow step that should have produced them was skipped.

---

## Philosophy

1. **Guardrails beat guidelines.** A pre-commit hook that blocks secrets is worth more than a wiki page saying "don't commit secrets."
2. **Ceremony scales with risk.** A database migration deserves an ADR and human review. A typo fix doesn't.
3. **AI agents need context, not conversation.** Well-maintained context files beat re-explaining your architecture every prompt.
4. **Documentation is a side effect, not a task.** If your workflow doesn't produce docs naturally, your workflow is wrong.
5. **Infrastructure is the foundation.** KEEL gives you the plumbing. Your workflow tools, memory systems, and enforcement layers plug in on top.

---

## Versioning

KEEL follows Semantic Versioning. The `VERSION` file is the source of truth.

```bash
copier copy gh:ehowardtillit/keel.git --vcs-ref=v0.1.0 my-project
copier update --vcs-ref=v0.2.0
copier update  # latest
```

---

## License

AGPL-3.0 -- see [LICENSE](LICENSE) and [LICENSE-FAQ.md](LICENSE-FAQ.md).

**Your projects are yours.** KEEL is a template. The generated output (CI pipelines, pre-commit configs, CLI, documentation) is your project, licensed however you choose. AGPL applies to KEEL itself, not to projects you create with it.

Commercial licensing available -- contact the maintainers.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
