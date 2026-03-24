---
name: workday-roster-validator
description: "Validates whether Workday Worker Change History has propagated correctly into a downstream roster (PowerBI ARS, Workday snapshot, or equivalent). Joins on WIN, compares field-level Proposed values against roster values, and produces a three-sheet Excel reconciliation report with a prioritized action list."
version: 1.1.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - hr-data
  - workday
  - reconciliation
  - data-quality
  - roster-validation
  - ANCT-designed
model_recommendation: sonnet
risk_level: low
---

# 🔁 Workday Roster Validator

> Confirm Workday changes have landed — before your next reorg, cycle close, or audit.

When Workday processes transfers, promotions, manager changes, and cost center moves,
those changes should propagate downstream to PowerBI rosters, ARS exports, and headcount
systems within 24–48 hours. This skill automates the validation:

- Joins Workday change history to the roster on WIN (Associate ID)
- Handles Workday's compound field formats (location strings, code+name cost centers, position IDs)
- Aggregates multiple change rows per associate to capture all proposed changes
- Compares proposed values field-by-field against live roster values
- Produces a structured Excel report with a prioritized ⚠️ Action Required tab

**What this skill knows:**
- Workday reports use merged header rows — row 0 is the report title, row 1 is the column header
- Location strings encode building, state, and city in a compound format requiring extraction
- Job codes carry country prefixes (e.g., `US-100022465`) that must be stripped for comparison
- Manager names may include `(LAST_NAME)` annotations or ` - Team Name` suffixes
- Position fields combine a position code with the position description
- The same associate may have N change rows — all proposed values must be gathered and compared
- Changes dated after the roster snapshot date will not be reflected — this is expected, not an error

---

## 🔬 Core Philosophy

- **WIN is truth** — the join key is always WIN (Associate ID in changes, WIN Number in roster)
- **Proposed is the assertion** — the change report's "Proposed" column is what Workday committed to; the roster should match it
- **Normalize before comparing** — Workday and downstream systems use different formats for the same data; smart normalization prevents false positives
- **Classify mismatches by severity** — missing manager is different from missing WIN; the report must distinguish these
- **Snapshot date awareness** — changes after the roster snapshot date are expected to be missing; flag them as "pending", not "missing"

---

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake | E1 – Deterministic | DELEGATE | File paths + join key are known inputs |
| 2. Schema Discovery | E2 – Procedural | DELEGATE | Read headers, detect merged rows, map columns |
| 3. WIN Key Match | E1 – Deterministic | DELEGATE | Set intersection — no ambiguity |
| 4. Field-Level Comparison | E2 – Procedural | DELEGATE | Apply normalization rules per field type |
| 5. Report Production | E1 – Deterministic | DELEGATE | Structured Excel output from validated results |

**Circuit Breakers:**
- Phase 2: If `Associate ID` column not found → halt; surface available column names; ask user to confirm join key
- Phase 3: If match rate < 50% → pause; surface the unmatched WINs and ask whether the roster file is the right one
- Phase 4: If 0 field comparisons are possible (no overlapping field names after normalization) → halt and surface the field-mapping table for user correction

