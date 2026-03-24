---
name: audit-prep-assistant
description: "Guides people analytics leaders through internal audit preparation by organizing data methodology, classifying what to share vs. redact, drafting plain-language methodology narratives, and packaging a complete audit-ready kit with anticipated Q&A."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - audit
  - compliance
  - hr-analytics
  - data-governance
  - org-health
  - people-analytics
  - headcount-reporting
  - methodology-documentation
  - ANCT-designed
---

# Audit Prep Assistant

A people analytics audit preparation skill that turns an auditor's inquiry into a
structured, defensible package — organized methodology, classified data inventory,
anticipated Q&A, and a clear brief on what to say, share, and withhold.

1. **A classified data inventory** — every report, source, and methodology mapped to
   a disposition: share as-is, redact before sharing, or do not share
2. **A methodology narrative** — plain-language walkthrough of your data pipeline
   written for non-technical auditors, not your data team
3. **An audit prep kit** — what to bring to the room, what to say when asked, and
   a post-audit tracker for commitments and follow-ups

This is not a document generator. It is a **structured audit readiness workflow**
that applies disciplined classification to complex, PII-adjacent data systems and
produces defensible, professional responses under scrutiny.

**Design target:** Full audit inquiry to prep-kit-complete in under 2 hours.

---

## Core Philosophy

- **Auditors are not your data team** — every methodology explanation must work for
  someone who has never opened Workday or seen a headcount report.
- **Classification precedes sharing** — nothing leaves your hands until it has been
  reviewed against the redaction policy. Intent doesn't protect you; process does.
- **Silence is not safety** — an unprepared "I'll follow up" in an audit room is a
  commitment. Know what you will and won't say before you walk in.
- **Your methodology is the audit** — if you can't explain your data pipeline clearly,
  the auditor will draw their own conclusions. Own the narrative.
- **Track every commitment** — whatever you say you'll send, confirm, or follow up on
  becomes an auditor expectation. Log it immediately.

---

## ANCT Architecture

### Entropy Profile

```
Phase:      1          2          3          4→3        3          1-2        2
Entropy:    E1         E2         E3         E4→E3      E3         E1-E2      E2
Mode:       DELEGATE   DELEGATE   NARRATE    GEN→NAR    NARRATE    DELEGATE   DELEGATE

            capture    enumerate  classify   draft      anticipate package    track
            inquiry    data       items      narrative  questions  kit        follow-ups
            details    sources
```

### Why This Entropy Map

| Phase | Why This Entropy Level |
|-------|------------------------|
| 1. Intake | E1 — structured data capture, no judgment yet |
| 2. Inventory | E2 — enumeration against known systems and reports |
| 3. Classify | E3 — requires judgment: what is safe, sensitive, or off-limits? |
| 4. Brief | E4→E3 — creative drafting compressed by accuracy requirements |
| 5. Prep Questions | E3 — analytical: anticipate, not improvise |
| 6. Package | E1-E2 — structured assembly, format work |
| 7. Follow-Up Tracker | E2 — procedural logging of commitments made |

---

## Intake: Customize This Skill

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{AUDIT_SCOPE}}` | What the audit is reviewing (e.g., "Resource Planning & Allocation Oversight") | text | Yes | — |
| `{{AUDIT_DATE}}` | Date or date range of the audit review / walkthrough | date | Yes | — |
| `{{AUDITOR_NAME}}` | Name and team of the lead auditor(s) | text | Yes | — |
| `{{WHAT_ALREADY_SHARED}}` | Any materials already sent to auditors prior to this session | list | No | — |
| `{{DATA_SOURCES}}` | Systems and reports in scope (e.g., Workday, MBR dashboard, headcount file) | list | Yes | — |
| `{{REDACTION_POLICY}}` | What must be redacted before any data leaves | text | No | Redact individual names and employee IDs (WINs) from all shared data; aggregate to team or org level minimum |

---

## Phase 1: INTAKE
**Control Mode: DELEGATE** | **Entropy: E1 (Deterministic)**

Pure information capture. No judgment. Establish the factual envelope before
any classification or narrative work begins.

### Actions

1. Collect the following from the user:

```yaml
audit_intake:
  audit_name: "e.g., FY27 Resource Planning & Allocation Oversight Review"
  audit_scope: "{{AUDIT_SCOPE}}"
  audit_date: "{{AUDIT_DATE}}"
  auditor_name: "{{AUDITOR_NAME}}"
  auditor_team: "e.g., Global Internal Audit"
  fiscal_year_in_scope: "e.g., FY27"
  what_already_shared:
    - item: "document or data name"
      shared_on: "date"
      shared_via: "email | portal | meeting"
  data_sources_in_scope: "{{DATA_SOURCES}}"
  redaction_policy: "{{REDACTION_POLICY}}"
  known_sensitivities: "any areas already flagged as sensitive by legal/HR"
  my_role_in_audit: "e.g., primary data owner, support role, subject matter expert"
  prep_deadline: "when do you need to be ready by?"
