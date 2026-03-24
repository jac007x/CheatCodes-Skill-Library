---
name: decision-memo-distiller
description: "Distills raw meeting notes, threads, or conversations into structured decision memos with owners, deadlines, and open items."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - meetings
  - decisions
  - documentation
  - summarization
model_recommendation: sonnet
risk_level: low
---

# 🎯 Decision Memo Distiller

> Extract what was actually decided, who owns it, and what's still open — from any raw meeting artifact.

## Core Philosophy

A meeting without a decision memo is a meeting where everyone left with a different understanding of what happened. In high-velocity organizations, this is not an edge case — it is the default. Someone sends recap notes that read like a transcript. Someone else sends a bullet-point summary that omits three of the five decisions. A week later, two teams are executing against contradictory understandings of who owns what, and no one can reconstruct where the disagreement started.

The decision memo exists to prevent that failure. Not a summary — a structured artifact that distinguishes between what was decided and what was discussed, who owns each action and by when, what was deliberately deferred and why, and what remains genuinely unresolved. The distinction between these four categories is everything. Discussion masquerading as a decision is a liability. A deferred item without a record is a forgotten item. An open question that gets closed prematurely because it was uncomfortable to leave open will resurface as a crisis.

This skill applies a disciplined classification process before any writing begins. Every piece of content in the source material is categorized before the memo is assembled. The classification work is the hard work; the memo assembly is mechanical. Getting the classification right requires analytical judgment — this is where the NARRATE phases in the ANCT architecture carry the most weight. The phases are designed so that the output is not a summary of the meeting but a precise record of the meeting's outputs.

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake Raw Material | E1 – Deterministic | DELEGATE | Structured collection of source and context; no interpretation yet |
| 2. Classify Content | E3 – Analytical | NARRATE | Requires judgment: decision vs. discussion vs. deferred vs. open is not always obvious |
| 3. Extract Decisions | E3 – Analytical | NARRATE | Identifying what constitutes a decision, who made it, and what it implies requires interpretation |
| 4. Structure Memo | E2 – Procedural | DELEGATE | Assembly of classified elements into a fixed-format memo; follows a defined pattern |
| 5. Validate Completeness | E3 – Analytical | NARRATE | Requires judgment to identify gaps: missing owners, implicit assumptions, unresolved ambiguities |

---

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{SOURCE_MATERIAL}}` | Raw meeting notes, email thread, transcript, or Slack export | string | Yes | — |
| `{{OBJECTIVE}}` | What the meeting or discussion was convened to accomplish | string | Yes | — |
| `{{AUDIENCE}}` | Who receives the final memo and at what level of detail | string | Yes | — |
| `{{OWNER}}` | Person responsible for the memo's accuracy and distribution | string | Yes | — |
| `{{DEADLINE}}` | Distribution deadline for the memo | string | No | — |
| `{{KNOWN_FACTS}}` | Pre-established context that informs interpretation of the source material | string | No | — |
| `{{SENSITIVITY_LEVEL}}` | Confidentiality level: public, internal, sensitive, restricted | string | No | internal |

---

## ⚙️ Phases

### Phase 1: INTAKE RAW MATERIAL
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Collect and organize all inputs without interpretation. The source material is captured as-is. Context variables are structured into a working brief. No edits, no classifications, no opinions yet — this phase is purely organizational.

**Process:**
1. Capture `{{SOURCE_MATERIAL}}` in full. Note: source type (raw notes / email thread / meeting transcript / Slack/Teams export / hybrid), approximate length, and whether it appears to cover one meeting or multiple.
2. Record `{{OBJECTIVE}}`: what was the meeting or discussion convened to accomplish? If unstated, note as "not specified — to be inferred from content in Phase 2."
3. Record `{{AUDIENCE}}`, `{{OWNER}}`, `{{DEADLINE}}`, `{{KNOWN_FACTS}}`, and `{{SENSITIVITY_LEVEL}}`.
4. Identify all named participants from the source material. Note names, roles (if stated or inferable), and any attribution patterns (e.g., "who tends to own decisions vs. who tends to discuss").
5. Identify the meeting type from source content: single-topic decision meeting, multi-agenda working session, async thread with no formal meeting, standing/recurring review, or hybrid.
6. Flag any structural problems with the source: missing time context, unattributed statements, apparent gaps in the record, or sections that are clearly incomplete.
7. Produce an intake summary. No classifications yet.

**Output:**
```
INTAKE SUMMARY
Source type: [notes / thread / transcript / export / hybrid]
Source length: [approximate — short (<500 words) / medium / long (>2000 words)]
Meeting type: [decision / working session / async / standing review / hybrid]
Meeting objective: [stated or "not specified — inferred from content"]
Participants: [names + roles]
Owner: [who receives and distributes memo]
Audience: [who receives the memo]
Deadline: [distribution date or "not specified"]
Source quality: [complete / partial / fragmented — note issues]
Sensitivity: [level]
```

---

### Phase 2: CLASSIFY CONTENT
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Read through the entire source material and classify every substantive piece of content into one of five categories. This is the analytical core of the skill. The classification is not always obvious — this phase requires judgment, not pattern-matching.

**The Five Categories:**

1. **Decision Made** — A conclusion was reached. It is binding (within the scope of the meeting). It would be wrong for a participant to leave the meeting and act as though it had not been made.
2. **Action Item** — A specific task was assigned, accepted, or committed to. It has (or should have) a named owner and a deadline.
3. **Deferred** — The topic was raised, discussed, and deliberately set aside for a future time. Not abandoned — placed in a queue with an explicit or implicit expectation of return.
4. **Information Only** — Context, background, or an update shared with participants for awareness. No decision required. No action assigned.
5. **Open Question** — A question was raised that was not answered or resolved during the meeting. The answer matters for a decision or action but wasn't available or agreed upon.

**Classification Rules:**
- When in doubt between Decision Made and Information Only: did someone need to take action differently as a result of this content? If yes, it's a decision.
- When in doubt between Action Item and Open Question: was an owner named or accepted? If yes, it's an action item. If not, it's an open question.
- When in doubt between Deferred and Open Question: was there agreement to address this at a specific future point? If yes, it's deferred. If it just trailed off, it's an open question.
- Ambiguous items get flagged — do not force a classification that requires assumptions. Flag it with the relevant ambiguity noted.

**Process:**
1. Read the source material in full before classifying anything.
2. Pass through the source material again, tagging each substantive unit of content with its category.
3. Flag any items where the classification is uncertain and explain why.
4. Produce a classification register — the complete organized list of every item before memo assembly begins.

**Output:**
```
CLASSIFICATION REGISTER

