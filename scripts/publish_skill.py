#!/usr/bin/env python3
"""
publish_skill.py — Update a skill's manifest for a new version release.

Usage:
    python scripts/publish_skill.py \\
        --skill productivity/task-planner \\
        --version 2.0.0 \\
        --status stable \\
        --notes "Promoted from beta\\nFixed edge case in parallel track output"
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Run: pip install pyyaml")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

VALID_STATUSES = {"beta", "stable", "deprecated", "archived"}


def load_manifest(manifest_path: Path) -> dict:
    with open(manifest_path) as f:
        return yaml.safe_load(f) or {}


def validate_semver(version: str) -> bool:
    return bool(re.match(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$", version))


def dump_manifest(manifest: dict, manifest_path: Path) -> None:
    """Write manifest back to YAML, preserving a consistent structure."""
    with open(manifest_path, "w") as f:
        yaml.dump(
            manifest,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish a new skill version")
    parser.add_argument(
        "--skill", required=True, help="Skill path (e.g., productivity/task-planner)"
    )
    parser.add_argument("--version", required=True, help="New version (semver)")
    parser.add_argument(
        "--status",
        required=True,
        choices=sorted(VALID_STATUSES),
        help="New status",
    )
    parser.add_argument(
        "--notes",
        required=True,
        help="Release notes (newline-separated list of changes)",
    )
    args = parser.parse_args()

    # Validate version
    if not validate_semver(args.version):
        print(f"ERROR: version '{args.version}' is not valid semver (MAJOR.MINOR.PATCH)")
        sys.exit(1)

    skill_dir = SKILLS_DIR / args.skill
    manifest_path = skill_dir / "skill.yaml"

    if not manifest_path.exists():
        print(f"ERROR: {manifest_path} not found")
        sys.exit(1)

    manifest = load_manifest(manifest_path)
    today = date.today().strftime("%Y-%m-%d")

    # Update fields
    old_version = manifest.get("version", "unknown")
    manifest["version"] = args.version
    manifest["status"] = args.status
    manifest["updated"] = today

    # Prepend new changelog entry
    changes = [line.strip() for line in args.notes.splitlines() if line.strip()]
    new_entry = {
        "version": args.version,
        "date": today,
        "status": args.status,
        "changes": changes,
    }
    changelog = manifest.get("changelog", [])
    if not isinstance(changelog, list):
        changelog = []
    manifest["changelog"] = [new_entry] + changelog

    dump_manifest(manifest, manifest_path)
    print(
        f"✅ Updated {args.skill}: {old_version} → {args.version} ({args.status})"
    )


if __name__ == "__main__":
    main()