```

2. If any required fields are missing, prompt for them explicitly before proceeding.
3. Log `what_already_shared` — this list becomes the baseline for Phase 3 classification.
4. Confirm `redaction_policy` is set. If not provided, apply the default.

### Exit Condition
All required intake fields captured. Audit context documented. Redaction policy confirmed.

### Output
```
Intake complete.
Audit: [AUDIT_SCOPE] | Auditor: [AUDITOR_NAME] | Date: [AUDIT_DATE]
Data sources in scope: [N]
Already shared: [N items or "nothing yet"]
Redaction policy: [summary]
Proceeding to inventory.
```

---

## Phase 2: INVENTORY
**Control Mode: DELEGATE** | **Entropy: E2 (Procedural)**

Enumerate every data source, report, methodology, and artifact that could be in
scope. Systematic. Complete. No classification yet — just the full list.

### Actions

1. For each item in `{{DATA_SOURCES}}`, and by prompting the user to think through
   their full data footprint, capture:

```yaml
inventory_item:
  id: "INV-001"
  name: "e.g., MBR Exec Summary Dashboard"
  type: report | dashboard | raw_data | methodology_doc | process_doc | presentation | other
  system_source: "e.g., Workday, Excel, Power BI, SharePoint"
  description: "one-sentence description of what this contains"
  data_freshness: "how current is this? e.g., updated monthly, as of Q3 FY26"
  contains_pii: true | false | unknown
  pii_types: "e.g., employee names, WINs, compensation, performance ratings"
  owner: "who owns or maintains this?"
  location: "where does this live? e.g., SharePoint link, local file, database"
  already_shared: true | false  # populated from Phase 1
  auditor_likely_to_ask: true | false  # your assessment
  notes: "anything unusual or sensitive to flag"
```

2. Prompt the user to check for items they may have missed:

```
Common categories to verify:
  - Headcount reports (current and historical)
  - Org charts / reporting structure data
  - Turnover / attrition reports
  - Requisition / open role tracking
  - MBR or QBR decks with workforce data
  - Compensation band or pay equity analyses
  - Survey results (engagement, exit)
  - Workforce planning models or scenario files
  - Methodology documentation for any metrics
  - External benchmark data used in reporting
  - Email threads or meeting notes referencing workforce data
```

3. Assign sequential IDs (INV-001, INV-002, ...) to every item.

### Exit Condition
Complete inventory documented. Every in-scope item has an ID, type, and PII flag.

### Output
```
Inventory complete: [N] items catalogued
  Reports/dashboards: [N]
  Raw data files: [N]
  Methodology docs: [N]
  Other: [N]
PII-flagged items: [N]
Already shared: [N]
Proceeding to classification.
```

---

## Phase 3: CLASSIFY
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

This is where judgment begins. Each inventory item gets a disposition. No item
should reach the auditor's hands without passing through this phase.

### Classification Taxonomy

| Code | Disposition | Meaning |
|------|-------------|---------|
| **SHARE** | Safe to share as-is | Aggregated, anonymized, or non-sensitive. No edits needed. |
| **REDACT** | Share after redaction | Contains PII or sensitive detail; can be shared once scrubbed per `{{REDACTION_POLICY}}` |
| **HOLD** | Must not share | Legally privileged, too sensitive to share even redacted, or outside audit scope |
| **SENT** | Already shared | Documented in Phase 1; confirm no additional copies or versions exist |
| **EXPLAIN** | Share with context | Safe to share, but requires verbal or written explanation to avoid misinterpretation |

### Classification Rules

```
IF contains_pii = true AND aggregate_level < team → REDACT (apply redaction policy first)
IF item is in what_already_shared → SHARE (SENT — confirm version matches)
IF item contains compensation data at individual level → HOLD (escalate to HR/Legal)
IF item is a methodology doc with no individual data → SHARE
IF item contains open-ended survey responses → REDACT (free text may identify individuals)
IF item is a presentation built from already-SHARE items → EXPLAIN (verify no raw data embedded)
IF item scope is outside the audit focus area → HOLD (out of scope)
IF uncertain → flag for human review before proceeding
```

### Classification Output Per Item

```yaml
classification:
  id: "INV-001"
  disposition: SHARE | REDACT | HOLD | SENT | EXPLAIN
  rationale: "one sentence why"
  redaction_required: true | false
  redaction_instructions: "specific fields or rows to remove/aggregate"
  share_condition: "any conditions on sharing (e.g., only if auditor asks)"
  risk_flag: low | medium | high
  reviewer_note: "anything requiring human sign-off before action"
