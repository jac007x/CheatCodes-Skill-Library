#!/usr/bin/env python3
"""
Skill Compliance Validation Checker

Validates that a skill meets Walmart AI compliance requirements before
submission to the CheatCodes Skill Library.

Usage:
    python validate_skill.py skills/your-skill/
    python validate_skill.py --all
    python validate_skill.py --help

Checks:
    - Required files exist (skill.yaml, README.md)
    - Compliance section in README
    - Model recommendation specified
    - PII handling documented (if applicable)
    - No hardcoded secrets
    - Uses approved AI services only
    - Risk level documented
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional

# Try to import yaml, fall back to basic parsing if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# ANSI colors for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Patterns to detect potential secrets
SECRET_PATTERNS = [
    r'api[_-]?key\s*[=:]\s*["\'][^"\']+["\']',
    r'password\s*[=:]\s*["\'][^"\']+["\']',
    r'secret\s*[=:]\s*["\'][^"\']+["\']',
    r'token\s*[=:]\s*["\'][^"\']+["\']',
    r'ghp_[a-zA-Z0-9]{36}',  # GitHub PAT
    r'sk-[a-zA-Z0-9]{48}',   # OpenAI key
    r'xox[baprs]-[a-zA-Z0-9-]+',  # Slack token
]

# Approved AI services
APPROVED_SERVICES = [
    'wibey', 'claude', 'anthropic',
    'azure openai', 'azure-openai',
    'vertex', 'google vertex', 'palm',
    'walmart llm gateway', 'llm gateway',
    'msgraph', 'confluence', 'jira',  # Internal agents
]

# Model tiers
MODEL_TIERS = ['haiku', 'sonnet', 'opus']


class ValidationResult:
    def __init__(self, name: str, passed: bool, message: str, severity: str = "error"):
        self.name = name
        self.passed = passed
        self.message = message
        self.severity = severity  # error, warning, info


def print_result(result: ValidationResult):
    """Print a single validation result."""
    if result.passed:
        icon = f"{GREEN}✅{RESET}"
        status = "PASS"
    elif result.severity == "warning":
        icon = f"{YELLOW}⚠️{RESET}"
        status = "WARN"
    else:
        icon = f"{RED}❌{RESET}"
        status = "FAIL"

    print(f"{icon} {status}: {result.message}")


def check_file_exists(skill_path: Path, filename: str) -> ValidationResult:
    """Check if a required file exists."""
    file_path = skill_path / filename
    exists = file_path.exists()
    return ValidationResult(
        name=f"file_{filename}",
        passed=exists,
        message=f"{filename} {'exists' if exists else 'MISSING'}"
    )


def check_compliance_section(skill_path: Path) -> ValidationResult:
    """Check if README has a compliance section."""
    readme_path = skill_path / "README.md"
    if not readme_path.exists():
        return ValidationResult(
            name="compliance_section",
            passed=False,
            message="Cannot check compliance - README.md missing"
        )

    content = readme_path.read_text().lower()
    has_compliance = "## compliance" in content or "### compliance" in content

    return ValidationResult(
        name="compliance_section",
        passed=has_compliance,
        message=f"Compliance section {'found' if has_compliance else 'MISSING in README'}"
    )


def check_model_recommendation(skill_path: Path) -> ValidationResult:
    """Check if skill has a model recommendation."""
    # Check skill.yaml first
    yaml_path = skill_path / "skill.yaml"
    readme_path = skill_path / "README.md"

    model_found = None

    if yaml_path.exists() and HAS_YAML:
        try:
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
                if data and 'model_recommendation' in data:
                    model_found = data['model_recommendation']
        except:
            pass

    # Also check via text search in skill.yaml
    if not model_found and yaml_path.exists():
        content = yaml_path.read_text().lower()
        for tier in MODEL_TIERS:
            if f"model_recommendation: {tier}" in content:
                model_found = tier
                break

    if not model_found and readme_path.exists():
        content = readme_path.read_text().lower()
        for tier in MODEL_TIERS:
            if f"model" in content and tier in content:
                model_found = tier
                break

    if model_found:
        return ValidationResult(
            name="model_recommendation",
            passed=True,
            message=f"Model recommendation: {model_found.title()}"
        )

    return ValidationResult(
        name="model_recommendation",
        passed=False,
        message="Model recommendation MISSING - add to skill.yaml or README"
    )


def check_pii_handling(skill_path: Path) -> ValidationResult:
    """Check if PII handling is documented when needed."""
    readme_path = skill_path / "README.md"
    yaml_path = skill_path / "skill.yaml"

    if not readme_path.exists():
        return ValidationResult(
            name="pii_handling",
            passed=False,
            message="Cannot check PII - README.md missing"
        )

    readme_content = readme_path.read_text().lower()

    # Check if skill might handle PII
    pii_indicators = ['pii', 'employee', 'hr data', 'personal', 'email', 'calendar', 'name', 'roster']
    might_have_pii = any(indicator in readme_content for indicator in pii_indicators)

    # Check if PII handling is documented
    pii_documented = 'pii' in readme_content and ('control' in readme_content or 'handling' in readme_content)

    if not might_have_pii:
        return ValidationResult(
            name="pii_handling",
            passed=True,
            message="PII handling: Not applicable (no PII indicators found)",
            severity="info"
        )

    if pii_documented:
        return ValidationResult(
            name="pii_handling",
            passed=True,
            message="PII handling documented"
        )

    return ValidationResult(
        name="pii_handling",
        passed=False,
        message="PII handling MISSING - skill may process PII but controls not documented",
        severity="warning"
    )


def check_no_secrets(skill_path: Path) -> ValidationResult:
    """Check for hardcoded secrets in skill files."""
    secrets_found = []

    for file_path in skill_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.py', '.yaml', '.yml', '.json', '.md', '.txt']:
            try:
                content = file_path.read_text()
                for pattern in SECRET_PATTERNS:
                    if re.search(pattern, content, re.IGNORECASE):
                        secrets_found.append(file_path.name)
                        break
            except:
                pass

    if secrets_found:
        return ValidationResult(
            name="no_secrets",
            passed=False,
            message=f"Potential secrets in: {', '.join(set(secrets_found))}"
        )

    return ValidationResult(
        name="no_secrets",
        passed=True,
        message="No secrets detected"
    )


def check_approved_services(skill_path: Path) -> ValidationResult:
    """Check that only approved AI services are used."""
    yaml_path = skill_path / "skill.yaml"
    readme_path = skill_path / "README.md"

    # Combine content from both files
    content = ""
    if yaml_path.exists():
        content += yaml_path.read_text().lower()
    if readme_path.exists():
        content += readme_path.read_text().lower()

    # Look for unapproved services
    unapproved_patterns = [
        r'openai\.com',
        r'api\.openai',
        r'chatgpt',
        r'gpt-4(?!.*azure)',
        r'gpt-3\.5(?!.*azure)',
    ]

    unapproved_found = []
    for pattern in unapproved_patterns:
        if re.search(pattern, content):
            unapproved_found.append(pattern)

    if unapproved_found:
        return ValidationResult(
            name="approved_services",
            passed=False,
            message=f"Unapproved AI services detected - use Walmart-approved services only"
        )

    # Check if any approved service is mentioned
    approved_found = any(service in content for service in APPROVED_SERVICES)

    if approved_found:
        return ValidationResult(
            name="approved_services",
            passed=True,
            message="Uses approved AI services"
        )

    return ValidationResult(
        name="approved_services",
        passed=True,
        message="No external AI services detected",
        severity="info"
    )


def check_risk_level(skill_path: Path) -> ValidationResult:
    """Check if risk level is documented."""
    readme_path = skill_path / "README.md"
    yaml_path = skill_path / "skill.yaml"

    risk_found = None

    # Check README
    if readme_path.exists():
        content = readme_path.read_text().lower()
        if "risk level" in content or "risk_level" in content:
            if "low" in content:
                risk_found = "Low"
            elif "medium" in content:
                risk_found = "Medium"
            elif "high" in content:
                risk_found = "High"

    # Check skill.yaml via text search
    if not risk_found and yaml_path.exists():
        content = yaml_path.read_text().lower()
        if "risk_level:" in content:
            if "low" in content:
                risk_found = "Low"
            elif "medium" in content:
                risk_found = "Medium"
            elif "high" in content:
                risk_found = "High"

    # Check skill.yaml via yaml parsing
    if not risk_found and yaml_path.exists() and HAS_YAML:
        try:
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
                if data and 'risk_level' in data:
                    risk_found = data['risk_level']
        except:
            pass

    if risk_found:
        return ValidationResult(
            name="risk_level",
            passed=True,
            message=f"Risk level: {risk_found}"
        )

    return ValidationResult(
        name="risk_level",
        passed=False,
        message="Risk level MISSING - add Low/Medium/High assessment",
        severity="warning"
    )


def validate_skill(skill_path: Path) -> Tuple[bool, List[ValidationResult]]:
    """Run all validation checks on a skill."""
    results = []

    # Required file checks
    results.append(check_file_exists(skill_path, "skill.yaml"))
    results.append(check_file_exists(skill_path, "README.md"))

    # Content checks
    results.append(check_compliance_section(skill_path))
    results.append(check_model_recommendation(skill_path))
    results.append(check_pii_handling(skill_path))
    results.append(check_no_secrets(skill_path))
    results.append(check_approved_services(skill_path))
    results.append(check_risk_level(skill_path))

    # Determine overall pass/fail
    errors = [r for r in results if not r.passed and r.severity == "error"]
    warnings = [r for r in results if not r.passed and r.severity == "warning"]

    # Fail if any errors, warn if any warnings
    passed = len(errors) == 0

    return passed, results


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{BOLD}{'═' * 50}{RESET}")
    print(f"{BOLD}  {text}{RESET}")
    print(f"{BOLD}{'═' * 50}{RESET}\n")


def print_footer(passed: bool):
    """Print the final result footer."""
    print(f"\n{'═' * 50}")
    if passed:
        print(f"  {GREEN}{BOLD}VALIDATION RESULT: ✅ COMPLIANT{RESET}")
        print(f"  Ready for submission to library")
    else:
        print(f"  {RED}{BOLD}VALIDATION RESULT: ❌ NOT COMPLIANT{RESET}")
        print(f"  Fix issues above before submission")
    print(f"{'═' * 50}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Validate skill compliance for CheatCodes Skill Library"
    )
    parser.add_argument(
        "skill_path",
        nargs="?",
        help="Path to skill directory (e.g., skills/my-skill/)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all skills in the skills/ directory"
    )

    args = parser.parse_args()

    if not args.skill_path and not args.all:
        parser.print_help()
        sys.exit(1)

    # Find skills directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    skills_dir = repo_root / "skills"

    if args.all:
        # Validate all skills
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        all_passed = True

        print_header("Validating All Skills")

        for skill_dir in sorted(skill_dirs):
            print(f"\n{BOLD}▶ {skill_dir.name}{RESET}")
            passed, results = validate_skill(skill_dir)

            for result in results:
                print_result(result)

            if not passed:
                all_passed = False

            print(f"  → {'✅ Compliant' if passed else '❌ Issues found'}")

        print_footer(all_passed)
        sys.exit(0 if all_passed else 1)

    else:
        # Validate single skill
        skill_path = Path(args.skill_path)

        if not skill_path.exists():
            print(f"{RED}Error: Skill path does not exist: {skill_path}{RESET}")
            sys.exit(1)

        print_header(f"Validating: {skill_path.name}")

        passed, results = validate_skill(skill_path)

        for result in results:
            print_result(result)

        print_footer(passed)
        sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
