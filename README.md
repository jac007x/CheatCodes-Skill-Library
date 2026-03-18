# ⚡ CheatCodes Skill Library

> **Ready-made AI prompts for everyone.** No coding experience needed.

The CheatCodes Skill Library is a curated, versioned collection of high-quality
AI prompts ("skills") that you can pick up, fill in your details, and paste into
any AI assistant — ChatGPT, Claude, Copilot, Gemini, you name it.

Each skill is self-contained, documented, versioned, and designed to be
composable so you can chain skills together to tackle bigger workflows.

---

## 🚀 Get started in 30 seconds

**Option 1 — Open in your browser** *(no setup required)*

1. Download this repository (click **Code → Download ZIP** on GitHub).
2. Open `index.html` by double-clicking it.
3. Browse, fill in your details, copy, and paste into your AI assistant.

**Option 2 — Interactive concierge** *(guided experience, one-time setup)*

```bash
# Requires Python 3.8+ and git
git clone https://github.com/jac007x/CheatCodes-Skill-Library.git
cd CheatCodes-Skill-Library
python scripts/concierge.py
```

The concierge will greet you, help you find the right skill, walk you through
filling in the prompt, copy it to your clipboard, and save your favourites for
next time. No technical knowledge required.

**Option 3 — One-liner, no clone needed**

```bash
curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/concierge.py | python -
```

📖 **Detailed walkthrough:** [docs/quick-start.md](docs/quick-start.md)

---

## 📚 Available Skills

| Skill | Category | Status | What it does |
|-------|----------|--------|--------------|
| [📋 Task Planner](skills/productivity/task-planner/) | productivity | ✅ v1 stable / ⚠️ v2 beta | Break any goal into a phased, prioritised action plan |
| [🔍 Code Reviewer](skills/automation/code-reviewer/) | automation | ✅ stable | Structured code review with severity ratings and security checklist |
| [📝 Meeting Summarizer](skills/communication/meeting-summarizer/) | communication | ✅ stable | Convert raw notes into decisions, action items, and TL;DR |
| [📊 Data Analyzer](skills/data/data-analyzer/) | data | ✅ stable | Dataset insights, anomaly detection, and visualisation recommendations |
| [📈 MBR Engine](skills/mbr-engine/) | hr-analytics | 🔧 in development | Monthly Business Review automation with org health metrics and PowerPoint generation |

👉 **Full index:** [skills/README.md](skills/README.md)

---

## 🗂️ Repository Structure

```
CheatCodes-Skill-Library/
│
├── index.html                    # 🌐 Open in browser — visual skill browser & launcher
├── scripts/
│   ├── concierge.py              # 🤖 Interactive guided concierge (run me first!)
│   ├── clone-skill.sh            # 📥 Clone a single skill to your computer
│   ├── validate_skills.py        # ✅ CI: validate skill manifests
│   ├── audit.py                  # 🔍 CI: weekly library health audit
│   └── publish_skill.py          # 🚢 CI: version-bump a skill for release
│
├── skills/                       # All skills, organised by category
│   ├── productivity/
│   │   └── task-planner/
│   │       ├── skill.yaml        # Skill manifest (metadata, versioning)
│   │       ├── README.md         # Skill documentation
│   │       ├── v1/prompt.md      # Stable prompt
│   │       └── v2-beta/prompt.md # Beta prompt (new features)
│   ├── automation/code-reviewer/
│   ├── communication/meeting-summarizer/
│   ├── data/data-analyzer/
│   └── mbr-engine/               # Monthly Business Review automation
│
├── templates/skill-template/     # Starter template for new skills
├── registry.json                 # Skill registry metadata
├── docs/
│   └── quick-start.md            # 📖 Step-by-step guide for new users
│
└── .github/
    ├── workflows/                # CI/CD: validation, weekly audit, releases
    └── ISSUE_TEMPLATE/           # Skill requests, recommendations, bug reports
```

---

## 🔢 How Versioning Works

Every skill uses **semantic versioning** (`MAJOR.MINOR.PATCH`) and a clear status:

| Status | Badge | Meaning |
|--------|-------|---------|
| stable | ✅ | Tested and reliable. Use for everyday work. |
| beta | ⚠️ | New features being collected feedback on. Usually works great. |
| deprecated | 🔻 | Being replaced — migrate to the newer version. |
| archived | 🗄️ | Kept for reference; no longer maintained. |

**Key principle:** Old versions are never deleted. If v1 works perfectly for you,
you can always use v1. New versions add capabilities without breaking what works.

---

## 🤝 Contributing

We welcome skill contributions, improvement suggestions, and community variations.

| I want to… | How |
|-----------|-----|
| Request a new skill | [Open a Skill Request issue](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=skill_request.yml) |
| Improve an existing skill | [Open a Skill Recommendation issue](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=skill_recommendation.yml) |
| Submit a community version | [Open a Community Contribution issue](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=community_contribution.yml) |
| Report a bug | [Open a Bug Report issue](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=bug_report.yml) |
| Add a new skill via PR | See [templates/skill-template/](templates/skill-template/) for the starter files |

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

---

## ⚙️ Automation & CI

The library runs on autopilot so quality stays high even as it scales:

| Workflow | When it runs | What it does |
|----------|-------------|--------------|
| **Skill Validation** | Every PR touching `skills/` | Validates manifests, structure, and required files |
| **Weekly Audit** | Every Monday at 8am UTC | Generates a health report + roadmap suggestions as a GitHub issue |
| **Skill Release** | Manual trigger | Version-bumps a skill, creates a git tag, and publishes a GitHub release |

The audit report is reviewed 2–3 times a week and used to drive the roadmap.
Results are posted as a GitHub issue with a checklist for approving/rejecting items.

---

## 📋 ROADMAP

See [ROADMAP.md](ROADMAP.md) for what's planned, in progress, and recently shipped.

---

## 📄 License

[MIT](LICENSE) — free to use, modify, and distribute.