```

### Escalation Gate

Before finalizing any HOLD classification, surface to the user:
> "INV-[N] ([item name]) is flagged as HOLD. Reason: [rationale].
> Do you want to confirm HOLD, escalate to Legal/HR for a determination,
> or reclassify? [Hold / Escalate / Reclassify]"

### Exit Condition
Every inventory item has a disposition, rationale, and risk flag.
All HOLD items confirmed or escalated. All REDACT items have redaction instructions.

### Output
```
Classification complete:
  SHARE: [N] items
  REDACT: [N] items (redaction instructions attached)
  HOLD: [N] items (confirmed or escalated)
  SENT: [N] items (previously shared — versions verified)
  EXPLAIN: [N] items (context notes drafted)
High-risk flags: [N]
Proceeding to methodology brief.
```

---

## Phase 4: BRIEF
**Control Mode: GENERATE → NARRATE (Accuracy Gate)** | **Entropy: E4 → E3**

Draft the methodology narrative. This is the written walkthrough of your data
pipeline that auditors will read before the review session. It must be technically
accurate and plainly intelligible to a non-technical audience simultaneously.

### GENERATE Step: Draft the Narrative

For each data system or report in scope (starting with SHARE and EXPLAIN items),
draft a methodology section:

```markdown
## [Report or System Name]

**What it is:** One sentence on what this report/dashboard shows.

**Who uses it:** Audience and decision-making context.

**Data source:** Where the data originates (e.g., Workday HCM, extracted via
[process], refreshed [frequency]).

**How it's built:**
1. [Step 1 — data pull or export]
2. [Step 2 — transformation or calculation]
3. [Step 3 — aggregation or presentation layer]

**Key metrics defined:**
- [Metric name]: [plain-language definition]. Calculated as: [formula or logic].
- [Metric name]: ...

**Known limitations or caveats:**
- [Any data gaps, timing lags, or population exclusions]
- [Any metric that is directional rather than precise]

**What it does NOT show:** Explicit statement of scope boundaries.
```

### NARRATE Step: Accuracy Gate (Compression Checkpoint)

After drafting each section, verify:

```
Accuracy checks before finalizing:
  - Does each metric definition match how it is actually calculated?
  - Are any caveats or limitations understated or omitted?
  - Does the pipeline description match the actual process (not the ideal process)?
  - Would a non-technical auditor misread any section as a claim you cannot support?

IF any check fails → revise before proceeding
IF uncertain about accuracy → flag to user: "Please verify this pipeline description
   is accurate before I include it in the brief."
```

### Tone Guidelines

```
WRITE:    "Headcount is sourced from Workday HCM and reflects active employees
           as of the first day of the reporting month."
NOT:      "We pull headcount from Workday." (too vague)
NOT:      "Headcount is calculated using a proprietary extraction methodology
           aligned to enterprise data governance standards." (jargon wall)

WRITE:    "Attrition rate is calculated as total separations in the period
           divided by average headcount. It excludes internal transfers."
