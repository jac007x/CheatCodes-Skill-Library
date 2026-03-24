---
name: status-update-normalizer
description: "Normalizes inconsistent status inputs from multiple contributors into structured, consistent status updates with executive and team-level variants."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - status
  - reporting
  - normalization
  - communication
model_recommendation: haiku
risk_level: low
---

# 🎯 Status Update Normalizer

> One format, one signal, zero guesswork — regardless of how many people contributed.

## Core Philosophy

Status reporting is a coordination problem masquerading as a writing problem. When a program manager assembles updates from eight teams and every team writes in a different style, with different status signals, different levels of detail, and different definitions of "on track," the result is not a status report — it is a diversity of individual updates with a shared heading. Readers have to do the normalization work themselves, and they do it differently every time.

This skill treats normalization as a first-class operation. It is not about making everything sound the same — it is about making the critical signals (status, owner, action needed, timeline) extractable and comparable across every item, every contributor, every week. The narrative style can vary. The structure cannot.

The design produces two outputs by default because the two audiences have genuinely different needs. Executives need a single-screen view of where to direct their attention — blockers and escalations, nothing else. Teams need the full normalized list with owners and actions, because they are the ones who act on it. Collapsing these into a single document serves neither audience well. The skill keeps them separate.

---

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake Status Data | E1 – Deterministic | DELEGATE | Structured collection; all inputs accepted as-is, no interpretation |
| 2. Validate Completeness | E3 – Analytical | NARRATE | Requires judgment about what is missing and whether a gap matters |
| 3. Structure Update | E2 – Procedural | DELEGATE | Fixed normalization template; apply consistently to every item |
| 4. Produce Versions | E1 – Deterministic | DELEGATE | Format selection is rule-based; content is already normalized |

### Mode Transition Diagram

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐
│ DELEGATE  │→│ NARRATE   │→│ DELEGATE  │→│ DELEGATE              │
│ Collect   │  │ Check     │  │ Apply     │  │ Render exec version   │
│ all raw   │  │ each item │  │ standard  │  │ + team version        │
│ inputs    │  │ for gaps  │  │ template  │  │ from normalized list  │
│ E1        │  │ E3        │  │ E2        │  │ E1                    │
└──────────┘  └──────────┘  └────┬─────┘  └──────────────────────┘
                                  │
                          If gaps exist → flag
                          before templating.
                          Do not normalize
                          incomplete items silently.
```

---

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{SOURCE_MATERIAL}}` | All raw status inputs — Slack messages, email text, bullet dumps, deck notes | text | Yes | — |
| `{{REPORTING_PERIOD}}` | The period this update covers (e.g., "Week of March 17", "Q1 Sprint 4") | string | Yes | — |
| `{{AUDIENCE}}` | Who receives this report — exec team, program team, cross-functional leads | string | Yes | — |
| `{{CHANNEL}}` | How it will be delivered — email, Slack, deck, wiki, verbal | choice | Yes | email |
| `{{OWNER}}` | Name or team responsible for this report (not each item — the report itself) | string | No | — |
| `{{CONSTRAINTS}}` | Any items that must be handled carefully — sensitive escalations, known politics | text | No | — |

---

## ⚙️ Phases

### Phase 1: INTAKE STATUS DATA
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Accept all inputs exactly as provided. Do not interpret, rewrite, or make judgment calls in this phase. The goal is to convert the raw stream into a flat list of candidate items that Phase 2 can evaluate.

**Process:**
1. Parse `{{SOURCE_MATERIAL}}` and identify every discrete status item. A status item is anything that references a project, workstream, initiative, or task with at least one of: a named owner, a timeline reference, or an explicit status signal.
2. Assign each item a temporary ID (S1, S2, S3...) to track it across phases.
3. Record the source for each item (who submitted it, if identifiable from the input).
4. Do not consolidate, rephrase, or normalize in this phase. Preserve the contributor's original wording.
5. Flag any input that does not contain even one identifiable item: "This submission contained no extractable status items — returning to `{{OWNER}}` for clarification."

**Output:** Numbered list of candidate status items with source tags. Example:
```
S1 [Source: Engineering] "we're basically on track for the March 28 release except the auth module is still WIP"
S2 [Source: Design] "Figma handoff done. Dev has the files."
S3 [Source: PM - via Slack] "Vendor integration slipping — waiting on legal to sign off on the data agreement"
S4 [Source: Data] "Dashboard live in staging. Need product sign-off before prod push"
```

---

### Phase 2: VALIDATE COMPLETENESS
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Check each item against the four required fields for a normalized status entry. This phase requires judgment — not every gap is a blocker, and some gaps are intentional (e.g., no owner listed because the item is a team-level update). The skill must distinguish between gaps that distort the status signal and gaps that are acceptable context.

