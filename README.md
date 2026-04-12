# Batten

[![Release](https://img.shields.io/github/v/release/ehowardtillit/batten?style=flat-square&color=blue)](https://github.com/ehowardtillit/batten/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/ehowardtillit/batten/batten-ci.yml?branch=master&style=flat-square&label=CI)](https://github.com/ehowardtillit/batten/actions/workflows/batten-ci.yml)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-green?style=flat-square)](LICENSE)
[![Languages](https://img.shields.io/badge/languages-7-orange?style=flat-square)](#what-you-configure)
[![Agents](https://img.shields.io/badge/agents-Claude%20%C2%B7%20Cursor%20%C2%B7%20Copilot%20%C2%B7%20Codex-purple?style=flat-square)](#what-you-configure)
[![Built with Copier](https://img.shields.io/badge/built%20with-Copier-lightgrey?style=flat-square)](https://copier.readthedocs.io/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

Your codebase already has app code, tests, and maybe a CI pipeline you copied from Stack Overflow three years ago. What it probably doesn't have is a coherent engineering process that runs the same way every time, across every tool, without anyone having to remember the steps.

Batten is that process, shipped as infrastructure-as-code. One YAML file -- `batten.yml` -- declares your languages, agents, and tools. Batten turns that into CI pipelines, pre-commit hooks, agent instructions, and context files. Change the YAML, re-run `./batten regenerate`, and everything updates.

Think of it as docker-compose for your engineering process.

---

## What problem does this solve?

Most teams bolt on process ad hoc: a linter here, a CI job there, agent instructions that drift out of sync with reality. Six months later nobody knows which hooks are active, the Claude instructions reference deleted modules, and the new hire's first PR breaks because they didn't know about the secret handshake.

Batten solves this by making the process declarative. You state what you want. Batten generates the wiring. When something changes, you change one file and regenerate.

---

## Quick start

### New project

```bash
curl -sL https://raw.githubusercontent.com/ehowardtillit/batten/main/install.sh | sh -s my-project
cd my-project
```

### Existing project

```bash
curl -sL https://raw.githubusercontent.com/ehowardtillit/batten/main/install.sh | sh
```

The installer handles Copier, scaffolding, git init, and `./batten install` in one shot. If you prefer manual control:

```bash
pip install copier
copier copy gh:ehowardtillit/batten my-project
cd my-project && ./batten install
```

### Pulling updates

```bash
./batten regenerate
```

Reads your `batten.yml` and re-runs Copier with the current config. Your customizations stay intact.

---

## batten.yml

After setup your project has a `batten.yml`. This is the single source of truth for your engineering infrastructure.

```yaml
# batten.yml
version: 1

project:
  name: "My API"
  owner: "my-org"
  source_dirs: "src/"

methodology:
  type: "batten"          # "batten" for built-in tiers, "custom" to bring your own
  branching: "simple"     # "simple", "gitflow", or "trunk"

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
  engineering_memory:
    mempalace: true       # powers agent context, not a project runtime dep
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
```

Edit it, then:

```bash
./batten status              # what's configured
./batten validate            # check for errors
./batten validate --check-drift
./batten diff                # preview changes
./batten regenerate          # apply
```

The CLI is also the day-to-day interface:

```bash
./batten lint                # all linters (or --lang python)
./batten lint -- --fix       # pass flags through
./batten test                # all tests (or --lang go)
./batten format              # auto-format
./batten security-scan       # security scanners
./batten hooks install       # pre-commit hooks
./batten context refresh     # update AI context files
./batten eject               # remove Batten config, keep generated files
./batten --version
```

---

## Languages

Python, TypeScript, Go, Rust, PHP, Elixir/Erlang, Java/Kotlin. Enable any combination. Each one activates language-specific CI jobs, pre-commit hooks, formatters, and security scanners.

## Agents

Claude Code, Cursor, GitHub Copilot, OpenAI Codex. Batten generates instruction files for each in its native format -- all from the same guardrails. Enable any combination; each agent reads only its own file.

---

## Bring your own methodology

Batten ships with a default workflow (S/A/B/C tiers that scale ceremony with risk). If your organization already has an engineering methodology, point Batten at it:

```yaml
methodology:
  type: "custom"
  source: "git@github.com:org/your-methodology.git"
  path: ".methodology"
  init: "setup/init.sh"
  version: "v2.0.0"
```

Batten strips its own workflow content and keeps only the infrastructure. Your methodology provides the process; Batten provides the plumbing.

---

## MemPalace

When enabled, Batten wires MemPalace for the **engineering process** -- agent orientation, architecture search, and CI context-sync. It is not a project runtime dependency. Projects that want MemPalace as part of their application can add it independently.

What Batten configures:

- MCP server in `.mcp.json` so agents can query project context
- Bootstrap installs MemPalace and mines the repo
- CLI gains `./batten memory status`, `./batten memory mine`, `./batten context live`
- CI runs `mempalace mine` on merges to main
- Agent instructions include the memory protocol (search before assuming, journal after sessions)

---

## What gets generated

```
your-project/
├── batten.yml                       # stack manifest
├── batten                           # CLI
├── .github/
│   ├── workflows/ci.yml             # multi-language CI pipeline
│   ├── workflows/pr-validation.yml  # title format + tier detection
│   ├── instructions/                # guardrails, workflow, prompts, review
│   ├── context/                     # AI agent orientation files
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   ├── copilot-instructions.md
│   └── dependabot.yml
├── .cursor/rules/batten.mdc         # Cursor rules
├── CLAUDE.md                        # Claude Code playbook
├── AGENTS.md                        # Codex playbook
├── .mcp.json                        # MCP servers
├── .pre-commit-config.yaml          # multi-language guardrails
├── bootstrap.sh                     # one-shot setup
├── docs/                            # analysis, decisions, plans, implementations
├── CONTRIBUTING.md
└── renovate.json                    # if selected
```

---

## The stack

Batten sits at the infrastructure layer. It doesn't replace your tools -- it wires them together.

| Layer | Tool | What Batten does |
|-------|------|-----------------|
| **Eng. Memory** | MemPalace | MCP config, context sync, `./batten memory mine` |
| **Workflow** | gstack | Tier-to-sprint mapping, PR template references |
| **Runtime** | Caliper / AgentSteer | Hook installation, convention export |
| **Merge Gates** | agent-guardrails / roborev | Protected paths from tier system |
| **Security** | CodeGuard | Rule installation, CI deduplication |

---

## Guardrails

### Pre-commit (every commit, locally)

| Hook | What it catches | Languages |
|------|----------------|-----------|
| ruff | lint + format | Python |
| bandit | security anti-patterns | Python |
| semgrep | OWASP Top 10 | Python |
| detect-secrets | API keys, passwords, tokens | All |
| no-todo-fixme | blocks TODO/FIXME/HACK/PLACEHOLDER | All configured |
| no-silenced-exceptions | bare except: | Python |

### CI (every push/PR)

Jobs are generated per language. Each gets lint, test, security scan, dependency audit, and CodeQL where applicable.

Context staleness checks warn when `.github/context/` files are more than 30 days old.

---

## Tiered workflow (S/A/B/C)

Every change goes through a branch and PR. What varies is the ceremony.

| Tier | What triggers it | Ceremony | Review |
|------|-----------------|----------|--------|
| **S** | Schema, security, infra, auth, deploy | Issue > analysis > ADR > PR | Human required |
| **A** | New endpoint, service, model, integration | Issue > PR | Human required |
| **B** | Enhancement, refactor, logging, filters | PR | Auto-merge if green |
| **C** | Docs, comments, typos, log text | PR | Auto-merge if green |

Tier is auto-detected by CI from changed file paths. Override in the PR description.

---

## Philosophy

1. **Guardrails beat guidelines.** A pre-commit hook that blocks secrets is worth more than a wiki page saying "don't commit secrets."
2. **Ceremony scales with risk.** A database migration deserves an ADR and human review. A typo fix doesn't.
3. **AI agents need context, not conversation.** Well-maintained context files beat re-explaining your architecture every prompt.
4. **Documentation is a side effect, not a task.** If your workflow doesn't produce docs naturally, your workflow is wrong.

---

## Versioning

Batten follows semver. The `VERSION` file is the source of truth.

```bash
copier copy gh:ehowardtillit/batten.git --vcs-ref=v0.1.4 my-project
copier update --vcs-ref=v0.1.4
copier update  # latest
```

---

## License

AGPL-3.0 -- see [LICENSE](LICENSE) and [LICENSE-FAQ.md](LICENSE-FAQ.md).

**Your projects are yours.** Batten is a template. The generated output is your project, licensed however you choose. AGPL applies to Batten itself, not to projects you create with it. Commercial licensing available -- contact the maintainers.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