NOT:      "Attrition is a standard metric." (explains nothing)
```

### Exit Condition
Methodology narrative drafted for all SHARE and EXPLAIN items. Accuracy gate passed.
No unsupported claims in the document.

### Output
```
Methodology brief complete: [N] sections drafted
Accuracy flags resolved: [N]
Items flagged for user verification: [N]
Proceeding to anticipated questions.
```

---

## Phase 5: PREP QUESTIONS
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

Auditors ask the questions that expose gaps. Prepare for them before they surface
in the room. This phase produces a Q&A guide — anticipated questions with prepared,
defensible answers.

### Question Generation Framework

Generate anticipated questions across five categories:

#### Category 1: Methodology Questions
Auditors will probe how metrics are defined and calculated.

```
Examples:
- "How do you define 'active headcount'? Are contractors included?"
- "What is your data refresh cadence? How long is data stale before it's flagged?"
- "If two reports show different headcount numbers for the same org, why?"
- "Who validates the data before it reaches the executive dashboard?"
```

#### Category 2: Source and Lineage Questions
Auditors will trace data from system to report.

```
Examples:
- "Where exactly does this data come from in Workday?"
- "Who has access to pull this data? Is there a defined access list?"
- "Is there a reconciliation step between the raw extract and the published report?"
- "What happens when there's a data quality issue in the source system?"
```

#### Category 3: Scope and Coverage Questions
Auditors will test the boundaries of what is and is not measured.

```
Examples:
- "Does this include all global headcount or just U.S.?"
- "How are LOA employees handled? What about employees on PIP?"
- "Are contingent workers visible in any of these reports?"
- "What populations are intentionally excluded and why?"
```

#### Category 4: Governance and Control Questions
Auditors will assess whether controls exist and are followed.

```
Examples:
- "Who approves changes to the methodology?"
- "Is there documentation of how this metric has changed over time?"
- "How do you ensure consistency between fiscal year reporting periods?"
- "Who else reviews the executive dashboard before it goes to leadership?"
```

#### Category 5: Exception and Edge Case Questions
Auditors will probe for what happens when things go wrong.

```
Examples:
- "Has there ever been a material error in a report? How was it handled?"
- "What controls exist to prevent unauthorized changes to underlying data?"
- "If a headcount number looked wrong to an executive, what's the correction process?"
```

### Q&A Output Format

For each anticipated question, produce:

```yaml
qa_entry:
  id: "Q-001"
  category: methodology | source_lineage | scope_coverage | governance | exception
  question: "Exact question as an auditor would phrase it"
  prepared_answer: "Your response — factual, specific, and no longer than 3-4 sentences"
  supporting_evidence: "INV-[N] — what you would point to if asked for proof"
  if_you_dont_know: "Approved fallback: e.g., 'I'll confirm and follow up in writing by [date]'"
  risk_if_unprepared: low | medium | high
  notes: "anything to flag — e.g., this answer touches a known gap"
```

### High-Risk Q&A Flag

If a question has `risk_if_unprepared: high` and no clean prepared answer:
> "Q-[N] has no clean answer. This may indicate a process gap or a question that
> needs Legal or HR input before the audit session. Recommended action: [escalate /
> document the gap / prepare a 'we are working on this' response]."

### Exit Condition
Anticipated questions generated across all five categories. Every question has a
prepared answer or an approved fallback. High-risk gaps surfaced.

### Output
```
Q&A prep complete: [N] questions prepared
  Methodology: [N] | Source/lineage: [N] | Scope: [N]
  Governance: [N] | Exception: [N]
High-risk (unprepared): [N] — flagged for review
Proceeding to package assembly.
```

---

## Phase 6: PACKAGE
**Control Mode: DELEGATE** | **Entropy: E1-E2 (Deterministic-Procedural)**

Assemble the complete audit prep kit. Structured output. No new judgment — this
phase consolidates decisions made in Phases 1-5 into a single, usable artifact.

### Audit Prep Kit Structure

```markdown
# Audit Prep Kit
**Audit:** [AUDIT_SCOPE]
**Date:** [AUDIT_DATE]
**Auditor:** [AUDITOR_NAME]
**Prepared by:** [your name]
**Kit generated:** [date]

---

## Section 1: What to Bring

| Item | Disposition | File/Location | Redaction Needed? | Notes |
|------|-------------|---------------|-------------------|-------|
| [INV-001 name] | SHARE | [location] | No | — |
| [INV-002 name] | REDACT | [location] | Yes — see instructions | Remove names and WINs |
| [INV-003 name] | SENT | Already shared [date] | Verify version | — |
| [INV-004 name] | EXPLAIN | [location] | No | Bring context note |
| [INV-005 name] | HOLD | — | Do not bring | [rationale] |

---

## Section 2: Methodology Brief
[Full narrative from Phase 4 — one section per in-scope report/system]

---

## Section 3: Q&A Guide
[Full Q&A output from Phase 5 — organized by category]

---

## Section 4: What NOT to Say

These items are either out of scope, legally sensitive, or require escalation
before disclosure. If asked about them, use the approved response:

| Topic | Approved Response |
|-------|------------------|
| [HOLD item name] | "That falls outside the scope of this review. If you need that, I'd want to route that request through the appropriate channel." |
| Individual-level data | "Our policy is to share workforce data at the team level and above. I can provide aggregated views." |
| [Any other sensitive topic] | [Approved fallback from Q&A guide] |

