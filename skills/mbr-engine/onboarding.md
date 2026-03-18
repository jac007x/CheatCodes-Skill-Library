# Org Onboarding Sub-Skill

Guided workflow for adding new organizations to the MBR Engine with validation, context gathering, and threshold calibration.

## Overview

Onboarding ensures new orgs are set up correctly by:
1. **Validating data** - Schema detection, column mapping, quality checks
2. **Gathering context** - Work type, management style, org nuances
3. **Validating metrics** - Compare extracted vs expected values
4. **Calibrating thresholds** - Recommend and adjust thresholds
5. **Recording feedback** - Learn from adjustments for future orgs

## Onboarding Stages

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEW ORG ONBOARDING                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DATA DISCOVERY          ──────────────────────────────────▶ │
│     ├─ Detect schema from file                                  │
│     ├─ Map columns to canonical names                           │
│     ├─ Validate data quality (nulls, duplicates)                │
│     └─ Auto-detect data nuances                                 │
│                                                                 │
│  2. CONTEXT GATHERING       ──────────────────────────────────▶ │
│     ├─ Org basics (work type, size, age)                        │
│     ├─ Management style (player-coach vs pure-manager)          │
│     ├─ Data nuances (contractors, vacants, quirks)              │
│     └─ Validation expectations (known values)                   │
│                                                                 │
│  3. SAMPLE EXTRACTION       ──────────────────────────────────▶ │
│     ├─ Calculate metrics from data                              │
│     ├─ Compare vs expected values                               │
│     └─ Flag variances for investigation                         │
│                                                                 │
│  4. THRESHOLD CALIBRATION   ──────────────────────────────────▶ │
│     ├─ Recommend thresholds from context                        │
│     ├─ Allow manual adjustment                                  │
│     └─ Record feedback (for learning)                           │
│                                                                 │
│  5. FINAL VALIDATION        ──────────────────────────────────▶ │
│     ├─ Verify all stages complete                               │
│     ├─ Generate summary report                                  │
│     └─ Create org definition                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Usage

### Start Onboarding

```python
from mbr_engine.portability import OrgOnboarding

onboarding = OrgOnboarding()

# Start new session
session = onboarding.start_session("finance_us", "Finance - US Operations")
```

### Stage 1: Data Discovery

```python
session = onboarding.run_data_discovery(session, "path/to/finance_roster.xlsx")

# Check validation results
for v in session.validation_results:
    print(f"{v['status']}: {v['message']}")

# Output:
# passed: Successfully read file with 450 rows and 35 columns
# passed: Detected schema: walmart_roster_v1 (85% confidence)
# warning: 5 columns not mapped to schema
# passed: All required columns present
```

### Stage 2: Context Gathering

```python
# Get questions to ask
questions = onboarding.get_next_questions(session)

for q in questions:
    print(f"{q['id']}: {q['question']}")

# Output:
# work_type: What is the primary work type for this org?
# org_size: Approximately how many people are in this org?
# org_age: How long has this org existed in its current form?

# Record answers
session = onboarding.record_answers(session, {
    "work_type": "finance",
    "org_size": "medium",
    "org_age": "mature",
    "management_style": "pure-manager",
    "client_facing_pct": 40,
})
```

### Stage 3: Sample Extraction

```python
# Run with expected values for validation
session = onboarding.run_sample_extraction(
    session,
    expected_values={
        "ic_manager_ratio": 8.5,
        "total_headcount": 450,
    }
)

# Check variances
for metric, variance in session.metric_variances.items():
    print(f"{metric}: {variance:.1f}% variance")

# Output:
# ic_manager_ratio: 2.3% variance ✓
# total_headcount: 0.0% variance ✓
```

### Stage 4: Threshold Calibration

```python
session = onboarding.run_threshold_calibration(session)

# Review recommendations
for metric_id, values in session.recommended_thresholds.items():
    print(f"{metric_id}: green={values['green']} ({values['confidence']:.0%})")

# Adjust if needed
session = onboarding.adjust_threshold(
    session,
    metric_id="ic_manager_ratio",
    green_value=8.0,
    yellow_value=5.0,
    reason="Finance teams need more management touchpoints for compliance",
)
```

