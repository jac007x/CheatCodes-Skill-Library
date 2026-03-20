---
name: org-data-pipeline
description: "Universalized pipeline for pulling, reconciling, slicing, and reporting organizational data. Handles ad-hoc and recurring requests: ingest from any source, validate against a roster, cut by org dimensions, generate formatted reports, and distribute."
version: 1.0.0
author: jac007x
tags:
  - data-pipeline
  - reporting
  - org-analytics
  - reconciliation
  - heatmaps
  - cross-platform
  - automation
---

# 📊 Org Data Pipeline

A universalized, repeatable pipeline for turning raw organizational data requests
into validated, dimensionally-sliced, formatted reports — whether the ask is
ad-hoc ("pull me headcount by job family") or recurring ("monthly MBR data").

---

## 🧠 Core Philosophy

- **Never trust the source** — always validate and reconcile before reporting
- **Dimensions are the product** — raw totals are useless; cuts by org dimension drive decisions
- **Idempotent outputs** — same request + same data = same report, every time
- **Archive everything** — every pull gets timestamped and saved for audit trail
- **Self-serve is the goal** — recurring requests should become dashboards, not emails

---

## 🚀 Intake: Customize This Skill

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{DATA_SOURCE}}` | Where to pull data from | choice | ✅ | — |
| `{{SOURCE_DETAILS}}` | Connection string, file path, or API endpoint | string | ✅ | — |
| `{{ROSTER_FILE}}` | Path to authoritative roster for reconciliation | file-path | ❌ | `null` |
| `{{CUT_DIMENSIONS}}` | Org dimensions to slice by | list | ✅ | `[]` |
| `{{METRICS}}` | What to measure (headcount, turnover, tenure, etc.) | list | ✅ | `["headcount"]` |
| `{{FILTERS}}` | Standing filters (e.g., US-only, active associates) | dict | ❌ | `{}` |
| `{{OUTPUT_FORMAT}}` | How to deliver the report | choice | ❌ | `"html"` |
| `{{RECURRENCE}}` | One-time or recurring schedule | choice | ❌ | `"one-time"` |
| `{{PROJECT_NAME}}` | Prefix for output files | string | ❌ | `"report"` |
| `{{OUTPUT_DIR}}` | Where to save outputs | path | ❌ | `"./outputs"` |

### Data Source Options
- `PowerBI` — use powerbi sub-agent for DAX queries
- `BigQuery` — use bigquery-explorer sub-agent
- `Excel/CSV` — local file ingestion
- `Workday Report` — export from Workday, load as CSV/XLSX
- `API` — REST endpoint (provide URL + auth method)

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────┐
│               ORG DATA PIPELINE                    │
├───────────────────────────────────────────────────┤
│  REQUEST → ACQUIRE → RECONCILE → SLICE → REPORT    │
│     │         │          │          │        │      │
│     ▼         ▼          ▼          ▼        ▼      │
│  Parse     Pull from   Validate   Cut by   Format  │
│  intent    source(s)   vs roster  dims     & share  │
└───────────────────────────────────────────────────┘
```

---

## Phase 1: Request Parsing

**Goal:** Translate a natural language request into structured parameters.

Map the request to the intake variables:

| User Says | Maps To |
|-----------|---------|
| "by job family" | `CUT_DIMENSIONS += ["Job Family"]` |
| "for Sanjay's org" | `FILTERS["L3"] = "Sanjay"` |
| "last 12 months" | `FILTERS["date_range"] = "12mo"` |
| "headcount and turnover" | `METRICS = ["headcount", "turnover"]` |
| "as a slide" | `OUTPUT_FORMAT = "pptx"` |
| "every Monday" | `RECURRENCE = "weekly-monday"` |

---

## Phase 2: Data Acquisition

**Goal:** Pull data from the specified source.

### Source-Specific Strategies

**PowerBI:**
```
invoke_agent('powerbi', 'List datasets in workspace {{WORKSPACE_ID}},
  then run DAX: EVALUATE SUMMARIZECOLUMNS(...) with filters {{FILTERS}}')
```

**BigQuery:**
```
invoke_agent('bigquery-explorer', 'Query: SELECT {{METRICS}} FROM {{TABLE}}
  WHERE {{FILTERS}} GROUP BY {{CUT_DIMENSIONS}}')
```

**Excel/CSV:**
```python
def load_data(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, dtype=str)
    elif suffix in sx", ".xls"):
        return pd.read_excel(path, dtype=str)
    raise ValueError(f"Unsupported format: {suffix}")
```

### Data Freshness Check
- Log the data's last-modified timestamp
- Warn if data is > 7 days old for ad-hoc requests
- Warn if data is > 1 day old for recurring reports

---

## Phase 3: Reconciliation & Validation

**Goal:** Cross-reference against an authoritative roster and flag discrepancies.

```python
def reconcile(data: pd.DataFrame, roster: pd.DataFrame,
              join_key: str = "Employee ID") -> dict:
    """Compare data against roster. Return discrepancy report."""
    data_ids = set(data[join_key].dropna())
    roster_ids = set(roster[join_key].dropna())

    return {
        "in_data_not_roster": data_ids - roster_ids,
        "in_roster_not_data": roster_ids - data_ids,
        "matched": data_ids & roster_ids,
        "match_rate": len(data_ids & roster_ids) / max(len(data_ids), 1),
    }
```