---

## Section 5: Redaction Instructions
[For each REDACT item — specific fields, rows, or aggregation level required]

---

## Section 6: Pre-Brief Checklist

Before the audit session, confirm:
- [ ] All REDACT items have been scrubbed per redaction policy
- [ ] All SHARE items are the correct version (not draft, not superseded)
- [ ] SENT items — confirm auditor has the same version you have on file
- [ ] EXPLAIN items — context notes prepared and reviewable
- [ ] HOLD items are not in any folder or document you're bringing
- [ ] Q&A guide has been reviewed and you're comfortable with each answer
- [ ] You know your fallback phrase if asked something you cannot answer

```

### Exit Condition
Complete audit prep kit assembled. All six sections populated. Checklist ready.

### Output
```
Audit prep kit complete.
  Items to bring (SHARE + EXPLAIN + SENT): [N]
  Items requiring redaction: [N]
  Items on hold: [N]
  Q&A guide: [N] questions
  Pre-brief checklist: [N] items
Proceeding to follow-up tracker setup.
```

---

## Phase 7: FOLLOW-UP TRACKER
**Control Mode: DELEGATE** | **Entropy: E2 (Procedural)**

Post-audit commitment tracking. Everything you said you'd send, confirm, or
investigate in the audit session becomes a logged item with an owner and a date.

### Tracker Structure

```markdown
# Post-Audit Follow-Up Tracker
**Audit:** [AUDIT_SCOPE]
**Session date:** [AUDIT_DATE]
**Auditor:** [AUDITOR_NAME]

## Open Commitments

| ID | Commitment | Committed By | Due Date | Status | Notes |
|----|------------|-------------|---------|--------|-------|
| FU-001 | Send aggregated headcount by org level for Q1-Q3 FY27 | Josh Cramblet | [date] | Open | — |
| FU-002 | Provide methodology doc for attrition calculation | Josh Cramblet | [date] | Open | — |
| FU-003 | Confirm whether LOA employees are included in active headcount | Josh Cramblet | [date] | Open | — |

## Closed Commitments

| ID | Commitment | Completed On | Delivered Via | Notes |
|----|------------|-------------|---------------|-------|
| — | — | — | — | — |

## Auditor Requests (Not Yet Committed To)

| Request | Disposition | Rationale | Next Step |
|---------|-------------|-----------|-----------|
| [request] | Pending review | Requires HR/Legal input | Escalate by [date] |

## Session Notes
[Any observations, context, or flags from the audit session itself]
```

### Tracker Rules

1. Log every commitment made in the session, including verbal ones
2. Set a due date for every open item — default to 5 business days if not specified
3. Flag any request that was not committed to — document why and what the next step is
4. Update status to Closed only when the deliverable is confirmed sent and received
5. Share the tracker summary with the auditor as a written record if appropriate

### Escalation Trigger

If any open commitment is within 2 business days of its due date with no update:
> "FU-[N] ([commitment]) is due in [N] days and has no status update.
> Take action or update the due date."

### Exit Condition
All commitments from the audit session logged with owners and due dates.
Tracker is live and ready for ongoing updates.

### Output
```
Follow-up tracker initialized.
  Open commitments: [N]
  Due within 5 days: [N]
  Pending review (not committed): [N]
Tracker active — update as commitments are fulfilled.
```

---

## Operational Modes

### Mode 1: Full Prep (Default)
Run all 7 phases. Comprehensive intake through packaged kit. Ideal for a formal
audit engagement with scheduled review sessions.

**When:** 1-2 weeks before a scheduled audit walkthrough.
**Target:** Full kit ready in under 2 hours.

### Mode 2: Quick Classify
Run Phases 1-3 only. Intake + inventory + classification. Produces a disposition
table without the full narrative or Q&A.

**When:** Auditor has just made contact and you need to know immediately what you
can and cannot share.
**Target:** Classification complete in 30 minutes.

### Mode 3: Narrative Only
Run Phase 4 only against a provided inventory. Draft methodology brief without
full intake or classification workflow.

**When:** Auditor has specifically requested a methodology walkthrough document.
**Target:** Draft brief ready in 45 minutes.

### Mode 4: Q&A Drill
Run Phase 5 only. Generate anticipated questions and prepared answers from a
provided methodology document or description.

**When:** Pre-audit rehearsal or coaching another team member before a review session.
**Target:** Q&A guide complete in 30 minutes.

### Mode 5: Post-Audit Tracker
Run Phase 7 only. Set up follow-up tracker from notes taken during an audit session.

**When:** Immediately after the audit session, before commitments are forgotten.
**Target:** Tracker ready in 15 minutes.

---

## Anti-Patterns

```
AUDIT PREP ANTI-PATTERNS:

