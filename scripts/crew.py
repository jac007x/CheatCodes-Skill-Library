#!/usr/bin/env python3
"""
crew.py — CheatCodes Skill Library Automated Review Crew
=========================================================

Three specialist agents continuously review the skill library and produce
a prioritised roadmap report for the maintainer's 2–3× weekly review session.

  🏛️  Librarian  — Structural health: required fields, freshness, changelog
  🔭  Scout      — Gap analysis: missing skills, categories, adoption candidates
  🎯  Coach      — Quality: per-skill prompt quality and improvement suggestions

Usage:
    python scripts/crew.py                    # print to stdout
    python scripts/crew.py --output report.md # write to file
    python scripts/crew.py --agent librarian  # run one agent only
    python scripts/crew.py --agent scout
    python scripts/crew.py --agent coach

Runs automatically every Monday via .github/workflows/skill-audit.yml.
"""

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Run: pip install pyyaml")
    sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
TODAY = date.today()

# ── Thresholds ────────────────────────────────────────────────────────────────
STALE_DAYS = 180   # warn if a skill hasn't been updated in 6 months
BETA_DAYS  = 90    # warn if a beta skill is older than 3 months

# ── Known skill patterns Scout looks for ─────────────────────────────────────
# Curated list of skill types that are well-established in the AI prompting
# community and could be standardised for CheatCodes.
ADOPTION_CANDIDATES: list[dict[str, str]] = [
    # Communication
    {"name": "email-drafter",        "category": "communication",
     "tagline": "Draft professional emails from bullet points or rough notes",
     "source": "Widely requested; see awesome-chatgpt-prompts 'email' patterns"},
    {"name": "slack-update-writer",  "category": "communication",
     "tagline": "Convert work updates into clean, concise Slack messages",
     "source": "Async-first team communication pattern"},
    {"name": "feedback-writer",      "category": "communication",
     "tagline": "Write constructive, specific performance feedback",
     "source": "HR / management coaching pattern"},
    # Productivity
    {"name": "goal-setting",         "category": "productivity",
     "tagline": "Set SMART goals with measurable milestones using OKR / SMART framework",
     "source": "OKR / SMART framework prompting pattern"},
    {"name": "time-blocker",         "category": "productivity",
     "tagline": "Build a time-blocked daily schedule from a priority list",
     "source": "Deep-work / time-blocking methodology"},
    {"name": "retrospective-facilitator", "category": "productivity",
     "tagline": "Run a structured team retrospective (Start/Stop/Continue or 4Ls)",
     "source": "Agile / Scrum ceremonies — heavily searched"},
    # Automation
    {"name": "test-writer",          "category": "automation",
     "tagline": "Generate comprehensive unit tests for a function or module",
     "source": "GitHub Copilot patterns; github.com/topics/test-generation"},
    {"name": "documentation-generator", "category": "automation",
     "tagline": "Generate docstrings and README content from source code",
     "source": "Code documentation automation — github.com/topics/autodoc"},
    {"name": "pr-description-writer","category": "automation",
     "tagline": "Write a clear PR description from a diff or commit list",
     "source": "GitHub Copilot PR summary pattern; widely used"},
    # Data
    {"name": "sql-query-builder",    "category": "data",
     "tagline": "Convert plain-English questions into correct SQL queries",
     "source": "text-to-sql GitHub topic; LangChain SQL agent patterns"},
    {"name": "dashboard-designer",   "category": "data",
     "tagline": "Recommend KPI dashboards and metrics for a business goal",
     "source": "BI / analytics tooling pattern"},
    # DevOps
    {"name": "incident-runbook",     "category": "devops",
     "tagline": "Create step-by-step runbooks for common incident types",
     "source": "SRE / ops tooling — PagerDuty, OpsGenie prompt patterns"},
    {"name": "deployment-checklist", "category": "devops",
     "tagline": "Generate a safe deployment checklist for a service",
     "source": "DevOps best practices — widely reused"},
    # Security
    {"name": "threat-model",         "category": "security",
     "tagline": "Create a lightweight threat model for a feature using STRIDE",
     "source": "STRIDE / OWASP prompt patterns — security engineering community"},
    {"name": "security-review",      "category": "security",
     "tagline": "Review a system design or API for security risks",
     "source": "Secure-by-design review pattern — OWASP"},
]

