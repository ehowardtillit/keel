# Changelog

All notable changes to Batten are documented here.

## [0.2.0] - 2026-07-31

### Added
- `python_dir` copier variable: directory containing `requirements.txt` / `pyproject.toml` (default `"."` for root; zero-diff with existing projects)
- `typescript_dir` copier variable: directory containing `package.json` / `package-lock.json` (default `"."` for root)
- `languages.python.dir` / `languages.typescript.dir` keys in generated `batten.yml`
- GitHub CI (`ci.yml`): `working-directory` on `test-python` when `python_dir != "."`, `cache-dependency-path` and `defaults.run.working-directory` on TypeScript lint/test jobs when `typescript_dir != "."`
- GitHub CI (`ci.yml`): `dependency-audit-python` now checks `python_dir/requirements.txt` instead of hardcoded root
- GitLab CI (`.gitlab-ci.yml`): `cd <dir>` prefix on Python and TypeScript jobs when dirs are non-root
- CircleCI (`.circleci/config.yml`): `cd <dir>` prefix on Python and TypeScript jobs when dirs are non-root
- Dependabot (`.github/dependabot.yml`): pip and npm `directory:` now reflects `python_dir` / `typescript_dir` (previously always hardcoded `"/"`)
- `context-sync` CI job: condition now uses `github.event.repository.default_branch` instead of hardcoded `main` (fixes MemPalace mining on master-default repos)
- `batten` CLI: `_lang_cwd()` helper; `_lint_commands`, `_test_commands` return `(label, cmd, cwd)` triples; `cmd_lint`, `cmd_test`, `cmd_format`, `cmd_security_scan` pass `cwd=` to subprocess for TypeScript and Python
- `batten validate`: rejects absolute paths and `..` in `python_dir` / `typescript_dir`; warns if directory is missing
- `FIELD_MAP`: added `languages.python.dir` → `python_dir` and `languages.typescript.dir` → `typescript_dir` for round-trip via `./batten regenerate`

### Fixed
- `batten-ci.yml` triggers on `[main, master, develop]` — Batten's own CI now runs on this repo (previously only `main`, so CI never ran on the `master` default branch)
- `test-python` CI: Python test suite in non-root directory is no longer silently skipped
- `dependency-audit-python` CI: pip-audit now actually audits the configured manifest instead of silently skipping
- TypeScript CI: `setup-node` with `cache: npm` no longer fails with "Dependencies lock file not found" on split layouts

### Notes
- `dir` support is added for Python and TypeScript only in this release; Go, Rust, PHP, Elixir, Java, C#, and Ruby receive the same treatment in a future release
- Zero-diff guarantee: projects using the default `"."` for both dirs regenerate byte-identical output

## [0.1.6] - 2026-04-13

### Fixed
- `regenerate` no longer clobbers user-customized `AGENTS.md`, `CLAUDE.md`, `.github/context/*.md`, and `docs/{plans,decisions,implementations,analysis}/*.md`
- Removed `--force` flag from Copier invocations so `_skip_if_exists` is respected

### Added
- `./batten regenerate --dry-run` previews changes without writing files
- Regression tests for skip-if-exists behavior across all protected file categories

## [0.1.5] - 2026-04-12

### Added
- C#/.NET language support (dotnet format, dotnet test, vulnerability check, CodeQL)
- Ruby language support (rubocop, rspec, bundler-audit, brakeman, CodeQL)
- GitLab CI pipeline template (`.gitlab-ci.yml`) -- set `ci.platform: "gitlab"`
- CircleCI pipeline template (`.circleci/config.yml`) -- set `ci.platform: "circleci"`
- `ci.platform` config option in `batten.yml` (github, gitlab, circleci)
- `./batten doctor` command -- checks that required tools are installed per config
- Bootstrap sections for C#/.NET and Ruby toolchains

### Changed
- `_write_ci_custom` now uses proper YAML serialization (PyYAML when available, JSON fallback)
- Custom CI job generation supports all three CI platforms
- CONTRIBUTING.md pre-commit hooks section dynamically lists only enabled languages
- Jinja artifact test regex uses negative lookbehind for GitHub Actions `${{ }}` expressions
- Test conftest uses `--vcs-ref=HEAD` for reliable template rendering
- ARCHITECTURE.md filled with real project architecture documentation
- README updated: 9 languages, CI platform docs, `doctor` command

### Removed
- Dead `LANG_GLOBS` dict from CLI (replaced by `_build_find_name_expr`)

## [0.1.4] - 2026-04-12

### Changed
- **Renamed from KEEL to Batten** -- all files, CLI, config, templates, GitHub repo, and documentation
- `keel` CLI -> `batten`, `keel.yml` -> `batten.yml`, `.cursor/rules/keel.mdc` -> `.cursor/rules/batten.mdc`
- `keel-ci.yml` -> `batten-ci.yml`
- GitHub repo renamed from `ehowardtillit/keel` to `ehowardtillit/batten`
- MemPalace scoped to engineering process only (agent context, CI context-sync) -- not a project runtime dependency
- `stack.memory.mempalace` config path -> `stack.engineering_memory.mempalace`
- README and human-facing text rewritten for clarity and natural tone
- Backward-compatible: CLI accepts `methodology.type: "keel"` as equivalent to `"batten"`

## [0.1.3] - 2026-04-12

### Added
- Java/Kotlin language support (checkstyle, JUnit, SpotBugs, OWASP dep-check, maven cache)
- `./batten init` command for interactive project setup
- `./batten --version` / `-V` flag
- `./batten eject` command to cleanly remove config
- `./batten validate --check-drift` for detecting config drift
- `--` passthrough for lint/test commands (e.g., `./batten lint -- --fix`)
- Colored CLI output with `NO_COLOR` support
- Concurrency groups and cancel-in-progress in CI templates
- pip/npm/cargo/mix caching in CI templates
- MemPalace install step in CI context-sync job
- `npm ci` before TypeScript lint/test CI jobs
- Formatters for Go, Rust, TypeScript, PHP, Java
- Security scanners for TypeScript, Go, Rust, Java
- Multi-language context refresh
- Code review checklist template
- LLM guardrail taxonomy (H1-H5, I1-I5, Q1-Q5, D1-D3, O1-O5)
- Test harness with 25+ template rendering tests
- Overwrite confirmation before install/regenerate
- Path validation and init script confirmation for methodology install

### Changed
- CLI uses list-form subprocess calls (eliminates shell injection vectors)
- `_project_slug` uses regex sanitization
- `_has_cmd` uses `shutil.which()`
- `_write_ci_custom` uses YAML block scalars to prevent workflow injection
- YAML fallback parser is now quote-aware when stripping comments
- `github_owner` default changed to `CHANGE-ME`
- `lang_python` no longer defaults to `true`
- `skip_agent_instructions` only prompted when `custom_methodology` is true
- `security-events: write` scoped to CodeQL jobs only
- Pre-commit `no-todo-fixme` hooks use word boundaries
- Methodology content wrapped in `{% if not custom_methodology %}` guards
- SHA-pinned GitHub Actions

### Removed
- Makefile template (CLI is the single entry point)
