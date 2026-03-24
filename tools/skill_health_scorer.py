#!/usr/bin/env python3
"""
Skill Health Scorer for the CheatCodes Skill Library.

Produces per-skill health scores based on soft gate compliance and git freshness.
Used by scheduled CI workflows to surface improvement opportunities proactively.

Usage:
    python skill_health_scorer.py              # Print health table to stdout
    python skill_health_scorer.py --json       # Output full JSON report to stdout
    python skill_health_scorer.py --report PATH  # Write Markdown report to PATH
    python skill_health_scorer.py --threshold N  # Exit 1 if any skill soft_score < N
    python skill_health_scorer.py --critical-only  # Exit 1 only on hard gate failures
"""

from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Bootstrap: import validators from co-located validate_skill.py
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skill import (  # noqa: E402
    _discover_skill_dirs,
    _load_registry,
    _load_skill_metadata,
    run_hard_gates,
    run_soft_gates,
)

REPO_ROOT: Path = Path(__file__).resolve().parent.parent

STATUS_ORDER = ["critical", "at-risk", "needs-attention", "good", "healthy"]

STATUS_EMOJI: Dict[str, str] = {
    "healthy": "🟢",
    "good": "🟡",
    "needs-attention": "🟠",
    "at-risk": "🔴",
    "critical": "💀",
}

GATE_GUIDANCE: Dict[str, str] = {
    "S1": (
        "Add a `## Compliance` section to `SKILL.md` documenting AI governance "
        "alignment, PII risk level, and model recommendation."
    ),
    "S2": (
        "Add or expand an `## Example Applications` section with at least 4 "
        "real-world use cases. Use a table or list format."
    ),
    "S3": (
        "Add a `## Platform Notes` section describing how this skill works on "
        "different platforms (CLI, web, IDE, any LLM)."
    ),
    "S4": (
        "Document all `{{VARIABLE}}` intake variables in a table: name, "
        "description, type, required/optional, default."
    ),
    "S5": (
        "Add an `## Anti-Patterns` section listing common misuses and the "
        "correct alternative. Format: ✗ Wrong → ✓ Right."
    ),
    "S6": (
        "Add `model_recommendation` to `skill.yaml` (haiku / sonnet / opus). "
        "Explain the tradeoff in the Compliance section."
    ),
    "S7": (
        "Add `risk_level` to `skill.yaml` (low / medium / high). "
        "Reference the risk framework in `docs/COMPLIANCE.md`."
    ),
    "S8": (
        "Add PII handling controls to the `## Compliance` section: what data "
        "is processed, how it's protected, and storage/transmission constraints."
    ),
}


# ===========================================================================
# Git freshness
# ===========================================================================

def _git_last_modified(skill_path: Path) -> Optional[str]:
    """Return ISO date of the last commit that touched this skill directory."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cd", "--date=short", "--", str(skill_path)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=10,
        )
        date_str = result.stdout.strip()
        if result.returncode == 0 and date_str:
            return date_str
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return None


def _days_since(date_str: str) -> Optional[int]:
    """Return number of days since a YYYY-MM-DD date string."""
    try:
        d = datetime.date.fromisoformat(date_str)
        return (datetime.date.today() - d).days
    except (ValueError, TypeError):
        return None


# ===========================================================================
# Core scoring
# ===========================================================================

def score_skill(skill_path: Path, registry: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Score a single skill. Returns a structured health record."""
    hard_results = run_hard_gates(skill_path, registry)
    soft_results = run_soft_gates(skill_path)

    hard_failed = [r for r in hard_results if not r.passed]
    soft_failed = [r for r in soft_results if not r.passed]
    soft_passed = [r for r in soft_results if r.passed]

    soft_score = len(soft_passed)
    has_hard_failure = bool(hard_failed)

    last_modified = _git_last_modified(skill_path)
    days_stale = _days_since(last_modified) if last_modified else None
    is_stale = days_stale is not None and days_stale > 90

    if has_hard_failure:
        status = "critical"
    elif soft_score <= 3:
        status = "at-risk"
    elif soft_score <= 5:
        status = "needs-attention"
    elif soft_score <= 7:
        status = "good"
    else:
        status = "healthy"

    meta, _ = _load_skill_metadata(skill_path)
    version = (meta or {}).get("version", "unknown")
    maturity = (meta or {}).get("maturity_status", "unknown")

    return {
        "name": skill_path.name,
        "version": version,
        "maturity_status": maturity,
        "status": status,
        "soft_score": soft_score,
        "soft_total": len(soft_results),
        "hard_passed": len(hard_results) - len(hard_failed),
        "hard_total": len(hard_results),
        "soft_failures": [
            {"gate_id": r.gate_id, "name": r.name, "message": r.message}
            for r in soft_failed
        ],
        "hard_failures": [
            {"gate_id": r.gate_id, "name": r.name, "message": r.message}
            for r in hard_failed
        ],
        "last_modified": last_modified,
        "days_stale": days_stale,
        "is_stale": is_stale,
    }


