# Session Memory Bootstrap

🛠️ **Source**: Created by jac007x  
**Category**: Productivity, Session Management, AI Workflow  
**Model**: Sonnet recommended

Bootstrap a two-tier `MEMORY.md` system so Code Puppy ramps up instantly at the start of any session — no matter how many thousands of conversations have happened before.

---

## The Problem

AI assistants lose context between sessions. Without memory, every conversation starts from zero — rereading files, re-explaining the project, re-establishing preferences. At scale (10,000+ sessions), this is a serious productivity tax.

## The Solution

Two lean, structured files that an AI reads at session start:

| File | Cap | Purpose |
|---|---|---|
| `~/MEMORY.md` | ~150 lines | Global: who the user is, all projects, preferences, agents |
| `<project>/MEMORY.md` | ~300 lines | Deep: structure, conventions, people, recipes, live status |

### Why it stays lean forever

Three-section architecture:
- **Static** — rarely updated (structure, conventions, contacts, recipes)
- **Dynamic** — fully *replaced* each session (status, pending items)
- **Rolling log** — max 10 entries; entry 11 collapses oldest into a summary line

---

## Usage

Just tell Code Puppy:
> "Set up session memory for this project"
> "Create a MEMORY.md"
> "I want you to remember this project between sessions"

Code Puppy will:
1. Recon your project (files, git history, stack, patterns)
2. Create or update `<project>/MEMORY.md` — populated from real data, not a blank template
3. Create or update `~/MEMORY.md` — adding this project to your global directory
4. Verify line caps are respected
5. Commit the project MEMORY.md to git

---

## Maintenance

At the **end of each session**, Code Puppy should:
1. Replace `## 📡 Current Status` with today's state
2. Replace `## 📋 Pending Items` with what's currently in-flight
3. Prepend one line to `## 🗓 Session Log`, drop the oldest if > 10
4. Commit both files

At the **start of each session**, Code Puppy reads `~/MEMORY.md` first, then the relevant `<project>/MEMORY.md`.

---

## Anti-patterns

| ❌ Don't | ✅ Do instead |
|---|---|
| Copy-paste the template literally | Populate from real recon |
| Append to dynamic sections | Fully replace them |
| Let session log grow past 10 | Collapse oldest into summary |
| Exceed line caps | Trim static sections |
| Store secrets/tokens | Keep it safe and shareable |

---

## Compliance

| Requirement | Status | Notes |
|---|---|---|
| Approved AI Services | ✅ | Code Puppy (Walmart-approved) |
| PII Handling | ✅ Low risk | No secrets, no credentials. User controls what goes in. |
| Data Storage | ✅ | Local files only. No external transmission. |
| Risk Level | ✅ Low | Documentation skill — no system access beyond file writes |
