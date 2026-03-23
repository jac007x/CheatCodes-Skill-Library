# CheatCodes Skill Library

A public, open collection of universalized AI agent skills — reusable workflows
that any person, team, or organization can adopt, customize, and run on any
platform that consumes Markdown.

**Walmart-first, open-compatible:** Built to the quality bar of Walmart's AI
governance principles, but every skill is genericized so anyone can use them.

**License:** Apache 2.0

---

## What Is a Skill?

A **skill** is a universalized, parameterized workflow — not a script, not a
one-off prompt. It captures the *pattern* of something that works, strips
everything context-specific into labeled intake variables, and produces a
reusable capability anyone can customize.

```
Workflow that worked once
  → skill-universalizer extracts the pattern
  → SKILL.md documents the phases + intake variables
  → skill-improver watches sessions and improves it over time
  → Anyone activates it, fills the intake, gets the output
```

### The Intake Model

Every skill has an **intake step** — a set of `{{VARIABLES}}` that are
intentionally left blank. When you activate a skill, the agent collects your
specific context and fills those gaps. The universal logic never changes.
Only your context does.

---

## Repository Structure

```
CheatCodes-Skill-Library/
├── {skill-name}/          # Universalized skills (SKILL.md + skill.yaml)
├── templates/             # Skill template for new contributors
├── tools/                 # Validation tools and pre-commit hooks
├── docs/                  # Compliance alignment and discovery docs
├── .github/               # CI workflows and issue templates
├── DOCTRINE.md            # What this library is and believes (immutable)
├── GOVERNANCE.md          # Rules, gates, and pipeline mechanics
├── CONTRIBUTING.md        # How to contribute
├── registry.json          # Central registry of all skills
└── README.md
```

**Every skill contains at minimum:**
- `SKILL.md` — The full skill: philosophy, intake variables, phases, examples, anti-patterns
- `skill.yaml` — Metadata: name, version, origin, author, maturity status, tags

---

## Skill Origin Types

Every skill declares where it came from. Credit is permanent.

| Badge | Origin | Meaning |
|-------|--------|---------|
| 🛠️ | **Created** | Built from scratch by the author |
| 📚 | **Curated** | Adapted from an external source (always credited) |
| 🔱 | **Forked** | Modified from an existing skill |
| 🤝 | **Contributed** | Submitted by a community member |

---

## Skill Maturity

Skills earn trust through real-world usage. No skill is born production-ready.

| Badge | Status | Meaning |
|-------|--------|---------|
| 🧪 | **Beta** | Universalized and merged — functional but unproven at scale |
| ✅ | **Stable** | Proven through 5+ uses, low abandonment, positive signals |
| ⚠️ | **Deprecated** | Superseded or no longer maintained |

See [GOVERNANCE.md](GOVERNANCE.md) for promotion criteria.

---

## Meta-Skills

These skills govern the library and architect new workflows.

| Skill | What It Does | Maturity |
|-------|-------------|----------|
| [adaptive-workflow-architect](adaptive-workflow-architect/) | Designs entropy-aware workflows using Adaptive Narrative Control Theory (ANCT) | 🧪 Beta |
| [skill-suggestor](skill-suggestor/) | Detects repeating workflow patterns and proposes new skills (passive + on-demand) | 🧪 Beta |
| [skill-universalizer](skill-universalizer/) | 6-phase process to extract any working workflow into a reusable skill | 🧪 Beta |
| [skill-improver](skill-improver/) | Passively observes sessions, detects friction, proposes improvements | 🧪 Beta |

> **adaptive-workflow-architect** designs *how* to build it. **skill-suggestor** notices you need one. **skill-universalizer** codifies it. **skill-improver** refines it over time.

---

## Data & Analytics Skills

| Skill | What It Does | Origin | Maturity |
|-------|-------------|--------|----------|
| [survey-nlp-analyzer](survey-nlp-analyzer/) | Open-text NLP pipeline: topic modeling, sentiment analysis, clustering, quote extraction | 🛠️ | 🧪 Beta |
| [org-data-pipeline](org-data-pipeline/) | Pull → reconcile → slice → report organizational data | 🛠️ | 🧪 Beta |
| [powerbi-reports](powerbi-reports/) | PowerBI report generation and distribution patterns | 🛠️ | 🧪 Beta |
| [data-viz-expert](data-viz-expert/) | Data visualization best practices, chart selection, accessibility | 🛠️ | 🧪 Beta |

---

## Document Generation Skills

| Skill | What It Does | Origin | Maturity |
|-------|-------------|--------|----------|
| [talent-card-generator](talent-card-generator/) | Batch document generation from data + templates (PPTX, DOCX, PDF) | 🛠️ | 🧪 Beta |
| [pptx-expert](pptx-expert/) | PowerPoint generation, manipulation, and design patterns | 🛠️ | 🧪 Beta |
| [mbr-deck-builder](mbr-deck-builder/) | Monthly Business Review automation — metrics, analysis, slides | 🛠️ | 🧪 Beta |

