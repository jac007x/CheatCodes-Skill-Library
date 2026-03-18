# MBR Engine Skill

**Monthly Business Review automation** - Extract org health metrics from HR data, detect feature-worthy patterns, and generate PowerPoint presentations.

## Overview

The MBR Engine automates the creation of Monthly Business Reviews by:
1. **Extracting** metrics from HR roster, finance, turnover, and recognition data
2. **Detecting** patterns and anomalies worth highlighting
3. **Generating** formatted PowerPoint slides with tables, charts, and narratives

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        MBR ENGINE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │  DELTA   │    │   NOVA   │    │   PPTX   │                  │
│  │ (Extract)│───▶│(Analyze) │───▶│ (Build)  │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
│       │               │               │                         │
│       ▼               ▼               ▼                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │  Roster  │    │ Feature  │    │  Slides  │                  │
│  │ Finance  │    │  Engine  │    │  Tables  │                  │
│  │ Turnover │    │ Patterns │    │  Charts  │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                     GOVERNANCE LAYER                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ Thresholds │  │ Persistence│  │ Portability│               │
│  │ & Reviews  │  │ & Tracking │  │ & Onboard  │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. DELTA (Data Extraction Layer)
Extracts structured metrics from raw data files.

| Extractor | Source | Metrics |
|-----------|--------|---------|
| `OrgHealthExtractor` | HR Roster | IC:Mgr Ratio, Avg Span, Max Layers, Remote % |
| `HeadcountExtractor` | Finance | HC vs AOP, MoM Change |
| `TurnoverExtractor` | HR Reports | Total/Voluntary Turnover |
| `RecognitionExtractor` | MADA | Budget Utilization |

### 2. Feature Engine
Detects patterns worth highlighting in the MBR.

**Pattern Categories:**
- `MOM_SPIKE` - Significant month-over-month changes
- `THRESHOLD_BREACH` - Metrics outside healthy ranges
- `GEOGRAPHIC_SPLIT` - Regional variations
- `L3_OUTLIER` - Individual org anomalies

**Scoring Formula:**
```
Score = (Magnitude × 0.30) + (Breadth × 0.25) + (Strategic × 0.25) + (Novelty × 0.20)
```

### 3. PPTX Builder
Generates formatted PowerPoint slides.

**Slide Types:**
- Title slides
- Org Health tables (with color-coded thresholds)
- HC vs AOP charts
- Recognition utilization
- Feature deep-dives

### 4. Threshold Governance
Manages metric thresholds with continuous improvement.

**Features:**
- Org-specific thresholds (Tech vs Services vs AIPD)
- Color coding (GREEN/YELLOW/RED)
- Quarterly reviews (Feb, May, Aug, Nov)
- Annual calibration (December)
- Gradual change control (max 2 points/quarter)

### 5. Portability Layer
Makes the engine work with any organization.

**Components:**
- `OrgRegistry` - Define any org at any depth
- `SchemaRegistry` - Handle different data formats
- `MetricRegistry` - Drop/add metrics based on data availability
- `ThresholdDiscovery` - Auto-recommend thresholds from context
- `OrgOnboarding` - Guided setup for new orgs

## Quick Start

```python
from mbr_engine import MBRWorkflow, MBRSourceFiles

# Define source files
sources = MBRSourceFiles(
    roster_file="~/Downloads/Roster for MBR.xlsx",
    mada_file="~/Downloads/MBR_Budget_report_query.xlsx",
)

# Create workflow
workflow = MBRWorkflow(
    sources=sources,
    month="2026-03",
    output_dir="./output",
)

# Run extraction and analysis
result = workflow.run()

# Review detected topics
for topic in result.feature_topics[:5]:
    print(f"{topic.score:.0f} | {topic.title}")

# Generate slides
workflow.generate_slides(
    result,
    selected_topics=result.feature_topics[:2],
    output_filename="MBR_March_2026.pptx"
)
```