**Process:**
1. For each item from Phase 1, check for the four required fields:

   | Field | Description | If Missing |
   |-------|-------------|------------|
   | **Status indicator** | Is this On Track, At Risk, Blocked, or Complete? | Flag: cannot normalize without a status signal |
   | **Item name / scope** | What is this update about? | Infer from context if possible; flag if ambiguous |
   | **Owner** | Who is accountable for this item? | Flag if item will require action — omit flag if informational only |
   | **Timeline reference** | Is there a date, sprint, or deadline attached? | Flag only if the item references a milestone — omit flag if ongoing |

2. Distinguish gap severity:
   - **Hard gap:** Missing status indicator. Cannot normalize without this. Return to source for clarification OR apply a "Status Unknown" indicator as a default.
   - **Soft gap:** Missing owner on an action item. Note the gap; do not block normalization.
   - **Informational gap:** Missing timeline on a non-time-sensitive item. Skip the flag.

3. For items with hard gaps, produce a clarification request:
   ```
   GAP FLAG — S[N]: [original text]
   Missing: [status indicator / owner / scope]
   Request: Please confirm whether this item is On Track, At Risk, Blocked, or Complete.
   ```

4. For items with conflicting signals within the same submission (e.g., "on track but the auth module is WIP"), split into two items: one for the overall status and one for the exception.

**Output:** Validated item list with gap flags marked. Items with hard gaps are held pending clarification or assigned "Status Unknown" with explicit notation.

---

### Phase 3: STRUCTURE UPDATE
**Entropy Level:** E2 – Procedural
**Control Mode:** DELEGATE