---

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{CHANGE_REPORT}}` | Workday Worker Change History Report (.xlsx or .csv) | file path | Yes | — |
| `{{ROSTER}}` | PowerBI / ARS roster export (.xlsx or .csv) | file path | Yes | — |
| `{{CHANGE_WIN_COL}}` | Column name for WIN in the change report | string | No | `Associate ID` |
| `{{ROSTER_WIN_COL}}` | Column name for WIN in the roster | string | No | `WIN Number` |
| `{{SNAPSHOT_DATE}}` | Date the roster was exported (YYYY-MM-DD) | date | No | auto-detect from filename or `Snapshot Date` column |
| `{{OUTPUT_PATH}}` | Where to write the reconciliation report | file path | No | same dir as change report, with `_Reconciliation.xlsx` suffix |
| `{{FIELDS_TO_VALIDATE}}` | Comma-separated list of change fields to compare. Use `all` to compare every available Proposed column | string | No | `all` |
| `{{INCLUDE_LOCATION}}` | Whether to include location comparison (often benign format diffs) | bool | No | `true` |

---

## ⚙️ Phases

---

### Phase 1: INTAKE
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Collect and validate all variables. Both files must be present and readable.

**Process:**
1. Confirm `{{CHANGE_REPORT}}` — note file name, size, sheet name
2. Confirm `{{ROSTER}}` — note file name, size, sheet name, approximate row count
3. Resolve `{{SNAPSHOT_DATE}}` — check filename for date pattern (e.g., `3.24.26`), or read `Snapshot Date` column from roster, or ask user
4. Apply defaults for optional variables
5. **Scan both files for PII** (legal names, WIN numbers, compensation data, manager chains). Both inputs will contain HR PII by design. Invoke `privacy-guardrail` before Phase 2 if content extends beyond expected HR operational fields into sensitive categories (health data, disciplinary records, salary amounts).
6. Produce an **Intake Summary** — **mandatory blocking output; do not proceed to Phase 2 without presenting it**:

```
INTAKE SUMMARY
─────────────────────────────────────────
Change report:    [filename] — [sheet] — [N rows]
Roster:           [filename] — [sheet] — [N rows]
Change WIN col:   [{{CHANGE_WIN_COL}}]
Roster WIN col:   [{{ROSTER_WIN_COL}}]
Snapshot date:    [resolved date]
Fields to validate: [all / specific list]
Include location: [yes / no]
Output path:      [resolved path]
PII scan:         [HR operational data (expected) / extended PII detected — privacy-guardrail invoked]
─────────────────────────────────────────
Proceeding to Phase 2: Schema Discovery.
```

**Output:** Resolved variable set, confirmed file access

---

### Phase 2: SCHEMA DISCOVERY
**Entropy Level:** E2 – Procedural
**Control Mode:** DELEGATE

Read the actual file structure of both inputs. Handle Workday's non-standard layout.

**2A: Change Report Schema**

Workday reports include a merged title row before the column headers:
- **Row 0** (or first row): Report title — e.g., `"Work History Summary"` — **skip this row**
- **Row 1**: Actual column headers — use these as field names
- **Row 2+**: Data rows

Read row 1 to extract column headers. Identify:
- WIN column: `Associate ID` (or `{{CHANGE_WIN_COL}}`)
- All `*- Current` columns: the before-state
- All `*- Proposed` columns: the after-state (these are the assertion columns)
- Metadata columns: `Legal Name in General Display Format`, `Effective Date`, `Business Process Type`, `Business Process Reason`

**2B: Roster Schema**

Standard single-header row. Read row 0 as column headers. Identify:
- WIN column: `WIN Number` (or `{{ROSTER_WIN_COL}}`)
- Field columns mapped to change report's Proposed columns (see Field Mapping Table below)

**2C: Field Mapping Table**

Build the field mapping — which Proposed column maps to which roster column.

**Default mappings:**

| Change Report — Proposed Column | Roster Column | Normalization Rule |
|---|---|---|
| `Job Code - Proposed` | `Job Code` | Strip country prefix (`US-`, `IN-`, `GB-`, etc.) |
| `Job Profile - Proposed` | `Job Description` | Direct string comparison (strip whitespace) |
| `Manager(s) - Proposed` | `Manager Name` | Strip `(LAST_NAME)` annotation; strip ` - Team` suffix |
| `Cost Center - Proposed` | `Cost Center #` | Extract first token (e.g., `US11919` from `US11919 11919 PD SUPPLY CHAIN FULFILLMENT`) |
| `Location - Proposed` | `Work City` + `Work State` | Extract city+state from Workday compound location string (see Location Parsing below) |
| `Position - Proposed` | `Position Description` | Strip position code prefix (`P_XXXXXXXX `); then strip leading `(COUNTRY) ` prefix from both sides before comparing |
| `Companies - Proposed` / `Company - Proposed` | `Segment` | Direct comparison |
| `Region - Proposed` | `L2 Area` | Direct comparison |

**Location Parsing — Workday Format:**

Workday location strings follow the pattern:
```
(Country) [Building Description] STATE_CODE CITY [Home Office|Campus|Site|...]
```

Examples:
- `(USA) Change Building AR Bentonville Home Office` → city=`BENTONVILLE`, state=`AR`
- `(USA) SUNNYVALE TECH CORNERS CA SUNNYVALE Home Office` → city=`SUNNYVALE`, state=`CA`
- `(USA) 221 River St NJ HOBOKEN Home Office` → city=`HOBOKEN`, state=`NJ`

