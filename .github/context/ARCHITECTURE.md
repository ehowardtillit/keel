# Architecture Overview

Batten is a Copier-based template that generates engineering infrastructure from a single YAML manifest. It has three layers: the template layer, the CLI layer, and the generated output.

## System Design

```
batten.yml (user config)
    │
    ├── copier copy/update ──► Jinja2 templates (*.jinja) ──► Generated files
    │                                                           ├── CI pipelines
    │                                                           ├── Pre-commit hooks
    │                                                           ├── Agent instructions
    │                                                           └── Context files
    │
    └── ./batten CLI ──► Reads batten.yml at runtime
                         ├── lint / test / format / security-scan
                         ├── install / regenerate / validate / doctor
                         ├── context refresh / memory mine
                         └── hooks / secrets / eject
```

## Module Boundaries

| Module | Responsibility |
|--------|---------------|
| `copier.yml` | Copier question definitions -- variables that drive all templates |
| `batten` | CLI script (Python, no dependencies beyond stdlib + optional PyYAML) |
| `*.jinja` | Jinja2 templates rendered by Copier into the target project |
| `.github/workflows/ci.yml.jinja` | GitHub Actions CI pipeline template |
| `.gitlab-ci.yml.jinja` | GitLab CI pipeline template |
| `.circleci/config.yml.jinja` | CircleCI pipeline template |
| `.pre-commit-config.yaml.jinja` | Pre-commit hooks template |
| `CONTRIBUTING.md.jinja` | Contributing guide template |
| `batten.yml.jinja` | Stack manifest template (rendered into target project) |
| `bootstrap.sh.jinja` | One-shot setup script template |
| `CLAUDE.md.jinja` / `AGENTS.md.jinja` | Agent instruction templates |
| `.cursor/rules/batten.mdc.jinja` | Cursor rules template |
| `tests/` | Test suite (CLI unit tests + Copier template rendering tests) |
| `docs/` | Documentation templates (analysis, decisions, plans, implementations) |
| `.github/context/` | AI agent orientation files |

## Data Flow

1. User edits `batten.yml` (or answers Copier prompts via `./batten init`)
2. `copier.yml` defines the variable schema -- each question maps to a template variable
3. `./batten regenerate` calls `copier update` which renders all `*.jinja` templates
4. The CLI (`./batten`) reads `batten.yml` at runtime for commands like lint, test, doctor
5. `FIELD_MAP` in the CLI translates `batten.yml` dot-paths to Copier variable names

## External Dependencies

| Dependency | Role | Required? |
|-----------|------|-----------|
| Copier | Template engine for generation | Yes (for init/regenerate) |
| PyYAML | YAML parsing in CLI | Optional (fallback parser included) |
| pre-commit | Git hook framework | Recommended |
| detect-secrets | Secret scanning | Recommended |
| Language toolchains | Per-language lint/test/format | Per config |
| MemPalace | Engineering memory / agent context | Optional |
