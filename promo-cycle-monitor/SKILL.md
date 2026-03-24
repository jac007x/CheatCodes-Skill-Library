---
name: promo-cycle-monitor
description: "Monitors the promotion cycle pipeline by pulling panel assignments from inbox and {{NOMINATION_PLATFORM}}, classifying each by risk status, and surfacing stale or silently-dropped items before they become escalations."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - promotions
  - talent-management
  - cycle-monitoring
  - skyward
  - tech-panel
  - ANCT-designed
  - workflow-automation
---

# Promo Cycle Monitor

A pipeline-aware promotion cycle monitoring skill that doesn't just count open
assignments — it classifies their risk state and surfaces the ones that will
become escalations if no one acts today.

Most promotion cycle tooling is reactive. You find out a panel disappeared
after the deadline passed. You find out a panelist never responded after the
candidate has been waiting three weeks. You find out about a {{NOMINATION_PLATFORM}} access
issue when the panelist emails you in frustration.

This skill is architecturally different. It was designed using **Adaptive
Narrative Control Theory (ANCT)** — each phase uses the control mode matched
to its actual uncertainty level:

- **Pipeline pull** → DELEGATE (low entropy, just enumerate)
- **Risk classification** → NARRATE (medium entropy, requires judgment about what "stalled" means)
- **Exception triage** → NARRATE (E3, policy-governed decisions about edge cases)
- **Follow-up drafting** → GENERATE → NARRATE (high entropy, situation-specific messaging)
- **Status snapshot** → NARRATE → DELEGATE (compress findings into an actionable dashboard)

**The insight:** The most dangerous assignment in a promotion cycle is not the
one with a red flag — it's the one with no flag at all because it silently
expired. The skill is designed to find those first.

---

## Core Philosophy

- **Silence is a signal** — a panel with no activity after 5 days is not fine, it is at risk
- **Overdue is not one category** — some overdue panels need a nudge; some need escalation; some are already gone
- **Volume is the enemy of oversight** — 110+ assignments means no one catches the dropped ones manually
- **Classification before action** — the wrong follow-up (remind vs. escalate vs. reassign) makes things worse
- **The pipeline is the product** — the output is not a report, it is a current-state view of what needs a decision today

---

## ANCT Architecture

This skill was designed with the adaptive-workflow-architect meta-skill.
Here is its entropy profile and mode map:

```
Phase:      1          2          3          4          5            6
Entropy:    E1         E2         E3         E4         E3           E1→E2
Mode:       DELEGATE   DELEGATE   NARRATE    GEN→NAR    NARRATE      NAR→DEL

            pull       classify   surface    draft      triage       produce
            pipeline   by status  risks      follow-ups exceptions   snapshot
            from                  and stale             (access,     (counts,
            inbox/                items                 post-        flags,
            {{NOMINATION_PLATFORM}}                                     deadline)    decisions)
```

### Mode Transition Diagram

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐
│ DELEGATE  │→│ DELEGATE  │→│ NARRATE   │→│ GENERATE → NARRATE    │
│ Pull all  │  │ Classify  │  │ Surface   │  │ Draft follow-ups      │
│ open      │  │ each      │  │ at-risk,  │  │ per panelist and      │
│ panels    │  │ assignment│  │ overdue,  │  │ situation type        │
│ from      │  │ on-track/ │  │ silently  │  │                       │
│ inbox +   │  │ at-risk/  │  │ dropped   │  │ ⚡ COMPRESSION        │
│ {{NOMINATION_PLATFORM}}   │  │ stalled/  │  │ items     │  │ CHECKPOINT: one       │
│           │  │ dropped   │  │           │  │ action per assignment │
│ E1        │  │ E2        │  │ E3        │  │ required before E5    │
└──────────┘  └──────────┘  └──────────┘  └──────────────────────┘
                                                       │
                                                       ▼
                              ┌──────────┐  ┌──────────────────────┐
                              │ NAR→DEL   │←│ NARRATE               │
                              │ Produce   │  │ Triage exceptions:    │
                              │ status    │  │ post-deadline noms,   │
                              │ snapshot  │  │ access issues,        │
                              │ dashboard │  │ policy edge cases     │
                              │           │  │                       │
                              │ E1→E2     │  │ E3                    │
                              └──────────┘  └──────────────────────┘
