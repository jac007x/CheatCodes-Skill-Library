# Meeting Summarizer

> **Status:** `v1 stable` | **Category:** `communication`

## Overview

Converts raw meeting transcripts or notes into a concise, structured summary
with decisions, action items, and owners — eliminating post-meeting
note-taking overhead.

---

## Quick Start

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh) communication/meeting-summarizer
```

Or use the prompt directly: [v1/prompt.md](v1/prompt.md)

---

## Usage

1. Copy the prompt from [v1/prompt.md](v1/prompt.md).
2. Specify meeting type, participants, and date.
3. Paste your raw transcript or notes.
4. Distribute the structured summary to stakeholders.

### Supported Meeting Types

- Standup / daily sync
- Sprint planning
- Retrospective
- Decision meeting
- Brainstorming session
- Any ad-hoc meeting

---

## Examples

### Sprint Planning Summary

**Input:**
```
Meeting Type: Sprint planning
Participants: Alice (PM), Bob (Eng), Carol (Design)
Date: 2024-03-01
Notes: <raw notes>
```

**Output includes:**
- TL;DR (2–3 sentences)
- Decisions Made
- Action Items table (task, owner, due date)
- Open Questions
- Key Discussion Points
- Next Steps

---

## Versioning & Changelog

| Version | Status | Date | Notes |
|---------|--------|------|-------|
| `1.0.0` | ✅ stable | 2024-02-01 | Initial release |

---

## Contributing & Feedback

- 🐛 [Report a bug](../../issues/new?template=bug_report.yml)
- 💡 [Recommend an improvement](../../issues/new?template=skill_recommendation.yml)

---

## License

MIT — see [LICENSE](../../LICENSE)