## Metrics Reference

### Org Structure Metrics

| Metric | Description | Direction | Tech Threshold | Services Threshold |
|--------|-------------|-----------|----------------|-------------------|
| IC:Manager Ratio | ICs per manager | Higher is better | ≥12 (G), ≥8 (Y) | ≥10 (G), ≥6 (Y) |
| Avg Span of Control | Direct reports per manager | Range | 8-14 (G) | 6-12 (G) |
| Max Org Layers | Hierarchy depth | Lower is better | ≤8 (G), ≤9 (Y) | ≤9 (G), ≤10 (Y) |
| Mgrs Small Span % | Managers with few reports | Lower is better | ≤15% (G) | ≤25% (G) |

### People Metrics

| Metric | Description | Direction | Threshold |
|--------|-------------|-----------|-----------|
| Total Turnover | Annualized turnover | Lower is better | ≤15% (G), ≤18% (Y) |
| Voluntary Turnover | Regrettable attrition | Lower is better | ≤10% (G), ≤15% (Y) |
| Remote Associates % | ICs with remote exception | Lower is better | ≤4.5% (G) |
| Remote Managers % | Mgrs with remote exception | Lower is better | ≤2.5% (G) |

## Configuration

### Org Context (for threshold calibration)

```python
from mbr_engine.config import OrgContext, ThresholdDataStore

store = ThresholdDataStore()

context = OrgContext(
    org_name="Tech",
    captured_date="2026-03-18",
    work_type="mixed",
    client_facing_pct=22.5,
    management_style="tech-lead",
    restructuring_active=True,
)

store.save_org_context(context)
```

### Adding a New Org

```python
from mbr_engine.portability import OrgOnboarding

onboarding = OrgOnboarding()

# Start guided onboarding
session = onboarding.start_session("finance_us", "Finance - US")

# Run data discovery
session = onboarding.run_data_discovery(session, "path/to/data.xlsx")

# Answer context questions
session = onboarding.record_answers(session, {
    "work_type": "finance",
    "management_style": "pure-manager",
    "client_facing_pct": 40,
})

# Calibrate thresholds
session = onboarding.run_threshold_calibration(session)

# Complete
org = onboarding.complete_onboarding(session)
```

## File Structure

```
mbr-engine/
├── delta/                    # Data extraction
│   ├── base.py              # Base extractor class
│   ├── org_health.py        # Org health metrics
│   ├── headcount.py         # HC vs AOP
│   ├── turnover.py          # Turnover metrics
│   └── recognition.py       # Recognition utilization
├── feature_engine/          # Pattern detection
│   ├── detectors.py         # Pattern detectors
│   ├── scorer.py            # Topic scoring
│   └── engine.py            # Main engine
├── pptx_builder/            # Slide generation
│   ├── styles.py            # Walmart brand styles
│   ├── tables.py            # Table formatting
│   ├── charts.py            # Chart creation
│   └── builder.py           # Main builder
├── config/                   # Configuration
│   ├── thresholds.py        # Threshold definitions
│   ├── threshold_review.py  # Review engine
│   ├── persistence.py       # Data persistence
│   └── portability/         # Portability layer
│       ├── org_registry.py
│       ├── schema_registry.py
│       ├── metric_registry.py
│       ├── threshold_discovery.py
│       └── onboarding.py
├── orchestrator/            # Workflow coordination
│   └── workflow.py
└── models/                  # Data models
    ├── org_health.py
    ├── headcount.py
    └── feature_topics.py
```

## Dependencies

```
pandas>=2.0
openpyxl>=3.1
python-pptx>=0.6.21
```

## Related Skills

- [threshold-governance](./threshold-governance.md) - Detailed threshold management
- [org-portability](./portability.md) - Extending to new organizations
- [org-onboarding](./onboarding.md) - New org setup guide

## Status

**In Development** - Core extraction and threshold governance complete. PPTX builder and full workflow integration in progress.
