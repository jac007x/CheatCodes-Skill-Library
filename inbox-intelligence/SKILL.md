---
name: inbox-intelligence
description: "Entropy-aware communications intelligence skill that rapidly triages email and Teams messages, separates signal from noise, builds a persistent knowledge compendium with cross-referenced topics, and produces action-required lists — designed to take 300 unread messages to zero-anxiety in under an hour. The compendium becomes a living knowledge base that any agent can query, grows smarter through self-improvement, and feeds downstream skills like meeting-prep-assistant."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - workflow-automation
  - email
  - teams
  - inbox-triage
  - knowledge-management
  - compendium
  - entropy-aware
  - ANCT-designed
  - self-improving
  - cross-platform
---

# 📬 Inbox Intelligence

A communications intelligence skill that turns your overflowing inbox into
three things:

1. **An action list** — emails/messages you actually need to respond to, ranked by urgency
2. **A knowledge compendium** — everything you should know, organized by topic, cross-referenced, searchable by any agent
3. **Peace of mind** — the 280 emails that were noise are gone; the 20 that matter are visible

This is not an email summarizer. It's a **knowledge extraction and triage system**
that treats your inbox as an unstructured data stream, applies entropy-aware
processing to separate signal from noise, and builds a persistent, growing
intelligence layer that makes you smarter over time.

**Design target:** 300 unread → fully triaged in under 1 hour.

---

## 🧠 Core Philosophy

- **Your inbox is not a task list** — it's an unstructured data stream. Treat it like one.
- **Triage is not reading** — triage is classification. Reading happens later, only for what matters.
- **The compendium outlives the email** — an email gets archived; the knowledge it contained stays findable forever.
- **Links are first-class citizens** — every compendium entry links back to the source message and preserves attachment links.
- **The system gets smarter** — topic connections, prediction patterns, and cross-references improve with every triage session.
- **Manual reads count too** — emails you've already handled can still be logged to the compendium. Knowledge capture is independent of triage status.
- **Never make me think about where info is** — if it came through email or Teams, the compendium should have it. Ask the agent, get the answer.

---

## 🏗️ ANCT Architecture

### Entropy Profile

```
Phase:      1          2          3          4          5          6          7
Entropy:    E1         E2         E3         E4         E3         E2         E4→E3
Mode:       DELEGATE   DELEGATE   NARRATE    GEN→NAR    NARRATE    DELEGATE   GEN→NAR

            pull       classify   triage     extract    build      produce    learn &
            messages   by type    & rank     knowledge  compendium action     connect
                                                        entries    list
```

### Why This Entropy Map

| Phase | Why This Entropy Level |
|-------|----------------------|
| 1. Pull messages | E1 — API call, zero judgment |
| 2. Classify | E2 — pattern matching (newsletter vs thread vs 1:1 vs FYI) |
| 3. Triage & rank | E3 — requires judgment: what actually needs a response? |
| 4. Extract knowledge | E4 — creative: what's worth knowing? What connects to what? |
| 5. Build compendium | E3 — analytical: organize, cross-reference, link |
| 6. Produce action list | E2 — structured output from triage decisions |
| 7. Learn & connect | E4→E3 — discover patterns, predict needs, self-improve |

---

