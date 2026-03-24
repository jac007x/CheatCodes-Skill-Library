# Shared Intake Field Specification

> Standard intake variables used across CheatCodes skills. Skills that process communications, analytical outputs, or organizational data SHOULD use these field names for consistency. New skills should map their context-specific variables to these names where applicable.

---

## Standard Fields

| Variable | Description | Type | Required by Default | Example Values |
|----------|-------------|------|--------------------|--------------------|
| `{{OBJECTIVE}}` | The decision to be informed or action to be enabled by this output | string | Recommended | "Decide whether to proceed with reorg", "Inform Q3 board deck" |
| `{{AUDIENCE}}` | Who receives the output — name, role, or group | string | Recommended | "CHRO", "All Managers", "Finance leadership team" |
| `{{CHANNEL}}` | Output format or delivery mechanism | choice | Recommended | `email`, `deck`, `memo`, `verbal`, `one-pager`, `dashboard` |
| `{{DEADLINE}}` | When the output is needed | string | Optional | "Friday EOD", "Before 9am Monday", "Before the board meeting" |
| `{{SOURCE_MATERIAL}}` | Raw inputs — files, data, notes, threads, transcripts | file-path / string | Context-dependent | Path to CSV, pasted email thread, link to doc |
| `{{KNOWN_FACTS}}` | Pre-established facts, constraints, or context the output should respect | string | Optional | "Q3 attrition was 8.2%", "Budget is frozen until H2" |
| `{{CONSTRAINTS}}` | Limitations on the output — length, tone, scope, disclosure rules | string | Optional | "Max 1 page", "No financial details", "Executive tone only" |
| `{{CONFIDENCE_LEVEL}}` | Quality of the evidence or data behind the output | choice | Optional | `high` (validated data), `medium` (preliminary), `low` (estimates only) |
| `{{OWNER}}` | The person accountable for the output — requester or approver | string | Optional | "VP People Analytics", "jac007x" |
| `{{SENSITIVITY_LEVEL}}` | Privacy and people-data sensitivity of the content | choice | Situational | `low`, `medium`, `high`, `restricted` |

---

## Sensitivity Level Definitions

| Level | Definition | Handling |
|-------|-----------|----------|
| `low` | No personal data; aggregated or public information | Standard sharing; no special controls |
| `medium` | Aggregated people data with n≥10; no individual-level data | Limit distribution; confirm audience appropriateness |
| `high` | Individual-level data, performance data, or small-group aggregates (n<10) | Named recipients only; consider data masking |
| `restricted` | Medical, legal, investigation, or compensation data | Legal/HR approval required before sharing; do not distribute via standard channels |

---

## Confidence Level Definitions

| Level | Definition | Output Implication |
|-------|-----------|-------------------|
| `high` | Validated data from authoritative source; statistical methods applied | State findings confidently; include source |
| `medium` | Preliminary or partially validated data; reasonable assumptions made | Caveat findings; flag assumptions explicitly |
| `low` | Estimates, single data points, or unvalidated inputs | Lead with uncertainty; do not drive decisions without validation |

---

## Channel Format Conventions

| Channel | Structure | Typical Length | Audience Assumption |
|---------|-----------|---------------|---------------------|
| `email` | Subject → BLUF → context → ask/next step | 50–200 words | Busy; will skim |
| `memo` | Header → Situation → Recommendation → Supporting detail | 200–500 words | Will read fully |
| `deck` | Headline slide → supporting slides (1 idea per slide) | 5–12 slides | Will view, not read |
| `one-pager` | Headline → key points → recommendation → next step | 350–500 words | Reads in 2 minutes |
| `verbal` | Opening hook → 3 main points → call to action | 60–90 seconds | Listening, not reading |
| `dashboard` | KPI tiles → trend charts → drill-down tables | N/A | Self-serve exploration |

---

## Usage in Skills

Skills reference these fields using double-brace syntax: `{{OBJECTIVE}}`, `{{AUDIENCE}}`, etc.

When implementing a skill that needs one of these fields, use the exact variable name from this table. Do not create new names for the same concept (e.g., use `{{AUDIENCE}}` not `{{RECIPIENT}}` or `{{TARGET_AUDIENCE}}`).

Skills may define additional context-specific variables (e.g., `{{CORPUS_FILE}}`, `{{METRIC_CONCEPT}}`) when no standard field covers the concept.

---

## Skills Using This Schema

| Skill | Fields Used |
|-------|------------|
| `request-scope-builder` | OBJECTIVE, AUDIENCE, DEADLINE, CONSTRAINTS, SOURCE_MATERIAL, KNOWN_FACTS, CONFIDENCE_LEVEL |
| `executive-rewrite` | AUDIENCE, CHANNEL, OBJECTIVE, CONSTRAINTS, SENSITIVITY_LEVEL |
| `decision-memo-distiller` | OBJECTIVE, AUDIENCE, OWNER, DEADLINE, KNOWN_FACTS, SENSITIVITY_LEVEL, SOURCE_MATERIAL |
| `insight-narrative-builder` | SOURCE_MATERIAL, OBJECTIVE, AUDIENCE, CHANNEL, CONFIDENCE_LEVEL, CONSTRAINTS, KNOWN_FACTS |
| `status-update-normalizer` | SOURCE_MATERIAL, AUDIENCE, CHANNEL, OWNER, CONSTRAINTS |
| `objection-prep-simulator` | SOURCE_MATERIAL, AUDIENCE, OBJECTIVE, KNOWN_FACTS, CONSTRAINTS, SENSITIVITY_LEVEL |
| `metric-spec-builder` | OBJECTIVE, AUDIENCE, SOURCE_MATERIAL, CONSTRAINTS, OWNER |
| `change-comms-architect` | SOURCE_MATERIAL, OBJECTIVE, AUDIENCE, CHANNEL, DEADLINE, SENSITIVITY_LEVEL, CONSTRAINTS, OWNER |
| `output-router` | SOURCE_MATERIAL, CHANNEL, AUDIENCE, CONSTRAINTS, OBJECTIVE |
| `privacy-guardrail` | SOURCE_MATERIAL, AUDIENCE, CHANNEL, SENSITIVITY_LEVEL, CONSTRAINTS |
| `survey-nlp-analyzer` | SOURCE_MATERIAL, SENSITIVITY_LEVEL |
| `meeting-prep-assistant` | OBJECTIVE, AUDIENCE, CHANNEL |

---

*See [GOVERNANCE.md](../GOVERNANCE.md) for quality gate definitions. See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to add a new skill.*
