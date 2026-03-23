#!/usr/bin/env python3
"""
Tiered Quality Gate Validator for the CheatCodes Skill Library.

Implements the governance model defined in GOVERNANCE.md with two tiers:

  HARD gates (H1-H10) — block merge, exit code 1 on failure
  SOFT gates (S1-S8)  — produce warnings, exit code 0

Usage:
    python validate_skill.py <skill-path>           # validate one skill
    python validate_skill.py --all                   # validate every skill at repo root
    python validate_skill.py --hard-only             # only run hard gates (fast, for pre-commit)
    python validate_skill.py --registry-sync         # bidirectional registry.json sync check
    python validate_skill.py --all --hard-only       # combine flags
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Optional YAML import — fall back to regex-based front-matter parsing
# ---------------------------------------------------------------------------
try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# ---------------------------------------------------------------------------
# ANSI colour helpers
# ---------------------------------------------------------------------------
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CYAN = "\033[96m"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REPO_ROOT: Path = Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {"templates", "tools", "docs", ".github", "skills", ".git", "__pycache__", "node_modules"}

REQUIRED_YAML_FIELDS = {"name", "version", "description", "origin", "author", "maturity_status", "tags"}

VALID_ORIGINS = {"created", "curated", "forked", "contributed"}

ORIGIN_REQUIRED_FIELDS: Dict[str, List[str]] = {
    "curated": ["source_url", "curator"],
    "forked": ["forked_from", "fork_author"],
    "contributed": ["contributor"],
}

SCANNABLE_EXTENSIONS = {
    ".py", ".yaml", ".yml", ".json", ".md", ".txt", ".toml", ".cfg",
    ".ini", ".env", ".sh", ".bash", ".zsh", ".js", ".ts", ".html",
    ".xml", ".csv", ".rst", ".adoc",
}

# H2 — secret patterns (expanded from original)
SECRET_PATTERNS: List[re.Pattern[str]] = [
    re.compile(r'api[_-]?key\s*[=:]\s*["\'][^"\']{8,}["\']', re.IGNORECASE),
    re.compile(r'password\s*[=:]\s*["\'][^"\']{4,}["\']', re.IGNORECASE),
    re.compile(r'secret\s*[=:]\s*["\'][^"\']{8,}["\']', re.IGNORECASE),
    re.compile(r'token\s*[=:]\s*["\'][^"\']{8,}["\']', re.IGNORECASE),
    re.compile(r'ghp_[a-zA-Z0-9]{36,}'),                         # GitHub PAT
    re.compile(r'github_pat_[a-zA-Z0-9_]{20,}'),                  # GitHub fine-grained PAT
    re.compile(r'gho_[a-zA-Z0-9]{36,}'),                          # GitHub OAuth
    re.compile(r'ghu_[a-zA-Z0-9]{36,}'),                          # GitHub user-to-server
    re.compile(r'ghs_[a-zA-Z0-9]{36,}'),                          # GitHub server-to-server
    re.compile(r'sk-[a-zA-Z0-9]{20,}'),                           # OpenAI key
    re.compile(r'sk-proj-[a-zA-Z0-9_-]{20,}'),                    # OpenAI project key
    re.compile(r'xox[baprs]-[a-zA-Z0-9\-]{10,}'),                 # Slack tokens
    re.compile(r'AKIA[0-9A-Z]{16}'),                              # AWS access key
    re.compile(r'eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}'),    # JWT tokens
    re.compile(r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----'),    # Private keys
    re.compile(r'connection[_-]?string\s*[=:]\s*["\'][^"\']{15,}["\']', re.IGNORECASE),
]

# H1 — PII patterns
PII_EMAIL_PATTERN = re.compile(
    r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
)
PII_SAFE_EMAIL_DOMAINS = {
    "example.com", "example.org", "example.net",
    "test.com", "test.org", "placeholder.com",
    "domain.com", "company.com", "yourcompany.com",
    "yourdomain.com", "email.com", "mail.com",
}
PII_NAME_PATTERN = re.compile(
    r'\b[A-Z][a-z]{2,15}\.[A-Z][a-z]{2,20}\b',         # Firstname.Lastname
)
PII_EMPLOYEE_ID_PATTERNS: List[re.Pattern[str]] = [
    re.compile(r'\b[Ee]mployee[_\s]?[Ii][Dd]\s*[:=]\s*\w+'),
    re.compile(r'\bWIN\d{6,}\b'),                         # typical WIN IDs
    re.compile(r'\b[Bb]adge\s*#?\s*\d{5,}\b'),
]

# H3 — internal URL patterns
# We match URLs/domains, NOT plain-text attribution like "Built at Walmart".
INTERNAL_URL_PATTERNS: List[re.Pattern[str]] = [
    re.compile(r'https?://[a-zA-Z0-9._-]*\.walmart\.com\b', re.IGNORECASE),
    re.compile(r'https?://[a-zA-Z0-9._-]*\.wal-mart\.com\b', re.IGNORECASE),
    re.compile(r'https?://[a-zA-Z0-9._-]*\.walmart\.net\b', re.IGNORECASE),
    re.compile(r'https?://[a-zA-Z0-9._-]*\.service-now\.com/[^\s]*walmart', re.IGNORECASE),
    # Bare domain references (without http) that look like hostnames
    re.compile(r'\b[a-zA-Z0-9._-]+\.walmart\.com\b', re.IGNORECASE),
    re.compile(r'\b[a-zA-Z0-9._-]+\.wal-mart\.com\b', re.IGNORECASE),
    re.compile(r'\b[a-zA-Z0-9._-]+\.walmart\.net\b', re.IGNORECASE),
]

# H10 — pre-universalized content indicators
PRE_UNIVERSALIZED_PATTERNS: List[re.Pattern[str]] = [
    re.compile(r'\bskills/[a-zA-Z0-9_-]+/', re.IGNORECASE),   # skills/ subdirectory refs
    re.compile(r'team[_-]?specific', re.IGNORECASE),
    re.compile(r'internal[_-]?only', re.IGNORECASE),
]

# S8 — PII keyword indicators (to decide if PII handling docs are expected)
PII_KEYWORD_INDICATORS = [
    "pii", "employee", "hr data", "personal data", "email address",
    "calendar", "name", "roster", "badge", "ssn", "social security",
    "phone number", "salary", "compensation", "health",
]


# =========================================================================
# Data classes
# =========================================================================
class GateResult:
    """Outcome of a single quality gate check."""

    __slots__ = ("gate_id", "name", "passed", "message", "details", "tier")

    def __init__(
        self,
        gate_id: str,
        name: str,
        passed: bool,
        message: str,
        tier: str = "hard",
        details: Optional[List[str]] = None,
    ) -> None:
        self.gate_id = gate_id
        self.name = name
        self.passed = passed
        self.message = message
        self.tier = tier  # "hard" | "soft"
        self.details = details or []

    @property
    def is_hard(self) -> bool:
        return self.tier == "hard"


# =========================================================================
# Helpers
# =========================================================================
def _read_text_safe(path: Path) -> Optional[str]:
    """Read a file to string, returning None on any error."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return None


