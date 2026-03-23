---
name: mbr-deck-builder
description: "End-to-end MBR deck production orchestrator — data extraction, analysis, visualization, slide design, visual QA, and iterative refinement. Coordinates 3 expert skills + 5 agents into a unified 6-phase pipeline."
version: 2.0.0
author: jac007x
tags:
  - mbr
  - monthly-business-review
  - presentation
  - data-analytics
  - visualization
  - orchestration
  - executive-reporting
  - walmart
---

# 🏗️ MBR Deck Builder — Production Orchestrator

Orchestrates the **complete Monthly Business Review deck pipeline** — raw data to polished, executive-ready presentation in 6 phases.

---

## 🧠 Core Philosophy

- **Data-driven storytelling** — every slide starts with data, not opinions
- **Executive-first design** — optimized for senior leadership consumption
- **Iterative refinement** — build, review, improve in tight loops
- **Reproducible** — same process every month, improving each cycle

---

## 📦 Resources

### 3 Expert Skills (activate as needed)

| Skill | Scope | Key Content |
|---|---|---|
| **`data-viz-expert`** | Chart selection + rendering | Decision tree, Tufte rules, color theory, Chart.js + matplotlib patterns, anti-patterns |
| **`pptx-expert`** | Slide creation + design | python-pptx API, McKinsey rules, layout grids, typography, tables, shapes, Walmart brand |
| **`slide-analyzer`** | Visual + structural QA | 7-dim rubric, 20+ automated checks, Pillow previews, WCAG audit, improvement workflows |

### 5 Agents (invoke as needed)

| Agent | Role |
|---|---|
| `data-analytics` | Query BQ/Databricks, build analysis |
| `bigquery-explorer` | Deep BQ table exploration |
| `powerbi` | Extract Power BI data |
| `slide-creator` | Generate HTML slide decks |
| `your-publishing-agent` | Publish to your publishing platform |

### Architecture

```
┌─────────────────────┐
│   mbr-deck-builder   │ ← ORCHESTRATOR
│    (Phase 1→6)       │
└──────────┬──────────┘
           │
   ┌────────┼────────┐
   │        │        │
┌──▼──┐ ┌──▼──┐ ┌──▼──┐
│ DATA │ │DESIGN│ │  QA  │
│LAYER │ │LAYER │ │LAYER │
├──────┤ ├──────┤ ├──────┤
│data- │ │pptx- │ │slide-│
│viz-  │ │expert│ │analy-│
│expert│ │      │ │zer   │
└──┬───┘ └──┬───┘ └──┬───┘
   │        │        │
┌──▼──┐ ┌──▼──┐ ┌──▼──┐
│ BQ   │ │slide-│ │image │
│ PBI  │ │cretr │ │tools │
│ CSV  │ │      │ │      │
└──────┘ └──────┘ └──────┘
```

---

## 🚀 The 6-Phase Pipeline

```
Phase 1         Phase 2         Phase 3         Phase 4         Phase 5         Phase 6
DATA GATHER  →  ANALYSIS     →  DECK BUILD   →  VISUAL QA    →  REFINE       →  DELIVER
Query BQ        Trends          Slide deck      Screenshot      Fix issues      Share link
Pull PBI        Comparisons     Charts          Analyze         Rebuild         Open deck
Get CSVs        Anomalies       Tables          Score           Re-score        Git commit
Prior MBR       Insights        KPIs            Recommend       Iterate         Archive
```

---

## 📖 Phase 1: Data Gathering

| Source | Agent/Tool |
|---|---|
| BigQuery | `bigquery-explorer` → `data-analytics` |
| Power BI | `powerbi` agent |
| CSV/Excel | `read_file` tool |
| Prior MBR | `load_image_for_analysis` |
| Targets | Ask user or query |

**Standard data points:** Current period · Prior period (MoM) · Same period LY (YoY) · Targets · Daily granularity · Segment breakdowns

**Validation:** No NULLs in key metrics · Correct date ranges · Sanity-checked values · Consistent units

---

## 📖 Phase 2: Analysis

For each metric compute:
```
Current Value:  $14.2M
vs Target:      ▲ 3.1% above ($13.8M)
vs Prior Month: ▲ 12.3% growth
vs Same Mo LY:  ▲ 8.7% YoY
Trend:          Accelerating (3mo avg ▲)
Anomalies:      Nov 15 spike (+45% DoD)
Key Driver:     E-commerce +22% MoM
```

