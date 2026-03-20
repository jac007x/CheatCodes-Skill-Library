# Skill: Session Memory Bootstrap

Bootstrap a two-tier MEMORY.md system so Code Puppy can ramp up instantly at the start of any session.

---

## When to activate this skill

Activate when a user says any of:
- "set up memory for this project"
- "create a memory file"
- "add session memory"
- "I want you to remember this project"
- "reduce ramp-up time"
- "build a memory structure"

---

## Architecture (always explain this to the user first)

Two tiers:
1. **`~/MEMORY.md`** — global, ~150 line cap. Who the user is, project directory, cross-project prefs, agent toolkit, active focus, rolling session log.
2. **`<project>/MEMORY.md`** — per-project, ~300 line cap. Deep context: structure, conventions, key people, task recipes, current status, pending items, rolling session log.

Both use the same three-section pattern:
- **Static sections** — rarely change (structure, conventions, people, recipes)
- **Dynamic sections** — fully *replaced* each session, never appended (current status, pending items)
- **Rolling session log** — max 10 entries, oldest gets collapsed into a summary line

This design means the files **never grow unboundedly** across thousands of sessions.

---

## Execution Steps

### Step 1 — Reconnaissance (always do this first)

Before writing anything, gather context:

```
1. list_files(cwd, recursive=False)  — understand project structure
2. Check for existing git history: `git log --oneline -5`
3. Look for README, config files, package.json, pyproject.toml, etc.
4. Check if ~/MEMORY.md already exists
5. Check if <project>/MEMORY.md already exists
6. Read any existing MEMORY.md files before overwriting
```

Never write a generic template. Always populate from what you actually found.

---

### Step 2 — Write or update `<project>/MEMORY.md`

Create at `<project_root>/MEMORY.md`. Use this exact structure:

```markdown
# <Project Name> — Session Memory
_Last updated: <TODAY> by Code Puppy_

---

## 🐶 Code Puppy Instructions (read first, every session)

1. Read this entire file before doing anything.
2. Update only the three dynamic sections at the end of each session:
   - `## 📡 Current Status` — fully replace, don't append
   - `## 📋 Pending Items` — fully replace, don't append
   - `## 🗓 Session Log` — add 1 new entry at top, drop oldest if count > 10
3. Never let this file exceed ~300 lines. Tighten static sections if needed.
4. Commit MEMORY.md at the end of every session.

---

## 📁 Project Structure (static)

[List the actual files/dirs found. Explain what each does in 1 line.]
[Include any live URLs, publish targets, or key endpoints.]
[Include how to run/build/test/deploy the project.]

---

## 🗂 Data & Code Conventions (static)

[Document key enums, status values, naming patterns, formulas, or
 business rules that an AI needs to know to not break things.
 Only include what's non-obvious. Skip what's in the code comments.]

---

## 👥 Key People (static)

| Name | Role | Contact |
|---|---|---|
| [name] | [role] | [email/slack] |

[Only include people relevant to THIS project.]

---

## 🛠 Common Task Recipes (static)

[3-5 most common tasks with exact steps/code snippets.
 Think: what will Code Puppy be asked to do 80% of the time?
 Be specific enough that no file-reading is needed to execute.]

---

## 📡 Current Status (dynamic — replace entirely each session)

_As of <DATE TIME TZ>_

[2-5 bullet points: what state is the project in right now?
 Key metrics, blockers, what's done, what's next.]

---

## 📋 Pending Items (dynamic — replace entirely each session)

[Table or list of what's actively in-flight.
 Include owner, expected date, and any blockers.
 Remove items when they're done — don't let this become a graveyard.]

---

## 🗓 Session Log (dynamic — rolling last 10, collapse older into summary)

**Prior history summary:** [one-line summary of everything before the last 10 sessions]

| Date | Summary |
|---|---|
| <TODAY> | [What was done this session — 1 line max] |
```

---

### Step 3 — Write or update `~/MEMORY.md`

Create at `~/MEMORY.md` (user home directory). Use this exact structure:

```markdown
# Global Memory — <User Display Name>
_Last updated: <TODAY> by Code Puppy_

---

## 🐶 Code Puppy Instructions (read first, every session)

1. Read this file at the start of EVERY session.
2. If the user mentions a specific project, find it in the Project Directory
   and read its MEMORY.md next.
3. At end of session update:
   - `## 📡 Active Focus` — fully replace
   - `## 🗓 Session Log` — add 1 entry at top, drop oldest if > 10
4. Never exceed ~150 lines.

---

## 👤 Who Is <Name> (static)

- **Name:** [full name]
- **Username:** [username]
- **Email:** [email]
- **Org / Team:** [org and team]
- **Machine:** [mac/windows, path]
- **Preferred Code Puppy nickname:** [if they have one]

---

## 📁 Project Directory (update when projects are added/archived)

| Project | Path | MEMORY.md | Description |
|---|---|---|---|
| [name] | `~/projects/[name]` | ✅/❌ | [one-line description] |

---

## ⚙️ Global Preferences (static)

### Code & Stack
[User's preferred stack, languages, frameworks, patterns.]
[Any hard rules: line length caps, always use X instead of Y, etc.]

### Publishing
[How/where they publish output — puppy.walmart.com, GitHub Pages, etc.]

### Communication Tools
[How they handle email, Slack, Teams workflows.]

### Memory System Rules
- `~/MEMORY.md` — this file, global orientation, ~150 line cap
- `<project>/MEMORY.md` — per-project deep context, ~300 line cap
- Static sections: rarely change
- Dynamic sections: fully replaced each session
- Session log: rolling 10 entries max

### Agent Toolkit
| Agent | When to use |
|---|---|
[List only agents the user actually uses with a real use case per agent.]

---

## 📡 Active Focus (dynamic — replace entirely each session)

_As of <DATE>_

[1-3 bullets: what project/task is the user working on right now?
 Which project MEMORY.md to read next?]

---

## 🗓 Session Log (rolling last 10 — collapse older into summary)

**Prior history summary:** [one-liner of all history before last 10]

| Date | Project | Summary |
|---|---|---|
| <TODAY> | [project] | [1-line summary] |
```

---

### Step 4 — Quality checks before finishing

Before committing, verify:

- [ ] No section is a generic placeholder — everything populated from real recon
- [ ] Static sections contain only non-obvious info (not what's in the code)
- [ ] Dynamic sections clearly labeled "replace entirely each session"
- [ ] Session log has exactly 1 entry (today) for a new file
- [ ] Project MEMORY.md is under 300 lines: `wc -l <project>/MEMORY.md`
- [ ] Global MEMORY.md is under 150 lines: `wc -l ~/MEMORY.md`
- [ ] Both files committed to git (project one only — global isn't in a repo)
- [ ] Update `~/MEMORY.md` Project Directory table with ✅ for the new project

---

### Step 5 — If MEMORY.md already exists

Do NOT overwrite. Instead:
1. Read the existing file
2. Identify what's stale (dates, pending items, status)
3. Ask the user: "I found an existing MEMORY.md — want me to refresh it with today's context or leave the static sections and just update the dynamic ones?"
4. Apply targeted updates using ReplacementsPayload, not a full rewrite

---

## Anti-patterns (never do these)

- ❌ Copy-paste the template literally — always populate from real data
- ❌ Append to dynamic sections — always replace them
- ❌ Put implementation details in static sections (that's what the code is for)
- ❌ Let the session log grow past 10 entries
- ❌ Let the file exceed the line cap — trim static sections instead
- ❌ Create MEMORY.md without doing recon first
- ❌ Put secrets, tokens, or credentials anywhere in MEMORY.md
