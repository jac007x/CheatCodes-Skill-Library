# Task Planner

> **Status:** `v1 stable` / `v2 beta` | **Category:** `productivity`

## Overview

Breaks down a goal or project into clear, prioritized, actionable tasks.
Given a high-level goal or project description, Task Planner decomposes it
into a structured, prioritized task list, identifies dependencies, estimates
effort, and organises work into phases.

---

## Quick Start

```bash
# Clone just this skill into your working directory
bash <(curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh) productivity/task-planner
```

Or browse the versions directly:

| Version | Status | Prompt |
|---------|--------|--------|
| [v1](v1/prompt.md) | ✅ Stable | [v1/prompt.md](v1/prompt.md) |
| [v2-beta](v2-beta/prompt.md) | ⚠️ Beta | [v2-beta/prompt.md](v2-beta/prompt.md) |

---

## Usage

1. Pick the version you want (v1 for stable, v2-beta for parallel-track planning).
2. Copy the prompt from the version folder's `prompt.md`.
3. Paste it into your AI assistant and fill in the placeholders.
4. Review and refine the generated task breakdown.

### When to use v1 vs v2

| Scenario | Recommended Version |
|----------|-------------------|
| Simple project, single team track | v1 (stable) |
| Complex project, parallel workstreams | v2-beta |
| Production / mission-critical use | v1 (stable) |
| Want to try new features & give feedback | v2-beta |

---

## Examples

### Example — Plan a product launch (v1)

**Input:**
```
Goal: Launch a new SaaS analytics dashboard in 8 weeks.
Team size: 4 (1 PM, 2 engineers, 1 designer)
Constraints: No budget for paid ads, must integrate with Slack.
```

**Output structure:**
- Phase 1 — Discovery & Design (Week 1–2)
- Phase 2 — Core Development (Week 3–5)
- Phase 3 — Integration & Testing (Week 6–7)
- Phase 4 — Launch & Monitor (Week 8)

---

## Versioning & Changelog

| Version | Status | Date | Notes |
|---------|--------|------|-------|
| `2.0.0` | ⚠️ beta | 2024-03-01 | Parallel tracks, dependency graph, improved effort estimation |
| `1.0.0` | ✅ stable | 2024-01-01 | Initial release |

---

## Contributing & Feedback

- 🐛 [Report a bug](../../issues/new?template=bug_report.yml)
- 💡 [Recommend an improvement](../../issues/new?template=skill_recommendation.yml)
- 🌟 [Request a new skill](../../issues/new?template=skill_request.yml)
- 👥 [Submit a community variation](../../issues/new?template=community_contribution.yml)

---

## License

MIT — see [LICENSE](../../LICENSE)
