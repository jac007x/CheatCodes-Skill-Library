---
name: design-system-validator
description: "Walmart design system compliance auditor — brand palette validation, component standards, spacing rules, shadow depth, border radius, responsive breakpoints, and design debt detection."
version: 1.0.0
author: jac007x
tags:
  - design-system
  - branding
  - walmart
  - design-compliance
  - component-standards
  - color-validation
---

# 🎨 Design System Validator — Brand Compliance Engine

Automated validation of designs against Walmart's design system standards, ensuring consistency across all visual outputs.

---

## 🏗️ Walmart Design System Foundation

### Core Design Tokens

#### Color Palette (RGB + Hex)
```python
WALMART_COLORS = {
    # Primary Brand
    'blue': {
        5: (230, 240, 255),    # #E6F0FF - Lightest
        10: (214, 230, 255),   # #D6E6FF
        50: (153, 194, 255),   # #99C2FF
        100: (0, 83, 226),     # #0053E2 - Primary
        110: (0, 75, 203),     # #004BCB
        130: (0, 53, 153),     # #003599
        180: (0, 30, 88),      # #001E58 - Darkest
    },
    # Accent
    'spark': {
        5: (255, 251, 235),    # #FFFBEB
        10: (255, 242, 212),   # #FFF2D4
        100: (255, 194, 32),   # #FFC220 - Primary
        140: (153, 82, 19),    # #995213
    },
    # Semantic
    'red': {
        100: (234, 17, 0),     # #EA1100 - Error
        50: (252, 228, 225),   # #FCE4E1
    },
    'green': {
        100: (42, 135, 3),     # #2A8703 - Success
        50: (231, 245, 226),   # #E7F5E2
    },
    'cyan': {
        100: (0, 150, 214),    # #0096D6 - Info
        50: (230, 244, 251),   # #E6F4FB
    },
    # Grayscale (Neutral)
    'gray': {
        5: (250, 250, 250),    # #FAFAFA
        10: (245, 245, 245),   # #F5F5F5
        50: (217, 217, 217),   # #D9D9D9
        100: (116, 118, 123),  # #747677
        140: (198, 199, 202),  # #C6C7CA
        160: (46, 47, 50),     # #2E2F32 - Primary text
        180: (0, 0, 0),        # #000000
    },
    'white': (255, 255, 255), # #FFFFFF
    'black': (0, 0, 0),       # #000000
}
```

### Usage Rules by Component Type

| Component | Primary | Secondary | Tertiary | Rules |
|---|---|---|---|---|
| **Buttons** | blue.100 (white text) | white + gray.160 border | red.100 (destructive) | Hover: +10 shade, Pressed: +30, Disabled: gray.50 |
| **Text** | gray.160 | gray.100 | gray.50 | Min contrast 4.5:1 (WCAG AA) |
| **Data/Charts** | blue.100, spark.100, green.100, cyan.100, + 2 more | N/A | N/A | Max 6 colors per chart, consistent order |
| **Backgrounds** | white | gray.10 | gray.50 (borders) | Never gray below 10 for large areas |
| **Alerts** | Error=red.100, Success=green.100, Warning=spark.100, Info=cyan.100 | .10 level for bg | .50 for text | Use semantic color + icon, never color-only |
| **Hover States** | Current + 10 shade | + outline | N/A | Always show affordance (shadow/color/cursor) |
| **Disabled** | gray.50 (light bg), gray.100 (dark bg) | gray.100 text | N/A | No interaction, remove shadows, reduce opacity |

---

## 📏 Spacing System (8px Base Unit)

```python
SPACING = {
    'xs': '4px',    # 0.5 units
    'sm': '8px',    # 1 unit
    'md': '16px',   # 2 units
    'lg': '24px',   # 3 units
    'xl': '32px',   # 4 units
    'xxl': '48px',  # 6 units
    'xxxl': '64px', # 8 units
}

# Padding/Margin rules
# Buttons: 8px vertical, 16px horizontal
# Cards: 24px padding
# Page margins: 32px
# Section gaps: 32-48px
```

---

## 🔲 Border Radius & Shadow Depth

```python
BORDER_RADIUS = {
    'sm': '2px',   # Minimal UI (input boxes)
    'md': '4px',   # Cards, small buttons
    'lg': '8px',   # Buttons, containers
    'xl': '12px',  # Large modals, panels
    'full': '9999px', # Pills, circles
}

SHADOW_DEPTH = {
    'none': 'none',
    'sm': '0 1px 2px rgba(0,0,0,0.05)',
    'md': '0 4px 6px rgba(0,0,0,0.1)',
    'lg': '0 10px 15px rgba(0,0,0,0.1)',
    'xl': '0 20px 25px rgba(0,0,0,0.1)',
}

# Rules:
# - Interactive elements: shadow.md on hover
# - Cards/Panels at rest: shadow.sm
# - Modals: shadow.lg with overlay
# - No shadow on disabled elements
```

---

## 📱 Typography Standards