Apply the standard normalization template to every validated item. No exceptions. Items that do not fit the template signal either a gap (caught in Phase 2) or a misclassification (this isn't a status item).

**Process:**
1. For each validated item, apply this template:

   ```
   [STATUS_INDICATOR] [ITEM_NAME] — [ONE_SENTENCE_SUMMARY]. [ACTION_OR_OWNER if needed]
   ```

2. Status indicators:
   - 🟢 **On Track** — progressing as planned; no intervention needed
   - 🟡 **At Risk** — behind plan or facing an obstacle; monitoring required, may need intervention
   - 🔴 **Blocked** — cannot progress without external action; intervention required now
   - ✅ **Complete** — milestone or deliverable finished; no further action
   - ⬜ **Status Unknown** — insufficient information to classify; requires follow-up

3. Normalization rules:
   - One sentence for the summary. If the contributor wrote three sentences, compress to one without losing the key signal.
   - If the item is Blocked, the action must name: who needs to do what. "Blocked — legal review pending" is not acceptable. "Blocked — Legal to return signed data agreement by March 21; owner: [Legal lead name]" is acceptable.
   - If the item is At Risk, the summary must name the risk. "At Risk" with no risk description is noise.
   - Preserve specific dates and numbers from the original. "By EOQ" is acceptable if that was the contributor's framing. "Soon" is not.
   - Do not add information the contributor did not provide. If the owner is unknown, leave the action field blank and note the gap.

4. After normalizing all items, sort the list: Blocked first, then At Risk, then On Track, then Complete.

**Output:** Fully normalized status list in sort order. Example:
```
🔴 Vendor Integration — Legal data agreement unsigned; release gating on this item. Action: Legal to return executed agreement by March 21. Owner: [Legal lead].
🟡 Auth Module — WIP; at risk for March 28 release. Engineering tracking daily. No action needed yet.
🟢 Design Handoff — Complete. Figma files delivered to dev as of March 15.
🟢 Staging Dashboard — Live and tested. Pending product sign-off before production push. Owner: [Product lead].
✅ Q1 Roadmap Alignment — Confirmed in March 10 sync. No further action.
```

---

### Phase 4: PRODUCE VERSIONS
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Apply the fixed rendering rules for each output version. The content is already normalized — this phase is template application, not judgment.

**Process:**

**Version 1: Executive Report**

Rules:
- Headline status: one sentence naming the overall health of the program ("The program is on track for the March 28 release with one active blocker requiring immediate attention.")
- Feature only: all Blocked items (full detail), all At Risk items (summary only), and a count of On Track items ("8 items on track — see team report for detail").
- Complete items: not shown unless they were previously flagged as at risk.
- Maximum length: one screen or one email window. If it does not fit, the normalization is incomplete — go back and compress.

```
STATUS REPORT — [REPORTING_PERIOD]
Prepared by: [OWNER if provided]

HEADLINE: [One-sentence overall program health]

BLOCKERS (requires action):
🔴 [Item] — [Summary]. [Action + owner + date]

AT RISK (monitoring required):
🟡 [Item] — [Summary]. [What would move this to blocked]

ON TRACK: [N] items on track — full detail in team report.

COMPLETED THIS PERIOD: [N] items. [List names only]
```

**Version 2: Team Report**

Rules:
- All items shown in full normalized format from Phase 3.
- Sorted: Blocked → At Risk → On Track → Complete.
- Owners named on every item that has one.
- Gap flags shown: items with "Status Unknown" indicator are marked and a follow-up request attached.
- May be as long as needed — this version is for the team, not the executive.

```
TEAM STATUS REPORT — [REPORTING_PERIOD]

🔴 BLOCKED
[Full normalized items]

🟡 AT RISK
[Full normalized items]

🟢 ON TRACK
[Full normalized items]

✅ COMPLETE
[Full normalized items]

⬜ STATUS UNKNOWN — FOLLOW-UP NEEDED
[Items missing required fields + clarification request]
```

**Output:** Two documents — Executive Report and Team Report.

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Mixing format styles across items in the same report | All items follow the same template. The contributor's voice is in the summary sentence, not in the structure. |
| Omitting status indicators because they feel obvious | Every item must have an explicit signal. "The design handoff is done" is not a status indicator. ✅ Complete is. |
| Combining exec and team versions into one document | They serve different purposes. Executives stop reading at the first detail row. Teams need detail to act. Keep them separate. |
| Normalizing away context that changes meaning | "We're blocked but it'll resolve itself" is a different situation from "we're blocked and need escalation." The summary must preserve the distinction. |
| Treating Blocked and At Risk as equivalent severity | Blocked requires intervention now. At Risk requires monitoring. Conflating them causes executives to under-respond to real blockers. |
| Accepting "on track" with no date reference for items near a deadline | On Track is only meaningful relative to a timeline. Force the contributor to name the date, or add "Status Unknown." |
| Including complete items in the exec version by default | Executives care about what needs their attention. Completed items don't. Mention count only. |

---

## 💡 Example Applications

| Use Case | Input | Output |
|----------|-------|--------|
| End-of-week Slack dump from 8 teams | 8 messages averaging 3–5 sentences each, different formats, mixed use of emoji and bullet points | 24 normalized items. Executive report: 1 headline, 2 blockers, 3 at-risk items, 19 on track. Team report: full sorted list with owners and actions. |
| Email thread with embedded status updates across 4 projects | 6 emails, 2 reply chains, 3 projects mentioned multiple times with evolving status | Extracted 14 discrete items, deduplicated to 11 (3 were updates to earlier states), flagged 1 item with conflicting signals for clarification. |
| End-of-sprint status messages from 5 development teams | Sprint status in Jira comment format, inconsistent use of Done/In Progress/Blocked labels | Normalized to standard indicators. Velocity note added: 3 of 5 teams completed all committed items; 2 carried over stories. Exec summary in 3 sentences. |
| Program status deck contributions from 5 contributors ahead of a leadership review | Slide notes, bullet points, and one full paragraph; no consistent owner labeling | Normalized to single-template entries. Identified that two contributors described the same item differently (one said "on track," one said "at risk") — returned both for resolution before report assembly. |
| Weekly cross-functional sync update aggregation | 6 function leads, different cadences, some submitting via email, some via Slack, one verbal note passed through EA | Processed all sources. 2 items from verbal note returned with "Status Unknown" — insufficient detail to classify. All others normalized and version-split. |

---

## 🖥️ Platform Notes

**CLI:** Paste this SKILL.md as context. Provide all raw status inputs as `{{SOURCE_MATERIAL}}` inline. Request all phases at once for a full run, or call Phase 3 and 4 only if your inputs are already validated.

**Web (Claude, ChatGPT, Gemini):** Attach or paste the skill file. Paste `{{SOURCE_MATERIAL}}` directly. This skill is well-suited to haiku-class models — the primary work is template application, not creative generation.

**IDE:** Useful as a post-collection step in workflow automations — pipe collected status messages into `{{SOURCE_MATERIAL}}` and retrieve normalized output.

**Any LLM:** This skill is deliberately simple in model requirements. Haiku is the recommendation because the phases are rule-based, not reasoning-intensive. The only judgment call is Phase 2 (completeness assessment), which benefits from a model that can infer missing context from adjacent text.

---

## 📋 Compliance

**AI Governance Alignment:** The skill applies a fixed normalization template and does not generate opinions, assessments, or recommendations not present in the source material. It surfaces gaps but does not fill them with invented content. All output is traceable to the contributor's input.

**PII Risk Level:** low — Status updates typically reference project names, dates, and team-level owners. Individual names may appear as item owners; these are expected in work context. Do not paste updates containing personal performance information, compensation details, or sensitive HR content.

**Model Recommendation:** haiku — The phase logic is procedural and rule-based. Haiku handles template application, sorting, and gap-flagging reliably and efficiently. Sonnet is appropriate only if `{{SOURCE_MATERIAL}}` is highly ambiguous and requires significant inference to extract discrete items.

**Data Handling:** Session-local. Status reports often contain project timelines, resource names, and milestone information that may be confidential. Use in a compliant, private LLM environment for sensitive program content. Do not paste confidential roadmap or financial milestone data into public web interfaces.
