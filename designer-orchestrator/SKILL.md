---
name: designer-orchestrator
description: "Master design workflow orchestrator — coordinates all 7 design skills through a 4-phase pipeline: design validation, composition audit, accessibility compliance, and code bridge. Produces QA reports, design debt tracking, and hands off to Task Rabbit for documentation."
version: 1.0.0
author: jac007x
tags:
  - orchestration
  - design-workflow
  - qa-pipeline
  - multi-skill-coordination
  - design-governance
---

# 🎼 Designer Orchestrator — Master Design Pipeline

Coordinates the complete design quality assurance workflow, running all design skills in sequence and producing comprehensive audit reports with actionable remediation guidance.

---

## 🏗️ Design QA Pipeline Architecture

### 4-Phase Validation Flow

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: Design artifact (PPTX, Figma export, HTML, etc.)    │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────▼──────────────┐
        │  PHASE 1: BRAND COMPLIANCE │
        │ (Design System Validator)  │
        │ - Color usage audit        │
        │ - Spacing validation       │
        │ - Typography consistency   │
        │ - Component standards      │
        └──────────────┬─────────────┘
                       │
        ┌──────────────▼───────────────┐
        │  PHASE 2: COMPOSITION QA     │
        │(Layout Composition Analyzer) │
        │ - Balance scoring           │
        │ - Whitespace evaluation     │
        │ - Visual flow analysis      │
        │ - Alignment grid check      │
        └──────────────┬───────────────┘
                       │
        ┌──────────────▼──────────────┐
        │ PHASE 3: ACCESSIBILITY AUDIT │
        │  (A11Y WCAG Auditor)        │
        │ - Contrast validation       │
        │ - Text sizing check         │
        │ - Motor affordances         │
        │ - Cognition compliance      │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │ PHASE 4: CODE GENERATION    │
        │(Design-to-Code Bridge)      │
        │ - Extract measurements      │
        │ - Generate design tokens    │
        │ - Export CSS/HTML specs     │
        │ - Create baseline files     │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │  HAND OFF TO TASK RABBIT    │
        │ - Aggregate audit report    │
        │ - Document findings         │
        │ - Identify CI opportunities │
        │ - Track design debt         │
        │ - Escalate skill gaps       │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │  OUTPUT: Audit Report       │
        │  + Remediation Roadmap      │
        │  + Design Tokens            │
        │  + Code Specs               │
        │  + Jira Tickets (TBD)       │
        └──────────────────────────────┘
