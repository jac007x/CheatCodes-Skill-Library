#!/bin/sh
#
# Pre-commit hook for CheatCodes-Skill-Library
# Checks staged files for secrets, internal URLs, PII, signal logs, and pre-universalized content.
# Must complete in < 5 seconds.
#

set -e

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    echo "Pre-commit: no staged files to check."
    exit 0
fi

FAILED=0

# ---------------------------------------------------------------------------
# Helper: check a single pattern against all staged text files.
#   usage: check_pattern <label> <grep_extended_pattern>
# ---------------------------------------------------------------------------
check_pattern() {
    label="$1"
    pattern="$2"

    for file in $STAGED_FILES; do
        # Skip files that no longer exist on disk (deletes already filtered, but be safe)
        [ -f "$file" ] || continue

        # Skip binary / image files by extension
        case "$file" in
            *.png|*.jpg|*.jpeg|*.gif|*.ico|*.svg|*.bmp|*.tiff|*.webp) continue ;;
            *.woff|*.woff2|*.ttf|*.eot) continue ;;
            *.zip|*.tar|*.gz|*.bz2|*.xz|*.7z|*.jar|*.war) continue ;;
            *.pdf|*.doc|*.docx|*.xls|*.xlsx|*.ppt|*.pptx) continue ;;
            *.exe|*.dll|*.so|*.dylib|*.o|*.a|*.pyc|*.class) continue ;;
            *.mp3|*.mp4|*.wav|*.avi|*.mov|*.mkv) continue ;;
        esac

        # Search only the staged version of the file (not the working-tree copy)
        matches=$(git show ":$file" 2>/dev/null | grep -nE "$pattern" 2>/dev/null) || true

        if [ -n "$matches" ]; then
            echo "BLOCKED  [$label]"
            echo "  File: $file"
            echo "$matches" | while IFS= read -r line; do
                echo "    $line"
            done
            echo ""
            FAILED=1
        fi
    done
}

# ---------------------------------------------------------------------------
# 1. No secrets
# ---------------------------------------------------------------------------
check_pattern "Secret / credential detected" \
    '(api_key\s*=|password\s*=|token\s*=|ghp_[A-Za-z0-9]+|sk-[A-Za-z0-9]+|xox[bpars]-[A-Za-z0-9]+)'

# ---------------------------------------------------------------------------
# 2. No internal URLs
#    Match these hostnames when they appear as part of a URL (preceded by // or a dot).
# ---------------------------------------------------------------------------
check_pattern "Internal URL detected" \
    '(https?://(([a-zA-Z0-9._-]+\.)?walmart\.com|([a-zA-Z0-9._-]+\.)?wal-mart\.com|one\.walmart|dx\.walmart|wibey\.walmart|puppy\.walmart))'

# ---------------------------------------------------------------------------
# 3. No PII email patterns (internal email addresses)
# ---------------------------------------------------------------------------
check_pattern "Internal email (PII) detected" \
    '[A-Za-z0-9._%+-]+@(walmart\.com|wal-mart\.com)'

# ---------------------------------------------------------------------------
# 4. No .jsonl files (signal logs)
# ---------------------------------------------------------------------------
for file in $STAGED_FILES; do
    case "$file" in
        *.jsonl)
            echo "BLOCKED  [Signal log (.jsonl) file detected]"
            echo "  File: $file"
            echo ""
            FAILED=1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# 5. No files under skills/ directory (pre-universalized content)
# ---------------------------------------------------------------------------
for file in $STAGED_FILES; do
    case "$file" in
        skills/*)
            echo "BLOCKED  [Pre-universalized content in skills/ directory]"
            echo "  File: $file"
            echo ""
            FAILED=1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------
if [ "$FAILED" -ne 0 ]; then
    echo "---------------------------------------------"
    echo "Commit blocked. Fix the issues above and retry."
    exit 1
fi

echo "Pre-commit checks passed"
exit 0