---

## Design & Frontend Skills

| Skill | What It Does | Origin | Maturity |
|-------|-------------|--------|----------|
| [a11y-wcag-auditor](a11y-wcag-auditor/) | WCAG 2.2 Level AA accessibility auditing | 🛠️ | 🧪 Beta |
| [design-system-validator](design-system-validator/) | Design system token and component compliance validation | 🛠️ | 🧪 Beta |
| [design-to-code-bridge](design-to-code-bridge/) | Design → production code translation | 🛠️ | 🧪 Beta |
| [designer-orchestrator](designer-orchestrator/) | Multi-phase design QA pipeline coordinator | 🛠️ | 🧪 Beta |
| [layout-composition-analyzer](layout-composition-analyzer/) | Layout and visual composition analysis | 🛠️ | 🧪 Beta |
| [slide-analyzer](slide-analyzer/) | Slide deck structure and content analysis | 🛠️ | 🧪 Beta |

---

## Workflow & Automation Skills

| Skill | What It Does | Origin | Maturity |
|-------|-------------|--------|----------|
| [email-automation-pattern](email-automation-pattern/) | Email workflow automation patterns | 🛠️ | 🧪 Beta |
| [task-rabbit](task-rabbit/) | Task management, audit documentation, and remediation tracking | 🛠️ | 🧪 Beta |
| [session-memory](session-memory/) | Two-tier MEMORY.md system for instant AI session ramp-up | 🛠️ | 🧪 Beta |

---

## Platform Compatibility

All skills are plain Markdown — no proprietary syntax. Any agent or LLM that
reads Markdown can consume a skill.

| Platform | How to Use |
|----------|------------|
| **Any LLM** | Paste `SKILL.md` content as context or system prompt |
| **Custom agents** | Load `SKILL.md` as the agent's instruction set |
| **CLI tools** | Copy to the tool's skills directory |
| **IDE extensions** | Reference `SKILL.md` in your agent configuration |

---

## Adding a New Skill

### From a workflow you built (recommended)
1. Activate `skill-universalizer` in your private repo
2. Walk through the 6-phase extraction process
3. Human context review is mandatory — the agent proposes, you validate
4. Run `python tools/validate_skill.py your-skill/` to check quality gates
5. Submit a PR to this repo

### From scratch
1. Copy `templates/skill-template/`
2. Write `SKILL.md` following the standard sections
3. Fill `skill.yaml` with metadata (see [CONTRIBUTING.md](CONTRIBUTING.md))
4. Add to `registry.json`
5. Submit a PR

### Curating an external skill
1. Open a curation request issue
2. Adapt the pattern into a universalized SKILL.md
3. Set `origin: curated` with proper attribution
4. Submit a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

---

## Quality & Governance

This library enforces **tiered quality gates** on every contribution:

- **Hard gates** (block merge): No PII, no secrets, no internal URLs, valid structure,
  registered in registry, origin declared, attribution present
- **Soft gates** (warnings): Compliance section, example applications, platform notes,
  model recommendation, risk level

**Two layers of enforcement:**
- Pre-commit hook (local, fast)
- GitHub Actions CI (PR validation)

See [GOVERNANCE.md](GOVERNANCE.md) for the full quality framework.

---

## The Self-Improving System

The library gets better every time a skill is used — and it grows by
detecting workflows that should *become* skills:

1. `skill-suggestor` passively detects repeating patterns and proposes new skills
2. `skill-universalizer` extracts the pattern into a reusable SKILL.md
3. `skill-improver` watches sessions and proposes refinements to existing skills
4. All signals are logged privately (never in this repo)
5. Human reviews and approves every change

See [DOCTRINE.md](DOCTRINE.md) for the full philosophy.

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [DOCTRINE.md](DOCTRINE.md) | What this library is, what it believes, immutable principles |
| [GOVERNANCE.md](GOVERNANCE.md) | Quality gates, validation rules, promotion pipeline, CI mechanics |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute skills, improvements, or curations |
| [docs/COMPLIANCE.md](docs/COMPLIANCE.md) | AI governance alignment principles |

---

## Version History

| Date | What Changed |
|------|--------------|
| 2026-03-23 | Doctrine alignment: DOCTRINE.md, GOVERNANCE.md, tiered quality gates, maturity lifecycle, Apache 2.0 |
| 2026-03-20 | Added meta-skills, universalized 18 skills, initialized git |
| 2026-03-18 | Added compliance framework, 3 curated skills |
| 2026-03-17 | Added design ecosystem skills, MBR deck builder |
| 2026-03-13 | Initial library structure |