```

---

## Intake: Customize This Skill

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{CYCLE_NAME}}` | Name of the active promotion cycle | string | Yes | — |
| `{{PANEL_TYPE}}` | Panel type scope for this run | choice: Principal, F+, DE, All | Yes | All |
| `{{LOOKBACK_DAYS}}` | How many days back to pull panel activity from inbox | integer | Yes | 30 |
| `{{STALE_THRESHOLD_DAYS}}` | Days of inactivity before an assignment is flagged as stale | integer | No | 5 |
| `{{INBOX_SOURCE}}` | Where promotion cycle emails live | choice: outlook, gmail, manual-export | Yes | outlook |
| `{{COMPENDIUM_PATH}}` | Path to the inbox-intelligence knowledge compendium | filepath | No | — |
| `{{NOMINATION_PLATFORM}}` | The internal nomination and panel management platform (e.g., Skyward, Workday, SuccessFactors) | string | Yes | — |

---

## Phase 1: PULL PIPELINE
**Control Mode: DELEGATE** | **Entropy: E1 (Deterministic)**

This is pure enumeration. No judgment. Pull everything, classify nothing yet.

### Actions

1. Pull from `{{INBOX_SOURCE}}` all emails matching `{{CYCLE_NAME}}` within `{{LOOKBACK_DAYS}}`:
   - Panel assignment notifications
   - Panelist response emails (accepted, declined, completed)
   - Deadline reminder messages
   - {{NOMINATION_PLATFORM}} access request threads
   - Exception request emails (post-deadline nominations, panel swaps)
   - Escalation threads

2. Pull from {{NOMINATION_PLATFORM}} (if accessible) or `{{COMPENDIUM_PATH}}` (if set):
   - Open panel assignments by candidate
   - Assignment status per panelist
   - Deadline dates per assignment
   - Completion timestamps where present

3. Deduplicate and merge inbox signals with {{NOMINATION_PLATFORM}} records. One row per assignment.

4. Enumerate total counts by raw status bucket:
   - **Pending** — assigned, no response yet
   - **Accepted** — panelist confirmed, evaluation not yet submitted
   - **Submitted** — evaluation complete
   - **Overdue** — past deadline, not submitted
   - **Expired** — deadline passed with no panelist activity (no accept, no decline, no submission)
   - **Declined** — panelist declined or was removed

### Exit Condition

All assignments for `{{CYCLE_NAME}}` enumerated in a single flat list with raw status. Total count confirmed. If {{NOMINATION_PLATFORM}} is inaccessible, flag and continue from inbox data only.

### Output

```markdown
**Pipeline Pull — {{CYCLE_NAME}} ({{PANEL_TYPE}})**
**Source:** [inbox / {{NOMINATION_PLATFORM}} / compendium]
**Pulled:** [N] total assignments

| Status    | Count |
|-----------|-------|
| Pending   | N     |
| Accepted  | N     |
| Submitted | N     |
| Overdue   | N     |
| Expired   | N     |
| Declined  | N     |

**{{NOMINATION_PLATFORM}} access:** [available / unavailable — continuing from inbox]
```

---

## Phase 2: CLASSIFY STATUS
**Control Mode: DELEGATE** | **Entropy: E2 (Procedural)**

Same classification logic applied to every assignment. No judgment yet — that
is Phase 3's job. Apply the rules consistently.

### Classification Rules

| Observed State | Assigned Classification |
|----------------|------------------------|
| Assigned < `{{STALE_THRESHOLD_DAYS}}` days ago, no response | on-track |
| Assigned >= `{{STALE_THRESHOLD_DAYS}}` days ago, no response | at-risk |
| Panelist accepted, evaluation not submitted, deadline > 48h | on-track |
| Panelist accepted, evaluation not submitted, deadline <= 48h | at-risk |
| Panelist accepted, evaluation not submitted, deadline passed | stalled |
| No panelist activity, deadline passed | silently-dropped |
| Assignment removed from {{NOMINATION_PLATFORM}} with no completion record | silently-dropped |
| Evaluation submitted | completed |
| Panelist formally declined | declined-needs-reassignment |