X "Share everything, let the auditor sort it out"
  Sharing unreviewed data is not transparency — it is a compliance risk.
  → ANCT diagnosis: DELEGATE applied to E3 work. Classification requires
    judgment. Every item must pass Phase 3 before it moves.

X "I'll explain it verbally in the room"
  Verbal explanations without written backup are not auditable. If you said it
  and didn't document it, you said nothing.
  → ANCT diagnosis: Phase 4 skipped. The narrative brief exists so your
    explanation is consistent, accurate, and on the record.

X "I know this data well enough, I don't need to prep questions"
  Knowing your data and knowing how to answer an auditor's framing of your data
  are different skills.
  → ANCT diagnosis: Phase 5 skipped. Auditor questions probe methodology gaps,
    not data familiarity. Prep for their frame, not yours.

X "I'll figure out redactions on the fly"
  Ad-hoc redaction in the moment introduces errors and inconsistency.
  → ANCT diagnosis: Phase 3 skipped. Redaction instructions must be documented
    and applied before the audit session, not during it.

X "We don't need to track what we committed to"
  Untracked commitments become unmet expectations that become findings.
  → ANCT diagnosis: Phase 7 skipped. Every verbal commitment made to an auditor
    is a documented expectation. Track all of them.

X "The auditor asked for something we hold — just say we'll look into it"
  Vague deferrals without a clear process raise more scrutiny than a direct,
  policy-grounded refusal.
  → ANCT diagnosis: Phase 5 unprepared. Your "What NOT to Say" responses must
    be specific, calm, and grounded in policy.

CORRECT PATTERNS:

✓ Classify before sharing — every item, every time
✓ Draft the narrative in writing before the audit session
✓ Prepare Q&A across all five categories, especially governance and exceptions
✓ Apply redaction policy consistently using documented instructions
✓ Bring a printed or accessible checklist to the audit session
✓ Log commitments immediately — during or right after the session
✓ Hold items are held, not deferred — know the difference and say so clearly
```

---

## Compliance Note

**PII Risk: High.** This skill operates directly on workforce data, org health
metrics, and headcount reporting that contains or derives from personally
identifiable information. All materials processed through this skill should be
treated as sensitive.

- Apply `{{REDACTION_POLICY}}` strictly. The default policy (redact individual
  names and employee IDs; aggregate to team level or above) is a minimum standard,
  not a ceiling.
- Do not share any output from this skill through unsecured channels.
- Consult HR and Legal before sharing anything classified as HOLD, before
  disclosing compensation data at any level, and before making commitments about
  future data access.
- The methodology brief and Q&A guide are internal prep documents — they are not
  automatically appropriate to share with auditors as-is. Review before sharing.
- Model recommendation: Sonnet for full prep workflow. Opus for high-ambiguity
  classification decisions or legal-adjacent Q&A drafting.

---

## Cross-References

This skill is designed to work alongside:

- **[mbr-deck-builder](../mbr-deck-builder/)** — The MBR exec summary dashboard
  built from Workday data is a primary artifact in scope for people analytics audits.
  Use mbr-deck-builder to understand what the deck contains before classifying it
  in Phase 3. The methodology brief in Phase 4 should align with how mbr-deck-builder
  describes its own data pipeline.

- **[org-data-pipeline](../org-data-pipeline/)** — The org data pipeline defines
  how headcount, org structure, and workforce metrics flow from source systems into
  reporting layers. Phase 4 methodology narratives should reference and align with
  the pipeline documentation produced by org-data-pipeline. If the two are
  inconsistent, resolve before the audit session.

---

## Design Credit

This skill's architecture was designed using the
[adaptive-workflow-architect](../adaptive-workflow-architect/) meta-skill,
applying Adaptive Narrative Control Theory (ANCT) to map each phase to its
optimal control mode based on entropy level. It cross-references
[mbr-deck-builder](../mbr-deck-builder/) as the primary upstream artifact source
and [org-data-pipeline](../org-data-pipeline/) as the authoritative data lineage
reference for methodology documentation.
