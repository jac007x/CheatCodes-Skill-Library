#!/usr/bin/env python3
"""
validate_skills.py — Validate CheatCodes skill manifests and directory structure.

Usage:
    python scripts/validate_skills.py               # validate all skills
    python scripts/validate_skills.py --changed-only  # validate only changed skills (CI)
    python scripts/validate_skills.py --summary       # machine-readable summary
    python scripts/validate_skills.py skills/productivity/task-planner  # single skill
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Run: pip install pyyaml")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

REQUIRED_MANIFEST_FIELDS = [
    "name",
    "display_name",
    "version",
    "status",
    "category",
    "description",
    "author",
    "created",
    "updated",
    "changelog",
]

VALID_STATUSES = {"beta", "stable", "deprecated", "archived"}
VALID_CATEGORIES = {
    "productivity",
    "automation",
    "communication",
    "data",
    "hr-analytics",
    "devops",
    "security",
    "custom",
}


def get_changed_skill_dirs() -> list[Path]:
    """Return skill directories that have changed files in the current PR/commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT,
        )
        changed = result.stdout.splitlines()
    except subprocess.CalledProcessError:
        # Fall back to all skills if git diff fails
        return get_all_skill_dirs()

    skill_dirs: set[Path] = set()
    for changed_file in changed:
        parts = Path(changed_file).parts
        # skills/<category>/<skill-name>/...
        if len(parts) >= 3 and parts[0] == "skills":
            skill_dirs.add(REPO_ROOT / "skills" / parts[1] / parts[2])
    return list(skill_dirs)


def get_all_skill_dirs() -> list[Path]:
    """Return all skill directories (those containing a skill.yaml)."""
    return [p.parent for p in SKILLS_DIR.rglob("skill.yaml")]


def validate_skill(skill_dir: Path) -> list[str]:
    """
    Validate a single skill directory.
    Returns a list of error strings (empty = valid).
    """
    errors: list[str] = []
    manifest_path = skill_dir / "skill.yaml"

    # 1. skill.yaml must exist
    if not manifest_path.exists():
        errors.append(f"Missing skill.yaml in {skill_dir.relative_to(REPO_ROOT)}")
        return errors

    # 2. Parse YAML
    try:
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        errors.append(f"Invalid YAML in {manifest_path.relative_to(REPO_ROOT)}: {exc}")
        return errors

    if not isinstance(manifest, dict):
        errors.append(
            f"skill.yaml must be a YAML mapping in {manifest_path.relative_to(REPO_ROOT)}"
        )
        return errors

    # 3. Required fields
    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in manifest or not manifest[field]:
            errors.append(
                f"{manifest_path.relative_to(REPO_ROOT)}: missing required field '{field}'"
            )

    # 4. Status must be valid
    status = manifest.get("status", "")
    if status and status not in VALID_STATUSES:
        errors.append(
            f"{manifest_path.relative_to(REPO_ROOT)}: invalid status '{status}'. "
            f"Must be one of: {', '.join(sorted(VALID_STATUSES))}"
        )

    # 5. Category must be valid
    category = manifest.get("category", "")
    if category and category not in VALID_CATEGORIES:
        errors.append(
            f"{manifest_path.relative_to(REPO_ROOT)}: invalid category '{category}'. "
            f"Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
        )

    # 6. README.md must exist
    readme_path = skill_dir / "README.md"
    if not readme_path.exists():
        errors.append(
            f"Missing README.md in {skill_dir.relative_to(REPO_ROOT)}"
        )

    # 7. At least one versioned directory with a prompt.md must exist
    version_dirs = [
        d
        for d in skill_dir.iterdir()
        if d.is_dir() and (d.name.startswith("v") or "beta" in d.name)
    ]
    if not version_dirs:
        errors.append(
            f"No versioned directories (e.g., v1/, v2-beta/) found in "
            f"{skill_dir.relative_to(REPO_ROOT)}"
        )
    else:
        for vdir in version_dirs:
            prompt_file = vdir / "prompt.md"
            if not prompt_file.exists():
                errors.append(
                    f"Missing prompt.md in {vdir.relative_to(REPO_ROOT)}"
                )

    # 8. Changelog must be a list with at least one entry
    changelog = manifest.get("changelog")
    if changelog is not None:
        if not isinstance(changelog, list) or len(changelog) == 0:
            errors.append(
                f"{manifest_path.relative_to(REPO_ROOT)}: 'changelog' must be a "
                f"non-empty list"
            )

    # 9. Version field should be semver-ish (MAJOR.MINOR.PATCH)
    version = str(manifest.get("version", ""))
    if version:
        parts = version.split(".")
        if len(parts) != 3 or not all(p.split("-")[0].isdigit() for p in parts):
            errors.append(
                f"{manifest_path.relative_to(REPO_ROOT)}: version '{version}' "
                f"does not follow semver (MAJOR.MINOR.PATCH)"
            )

    return errors


def run_validation(
    skill_dirs: list[Path],
    summary_mode: bool = False,
) -> tuple[int, int]:
    """Run validation on a list of skill directories. Returns (errors, skills_checked)."""
    total_errors = 0
    total_skills = 0

    results: list[tuple[Path, list[str]]] = []
    for skill_dir in sorted(skill_dirs):
        if not skill_dir.exists():
            continue
        errs = validate_skill(skill_dir)
        results.append((skill_dir, errs))
        total_errors += len(errs)
        total_skills += 1

    if summary_mode:
        passed = sum(1 for _, e in results if not e)
        failed = sum(1 for _, e in results if e)
        print(f"| Skills checked | {total_skills} |")
        print(f"| ✅ Passed | {passed} |")
        print(f"| ❌ Failed | {failed} |")
        if total_errors:
            print("\n**Errors:**")
            for _, errs in results:
                for err in errs:
                    print(f"- {err}")
    else:
        for skill_dir, errs in results:
            rel = skill_dir.relative_to(REPO_ROOT)
            if errs:
                print(f"❌ {rel}")
                for err in errs:
                    print(f"   → {err}")
            else:
                print(f"✅ {rel}")

    return total_errors, total_skills


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate CheatCodes skill manifests")
    parser.add_argument(
        "skill_path",
        nargs="?",
        help="Path to a specific skill directory to validate",
    )
    parser.add_argument(
        "--changed-only",
        action="store_true",
        help="Only validate skills changed in the last commit (for CI use)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Output in machine-readable summary format",
    )
    args = parser.parse_args()

    if args.skill_path:
        skill_dirs = [Path(args.skill_path)]
    elif args.changed_only:
        skill_dirs = get_changed_skill_dirs()
    else:
        skill_dirs = get_all_skill_dirs()

    if not skill_dirs:
        print("No skills to validate.")
        sys.exit(0)

    errors, skills_checked = run_validation(skill_dirs, summary_mode=args.summary)

    if not args.summary:
        print(f"\n{'─' * 50}")
        print(f"Validated {skills_checked} skill(s). Errors: {errors}")

    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
