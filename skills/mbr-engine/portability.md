# Org Portability Sub-Skill

Makes the MBR Engine portable to any organization - Finance, Corporate Affairs, individual L3 teams, etc.

## Overview

The Portability Layer enables:
- **Any organization** - Not just Tech/Services/AIPD
- **Any org depth** - L2, L3, L4, or deeper
- **Custom metrics** - Add org-specific measurements
- **Schema flexibility** - Handle different data formats
- **Graceful degradation** - Work with incomplete data

## Components

### 1. Org Registry

Define any org with flexible filtering:

```python
from mbr_engine.portability import OrgDefinition, OrgRegistry, FilterConfig, OrgDepth

# Define Finance org
finance_org = OrgDefinition(
    org_id="finance_us",
    display_name="Finance - US Operations",
    depth=OrgDepth.L2,
    leader_name="Jane Smith",
    filter_config=FilterConfig(
        column_filters={"Department": "Finance", "Country": "United States"},
        exclude_filters={"Status": ["Terminated"]},
    ),
    context={
        "work_type": "finance",
        "client_facing_pct": 40,
        "management_style": "pure-manager",
    },
)

# Register
registry = OrgRegistry()
registry.register(finance_org)
```

### 2. Schema Registry

Handle different data formats with auto-detection:

```python
from mbr_engine.portability import SchemaRegistry

registry = SchemaRegistry()

# Auto-detect schema from file
schema, confidence = registry.detect_schema(df.columns)
# → ("walmart_roster_v1", 0.85)

# Get column mapping
mapping = schema.map_columns(df.columns)
# → {"employee_id": "Worker ID", "manager_indicator": "Is Manager", ...}
```

**Built-in Schemas:**
- `walmart_roster_v1` - HR roster export
- `walmart_finance_v1` - Finance HC vs AOP
- `walmart_turnover_v1` - Turnover reports
- `walmart_mada_v1` - Recognition data

### 3. Metric Registry

Drop/add metrics based on data availability:

```python
from mbr_engine.portability import MetricRegistry, MetricAvailability

registry = MetricRegistry()

# Check what's available
status = registry.check_availability("turnover_total", "finance_us", available_columns)
# → MetricAvailability.MISSING_DATA

# Disable metric (gracefully skip it)
registry.disable_metric("turnover_total", "finance_us", "No access to turnover data")

# Add custom metric
registry.add_custom_metric(
    MetricDefinition(
        metric_id="contractor_ratio",
        display_name="Contractor Ratio",
        required_columns=["employment_type"],
        formula="contractor_count / fte_count",
    ),
    org_id="finance_us",
)
```

### 4. Threshold Discovery

Auto-recommend thresholds from context:

```python
from mbr_engine.portability import ThresholdDiscovery

discovery = ThresholdDiscovery()

recommendation = discovery.recommend_thresholds(
    org_id="finance_us",
    org_display_name="Finance - US",
    context={
        "work_type": "finance",
        "client_facing_pct": 40,
        "management_style": "pure-manager",
    }
)

for t in recommendation.thresholds:
    print(f"{t.display_name}: green={t.green_value} ({t.confidence:.0%} confidence)")
# IC:Manager Ratio: green=9.0 (90% confidence)
# Avg Span: green=(7, 13) (90% confidence)
```

### 5. Portable Workflow

Run with graceful degradation:

```python
from mbr_engine.portability import PortableWorkflow, analyze_and_suggest

# Analyze what's possible with a file
report = analyze_and_suggest("path/to/finance_data.xlsx", "finance_us")
report.print_summary()

# Output:
# Schema: walmart_roster_v1 (85% confidence)
# Metrics Available: 7
#   ✓ ic_manager_ratio
#   ✓ avg_span_of_control
#   ...
# Metrics Unavailable: 3
#   ✗ turnover_total: missing_data
#   ...
# Suggestions:
#   → Disable unavailable metrics
#   → Consider contributing schema
```

## Org Depth Examples

### L2 Org (SVP Level)

```python
tech_org = OrgDefinition(
    org_id="tech",
    display_name="Global Technology",
    depth=OrgDepth.L2,
    leader_name="Suresh Kumar",
    filter_config=FilterConfig(
        column_filters={"L2 Full Name": "Suresh Kumar"},
    ),
)
```

### L3 Org (VP Level)

```python
from mbr_engine.portability import create_l3_org

platform_eng = create_l3_org(
    org_id="platform_eng",
    display_name="Platform Engineering",
    parent_org_id="tech",
    leader_name="Jane Smith",
    filter_column="L3 Full Name",
)
```

### L4 Org (Director Level)

```python
data_platform = OrgDefinition(
    org_id="data_platform",
    display_name="Data Platform",
    depth=OrgDepth.L4,
    parent_org_id="platform_eng",
    leader_name="John Doe",
    filter_config=FilterConfig(
        column_filters={"L4 Full Name": "John Doe"},
    ),
    inherit_thresholds_from="platform_eng",
)
```

## Schema Learning

Learn new schemas from files:

```python
# When you encounter a new data format
new_schema = registry.learn_from_file(
    file_path="path/to/new_format.xlsx",
    source_type="roster",
    org_name="corporate_affairs",
)

# Contribute back to skill repo
contribution = registry.prepare_contribution(
    schema_id=new_schema.schema_id,
    contributor_org="Corporate Affairs",
    anonymize=True,  # Strip identifying info
)
```

## Export/Import

Share configurations with skill repo:

```python
portable = PortableWorkflow()

# Export everything
export = portable.export_for_skill_repo()
# {
#   "orgs": {...},
#   "schemas": {...},
#   "metrics": {...},
# }

# Import from skill repo
portable.import_from_skill_repo(community_export)
```

## Quick Setup

```python
from mbr_engine.portability import quick_setup

org, thresholds = quick_setup(
    org_id="finance_us",
    display_name="Finance - US",
    work_type="finance",
    filter_column="Department",
    filter_value="Finance",
    client_facing_pct=40,
    management_style="pure-manager",
)

# Org is registered and thresholds are calibrated
```

## Related

- [MBR Engine](./README.md) - Main skill documentation
- [Threshold Governance](./threshold-governance.md) - Threshold management
- [Org Onboarding](./onboarding.md) - Guided setup for new orgs