```python
TYPOGRAPHY = {
    'heading-1': {'size': '32px', 'weight': 700, 'line-height': '40px', 'letter-spacing': '-0.5px'},
    'heading-2': {'size': '24px', 'weight': 700, 'line-height': '32px', 'letter-spacing': '-0.5px'},
    'heading-3': {'size': '20px', 'weight': 600, 'line-height': '28px', 'letter-spacing': '0px'},
    'heading-4': {'size': '16px', 'weight': 600, 'line-height': '24px', 'letter-spacing': '0px'},
    'body-lg': {'size': '16px', 'weight': 400, 'line-height': '24px', 'letter-spacing': '0px'},
    'body': {'size': '14px', 'weight': 400, 'line-height': '20px', 'letter-spacing': '0px'},
    'body-sm': {'size': '12px', 'weight': 400, 'line-height': '16px', 'letter-spacing': '0px'},
    'label': {'size': '12px', 'weight': 600, 'line-height': '16px', 'letter-spacing': '0.5px'},
    'caption': {'size': '10px', 'weight': 400, 'line-height': '14px', 'letter-spacing': '0.5px'},
}

# Font Family
FONT_STACK_PRIMARY = '"Segoe UI", Roboto, "Helvetica Neue", sans-serif'
FONT_STACK_MONO = '"Monaco", "Courier New", monospace'
```

---

## ✅ Validation Checklist

### Color Validation
- [ ] All text colors meet 4.5:1 contrast minimum (WCAG AA)
- [ ] Data colors use only approved palette
- [ ] No color-only information delivery (pair with icons/patterns)
- [ ] Hover states are visually distinct (+10 shade minimum)
- [ ] Disabled state is gray.50 or gray.100
- [ ] Spark.100 not used for text (fails contrast)

### Spacing Validation
- [ ] All margins/padding use 8px unit system
- [ ] Button padding: 8px vertical, 16px horizontal (minimum)
- [ ] Card padding: 24px
- [ ] Section margins: 32-48px
- [ ] No arbitrary spacing (e.g., 7px, 13px, 25px)

### Border & Shadow Validation
- [ ] Border radius uses approved set (sm/md/lg/xl/full)
- [ ] Card elevation: shadow.sm at rest
- [ ] Interactive hover: shadow.md
- [ ] Modal overlay: shadow.lg
- [ ] No shadow on disabled elements

### Typography Validation
- [ ] Headings use heading-1/2/3/4 styles
- [ ] Body text is 14px minimum (12px for labels/captions)
- [ ] Line height minimum 1.4 (Walmart: 1.5)
- [ ] Font weight: 400 (regular), 600 (semibold), 700 (bold) only
- [ ] No all-caps for body text (headings OK)
- [ ] Max line length: 50-75 characters for readability

### Component Validation
- [ ] All buttons follow state pattern (default → hover → pressed → disabled)
- [ ] Alert icons paired with colors (error=❌, success=✓, warning=⚠, info=ℹ)
- [ ] Form inputs: 2px border.md, 4px radius.md, 8px padding
- [ ] Consistent corner treatment across all components

---

## 🔍 Automated Validation Function

```python
def validate_design_system(design_object):
    """
    Audit design object against Walmart standards.
    Returns: {compliant: bool, violations: [], warnings: []}
    """
    report = {'compliant': True, 'violations': [], 'warnings': []}
    
    # Check color usage
    for element in design_object.elements:
        if not is_approved_color(element.color):
            report['violations'].append(f"{element.name}: Unapproved color {element.color}")
            report['compliant'] = False
        if not meets_contrast(element.color, element.bg_color):
            report['violations'].append(f"{element.name}: Contrast {get_contrast(element.color, element.bg_color)}:1 < 4.5:1")
            report['compliant'] = False
    
    # Check spacing
    for spacing in design_object.spacings:
        if spacing not in APPROVED_SPACINGS:
            report['warnings'].append(f"Non-standard spacing: {spacing}")
    
    # Check typography
    for text in design_object.text_elements:
        if text.font_size < 12:
            report['warnings'].append(f"{text.name}: Font size {text.font_size}px may be too small")
    
    return report
```

---

## 📊 Design Debt Scoring

```python
DEBT_CATEGORIES = {
    'color': {
        'unapproved_color': 5,          # Critical
        'contrast_fail': 10,            # Critical (accessibility)
        'inconsistent_palette': 2,      # Low
    },
    'spacing': {
        'arbitrary_spacing': 1,         # Low
        'inconsistent_margins': 2,      # Low
    },
    'typography': {
        'too_many_fonts': 3,            # Medium
        'too_many_sizes': 2,            # Low
        'illegible_size': 5,            # Critical
    },
    'components': {
        'missing_states': 2,            # Low
        'inconsistent_radius': 1,       # Low
    },
}

def calculate_debt_score(violations):
    score = sum(DEBT_CATEGORIES[v['category']][v['type']] for v in violations)
    severity = 'critical' if score >= 15 else 'high' if score >= 8 else 'medium' if score >= 3 else 'low'
    return {'score': score, 'severity': severity}
```

---

## 🔗 Integration Points

- **pptx-expert**: Validate PPTX color usage during deck creation
- **data-viz-expert**: Enforce color palette for charts
- **slide-analyzer**: Check design compliance in visual audit
- **Designer Orchestrator**: First validation pass after design creation
- **Task Rabbit**: Log violations and track remediation

---

## 📝 Output Format

```json
{
  "design_name": "Q4 MBR Deck",
  "timestamp": "2026-03-16T22:30:34",
  "overall_score": "A (95/100)",
  "compliance": {
    "colors": "PASS",
    "spacing": "PASS",
    "typography": "PASS",
    "components": "WARN"
  },
  "violations": [
    {"element": "Button: Primary", "issue": "Contrast 3.2:1 < 4.5:1", "severity": "critical"}
  ],
  "warnings": [
    {"element": "Card Footer", "issue": "Non-standard spacing: 13px", "severity": "low"}
  ],
  "design_debt": {"score": 3, "severity": "low"},
  "recommendations": ["Consider consolidating to 3-4 heading sizes", "..."]
}
```