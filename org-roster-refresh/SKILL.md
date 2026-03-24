---
name: org-roster-refresh
description: "Operationalizes the recurring org roster refresh workflow: parse an inbound request (by leader, org, cost center, or segment), pull the latest snapshot from your HR system of record (Workday, ARS, or equivalent), validate freshness against known recent changes, slice and format the output as xlsx or summary, cross-check headcount against the prior snapshot, and deliver a structured summary of what changed and any anomalies."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - roster-management
  - workday
  - org-data
  - hr-analytics
  - workflow-automation
  - ANCT-designed
model_recommendation: haiku
risk_level: low
designed_with: adaptive-workflow-architect
---

# Org Roster Refresh

> Pull, slice, validate, and deliver — without skipping the freshness check.

People Partners submit roster refresh requests multiple times per week. The pattern is always the same: pull the latest associate data from {{HR_SOURCE}}, slice it by a dimension (L3 leader, org, cost center, or segment), validate that recent HR system uploads have landed, format the output as xlsx or a written summary, and deliver with a clear change narrative. This skill encodes that end-to-end workflow so it runs consistently every time, regardless of which dimension is requested or who is asking.

**What this skill knows:**
- Roster requests arrive as plain-language emails — they need to be parsed into a structured execution plan before any data is touched
- {{HR_SOURCE}} exports have different freshness windows; a snapshot that is 48 hours old may not reflect an org move that processed this morning
- Slicing by leader versus by cost center versus by segment produces different output shapes — the format step must adapt to the dimension
- Headcount anomalies are only visible if you compare to a prior snapshot; delivering a point-in-time roster without a delta narrative misses the most useful part of the answer
- PII is inherent to this data; delivery channel matters as much as output format

---

## Core Philosophy

- **Freshness first** — do not slice or format until you have confirmed whether the source data reflects known recent Workday activity; a stale roster delivered confidently is worse than a delayed one
- **Dimension drives format** — the slice dimension (leader / org / CC / segment) determines column selection, sort order, and output tab structure; resolve this before touching data
- **Delta is the deliverable** — the recipient already knows the roster exists; what they need is what changed, who moved, and what headcount anomalies appeared since the last run
- **Anomalies surface up** — unexpected headcount shifts, people in the wrong org or CC, and associates absent from their expected leader's slice must be called out explicitly, not buried in a data tab
- **Secure channel, not email attachment** — roster output files contain PII (WIN numbers, names, compensation grade) and must travel via OneDrive or equivalent secured share, never as broad-list email attachments

---

## ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Parse Request | E1 – Deterministic | DELEGATE | Structured extraction from plain-language email; variables are well-defined |
| 2. Pull Source Data | E1 – Deterministic | DELEGATE | File read or API pull against a known source; no ambiguity if path is resolved |
| 3. Validate Freshness | E2 – Procedural | DELEGATE | Compare snapshot date to known recent Workday activity; requires judgment on staleness threshold |
| 4. Slice and Format | E2-E3 – Procedural to Interpretive | DELEGATE | Dimension logic is rule-based; output formatting requires layout decisions |
| 5. Cross-Check | E3 – Interpretive | DELEGATE | Anomaly detection against prior snapshot; requires judgment on what constitutes a meaningful delta |
| 6. Deliver | E1 – Deterministic | DELEGATE | Structured summary from validated outputs; format is fixed |

**Circuit Breakers:**
- Phase 1: If `SLICE_BY` cannot be resolved from `REQUEST_TEXT` → pause; present candidate interpretations and ask requester to confirm before proceeding
- Phase 2: If source file is not found at `SOURCE_PATH` → halt; surface the expected path; ask whether to use a cached snapshot or wait for a fresh pull
- Phase 3: If source snapshot date is more than 48 hours older than the most recent known Workday upload → flag as stale and require explicit requester acknowledgment before Phase 4
- Phase 5: If headcount delta vs prior snapshot exceeds 5% in either direction → surface as a high-priority anomaly before generating the delivery summary; do not bury in the data

