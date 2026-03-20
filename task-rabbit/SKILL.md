---
name: task-rabbit
description: "Design audit task manager — owns documentation, identifies CI opportunities, tracks design debt, documents skill gaps, escalates to engineering, and manages remediation workflows. Acts as the executive assistant for design quality assurance."
version: 1.0.0
author: jac007x
tags:
  - task-management
  - documentation
  - ci-opportunities
  - design-debt-tracking
  - skill-gap-identification
  - workflow-orchestration
---

# 🐰 Task Rabbit — Design QA Task Manager & Documentation Owner

Manages all design audit outputs, documentation, CI opportunity identification, skill gap tracking, and remediation workflow orchestration. Acts as the executive assistant coordinating design quality assurance across teams.

---

## 🎯 Core Responsibilities

### 1. Documentation Ownership
- Create/update design guidelines from audit findings
- Generate component library specifications
- Document discovered patterns and anti-patterns
- Build design debt ledger
- Maintain audit archive

### 2. CI/CD Opportunity Identification
- Identify automation potential in audit phases
- Recommend pre-commit hooks
- Design testing infrastructure gaps
- Suggest monitoring/alerting points

### 3. Skill Gap Analysis
- Document which skills/agents are needed
- Identify missing expertise areas
- Create skill development roadmap
- Recommend tool/agent creation priorities

### 4. Escalation & Workflow
- Generate remediation tickets
- Assign tasks to teams
- Track burn-down
- Manage dependencies
- Escalate blockers

---

## 📋 Input from Orchestrator

```json
{
  "orchestrator_handoff": {
    "audit_id": "audit-20260316-001",
    "design_file": "Q4_MBR_Deck_v2.1.pptx",
    "audit_report": { /* full audit JSON */ },
    "phases_completed": ["brand_compliance", "composition", "accessibility", "code_bridge"],
    "total_findings": 4,
    "design_debt_score": 6,
    "code_artifacts": {
      "design_spec": "design_spec.json",
      "design_tokens": "design_tokens.css",
      "components": ["button.html", "card.html", ...]
    }
  }
}
```

---

## 📚 DOCUMENTATION RESPONSIBILITY

### 1. Design Audit Archive

```markdown
# Design Audit Archive

## Q4 MBR Deck v2.1 (Audit ID: audit-20260316-001)

**Date Audited:** March 16, 2026
**Status:** PASS_WITH_WARNINGS (Score: 91/100)
**Auditor:** Designer Orchestrator v1.0

### Audit ary
- Brand Compliance: 92/100 (1 high violation)
- Composition: 85/100 (2 medium issues)
- Accessibility: 94/100 (1 low warning)
- Code Bridge: PASS (28 tokens generated)

### Critical Findings
- Chart legend contrast: 3.2:1 vs 4.5:1 required

### Design Debt
- Total Score: 6 (Low severity)
- Categories: Color (2), Spacing (1), Typography (2), Accessibility (1)

### Remediation
- Status: Not Started
- Estimated Effort: 2 hours
- Assigned To: Design Team

[Full Report Link](./audit-20260316-001.html)
```

### 2. Component Library Documentation

Generated from code bridge phase:

```markdown
# Component Library Specification

## Extracted Components

### Button Component
- **States:** Default, Hover, Pressed, Disabled, Focus
- **Sizes:** SM (32px), MD (40px), LG (48px)
- **Variants:** Primary, Secondary, Destructive
- **Accessibility:** WCAG AA compliant, focus indicator visible
- **CSS Class:** `.btn`
- **HTML:** [See button.html](./components/button.html)
- **Design Token Dependencies:** `--color-blue-100`, `--spacing-md`, `--radius-md`

### Card Component
- **States:** Default, Hover (shadow elevation), Active
- **Padding:** 24px (--spacing-lg)
- **Border Radius:** 4px (--radius-md)
- **Shadow:** shadow-sm at rest, shadow-md on hover
- **Responsive:** Stacks on mobile (768px breakpoint)

[View all components...](./components/)
```

### 3. Discovered Patterns & Antipatterns