### Escalation → NARRATE

If an assignment's state does not fit cleanly into the above table (ambiguous
email signals, conflicting {{NOMINATION_PLATFORM}} vs. inbox data, partial completion records):

- Flag the assignment as **ambiguous**
- Carry it into Phase 3 for manual classification judgment

### Exit Condition

Every assignment has exactly one classification. Ambiguous assignments are
flagged and carried forward. No assignment remains unclassified.

### Output

```markdown
**Classification Results — {{CYCLE_NAME}}**

| Classification             | Count |
|----------------------------|-------|
| on-track                   | N     |
| at-risk                    | N     |
| stalled                    | N     |
| silently-dropped           | N     |
| completed                  | N     |
| declined-needs-reassignment| N     |
| ambiguous (flagged)        | N     |
```

---

## Phase 3: SURFACE RISKS
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

This is where judgment begins. Not every at-risk assignment is the same risk.
Not every overdue item needs the same action. Prioritize by impact and urgency.

### Actions

1. From the Phase 2 classifications, pull all assignments that are:
   - **silently-dropped** (highest priority — these are invisible without this step)
   - **stalled** (deadline passed, panelist accepted but did not submit)
   - **at-risk** (approaching deadline or unresponsive panelist)
   - **ambiguous** (unresolved from Phase 2)
   - **declined-needs-reassignment** (panel is uncovered)

