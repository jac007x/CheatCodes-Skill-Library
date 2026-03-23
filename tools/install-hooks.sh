#!/bin/sh
#
# Installs the pre-commit hook for CheatCodes-Skill-Library.
#

set -e

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
    echo "Error: not inside a git repository." >&2
    exit 1
}

HOOK_SRC="$REPO_ROOT/tools/pre-commit-hook.sh"
HOOK_DST="$REPO_ROOT/.git/hooks/pre-commit"

if [ ! -f "$HOOK_SRC" ]; then
    echo "Error: source hook not found at $HOOK_SRC" >&2
    exit 1
fi

cp "$HOOK_SRC" "$HOOK_DST"
chmod +x "$HOOK_DST"

echo "Pre-commit hook installed successfully."
echo "  Source: $HOOK_SRC"
echo "  Installed to: $HOOK_DST"