DECISIONS MADE:
  D1. [One-sentence statement of what was decided]
  D2. [...]

ACTION ITEMS:
  A1. [Task] — Owner: [name or "unassigned"] — Deadline: [date or "unspecified"]
  A2. [...]

DEFERRED:
  Def1. [Topic] — Deferred to: [date / next occurrence / "TBD"]
  Def2. [...]

INFORMATION ONLY:
  I1. [Context shared] — [who shared it]
  I2. [...]

OPEN QUESTIONS:
  Q1. [Question] — [why it matters, what it blocks]
  Q2. [...]

FLAGGED / AMBIGUOUS:
  F1. [Content] — [classification uncertainty] — [what would resolve it]
  F2. [...]
```

---

### Phase 3: EXTRACT DECISIONS
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

For each Decision Made item from Phase 2, extract the full decision record: not just what was decided, but who made it, what rationale was stated or inferable, and what the implications are for action or further discussion.

**Process:**
1. For each decision (D1, D2, etc.) from the classification register:
   - **Decision statement:** One clear sentence stating what was decided in active voice.
   - **Decision-maker:** Who made or ratified the decision? In a group setting, was it a consensus, a vote, or a unilateral call by one person? Note the decision-making mode.
   - **Rationale:** What reason was given, if any? If no reason was stated, note "no rationale stated." Do not invent one. If the rationale can be confidently inferred from context, note it as inferred.
   - **Implications:** What does this decision require or preclude? Does it trigger an action? Does it close an open question? Does it create a dependency for another team or process?
   - **Confidence:** Was this decision clearly and explicitly made, or is the classification inferring a decision from the discussion? Flag low-confidence decisions.
2. Check each decision against `{{KNOWN_FACTS}}`. Does any pre-existing context change how this decision should be understood or recorded?
3. Separate decisions from the action items they may have generated. A decision may trigger an action, but they are distinct records.

**Output:**
```
DECISION RECORD

D1: [Decision statement — active voice, one sentence]
    Decision-maker: [name(s) / consensus / unilateral]
    Rationale: [stated rationale or "not stated" or "inferred: [reason]"]
    Implications: [what this triggers, closes, or constrains]
    Confidence: [high — explicitly stated / medium — clearly implied / low — inferred from discussion]