**Extraction algorithm:**
1. Strip trailing `Home Office`, `Campus`, `Site`, `DC` (case-insensitive)
2. Find the last occurrence of a US 2-letter state code followed by city text
3. City = the text after the state code to end of string
4. Compare city (case-insensitive) against roster's `Work City`; compare state against `Work State`

**Present the Field Mapping Table before Phase 3 — mandatory output; do not proceed to Phase 3 without surfacing it.** If any Proposed column has no roster mapping, flag it as ❌ unmapped and confirm with the user whether to skip or manually map it.

```
FIELD MAPPING TABLE
─────────────────────────────────────────
Change Report Column       → Roster Column          Status
Job Code - Proposed        → Job Code               ✅ mapped
Job Profile - Proposed     → Job Description        ✅ mapped
Manager(s) - Proposed      → Manager Name           ✅ mapped
Cost Center - Proposed     → Cost Center #          ✅ mapped
Location - Proposed        → Work City / Work State ✅ mapped (with extraction)
Position - Proposed        → Position Description   ✅ mapped
Companies - Proposed       → Segment                ⚠️ verify
[Column X - Proposed]      → [no match found]       ❌ unmapped — will skip
─────────────────────────────────────────
```

**Circuit Breaker:** If `{{CHANGE_WIN_COL}}` not found in change report headers → halt; show available headers; ask user to correct.

**Output:** Confirmed schema for both files, resolved field mapping table

---

### Phase 3: WIN KEY MATCH
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Perform set intersection between WINs in the change report and WINs in the roster.

**Process:**
1. Extract all unique WINs from change report (`Associate ID`)
2. Build roster lookup dict: `WIN Number` → row record
3. Classify each change WIN:

| Status | Condition |
|---|---|
| **Matched** | WIN found in roster |
| **Not in Roster** | WIN not found in roster |
| **New Hire (expected)** | BP Type = `Hire` AND Effective Date ≥ snapshot date |
| **Terminated (expected)** | BP Type = `Terminate` — may not be in active roster |

4. Produce **WIN Match Summary** (mandatory output):

```
WIN KEY MATCH SUMMARY
─────────────────────────────────────────
Total unique WINs in change report: [N]
  ✅ Found in roster:               [N]
  ❌ Not in roster:                 [N]
     → New hires (expected):        [N]  (Hire BP on/after snapshot date)
     → Unexpected missing:          [N]  ⚠️ requires investigation
─────────────────────────────────────────
Unexpected missing WINs:
  [WIN] — [Name] — BP: [type] — Effective: [date]
  ...
─────────────────────────────────────────
```

**Circuit Breaker:** If match rate < 50% → pause and present:
```
⚠️ LOW MATCH RATE: Only [N]% of change report WINs found in roster.
This may mean:
  • The roster file is a different org/segment than the change report
  • The roster snapshot date is much earlier than the changes
  • The WIN column mapping is incorrect

Continue with field validation anyway? [Y / N / Adjust column mapping]
```

**Output:** Matched WIN set, not-in-roster list (with classification), match rate

---

### Phase 4: FIELD-LEVEL COMPARISON
**Entropy Level:** E2 – Procedural
**Control Mode:** DELEGATE

For every matched WIN, compare each mapped Proposed field against the roster value.

**Process:**
1. For each WIN, aggregate **all change rows** (there may be multiple per associate due to multi-step business processes)
2. For each mapped field, collect the set of all unique Proposed values across all change rows
3. Apply the normalization rule for that field type
4. Compare normalized proposed value(s) against normalized roster value
5. Classify result:

| Result | Condition |
|---|---|
| `✅ Match` | Any proposed value (after normalization) equals roster value |
| `⚠️ Mismatch` | No proposed value matches roster value (change not reflected) |
| `⏩ No Change` | Proposed column is empty or equals Current column (no change was made to this field) |
| `🕐 Pending` | Effective Date is after `{{SNAPSHOT_DATE}}` (expected not to appear yet) |

**Multi-row aggregation rule:** If an associate has 3 change rows and Manager is proposed as `A` in row 1 and `B` in row 2, and the roster shows `B`, report `✅ Match` — the most recent proposed value is what matters. Use Effective Date descending to determine recency for each field independently.