### Validation Rules
- [ ] No duplicate employee IDs (warn + dedupe, keeping latest)
- [ ] Org dimension values are non-null for >90% of rows
- [ ] Numeric metrics parse correctly (no "N/A", "#REF!", etc.)
- [ ] Date fields are parseable and within expected range
- [ ] Match rate against roster > 95% (warn if lower)

---

## Phase 4: Dimensional Slicing

**Goal:** Cut the data by `{{CUT_DIMENSIONS}}` and compute `{{METRICS}}`.

```python
def slice_and_dice(df: pd.DataFrame, dimensions: list[str],
                   metrics: dict[str, str]) -> pd.DataFrame:
    """
    Group by dimensions, compute metrics.
    metrics = {"headcount": "count", "avg_tenure": ("Tenure", "mean")}
    """
    agg_spec = {}
    for name, spec in metrics.items():
        if spec == "count":
            agg_spec[name] = (dimensions[0], "count")
        elif isinstance(spec, tuple):
            agg_spec[name] = spec
    return df.groupby(dimensions, dropna=False).agg(**agg_spec).reset_index()
```

### Standard Metric Definitions

| Metric | Computation | Notes |
|--------|------------|-------|
| Headcount | Count distinct employee IDs | Active only |
| Turnover | Termed / Avg HC × 100 | Annualize if partial period |
| Avg Tenure | Mean of tenure-in-months | Exclude < 30 days |
| Open Reqs | Count open requisitions | From recruiting data |
| Span of Control | Direct reports per manager | Mean + distribution |
| Promo Rate | Promoted / Total HC × 100 | By level band |

---

## Phase 5: Report Generation

**Goal:** Format the sliced data into the requested output.

### HTML Dashboard (Default)
- Tailwind CSS + Chart.js
- Executive summary at top with key callouts
- Sortable data table
- Bar/line charts per metric
- Heatmap for multi-dimensional views
- Walmart colors: `#0053e2` primary, `#ffc220` accent
- Wrap Chart.js canvases in fixed-height container divs

### Excel
```python
def write_excel(df: pd.DataFrame, path: Path, sheet_name: str = "Report"):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
```

### Slide Deck
```
invoke_agent('slide-deck', 'Create a deck from this data: {{summary_json}}')
```

---

## Phase 6: Distribution & Archival

**Goal:** Deliver the report and archive it.

### Distribution Options
- `open` — open HTML on Mac with `open /path/to/report.html`
- `share-puppy` — publish to puppy.walmart.com
- `email` — send via msgraph agent
- `teams` — post to Teams channel via msgraph agent

### Archival
```
{{OUTPUT_DIR}}/
  {{PROJECT_NAME}}_{{YYYYMMDD}}.html
  {{PROJECT_NAME}}_{{YYYYMMDD}}.csv
  {{PROJECT_NAME}}_{{YYYYMMDD}}_reconciliation.json
  {{PROJECT_NAME}}_{{YYYYMMDD}}_audit.log
```

---

## 🛡️ Bulletproofing Checklist

- [ ] Always check data freshness before reporting
- [ ] Reconcile against roster when available
- [ ] Suppress cells with N < 5 (privacy threshold)
- [ ] Never expose individual-level data in shared reports
- [ ] Timestamp every output file for auditability
- [ ] Log every filter applied so the report is reproducible
- [ ] Validate that dimension columns have reasonable cardinality (<500 unique values)
- [ ] Test with a small filter first, then expand

---

## 📚 Example Applications

| Context | Data Source | Dimensions | Metrics | Output |
|---------|------------|------------|---------|--------|
| Monthly HC review | ARS PowerBI | L2, L3, Job Family | HC, Turnover | Slides |
| Ad-hoc MADA request | Budget report Excel | Cost Center, Leader | Spend, HC | Excel |
| Weekly hiring report | Workday Recruiting | Req Status, Org | Open Reqs, TTF | HTML |
| Quarterly talent review | Master Talent XLSX | Level, Perf Rating, Potential | HC, Promo Rate | Dashboard |
| Job family cleanup audit | Workday export | Job Family, Job Profile | Mismatch count | CSV |

---

## ⚠️ Anti-Patterns

```
❌ Sending raw exports without validation (always reconcile first)
❌ Hardcoding org dimension names (parameterize everything)
❌ Reporting on stale data without noting the refresh date
❌ Building a one-off script when a recurring dashboard would serve better
❌ Manually cutting the same data 20 ways (automate the dimension loop)
❌ Forgetting to suppress small-N cells (privacy violation risk)
❌ Emailing Excel files instead of sharing via OneDrive/SharePoint link
```

---

## 🌐 Platform Notes

| Platform | Compatible | Notes |
|----------|-----------|-------|
| code-puppy | ✅ | Activate with `/skill org-data-pipeline` |
| wibey | ✅ | Copy SKILL.md to `~/.wibey/skills/org-data-pipeline/` |
| Codex | ✅ | Paste as system prompt prefix |
| Any LLM | ✅ | Plain Markdown — paste as context |

---

## 🔁 Deployment Ladder

| Stage | Team | What to validate |
|-------|------|-------------------|
| **Refine** | Strategy & PMO | Reconciliation logic, metric definitions, output formatting |
| **Prove** | DAX People team | Cross-org dimension cuts, data source integrations |
| **Scale** | Walmart Home Office | Self-serve dashboard mode, recurring schedules, multi-source joins |