D2: [...]
```

---

### Phase 4: STRUCTURE MEMO
**Entropy Level:** E2 – Procedural
**Control Mode:** DELEGATE

Assemble the classification register and decision record into the standard decision memo format. This phase is mechanical — the hard analytical work is complete. The memo format is fixed. Every section has a defined structure. The output is a clean, standalone document ready for distribution.

**Process:**
1. Build the header block: meeting/thread name, date, participants, owner, distribution date.
2. Write a one-paragraph executive summary (3-5 sentences): meeting objective, number of decisions made, number of actions assigned, key open items. This paragraph is the only place narrative prose appears.
3. Assemble the Decisions Made section from the decision record (Phase 3).
4. Assemble the Actions section from the Action Items in the classification register. Every action must have a named owner. If Phase 2 flagged an action as unowned, carry that flag forward — do not assign an owner that wasn't established in the source material.
5. Assemble the Deferred Items section. Include the topic, why it was deferred, and the expected return date or trigger.
6. Assemble the Open Questions section. For each open question, include what blocks on it and who is responsible for resolving it (if stated or inferable).
7. Add the Next Steps section: the immediate actions required to distribute and execute the memo, with owner and date.
8. Flag any items that require the memo owner's attention before distribution (unowned actions, low-confidence decisions, unresolved ambiguities).

**Output:**

```markdown
# Decision Memo: [Meeting / Discussion Name]

**Date:** [meeting date]
**Participants:** [names + roles]
**Owner:** [memo owner]
**Distribution:** [audience] — [distribution date]
**Sensitivity:** [level]

---