**Per-associate result record:**
```
WIN: [win]  Name: [name]
Overall Status: ✅ FULLY APPLIED | ⚠️ PARTIAL | ❌ NOT IN ROSTER
BP Types: [list]  |  Effective Dates: [list]

  Field                          Proposed          Roster        Match
  ─────────────────────────────────────────────────────────────────────
  Job Code - Proposed → Job Code  100022465        100022465     ✅
  Job Profile - Proposed → Job D…  (USA) Sr PM    (USA) Sr PM   ✅
  Manager(s) - Proposed → Mgr     Paul Saelzler   Paul Saelzler ✅
  Cost Center - Proposed → CC#    US11919         US11919        ✅
  Location - Proposed → City/St   BENTONVILLE, AR BENTONVILLE   ✅
  Position - Proposed → Pos Desc  (USA) Sr PM     (USA) Sr PM   ✅
```

**Severity Classification for Mismatches:**

| Severity | Field | Why |
|---|---|---|
| 🔴 High | Manager, Cost Center | Org structure errors; affect reporting chains and finance |
| 🟡 Medium | Job Code, Job Profile, Position | Compensation and leveling impact |
| 🟢 Low | Location | Often format differences; lower operational risk |

**Output:** Per-WIN field comparison results, overall status per associate

---

### Phase 5: REPORT PRODUCTION
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Generate a three-sheet Excel reconciliation report at `{{OUTPUT_PATH}}`.

**Sheet 1: Summary**
- Roster snapshot date, change report date range
- Total WINs: matched / partial / not-in-roster counts
- Genuine field mismatches (non-location) count
- Location-format-only flags count (informational)
- Generated timestamp

**Sheet 2: Reconciliation Detail**
- One block of rows per associate (merged identity cells)
- Columns: WIN | Name | Status | BP Types | Effective Dates | Field | Proposed Value (Workday) | Roster Value (PowerBI) | Match
- Color coding: green = match, yellow = mismatch, red = not in roster
- Frozen header row + column widths optimized for readability

**Sheet 3: ⚠️ Action Required**
- Only the records that need follow-up:
  - Genuine field mismatches (mismatch on non-location fields)
  - WINs not in roster that are NOT classified as expected new hires
- Columns: WIN | Name | Field | Proposed (Workday) | Roster Value (PowerBI) | BP Type | Severity
- Sorted by Severity (High → Medium → Low)

After saving, produce a **console reconciliation summary**:

```
RECONCILIATION COMPLETE
─────────────────────────────────────────
Roster snapshot:   [date]
Change date range: [min] – [max]

Total WINs:        [N]
✅ Fully applied:  [N]   ([N]% propagation rate)
⚠️ Partial match:  [N]
❌ Not in roster:  [N]   ([N] expected new hires, [N] unexpected)

Action required:   [N] associates, [N] field corrections
Report saved →     [{{OUTPUT_PATH}}]
─────────────────────────────────────────

TOP ISSUES:
  🔴 [WIN] [Name] — Manager not updated: [Proposed] → roster shows [Roster]
  🔴 [WIN] [Name] — Cost Center mismatch: [Proposed] → roster shows [Roster]
  ...
```

**Output:** Excel report at `{{OUTPUT_PATH}}` + console summary

---

## 🔧 Normalization Reference

This section is the canonical reference for field-type normalization. Apply these rules in Phase 4.

### Job Code
```
Input:  "US-100022465"  or  "IN_100022465"  or  "100022465"
Rule:   Strip leading 2–3 letter country prefix + separator (-, _, /)
Output: "100022465"
```

### Manager Name
```
Input:  "Paul Saelzler"
        "ARPAN BAJORIA (BAJORIA)"    ← strip parenthetical annotation
        "Ian Hanson - SC Product"    ← strip " - Team" suffix
Rule:   1. Strip trailing (ANNOTATION)
        2. Split on " - "; take first part
        3. Case-insensitive comparison
Output: "paul saelzler"
```

### Cost Center
```
Input:  "US11919 11919 PD SUPPLY CHAIN FULFILLMENT"
Rule:   Split on whitespace; take first token
Output: "US11919"
```

### Location (Workday → City/State)
```
Input:  "(USA) Change Building AR Bentonville Home Office"
Rule:   1. Strip trailing "Home Office" / "Campus" / "Site" (case-insensitive)
        2. Find last US state code (2-letter) + following city text
        3. City = text after state code to end; strip whitespace
Output: city="BENTONVILLE", state="AR"

Compare: city (case-insensitive) vs roster Work City
         state (exact, 2-letter) vs roster Work State
```