EXPECTED_CATEGORIES = {"productivity", "automation", "communication", "data", "devops", "security"}


# ── Data helpers ──────────────────────────────────────────────────────────────

def _load_manifest(skill_dir: Path) -> dict[str, Any] | None:
    p = skill_dir / "skill.yaml"
    if not p.exists():
        return None
    try:
        with open(p) as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError:
        return None


def _get_all_skills() -> list[tuple[Path, dict[str, Any]]]:
    return [
        (mp.parent, m)
        for mp in sorted(SKILLS_DIR.rglob("skill.yaml"))
        if (m := _load_manifest(mp.parent)) is not None
    ]


def _parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(str(s), "%Y-%m-%d").date()
    except ValueError:
        return None


def _days_since(d: date | None) -> int | None:
    return None if d is None else (TODAY - d).days


def _version_dirs(skill_dir: Path) -> list[Path]:
    return sorted(
        (d for d in skill_dir.iterdir() if d.is_dir() and re.match(r"^v\d", d.name)),
        key=lambda d: d.name,
    )


def _read_prompt(skill_dir: Path) -> str:
    """Return concatenated text of all prompt.md files in a skill's version folders."""
    parts: list[str] = []
    for vd in _version_dirs(skill_dir):
        pf = vd / "prompt.md"
        if pf.exists():
            try:
                parts.append(pf.read_text(encoding="utf-8"))
            except OSError:
                pass
    return "\n".join(parts)


# ── 🏛️  Librarian — structural health ─────────────────────────────────────────