def _parse_yaml_front_matter(text: str) -> Optional[Dict[str, Any]]:
    """Extract YAML front matter delimited by --- ... --- from markdown."""
    match = re.match(r"^---\s*\n(.*?\n)---", text, re.DOTALL)
    if not match:
        return None
    raw = match.group(1)
    if HAS_YAML:
        try:
            return yaml.safe_load(raw) or {}
        except yaml.YAMLError:
            return None
    # Minimal fallback parser for flat key: value pairs
    data: Dict[str, Any] = {}
    for line in raw.splitlines():
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.+)', line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"').strip("'")
            data[key] = val
    return data


def _load_yaml_file(path: Path) -> Optional[Dict[str, Any]]:
    """Load a YAML file, returning None on failure."""
    text = _read_text_safe(path)
    if text is None:
        return None
    if HAS_YAML:
        try:
            return yaml.safe_load(text) or {}
        except yaml.YAMLError:
            return None
    # Minimal fallback
    data: Dict[str, Any] = {}
    for line in text.splitlines():
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.+)', line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"').strip("'")
            data[key] = val
    return data


def _load_skill_metadata(skill_path: Path) -> Tuple[Optional[Dict[str, Any]], str]:
    """Load skill metadata from skill.yaml or SKILL.md front matter.

    Returns (metadata_dict, source_description).
    """
    # Prefer standalone skill.yaml
    yaml_path = skill_path / "skill.yaml"
    if yaml_path.exists():
        data = _load_yaml_file(yaml_path)
        if data is not None:
            return data, "skill.yaml"

    # Fall back to SKILL.md YAML front matter
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        text = _read_text_safe(skill_md)
        if text is not None:
            data = _parse_yaml_front_matter(text)
            if data is not None:
                return data, "SKILL.md front matter"

    return None, "none"


