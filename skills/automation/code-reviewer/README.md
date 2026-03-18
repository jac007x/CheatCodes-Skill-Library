# Code Reviewer

> **Status:** `v1 stable` | **Category:** `automation`

## Overview

Performs an automated, structured code review of a diff or file set, surfacing
bugs, style issues, security risks, and improvement suggestions. Output is a
structured review comment list ready to paste into a PR.

---

## Quick Start

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh) automation/code-reviewer
```

Or use the prompt directly: [v1/prompt.md](v1/prompt.md)

---

## Usage

1. Copy the prompt from [v1/prompt.md](v1/prompt.md).
2. Paste it into your AI assistant.
3. Fill in: language/framework, review focus, and paste your diff or code.
4. Apply the structured review comments to your PR.

### Review Focus Options

| Focus | What it checks |
|-------|---------------|
| `correctness` | Logic errors, edge cases, incorrect assumptions |
| `security` | OWASP vulnerabilities, secrets, injection risks |
| `performance` | Unnecessary loops, memory issues, slow queries |
| `style` | Readability, naming, formatting consistency |
| `all` | All of the above |

---

## Examples

### Review a Python function

**Input:**
```
Language: Python
Focus: correctness, security
Code: <paste diff>
```

**Output:** Structured Markdown table of issues with severity ratings, plus
an overall APPROVE / REQUEST CHANGES recommendation.

---

## Versioning & Changelog

| Version | Status | Date | Notes |
|---------|--------|------|-------|
| `1.0.0` | ✅ stable | 2024-01-15 | Initial release |

---

## Contributing & Feedback

- 🐛 [Report a bug](../../issues/new?template=bug_report.yml)
- 💡 [Recommend an improvement](../../issues/new?template=skill_recommendation.yml)

---

## License

MIT — see [LICENSE](../../LICENSE)