def _sort_key(s: Dict[str, Any]) -> tuple:
    """Sort: critical first, then by ascending soft_score, then name."""
    status_rank = STATUS_ORDER.index(s["status"]) if s["status"] in STATUS_ORDER else 99
    return (status_rank, s["soft_score"], s["name"])


# ===========================================================================
# Report generation
# ===========================================================================

def build_markdown_report(scores: List[Dict[str, Any]]) -> str:
    """Build a Markdown health report from all scored skills."""
    today = datetime.date.today().isoformat()
    total = len(scores)

    by_status: Dict[str, List] = {k: [] for k in STATUS_ORDER}
    for s in scores:
        by_status.get(s["status"], by_status["healthy"]).append(s)
    stale = [s for s in scores if s["is_stale"]]

    lines: List[str] = [
        f"# Skill Health Report — {today}",
        f"> Auto-generated by skill-health-report CI. {total} skills scored.",
        "",
        "## 📊 Summary",
        "",
        "| Status | Count | Threshold |",
        "|--------|-------|-----------|",
        f"| 🟢 Healthy | {len(by_status['healthy'])} | 8/8 soft gates |",
        f"| 🟡 Good | {len(by_status['good'])} | 6–7/8 soft gates |",
        f"| 🟠 Needs Attention | {len(by_status['needs-attention'])} | 4–5/8 soft gates |",
        f"| 🔴 At Risk | {len(by_status['at-risk'])} | ≤3/8 soft gates |",
        f"| 💀 Critical | {len(by_status['critical'])} | Any hard gate failure |",
        f"| ⏰ Stale | {len(stale)} | Not updated in 90+ days |",
        "",
        "## 🏥 Health Dashboard",
        "",
        "| Skill | Ver | Maturity | Status | Soft | Hard | Last Updated | Days |",
        "|-------|-----|----------|--------|------|------|--------------|------|",
    ]

    for s in sorted(scores, key=_sort_key):
        emoji = STATUS_EMOJI.get(s["status"], "❓")
        stale_tag = " ⏰" if s["is_stale"] else ""
        last = s["last_modified"] or "—"
        days = str(s["days_stale"]) if s["days_stale"] is not None else "—"
        lines.append(
            f"| `{s['name']}` | {s['version']} | {s['maturity_status']} | "
            f"{emoji} {s['status']}{stale_tag} | "
            f"{s['soft_score']}/{s['soft_total']} | "
            f"{s['hard_passed']}/{s['hard_total']} | {last} | {days} |"
        )

    lines += [""]

    # Improvement backlog
    improvements = [s for s in scores if s["soft_failures"] or s["hard_failures"]]
    if improvements:
        lines += [
            "## 🛠️ Improvement Backlog",
            "",
            "Sorted by priority (critical first, then lowest soft score):",
            "",
        ]
        for s in sorted(improvements, key=_sort_key):
            emoji = STATUS_EMOJI.get(s["status"], "❓")
            lines += [f"### {emoji} `{s['name']}` (v{s['version']})"]
            if s["hard_failures"]:
                lines += ["**Hard Gate Failures — must fix before merge:**"]
                for f in s["hard_failures"]:
                    lines += [f"- `{f['gate_id']}` **{f['name']}**: {f['message']}"]
            if s["soft_failures"]:
                lines += ["**Soft Gate Failures — improvement opportunities:**"]
                for f in s["soft_failures"]:
                    guidance = GATE_GUIDANCE.get(f["gate_id"], "")
                    lines += [f"- `{f['gate_id']}` **{f['name']}**: {f['message']}"]
                    if guidance:
                        lines += [f"  → *{guidance}*"]
            if s["is_stale"]:
                lines += [
                    f"- ⏰ **Stale**: Last updated {s['last_modified']} "
                    f"({s['days_stale']} days ago)"
                ]
            lines += [""]

    if stale:
        lines += [
            "## ⏰ Stale Skills (90+ Days Without Update)",
            "",
            "| Skill | Last Updated | Days Since Update |",
            "|-------|-------------|-------------------|",
        ]
        for s in sorted(stale, key=lambda x: x.get("days_stale") or 0, reverse=True):
            lines.append(
                f"| `{s['name']}` | {s['last_modified'] or '—'} | {s['days_stale']} |"
            )
        lines += [""]

    lines += [
        "---",
        "",
        "_Generated by "
        "[skill-health-report](.github/workflows/skill-health-report.yml) · "
        "See [GOVERNANCE.md](GOVERNANCE.md) for gate definitions._",
    ]
    return "\n".join(lines)


