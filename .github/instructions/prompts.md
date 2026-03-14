# Prompt Patterns

Quick-start commands to trigger specific workflows:

### /analyze: Investigate before implementing
1. Create GitHub issue: `gh issue create --title "[Analysis] <topic>" --label "analysis,tier-s"`
2. Create branch: `git checkout -b analysis/<topic>`
3. Write analysis doc in `docs/analysis/NNN-<topic>.md` using the existing template (see `docs/analysis/README.md`)
4. Answer: What's the problem? What are the options? What do we recommend?
5. Push and open draft PR for review

### /plan: Design the implementation approach
1. Read the analysis doc (if Tier S) or issue description
2. Write plan doc: `docs/plans/NNN-<title>.md` using template (`docs/plans/000-template.md`)
3. Include: goal, approach, affected files/modules, risks, acceptance criteria
4. Commit the plan and get approval before implementing

### /implement: Build from a plan
1. Read the plan doc (and analysis doc if Tier S)
2. Create branch: `git checkout -b feat/<ticket>-<description>`
3. Implement with sub-agents
4. Write tests (unit + integration as appropriate)
5. Run linting and tests
6. **Write implementation record:** `docs/implementations/NNN-<title>.md` -- what was built, files changed, decisions made during implementation, lessons learned
7. Update `.github/context/` files if architecture/API/module changes
8. Commit with conventional message + Co-authored-by trailer
9. Open PR

### /test: Add or fix tests
1. Identify coverage gaps: `pytest --cov=<module> --cov-report=term-missing`
2. Write tests following `test_<function>_<scenario>` naming
3. Run full suite

### /review: Review changes before PR
1. Run linting and tests
2. Check for LLM common issues (see verification checklist in `.github/instructions/guardrails.md`)
3. Verify `.github/context/` files are current

### /status: Report current state
1. `git --no-pager log --oneline -10`
2. Check project status
3. Query todos: check SQL todos table
