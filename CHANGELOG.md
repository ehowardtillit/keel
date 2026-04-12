# Changelog

All notable changes to KEEL are documented here.

## [0.1.3] - 2026-04-12

### Added
- Java/Kotlin language support (checkstyle, JUnit, SpotBugs, OWASP dep-check, maven cache)
- `./keel init` command for interactive project setup
- `./keel --version` / `-V` flag
- `./keel eject` command to cleanly remove KEEL config
- `./keel validate --check-drift` for detecting config drift
- `--` passthrough for lint/test commands (e.g., `./keel lint -- --fix`)
- Colored CLI output with `NO_COLOR` support
- Concurrency groups and cancel-in-progress in CI templates
- pip/npm/cargo/mix caching in CI templates
- MemPalace install step in CI context-sync job
- `npm ci` before TypeScript lint/test CI jobs
- Formatters for Go (gofmt), Rust (cargo fmt), TypeScript (prettier), PHP (php-cs-fixer), Java (fmt-maven-plugin)
- Security scanners for TypeScript (npm audit), Go (govulncheck), Rust (cargo audit), Java (OWASP dep-check)
- Multi-language context refresh (scans all enabled languages)
- Code review checklist template (`code-review.md.jinja`)
- LLM guardrail taxonomy (H1-H5, I1-I5, Q1-Q5, D1-D3, O1-O5)
- Test harness with 25+ template rendering tests
- Overwrite confirmation before install/regenerate
- Path validation and init script confirmation for methodology install

### Changed
- CLI now uses list-form subprocess calls (eliminates shell injection vectors)
- `_project_slug` uses regex sanitization
- `_has_cmd` uses `shutil.which()` instead of `which` command
- `_write_ci_custom` uses YAML block scalars to prevent workflow injection
- YAML fallback parser is now quote-aware when stripping comments
- `github_owner` default changed to `CHANGE-ME`
- `lang_python` no longer defaults to `true`
- `skip_agent_instructions` only prompted when `custom_methodology` is true
- `security-events: write` scoped to CodeQL jobs only
- Pre-commit `no-todo-fixme` hooks use word boundaries (`\b`)
- Bandit pre-commit hook no longer uses `-r` flag
- `no-console-log` hook now covers JavaScript and JSX files
- Methodology content wrapped in `{% if not custom_methodology %}` guards
- License templates reference full text URLs
- Copier version pinned to `>=9,<11` in installer
- ARCHITECTURE.md creation handles missing file properly
- Subprocess timeout (300s) and diagnostic error messages

### Removed
- Makefile template (CLI is the single entry point)
- BANNER constant (uses argparse help)
- `shell=True` with user-controlled input