## Executive Summary
[3-5 sentences: objective, how many decisions, how many actions, what's still open]

---

## Decisions Made

| # | Decision | Decision-Maker | Rationale | Implications |
|---|----------|----------------|-----------|--------------|
| D1 | [statement] | [who] | [rationale or "not stated"] | [what this triggers] |
| D2 | [...] | [...] | [...] | [...] |

---

## Actions

| # | Action | Owner | Deadline | Dependencies |
|---|--------|-------|----------|--------------|
| A1 | [task] | [name] | [date] | [what it depends on, if any] |
| A2 | [...] | [...] | [...] | [...] |

⚠️ Unowned actions (require owner assignment before execution):
- [action] — flagged from source: no owner identified

---

## Deferred Items

| # | Topic | Reason for Deferral | Return Date / Trigger |
|---|-------|--------------------|-----------------------|
| Def1 | [topic] | [reason] | [when or what triggers return] |

---

## Open Questions

| # | Question | Blocks | Resolution Owner | Target Date |
|---|----------|--------|-----------------|-------------|
| Q1 | [question] | [what depends on the answer] | [who resolves it or "unassigned"] | [date or "TBD"] |

---

## Next Steps

| Action | Owner | By When |
|--------|-------|---------|
| Distribute this memo | [{{OWNER}}] | [{{DEADLINE}}] |
| [First action from Actions table] | [owner] | [date] |
| [Resolve unowned actions] | [{{OWNER}}] | [date] |

---

**Flagged items requiring owner review before distribution:**
- [ ] [Flag 1]
- [ ] [Flag 2]
```

---

### Phase 5: VALIDATE COMPLETENESS
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Before the memo is finalized, validate that it is complete, accurate, and internally consistent. This phase surfaces the gaps the assembly process may have papered over. It is quality assurance with analytical judgment — not a formatting check.

**Validation Checklist:**
1. **Every action has a named owner.** If any action in the Actions table has no owner, it must be flagged. The memo cannot be distributed with unowned actions that the recipient group will assume are owned.
2. **Every decision has a rationale or a clear "not stated" acknowledgment.** Rationale-less decisions create re-litigation risk — if people don't know why a decision was made, they'll relitigate it when it creates friction.
3. **No ambiguity has been silently resolved.** Review every flagged/ambiguous item from Phase 2. Were they carried forward as flags, or were they cleaned up without acknowledgment? Silent cleanup is a failure mode.
4. **Deferred items have an expected return mechanism.** "TBD" is acceptable; invisible is not. Every deferred item must appear in the memo so it has a paper trail.
5. **Open questions are distinct from decisions.** Review the open questions against the decisions. Is there any question that was actually decided but classified as open? Is there any decision that is actually still a question?
6. **The executive summary accurately represents the body.** Count: does the summary state the same number of decisions and actions that appear in the tables?
7. **No PII or sensitive information is present that violates `{{SENSITIVITY_LEVEL}}`.** If the memo is restricted to a specific group but contains names or specifics that shouldn't travel beyond that audience, flag for the owner to redact.

**Process:**
1. Run every validation check against the assembled memo from Phase 4.
2. For each gap found: describe the gap, state what's needed to resolve it, and flag it for the memo owner.
3. If no gaps are found, confirm the memo is ready for distribution.
4. Produce the final validation summary.

**Output:**
```
VALIDATION SUMMARY

Status: [Ready for distribution / Requires owner action before distribution]

Gaps found:
- [Gap type]: [Description] — Action required: [what owner must do]
- [Gap type]: [Description] — Action required: [what owner must do]

Checks passed:
- All actions have named owners: [Yes / No — N unowned]
- All decisions have rationale or explicit "not stated": [Yes / No]
- No silent ambiguity cleanup: [Yes / No]
- Deferred items have return mechanisms: [Yes / No]
- Open questions distinct from decisions: [Yes / No]
- Executive summary accurate: [Yes / No]
- Sensitivity compliance: [Yes / No]
```

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Summarizing the discussion without classifying decisions separately | Phase 2 classification always runs first; decisions and discussion are always separate categories |
| Assigning an action in the memo that had no owner in the source material | Flag unowned actions; do not assign an owner that wasn't established during the meeting |
| Omitting deferred items because "nothing was decided about them" | Deferred is not forgotten; every deferred item must appear in the memo with a return mechanism |
| Cleaning up ambiguous statements to make the memo read more cleanly | Surface uncertainties and flag them; a memo that hides ambiguity is a liability document |
| Producing a narrative summary instead of a structured memo | Memo format with tables for decisions, actions, deferred, and open items — prose only in the executive summary |
| Assigning "consensus" as the decision-maker when one person clearly made the call | Record decision-maker accurately; misattributing consensus creates accountability gaps |
| Treating a tentative commitment as a confirmed action item | Flag tentative commitments; confirmed actions require explicit owner acceptance |

---

## 💡 Example Applications

| Use Case | Input | Output |
|----------|-------|--------|
| Leadership team quarterly review | 3 hours of raw meeting notes, 8 participants, 22 discussion topics | 1-page decision memo: 6 decisions with owners and rationale, 14 action items with named owners and dates, 4 deferred items with return dates, 3 open questions flagged |
| Email thread decision | 40-message email thread spanning 5 days, decision buried in message 34 | Clean decision record: 3 decisions extracted, 5 action items with owners, 2 open questions flagged, thread context preserved in executive summary |
| Async Slack discussion | Week-long channel export with 80 messages, multiple participants | Decision log for async discussion: attributions preserved, 2 decisions confirmed, 8 action items, 1 large question still open, flagged for synchronous resolution |
| Post-integration kickoff | Cross-functional call with 12 participants, 6 workstreams represented | Decision memo with cross-functional owner matrix: decisions organized by workstream, dependencies mapped across owners, 3 items requiring executive escalation flagged |
| Ambiguous meeting notes | Notes that say "we agreed to move forward" without specifying what "forward" means or who owns it | Phase 2 flags the ambiguity; memo carries the flag forward with a note that owner must clarify before distribution; not invented, surfaced |

---

## 🖥️ Platform Notes

**CLI:** Invoke with `/skill decision-memo-distiller`. Pass `{{SOURCE_MATERIAL}}` as input. For long transcripts, consider summarizing the source first with a length-reduction pass, then running the full skill on the summarized version.

**Web:** Paste SKILL.md as system context. Provide source material and intake variables in the first message. For long source material, paste in sections and ask the skill to hold classification state across messages.

**IDE:** Reference in agent configuration for post-meeting documentation workflows. Pairs effectively with meeting-prep-assistant — prep-assistant prepares you going in, decision-memo-distiller produces the output coming out.

**Any LLM:** Copy SKILL.md contents into context. Provide source material and intake variables. Phase 2 (classification) and Phase 3 (decision extraction) benefit materially from a strong reasoning model. Sonnet recommended over Haiku for any source material with ambiguity.

---

## 📋 Compliance

**AI Governance Alignment:** The skill preserves attribution — decisions are attributed to the stated decision-maker, actions to the stated owner, open questions to the stated asker. The skill does not invent owners, rationale, or conclusions. Flags are surfaced rather than silently resolved. This approach supports accurate organizational record-keeping and reduces the risk of AI-generated memos misrepresenting what participants agreed to.

**PII Risk Level:** low — the skill processes meeting content that may contain participant names, roles, and organizational context. If `{{SOURCE_MATERIAL}}` contains employee performance content, salary data, or personnel decisions, it is classified as sensitive; do not process through a public LLM interface. Use a private or enterprise deployment.

**Model Recommendation:** sonnet — Phase 2 (classification) and Phase 3 (decision extraction) require strong analytical reasoning to distinguish decision from discussion, to identify rationale where it was implied but not stated, and to flag genuine ambiguities rather than papering them over. Haiku is insufficient for source material of moderate complexity or ambiguity.

**Data Handling:** Processes meeting notes, email threads, and conversation exports. Output is a structured Markdown memo. No source content is stored or transmitted beyond the active session. Meeting content should be handled according to its stated `{{SENSITIVITY_LEVEL}}` both when providing input and when distributing the output memo.