```markdown
# Design Patterns Discovered

## Effective Patterns

### Executive Summary Layout
**When to use:** Opening slides, quarterly reviews
**Structure:**
- Headline with clear takeaway
- 3-4 KPI cards in grid
- Supporting callout box
- Footer with source/date

**Why it works:**
- Balances information density with readability
- Clear focal point (headline → KPIs → callout)
- Meets WCAG AA accessibility
- Responsive to different screen sizes

**Code Example:** [View spec](./patterns/executive-summary.html)

---

## Antipatterns Identified

### Too Many Font Sizes
**Issue:** Design uses 8 different font sizes (too many)
**Impact:** Reduces visual hierarchy clarity
**Recommendation:** Consolidate to 4-5 standard sizes using design tokens
**Effort:** 2 hours

### Arbitrary Spacing Values
**Issue:** Spacing uses 7px, 13px, 25px (not on 8px grid)
**Impact:** Makes responsive design harder, reduces consistency
**Recommendation:** Normalize to 8px unit system (4, 8, 16, 24, 32, 48, 64)
**Effort:** 3 hours
```

### 4. Design Guidelines Update

Task Rabbit updates master design guidelines based on audits:

```markdown
# Walmart Design System Guidelines
## Updated: March 16, 2026 (Based on Q4 MBR Audit)

### Color Usage Rules
- ✅ Always validate text contrast before using
- ✅ Pair colors with icons/text (never color alone)
- ✅ Test with color-blindness simulator
- ❌ Never use spark.100 for body text (fails contrast)
- ❌ Never use gray.50 for small text

### Spacing Standards
- Use 8px unit system only: 4, 8, 16, 24, 32, 48, 64px
- Button padding: 8px vertical, 16px horizontal minimum
- Card padding: 24px
- Section margins: 32-48px
- Gutter/gap: 16-24px

[Full guidelines...](./design-guidelines.md)
```

---

## 🚀 CI/CD OPPORTUNITY IDENTIFICATION

### Automated Design Validation Pipeline

```markdown
# CI/CD Opportunities Identified

## Priority 1: Pre-Commit Hook - Design Lint

### Description
Automatically check design files for common violations before commit

### What to Scan
- [ ] PPTX color usage against approved palette
- [ ] Font weight validation (400/600/700 only)
- [ ] Spacing grid adherence
- [ ] Missing alt text on images
- [ ] Slide dimension consistency (16:9 ratio)

### Implementation
```bash
# .husky/pre-commit
python scripts/design_lint.py --file "$1"
if [ $? -ne 0 ]; then
  echo "❌ Design validation failed. Run: design-orchestrator --auto-fix"
  exit 1
fi
```

### Effort: 4 hours (Python script + Git hook setup)
### ROI: Prevents 90% of brand violations from entering repo

---

## Priority 2: CI Pipeline - Contrast Checker

### Description
Automated WCAG contrast validation on all design changes

### Test Cases
- Extract all text colors and backgrounds
- Calculate contrast ratio for each element
- Flag violations <4.5:1 for body, <3:1 for UI
- Generate accessibility report

### GitHub Actions Workflow
```yaml
name: Design Accessibility Check
on: [pull_request]
jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Extract design specs
        run: python scripts/extract_colors.py
      - name: Run contrast checker
        run: python scripts/wcag_contrast_check.py
      - name: Report violations
        if: failure()
        run: |
          echo "WCAG Violations found:"
          cat contrast_report.json
```

### Effort: 3 hours
### ROI: Catches accessibility regressions automatically

---

## Priority 3: Visual Regression Testing

### Description
Automated visual diff detection for design changes

### Test Setup
```python
# tests/test_design_visual_regression.py

import pytest
from design_lib import DesignSpec, VisualDiff

@pytest.mark.design
def test_q4_mbr_deck_no_unintended_changes():
    """
    Verify deck matches approved baseline measurements
    """
    design = DesignSpec('Q4_MBR_Deck.pptx')
    baseline = DesignSpec('Q4_MBR_Deck_approved.pptx')
    
    diff = VisualDiff.compare(design, baseline)
    
    # Allow minor variations (<2px), flag larger changes
    assert diff.max_variance_px < 2, f"Design changed: {diff.report}"
    assert diff.colors_changed < 2, "Color palette changed"
    assert diff.font_sizes_consistent, "Typography changed"
