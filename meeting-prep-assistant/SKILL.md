---
name: meeting-prep-assistant
description: "Entropy-aware meeting preparation skill that pulls context, assesses attendee relationships, surfaces open items, infers the real meeting purpose, and produces an adaptive prep brief — designed with ANCT architecture where each phase uses the control mode matched to its uncertainty level."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - workflow-automation
  - meeting-prep
  - calendar
  - entropy-aware
  - ANCT-designed
  - cross-platform
---

# 📋 Meeting Prep Assistant

An entropy-aware meeting preparation skill that doesn't just aggregate data —
it **thinks about why the meeting exists** and prepares you accordingly.

Most meeting prep tools treat every phase as data retrieval. They dump your
calendar, paste in attendee names, and call it done. The result is a brief
you could have written yourself in 30 seconds.

This skill is architecturally different. It was designed using **Adaptive
Narrative Control Theory (ANCT)** — each phase uses the control mode matched
to its actual uncertainty level:

- **Data pull** → DELEGATE (low entropy, just execute)
- **Relevance judgment** → NARRATE (medium entropy, requires interpretation)
- **Meeting purpose inference** → GENERATE → NARRATE (high entropy, requires exploring hypotheses then compressing)
- **Brief output** → adapts format to the meeting's entropy level

**The insight:** The highest-value phase — "what is this meeting *really* about?" —
is the one most tools skip entirely.

---

## 🧠 Core Philosophy

- **Prep is inference, not aggregation** — pulling data is step 1 of 6, not the whole job
- **Meetings have entropy levels** — a recurring standup needs a bullet list, a skip-level needs deep framing
- **Purpose is the product** — the most valuable sentence in the brief is "what this meeting is really about"
- **Format follows entropy** — low-entropy meetings get quick briefs, high-entropy meetings get deep briefs
- **Better to surface one insight than ten facts** — synthesis over volume

---

## 🏗️ ANCT Architecture

This skill was designed with the adaptive-workflow-architect meta-skill.
Here is its entropy profile and mode map:

```
Phase:      1          2          3          4          5            6
Entropy:    E1         E2         E3         E3         E4           E3→E2
Mode:       DELEGATE   DELEGATE   NARRATE    NARRATE    GEN→NAR      NAR→DEL

            pull       look up    select     prioritize  infer real   write
            metadata   attendees  relevant   open items  purpose      the brief
                                  notes                  (3→1)
```

### Mode Transition Diagram

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ DELEGATE  │→│ DELEGATE  │→│ NARRATE   │→│ NARRATE   │
│ Pull      │  │ Lookup    │  │ Select    │  │ Prioritize│
│ metadata  │  │ attendees │  │ relevant  │  │ open      │
│           │  │           │  │ notes     │  │ items     │
│ E1        │  │ E2        │  │ E3        │  │ E3        │
└──────────┘  └──────────┘  └────┬─────┘  └────┬─────┘
                                  │              │
                 if empty → GENERATE    if empty → GENERATE
                            infer                  predict
                            context                questions

┌──────────────────────┐  ┌──────────────────────┐
│ GENERATE → NARRATE   │→│ NARRATE → DELEGATE    │
│ Assess real purpose   │  │ Write the brief       │
│ 3 hypotheses → pick 1 │  │ Format adapts to      │
│                       │  │ meeting entropy level  │
│ ⚡ COMPRESSION        │  │                       │
│ CHECKPOINT: 1-sentence│  │                       │
│ purpose required      │  │                       │
└──────────────────────┘  └──────────────────────┘
```

---

## 📥 Intake: Customize This Skill

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{MEETING_IDENTIFIER}}` | Calendar event link, title, or description | string | Yes | — |
| `{{CALENDAR_SOURCE}}` | Where your calendar lives | choice: outlook, google, ical, manual | Yes | outlook |
| `{{NOTE_SOURCES}}` | Where past meeting notes live | list: email, docs, wiki, notion, markdown, none | Yes | — |
| `{{TASK_SOURCES}}` | Where open items / action items live | list: jira, asana, todoist, email, none | No | none |
| `{{RELATIONSHIP_CONTEXT}}` | Any known context about attendees (roles, dynamics, recent interactions) | text | No | — |
| `{{YOUR_ROLE}}` | Your role in this meeting (presenter, participant, decision-maker, observer) | choice | No | participant |
| `{{PREP_DEPTH}}` | How deep should the prep go? | choice: quick, standard, deep | No | standard |

---

## Phase 1: EXTRACT MEETING METADATA
**Control Mode: DELEGATE** | **Entropy: E1 (Deterministic)**