def _load_registry(repo_root: Path) -> Optional[Dict[str, Any]]:
    """Load registry.json from repo root."""
    reg_path = repo_root / "registry.json"
    if not reg_path.exists():
        return None
    try:
        return json.loads(reg_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _get_registry_ids(registry: Dict[str, Any]) -> set[str]:
    """Return the set of skill id values from registry.json."""
    skills = registry.get("skills", [])
    return {s["id"] for s in skills if isinstance(s, dict) and "id" in s}


def _scannable_files(skill_path: Path) -> List[Path]:
    """Return all scannable text files in the skill directory tree."""
    files: List[Path] = []
    for fp in skill_path.rglob("*"):
        if fp.is_file() and fp.suffix.lower() in SCANNABLE_EXTENSIONS:
            files.append(fp)
    return files


def _discover_skill_dirs(repo_root: Path) -> List[Path]:
    """Find all root-level directories that contain SKILL.md."""
    dirs: List[Path] = []
    for entry in sorted(repo_root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        if entry.name.lower() in EXCLUDED_DIRS:
            continue
        skill_md = entry / "SKILL.md"
        if skill_md.exists():
            dirs.append(entry)
    return dirs


# =========================================================================
# HARD gate implementations (H1-H10)
# =========================================================================
def h1_no_pii(skill_path: Path) -> GateResult:
    """H1: Scan for PII — emails (non-example), Firstname.Lastname, employee IDs."""
    violations: List[str] = []
    for fp in _scannable_files(skill_path):
        text = _read_text_safe(fp)
        if text is None:
            continue
        rel = fp.relative_to(skill_path)

        # Emails
        for m in PII_EMAIL_PATTERN.finditer(text):
            email = m.group(0)
            domain = email.split("@", 1)[1].lower()
            if domain not in PII_SAFE_EMAIL_DOMAINS:
                violations.append(f"  {rel}: email '{email}'")

        # Firstname.Lastname patterns
        for m in PII_NAME_PATTERN.finditer(text):
            name = m.group(0)
            # Skip common false positives (class names, module refs, file exts)
            if "." in name:
                left, right = name.split(".", 1)
                # Allow things like Path.resolve, Type.Hint, etc.
                fp_text_lower = name.lower()
                if fp_text_lower in {
                    "skill.md", "skill.yaml", "readme.md", "registry.json",
                }:
                    continue
            violations.append(f"  {rel}: name pattern '{name}'")

        # Employee IDs
        for pat in PII_EMPLOYEE_ID_PATTERNS:
            for m in pat.finditer(text):
                violations.append(f"  {rel}: employee ID pattern '{m.group(0)}'")

    if violations:
        return GateResult(
            gate_id="H1",
            name="No PII",
            passed=False,
            message="PII detected in skill files",
            tier="hard",
            details=violations[:20],  # cap detail output
        )
    return GateResult("H1", "No PII", True, "No PII detected", "hard")


def h2_no_secrets(skill_path: Path) -> GateResult:
    """H2: Regex scan for API keys, tokens, passwords, PATs, etc."""
    violations: List[str] = []
    for fp in _scannable_files(skill_path):
        text = _read_text_safe(fp)
        if text is None:
            continue
        rel = fp.relative_to(skill_path)
        for pat in SECRET_PATTERNS:
            for m in pat.finditer(text):
                snippet = m.group(0)[:60]
                violations.append(f"  {rel}: '{snippet}...'")
    if violations:
        return GateResult(
            gate_id="H2",
            name="No Secrets",
            passed=False,
            message="Potential secrets detected",
            tier="hard",
            details=violations[:20],
        )
    return GateResult("H2", "No Secrets", True, "No secrets detected", "hard")


def h3_no_internal_urls(skill_path: Path) -> GateResult:
    """H3: Scan for internal/intranet URLs. Plain 'Walmart' text for attribution is OK."""
    violations: List[str] = []
    for fp in _scannable_files(skill_path):
        text = _read_text_safe(fp)
        if text is None:
            continue
        rel = fp.relative_to(skill_path)
        for pat in INTERNAL_URL_PATTERNS:
            for m in pat.finditer(text):
                url = m.group(0)
                violations.append(f"  {rel}: '{url}'")
    if violations:
        return GateResult(
            gate_id="H3",
            name="No Internal URLs",
            passed=False,
            message="Internal/intranet URLs detected",
            tier="hard",
            details=violations[:20],
        )
    return GateResult("H3", "No Internal URLs", True, "No internal URLs detected", "hard")


def h4_skill_md_exists(skill_path: Path) -> GateResult:
    """H4: SKILL.md must exist."""
    exists = (skill_path / "SKILL.md").exists()
    return GateResult(
        gate_id="H4",
        name="SKILL.md Exists",
        passed=exists,
        message="SKILL.md exists" if exists else "SKILL.md is MISSING",
        tier="hard",
    )


def h5_skill_yaml_exists(skill_path: Path) -> GateResult:
    """H5: skill.yaml must exist (standalone file or YAML front matter in SKILL.md)."""
    yaml_path = skill_path / "skill.yaml"
    if yaml_path.exists():
        return GateResult("H5", "skill.yaml Exists", True, "skill.yaml exists (standalone file)", "hard")

    # Check SKILL.md front matter as alternative
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        text = _read_text_safe(skill_md)
        if text and text.strip().startswith("---"):
            fm = _parse_yaml_front_matter(text)
            if fm is not None and len(fm) > 0:
                return GateResult(
                    "H5",
                    "skill.yaml Exists",
                    True,
                    "Skill metadata found in SKILL.md YAML front matter",
                    "hard",
                )

    return GateResult(
        "H5",
        "skill.yaml Exists",
        False,
        "No skill.yaml file and no YAML front matter in SKILL.md",
        "hard",
    )


def h6_yaml_schema_valid(skill_path: Path) -> GateResult:
    """H6: skill.yaml (or front matter) has all required fields."""
    meta, source = _load_skill_metadata(skill_path)
    if meta is None:
        return GateResult(
            "H6",
            "skill.yaml Schema Valid",
            False,
            "Cannot validate schema — metadata not loadable",
            "hard",
        )
    missing = REQUIRED_YAML_FIELDS - set(meta.keys())
    if missing:
        return GateResult(
            "H6",
            "skill.yaml Schema Valid",
            False,
            f"Missing required fields in {source}: {', '.join(sorted(missing))}",
            "hard",
            details=[f"  Required: {', '.join(sorted(REQUIRED_YAML_FIELDS))}"],
        )
    return GateResult(
        "H6",
        "skill.yaml Schema Valid",
        True,
        f"All required fields present in {source}",
        "hard",
    )


def h7_registered_in_registry(skill_path: Path, registry: Optional[Dict[str, Any]]) -> GateResult:
    """H7: Skill directory name must match an id in registry.json."""
    if registry is None:
        return GateResult(
            "H7",
            "Registered in registry.json",
            False,
            "registry.json not found or not loadable",
            "hard",
        )
    skill_name = skill_path.name
    ids = _get_registry_ids(registry)
    if skill_name in ids:
        return GateResult(
            "H7",
            "Registered in registry.json",
            True,
            f"'{skill_name}' found in registry.json",
            "hard",
        )
    return GateResult(
        "H7",
        "Registered in registry.json",
        False,
        f"'{skill_name}' has no entry in registry.json (no matching id)",
        "hard",
    )


def h8_origin_valid(skill_path: Path) -> GateResult:
    """H8: origin field must be one of the allowed values."""
    meta, source = _load_skill_metadata(skill_path)
    if meta is None:
        return GateResult("H8", "Origin Declared", False, "Metadata not loadable", "hard")
    origin = meta.get("origin")
    if origin is None:
        return GateResult("H8", "Origin Declared", False, "origin field missing from metadata", "hard")
    origin_str = str(origin).strip().lower()
    if origin_str in VALID_ORIGINS:
        return GateResult("H8", "Origin Declared", True, f"origin: {origin_str}", "hard")
    return GateResult(
        "H8",
        "Origin Declared",
        False,
        f"origin '{origin}' is invalid — must be one of: {', '.join(sorted(VALID_ORIGINS))}",
        "hard",
    )


def h9_attribution_present(skill_path: Path) -> GateResult:
    """H9: Based on origin type, required attribution fields must be present."""
    meta, source = _load_skill_metadata(skill_path)
    if meta is None:
        return GateResult("H9", "Attribution Present", False, "Metadata not loadable", "hard")
    origin = str(meta.get("origin", "")).strip().lower()
    if origin not in ORIGIN_REQUIRED_FIELDS:
        # 'created' has no additional attribution requirements
        return GateResult(
            "H9",
            "Attribution Present",
            True,
            f"origin '{origin}' requires no additional attribution fields",
            "hard",
        )
    required = ORIGIN_REQUIRED_FIELDS[origin]
    missing = [f for f in required if f not in meta or not meta[f]]
    if missing:
        return GateResult(
            "H9",
            "Attribution Present",
            False,
            f"origin '{origin}' requires: {', '.join(required)} — missing: {', '.join(missing)}",
            "hard",
        )
    return GateResult(
        "H9",
        "Attribution Present",
        True,
        f"All attribution fields present for origin '{origin}'",
        "hard",
    )


def h10_no_pre_universalized(skill_path: Path) -> GateResult:
    """H10: No pre-universalized content (skills/ subdirectory refs, team-specific markers)."""
    violations: List[str] = []

    # Check for a skills/ subdirectory inside the skill directory itself
    skills_subdir = skill_path / "skills"
    if skills_subdir.is_dir():
        violations.append("  Contains a 'skills/' subdirectory (pre-universalized structure)")

    for fp in _scannable_files(skill_path):
        text = _read_text_safe(fp)
        if text is None:
            continue
        rel = fp.relative_to(skill_path)
        for pat in PRE_UNIVERSALIZED_PATTERNS:
            for m in pat.finditer(text):
                violations.append(f"  {rel}: '{m.group(0)}'")

    if violations:
        return GateResult(
            "H10",
            "No Pre-Universalized Content",
            False,
            "Pre-universalized content detected",
            "hard",
            details=violations[:20],
        )
    return GateResult("H10", "No Pre-Universalized Content", True, "No pre-universalized content", "hard")


# =========================================================================
# SOFT gate implementations (S1-S8)
# =========================================================================
def _read_skill_md(skill_path: Path) -> Optional[str]:
    """Helper: read SKILL.md content."""
    return _read_text_safe(skill_path / "SKILL.md")


def s1_compliance_section(skill_path: Path) -> GateResult:
    """S1: SKILL.md should have a compliance/governance section."""
    text = _read_skill_md(skill_path)
    if text is None:
        return GateResult("S1", "Compliance Section", False, "SKILL.md not readable", "soft")
    lower = text.lower()
    found = any(
        marker in lower
        for marker in ["## compliance", "### compliance", "## governance", "### governance"]
    )
    return GateResult(
        "S1",
        "Compliance Section",
        found,
        "Compliance section found in SKILL.md" if found else "No compliance/governance section in SKILL.md",
        "soft",
    )


def s2_example_applications(skill_path: Path) -> GateResult:
    """S2: At least 4 example applications listed."""
    text = _read_skill_md(skill_path)
    if text is None:
        return GateResult("S2", ">=4 Example Applications", False, "SKILL.md not readable", "soft")
    lower = text.lower()

    # Look for a section header mentioning examples/applications
    example_section = re.search(
        r'#{1,3}\s*(?:example|sample|use[- ]?case|application)s?.*?\n(.*?)(?=\n#{1,3}\s|\Z)',
        lower,
        re.DOTALL,
    )
    if not example_section:
        return GateResult(
            "S2", ">=4 Example Applications", False,
            "No example applications section found", "soft",
        )

    section_text = example_section.group(1)
    # Count table rows (| ... |) or list items (- or *)
    row_count = len(re.findall(r'^\s*\|(?!\s*-+\s*\|)', section_text, re.MULTILINE))
    list_count = len(re.findall(r'^\s*[-*]\s+\S', section_text, re.MULTILINE))
    total = max(row_count, list_count)

    if total >= 4:
        return GateResult("S2", ">=4 Example Applications", True, f"{total} example applications found", "soft")
    return GateResult(
        "S2", ">=4 Example Applications", False,
        f"Only {total} example applications found (recommend >=4)", "soft",
    )


def s3_platform_notes(skill_path: Path) -> GateResult:
    """S3: Platform compatibility / notes section exists."""
    text = _read_skill_md(skill_path)
    if text is None:
        return GateResult("S3", "Platform Notes", False, "SKILL.md not readable", "soft")
    lower = text.lower()
    found = any(
        marker in lower
        for marker in ["## platform", "### platform", "## compatibility", "### compatibility"]
    )
    return GateResult(
        "S3", "Platform Notes", found,
        "Platform notes section found" if found else "No platform notes section in SKILL.md",
        "soft",
    )


def s4_intake_variables(skill_path: Path) -> GateResult:
    """S4: Intake variables ({{VARIABLE}}) are documented."""
    text = _read_skill_md(skill_path)
    if text is None:
        return GateResult("S4", "Intake Variables Documented", False, "SKILL.md not readable", "soft")

    variables = re.findall(r'\{\{[A-Z][A-Z0-9_]*\}\}', text)
    if not variables:
        return GateResult(
            "S4", "Intake Variables Documented", True,
            "No intake variables found (may not be needed)", "soft",
        )

    # Check for intake table/section
    lower = text.lower()
    has_intake_section = any(
        marker in lower
        for marker in ["## intake", "### intake", "## variables", "### variables", "## customize", "### customize"]
    )
    unique_vars = sorted(set(variables))
    if has_intake_section:
        return GateResult(
            "S4", "Intake Variables Documented", True,
            f"{len(unique_vars)} intake variable(s) documented: {', '.join(unique_vars[:5])}",
            "soft",
        )
    return GateResult(
        "S4", "Intake Variables Documented", False,
        f"{len(unique_vars)} intake variable(s) found but no intake documentation section",
        "soft",
    )


def s5_anti_patterns(skill_path: Path) -> GateResult:
    """S5: Anti-patterns / pitfalls section exists."""
    text = _read_skill_md(skill_path)
    if text is None:
        return GateResult("S5", "Anti-Patterns Section", False, "SKILL.md not readable", "soft")
    lower = text.lower()
    found = any(
        marker in lower
        for marker in [
            "## anti-pattern", "### anti-pattern",
            "## pitfall", "### pitfall",
            "## common mistake", "### common mistake",
            "## what not to do", "### what not to do",
            "anti-patterns", "## gotcha", "### gotcha",
        ]
    )
    return GateResult(
        "S5", "Anti-Patterns Section", found,
        "Anti-patterns section found" if found else "No anti-patterns section in SKILL.md",
        "soft",
    )


def s6_model_recommendation(skill_path: Path) -> GateResult:
    """S6: Model recommendation in metadata."""
    meta, source = _load_skill_metadata(skill_path)
    if meta and meta.get("model_recommendation"):
        return GateResult(
            "S6", "Model Recommendation", True,
            f"Model recommendation: {meta['model_recommendation']} (from {source})", "soft",
        )
    return GateResult(
        "S6", "Model Recommendation", False,
        "No model_recommendation in skill metadata", "soft",
    )


def s7_risk_level(skill_path: Path) -> GateResult:
    """S7: Risk level in metadata."""
    meta, source = _load_skill_metadata(skill_path)
    if meta and meta.get("risk_level"):
        return GateResult(
            "S7", "Risk Level", True,
            f"Risk level: {meta['risk_level']} (from {source})", "soft",
        )
    return GateResult(
        "S7", "Risk Level", False,
        "No risk_level in skill metadata", "soft",
    )


def s8_pii_handling_documented(skill_path: Path) -> GateResult:
    """S8: If skill may handle PII (based on keyword indicators), PII controls are documented."""
    text = _read_skill_md(skill_path)
    if text is None:
        return GateResult("S8", "PII Handling Documented", True, "SKILL.md not readable (skipped)", "soft")

    lower = text.lower()
    might_have_pii = any(kw in lower for kw in PII_KEYWORD_INDICATORS)
    if not might_have_pii:
        return GateResult(
            "S8", "PII Handling Documented", True,
            "No PII indicators found — check not applicable", "soft",
        )

    pii_documented = "pii" in lower and any(
        w in lower for w in ["control", "handling", "protection", "de-identif", "anonymi", "redact"]
    )
    if pii_documented:
        return GateResult("S8", "PII Handling Documented", True, "PII handling controls documented", "soft")
    return GateResult(
        "S8", "PII Handling Documented", False,
        "Skill may process PII but no PII handling controls documented in SKILL.md", "soft",
    )


# =========================================================================
# Orchestration
# =========================================================================
def run_hard_gates(skill_path: Path, registry: Optional[Dict[str, Any]]) -> List[GateResult]:
    """Run all hard gates (H1-H10) against a skill directory."""
    return [
        h1_no_pii(skill_path),
        h2_no_secrets(skill_path),
        h3_no_internal_urls(skill_path),
        h4_skill_md_exists(skill_path),
        h5_skill_yaml_exists(skill_path),
        h6_yaml_schema_valid(skill_path),
        h7_registered_in_registry(skill_path, registry),
        h8_origin_valid(skill_path),
        h9_attribution_present(skill_path),
        h10_no_pre_universalized(skill_path),
    ]


def run_soft_gates(skill_path: Path) -> List[GateResult]:
    """Run all soft gates (S1-S8) against a skill directory."""
    return [
        s1_compliance_section(skill_path),
        s2_example_applications(skill_path),
        s3_platform_notes(skill_path),
        s4_intake_variables(skill_path),
        s5_anti_patterns(skill_path),
        s6_model_recommendation(skill_path),
        s7_risk_level(skill_path),
        s8_pii_handling_documented(skill_path),
    ]


def validate_skill(
    skill_path: Path,
    registry: Optional[Dict[str, Any]],
    hard_only: bool = False,
) -> Tuple[List[GateResult], List[GateResult]]:
    """Validate a single skill. Returns (hard_results, soft_results)."""
    hard_results = run_hard_gates(skill_path, registry)
    soft_results = run_soft_gates(skill_path) if not hard_only else []
    return hard_results, soft_results


# =========================================================================
# Registry sync check
# =========================================================================
def check_registry_sync(repo_root: Path) -> Tuple[bool, List[str]]:
    """Bidirectional sync: every skill dir <-> registry.json entry.

    Returns (all_ok, messages).
    """
    messages: List[str] = []
    registry = _load_registry(repo_root)
    if registry is None:
        return False, [f"{RED}  registry.json not found or not loadable{RESET}"]

    reg_ids = _get_registry_ids(registry)
    skill_dirs = _discover_skill_dirs(repo_root)
    dir_names = {d.name for d in skill_dirs}

    # Dirs without registry entries
    orphan_dirs = sorted(dir_names - reg_ids)
    for name in orphan_dirs:
        messages.append(f"{RED}  Orphan directory (no registry entry): {name}/{RESET}")

    # Registry entries without dirs
    phantom_ids = sorted(reg_ids - dir_names)
    for rid in phantom_ids:
        messages.append(f"{RED}  Phantom registry entry (no directory): {rid}{RESET}")

    all_ok = len(orphan_dirs) == 0 and len(phantom_ids) == 0
    if all_ok:
        messages.append(f"{GREEN}  All {len(dir_names)} skill(s) in sync with registry.json{RESET}")

    return all_ok, messages


# =========================================================================
# Presentation
# =========================================================================
def _gate_icon(result: GateResult) -> str:
    if result.passed:
        return f"{GREEN}PASS{RESET}"
    if result.is_hard:
        return f"{RED}FAIL{RESET}"
    return f"{YELLOW}WARN{RESET}"


def _gate_symbol(result: GateResult) -> str:
    if result.passed:
        return f"{GREEN}[PASS]{RESET}"
    if result.is_hard:
        return f"{RED}[FAIL]{RESET}"
    return f"{YELLOW}[WARN]{RESET}"


def print_gate(result: GateResult) -> None:
    symbol = _gate_symbol(result)
    print(f"  {symbol} {result.gate_id} {result.name}: {result.message}")
    for detail in result.details:
        print(f"         {DIM}{detail}{RESET}")


def print_skill_header(skill_name: str) -> None:
    width = 60
    print(f"\n{BOLD}{CYAN}{'=' * width}{RESET}")
    print(f"{BOLD}{CYAN}  Validating: {skill_name}{RESET}")
    print(f"{BOLD}{CYAN}{'=' * width}{RESET}")


def print_section(title: str) -> None:
    print(f"\n  {BOLD}{title}{RESET}")
    print(f"  {'-' * 40}")


def print_summary(
    hard_results: List[GateResult],
    soft_results: List[GateResult],
) -> bool:
    """Print a summary and return True if all hard gates passed."""
    hard_passed = sum(1 for r in hard_results if r.passed)
    hard_total = len(hard_results)
    hard_failed = hard_total - hard_passed

    soft_passed = sum(1 for r in soft_results if r.passed)
    soft_total = len(soft_results)
    soft_warnings = soft_total - soft_passed

    all_hard_ok = hard_failed == 0

    print(f"\n  {'=' * 50}")
    # Hard gates line
    if all_hard_ok:
        print(f"  {GREEN}{BOLD}Hard gates:  {hard_passed}/{hard_total} passed{RESET}")
    else:
        print(f"  {RED}{BOLD}Hard gates:  {hard_passed}/{hard_total} passed, {hard_failed} FAILED{RESET}")

    # Soft gates line
    if soft_total > 0:
        if soft_warnings == 0:
            print(f"  {GREEN}{BOLD}Soft gates:  {soft_passed}/{soft_total} passed{RESET}")
        else:
            print(f"  {YELLOW}{BOLD}Soft gates:  {soft_passed}/{soft_total} passed, {soft_warnings} warning(s){RESET}")

    # Verdict
    if all_hard_ok and soft_warnings == 0:
        print(f"\n  {GREEN}{BOLD}RESULT: COMPLIANT — ready for merge{RESET}")
    elif all_hard_ok:
        print(f"\n  {YELLOW}{BOLD}RESULT: COMPLIANT WITH WARNINGS — reviewer must acknowledge{RESET}")
    else:
        print(f"\n  {RED}{BOLD}RESULT: NOT COMPLIANT — fix hard gate failures before merge{RESET}")
    print(f"  {'=' * 50}\n")

    return all_hard_ok


# =========================================================================
# CLI entry point
# =========================================================================
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tiered Quality Gate Validator for the CheatCodes Skill Library",
        epilog="See GOVERNANCE.md for full gate definitions.",
    )
    parser.add_argument(
        "skill_path",
        nargs="?",
        default=None,
        help="Path to a single skill directory to validate",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="validate_all",
        help="Validate all root-level skill directories (auto-discovers via SKILL.md)",
    )
    parser.add_argument(
        "--hard-only",
        action="store_true",
        help="Only run hard gates (H1-H10) — useful for pre-commit hooks",
    )
    parser.add_argument(
        "--registry-sync",
        action="store_true",
        help="Check bidirectional sync between skill directories and registry.json",
    )

    args = parser.parse_args()

    # --registry-sync can run standalone or alongside other modes
    if args.registry_sync:
        print(f"\n{BOLD}{CYAN}Registry Sync Check{RESET}")
        print(f"{CYAN}{'-' * 40}{RESET}")
        ok, msgs = check_registry_sync(REPO_ROOT)
        for msg in msgs:
            print(msg)
        if not ok and not args.validate_all and args.skill_path is None:
            sys.exit(1)
        if not args.validate_all and args.skill_path is None:
            sys.exit(0)

    if not args.validate_all and args.skill_path is None:
        parser.print_help()
        sys.exit(1)

    registry = _load_registry(REPO_ROOT)

    # Collect all skill paths to validate
    if args.validate_all:
        skill_paths = _discover_skill_dirs(REPO_ROOT)
        if not skill_paths:
            print(f"{YELLOW}No skill directories found at repo root.{RESET}")
            sys.exit(0)
    else:
        p = Path(args.skill_path).resolve()
        if not p.is_dir():
            print(f"{RED}Error: '{args.skill_path}' is not a directory.{RESET}")
            sys.exit(1)
        skill_paths = [p]

    # Validate
    overall_pass = True
    total_hard_results: List[GateResult] = []
    total_soft_results: List[GateResult] = []

    for skill_path in skill_paths:
        print_skill_header(skill_path.name)

        hard_results, soft_results = validate_skill(skill_path, registry, hard_only=args.hard_only)

        print_section("Hard Gates (block merge)")
        for r in hard_results:
            print_gate(r)

        if soft_results:
            print_section("Soft Gates (warnings)")
            for r in soft_results:
                print_gate(r)

        skill_ok = print_summary(hard_results, soft_results)
        if not skill_ok:
            overall_pass = False

        total_hard_results.extend(hard_results)
        total_soft_results.extend(soft_results)

    # Grand summary when validating multiple skills
    if len(skill_paths) > 1:
        total_hard_passed = sum(1 for r in total_hard_results if r.passed)
        total_hard_count = len(total_hard_results)
        total_soft_passed = sum(1 for r in total_soft_results if r.passed)
        total_soft_count = len(total_soft_results)
        total_hard_failed = total_hard_count - total_hard_passed
        total_soft_warnings = total_soft_count - total_soft_passed

        print(f"\n{BOLD}{'=' * 60}{RESET}")
        print(f"{BOLD}  GRAND SUMMARY — {len(skill_paths)} skill(s) validated{RESET}")
        print(f"{BOLD}{'=' * 60}{RESET}")
        print(f"  Hard gates: {total_hard_passed}/{total_hard_count} passed", end="")
        if total_hard_failed:
            print(f", {RED}{total_hard_failed} FAILED{RESET}")
        else:
            print(f" {GREEN}(all clear){RESET}")
        if total_soft_count:
            print(f"  Soft gates: {total_soft_passed}/{total_soft_count} passed", end="")
            if total_soft_warnings:
                print(f", {YELLOW}{total_soft_warnings} warning(s){RESET}")
            else:
                print(f" {GREEN}(all clear){RESET}")

        if overall_pass:
            print(f"\n  {GREEN}{BOLD}ALL SKILLS COMPLIANT{RESET}\n")
        else:
            print(f"\n  {RED}{BOLD}SOME SKILLS FAILED HARD GATES — see details above{RESET}\n")

    # Also run registry sync if --all is specified (always useful to check)
    if args.validate_all and not args.registry_sync:
        print(f"\n{BOLD}{CYAN}Registry Sync Check{RESET}")
        print(f"{CYAN}{'-' * 40}{RESET}")
        sync_ok, sync_msgs = check_registry_sync(REPO_ROOT)
        for msg in sync_msgs:
            print(msg)
        if not sync_ok:
            overall_pass = False
            print(f"  {RED}Registry sync failure counts as a hard gate violation.{RESET}\n")

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
