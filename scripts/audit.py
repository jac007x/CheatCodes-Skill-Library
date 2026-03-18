#!/usr/bin/env python3
"""
audit.py — CheatCodes Skill Library automated audit tool.

Analyses the entire skill library and produces:
  - A health report (missing fields, outdated skills, structural issues)
  - Gap analysis (underrepresented categories, missing skill types)
  - Improvement suggestions
  - A roadmap of recommended actions

Designed to run weekly in CI and post results as a GitHub issue.

Usage:
    python scripts/audit.py                         # print to stdout
    python scripts/audit.py --output report.md      # write to file
"""

import argparse
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Run: pip install pyyaml")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

TODAY = date.today()
STALE_THRESHOLD_DAYS = 180  # skills not updated in 6 months
BETA_THRESHOLD_DAYS = 90    # beta skills older than 3 months should be promoted

EXPECTED_CATEGORIES = {
    "productivity",
    "automation",
    "communication",
    "data",
    "devops",
    "security",
}

# Skills commonly needed in well-rounded libraries
COMMON_SKILL_PATTERNS = [
    ("productivity", "goal-setting"),
    ("productivity", "time-blocker"),
    ("automation", "test-writer"),
    ("automation", "documentation-generator"),
    ("communication", "email-drafter"),
    ("communication", "slack-update-writer"),
    ("data", "sql-query-builder"),
    ("data", "dashboard-designer"),
    ("devops", "incident-runbook"),
    ("devops", "deployment-checklist"),
    ("security", "threat-model"),
    ("security", "security-review"),
]


def load_manifest(skill_dir: Path) -> dict[str, Any] | None:
    manifest_path = skill_dir / "skill.yaml"
    if not manifest_path.exists():
        return None
    try:
        with open(manifest_path) as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError:
        return None


def get_all_skills() -> list[tuple[Path, dict[str, Any]]]:
    skills = []
    for manifest_path in SKILLS_DIR.rglob("skill.yaml"):
        skill_dir = manifest_path.parent
        manifest = load_manifest(skill_dir)
        if manifest:
            skills.append((skill_dir, manifest))
    return skills


def parse_date(date_str: str | None) -> date | None:
    if not date_str:
        return None
    try:
        return datetime.strptime(str(date_str), "%Y-%m-%d").date()
    except ValueError:
        return None


def days_since(d: date | None) -> int | None:
    if d is None:
        return None
    return (TODAY - d).days


def audit_skill(
    skill_dir: Path, manifest: dict[str, Any]
) -> dict[str, list[str]]:
    """Return a dict of {severity: [findings]} for a single skill."""
    findings: dict[str, list[str]] = {"critical": [], "warning": [], "suggestion": []}
    rel = skill_dir.relative_to(REPO_ROOT)

    # Missing required fields
    for field in ["name", "description", "author", "version", "status", "changelog"]:
        if not manifest.get(field):
            findings["critical"].append(f"`{rel}`: missing required field `{field}`")

    # Stale skill
    updated = parse_date(manifest.get("updated"))
    staleness = days_since(updated)
    if staleness is not None and staleness > STALE_THRESHOLD_DAYS:
        findings["warning"].append(
            f"`{rel}`: not updated in {staleness} days — review for relevance"
        )

    # Beta too long
    status = manifest.get("status", "")
    if status == "beta":
        created = parse_date(manifest.get("created"))
        age = days_since(created)
        if age is not None and age > BETA_THRESHOLD_DAYS:
            findings["warning"].append(
                f"`{rel}`: has been in beta for {age} days — "
                f"consider promoting to stable or archiving"
            )

    # No examples in manifest
    examples = manifest.get("examples", [])
    if not examples:
        findings["suggestion"].append(
            f"`{rel}`: add at least one example to `skill.yaml` to help discovery"
        )

    # Missing tags
    tags = manifest.get("tags", [])
    if not tags:
        findings["suggestion"].append(
            f"`{rel}`: add tags to improve searchability"
        )

    # Missing long_description
    if not manifest.get("long_description"):
        findings["suggestion"].append(
            f"`{rel}`: add `long_description` for richer documentation"
        )

    # README missing
    if not (skill_dir / "README.md").exists():
        findings["critical"].append(f"`{rel}`: missing README.md")

    return findings


def find_coverage_gaps(skills: list[tuple[Path, dict[str, Any]]]) -> list[str]:
    """Identify missing categories and common skill patterns."""
    existing_categories: set[str] = set()
    existing_skills: set[tuple[str, str]] = set()

    for skill_dir, manifest in skills:
        cat = manifest.get("category", "")
        name = manifest.get("name", "")
        if cat:
            existing_categories.add(cat)
        if cat and name:
            existing_skills.add((cat, name))

    gaps: list[str] = []

    # Missing categories
    for cat in EXPECTED_CATEGORIES - existing_categories:
        gaps.append(
            f"Category `{cat}` has no skills — consider adding foundational skills "
            f"for this area"
        )

    # Common patterns not yet present
    for pattern_cat, pattern_name in COMMON_SKILL_PATTERNS:
        if (pattern_cat, pattern_name) not in existing_skills:
            gaps.append(
                f"No `{pattern_name}` skill in `{pattern_cat}` — "
                f"commonly needed in skills libraries"
            )

    return gaps