---

## Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{REQUEST_TEXT}}` | Plain-language email or message from the requester | string | Yes | — |
| `{{SOURCE_PATH}}` | File path to {{HR_SOURCE}} export, HR system snapshot, or cached roster file | file path | Yes | — |
| `{{SLICE_BY}}` | Dimension to slice on: `leader`, `org`, `cc`, or `segment` | enum | Yes | — |
| `{{PRIOR_SNAPSHOT_PATH}}` | File path to the previous roster run, for delta comparison | file path | No | — (delta section skipped if absent) |
| `{{OUTPUT_FORMAT}}` | Desired output: `xlsx`, `summary`, or `both` | enum | No | `both` |
| `{{REQUESTER}}` | Name of the person who submitted the request | string | No | inferred from `REQUEST_TEXT` |
| `{{HR_SOURCE}}` | The HR data source to pull from (e.g., ARS, Workday, SuccessFactors, BambooHR) | string | Yes | — |

---

## Phases

---

### Phase 1: PARSE REQUEST
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Extract the structured execution plan from the plain-language request before touching any data.

**Process:**
1. Read `{{REQUEST_TEXT}}` and extract:
   - **Requester** — who sent it (name and role if present)
   - **Slice dimension** — resolve to one of: `leader`, `org`, `cc`, `segment`; if ambiguous, surface candidates and pause
   - **Validation needed** — does the requester mention confirming counts, checking a specific person, or validating recent moves? (`yes` / `no`)
   - **Output format** — explicit mention of xlsx, summary, email, deck? Map to `xlsx`, `summary`, or `both`
   - **Deadline** — any urgency signal ("by EOD", "before the 2pm call", "ASAP")
   - **Scope modifier** — is this a full-org refresh or a targeted pull (e.g., "just Tarun and his team")?
2. Apply defaults for any unspecified variables
3. Produce a **Parse Summary** — **mandatory blocking output; do not proceed to Phase 2 without presenting it:**

```
PARSE SUMMARY
─────────────────────────────────────────
Requester:        [name / role]
Slice by:         [leader / org / cc / segment]
Scope modifier:   [full org / specific leader or filter]
Validation:       [yes / no]
Output format:    [xlsx / summary / both]
Deadline:         [resolved deadline or "none specified"]
Source path:      [{{SOURCE_PATH}}]
Prior snapshot:   [{{PRIOR_SNAPSHOT_PATH}} / none — delta will be skipped]
─────────────────────────────────────────
Proceeding to Phase 2: Pull Source Data.
```

**Circuit Breaker:** If `SLICE_BY` is ambiguous (e.g., request mentions both a leader name and a cost center) → pause and ask: "Should I slice by leader (showing all associates under [Name]) or by cost center ([CC#])?"

**Output:** Resolved variable set ready for Phase 2

---

### Phase 2: PULL SOURCE DATA
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Load the source roster data from the file or export identified in `{{SOURCE_PATH}}`.

**Process:**
1. Open `{{SOURCE_PATH}}` and detect format (xlsx or csv)
2. Read column headers — confirm the following core columns are present:

| Required Column | Notes |
|-----------------|-------|
| `WIN` or `WIN Number` | Associate ID — primary join key |
| `Name` or `Legal Name` | Full associate name |
| `L3 Leader` | Third-level leader in the org hierarchy |
| `Org` or `Organization` | Org unit name |
| `Cost Center` or `Cost Center #` | Cost center code |
| `Job Family` | Job family grouping |
| `Level` or `Job Level` | Career level |
| `Segment` | Business segment (if applicable) |

3. Note the file's snapshot date — check filename for date pattern (e.g., `3.24.26`, `2026-03-24`), or read a `Snapshot Date` or `As Of` column if present
4. Record row count as the total population in this snapshot
5. Produce a **Source Summary** (inline, not a blocking pause):