```

### Effort: 5 hours (Figma/PPTX image rendering + comparison)
### ROI: Prevents accidental design drift in production

---

## Priority 4: Design Token Sync

### Description
Automatically sync design tokens from PPTX to CSS codebase

### Workflow
1. Design changes design.pptx colors/spacing
2. Designer runs: `design-orchestrator --export-tokens`
3. Token changes auto-generated to design_tokens.css
4. PR created for code review
5. Once merged, frontend automatically uses new tokens

### Implementation
```bash
# scripts/sync_design_tokens.py
# Triggered by design file commit

if design_file_changed('design.pptx'):
    tokens = extract_design_tokens('design.pptx')
    generate_css_file('src/styles/design_tokens.css', tokens)
    create_pr('Sync design tokens from PPTX', tokens_diff)
```

### Effort: 6 hours
### ROI: Single source of truth for design specs, prevents sync issues

---

## Estimated CI/CD Investment
| Feature | Effort | ROI | Priority |
|---------|--------|-----|----------|
| Design Lint (pre-commit) | 4h | 90% prevention | 1 |
| Contrast Checker (CI) | 3h | Accessibility guarantee | 2 |
| Visual Regression | 5h | Drift detection | 3 |
| Token Sync | 6h | Single source of truth | 2 |
| **Total** | **18h** | **High** | — |
```

---

## 🔍 SKILL GAP IDENTIFICATION

### Current Skill Inventory
```json
{
  "existing_skills": [
    "pptx-expert",
    "data-viz-expert",
    "slide-analyzer",
    "design-system-validator",
    "layout-composition-analyzer",
    "a11y-wcag-auditor",
    "design-to-code-bridge",
    "designer-orchestrator",
    "task-rabbit"
  ],
  "existing_agents": [
    "slide-creator",
    "share-puppy",
    "gui-cub",
    "code-puppy"
  ]
}
```

### Identified Skill Gaps

```markdown
# Skill Gap Report

## Gap 1: Motion & Animation Designer
**When Needed:** Designs with transitions, video, micro-interactions
**Impact:** Can't audit animations for seizure risk (flashing >3/sec)
**Recommendation:** Create skill for motion design best practices
**Effort to Create:** 8 hours
**Priority:** Medium (not all designs need motion)

## Gap 2: Figma Integration Skill
**When Needed:** Working with Figma native files
**Current:** Only PPTX/HTML supported
**Workaround:** Export Figma → PDF → manual review
**Recommendation:** Create Figma API integration skill
**Effort to Create:** 12 hours
**Priority:** High (Figma gaining adoption)

## Gap 3: Design-to-Frontend Component Generation
**When Needed:** Automatically generate React/Vue components from specs
**Current:** Manual code generation
**Benefit:** Reduce implementation time by 70%
**Effort to Create:** 20 hours
**Priority:** High (ROI: dev time savings)

## Gap 4: Typography Detail Expert
**When Needed:** Deep text hierarchy, kerning, ligature validation
**Current:** Basic size/weight/color only
**Recommendation:** Advanced typography skill
**Effort to Create:** 6 hours
**Priority:** Low (niche use case)

## Gap 5: Interactive Prototype Analyzer
**When Needed:** Validating prototypes (Figma, Framer)
**Current:** Static design only
**Recommendation:** Create prototype validation skill
**Effort to Create:** 10 hours
**Priority:** Medium

---

## Gap Remediation Roadmap

### Q2 2026 (Priority 1)
- [ ] Figma Integration Skill (high demand)
- [ ] Design-to-Component Generator (high ROI)

### Q3 2026 (Priority 2)
- [ ] Motion & Animation Auditor
- [ ] Interactive Prototype Validator

### Q4 2026 (Priority 3)
- [ ] Advanced Typography Expert
- [ ] Branding Guideline Enforcer
```

---

