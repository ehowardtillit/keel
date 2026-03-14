#!/usr/bin/env bash
# ⚓ KEEL Bootstrap -- run once after cloning a KEEL-based project
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${BOLD}⚓ $1${NC}"; }
ok()    { echo -e "${GREEN}✅ $1${NC}"; }
warn()  { echo -e "${YELLOW}⚠️  $1${NC}"; }
fail()  { echo -e "${RED}❌ $1${NC}"; exit 1; }

echo ""
info "KEEL Bootstrap -- KEEL Enforces Engineering Layouts"
echo ""

# --- 1. Check Python ---
info "Checking Python..."
if ! command -v python3 &>/dev/null; then
    fail "Python 3 not found. Install Python 3.11+ first."
fi
PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
ok "Python ${PYVER}"

# --- 2. Create virtual environment ---
info "Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    ok "Created .venv"
else
    ok ".venv already exists"
fi
# shellcheck disable=SC1091
source .venv/bin/activate

# --- 3. Install pre-commit ---
info "Installing pre-commit..."
pip install --quiet pre-commit
ok "pre-commit $(pre-commit --version | awk '{print $2}')"

# --- 4. Install dev tools ---
info "Installing development tools..."
pip install --quiet ruff bandit pytest pytest-cov pip-audit detect-secrets
ok "Dev tools installed (ruff, bandit, pytest, pip-audit)"

# --- 5. Install git hooks ---
info "Installing git hooks..."
if [ ! -d ".git" ]; then
    fail "Not a git repository. Run 'git init' first."
fi
pre-commit install --quiet
ok "Pre-commit hooks installed"

# --- 6. Generate secrets baseline ---
info "Generating secrets baseline..."
detect-secrets scan \
    --exclude-files '\.venv|venv|__pycache__|node_modules|\.git|docs/book' \
    > .secrets.baseline
FINDINGS=$(python3 -c "import json; d=json.load(open('.secrets.baseline')); print(sum(len(v) for v in d.get('results',{}).values()))")
ok "Secrets baseline generated (${FINDINGS} known findings to review)"

if [ "$FINDINGS" -gt 0 ]; then
    warn "Review findings: python3 -c \"import json; [print(f'{k}: {len(v)} findings') for k,v in json.load(open('.secrets.baseline'))['results'].items()]\""
fi

# --- 7. Download pre-commit hook environments ---
info "Downloading hook environments (first run may take ~2 min)..."
pre-commit run --all-files &>/dev/null || true
ok "Hook environments cached"

# --- 8. Customization checklist ---
echo ""
info "Customize these files for your project:"
echo ""
echo "  .github/copilot-instructions.md  → Add project overview and directory map"
echo "  .github/context/ARCHITECTURE.md  → Describe your system design"
echo "  .github/context/API_SURFACE.md   → Document your API endpoints"
echo "  .github/context/MODULE_MAP.md    → List your modules"
echo "  .github/context/CONVENTIONS.md   → Add project-specific conventions"
echo "  .github/CODEOWNERS               → Set your GitHub username"
echo "  .github/workflows/ci.yml         → Adjust source paths and test commands"
echo ""
ok "KEEL bootstrap complete ⚓"
echo ""
warn "Run 'source .venv/bin/activate' before using make commands"