This is pure data pull. No judgment. Execute the pattern.

### Actions
1. Pull from `{{CALENDAR_SOURCE}}`:
   - Meeting title
   - Date, time, duration
   - Attendee list (names + emails)
   - Agenda / description (if present)
   - Recurrence pattern (one-time, weekly, monthly, ad-hoc)
   - Meeting series history (how many past occurrences)
   - Location / video link

2. Classify meeting recurrence:
   - **Recurring** → there's history to pull (Phase 3 matters)
   - **First-time** → no history, Phase 5 (purpose inference) becomes critical
   - **Ad-hoc** → someone called this for a reason — Phase 5 is highest priority

### Exit Condition
All metadata fields populated. If agenda is blank, flag for Phase 5
(purpose inference becomes more important).

### Output
```markdown
**Meeting:** [title]
**When:** [date, time, duration]
**Recurrence:** [pattern]
**Attendees:** [count] — [names]
**Agenda:** [text or "None provided"]
**Series history:** [N previous meetings]
```

---

## Phase 2: IDENTIFY ATTENDEES + RELATIONSHIPS
**Control Mode: DELEGATE** | **Entropy: E2 (Procedural)**

Same lookup process every time, different people.

### Actions
For each attendee, pull (from `{{RELATIONSHIP_CONTEXT}}` or available sources):

| Field | Source |
|-------|--------|
| Name + title | Calendar / directory |
| Role in this meeting | Infer from title + meeting type |
| Last interaction | Email / calendar history |
| Open threads with you | Email / task systems |
| Reporting relationship | Org chart if available |

### Escalation → NARRATE
If an attendee is **unknown** (no prior interaction, no context):
- Flag them in the brief
- In Phase 5, weight their presence as a signal about meeting purpose

### Exit Condition
Every attendee has at minimum: name, inferred role, and last interaction date (or "unknown").

### Output
```markdown
**Attendees:**
- [Name] — [Title/Role] — Last interaction: [date] — [context note]
- [Name] — [Title/Role] — ⚠️ Unknown — first meeting with this person
```

---

## Phase 3: PULL & SELECT RELEVANT NOTES
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

This is where judgment begins. You're not pulling all notes — you're
deciding which ones **matter for this specific meeting**.

### Actions
1. Query `{{NOTE_SOURCES}}` for:
   - Previous meeting notes from same series (if recurring)
   - Notes mentioning attendees from Phase 2
   - Notes mentioning the meeting topic/agenda items
   - Recent notes (last 14 days) from related projects

2. **Relevance filter** (this is the NARRATE work):
   - Does this note contain decisions that are still open?
   - Does it reference commitments made by attendees?
   - Does it contain context the meeting will build on?
   - Is it recent enough to be actionable?

3. Select top 3-5 most relevant notes. For each, extract:
   - One-line summary
   - Key decisions or commitments
   - Unresolved items

### Escalation → GENERATE (if notes are sparse)
If fewer than 2 relevant notes found:
> "No substantial notes found. Based on the attendees ([names]) and
> topic ([agenda]), what context would likely exist? What has probably
> been discussed before?"

Generate inferred context rather than returning empty.

### Exit Condition
3-5 relevant notes identified with key takeaways, OR generated context
if notes don't exist.

### Output
```markdown
**Relevant Context:**
1. [Date] — [Note summary] — Key point: [decision/commitment/open item]
2. [Date] — [Note summary] — Key point: [decision/commitment/open item]
3. [Inferred] — Based on attendees and topic, likely prior context: [inference]
```

---

## Phase 4: SURFACE OPEN ITEMS
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

Not just "what's open" but "what's open that matters for THIS meeting."

### Actions
1. Query `{{TASK_SOURCES}}` for:
   - Items assigned to you related to this meeting's topic
   - Items assigned to attendees that you're involved in
   - Items mentioned in Phase 3 notes that are still open
   - Overdue items involving any attendee

2. **Prioritization** (NARRATE work):
   - Which items are the attendees likely to ask about?
   - Which items have been open long enough to create tension?
   - Which items block something the meeting will discuss?

3. Rank by relevance to this meeting. Top 3-7 items.

### Escalation → GENERATE (if no open items found)
If task systems return nothing relevant:
> "No tracked items found. Given the meeting topic and attendees,
> what questions should you be prepared to answer? What might
> someone ask you for a status on?"

Generate anticipated questions rather than returning empty.

### Exit Condition
Prioritized list of 3-7 open items, OR generated anticipated questions.

