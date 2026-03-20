# 🐶 CheatCodes Skill Library

A living library of reusable AI agent skills built for and proven by the
**DAX People Strategy & PMO team**, with a deployment target of Walmart Home Office.

Skills work across platforms: **code-puppy, wibey, Codex, and any LLM**
that can consume a Markdown system prompt.

---

## 🧠 What Is a Skill?

A **skill** is a universalized, parameterized workflow — not a script, not a one-off
prompt. It captures the *pattern* of something that works, strips everything
team-specific into labeled intake variables, and produces a reusable capability
anyone can customize to their situation.

```
Workflow that worked once
  → skill-universalizer extracts the pattern
  → SKILL.md documents the phases + intake variables
  → skill-improver watches sessions and improves it over time
  → Anyone activates it, fills the intake, gets the output
```

### The Intake Model
Every skill has an **intake step** — a set of `{{VARIABLES}}` that are intentionally
left blank. When you activate a skill, the agent collects your specific context
(your file, your columns, your team structure) and fills those gaps. The universal
logic never changes. Only your context does.

---

## 📂 Repository Structure

```
CheatCodes-Skill-Library/
├── {skill-name}/          # New-format skills (SKILL.md + skill.json)
├── skills/                # Original-format skills (deeper structure)
├── docs/                  # Compliance, discovery, contributing guides
├── templates/             # Skill templates for new contributors
├── registry.json          # Skill registry metadata
└── README.md
```

**Skill format:** Each skill contains at minimum:
- `SKILL.md` — The full skill: philosophy, intake variables, phases, code patterns, anti-patterns
- `skill.json` — Metadata: name, version, author, tags, description

---

## 🧬 Meta-Skills (The Governance Layer)

These two skills manage the library itself.

| Skill | Version | What It Does |
|-------|---------|-------------|
| [skill-universalizer](skill-universalizer/) | 1.0.0 | 6-phase process to extract any working workflow into a reusable, cross-platform skill |
| [skill-improver](skill-improver/) | 1.0.0 | Passively observes session flow, friction, and termination behavior to surface improvement proposals — no user feedback required |

> **skill-universalizer** creates skills. **skill-improver** makes them better over time.
> The user's silence is data. Premature closure is data. Rage quits trigger critical proposals.

---

## 📊 Universal Skills — Data & Analytics

| Skill | Version | What It Does | Platforms |
|-------|---------|-------------|----------|
| [survey-nlp-analyzer](survey-nlp-analyzer/) | 1.1.0 | Open-text insights pipeline: topic modeling (NMF), sentiment analysis (VADER), fallback clustering, quote extraction, dimensional heatmaps. Works on surveys, transcripts, feedback forms, open-door cases, idea boards, anything. | All |
| [org-data-pipeline](org-data-pipeline/) | 1.0.0 | Pull → reconcile → cut by dimension → report → archive. Handles ad-hoc and recurring data requests from PowerBI, BigQuery, Excel, Workday. | All |
| [powerbi-reports](powerbi-reports/) | 1.0.0 | PowerBI report generation and distribution patterns | All |

---

## 📝 Universal Skills — Document Generation

| Skill | Version | What It Does | Platforms |
|-------|---------|-------------|----------|
| [talent-card-generator](talent-card-generator/) | 1.0.0 | Batch document generation from data + templates. Maps fields, populates one doc per record, validates, audits. PPTX run-splitting fix included. Applies to talent cards, offer letters, performance reviews, onboarding packets. | All |
| [pptx-expert](pptx-expert/) | 1.0.0 | PowerPoint generation, manipulation, and styling patterns | All |
| [mbr-deck-builder](mbr-deck-builder/) | 2.0.0 | Monthly Business Review automation — org health metrics extraction, pattern detection, slide generation | All |

---

## 🎨 Universal Skills — Design & Frontend

| Skill | What It Does |
|-------|-------------|
| [a11y-wcag-auditor](a11y-wcag-auditor/) | WCAG 2.2 Level AA accessibility auditing |
| [data-viz-expert](data-viz-expert/) | Data visualization best practices and Chart.js patterns |
| [design-system-validator](design-system-validator/) | Design system token and component compliance validation |
| [design-to-code-bridge](design-to-code-bridge/) | Figma/design → production code translation |
| [designer-orchestrator](designer-orchestrator/) | Multi-phase design QA pipeline coordinator |
| [layout-composition-analyzer](layout-composition-analyzer/) | Layout and visual composition analysis |
| [slide-analyzer](slide-analyzer/) | Slide deck structure and content analysis |