# ===========================================================================
# CLI output
# ===========================================================================

def print_table(scores: List[Dict[str, Any]]) -> None:
    """Print a compact colour-coded health table to stdout."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

    header = f"{'Skill':<36} {'Status':<20} {'Soft':<6} {'Hard':<6} Last Updated"
    print(f"\n{header}")
    print("-" * 80)
    for s in sorted(scores, key=_sort_key):
        if s["status"] in ("healthy", "good"):
            color = GREEN
        elif s["status"] == "needs-attention":
            color = YELLOW
        else:
            color = RED
        stale = " ⏰" if s["is_stale"] else ""
        print(
            f"{s['name']:<36} "
            f"{color}{s['status']:<18}{RESET}{stale}  "
            f"{s['soft_score']}/{s['soft_total']}  "
            f"{s['hard_passed']}/{s['hard_total']}  "
            f"{s['last_modified'] or '—'}"
        )


# ===========================================================================
# CLI entry point
# ===========================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score the health of all skills in the CheatCodes library.",
        epilog="See GOVERNANCE.md for full gate definitions.",
    )
    parser.add_argument("--json", action="store_true", help="Output full JSON report to stdout")
    parser.add_argument(
        "--report", metavar="PATH",
        help="Write a Markdown health report to PATH (creates parent dirs as needed)",
    )
    parser.add_argument(
        "--threshold", type=int, default=0, metavar="N",
        help="Exit 1 if any skill's soft_score is below N (0 = disabled)",
    )
    parser.add_argument(
        "--critical-only", action="store_true",
        help="Exit 1 only when there are hard gate failures (ignore soft scores)",
    )
    args = parser.parse_args()

    registry = _load_registry(REPO_ROOT)
    skill_dirs = _discover_skill_dirs(REPO_ROOT)

    if not skill_dirs:
        print("No skill directories found.")
        sys.exit(0)

    scores = [score_skill(d, registry) for d in skill_dirs]

    # --- JSON mode (always exits 0 — output is consumed by CI steps) ---
    if args.json:
        print(json.dumps({
            "generated": datetime.date.today().isoformat(),
            "skill_count": len(scores),
            "skills": scores,
        }, indent=2))
        return

    # --- Report mode (always exits 0 — alerting is handled by the issue-creation step) ---
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(build_markdown_report(scores), encoding="utf-8")
        print(f"Report written to {report_path}")
        return

    # --- Table mode: print + apply exit code logic ---
    print_table(scores)

    critical_skills = [s for s in scores if s["status"] == "critical"]
    below_threshold = [
        s for s in scores
        if args.threshold > 0 and s["soft_score"] < args.threshold
    ]

    if args.critical_only:
        if critical_skills:
            print(f"\n{len(critical_skills)} skill(s) have hard gate failures:", file=sys.stderr)
            for s in critical_skills:
                print(f"  - {s['name']}", file=sys.stderr)
            sys.exit(1)
        return

    if critical_skills or below_threshold:
        if critical_skills:
            print(f"\n{len(critical_skills)} skill(s) have hard gate failures.", file=sys.stderr)
        if below_threshold:
            print(
                f"{len(below_threshold)} skill(s) score below threshold {args.threshold}:",
                file=sys.stderr,
            )
            for s in below_threshold:
                print(f"  - {s['name']} (score: {s['soft_score']})", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
