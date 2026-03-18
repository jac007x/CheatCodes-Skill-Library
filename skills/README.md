# Skills Index

Browse all available CheatCodes skills. Each skill includes a versioned
prompt, manifest, documentation, and a quick-clone command.

---

## Categories

| Category | Description | Skills |
|----------|-------------|--------|
| [productivity](productivity/) | Planning, organisation, focus, GTD | 1 |
| [automation](automation/) | Code, workflows, bots, CI/CD | 1 |
| [communication](communication/) | Meetings, writing, async updates | 1 |
| [data](data/) | Analysis, insights, visualisation | 1 |
| [hr-analytics](mbr-engine/) | HR metrics, org health, reporting | 1 |

---

## All Skills

| Skill | Category | Status | Latest | Description |
|-------|----------|--------|--------|-------------|
| [task-planner](productivity/task-planner/) | productivity | ⚠️ v2 beta / ✅ v1 stable | 2.0.0 | Break down goals into prioritised, actionable tasks |
| [code-reviewer](automation/code-reviewer/) | automation | ✅ stable | 1.0.0 | Automated structured code review with severity ratings |
| [meeting-summarizer](communication/meeting-summarizer/) | communication | ✅ stable | 1.0.0 | Convert meeting notes into decisions + action items |
| [data-analyzer](data/data-analyzer/) | data | ✅ stable | 1.0.0 | Dataset insights, anomalies, and visualisation recommendations |
| [mbr-engine](mbr-engine/) | hr-analytics | 🔧 in development | 2.0.0 | Monthly Business Review automation with org health metrics and PowerPoint generation |

---

## Status Legend

| Badge | Meaning |
|-------|---------|
| ✅ stable | Battle-tested, safe for production use |
| ⚠️ beta | Feature-complete but collecting feedback — use with care |
| 🗄️ archived | Superseded; available for reference but no longer maintained |

---

## How to Clone a Skill

```bash
# Clone the latest stable version of a skill
bash <(curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh) <category>/<skill-name>

# Clone a specific version
bash <(curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh) <category>/<skill-name> --version v1

# List all available skills
bash <(curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh) --list
```

---

## Requesting a New Skill

👉 [Open a Skill Request issue](../issues/new?template=skill_request.yml)

---

## Recommending an Improvement

👉 [Open a Skill Recommendation issue](../issues/new?template=skill_recommendation.yml)
