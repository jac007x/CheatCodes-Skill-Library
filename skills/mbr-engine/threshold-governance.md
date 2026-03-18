# Threshold Governance Sub-Skill

Manages metric thresholds with continuous improvement, quarterly reviews, and explainable recommendations.

## Overview

Threshold Governance ensures that metric thresholds remain:
- **Achievable** - Not too aspirational to be meaningless
- **Challenging** - Not too easy to drive improvement
- **Org-appropriate** - Different orgs have different needs
- **Explainable** - PP leads can understand and approve changes

## Threshold Types

### Direction Types

```python
class ThresholdDirection(Enum):
    LOWER_IS_BETTER = "lower"   # e.g., Turnover (want low)
    HIGHER_IS_BETTER = "higher" # e.g., IC:Mgr Ratio (want high)
    RANGE_IS_BETTER = "range"   # e.g., Avg Span (want 8-14)
```

### Color Coding

| Color | Meaning | Action Required |
|-------|---------|-----------------|
| 🟢 GREEN | Healthy / On Track | None |
| 🟡 YELLOW | Warning / Needs Attention | Monitor closely |
| 🔴 RED | Critical / Action Required | Requires explanation |

## Org-Specific Thresholds

| Metric | Tech | Services | AIPD | Rationale |
|--------|------|----------|------|-----------|
| IC:Manager | 12/8 | 10/6 | 10/6 | Engineering supports higher ratios |
| Avg Span | 8-14 | 6-12 | 6-12 | Services needs more touchpoints |
| Max Layers | 8/9 | 9/10 | 7/8 | AIPD should be flatter (newer org) |
| Small Span % | 15/25 | 25/35 | 20/30 | Services has specialized teams |

## Review Cycles

### Quarterly Lookback (Feb, May, Aug, Nov)

Analyzes threshold achievability:
- **Too Easy?** - 6+ consecutive green months → recommend tighten
- **Too Hard?** - 4+ consecutive red months → recommend loosen

```python
workflow = MBRWorkflow(sources=..., month="2026-02")
report = workflow.run_quarterly_review()
# → Generates recommendations with reasoning
```

### Annual Full Review (December)

Comprehensive review including:
- Full achievability analysis
- Industry benchmark comparison
- Org context integration
- Multi-year trend analysis

```python
report = workflow.run_annual_review(industry_benchmarks=benchmarks)
```

## Context Gathering

Questions asked during org setup that influence thresholds:

| Question | Options | Impacts |
|----------|---------|---------|
| Work type | Engineering, Support, Product, etc. | IC:Mgr, Span, Turnover |
| Client-facing % | 0-100% | IC:Mgr, Span |
| Management style | Player-Coach, Pure Manager, Tech Lead | Span, Small Span % |
| Org maturity | New, Growing, Mature, Transforming | Layers, Small Span % |
| Restructuring | Yes/No | Turnover, Small Span % |

## Change Control

### Gradual Changes

Thresholds change gradually to avoid disruption:
- **Max change per quarter**: 2 percentage points
- **Change path**: Shows quarter-by-quarter transition

```python
# Example change path
[
    {"quarter": "FY27Q3", "green": 13, "yellow": 9},
    {"quarter": "FY27Q4", "green": 14, "yellow": 10},
    {"quarter": "FY28Q1", "green": 15, "yellow": 11},
]
```

### Recommendation Format

Each recommendation includes:
- **Current thresholds**
- **Proposed thresholds**
- **Historical analysis** - Trend data
- **Industry comparison** - External benchmarks
- **Org context factors** - What makes this org different
- **Achievability assessment** - Too easy/hard analysis
- **Risks of change** - What could go wrong
- **Risks of no change** - What happens if we don't act
- **Confidence level** - High/Medium/Low

## Persistence

### Data Storage

```
~/.mbr-engine/threshold_data/
├── monthly/                    # MoM metric tracking
│   ├── 2026-01_Tech.json
│   └── 2026-02_Tech.json
├── context/                    # Org context (versioned)
│   ├── Tech_current.json
│   └── Tech_2026-01.json
├── changes/
│   └── change_log.json         # Audit trail
├── reviews/
│   ├── 2026-02_quarterly.json
│   └── 2026-12_annual.json
└── outcomes/
    └── outcome_log.json        # CI feedback
```

### Continuous Improvement

Track review outcomes for learning:

```python
store.record_outcome(ReviewOutcome(
    recommendation_id="...",
    outcome="approved",  # or "rejected", "deferred", "modified"
    reviewer="Jane Smith",
    reviewer_notes="Agreed - threshold too lenient",
))

# CI metrics
approval_rate = store.get_approval_rate()
# {"approval_rate": 75.0, "rejection_rate": 10.0, ...}
```

## Usage Examples

### Check Current Color

```python
from mbr_engine.config import get_color, ThresholdColor

color = get_color("ic_manager_ratio", 8.12, "Tech")
# → ThresholdColor.YELLOW
```

### Get Historical Trend

```python
trend = workflow.get_historical_trend("ic_manager_ratio", "Tech", months=12)
# {
#   "trend": "stable",
#   "consecutive_greens": 2,
#   "consecutive_reds": 0,
#   "average": 8.5,
# }
```

### Generate Review Report

```python
report = workflow.run_quarterly_review()
print(report)  # Markdown format for PP lead review
```

## Related

- [MBR Engine](./README.md) - Main skill documentation
- [Org Portability](./portability.md) - Adding new organizations
- [Org Onboarding](./onboarding.md) - New org setup guide
