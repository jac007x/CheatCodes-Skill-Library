# 🗺️ CheatCodes Skill Library — Roadmap

This roadmap is updated 2–3 times per week after the maintainer reviews the
automated weekly audit report. Items are approved, rejected, or re-prioritised
at each review session.

---

## ✅ Recently Shipped

| Item | Version | Date |
|------|---------|------|
| Initial skill library structure | — | 2024-03-18 |
| Task Planner v1 (stable) | 1.0.0 | 2024-01-01 |
| Task Planner v2 (beta) — parallel tracks + dependency graph | 2.0.0-beta | 2024-03-01 |
| Code Reviewer v1 (stable) | 1.0.0 | 2024-01-15 |
| Meeting Summarizer v1 (stable) | 1.0.0 | 2024-02-01 |
| Data Analyzer v1 (stable) | 1.0.0 | 2024-02-15 |
| Interactive Concierge (guided novice launcher) | — | 2024-03-18 |
| Web skill browser (`index.html`) | — | 2024-03-18 |
| Automated weekly CI audit | — | 2024-03-18 |
| GitHub Issue templates (request, recommend, community, bug) | — | 2024-03-18 |

---

## 🔵 In Progress

| Item | Priority | Owner | Notes |
|------|----------|-------|-------|
| Task Planner v2 → stable promotion | High | jac007x | Collecting beta feedback |
| Email Drafter skill (communication) | Medium | — | Requested by community |

---

## 📋 Planned

### New Skills

| Skill | Category | Priority | Notes |
|-------|----------|----------|-------|
| Email Drafter | communication | High | Draft professional emails from bullet points |
| Slack Update Writer | communication | Medium | Convert work updates into Slack-ready messages |
| Test Writer | automation | High | Generate unit tests for a function or class |
| Documentation Generator | automation | High | Generate docstrings and README from code |
| SQL Query Builder | data | Medium | Build complex SQL queries from plain-English descriptions |
| Dashboard Designer | data | Medium | Recommend KPI dashboards from business goals |
| Goal Setting Framework | productivity | Medium | Set SMART goals with measurable milestones |
| Incident Runbook | devops | High | Step-by-step runbook for common incidents |
| Threat Model | security | High | Simple threat model for a feature or system |

### Infrastructure

| Item | Priority | Notes |
|------|----------|-------|
| Search index (auto-generated JSON for `index.html`) | Medium | Sync skills data from YAML → HTML automatically |
| Skill categories page (devops, security) | Medium | Add foundational skills for missing categories |
| Alias/shortcut installer script | Low | `python scripts/concierge.py --install-alias` |
| Shell completion for `concierge.py` | Low | Tab-complete skill names |

---

## ❓ Under Consideration

These items are being evaluated. Feedback welcome via issues.

| Item | Notes |
|------|-------|
| VS Code extension | Launch skills directly from the editor |
| Slack bot integration | Use skills from a Slack slash command |
| Skills chaining (compose multiple skills) | Run skills in sequence as a pipeline |
| Community skill ratings | Thumbs up/down on skill quality |
| Export to Notion / Confluence | Push skill output directly to a workspace |

---

## 🔻 Rejected / Won't Do

| Item | Reason |
|------|--------|
| Automatic prompt execution (no human review) | Safety — human-in-the-loop is intentional |
| Paid tier or feature gating | This library stays 100% free and open source |

---

## How the roadmap is updated

1. The CI audit runs every Monday at 8am UTC and posts a GitHub issue with
   health findings, gap analysis, and suggested roadmap items.
2. The maintainer reviews the issue 2–3 times per week and moves items
   between sections of this file.
3. Community members can vote on items or open new issues to request additions.

Want to influence the roadmap? Open an issue using one of the templates:
- 🌟 [Request a new skill](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=skill_request.yml)
- 💡 [Recommend an improvement](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=skill_recommendation.yml)
- 👥 [Submit a community contribution](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=community_contribution.yml)