## 📥 Intake: Customize This Skill

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{MESSAGE_SOURCES}}` | Where to pull from | list: outlook, gmail, teams, slack | Yes | outlook, teams |
| `{{COMPENDIUM_PATH}}` | Where the compendium lives (Markdown file) | file-path | Yes | `./COMPENDIUM.md` |
| `{{LOOKBACK_WINDOW}}` | How far back to scan | choice: today, 3-days, 7-days, 14-days, 30-days | No | 7-days |
| `{{KNOWN_PRIORITIES}}` | People or topics that are always high-priority | list | No | — |
| `{{NOISE_PATTERNS}}` | Newsletters, auto-notifications, or senders to always skip | list | No | — |
| `{{TOPIC_TAXONOMY}}` | Pre-defined topic categories for the compendium | list | No | auto-detected |
| `{{TRIAGE_MODE}}` | How aggressive should noise filtering be? | choice: conservative, standard, aggressive | No | standard |
| `{{INCLUDE_HANDLED}}` | Also process emails you've already read/responded to for compendium capture? | bool | No | true |
| `{{ATTACHMENT_HANDLING}}` | How to handle attachments | choice: links-only, scan-and-summarize, full-extract | No | scan-and-summarize |

---

## Phase 1: PULL MESSAGES
**Control Mode: DELEGATE** | **Entropy: E1 (Deterministic)**

Pure data retrieval. No judgment.

### Actions

1. Connect to `{{MESSAGE_SOURCES}}`
2. Pull all messages within `{{LOOKBACK_WINDOW}}`
3. For each message, capture:

```yaml
message:
  id: unique-id
  source: outlook | teams | gmail | slack
  type: email | teams-chat | teams-channel | thread-reply
  from: sender name + address
  to: recipients
  cc: cc list
  date: timestamp
  subject: subject line
  body_preview: first 200 chars
  has_attachments: bool
  attachment_names: list
  attachment_links: list  # preserve direct links
  thread_id: conversation thread ID
  is_read: bool
  is_replied: bool
  importance: sender-flagged priority
  channel: Teams channel name (if applicable)
```

4. If `{{INCLUDE_HANDLED}}` is true, pull read messages too (flagged `is_read: true`)
5. Deduplicate: collapse thread replies into conversation objects

### Exit Condition
All messages pulled, deduplicated, structured. Count logged.

### Output
```
Pulled [N] messages ([X] unread, [Y] read) from [sources] over [window]
Collapsed into [M] conversations
```

---

## Phase 2: CLASSIFY BY TYPE
**Control Mode: DELEGATE** | **Entropy: E2 (Procedural)**

Pattern-match each message into a category. Same rules every time.

### Classification Taxonomy

| Category | Signal | Examples |
|----------|--------|---------|
| **🔴 Direct request** | You're in TO, specific ask in body, question directed at you | "Can you send me...", "Please review...", "What's the status of..." |
| **🟡 FYI — important** | Relevant to your work, from key people, mentions your projects | Leadership updates, project announcements, policy changes |
| **🟢 FYI — peripheral** | Tangentially relevant, good to know but not actionable | Org-wide announcements, team newsletters, event invites |
| **⚪ Noise** | Auto-notifications, marketing, system alerts, distribution lists you don't need | Build notifications, HR system emails, newsletter digests |
| **🔵 Thread / conversation** | Reply chain you're part of, may or may not need your input | Ongoing discussions, decision threads, FYI cc chains |
| **📎 Document share** | Primary content is an attachment or link, not the email body | "See attached", shared drive links, document reviews |

### Classification Rules

```
IF sender in {{KNOWN_PRIORITIES}} → at minimum 🟡, check for 🔴
IF sender in {{NOISE_PATTERNS}} → ⚪ (skip)
IF you're only in CC and body has no question → 🟢 or ⚪
IF body contains "?" directed at you → 🔴
IF subject contains "FYI" or "no action needed" → 🟡 or 🟢
IF has_attachments and body is short → 📎
IF is thread_reply and you're not addressed → 🔵
```

### Exit Condition
Every message has a category. Counts per category logged.

### Output
```
Classification: 🔴 [N] direct requests | 🟡 [N] important FYI | 🟢 [N] peripheral
               ⚪ [N] noise (auto-archived) | 🔵 [N] threads | 📎 [N] document shares
```

---

## Phase 3: TRIAGE & RANK
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

This is where judgment begins. Not everything marked 🔴 is equally urgent.
Not everything marked 🟢 is equally disposable.

### Triage Dimensions

For each non-noise message, score on three dimensions:

| Dimension | Question | Scale |
|-----------|----------|-------|
| **Urgency** | When does this need a response? | 1 (whenever) → 5 (today) |
| **Importance** | What happens if I ignore this? | 1 (nothing) → 5 (real consequences) |
| **Knowledge value** | Does this contain something I should know? | 1 (no) → 5 (critical intelligence) |

### Triage Matrix

```
              High importance     Low importance
