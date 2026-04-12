#!/bin/sh
set -e

# Batten installer
# Usage: curl -sL https://raw.githubusercontent.com/ehowardtillit/batten/main/install.sh | sh
# Or:    curl -sL https://raw.githubusercontent.com/ehowardtillit/batten/main/install.sh | sh -s my-project

REPO="gh:ehowardtillit/batten"
TARGET="${1:-.}"

info()  { printf '\033[0;34m[batten]\033[0m %s\n' "$1"; }
ok()    { printf '\033[0;32m[batten]\033[0m %s\n' "$1"; }
err()   { printf '\033[0;31m[batten]\033[0m %s\n' "$1" >&2; }

info "Batten installer"

# -- Check dependencies -------------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
    err "python3 is required but not found."
    err "Install Python 3.11+ from https://python.org"
    exit 1
fi

if ! command -v pip3 >/dev/null 2>&1 && ! python3 -m pip --version >/dev/null 2>&1; then
    err "pip is required but not found."
    err "Install with: python3 -m ensurepip --upgrade"
    exit 1
fi

PIP="pip3"
if ! command -v pip3 >/dev/null 2>&1; then
    PIP="python3 -m pip"
fi

# -- Install Copier if needed -------------------------------------------------

if ! command -v copier >/dev/null 2>&1; then
    info "Installing Copier..."
    $PIP install --user "copier>=9,<11" >/dev/null 2>&1 || $PIP install "copier>=9,<11" >/dev/null 2>&1
    if ! command -v copier >/dev/null 2>&1; then
        COPIER_PATH=$(python3 -c "import site; print(site.getusersitepackages().replace('lib/python','bin').rsplit('lib',1)[0] + 'bin')" 2>/dev/null || true)
        if [ -n "$COPIER_PATH" ] && [ -x "$COPIER_PATH/copier" ]; then
            export PATH="$COPIER_PATH:$PATH"
        fi
    fi
    if ! command -v copier >/dev/null 2>&1; then
        err "Failed to install Copier. Install manually: pip install 'copier>=9,<11'"
        exit 1
    fi
    ok "Copier installed."
else
    ok "Copier found."
fi

# -- Scaffold ------------------------------------------------------------------

if [ "$TARGET" = "." ]; then
    info "Scaffolding Batten into current directory..."
    copier copy --trust "$REPO" .
else
    info "Scaffolding Batten into $TARGET..."
    copier copy --trust "$REPO" "$TARGET"
    cd "$TARGET"
fi

chmod +x batten 2>/dev/null || true
chmod +x bootstrap.sh 2>/dev/null || true

# -- Init git if needed --------------------------------------------------------

if [ ! -d .git ]; then
    info "Initializing git repository..."
    git init -q
    git add -A
    git commit -q -m "feat: init from Batten scaffold"
    ok "Git initialized with initial commit."
fi

# -- Install -------------------------------------------------------------------

info "Running ./batten install..."
echo ""
./batten install

echo ""
ok "Done. Your project is ready."
echo ""
info "Next steps:"
echo "  1. Edit batten.yml to configure your stack"
echo "  2. Run ./batten regenerate to apply changes"
echo "  3. Run ./batten status to verify"
echo ""
