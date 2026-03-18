#!/usr/bin/env bash
# clone-skill.sh — Clone a CheatCodes skill into your current directory.
#
# USAGE
#   bash <(curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh) <category>/<skill-name> [OPTIONS]
#
# OPTIONS
#   --version <vX>   Clone a specific version folder (e.g., --version v1)
#                    Default: clones the whole skill directory (all versions)
#   --list           List all available skills
#   --dest <dir>     Clone into <dir> instead of ./<skill-name>
#
# EXAMPLES
#   Clone latest (all versions):
#     bash clone-skill.sh productivity/task-planner
#
#   Clone only v1:
#     bash clone-skill.sh productivity/task-planner --version v1
#
#   List all skills:
#     bash clone-skill.sh --list

set -euo pipefail

REPO="jac007x/CheatCodes-Skill-Library"
BASE_URL="https://raw.githubusercontent.com/${REPO}/main"
API_URL="https://api.github.com/repos/${REPO}/contents"
BRANCH="main"

# ── Colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}[info]${RESET}  $*"; }
success() { echo -e "${GREEN}[done]${RESET}  $*"; }
warn()    { echo -e "${YELLOW}[warn]${RESET}  $*"; }
error()   { echo -e "${RED}[error]${RESET} $*" >&2; exit 1; }

# ── Dependency check ─────────────────────────────────────────────────────────
require() { command -v "$1" >/dev/null 2>&1 || error "Required tool not found: $1"; }
require curl
require git

# ── Argument parsing ──────────────────────────────────────────────────────────
SKILL_PATH=""
VERSION=""
DEST=""
LIST_MODE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list)        LIST_MODE=true; shift ;;
    --version)     VERSION="$2"; shift 2 ;;
    --dest)        DEST="$2"; shift 2 ;;
    -*)            error "Unknown option: $1" ;;
    *)             SKILL_PATH="$1"; shift ;;
  esac
done

# ── List mode ─────────────────────────────────────────────────────────────────
if $LIST_MODE; then
  info "Fetching skill list from ${REPO}…"
  SKILLS_URL="${API_URL}/skills"
  # Iterate categories
  CATEGORIES=$(curl -fsSL "${SKILLS_URL}" | grep -o '"name": "[^"]*"' | grep -v 'README' | sed 's/"name": "//;s/"//')
  echo ""
  echo -e "${BOLD}Available skills:${RESET}"
  echo ""
  while IFS= read -r cat; do
    SKILL_LIST=$(curl -fsSL "${SKILLS_URL}/${cat}" | grep -o '"name": "[^"]*"' | grep -v 'README\|skill.yaml' | sed 's/"name": "//;s/"//')
    while IFS= read -r skill; do
      printf "  %-15s %s\n" "${cat}" "${skill}"
    done <<< "$SKILL_LIST"
  done <<< "$CATEGORIES"
  echo ""
  exit 0
fi

# ── Validate skill path ───────────────────────────────────────────────────────
[[ -z "$SKILL_PATH" ]] && error "Usage: clone-skill.sh <category>/<skill-name> [--version <vX>]"

# Normalise path (strip leading skills/ if provided)
SKILL_PATH="${SKILL_PATH#skills/}"
IFS='/' read -r CATEGORY SKILL_NAME <<< "$SKILL_PATH"
[[ -z "$CATEGORY" || -z "$SKILL_NAME" ]] && error "Skill path must be <category>/<skill-name>"

# ── Destination ───────────────────────────────────────────────────────────────
DEST="${DEST:-${SKILL_NAME}}"

# ── Clone using sparse checkout ───────────────────────────────────────────────
REMOTE="https://github.com/${REPO}.git"
SPARSE_PATH="skills/${CATEGORY}/${SKILL_NAME}"
[[ -n "$VERSION" ]] && SPARSE_PATH="${SPARSE_PATH}/${VERSION}"

info "Cloning ${BOLD}${SKILL_PATH}${RESET}${VERSION:+ (${VERSION})} into ${BOLD}./${DEST}${RESET}…"

# If destination already exists, bail
[[ -d "$DEST" ]] && error "Destination './${DEST}' already exists. Remove it first or use --dest."

# Use sparse checkout for efficiency (avoids downloading the entire repo)
git clone --depth 1 --filter=blob:none --sparse "$REMOTE" "$DEST" --quiet

cd "$DEST"
git sparse-checkout set "$SPARSE_PATH" --quiet

# Move the cloned sub-tree to the root of the destination for convenience
if [[ -d "$SPARSE_PATH" ]]; then
  # Copy contents up to the destination root
  shopt -s dotglob
  mv "${SPARSE_PATH}"/* . 2>/dev/null || true
  # Remove the now-empty scaffolding directories
  rm -rf "skills"
fi

# Remove the .git folder so users get a clean working copy
rm -rf .git

cd ..
success "Skill '${SKILL_PATH}'${VERSION:+ version '${VERSION}'} cloned into './${DEST}'"
echo ""
echo -e "  ${BOLD}Next steps:${RESET}"
echo -e "  1. Open ${CYAN}./${DEST}/README.md${RESET} for usage instructions."
if [[ -n "$VERSION" ]]; then
  echo -e "  2. Copy ${CYAN}./${DEST}/prompt.md${RESET} into your AI assistant."
else
  echo -e "  2. Browse version folders and pick the prompt you want."
fi
echo ""