High urgency  → RESPOND NOW      → QUICK REPLY
Low urgency   → RESPOND SOON     → LOG TO COMPENDIUM ONLY
```

Messages with high knowledge value (3+) go to Phase 4 regardless of urgency.

### Ranking
Produce a ranked action list:
1. Respond Now (urgency 4-5 + importance 4-5)
2. Respond Soon (urgency 3+ OR importance 3+)
3. Quick Reply (urgency high but importance low — "thanks", "got it", "acknowledged")
4. Read & Archive (no response needed, low knowledge value)
5. Skip (noise — already filtered in Phase 2)

### Escalation → GENERATE
If triage is ambiguous (can't determine urgency/importance from preview):
> Read the full message body. If still ambiguous, flag for human decision
> with a one-line summary and ask: "Respond, log, or skip?"

### Exit Condition
Every message has urgency + importance + knowledge scores. Ranked action list produced.

---

## Phase 4: EXTRACT KNOWLEDGE
**Control Mode: GENERATE → NARRATE** | **Entropy: E4 (Creative)**

**The highest-value phase.** This is where emails become knowledge.

For every message with knowledge value ≥ 2, extract:

### Knowledge Extraction Framework

```yaml
knowledge_entry:
  # === Source ===
  source_id: message-id
  source_type: email | teams-message | teams-channel
  source_link: "deep link to original message"
  source_date: timestamp
  source_from: sender

  # === Content ===
  topic: primary topic (from taxonomy or auto-detected)
  secondary_topics: list of related topics
  summary: 2-3 sentence extraction of what matters
  key_facts: bulleted list of specific facts, numbers, dates, decisions
  quotes: exact quotes worth preserving (with attribution)
  sentiment: positive | neutral | negative | urgent | cautionary

  # === Attachments ===
  attachments:
    - name: filename
      link: "direct link to attachment"
      type: document | spreadsheet | presentation | image | other
      summary: 1-2 sentence description of attachment content (if scanned)
      key_data: extracted data points (if full-extract mode)

  # === Connections ===
  related_entries: list of compendium entries this connects to
  people_involved: who is relevant to this knowledge
  decisions_made: any decisions documented in this message
  action_items: commitments made by anyone (not just you)
  open_questions: unresolved questions mentioned
  deadlines: any dates or timelines mentioned

  # === Meta ===
  confidence: high | medium | low (how sure are we about the extraction)
  compendium_priority: 1-5 (how important is this for long-term reference)
```

### GENERATE Step: Attachment Processing

Based on `{{ATTACHMENT_HANDLING}}`:

| Mode | What Happens |
|------|-------------|
| **links-only** | Preserve attachment link and filename. No content scan. |
| **scan-and-summarize** | Open attachment, extract key points (1-3 sentences per doc). Preserve link. |
| **full-extract** | Deep scan: extract all data points, tables, key findings. Preserve link. Add full summary to compendium. |

### GENERATE Step: Topic Detection

If `{{TOPIC_TAXONOMY}}` is not provided, auto-detect topics:

1. Scan all extracted summaries for recurring themes
2. Cluster by similarity
3. Propose a taxonomy (user can refine)
4. Assign each entry to 1 primary + 0-3 secondary topics

### ⚡ COMPRESSION CHECKPOINT
> Every knowledge entry must have:
> - A summary ≤ 3 sentences
> - At least 1 key fact
> - A source link
> - A topic assignment
>
> If any field is empty, the entry is incomplete. Re-examine the source.

### Escalation → Human
If content is ambiguous or potentially sensitive:
> "This message discusses [topic]. Confidence is low on extraction.
> Should I log it to the compendium? [Yes / Skip / Let me read it first]"

### Exit Condition
Knowledge entries produced for all messages with knowledge value ≥ 2.
Attachments processed per `{{ATTACHMENT_HANDLING}}` mode.

---

## Phase 5: BUILD COMPENDIUM
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

The compendium is a **persistent, growing Markdown knowledge base** stored at
`{{COMPENDIUM_PATH}}`. Every triage session adds to it. It never resets — it
accumulates.

### Compendium Structure

```markdown
# Communications Compendium
> Last updated: [timestamp]
> Total entries: [N] | Topics: [N] | Sources: [N]