### Output
```markdown
**Open Items:**
- 🔴 [Overdue/urgent] [item] — owner: [who] — status: [status]
- 🟡 [Active] [item] — owner: [who] — likely to come up because [reason]
- 🟢 [FYI] [item] — context for discussion

**If nothing tracked:**
- ❓ Be ready to discuss: [anticipated question]
- ❓ Possible status request: [topic]
```

---

## Phase 5: ASSESS REAL MEETING PURPOSE
**Control Mode: GENERATE → NARRATE** | **Entropy: E4 (Creative)**

**This is the highest-entropy phase and the most valuable.**

The agenda says "sync" or "status update" or "discuss Q3 plan." That's
the stated purpose. The *real* purpose is often different:
- A "status update" might actually be "I need to know if I can trust this timeline"
- A "1:1" might actually be "I'm about to give you feedback"
- A "brainstorm" might actually be "I already have an answer, I want buy-in"

### GENERATE Step (expand)
Using all context from Phases 1-4, generate **3 hypotheses** about why
this meeting really exists:

```
Hypothesis 1 (surface): [What the agenda says]
Hypothesis 2 (deeper):  [What the attendee mix suggests]
Hypothesis 3 (deepest): [What the timing, recurrence, and open items suggest]
```

Signals to weigh:
- **Who called the meeting?** Their role + seniority = intent signal
- **Who's invited who isn't normally there?** New attendees = new agenda
- **What just happened?** Recent events that would trigger this meeting
- **What's the cadence delta?** A weekly that got moved to daily = urgency signal
- **Is there an agenda?** No agenda on a meeting with senior people = the topic is sensitive

### ⚡ COMPRESSION CHECKPOINT
> **You cannot proceed to Phase 6 until the 3 hypotheses are compressed
> to a single sentence:**
>
> "This meeting is really about: _______________"

### NARRATE Step (compress)
Select the most likely purpose. State it in one sentence.
Note the runner-up hypothesis as an alternative reading.

### Exit Condition
One-sentence primary purpose + one-sentence alternative reading.

### Output
```markdown
**What this meeting is really about:**
[One sentence — primary hypothesis]

**Alternative reading:**
[One sentence — second hypothesis]
```

---

## Phase 6: GENERATE THE PREP BRIEF
**Control Mode: NARRATE → DELEGATE** | **Entropy: E3 → E2**

Synthesize all phases into a prep brief. **Format adapts to meeting entropy.**

### Meeting Entropy Classification

| Signal | Low Entropy | High Entropy |
|--------|------------|--------------|
| Recurrence | Regular cadence, no changes | First-time or ad-hoc |
| Attendees | Usual group | New people, senior additions |
| Agenda | Clear, specific | Vague or missing |
| Open items | Routine updates | Overdue, tense, or escalated |
| Purpose inference | Surface matches deep | Surface and deep diverge |

### Brief Format A: Quick Prep (Low-Entropy Meeting)

For recurring meetings with familiar attendees and clear agendas.
`{{PREP_DEPTH}}` = quick, OR auto-detected low entropy.

```markdown
## [Meeting Title] — Quick Prep
**[Date] [Time] ([Duration])**

**Purpose:** [one sentence from Phase 5]

**Attendees:** [names + roles, one line]

**Your items:**
- [open item 1]
- [open item 2]

**Since last time:**
- [key change from recent notes]
- [key change from recent notes]

**One thing to know going in:**
[single most important context point]
```

### Brief Format B: Standard Prep (Medium-Entropy Meeting)

For meetings with some uncertainty — mixed attendees, partially clear agenda.
`{{PREP_DEPTH}}` = standard, OR auto-detected medium entropy.

```markdown
## [Meeting Title] — Prep Brief
**[Date] [Time] ([Duration])**

**What this meeting is really about:**
[one sentence from Phase 5]

**Attendees:**
- [Name] — [Role] — [one-line context]
- [Name] — [Role] — [one-line context]

**Relevant context:**
- [Key point from notes 1]
- [Key point from notes 2]

**Open items likely to surface:**
- 🔴 [urgent item]
- 🟡 [active item]

**Your position going in:**
[What do you think/want/need from this meeting?]
```

### Brief Format C: Deep Prep (High-Entropy Meeting)

For first-time meetings, skip-level conversations, strategy sessions,
meetings with vague agendas and senior attendees.
`{{PREP_DEPTH}}` = deep, OR auto-detected high entropy.