---

## ⚙️ Universal Skills — Workflow & Automation

| Skill | What It Does |
|-------|-------------|
| [email-automation-pattern](email-automation-pattern/) | Email workflow automation patterns |
| [task-rabbit](task-rabbit/) | Task management, audit documentation, and remediation tracking |

---

## 🧪 Proving Grounds — DAX People Team

These skills were built for specific DAX People workflows and are on the
path to universalization. They work as-is; they just carry more team-specific
context than the universal skills above.

| Skill | What It Does | Next Step |
|-------|-------------|----------|
| [fplus-tech-panel](fplus-tech-panel/) | F+ tech panel nomination tracking, panelist email automation, calibration reporting | Universalize → `review-cycle-manager` |
| [skyward-panel-status](skyward-panel-status/) | Check tech panel feedback status from Skyward API, update tracking spreadsheet | Merge into `review-cycle-manager` |

---

## 📚 Curated Skills (Original Library)

These skills live in the `skills/` subfolder and use the original skill format.

| Skill | Source | What It Does |
|-------|--------|--------------|
| [mbr-engine](skills/mbr-engine/) | 🛠️ Created | MBR automation with Python pipeline |
| [msgraph-people](skills/msgraph-people/) | 📚 Curated | Calendar & email workflows for People |
| [document-processing](skills/document-processing/) | 📚 Curated | PDF, PPTX, and form extraction |
| [confluence-people](skills/confluence-people/) | 📚 Curated | Knowledge management for People |
| [jira-people](skills/jira-people/) | 📚 Curated | Work management for People |

---

## 🚀 Deployment Ladder

Every skill moves through three validation stages before it's considered
ready for Walmart Home Office scale:

```
┌───────────────────────────────────────────────┐
│ 🧪 REFINE    Strategy & PMO           │
│          Testing and refinement team     │
│          ↓                               │
│ 🔬 PROVE     DAX People Team           │
│          Proving grounds across orgs     │
│          ↓                               │
│ 🌐 SCALE     Walmart Home Office        │
│          Universal, self-serve           │
└───────────────────────────────────────────────┘
```

---

## 🌐 Platform Compatibility

All skills in SKILL.md format are plain Markdown — no proprietary syntax.

| Platform | How to Use |
|----------|------------|
| **code-puppy** | `/skill {skill-name}` |
| **wibey** | Copy `SKILL.md` to `~/.wibey/skills/{skill-name}/` |
| **Codex** | Paste `SKILL.md` content as system prompt prefix |
| **ChatGPT / Claude / Gemini** | Paste `SKILL.md` into conversation as context |

---

## ➕ Adding a New Skill

### From a workflow you built (recommended)
1. Activate `skill-universalizer`
2. Walk through the 6-phase extraction process
3. Human context review is mandatory — the agent proposes, you validate
4. Commit with a meaningful message and version tag

### From scratch
1. Copy `templates/skill-template/`
2. Write `SKILL.md` following the standard sections
3. Fill `skill.json` with metadata
4. Add to `registry.json`
5. Submit PR

### Curating an external skill
1. [Submit a curation request](../../issues/new?template=curate-skill.yml)
2. Evaluate, adapt, attribute
3. Add `"source": "curated"` in `skill.json`

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## 🛡️ Compliance

All skills comply with **Walmart's Ethical AI principles** and **AI-01-02 standards**.
PII handling is documented per skill. Raw data files are excluded from git.

| Category | Risk Level | PII Handling |
|----------|------------|-------------|
| NLP / text analysis skills | Medium | ⚠️ May contain survey verbatims — never commit raw data |
| Document generation skills | Low–Medium | ⚠️ May contain HR data — validate before sharing output |
| Design / frontend skills | Low | ✅ No PII |
| Workflow / automation skills | Low | ✅ No PII in skill itself |
| Meta-skills | Low | ⚠️ Signal logs may contain session snippets — gitignored |

See [docs/COMPLIANCE.md](docs/COMPLIANCE.md) for the full framework.

---

## 📜 Version History

| Date | What Changed |
|------|--------------|
| 2026-03-20 | Added 5 new skills: `survey-nlp-analyzer` v1.1.0, `org-data-pipeline`, `talent-card-generator`, `skill-universalizer`, `skill-improver`. Initialized git. Connected remote. |
| 2026-03-18 | Added compliance framework, model recommendations, 3 curated People skills |
| 2026-03-17 | Added design ecosystem skills (7 skills), MBR deck builder |
| 2026-03-13 | Initial library structure, MBR engine, MS Graph for People |