def librarian_run(skills: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    """
    The Librarian audits every skill for structural correctness and freshness.
    Returns a findings dict used by the Coordinator.
    """
    per_skill: list[dict[str, Any]] = []

    for skill_dir, manifest in skills:
        rel = str(skill_dir.relative_to(REPO_ROOT))
        findings: dict[str, list[str]] = {"critical": [], "warning": [], "note": []}

        # Required fields
        for field in ("name", "description", "author", "version", "status", "changelog"):
            if not manifest.get(field):
                findings["critical"].append(f"Missing required field `{field}`")

        # Status value
        status = manifest.get("status", "")
        if status and status not in {"beta", "stable", "deprecated", "archived"}:
            findings["critical"].append(f"Invalid status `{status}`")

        # Semver
        version = str(manifest.get("version", ""))
        parts = version.split(".")
        if version and not (len(parts) == 3 and all(p.split("-")[0].isdigit() for p in parts)):
            findings["warning"].append(f"Version `{version}` is not semver (MAJOR.MINOR.PATCH)")

        # README
        if not (skill_dir / "README.md").exists():
            findings["critical"].append("Missing README.md")

        # At least one versioned prompt
        ver_dirs = _version_dirs(skill_dir)
        if not ver_dirs:
            findings["critical"].append("No versioned directories (e.g. v1/) found")
        else:
            for vd in ver_dirs:
                if not (vd / "prompt.md").exists():
                    findings["critical"].append(f"Missing prompt.md in `{vd.name}/`")

        # Changelog is a non-empty list
        changelog = manifest.get("changelog")
        if changelog is not None and (not isinstance(changelog, list) or len(changelog) == 0):
            findings["warning"].append("`changelog` must be a non-empty list")

        # Staleness
        updated = _parse_date(manifest.get("updated"))
        staleness = _days_since(updated)
        if staleness is not None and staleness > STALE_DAYS:
            findings["warning"].append(
                f"Not updated in {staleness} days — review for relevance"
            )

        # Beta age
        if status == "beta":
            created = _parse_date(manifest.get("created"))
            age = _days_since(created)
            if age is not None and age > BETA_DAYS:
                findings["warning"].append(
                    f"Beta for {age} days — consider promoting to stable or archiving"
                )

        per_skill.append({"path": rel, "name": manifest.get("name", rel), "findings": findings})

    return {"per_skill": per_skill}


# ── 🔭  Scout — gap analysis + adoption ──────────────────────────────────────

def scout_run(skills: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    """
    The Scout maps the library's coverage, flags missing categories and skill
    patterns, and surfaces adoption candidates from the wider community.
    """
    present_cats: set[str] = set()
    present_skills: set[tuple[str, str]] = set()

    for skill_dir, manifest in skills:
        cat  = manifest.get("category", "")
        name = manifest.get("name", "")
        if cat:
            present_cats.add(cat)
        if cat and name:
            present_skills.add((cat, name))

    # Missing categories
    missing_cats: list[str] = sorted(EXPECTED_CATEGORIES - present_cats)

    # Adoption candidates not yet in the library
    new_candidates: list[dict[str, str]] = [
        c for c in ADOPTION_CANDIDATES
        if (c["category"], c["name"]) not in present_skills
    ]

    # Category breakdown
    cat_counts: dict[str, int] = {}
    for _, manifest in skills:
        cat = manifest.get("category", "unknown")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    return {
        "present_categories": sorted(present_cats),
        "missing_categories": missing_cats,
        "cat_counts": cat_counts,
        "adoption_candidates": new_candidates,
    }


# ── 🎯  Coach — prompt quality ────────────────────────────────────────────────

def coach_run(skills: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    """
    The Coach reviews each skill's prompt quality and suggests concrete improvements.
    """
    per_skill: list[dict[str, Any]] = []

    for skill_dir, manifest in skills:
        rel = str(skill_dir.relative_to(REPO_ROOT))
        suggestions: list[str] = []
        prompt_text = _read_prompt(skill_dir)

        # Tags / discoverability
        if not manifest.get("tags"):
            suggestions.append("Add `tags` to skill.yaml to improve search and discovery")

        # Examples in manifest
        if not manifest.get("examples"):
            suggestions.append("Add at least one `examples` entry to skill.yaml")

        # Long description
        if not manifest.get("long_description"):
            suggestions.append("Add `long_description` for richer documentation")

        if prompt_text:
            # Structured output (numbered sections or tables)
            has_structure = bool(
                re.search(r"^#{1,3} ", prompt_text, re.MULTILINE)
                or re.search(r"^\|.+\|", prompt_text, re.MULTILINE)
                or re.search(r"^\d+\.", prompt_text, re.MULTILINE)
            )
            if not has_structure:
                suggestions.append(
                    "Prompt output has no Markdown structure (headers/tables/numbered lists) "
                    "— adding structure makes AI output much easier to read"
                )

            # Placeholder check
            placeholders = re.findall(r"\[([A-Z][A-Z0-9 /]+)\]", prompt_text)
            if not placeholders:
                suggestions.append(
                    "No [PLACEHOLDER] tokens found — adding placeholders lets users "
                    "customise the prompt for their context"
                )

            # Role-setting ("You are a...")
            has_role = bool(re.search(r"you are (an? |the )", prompt_text, re.IGNORECASE))
            if not has_role:
                suggestions.append(
                    "Prompt doesn't set an AI role ('You are a …') — role-setting "
                    "significantly improves response quality"
                )

            # Beta skills with no second version
            if manifest.get("status") == "stable" and len(_version_dirs(skill_dir)) < 2:
                suggestions.append(
                    "Consider creating a v2-beta to explore improvements without "
                    "disrupting existing users"
                )

        per_skill.append({
            "path": rel,
            "name": manifest.get("name", rel),
            "suggestions": suggestions,
        })

    return {"per_skill": per_skill}


# ── Coordinator — assemble final report ───────────────────────────────────────

def _health_score(lib_findings: dict[str, Any]) -> int:
    """Compute a 0–100 health score from Librarian findings."""
    critical = sum(len(s["findings"]["critical"]) for s in lib_findings["per_skill"])
    warnings  = sum(len(s["findings"]["warning"])  for s in lib_findings["per_skill"])
    score = max(0, 100 - (critical * 10) - (warnings * 3))
    return min(100, score)


def coordinator_assemble(
    skills: list[tuple[Path, dict[str, Any]]],
    lib: dict[str, Any],
    scout: dict[str, Any],
    coach: dict[str, Any],
) -> str:
    """Assemble the three agents' findings into a single Markdown report."""
    total = len(skills)
    health = _health_score(lib)

    # Count totals
    total_critical = sum(len(s["findings"]["critical"]) for s in lib["per_skill"])
    total_warnings  = sum(len(s["findings"]["warning"])  for s in lib["per_skill"])
    total_notes     = sum(len(s["findings"]["note"])     for s in lib["per_skill"])
    total_coach     = sum(len(s["suggestions"])          for s in coach["per_skill"])

    lines: list[str] = [
        "# 🤖 CheatCodes Skill Library — Crew Review Report",
        "",
        f"**Date:** {TODAY.strftime('%Y-%m-%d')}  ",
        f"**Total Skills:** {total}  ",
        f"**Library Health Score:** {health}/100",
        "",
        "> Generated by the automated review crew: "
        "🏛️ Librarian · 🔭 Scout · 🎯 Coach",
        "",
        "---",
        "",
        "## 📊 Library Overview",
        "",
        "| Category | Skills |",
        "|----------|--------|",
    ]
    for cat, count in sorted(scout["cat_counts"].items()):
        lines.append(f"| {cat} | {count} |")

    # Status breakdown
    status_counts: dict[str, int] = {}
    for _, m in skills:
        s = m.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1
    lines += [
        "",
        "| Status | Count |",
        "|--------|-------|",
    ]
    badges = {"stable": "✅", "beta": "⚠️", "deprecated": "🔻", "archived": "🗄️"}
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {badges.get(status, '❓')} {status} | {count} |")

    # ── Librarian ─────────────────────────────────────────────────────────────
    lines += [
        "",
        "---",
        "",
        "## 🏛️ Librarian — Structural Health",
        "",
        f"*{total_critical} critical issue(s) · {total_warnings} warning(s)*",
        "",
    ]

    critical_items: list[str] = []
    warning_items:  list[str] = []
    for skill_data in lib["per_skill"]:
        path = skill_data["path"]
        for item in skill_data["findings"]["critical"]:
            critical_items.append(f"`{path}`: {item}")
        for item in skill_data["findings"]["warning"]:
            warning_items.append(f"`{path}`: {item}")

    if critical_items:
        lines.append("**🔴 Critical — fix before next release:**")
        lines.append("")
        for item in critical_items:
            lines.append(f"- {item}")
    else:
        lines.append("_No critical issues found. 🎉_")

    if warning_items:
        lines += ["", "**🟠 Warnings — address soon:**", ""]
        for item in warning_items:
            lines.append(f"- {item}")
    else:
        lines += ["", "_No warnings. 👍_"]

    # ── Scout ─────────────────────────────────────────────────────────────────
    lines += [
        "",
        "---",
        "",
        "## 🔭 Scout — Coverage & Adoption Opportunities",
        "",
    ]

    if scout["missing_categories"]:
        lines.append("**Missing categories** (no skills yet):")
        lines.append("")
        for cat in scout["missing_categories"]:
            lines.append(f"- `{cat}` — consider adding at least one foundational skill")
    else:
        lines.append("_All expected categories are represented. ✅_")

    lines += ["", "**Adoption candidates** — skills common in the wider AI prompting community that don't yet exist here:", ""]

    if scout["adoption_candidates"]:
        lines.append("| Skill | Category | What it does | Where to find inspiration |")
        lines.append("|-------|----------|--------------|--------------------------|")
        for c in scout["adoption_candidates"]:
            lines.append(
                f"| `{c['name']}` | {c['category']} "
                f"| {c['tagline']} | {c['source']} |"
            )
    else:
        lines.append("_All tracked adoption candidates are already in the library!_")

    # ── Coach ─────────────────────────────────────────────────────────────────
    lines += [
        "",
        "---",
        "",
        "## 🎯 Coach — Prompt Quality Suggestions",
        "",
        f"*{total_coach} suggestion(s) across {total} skill(s)*",
        "",
    ]

    any_suggestions = False
    for skill_data in coach["per_skill"]:
        if skill_data["suggestions"]:
            any_suggestions = True
            lines.append(f"**`{skill_data['path']}`**")
            for s in skill_data["suggestions"]:
                lines.append(f"- {s}")
            lines.append("")

    if not any_suggestions:
        lines.append("_No quality improvements suggested. 🚀_")

    # ── Roadmap actions ───────────────────────────────────────────────────────
    lines += [
        "",
        "---",
        "",
        "## 📅 Recommended Roadmap Actions",
        "",
        "Prioritised list for the maintainer's next review session:",
        "",
    ]

    n = 1
    for item in critical_items:
        lines.append(f"{n}. 🔴 **[Critical — Librarian]** {item}")
        n += 1
    for item in warning_items:
        lines.append(f"{n}. 🟠 **[Warning — Librarian]** {item}")
        n += 1
    for cat in scout["missing_categories"]:
        lines.append(f"{n}. 🆕 **[Gap — Scout]** Add foundational skills for `{cat}` category")
        n += 1
    # Top 5 adoption candidates
    for c in scout["adoption_candidates"][:5]:
        lines.append(
            f"{n}. 🔭 **[Adopt — Scout]** "
            f"Evaluate `{c['name']}` ({c['category']}): {c['tagline']}"
        )
        n += 1
    # Top 3 coach suggestions (one per skill)
    added_coach = 0
    for skill_data in coach["per_skill"]:
        if skill_data["suggestions"] and added_coach < 3:
            tip = skill_data["suggestions"][0]
            lines.append(
                f"{n}. 💡 **[Quality — Coach]** `{skill_data['path']}`: {tip}"
            )
            n += 1
            added_coach += 1

    if n == 1:
        lines.append("_Nothing urgent — keep up the great work!_")

    # ── Review checklist ──────────────────────────────────────────────────────
    lines += [
        "",
        "---",
        "",
        "## ✅ Maintainer Review Checklist",
        "",
        "Use during your 2–3× weekly review session:",
        "",
        "- [ ] Triage all 🔴 Critical issues above",
        "- [ ] Approve, reject, or defer 🟠 Warning items",
        "- [ ] Pick 1–2 🔭 Adoption candidates to schedule",
        "- [ ] Review beta skills for promotion to stable",
        "- [ ] Approve or close pending Skill Request issues",
        "- [ ] Review and merge pending Community Contribution PRs",
        "",
        "---",
        "",
        "*Generated by `scripts/crew.py` — "
        "run manually: `python scripts/crew.py`*",
    ]

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="CheatCodes Review Crew — library health, gap, and quality report"
    )
    parser.add_argument("--output", "-o", help="Write report to this file path")
    parser.add_argument(
        "--agent",
        choices=["librarian", "scout", "coach", "all"],
        default="all",
        help="Run only one agent (default: all)",
    )
    args = parser.parse_args()

    if not SKILLS_DIR.exists():
        print("ERROR: skills/ directory not found. Run from the repo root.", file=sys.stderr)
        sys.exit(1)

    skills = _get_all_skills()

    if not skills:
        print("No skills found in skills/. Nothing to review.")
        sys.exit(0)

    if args.agent == "librarian":
        result = librarian_run(skills)
        for s in result["per_skill"]:
            print(f"\n## {s['path']}")
            for level in ("critical", "warning", "note"):
                for item in s["findings"][level]:
                    print(f"  [{level.upper()}] {item}")
        return

    if args.agent == "scout":
        result = scout_run(skills)
        print(f"Missing categories: {result['missing_categories']}")
        print(f"\nAdoption candidates ({len(result['adoption_candidates'])}):")
        for c in result["adoption_candidates"]:
            print(f"  - [{c['category']}] {c['name']}: {c['tagline']}")
        return

    if args.agent == "coach":
        result = coach_run(skills)
        for s in result["per_skill"]:
            if s["suggestions"]:
                print(f"\n## {s['path']}")
                for tip in s["suggestions"]:
                    print(f"  - {tip}")
        return

    # Full crew run
    lib_findings   = librarian_run(skills)
    scout_findings = scout_run(skills)
    coach_findings = coach_run(skills)

    report = coordinator_assemble(skills, lib_findings, scout_findings, coach_findings)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report)
        print(f"Crew report written to: {out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
