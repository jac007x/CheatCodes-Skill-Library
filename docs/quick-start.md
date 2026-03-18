# ⚡ Quick Start Guide

> **No coding experience needed.** This guide will get you using your first skill in under 5 minutes.

---

## What is a skill?

A **skill** is a ready-made prompt — a set of instructions you paste into an AI assistant
(like ChatGPT, Claude, or Microsoft Copilot). Each skill is carefully crafted to do one
thing really well, so you get a great result without figuring out the right words yourself.

---

## Three ways to get started

Pick the one that sounds easiest to you:

---

### 🌐 Option A — Use the web browser (easiest)

1. Open `index.html` in your web browser (just double-click the file).
2. Browse or search for the skill you need.
3. Click on a skill card.
4. Fill in your details in the form.
5. Click **"Build & Copy Prompt"**.
6. Paste into your AI assistant and read the result.

> If you haven't cloned the repo yet, you can also browse skills directly on GitHub:
> **[github.com/jac007x/CheatCodes-Skill-Library/tree/main/skills](https://github.com/jac007x/CheatCodes-Skill-Library/tree/main/skills)**

---

### 💻 Option B — Use the interactive concierge (guided terminal)

The concierge is like a friendly assistant that walks you through everything step by step.

**One-time setup:**
```bash
# 1. Make sure Python is installed (version 3.8 or newer)
python --version        # or:  python3 --version

# 2. Clone the repository (download it to your computer)
git clone https://github.com/jac007x/CheatCodes-Skill-Library.git
cd CheatCodes-Skill-Library

# 3. Launch the concierge
python scripts/concierge.py
```

**After the first time:**
```bash
cd CheatCodes-Skill-Library
python scripts/concierge.py
```

**Optional shortcut** (add to your shell profile so you can type `cheat` anywhere):
```bash
# Add this line to ~/.bashrc or ~/.zshrc
alias cheat='python ~/CheatCodes-Skill-Library/scripts/concierge.py'
```

---

### 📁 Option C — Use skills directly (manual)

1. Browse the [`skills/`](../skills/) folder.
2. Open the skill folder you want (e.g., `skills/productivity/task-planner/`).
3. Read the `README.md` for instructions.
4. Open a version folder (e.g., `v1/`) and copy `prompt.md`.
5. Fill in the `[PLACEHOLDERS]` with your details.
6. Paste into your AI assistant.

---

## Step-by-step example: Plan a project with Task Planner

Let's say you want to plan a website redesign project.

### Using the web browser (Option A)

1. Open `index.html` — you'll see all skills.
2. Search for `"plan"` or click the **🚀 Productivity** filter.
3. Click the **📋 Task Planner** card.
4. Choose **v1 (Stable)**.
5. Fill in:
   - **Goal:** "Redesign our company website"
   - **Team size:** "3 people — 1 designer, 1 developer, 1 PM"
   - **Timeline:** "6 weeks"
   - **Constraints:** "Must stay on brand, no new tools"
6. Click **"Build & Copy Prompt"** — your completed prompt is ready and copied.
7. Paste it into ChatGPT, Claude, or your AI assistant of choice.

### What you'll get back

The AI will produce a structured plan like this:

```
# Website Redesign Project Plan

## Goal
Deliver a refreshed company website in 6 weeks that stays on brand…

## Phase 1 — Discovery & Design (Week 1–2)
- [ ] Stakeholder interviews  [High / 4h / Owner: PM]
- [ ] Content audit           [Medium / 3h / Owner: PM]
- [ ] Wireframes              [High / 8h / Owner: Designer]
…

## Summary Table
| Task               | Priority | Effort | Phase |
|--------------------|----------|--------|-------|
| Stakeholder review | Critical | 2h     | 1     |
…
```

---

## Frequently asked questions

**Do I need to pay for anything?**
No. The skill library is free and open source. You do need an AI assistant
(ChatGPT, Claude, Copilot, etc.) — most have a free tier.

**What AI assistant should I use?**
Any of these work great: ChatGPT (chat.openai.com), Claude (claude.ai),
Microsoft Copilot (copilot.microsoft.com), Google Gemini (gemini.google.com).

**What does "stable" vs "beta" mean?**
- ✅ **Stable** — tested and reliable. Use for everyday work.
- ⚠️ **Beta** — new features being tested. Usually works great, but
  results may vary. Share feedback via GitHub issues.

**How do I request a new skill?**
Open [this link](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=skill_request.yml)
and fill in the short form. The team reviews requests 2–3 times a week.

**How do I save a skill to use offline?**
```bash
# Clone just one skill
bash <(curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh) productivity/task-planner
```

**Something isn't working — what do I do?**
[Open a bug report](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=bug_report.yml)
and describe what happened. We'll fix it quickly.

---

## What's next?

- Browse all skills → [`skills/`](../skills/README.md)
- Read the full README → [`README.md`](../README.md)
- See what's coming → [`ROADMAP.md`](../ROADMAP.md)
- Contribute a skill → [`CONTRIBUTING.md`](../CONTRIBUTING.md)