```markdown
## [Meeting Title] — Deep Prep
**[Date] [Time] ([Duration])**

**What this meeting is really about:**
[one sentence — primary hypothesis from Phase 5]

**Alternative reading:**
[one sentence — what else this could be about]

**Key relationships in the room:**
- [Name] — [Role] — [dynamic: ally, new stakeholder, decision-maker, observer]
- [Name] — ⚠️ Unknown — [what their presence might signal]

**Context you need:**
- [Synthesized point from notes — not a raw note, a takeaway]
- [Synthesized point from notes]
- [Inferred context if no notes exist]

**What you should be ready for:**
- [Anticipated question or topic 1]
- [Anticipated question or topic 2]
- [Uncomfortable possibility to be aware of]

**Open threads that may surface:**
- 🔴 [item + whose it is + why it's tense]
- 🟡 [item + status + what's expected of you]

**Your position:**
[What do you think going in? What do you want out of this meeting?]
[What would success look like when it ends?]

**One sentence to have ready:**
[If someone puts you on the spot, this is your grounding statement]
```

---

## ⚠️ Anti-Patterns

```
MEETING PREP ANTI-PATTERNS (from ANCT failure mode analysis):

✗ "Data dump" brief
  Lists attendees, pastes raw notes, shows all open items.
  No synthesis. No purpose inference.
  → ANCT diagnosis: all-DELEGATE, skipped NARRATE and GENERATE phases

✗ "Every meeting gets the same brief"
  Recurring standup gets the same format as a board prep.
  → ANCT diagnosis: flat entropy assumption, no format adaptation

✗ "First hypothesis accepted"
  "It says 'status update' so it's a status update."
  → ANCT diagnosis: premature compression, skipped GENERATE in Phase 5

✗ "No brief because no notes"
  Notes don't exist, so the skill returns nothing.
  → ANCT diagnosis: missing escalation, should GENERATE inferred context

✗ "20-item open item list"
  Everything remotely related is included. No prioritization.
  → ANCT diagnosis: DELEGATE applied to E3 phase, no NARRATE filter

CORRECT PATTERNS:

✓ Phase 5 always runs (even for "obvious" meetings)
✓ Brief format matches meeting entropy level
✓ Empty data triggers generation, not silence
✓ Open items filtered to "what THIS meeting will care about"
✓ One sentence of purpose is worth more than ten facts
```

---

## 📚 Example Applications

| Meeting Type | Entropy | Brief Format | Key ANCT Insight |
|-------------|---------|--------------|------------------|
| **Weekly team standup** | E1-E2 | Quick | Phase 5 still runs but output is one line. Value is in surfacing what changed since last time. |
| **1:1 with your manager** | E3 | Standard | Phase 5 matters: is this a check-in or a course correction? Attendee history is the signal. |
| **Skip-level with VP** | E4 | Deep | Phase 5 is critical. "Why is this happening now?" The agenda is never the real agenda. |
| **Cross-functional kickoff** | E4 | Deep | New attendees = high entropy. Phase 2 (relationships) and Phase 5 (purpose) carry the prep. |
| **Recurring project sync** | E2 | Quick | Low ceremony. Value is in open items that are overdue or about to slip. |
| **Feedback/review session** | E4 | Deep | Phase 5 GENERATE must explore: is this developmental, evaluative, or political? Changes your prep entirely. |

---

## 🌐 Platform Notes

| Platform | How to Use |
|----------|------------|
| **Any LLM** | Paste this SKILL.md as context. Provide meeting details and ask for a prep brief. |
| **With calendar integration** | Connect to Outlook/Google Calendar API for automatic Phase 1-2. |
| **CLI tools** | Copy to skills directory; invoke with `/skill meeting-prep-assistant` |
| **IDE extensions** | Reference in agent config for pre-meeting prep sessions |

---

## Compliance

- **PII Risk:** Medium. Meeting attendees, calendar data, and notes may contain
  names, emails, and organizational context. All processing is session-local.
  No data is stored by the skill itself. Users should not paste sensitive meeting
  content into public LLM interfaces.
- **Model Recommendation:** Sonnet for standard prep (Phase 5 inference benefits
  from strong reasoning). Haiku for quick prep on low-entropy recurring meetings.
- **Human Oversight:** The brief is a proposal. The user reads it, adjusts their
  framing, and walks into the meeting with their own judgment — not the agent's.

---

## Design Credit

This skill's architecture was designed using the
[adaptive-workflow-architect](../adaptive-workflow-architect/) meta-skill,
applying Adaptive Narrative Control Theory (ANCT) to map each phase to its
optimal control mode based on entropy level.