### Stage 5: Complete

```python
# Run final validation
session = onboarding.run_final_validation(session)

# Complete onboarding
org = onboarding.complete_onboarding(
    session,
    notes="Setup complete. Compliance team may need smaller spans."
)

print(f"Created org: {org.display_name}")
```

## Context Questions

### Org Basics

| Question | Type | Options | Impact |
|----------|------|---------|--------|
| Work type | Choice | Engineering, Support, Product, Design, Finance, Corporate, Mixed | IC:Mgr, Span, Turnover |
| Org size | Choice | Small (<100), Medium (100-500), Large (500-2000), XLarge (2000+) | Layers, IC:Mgr |
| Org age | Choice | New, Young, Established, Mature, Transforming | Layers, Small Span % |

### Management

| Question | Type | Options | Impact |
|----------|------|---------|--------|
| Management style | Choice | Player-Coach, Pure Manager, Tech Lead, Supervisory | Span, Small Span % |
| Client-facing % | Percentage | 0-100% | IC:Mgr, Span |
| Specialized teams | Boolean + Detail | Yes/No | Small Span % |

### Data Nuances

| Question | Type | Options | Impact |
|----------|------|---------|--------|
| Contractor inclusion | Choice | Included, Separate, Excluded, Mixed | Headcount, IC:Mgr |
| Vacant positions | Choice | Not included, Flagged, Unflagged, Separate | HC vs AOP |
| Reporting quirks | Multi-select | Dotted-line, Matrix, Interim, Cross-org | IC:Mgr, Span, Layers |

## Data Nuances

Capture org-specific data quirks:

```python
from mbr_engine.portability import DataNuance

nuance = DataNuance(
    nuance_id="mgr_indicator_values",
    category="column_mapping",
    description="Manager column uses 'Supervisor' instead of 'Manager'",
    impact="May affect IC vs Manager classification",
    resolution="Map 'Supervisor' → 'Manager'",
)

session = onboarding.record_nuance(session, nuance)
```

## Resumable Sessions

Sessions are persisted and can be resumed:

```python
# Resume existing session
session = onboarding.resume_session("finance_us")

# List all sessions
sessions = onboarding.list_sessions()
for s in sessions:
    print(f"{s['org_id']}: {s['stage']} (started {s['started']})")
```

## Feedback Loop

Threshold adjustments are recorded for learning:

```python
# Adjustments saved to calibration_feedback.json
{
    "metric_id": "ic_manager_ratio",
    "recommended_green": 9.0,
    "recommended_yellow": 6.0,
    "actual_green": 8.0,
    "actual_yellow": 5.0,
    "adjustment_reason": "Finance needs more touchpoints",
    "org_id": "finance_us"
}
```

This feedback improves future recommendations for similar orgs.

## Summary Report

Generate onboarding summary:

```python
summary = onboarding.get_onboarding_summary(session)
print(summary)
```

Output:
```markdown
# Onboarding Summary: Finance - US Operations

**Org ID:** finance_us
**Stage:** completed
**Started:** 2026-03-18

## Data Discovery
- **Source File:** /path/to/finance_roster.xlsx
- **Schema:** walmart_roster_v1 (85% confidence)
- **Columns Mapped:** 30
- **Unmapped Columns:** 5

## Context Gathered
- **work_type:** finance
- **management_style:** pure-manager
- **client_facing_pct:** 40

## Sample Metrics
- **ic_manager_ratio:** 8.3 (variance: 2.3%)
- **total_headcount:** 450 (variance: 0.0%)

## Data Nuances
- **column_mapping:** Manager column uses 'Supervisor'

## Validation Results
- ✓ File read successful
- ✓ Schema detected
- ✓ Required columns present
- ✓ Metrics within tolerance
```

## Storage

```
~/.mbr-engine/onboarding/
├── session_finance_us.json       # Onboarding state
├── session_corp_affairs.json
└── calibration_feedback.json     # Learning from adjustments
```

## Related

- [MBR Engine](./README.md) - Main skill documentation
- [Threshold Governance](./threshold-governance.md) - Threshold management
- [Org Portability](./portability.md) - Multi-org support