## Table of Contents
- [Topic 1](#topic-1) ([N] entries)
- [Topic 2](#topic-2) ([N] entries)
- ...

---

## Topic 1: [Topic Name]
> [N] entries | Last updated: [date] | Key people: [names]

### [Entry Title] — [Date]
**Source:** [sender] via [email|teams] | [link to original]
**Summary:** [2-3 sentences]
**Key facts:**
- [fact 1]
- [fact 2]
**Attachments:** [filename](link) — [1-line description]
**Decisions:** [if any]
**Open questions:** [if any]
**Related:** [links to related compendium entries]

### [Entry Title] — [Date]
...

---

## Topic 2: [Topic Name]
...

---

## Cross-Reference Index
| Topic | Related Topics | Key People | Recent Activity |
|-------|---------------|------------|-----------------|
| [topic] | [topic, topic] | [names] | [date of last entry] |

---

## People Index
| Person | Topics They Appear In | Last Interaction | Open Items With Them |
|--------|----------------------|------------------|---------------------|
| [name] | [topics] | [date] | [items] |

---

## Timeline
| Date | Topic | Event | Source |
|------|-------|-------|--------|
| [date] | [topic] | [what happened] | [link] |

---

## Decisions Log
| Date | Decision | Made By | Context | Source |
|------|----------|---------|---------|--------|
| [date] | [decision] | [who] | [topic] | [link] |
```

### Compendium Update Rules

1. **New entries** append under their topic section
2. **Existing topics** get new entries added chronologically
3. **New topics** get a new section created
4. **Cross-references** are updated when related entries are added
5. **People index** is updated when new people appear in entries
6. **Timeline** gets a new row for significant events
7. **Decisions log** captures any decisions mentioned in messages

### Deduplication
If a knowledge entry covers the same information as an existing entry:
- Update the existing entry with new details
- Add the new source link as an additional reference
- Don't create a duplicate

### Exit Condition
All Phase 4 knowledge entries written to compendium. Indexes updated.
Cross-references current.

---

## Phase 6: PRODUCE ACTION LIST
**Control Mode: DELEGATE** | **Entropy: E2 (Procedural)**

Structured output from triage decisions. Template work.

### Action List Output

```markdown
# Inbox Triage — [Date]
> Processed: [N] messages | Time: [duration]
> Sources: [email, teams, ...]

## 🔴 Respond Now ([N])
| # | From | Subject | Why It's Urgent | Source |
|---|------|---------|-----------------|--------|
| 1 | [name] | [subject] | [one-line reason] | [link] |
| 2 | ... | ... | ... | ... |

**Suggested responses:** _(for each, a 1-2 sentence draft if possible)_
1. → [draft response or response strategy]
2. → ...

## 🟡 Respond Soon ([N])
| # | From | Subject | By When | Source |
|---|------|---------|---------|--------|
| 1 | [name] | [subject] | [suggested deadline] | [link] |

## ⚡ Quick Reply ([N])
| # | From | Subject | Suggested Reply | Source |
|---|------|---------|-----------------|--------|
| 1 | [name] | [subject] | "Thanks, acknowledged" | [link] |

## 📚 Logged to Compendium ([N])
| Topic | Entries Added | Key Takeaway |
|-------|-------------|--------------|
| [topic] | [N] | [one-line summary of what was learned] |

## ⚪ Archived as Noise ([N])
[count] messages auto-archived. No action needed.

## 📊 Session Stats
- Total processed: [N]
- Response needed: [N] (🔴 [n] + 🟡 [n] + ⚡ [n])
- Knowledge captured: [N] compendium entries
- New topics discovered: [N]
- Attachments processed: [N]
- Noise filtered: [N] ([%] of total)
```

---

## Phase 7: LEARN & CONNECT
**Control Mode: GENERATE → NARRATE** | **Entropy: E4 → E3**

**This phase is what makes the skill get smarter over time.**

### 7A: Cross-Reference Discovery (GENERATE)

After each triage session, scan the compendium for connections:

1. **Topic clustering:** Are any topics converging? (e.g., "Budget" entries
   and "Hiring" entries are both about the same headcount decision)
2. **People overlap:** Who appears across multiple topics? (signals
   who the key connectors/decision-makers are)
3. **Timeline patterns:** Is a topic accelerating? (more entries in
   shorter timeframes = something is happening)
4. **Decision chains:** Do earlier decisions connect to later ones?

### 7B: Predictive Signals (GENERATE)

Based on compendium history, surface:

```markdown
## Predictions & Reminders

### Things You'll Probably Need Soon
- [Topic X] has had [N] entries in [timeframe]. You'll likely be asked
  about this in your next [meeting with person].
  → Compendium summary: [link to topic section]

### Connections You Might Not See
- [Topic A] and [Topic B] are converging: [evidence].
  Consider preparing a unified view.

### Stale Topics (No Updates in 14+ Days)
- [Topic] last updated [date] — still relevant? Open items remain:
  [list of open items from compendium]

### People to Follow Up With
- [Person] has [N] open items across [topics]. Last interaction: [date].
```

### 7C: Self-Improvement (NARRATE — compress learnings)

After each session, log:

```yaml
session_learning:
  timestamp: [date]
  messages_processed: [N]
  triage_accuracy: [how many classifications did the user override?]
  missed_signals: [any important messages initially classified as noise?]
  compendium_health:
    topics_growing: [list]
    topics_stale: [list]
    cross_references_added: [N]
  improvement_proposals:
    - "Sender [X] was classified as noise but user flagged as important.
       Add to {{KNOWN_PRIORITIES}}."
    - "Topic [Y] is fragmenting into sub-topics. Propose restructure."
    - "[N] messages about [topic] had no attachment scanning. Switch to
       scan-and-summarize for this sender."
```

**These learnings feed back into the next session:**
- Classification rules improve (fewer misclassifications)
- Topic taxonomy evolves (new topics emerge, old ones merge)
- Priority patterns sharpen (the system learns who matters to you)
- Prediction accuracy improves (correlation patterns strengthen)

---

## 🔗 Integration: Meeting Prep Assistant

The compendium is a **direct input to meeting-prep-assistant**.

When meeting-prep-assistant runs Phase 3 (Pull Relevant Notes) and Phase 5
(Assess Real Purpose), it can query the compendium:

```
meeting-prep-assistant Phase 3:
  "What does the compendium have on [meeting topic]?"
  → Returns: all entries under that topic, with links, decisions, open items

meeting-prep-assistant Phase 5:
  "What's the recent trajectory of [topic]?"
  → Returns: timeline entries, acceleration signals, predictions

meeting-prep-assistant Phase 2:
  "What do I know about [attendee]?"
  → Returns: people index entry, topics they appear in, last interaction, open items
```

**Result:** Meeting prep briefs become dramatically richer because they pull
from structured knowledge, not just raw email search.

### Bidirectional Value

| From | To | Value |
|------|----|-------|
| **inbox-intelligence → meeting-prep** | Compendium provides rich context for prep briefs | Briefs cite specific emails, decisions, timelines |
| **meeting-prep → inbox-intelligence** | Meeting outcomes update the compendium | Post-meeting notes feed back as new knowledge entries |

---

## 🔄 Operational Modes

### Mode 1: Full Triage (Default)
Run all 7 phases. Process entire lookback window. Ideal for catching up
on a backlog.

**When:** Weekly inbox cleanup, Monday morning, after PTO, after ignoring
inbox for too long.

**Target:** 300 unread → triaged in under 1 hour.

### Mode 2: Quick Scan
Run Phases 1-3 + Phase 6 only. Skip knowledge extraction and compendium.
Produces action list fast.

**When:** Mid-day check, looking for fires only.

**Target:** 50 new messages → action list in 5 minutes.

### Mode 3: Compendium Catch-Up
Run Phase 4-5 only against already-read messages. Captures knowledge
from emails you've handled but didn't log.

**When:** You've been manually reading emails and want to capture the
knowledge into the compendium retroactively.

**Target:** Scan last 7 days of read messages → compendium updated.

### Mode 4: Compendium Query
No triage. Just query the existing compendium.

**When:** "What do I know about [topic]?" or "Summarize everything from
[person] in the last month."

**Target:** Answer in seconds from structured compendium data.

### Mode 5: Learning Review
Run Phase 7 only. Review cross-references, predictions, and improvement
proposals from the compendium.

**When:** Weekly reflection, pre-planning, or when you sense a topic
is getting complex and want to see the full picture.

---

## ⚠️ Anti-Patterns

```
INBOX INTELLIGENCE ANTI-PATTERNS:

✗ "Summarize everything"
  Summarizing 300 emails produces a 300-item list. That's not triage.
  → ANCT diagnosis: NARRATE applied to E1 work. Classify first, then
    only narrate what survived triage.

✗ "Read everything to triage it"
  Reading full emails before classifying is O(n) on the wrong step.
  → ANCT diagnosis: Over-investing in Phase 3. Use subject + sender +
    preview for classification. Full read only on Phase 4 knowledge extraction.

✗ "Flat compendium"
  Dumping all summaries into one file with no structure.
  → The compendium must have: topic sections, cross-references, people
    index, timeline, decisions log. Structure IS the value.

✗ "Compendium as archive"
  Storing everything verbatim from emails.
  → The compendium stores extracted knowledge, not email text. Summaries,
    key facts, decisions, and links. Not copy-paste.

✗ "No links back to source"
  Knowledge entries without links to the original message.
  → Every entry must link back. The compendium is an index, not a replacement.

✗ "One-time use"
  Running triage once and never building on it.
  → The value is compound. Each session adds knowledge, improves
    classification, and strengthens predictions. Use it consistently.

CORRECT PATTERNS:

✓ Classify first (DELEGATE), judge second (NARRATE), extract third (GENERATE)
✓ Compendium is structured, indexed, and cross-referenced
✓ Every entry has a source link
✓ Attachments are at minimum linked, ideally scanned
✓ Phase 7 runs every session — the system learns
✓ Manual reads still get logged (INCLUDE_HANDLED = true)
✓ Compendium feeds meeting-prep-assistant and any querying agent
```

---

## 📚 Example Applications

| Context | Message Volume | Key ANCT Insight |
|---------|---------------|------------------|
| **Executive assistant** | 500+/week | Phase 2 classification is critical. Most messages are delegatable. Phase 4 extracts decisions only the EA would notice. |
| **Project manager** | 200+/week | Phase 5 compendium cross-references surface project risks that individual emails don't reveal. |
| **People leader** | 150+/week | Phase 7 predictions: "3 messages about [team member] frustration this month — pattern emerging." |
| **Individual contributor** | 100+/week | Mode 2 (quick scan) is the daily driver. Full triage weekly. Compendium catches context they'd otherwise lose. |
| **Consultant / multi-client** | 300+/week | Topic taxonomy maps to clients. Compendium becomes the client knowledge base. |
| **Post-PTO catch-up** | 300+ backlog | Mode 1 full triage. The nightmare scenario this skill was designed for. |

---

## 🌐 Platform Notes

| Platform | How to Use |
|----------|------------|
| **With email/Teams integration** | Connect to Outlook/Gmail + Teams API. Fully automated pull + triage. |
| **Any LLM (manual)** | Export inbox to text/CSV. Paste batches for triage. Build compendium manually. |
| **CLI tools** | Copy to skills directory; invoke with `/skill inbox-intelligence` |
| **Paired with meeting-prep** | Run inbox-intelligence first, then meeting-prep-assistant queries the compendium |

---

## Compliance

- **PII Risk:** High. Email content, sender names, organizational context, attachments.
  All processing is session-local. The compendium is stored at `{{COMPENDIUM_PATH}}`
  which should be in a **private, secure location** (private repo, local machine,
  encrypted drive). Never store the compendium in a public repo.
- **Model Recommendation:** Sonnet for full triage (Phase 3-4 judgment + extraction).
  Haiku for Mode 2 quick scan. Opus for Phase 7 deep cross-reference analysis.
- **Human Oversight:** Triage decisions are proposals. The user reviews the action
  list before responding. The compendium is additive — the user can edit, correct,
  or remove entries at any time. Noise classification can be overridden.

---

## Design Credit

This skill's architecture was designed using the
[adaptive-workflow-architect](../adaptive-workflow-architect/) meta-skill,
applying Adaptive Narrative Control Theory (ANCT) to map each phase to its
optimal control mode based on entropy level. It integrates with
[meeting-prep-assistant](../meeting-prep-assistant/) as a knowledge source
for meeting preparation briefs.