```
SOURCE LOADED
─────────────────────────────────────────
File:             [filename]
Format:           [xlsx / csv]
Sheet:            [sheet name]
Row count:        [N associates]
Snapshot date:    [resolved date]
Core columns:     [present / missing: list any missing]
─────────────────────────────────────────
```

**Circuit Breaker:** If `{{SOURCE_PATH}}` does not resolve to a readable file → halt; surface the expected path; ask whether to use a different file or wait for a fresh export.

**Circuit Breaker:** If any required column is missing → pause; show the available column headers; ask the requester to confirm the correct column mapping before slicing.

**Output:** Loaded roster dataframe, confirmed schema, resolved snapshot date

---

### Phase 3: VALIDATE FRESHNESS
**Entropy Level:** E2 – Procedural
**Control Mode:** DELEGATE

Confirm whether the source snapshot reflects the most recent known Workday activity before any output is generated.

**Process:**
1. Compare the snapshot date (from Phase 2) against:
   - Today's date — flag if the snapshot is more than 2 business days old
   - Any known recent Workday upload referenced in `{{REQUEST_TEXT}}` (e.g., "the 3.16 enriched roster" implies an upload event on or around 3/16)
2. Check whether the `{{REQUEST_TEXT}}` mentions specific recent changes (e.g., a person's org move, a cost center update) — if so, attempt to confirm those changes are visible in the loaded data
3. Classify freshness:

| Status | Condition |
|--------|-----------|
| `Fresh` | Snapshot is current (within 2 business days) and no stale signals detected |
| `Stale — flagged` | Snapshot is older than 2 business days OR request references a Workday upload not yet reflected |
| `Unverifiable` | Cannot determine snapshot date; proceed with caution flag |

4. Produce **Freshness Assessment** (inline):

```
FRESHNESS ASSESSMENT
─────────────────────────────────────────
Snapshot date:    [date]
Today:            [date]
Age:              [N business days]
Status:           [Fresh / Stale — flagged / Unverifiable]
Notes:            [e.g., "Request references 3.16 upload — confirm changes landed"]
─────────────────────────────────────────
```

**Circuit Breaker:** If status is `Stale — flagged` → pause and surface:
```
FRESHNESS WARNING
The source snapshot is [N] business days old [and/or] may not reflect [known change].
Delivering a stale roster without flagging this would be misleading.

Options:
  1. Proceed and include a freshness caveat in the delivery summary
  2. Pull a fresh export before continuing
  3. Proceed for a specific targeted validation only (e.g., confirm one leader's count)

How would you like to proceed?
```

**Output:** Freshness classification, any staleness flags to carry into the delivery summary

---

### Phase 4: SLICE AND FORMAT
**Entropy Level:** E2-E3 – Procedural to Interpretive
**Control Mode:** DELEGATE

Apply the dimension slice from `{{SLICE_BY}}` and produce the output in the format specified by `{{OUTPUT_FORMAT}}`.

**Process:**

**4A: Apply the Slice**

| Slice Dimension | Logic |
|-----------------|-------|
| `leader` | Group rows by `L3 Leader`; produce one section or tab per leader; sort associates by Name within each group |
| `org` | Group rows by `Org`; produce one section or tab per org unit |
| `cc` | Group rows by `Cost Center` / `Cost Center #`; produce one section or tab per cost center code |
| `segment` | Group rows by `Segment`; produce one section or tab per segment |

If a scope modifier was identified in Phase 1 (e.g., "just Tarun"), filter to that leader or cost center before slicing.

**4B: Output Columns**

Include these columns in the output, in this order:

| # | Column | Source |
|---|--------|--------|
| 1 | WIN | WIN / WIN Number |
| 2 | Name | Name / Legal Name |
| 3 | L3 Leader | L3 Leader |
| 4 | Org | Org / Organization |
| 5 | Cost Center | Cost Center / Cost Center # |
| 6 | Job Family | Job Family |
| 7 | Level | Level / Job Level |

Include `Segment` as column 8 if `SLICE_BY = segment` or if the request references segment-level distribution.

**4C: Format Output**

- If `OUTPUT_FORMAT = xlsx` or `both`:
  - Produce one Excel workbook with one tab per slice group (e.g., one tab per L3 leader)
  - Include a Summary tab: total headcount, headcount per group, snapshot date, generated timestamp
  - Frozen header rows; column widths optimized for readability
  - Apply conditional formatting: highlight any row where a required field (L3 Leader, Cost Center, Org) is blank

- If `OUTPUT_FORMAT = summary` or `both`:
  - Produce a written summary block per group: group name, headcount, any notable composition (e.g., job family breakdown if relevant to request)

**Output:** Formatted xlsx file and/or written summary, ready for cross-check

---

### Phase 5: CROSS-CHECK
**Entropy Level:** E3 – Interpretive
**Control Mode:** DELEGATE

Compare the current slice output against the prior snapshot to surface headcount changes and anomalies. Skip this phase if `{{PRIOR_SNAPSHOT_PATH}}` is not provided; note the skip in the delivery summary.

**Process:**
1. Load `{{PRIOR_SNAPSHOT_PATH}}` and apply the same slice dimension used in Phase 4
2. Compare per-group headcount: current vs prior

| Delta Signal | Condition |
|--------------|-----------|
| Expected growth/attrition | 1–3 associate delta within a group; no further investigation needed |
| Anomalous increase | More than 5% headcount increase in a group — flag for review |
| Anomalous decrease | More than 5% headcount decrease in a group — flag for review |
| Group appeared | A slice group (leader / org / CC) present in current snapshot but not in prior — flag as new |
| Group disappeared | A slice group present in prior but absent from current — flag as dissolved or merged |

3. Identify associates who moved between groups: appear under a different leader / org / CC in current vs prior
4. Identify associates present in prior but absent in current (potential terminations or data issues)
5. Identify associates present in current but absent in prior (new hires or transfers in)
6. Classify all findings as: expected (hire BP, transfer), flagged (unexpected), or data quality (WIN mismatch, blank fields)

**Produce Cross-Check Summary:**

```
CROSS-CHECK SUMMARY
─────────────────────────────────────────
Prior snapshot:     [filename] — [date]
Current snapshot:   [filename] — [date]

Total headcount:    Prior [N] → Current [N] (delta: [+/-N])

Per-group deltas:
  [Group Name]      Prior [N] → Current [N]  [status]
  ...

Associates moved between groups:    [N]
  [WIN] [Name] — was: [prior group] → now: [current group]

New to roster (not in prior):       [N]
  [WIN] [Name] — [hire/transfer/data?]

Missing from current (in prior):    [N]
  [WIN] [Name] — [term/transfer out/data?]

Anomalies flagged:                  [N]
  [description of each anomaly]
─────────────────────────────────────────
```

**Circuit Breaker:** If headcount delta exceeds 5% in any group → surface as a high-priority anomaly and require acknowledgment before Phase 6. Do not deliver without surfacing this.

**Output:** Cross-check summary, anomaly list, movement table

---

### Phase 6: DELIVER
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Produce the final delivery summary for the requester. This is the artifact the requester uses to understand what was pulled, what changed, and what needs attention.

**Process:**
1. Assemble all outputs: xlsx file (if applicable), written summary (if applicable), cross-check delta (if applicable), freshness flags (if any)
2. Produce a **Delivery Summary:**

```
ROSTER REFRESH COMPLETE
─────────────────────────────────────────
Request:          [brief plain-language description of what was asked]
Requester:        [name]
Slice by:         [leader / org / cc / segment]
Source:           [filename] — snapshot date: [date]
Freshness:        [Fresh / Stale — see caveat below]
Generated:        [timestamp]

Headcount:        [N] total associates
  By [dimension]: [Group A: N | Group B: N | ...]

Changes vs prior: [N associates moved, N new, N missing — or "no prior snapshot provided"]

Anomalies:        [N flagged — see below / none]

Output:           [xlsx saved to: [path] / summary below]
─────────────────────────────────────────

ANOMALIES:
  [description of each anomaly, or "None detected"]

FRESHNESS CAVEAT (if applicable):
  Snapshot is [N] business days old. [Known change] may not be reflected.
  Recommend re-running after [expected upload date or event].

DELIVERY NOTE:
  Share output file via OneDrive only. Do not attach to broad-list email.
─────────────────────────────────────────
```

**Output:** Delivery summary + output file(s) ready for sharing

---

## Anti-Patterns

| Wrong | Right |
|-------|-------|
| Deliver the roster without noting its snapshot date | Always surface the snapshot date and freshness classification in the delivery summary |
| Slice the data before validating whether recent Workday uploads have completed | Phase 3 (Validate Freshness) must complete and be acknowledged before Phase 4 begins |
| Produce only raw data output without a delta narrative | Always compare against prior snapshot when one is available; the delta is the most useful part |
| Bury headcount anomalies in a data tab | Surface anomalies explicitly in the cross-check summary and delivery summary before finalizing |
| Share the output xlsx as a broad-list email attachment | Route all PII-containing output files through OneDrive or equivalent secured channel |
| Proceed when `SLICE_BY` is ambiguous | Pause at Phase 1 and confirm the dimension with the requester before any data access |
| Treat a 5%+ headcount swing as normal without flagging | Circuit-break at Phase 5 and require explicit acknowledgment before delivering |

---

## Example Invocations

```
# Standard leader refresh (most common pattern)
"Refresh the roster by leader for L3 distribution.
 Source: /OneDrive/ARS_Roster_3.24.26.xlsx
 Prior: /OneDrive/ARS_Roster_3.16.26.xlsx"

# Targeted single-leader pull with validation
"Pull just Tarun and validate his associate count.
 Source: /OneDrive/ARS_Roster_3.23.26.xlsx"

# Enriched roster update after a known Workday upload
"Update the 3.16 enriched roster by leader — Workday upload completed this morning.
 Source: /OneDrive/Enriched_Roster_3.24.26.xlsx
 Prior: /OneDrive/Enriched_Roster_3.16.26.xlsx
 Output: both"

# Cost center slice for finance review
"Pull the full org roster sliced by cost center, xlsx output.
 Source: /OneDrive/ARS_Roster_3.24.26.xlsx"

# Segment-level summary only
"Need a quick headcount summary by segment, no xlsx needed."
```

---

## Cross-References

| Skill | Relationship |
|-------|-------------|
| `workday-roster-validator` | Validation logic — when the request specifically asks to confirm whether a Workday change has landed in the roster, hand off to workday-roster-validator for field-level reconciliation |
| `org-data-pipeline` | Source pipeline — if `SOURCE_PATH` is not a static file but a live pipeline, org-data-pipeline manages the pull and refresh cadence |
| `mada-mtda-tracker` | Award eligibility — roster composition (headcount, org, cost center) sometimes gates MADA/MTDA award eligibility; cross-reference when requests mention award cycles |

---

## Compliance

**Data Sensitivity:** PII High. Roster output contains WIN numbers (Associate IDs), full legal names, manager chains, cost centers, job families, and levels. All output files are sensitive HR data.

**PII Handling:**
- Do not log, cache, or store roster file contents outside the intended output path
- Output files must be shared only via secured channels (OneDrive, SharePoint) — never as broad-list email attachments
- If a request routes output to an unsecured destination, flag this before Phase 6 and ask the requester to confirm a secured path

**Audit Trail:** The delivery summary serves as the run record for each refresh — retain it alongside the output file per your org's data retention policy.

**Model Recommendation:** Haiku — this is a procedural, deterministic workflow with well-defined inputs and outputs. The logic is rule-based and does not require deep analytical reasoning. Haiku handles the extraction, slicing, formatting, and delta comparison accurately and efficiently.