```

---

## 📋 Orchestrator Configuration

### Input Specification
```json
{
  "task_id": "designer-orch-001",
  "design_file": "/path/to/design.pptx",
  "design_type": "pptx | figma | html | sketch",
  "phases_enabled": {
    "brand_compliance": true,
    "composition": true,
    "accessibility": true,
    "code_bridge": true
  },
  "severity_threshold": "high",
  "auto_remediation": false,
  "output_format": "html | json | markdown",
  "jira_project": "DESIGNQA",
  "notify_on_complete": "designer@walmart.com"
}
```

---

## 🔄 Phase 1: Brand Compliance (5 min)

### Validation Steps
1. **Parse Design Artifact**
   - Load PPTX/Figma/HTML
   - Inventory all visual elements
   - Extract colors, fonts, spacing

2. **Design System Validator**
   - Check all colors against approved palette
   - Verify spacing uses 8px unit system
   - Validate font weights (400/600/700 only)
   - Check border radius consistency
   - Audit shadows (approved depths only)

3. **Score & Report**
   - Rating: A+/A/B/C/F
   - Violations list (critical/high/low)
   - Design debt score
   - Quick remediation guide

### Early Exit Rules
If CRITICAL violations found (unapproved colors, contrast fail, extreme spacing):
- Flag for immediate remediation
- Continue to remaining phases (don't skip)
- Mark report as "REVIEW REQUIRED BEFORE FINALIZATION"

---

## 🎯 Phase 2: Composition Analysis (5 min)

### Validation Steps
1. **Visual QA (pptx → image conversion)**
   - Render PPTX to high-res images (300 DPI)
   - Analyze each slide visually

2. **Layout Composition Analyzer**
   - Evaluate balance (symmetry vs asymmetry)
   - Score visual hierarchy
   - Check whitespace percentage (target: 20-40%)
   - Verify alignment to grid
   - Identify reading flow pattern (F/Z/S/Grid)
   - Score focal point clarity

3. **Gestalt Principle Check**
   - Proximity: Related elements grouped?
   - Similarity: Consistent styling?
   - Continuity: Smooth visual flow?
   - Closure: Any floating/orphaned elements?
   - Figure-ground: Clear primary/secondary?

4. **Output**
   - Composition score (0-100)
   - Issues by dimension
   - Before/after suggestions

---

## ♿ Phase 3: Accessibility Audit (5-10 min)

### Validation Steps
1. **Contrast Evaluation**
   - Analyze all text colors vs backgrounds
   - Calculate contrast ratios (WCAG formula)
   - Flag violations: body text <4.5:1, UI <3:1

2. **Readability Check**
   - Font size validation (min 12px body)
   - Line height audit (min 1.5)
   - Letter spacing check
   - Longest line length evaluation

3. **Motor Affordances**
   - Touch target sizes (min 44×44px)
   - Spacing between interactive elements
   - Focus indicator visibility
   - Keyboard navigation paths

4. **Cognitive Compliance**
   - Language clarity analysis
   - Chunking evaluation
   - Color usage (not sole indicator?)
   - Motion/animation safety

5. **Color Blindness Simulation**
   - Render with protanopia filter
   - Render with deuteranopia filter
   - Check visual clarity maintained

6. **Output**
   - WCAG 2.2 Level AA compliance: PASS/FAIL
   - Accessibility score (0-100)
   - Critical violations (must fix)
   - Warnings (should fix)
   - Remediation priority

---

## 🌉 Phase 4: Code Generation (10 min)

### Validation Steps
1. **Measurement Extraction**
   - Extract all element positions, sizes
   - Export typography specs
   - Capture color values
   - Record spacing measurements

2. **Design Token Generation**
   - Create CSS custom properties
   - Normalize to system tokens
   - Flag non-standard values

3. **Specification Export**
   - Generate JSON design spec
   - Create HTML/CSS templates
   - Export component library specs
   - Build measurement baseline

4. **Quality Checks**
   - CSS linting (no syntax errors)
   - HTML validity
   - Token completeness
   - Baseline file integrity

5. **Output**
   - Design spec (JSON)
   - CSS tokens file
   - HTML templates
   - Component specs
   - Measurement baseline
   - Spec report (HTML)

---

## 📊 Aggregate Audit Report

### Report Structure
```json
{
  "audit_id": "audit-20260316-001",
  "design_file": "Q4_MBR_Deck_v2.1.pptx",
  "audit_timestamp": "2026-03-16T22:30:34",
  "overall_status": "PASS_WITH_WARNINGS",
  "phases": {
    "brand_compliance": {
      "status": "PASS",
      "score": 92,
      "critical_violations": 0,
      "high_violations": 1,
      "design_debt": {"score": 3, "severity": "low"}
    },
    "composition": {
      "status": "PASS",
      "score": 85,
      "issues_found": 2,
      "whitespace_pct": 32,
      "reading_pattern": "Z-pattern"
    },
    "accessibility": {
      "status": "PASS",
      "wcag_level": "AA",
      "score": 94,
      "contrast_violations": 1,
      "color_blindness_safe": true
    },
    "code_bridge": {
      "status": "PASS",
      "tokens_generated": 28,
      "components_specs": 8,
      "code_quality": "A"
    }
  },
  "summary": {
    "total_issues": 4,
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 1,
    "estimated_remediation_time": "2 hours"
  },
  "findings": [
    {
      "phase": "brand_compliance",
      "issue": "Chart legend text: gray.100 fails contrast (3.2:1 < 4.5:1)",
      "severity": "high",
      "location": "slide_3",
      "remediation": "Use gray.160 instead",
      "effort": "5 min"
    },
    // ... more findings
  ],
  "design_debt_summary": {
    "total_score": 6,
    "by_category": {
      "color": 2,
      "spacing": 1,
      "typography": 2,
      "accessibility": 1
    }
  },
  "recommendations": [
    "Consolidate to 3-4 heading sizes (currently 5)",
    "Increase slide footer padding for breathing room",
    "Review data label font size for small screens"
  ],
  "deliverables": {
    "design_spec_json": "/exports/design_spec.json",
    "design_tokens_css": "/exports/design_tokens.css",
    "component_specs": "/exports/components/",
    "audit_report_html": "/exports/audit_report.html"
  }
}
```

---

## 🐰 Hand-Off to Task Rabbit

Once all 4 phases complete, orchestrator hands off to **Task Rabbit** with:

1. **Audit Summary**
   - All violations and warnings
   - Design debt breakdown
   - Severity distribution

2. **Documentation Tasks**
   - [ ] Create design guidelines doc
   - [ ] Document discovered patterns
   - [ ] Create component library spec

3. **CI/CD Opportunities**
   - Automated contrast checking (pre-commit hook)
   - Design token linting
   - Visual regression testing baselines
   - Accessibility scanning in CI pipeline

4. **Skill Gaps Identified**
   - Missing design system module (e.g., button states)
   - Need motion/animation skill
   - Figma integration skill needed
   - Form field accessibility expertise gap

5. **Follow-Up Tasks**
   - Generate Jira tickets for violations
   - Schedule remediation sprint
   - Assign to design team
   - Track burn-down

---

## 🎛️ Orchestrator Configuration Options

### Partial Run (Skip Phases)
```json
{
  "phases_enabled": {
    "brand_compliance": true,
    "composition": false,      // Skip
    "accessibility": true,
    "code_bridge": false       // Skip
  }
}
```

### Severity Filtering
```json
{
  "severity_threshold": "high",  // Only report HIGH and CRITICAL
  // vs
  "severity_threshold": "low"    // Report all issues
}
```

### Auto-Remediation (Advanced)
```json
{
  "auto_remediation": true,
  "allowed_fixes": [
    "font_size_adjust",           // Can auto-increase small fonts
    "spacing_normalize",           // Can normalize to 8px grid
    "color_contrast_darken_text",  // Can darken text for contrast
  ],
  "forbidden_fixes": [
    "remove_elements",             // Never delete content
    "crop_content"                 // Never crop
  ]
}
```

---

## 📤 Output Artifacts

```
audit_results/
├── audit_report.html              # Human-readable report
├── audit_report.json              # Machine-readable findings
├── findings_by_severity.csv        # For tracking
├── design_debt_dashboard.html      # Visual debt summary
├── remediation_roadmap.md          # Prioritized fixes
├── code_exports/
│   ├── design_spec.json
│   ├── design_tokens.css
│   ├── components/
│   └── measurements_baseline.json
└── task_rabbit_handoff.json        # For Task Rabbit
```

---

## 🔗 Integration Points

**Orchestrator consumes:**
- design-system-validator (Phase 1)
- layout-composition-analyzer (Phase 2)
- a11y-wcag-auditor (Phase 3)
- design-to-code-bridge (Phase 4)

**Orchestrator feeds:**
- task-rabbit (final handoff)
- jira (auto-ticket creation)
- confluence (documentation)
- slack (notifications)

---

## 🚀 Quick Start

### Run Full Pipeline
```bash
velcro design-orchestrator --file design.pptx --output report.html
# ✓ Phase 1: Brand Compliance (92%)
# ✓ Phase 2: Composition Analysis (85%)
# ✓ Phase 3: Accessibility Audit (94%)
# ✓ Phase 4: Code Generation (PASS)
# ✓ Handing off to Task Rabbit...
```

### Run Specific Phases
```bash
velcro design-orchestrator --file design.pptx --phases accessibility,code-bridge
```

### Generate Report Only
```bash
velcro design-orchestrator --file design.pptx --report-only --format html
```