**Insight rules:**
1. Lead with "so what" — “Revenue exceeded target by 3.1%, driven by e-commerce”
2. Quantify everything — “Improved 12.3% MoM” not “improved significantly”
3. Provide context — always vs target/prior/benchmark
4. Flag anomalies with root cause
5. Recommend action

---

## 📖 Phase 3: Deck Construction

### Standard MBR Slide Sequence

| # | Type | Content |
|---|---|---|
| 1 | Title | MBR title, period, team |
| 2 | Exec Summary | 4 KPI cards + 3 insights |
| 3 | Agenda | Section overview |
| 4-5 | KPI Deep Dive | Each KPI + trend chart |
| 6 | Monthly Trend | Daily line chart |
| 7 | Quarterly View | 3-month bar + targets |
| 8 | YoY Comparison | Same month across years |
| 9 | Segment Breakdown | Category/region split |
| 10 | Wins | What went well |
| 11 | Risks | RAG status table |
| 12 | Actions | Next month commitments |
| 13 | Appendix | Detailed data tables |

### Process
1. **Activate `pptx-expert`** — layout/typography/design rules
2. **Activate `data-viz-expert`** — chart selection + styling
3. Map each metric → best chart type
4. Write **action titles** for every slide
5. Build via `slide-creator` agent or `python-pptx`
6. Apply Walmart brand colors

### slide-creator Prompt Pattern
```
Slide 3 - "Revenue grew 12% MoM driven by e-commerce"
  Chart: Combo (bar=monthly revenue, line=target)
  Data: Jan=$10.2M, Feb=$11.1M, ... Dec=$14.2M
  Target line: $13.8M
  Highlight: December in blue.100, others in blue.60
```

---

## 📖 Phase 4: Visual QA

1. Screenshot each slide (or render previews)
2. **Activate `slide-analyzer`**
3. Load each image → apply 7-dimension rubric
4. **Target: ≥4.0/5.0** on every slide

### Auto-QA Checklist (no screenshots needed)
- [ ] Every slide has action title (verb + data)
- [ ] Every chart has labeled axes with units
- [ ] Every data slide has source citation
- [ ] KPI cards show delta vs target/prior
- [ ] Walmart brand palette throughout
- [ ] No slide >100 words · No pie >5 slices
- [ ] Chart.js canvases in fixed-height containers
- [ ] Numbers right-aligned in tables
- [ ] Green=positive, Red=negative consistently

---

## 📖 Phase 5: Refinement

```
while score < 4.0 or user_has_feedback:
    1. Collect feedback (analysis or user)
    2. Identify specific changes
    3. Apply fixes
    4. Re-evaluate
```

| User Says | Action |
|---|---|
| "Make chart bigger" | Increase container (300→450px) |
| "Change chart type" | `data-viz-expert` → select better type |
| "Simplify" | Remove secondary elements, one message |
| "Colors wrong" | Apply Walmart palette from `pptx-expert` |
| "Table too busy" | Remove cols, add formatting, or convert to chart |

---

## 📖 Phase 6: Delivery

1. **Open** — `open presentation.html` (Mac) / `start` (Win)
2. **Share** — `your-publishing-agent` agent → your publishing platform
3. **Git** — `git commit -m 'MBR Dec 2025 deck v1'`
4. **Archive** — `mbr/2025-12/presentation.html`

---

## 🔄 Handling Existing Decks

### Screenshots/images provided
1. Load → `slide-analyzer` rubric → extract data → confirm → rebuild → compare

### PPTX file provided
1. `audit_deck('file.pptx')` → structural analysis + previews
2. `slide-analyzer` rubric on preview images
3. Generate python-pptx fixes via `pptx-expert`
4. Apply programmatically + re-export

### Raw data + old structure
1. Review old narrative flow
2. Identify improvements via skills
3. Rebuild with better viz + design

---

## 🎯 Quick Commands

| Command | Workflow |
|---|---|
| "Build me an MBR" | Full Phase 1→6 |
| "Analyze this slide" | Phase 4 only |
| "Improve this chart" | Load → analyze → suggest → rebuild |
| "Review the deck" | Multi-slide analysis + consistency |
| "Make it exec-ready" | Full QA + refine until ≥4.0 |
| "Run design audit" | `python runner.py DESIGN_AUDIT` |