### Position Description
```
Input:  "P_0010902585 Staff, Product Manager"    ← Workday proposed (code + title)
        "(USA) Staff, Product Manager"            ← Roster value (country prefix + title)

Rule:   1. Strip leading "P_XXXXXXXX " prefix from proposed (P_ + digits + space)
        2. Strip leading "(COUNTRY) " prefix from BOTH sides — e.g. "(USA) ", "(IND) "
        3. Case-insensitive comparison on remaining title text

Output: "staff, product manager" == "staff, product manager"  → ✅ Match

Why:    Workday proposed encodes the position ID + raw title.
        Roster stores the fully qualified title with a country prefix.
        After stripping both artifacts, the job title itself is the true comparison target.
```

### Job Profile / Job Description
```
Input:  "(USA) Senior Product Manager"
Rule:   Direct string comparison; strip leading/trailing whitespace; case-insensitive
Output: "(usa) senior product manager"
```

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Compare raw Workday strings directly to roster values | Normalize each field type before comparison |
| Treat location mismatches the same as manager mismatches | Classify by severity; location diffs are often benign format variations |
| Use only the most recent change row per WIN | Collect all proposed values across all change rows; compare against roster; any match = ✅ |
| Report "Mismatch" for changes after the snapshot date | Classify as `🕐 Pending` — these are expected and should not appear in Action Required |
| Flag every new hire as "not in roster" without context | Distinguish Hire BP type + date; expected new hires are informational, not action items |
| Treat empty Proposed column as a change to blank | Empty Proposed = no change was made to this field; skip comparison for that field |
| Produce only a console summary | Always produce the Excel report — it's the deliverable for stakeholder review |

---

## 💡 Example Invocations

```
# Standard weekly change validation
"Validate this week's Workday change report against the PowerBI roster.
 Change report: /Downloads/Worker_Change_History_Report.xlsx
 Roster: /Documents/ARS_Roster_3.24.26_Power_BI.xlsx"

# With explicit date
"Run workday-roster-validator.
 Change file: ~/Downloads/changes_2026-03-28.xlsx
 Roster: ~/Documents/roster_3.28.26.xlsx
 Snapshot date: 2026-03-28"

# Location excluded (skip location comparison)
"Validate changes vs roster, skip location field"

# Specific fields only
"Only validate Manager and Cost Center changes"
```

---

## 📋 Expected Inputs — File Format Reference

### Workday Worker Change History Report
- Format: `.xlsx`
- Sheet: typically `Worker Change History Report` or the first sheet
- **Row 0**: Report title (e.g., `"Work History Summary"`) — **skip**
- **Row 1**: Column headers
- **Row 2+**: Data rows
- Key columns: `Associate ID`, `Legal Name in General Display Format`, `Effective Date`, `Business Process Type`, `Business Process Reason`, and paired `[Field] - Current` / `[Field] - Proposed` columns

### Roster Export (PowerBI ARS)
- Format: `.xlsx`
- Sheet: `Export` or first sheet
- **Row 0**: Column headers (single header row — no title row)
- **Row 1+**: Data rows
- Key columns: `WIN Number`, `Manager Name`, `Cost Center #`, `Job Code`, `Job Description`, `Work City`, `Work State`, `Position Description`

---

## 🔄 Recurring Use Pattern

This skill is designed for **weekly operational use** after Workday batch processing:

1. Workday processes batch changes (transfers, promotions, manager moves)
2. Changes propagate to downstream systems (24–48h)
3. PowerBI / ARS roster refreshes
4. **Run this skill** to verify propagation was complete
5. Escalate Action Required items to HRIS or data operations team
6. Rerun after corrections to confirm resolution

**Recommended schedule:** Run 2 business days after the Workday batch processing date.

---

## 📋 Compliance

**Data Sensitivity:** This skill processes HR data including names, WIN numbers, manager chains, cost centers, and compensation grade information. Treat all output files as sensitive — do not share reconciliation reports in public channels or attach to non-secured storage.

**PII Handling:** Change reports contain full legal names, WIN numbers, and org structure data. Do not log or cache file contents. The output report should be stored in the same secured location as the source files.

**Audit Trail:** The Excel report's Reconciliation Detail sheet serves as the audit record for each validation run. Retain per your org's data retention policy.

**Model Recommendation:** Sonnet — field-level comparisons and normalization logic benefit from strong analytical reasoning; the skill is mostly deterministic but exception classification requires nuanced judgment.