def compute_health_score(
    all_findings: list[dict[str, list[str]]], total_skills: int
) -> int:
    """Compute a simple 0–100 health score."""
    if total_skills == 0:
        return 0
    critical = sum(len(f["critical"]) for f in all_findings)
    warnings = sum(len(f["warning"]) for f in all_findings)
    score = max(0, 100 - (critical * 10) - (warnings * 3))
    return min(100, score)


def generate_report(
    skills: list[tuple[Path, dict[str, Any]]],
    all_findings: list[dict[str, list[str]]],
    gaps: list[str],
) -> str:
    total_skills = len(skills)
    critical_count = sum(len(f["critical"]) for f in all_findings)
    warning_count = sum(len(f["warning"]) for f in all_findings)
    suggestion_count = sum(len(f["suggestion"]) for f in all_findings)
    health_score = compute_health_score(all_findings, total_skills)

    # Category breakdown
    category_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for _, manifest in skills:
        cat = manifest.get("category", "unknown")
        status = manifest.get("status", "unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    lines: list[str] = [
        "# 📋 CheatCodes Skill Library — Weekly Audit Report",
        "",
        f"**Date:** {TODAY.strftime('%Y-%m-%d')}  ",
        f"**Total Skills:** {total_skills}  ",
        f"**Library Health Score:** {health_score}/100",
        "",
        "---",
        "",
        "## 📊 Library Overview",
        "",
        "### Skills by Category",
        "",
        "| Category | Count |",
        "|----------|-------|",
    ]
    for cat, count in sorted(category_counts.items()):
        lines.append(f"| {cat} | {count} |")

    lines += [
        "",
        "### Skills by Status",
        "",
        "| Status | Count |",
        "|--------|-------|",
    ]
    for status, count in sorted(status_counts.items()):
        emoji = {"stable": "✅", "beta": "⚠️", "deprecated": "🔻", "archived": "🗄️"}.get(
            status, "❓"
        )
        lines.append(f"| {emoji} {status} | {count} |")

    lines += [
        "",
        "---",
        "",
        "## 🔴 Critical Issues",
        f"*{critical_count} issue(s) require immediate attention.*",
        "",
    ]
    critical_items = [
        item
        for f in all_findings
        for item in f["critical"]
    ]
    if critical_items:
        for item in critical_items:
            lines.append(f"- {item}")
    else:
        lines.append("_No critical issues found. 🎉_")

    lines += [
        "",
        "---",
        "",
        "## 🟠 Warnings",
        f"*{warning_count} warning(s) should be addressed soon.*",
        "",
    ]
    warning_items = [item for f in all_findings for item in f["warning"]]
    if warning_items:
        for item in warning_items:
            lines.append(f"- {item}")
    else:
        lines.append("_No warnings. 👍_")

    lines += [
        "",
        "---",
        "",
        "## 💡 Improvement Suggestions",
        f"*{suggestion_count} suggestion(s) to improve quality and discoverability.*",
        "",
    ]
    suggestion_items = [item for f in all_findings for item in f["suggestion"]]
    if suggestion_items:
        for item in suggestion_items:
            lines.append(f"- {item}")
    else:
        lines.append("_No suggestions. 🚀_")

    lines += [
        "",
        "---",
        "",
        "## 🗺️ Gap Analysis",
        "*Skills and categories that are missing from the library.*",
        "",
    ]
    if gaps:
        for gap in gaps:
            lines.append(f"- {gap}")
    else:
        lines.append("_No significant gaps detected._")

    lines += [
        "",
        "---",
        "",
        "## 📅 Recommended Roadmap Actions",
        "",
        "Based on this audit, the following actions are recommended for the next review cycle:",
        "",
    ]

    priority = 1
    for item in critical_items:
        lines.append(f"{priority}. 🔴 **[Critical]** {item}")
        priority += 1
    for item in warning_items:
        lines.append(f"{priority}. 🟠 **[Warning]** {item}")
        priority += 1
    for gap in gaps[:5]:  # Top 5 gaps
        lines.append(f"{priority}. 🆕 **[Gap]** {gap}")
        priority += 1
    for item in suggestion_items[:5]:  # Top 5 suggestions
        lines.append(f"{priority}. 💡 **[Suggestion]** {item}")
        priority += 1

    if priority == 1:
        lines.append("_Nothing urgent. Keep up the great work!_")

    lines += [
        "",
        "---",
        "",
        "## ✅ Review Checklist",
        "",
        "Use this checklist during your 2–3× weekly review:",
        "",
        "- [ ] Review and triage critical issues above",
        "- [ ] Approve, reject, or prioritise warning items",
        "- [ ] Select 1–2 gap items to schedule for the next sprint",
        "- [ ] Review any open beta skills for promotion to stable",
        "- [ ] Approve or close pending Skill Request issues",
        "- [ ] Approve or merge pending Community Contribution PRs",
        "",
        "---",
        "",
        "*This report was generated automatically by `scripts/audit.py`. "
        "To run manually: `python scripts/audit.py`*",
    ]

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit the CheatCodes Skill Library and generate a roadmap report"
    )
    parser.add_argument("--output", "-o", help="Write report to this file path")
    args = parser.parse_args()

    skills = get_all_skills()
    all_findings: list[dict[str, list[str]]] = []

    for skill_dir, manifest in skills:
        findings = audit_skill(skill_dir, manifest)
        all_findings.append(findings)

    gaps = find_coverage_gaps(skills)
    report = generate_report(skills, all_findings, gaps)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)
        print(f"Audit report written to: {output_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