## 🎫 REMEDIATION WORKFLOW MANAGEMENT

### Generate Jira Tickets from Audit

```python
def create_remediation_tickets(audit_report):
    """
    Convert audit findings into actionable Jira tickets
    """
    tickets = []
    
    # Group by severity
    critical = audit_report.findings_by_severity('critical')
    for finding in critical:
        ticket = {
            'project': 'DESIGNQA',
            'issue_type': 'Bug',
            'summary': f"CRITICAL: {finding['issue']}",
            'description': f"""
Found in: {finding['location']}
Severity: {finding['severity']}
Remediation: {finding['remediation']}
Estimated Effort: {finding['effort']}

Audit ID: {audit_report.audit_id}
            """,
            'labels': ['design-debt', 'must-fix'],
            'priority': 'Blocker',
            'assignee': 'design-team',
        }
        tickets.append(ticket)
    
    # High severity tickets
    high = audit_report.findings_by_severity('high')
    for finding in high:
        ticket = {
            'project': 'DESIGNQA',
            'issue_type': 'Task',
            'summary': f"FIX: {finding['issue']}",
            'priority': 'High',
            'estimate': finding['effort_minutes'],
        }
        tickets.append(ticket)
    
    return tickets
```

### Remediation Tracking Dashboard

```markdown
# Design Remediation Status
## Q4 MBR Deck v2.1 (Audit: audit-20260316-001)

| Issue | Severity | Status | Assigned | Due | Effort |
|-------|----------|--------|----------|-----|--------|
| Chart legend contrast | High | In Progress | Jane | 2026-03-20 | 5min |
| Font size consolidation | Medium | Not Started | John | 2026-03-25 | 2hr |
| Button focus state | Medium | Not Started | Jane | 2026-03-22 | 1hr |
| Whitespace optimization | Low | Not Started | Unassigned | 2026-04-01 | 1.5hr |

**Completion:** 25% (1/4 in progress)
**Burn-down:** On track for March 25 completion
**Blockers:** None
```

---

## 📤 OUTPUT ARTIFACTS

```
task_rabbit_outputs/
├── documentation/
│   ├── audit_archive.md              # Audit history
│   ├── component_library_spec.md     # Component reference
│   ├── design_patterns.md            # Discovered patterns
│   └── design_guidelines_updated.md  # Updated guidelines
├── ci_opportunities/
│   ├── design_lint_proposal.md       # Pre-commit hook spec
│   ├── contrast_checker_spec.md      # CI pipeline spec
│   ├── visual_regression_setup.md    # Test framework
│   └── token_sync_proposal.md        # Automation proposal
├── skill_gaps/
│   ├── skill_gap_report.md           # Gap analysis
│   ├── remediation_roadmap.md        # Skills to build
│   └── priority_matrix.json          # Prioritization
├── remediation/
│   ├── jira_tickets.json             # Auto-generated tickets
│   ├── remediation_roadmap.md        # Timeline/plan
│   └── tracking_dashboard.html       # Status view
└── executive_summary.html            # One-page overview
```

---

## 🔗 Integration Points

**Task Rabbit receives from:**
- Designer Orchestrator (audit findings)
- Code bridge (design specs, tokens)

**Task Rabbit sends to:**
- Confluence (documentation updates)
- Jira (remediation tickets)
- Slack (notifications)
- GitHub (CI/CD setup proposals)
- Design team (remediation assignments)

---

## 📊 Metrics Tracked

```python
METRICS = {
    'documentation': {
        'audits_archived': 0,
        'components_documented': 0,
        'patterns_documented': 0,
        'guidelines_updated': 0,
    },
    'ci_opportunities': {
        'identified': 0,
        'implemented': 0,
        'estimated_effort_hours': 0,
        'estimated_roi_percent': 0,
    },
    'skill_gaps': {
        'total_gaps': 0,
        'high_priority': 0,
        'estimated_creation_hours': 0,
    },
    'remediation': {
        'tickets_created': 0,
        'tickets_resolved': 0,
        'avg_resolution_time': 0,
        'design_debt_score_improvement': 0,
    },
}
```