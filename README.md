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
│   └── data/data-analyzer/
│
├── templates/skill-template/     # Starter template for new skills
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

### 🧑‍✈️ Concierge — your guided skill navigator

The **concierge** is the recommended way for any user — especially beginners — to
interact with the library. It requires no technical knowledge.

```bash
# Requires Python 3.8+ (no extra packages) and git
git clone https://github.com/jac007x/CheatCodes-Skill-Library.git
cd CheatCodes-Skill-Library
python scripts/concierge.py
```

**One-liner — no clone needed:**

```bash
curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/concierge.py | python -
```

What the concierge does for you:

| Feature | How it helps |
|---------|-------------|
| **Browse by category** | Lists every skill grouped by what it does |
| **Keyword search** | Type what you want; it finds the best match |
| **Guided launch wizard** | Asks you questions, fills in the prompt, copies it to your clipboard |
| **Version picker** | Choose stable or beta; shows warnings for beta usage |
| **Favourites** | Save skills you use often for instant re-launch |
| **Clone a skill** | Gives you the exact terminal command to save a skill locally |
| **Library health check** | Runs the review crew and shows you a summary |
| **Request / Recommend** | Opens the right GitHub issue form in one click |

The concierge also **auto-loads any new skills** added to `skills/` — you never
need to update the code to see new skills.

---

### 🤖 Automated Review Crew — the library's sentient quality team

Three specialist agents run **every Monday at 8am UTC** and post their findings as
a GitHub issue for the maintainer's 2–3× weekly review session.

```bash
# Run the crew manually at any time
python scripts/crew.py

# Run a single agent
python scripts/crew.py --agent librarian   # structural health only
python scripts/crew.py --agent scout       # gap analysis only
python scripts/crew.py --agent coach       # prompt quality only

# Write the report to a file
python scripts/crew.py --output report.md
```

| Agent | Role | What it finds |
|-------|------|---------------|
| 🏛️ **Librarian** | Structural health | Missing required fields, stale skills, invalid status/version values, missing README or prompt files, changelog format issues |
| 🔭 **Scout** | Coverage & adoption | Missing categories, skill patterns not yet in the library, 15 curated adoption candidates sourced from the wider AI prompting community |
| 🎯 **Coach** | Prompt quality | Prompts missing structure, role-setting, placeholders; skills that could benefit from a beta version; discoverability improvements |

The **Coordinator** assembles all three agents' findings into a single prioritised
roadmap report with a maintainer review checklist. Results are posted as a GitHub
issue labelled `audit · roadmap · automated`.

The library health score (0–100) gives a quick signal of overall quality.
Critical issues cost 10 points each; warnings cost 3 points.

---

### Other workflows

| Workflow | When it runs | What it does |
|----------|-------------|--------------|
| **Skill Validation** | Every PR touching `skills/` | Validates manifests, structure, and required files |
| **Crew Review** | Every Monday at 8am UTC | Runs all three crew agents and posts findings as a GitHub issue |
| **Skill Release** | Manual trigger | Version-bumps a skill, creates a git tag, and publishes a GitHub release |

---

## 📋 ROADMAP

See [ROADMAP.md](ROADMAP.md) for what's planned, in progress, and recently shipped.

---

## 📄 License

[MIT](LICENSE) — free to use, modify, and distribute.
