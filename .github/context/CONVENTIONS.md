# Coding Conventions

## Python Style
- **Formatter/Linter:** ruff (replaces black, isort, flake8)
- **Type hints:** Required on all public function signatures
- **Docstrings:** Google style for public APIs
- **Naming:** snake_case (functions/variables), PascalCase (classes), UPPER_SNAKE (constants)

## Git
- **Commits:** Conventional Commits (`feat|fix|docs|refactor|test|chore|ci|perf:`)
- **Branches:** `feat/<desc>`, `fix/<desc>`, `chore/<desc>`, `docs/<desc>`
- **No direct pushes to main** -- always branch + PR

## Testing
- **Location:** `tests/unit/test_<module>.py`
- **Naming:** `test_<function>_<scenario>`
- **Markers:** `unit`, `integration`, `e2e`, `slow`

## Security
- Parameterized SQL only -- no string interpolation in queries
- No secrets in source code
- Validate all user input at the boundary layer