2. For each flagged assignment, assess:
   - How long has it been since any activity? (days since last signal)
   - Is the candidate's promotion decision blocked by this panel?
   - Has this panelist gone silent on other assignments in the same cycle?
   - Is this a pattern (same panelist, same manager's nominees) or isolated?
   - Is there an upcoming deadline cascade (multiple panels expiring same week)?

3. **Prioritization** (this is the NARRATE work):
   - Priority 1: silently-dropped + candidate decision imminent
   - Priority 2: stalled + panelist unresponsive > 7 days
   - Priority 3: at-risk + deadline within 48 hours
   - Priority 4: declined-needs-reassignment (panel uncovered)
   - Priority 5: ambiguous (needs human resolution)

4. Surface the top items. Do not list all 110+ assignments — surface the ones
   that require a decision or action today.

### Escalation → GENERATE (if no risks surface)

If Phase 2 classifications show all on-track or completed and no risks surface:

> "No at-risk or dropped assignments detected. Given the cycle volume
> and typical patterns, what assignments might be misclassified as on-track?
> What signals in the inbox data are ambiguous?"

Generate a skeptical secondary pass rather than accepting a clean state at face value.

### Exit Condition

Prioritized list of assignments requiring action, with reasoning for priority.
Or: generated skeptical review of the clean-state result.

### Output

```markdown
**At-Risk Assignments — {{CYCLE_NAME}}**

Priority 1 — Silently Dropped (candidate decision imminent):
- [Candidate] / [Panelist] — last activity: [N days ago] — deadline: [date] — [note]

Priority 2 — Stalled (accepted, not submitted, unresponsive):
- [Candidate] / [Panelist] — accepted [date] — [N] days since last contact

Priority 3 — At Risk (deadline within 48h):
- [Candidate] / [Panelist] — deadline: [date/time] — status: [accepted / no response]

Priority 4 — Uncovered Panels (needs reassignment):
- [Candidate] — panelist [name] declined [date] — no replacement assigned

Priority 5 — Ambiguous (needs human judgment):
- [Candidate] / [Panelist] — conflict: [describe inbox vs. {{NOMINATION_PLATFORM}} discrepancy]
```

---

## Phase 4: GENERATE FOLLOW-UPS
**Control Mode: GENERATE → NARRATE** | **Entropy: E4 (Creative)**

**This is the highest-entropy phase.** The same follow-up message sent to
a panelist who forgot and a panelist who is blocking on a {{NOMINATION_PLATFORM}} access
issue will get different responses — the wrong one wastes time or creates friction.

### GENERATE Step (expand)

For each Priority 1-3 assignment from Phase 3, generate **2 follow-up drafts**
based on the most likely situation:

```
Draft A (default): Polite reminder — assumes the panelist forgot or deprioritized
Draft B (escalation): Situation-aware — acknowledges a specific barrier
                      (access issue, unclear instructions, conflict)
```

Signals to weigh per panelist:
- **No activity at all** (never responded to assignment) → Draft A first, then B if no response
- **Accepted but no submission** + long gap → ask if there is a blocker (Draft B)
- **Previous {{NOMINATION_PLATFORM}} access thread in inbox** → Draft B immediately (access is the known barrier)
- **Pattern across multiple candidates** → flag for manager escalation, not another nudge
- **Same panelist, multiple silently-dropped** → escalate upward, do not re-remind

### COMPRESSION CHECKPOINT

> **Before proceeding to Phase 5, each at-risk assignment must have
> exactly one recommended action:**
>
> send Draft A / send Draft B / escalate to manager / reassign panel / flag for human decision

No assignment leaves Phase 4 without a recommended action.

### NARRATE Step (compress)

Select the most appropriate draft per assignment. Annotate why. Surface any
assignments where both drafts are inadequate and human judgment is required.

### Exit Condition

One recommended action and one draft message per at-risk assignment. Assignments
requiring escalation beyond a message are separated into an escalation list.

### Output

```markdown
**Follow-Up Drafts — {{CYCLE_NAME}}**

---
**[Candidate] / [Panelist]** | Action: Send Draft A
> Subject: Promotion Panel — {{CYCLE_NAME}} — [Candidate Name]
>
> Hi [Panelist],
>
> Just following up on the panel assignment for [Candidate] as part of
> {{CYCLE_NAME}}. The evaluation window [closes / closed] on [date].
>
> If you have any questions or need access to {{NOMINATION_PLATFORM}}, reply here and
> I can help get that sorted quickly.
>
> Thanks,
> [Your name]

---
**[Candidate] / [Panelist]** | Action: Send Draft B (known access issue)
> Subject: Re: {{NOMINATION_PLATFORM}} Access — {{CYCLE_NAME}} Panel
>
> Hi [Panelist],
>
> I saw the earlier thread about {{NOMINATION_PLATFORM}} access. If that's still
> blocking you on the [Candidate] panel, I want to make sure we get
> it resolved before [deadline]. Can you confirm whether access is
> working or if I should re-open a ticket?
>
> [Your name]

---
**[Candidate] / [Panelist]** | Action: ESCALATE — pattern detected (3 assignments, no activity)
> Recommend: Reach out to [Panelist]'s manager directly.
> Do not send another reminder — prior reminders have not been effective.
```

---

## Phase 5: EXCEPTION TRIAGE
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

Exceptions are the cases where the standard process does not apply and a
policy-governed decision is required. These are not failures — they are
judgment calls that need to be surfaced explicitly so a human can decide.

### Exception Types to Triage

| Exception Type | Description | Decision Required |
|----------------|-------------|-------------------|
| Post-deadline nomination | Candidate nominated after the cycle deadline | Accept with justification, or decline — cannot silently include |
| Panel swap request | Assigned panelist requests to be replaced | Approve reassignment, or hold — requires tracking the new assignment |
| {{NOMINATION_PLATFORM}} access failure | Panelist cannot access the evaluation system | Open IT ticket, extend deadline, or accept off-system submission |
| Incomplete panel | One panelist submitted, second did not — decision threshold unclear | Determine if single submission is sufficient for the candidate level |
| Conflict of interest flag | Panelist raises a conflict with the candidate | Remove and reassign; document the flag |
| Candidate withdrawal | Candidate withdraws from consideration mid-cycle | Close all open panels; notify assigned panelists |

### Actions

1. Identify all exception threads from Phase 1 inbox pull.
2. For each exception, classify the type using the table above.
3. Determine whether the exception has already been resolved (look for a reply confirming resolution).
4. Surface unresolved exceptions with the decision that is required.
5. Do not make the policy decision — surface it for human action.

### Exit Condition

All exceptions identified, classified, and resolution-status assessed.
Unresolved exceptions surfaced with the specific decision required.

### Output

```markdown
**Exception Triage — {{CYCLE_NAME}}**

Unresolved Exceptions Requiring a Decision:

1. [Type: Post-deadline nomination]
   Candidate: [Name] | Nominated by: [Manager] | Date: [N days after deadline]
   Decision required: Accept with justification / Decline

2. [Type: {{NOMINATION_PLATFORM}} access failure]
   Panelist: [Name] | Candidate: [Name] | IT ticket: [open / not yet filed]
   Decision required: Extend deadline / Accept off-system / Reassign

3. [Type: Incomplete panel]
   Candidate: [Name] | Submitted: 1 of 2 panelists | Missing: [Panelist]
   Decision required: Proceed with single submission / Hold for second

Resolved Exceptions (no action needed):
- [Candidate] — panel swap approved, replacement [Name] assigned [date]
```

---

## Phase 6: PRODUCE STATUS SNAPSHOT
**Control Mode: NARRATE → DELEGATE** | **Entropy: E1 → E2**

Synthesize all phases into a single cycle dashboard. This is the artifact that
gets shared, acted on, or filed. Format is consistent — this is the output
that builds trust because it looks the same every time you run it.

### Dashboard Structure

```markdown
## Promotion Cycle Status Snapshot
**Cycle:** {{CYCLE_NAME}} | **Panel Type:** {{PANEL_TYPE}}
**Run date:** [date] | **Lookback:** {{LOOKBACK_DAYS}} days

---

### Pipeline Summary

| Status             | Count |
|--------------------|-------|
| Completed          | N     |
| On-Track           | N     |
| At-Risk            | N     |
| Stalled            | N     |
| Silently Dropped   | N     |
| Needs Reassignment | N     |
| Ambiguous          | N     |
| **Total**          | **N** |

---

### Red Flags — Action Required Today

1. [Assignment] — [Classification] — [Recommended action] — [Deadline]
2. [Assignment] — [Classification] — [Recommended action] — [Deadline]
3. [Assignment] — silently dropped — escalate immediately

---

### Pending Decisions

| Exception | Type | Decision Needed |
|-----------|------|-----------------|
| [Candidate] | Post-deadline nomination | Accept / Decline |
| [Panelist] | {{NOMINATION_PLATFORM}} access | Extend / Reassign |

---

### Follow-Ups Staged (ready to send)

- [N] Draft A reminders
- [N] Draft B situation-aware messages
- [N] Escalation recommendations (do not send another reminder)

---

### Cycle Health Indicator

[GREEN / YELLOW / RED]

GREEN:  >80% completed or on-track, <3 silently dropped, no unresolved exceptions
YELLOW: 15-30% at-risk or stalled, or 3-7 silently dropped, or 1-2 unresolved exceptions
RED:    >30% at-risk/stalled, or >7 silently dropped, or exception cascade in progress
```

---

## Anti-Patterns

```
PROMO CYCLE MONITOR ANTI-PATTERNS (from ANCT failure mode analysis):

X "Remind again" as default for all overdue
  Every overdue assignment gets the same nudge email.
  No distinction between a panelist who forgot and one who is blocked on {{NOMINATION_PLATFORM}}.
  → ANCT diagnosis: flat DELEGATE applied to E4 phase; skipped GENERATE step
  → Correct: classify the barrier first, then select Draft A or Draft B

X Marking silently-dropped panels as complete
  {{NOMINATION_PLATFORM}} shows the assignment as closed. No submission record exists.
  Assumes the system is correct and the panel was completed.
  → ANCT diagnosis: DELEGATE applied where NARRATE was required;
    absence of completion record was not treated as a signal
  → Correct: flag as silently-dropped; require positive confirmation of completion

X Clean dashboard accepted at face value
  All assignments show on-track. No further investigation.
  In a 110+ assignment cycle, some are always misclassified.
  → ANCT diagnosis: premature compression; skipped skeptical GENERATE pass
  → Correct: if no risks surface, run a secondary skeptical scan (Phase 3 escalation)

X Treating all exceptions as standard delays
  A post-deadline nomination is processed the same as a late submission.
  → ANCT diagnosis: exception triage skipped; E3 judgment replaced with E1 rule
  → Correct: surface exceptions separately; make the policy decision explicit

X Listing all 110+ assignments in the output
  Volume obscures the actual risks.
  → ANCT diagnosis: Phase 3 NARRATE filter not applied; DELEGATE logic returned all rows
  → Correct: surface only items requiring action; snapshot shows counts, not rows
```

---

## Example Applications

| Scenario | Entropy | Key Phase | ANCT Insight |
|----------|---------|-----------|--------------|
| **Monday morning cycle check** | E1-E2 | Phase 6 | Snapshot first. If health is GREEN, stop. If YELLOW or RED, go deeper. |
| **Panelist has not responded in 8 days** | E3 | Phase 4 | Do not auto-remind. Check for {{NOMINATION_PLATFORM}} access thread first. Draft B may be correct. |
| **5 panels expired same week** | E4 | Phase 3 + 5 | This is a pattern, not a coincidence. May indicate a manager block or a {{NOMINATION_PLATFORM}} outage. Escalation, not reminders. |
| **Post-deadline nomination arrives** | E3 | Phase 5 | Do not process silently. Surface for explicit accept/decline decision with justification. |
| **Cycle closing in 72 hours** | E3-E4 | Phase 3 | Tighten `{{STALE_THRESHOLD_DAYS}}` to 1. Every at-risk becomes a red flag. |
| **{{NOMINATION_PLATFORM}} is down** | E4 | Phase 5 | Exception cascade in progress. All panelists with open assignments are effectively blocked. Single triage, not 110 individual tickets. |

---

## Platform Notes

| Platform | How to Use |
|----------|------------|
| **Any LLM** | Paste this SKILL.md as context. Provide exported inbox data or {{NOMINATION_PLATFORM}} report and ask for a cycle status snapshot. |
| **With inbox-intelligence** | Set `{{COMPENDIUM_PATH}}` to the active compendium. Phases 1 and 5 get richer signals from indexed email threads. |
| **CLI tools** | Copy to skills directory; invoke with `/skill promo-cycle-monitor` |
| **Recurring use** | Run at the same time each day during an active cycle. Snapshot format is consistent — deltas are visible. |

---

## Cross-References

This skill is designed to work with related skills in the library:

| Skill | Integration Point |
|-------|-------------------|
| **inbox-intelligence** | Primary data source. Set `{{COMPENDIUM_PATH}}` to pull indexed panel emails instead of raw inbox. Eliminates Phase 1 manual export. |
| **workday-roster-validator** | Validates panelist roster before Phase 1 completes. Catches removed or transferred employees who still appear as assigned panelists. |
| **skyward-support-responder** | Determines when a {{NOMINATION_PLATFORM}} access issue warrants a formal IT escalation vs. a direct follow-up. Phase 5 hands off access exceptions here. |

### How to Use Together

1. Run `inbox-intelligence` on the promotion cycle inbox folder before running this skill
2. The compendium indexes all panel assignment threads, {{NOMINATION_PLATFORM}} notifications, and panelist replies
3. Set `{{COMPENDIUM_PATH}}` when invoking `promo-cycle-monitor`
4. Phase 1 queries the compendium instead of raw inbox — faster and cross-referenced
5. Phase 4 (follow-up drafts) references prior interaction history from the compendium to avoid re-sending messages that were already sent

---

## Compliance

- **PII Risk:** Medium. Panelist names, candidate names, evaluation status, and communication history appear in all phase outputs. Store the status snapshot in a private compendium only. Do not paste output into shared channels or public interfaces.
- **Retention:** Cycle snapshots should be archived per your organization's talent data retention policy. Do not retain candidate or panelist data after the cycle closes unless required for audit.
- **Model Recommendation:** Sonnet for full runs (Phase 4 follow-up generation and Phase 5 exception triage benefit from strong reasoning). Haiku is acceptable for Phase 6 snapshot-only runs on a clean pipeline.
- **Human Oversight:** The skill surfaces risks and drafts messages — it does not send them. Every follow-up and every exception decision requires human review before action. The recommended action per assignment is a recommendation, not an execution.

---

## Design Credit

This skill's architecture was designed using the
[adaptive-workflow-architect](../adaptive-workflow-architect/) meta-skill,
applying Adaptive Narrative Control Theory (ANCT) to map each phase to its
optimal control mode based on entropy level.
