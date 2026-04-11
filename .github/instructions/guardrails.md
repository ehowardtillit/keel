# Guardrails

## Guardrails: NEVER Do

Hard blocks. Violating any of these requires explicit user override:

- NEVER drop a database or schema (`DROP DATABASE`, `DROP SCHEMA`)
- NEVER delete infrastructure files (`Makefile`, CI workflows, deploy scripts, migration configs)
- NEVER push directly to main -- always branch + PR
- NEVER skip tests to save time
- NEVER store secrets in code or commit `.env` files with real credentials
- NEVER use `allow_origins=["*"]` in CORS configuration
- NEVER run `ALTER TABLE ... DROP COLUMN` without a 2-phase migration plan
- NEVER delete data in production without backup confirmation
- NEVER add dependencies without checking for CVEs (`pip-audit`)
- NEVER auto-run migrations on deploy without review for destructive operations
- NEVER auto-deploy to production environments

---

## Guardrails: ALWAYS Do

- ALWAYS run existing tests before AND after changes
- ALWAYS update `.github/context/` files if your changes affect architecture, API surface, or module structure (last step of every task)
- ALWAYS use parameterized SQL -- never f-strings for WHERE/SET clauses
- ALWAYS delegate implementation to sub-tasks when available -- main thread is for reporting, deciding, and delegating
- ALWAYS use API-first approach -- build API endpoints first, UI comes after with mock data
- ALWAYS follow OWASP Top 10 best practices
- ALWAYS validate user input at the router level (Pydantic models)

---

## Guardrails: LLM / AI-Generated Code

AI assistants produce common failure modes that humans don't. These rules are **mandatory** for all AI-generated code:

### NEVER (LLM-specific)

- NEVER leave `TODO`, `FIXME`, `HACK`, `XXX`, or `PLACEHOLDER` in committed code -- implement it or don't write it
- NEVER generate "ghost implementations" -- functions that exist but are never called, imported, or tested
- NEVER add imports without verifying the module/function actually exists in the codebase or installed packages
- NEVER add a dependency to requirements.txt unless it's actually imported in source code
- NEVER generate placeholder/stub functions that return hardcoded values or `pass` -- if it's not implemented, don't create it
- NEVER over-abstract -- no base classes with a single subclass, no factory patterns for one type, no interfaces with one implementor
- NEVER add comments that just restate the code (`# increment counter` above `counter += 1`)
- NEVER silence errors with bare `except:`, `except Exception: pass`, or `except Exception as e: pass`
- NEVER generate "aspirational code" -- code for features nobody asked for
- NEVER hallucinate API endpoints, database columns, or config keys that don't exist

### ALWAYS (LLM-specific)

- ALWAYS verify every import resolves -- run the code or check `grep -r "def function_name\|class ClassName" .`
- ALWAYS verify new functions are actually called somewhere -- dead code is worse than no code
- ALWAYS keep functions under 50 lines -- if longer, split. LLMs tend to generate monoliths
- ALWAYS match existing code style in the file -- don't introduce new patterns alongside old ones
- ALWAYS check that generated tests actually test behavior, not just assert True or mock everything
- ALWAYS remove scaffolding code before committing -- temporary debug prints, commented-out blocks, example usage in `if __name__`
- ALWAYS run the code path you changed -- `python -c "from module import function"` at minimum
- ALWAYS prefer editing existing files over creating new ones -- LLMs default to creating; the answer is usually to extend what's there

### Verification Protocol

Before committing ANY AI-generated code, run this protocol:

```bash
# 1. No TODOs/FIXMEs left behind
grep -rn "TODO\|FIXME\|HACK\|XXX\|PLACEHOLDER" <changed_files>

# 2. No phantom imports
python -c "import ast, sys
for f in sys.argv[1:]:
    tree = ast.parse(open(f).read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            print(f'{f}: {ast.dump(node)}')" <changed_files>
# Then verify each import resolves

# 3. No dead functions (defined but never referenced elsewhere)
grep -rn "def " <changed_files> | while read line; do
    func=$(echo "$line" | grep -oP 'def \K\w+')
    refs=$(grep -rn "$func" . --include="*.py" | grep -v "def $func" | wc -l)
    [ "$refs" -eq 0 ] && echo "⚠️  DEAD: $func in $line"
done

# 4. No silenced exceptions
grep -rn "except.*pass$\|except:$" <changed_files>

# 5. No bloat -- functions over 50 lines
awk '/^def /{name=$0; start=NR} /^def |^class /{if(NR-start>50) print "⚠️  LONG: "name" ("NR-start" lines)"}' <changed_files>
```

---

## LLM Verification Checklist

Quick summary -- see **Guardrails: LLM / AI-Generated Code** section above for full rules.

Before committing AI-generated code, verify:

| Check | Command |
|-------|---------|
| No TODOs/FIXMEs | `grep -rn "TODO\|FIXME\|HACK\|XXX" <files>` |
| No phantom imports | `python -c "from <module> import <name>"` for each new import |
| No dead functions | Verify each new `def` is called/imported somewhere |
| No silenced errors | `grep -rn "except.*pass$" <files>` |
| No bloated functions | No function over 50 lines |
| No ghost dependencies | Every `requirements.txt` entry is actually imported |
| Tests test behavior | Tests assert real outcomes, not just `assert True` |
| Code actually runs | Execute the changed code path, don't just read it |
