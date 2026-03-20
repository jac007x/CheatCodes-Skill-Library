---
name: design-to-code-bridge
description: "Design specification exporter — extract measurements, colors, typography specs, spacing values from designs and generate CSS/HTML/JSON specs. Converts PPTX/Figma to code-ready design tokens, component APIs, and visual regression baselines."
version: 1.0.0
author: jac007x
tags:
  - design-to-code
  - design-tokens
  - css-generation
  - html-specs
  - design-specs
  - measurement-export
---

# 🌉 Design-to-Code Bridge — Specification Exporter

Extracts design specifications from presentations and graphics, generating production-ready code, CSS, and design tokens for front-end implementation.

---

## 📐 Measurement Extraction

### From PowerPoint (python-pptx)
```python
from pptx import Presentation
from pptx.util import Inches, Pt

def extract_measurements(pptx_path):
    """
    Export all design measurements from PPTX
    """
    prs = Presentation(pptx_path)
    measurements = []
    
    for slide_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            measurements.append({
                'slide': slide_idx,
                'element': shape.name,
                'type': shape.shape_type,
                'left': shape.left.inches,
                'top': shape.top.inches,
                'width': shape.width.inches,
                'height': shape.height.inches,
                'font_size': shape.text_frame.paragraphs[0].font.size.pt if shape.has_text_frame else None,
                'text': shape.text if shape.has_text_frame else None,
            })
    
    return measurements

# Output: CSV/JSON with all measurements
# Use for baseline references, visual regression testing
```

---

## 🎨 Color & Token Extraction

### Color Spec Export
```python
def extract_colors(pptx_path):
    """
    Export all unique colors used in presentation
    """
    colors = {}
    
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.fill.type:
                rgb = shape.fill.fore_color.rgb
                hex_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
                colors[hex_color] = (rgb[0], rgb[1], rgb[2])
    
    return colors

# Output JSON
# {
#   "#0053E2": {"name": "blue.100", "rgb": "rgb(0, 83, 226)", "usage": "primary"},
#   "#2E2F32": {"name": "gray.160", "rgb": "rgb(46, 47, 50)", "usage": "text"}
# }
```

### Design Token Generation
```python
def generate_design_tokens(design_spec):
    """
    Generate CSS custom properties (variables) for design system
    """
    tokens = f"""
:root {{
  /* Colors */
  --color-blue-100: #0053E2;
  --color-blue-110: #004BCB;
  --color-gray-160: #2E2F32;
  --color-spark-100: #FFC220;
  
  /* Typography */
  --font-size-heading-1: 32px;
  --font-size-heading-2: 24px;
  --font-size-body: 14px;
  --font-size-caption: 10px;
  
  --font-weight-regular: 400;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  --line-height-tight: 1.4;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.6;
  
  /* Spacing (8px unit system) */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-xxl: 48px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  
  /* Border Radius */
  --radius-sm: 2px;
  --radius-md: 4px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 9999px;
}}
    """
    return tokens
```

---

## ✏️ Typography Extraction

### Font Stack Specification
```python
def extract_typography(pptx_path):
    """
    Export typography hierarchy from presentation
    """
    typography = {}
    
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        key = f"{run.font.size.pt}pt_{run.font.bold}"
                        if key not in typography:
                            typography[key] = {
                                'size': run.font.size.pt,
                                'weight': 700 if run.font.bold else 400,
                                'color': run.font.color.rgb if hasattr(run.font.color, 'rgb') else None,
                                'font_name': run.font.name,
                                'examples': [],
                            }
                        typography[key]['examples'].append(run.text[:50])
    
    return typography

# Output: Normalized typography scale
# Key insight: Find duplicate/similar sizes and consolidate
```

### Consolidate to System
```python
def normalize_typography(extracted_typography):
    """
    Map custom sizes to design system tokens
    """
    system = {
        'heading-1': {'size': '32px', 'weight': 700},
        'heading-2': {'size': '24px', 'weight': 700},
        'heading-3': {'size': '20px', 'weight': 600},
        'body': {'size': '14px', 'weight': 400},
        'caption': {'size': '10px', 'weight': 400},
    }
    
    # Match extracted to system, flag outliers
    outliers = []
    for key, spec in extracted_typography.items():
        closest = find_closest_size(spec['size'], system)
        if abs(spec['size'] - system[closest]['size']) > 2:
            outliers.append({'found': key, 'suggest': closest, 'variance': spec['size'] - system[closest]['size']})
    
    return {'mapped': extracted_typography, 'outliers': outliers}
```

---

## 🎯 HTML/CSS Generation

### Component HTML Template
```html
<!-- Input: Design spec JSON -->
<!-- Output: Production-ready HTML -->

<template id="executive-summary-slide">
  <section class="slide slide--16-9">
    <!-- Title -->
    <header class="slide__header">
      <h1 class="slide__title">Executive Summary: Q4 Performance</h1>
      <span class="slide__date">March 16, 2026</span>
    </header>
    
    <!-- KPI Grid -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-value">$14.2M</div>
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-change kpi-change--up">▲ 12.3%</div>
      </div>
      <!-- More cards... -->
    </div>
    
    <!-- Footer -->
    <footer class="slide__footer">
      <span class="slide__source">Source: Revenue Dashboard</span>
      <span class="slide__page">Page 1 of 12</span>
    </footer>
  </section>
</template>
```

### CSS Generation
```css
/* Extracted from design, normalized to system */

.slide {
  width: 13.333in;  /* 16:9 aspect ratio */
  height: 7.5in;
  padding: var(--spacing-lg);  /* 24px */
  background: var(--color-white);
}

.slide__header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: var(--spacing-xl);  /* 32px */
  border-bottom: 1px solid var(--color-gray-50);
}

.slide__title {
  font-size: var(--font-size-heading-1);  /* 32px */
  font-weight: var(--font-weight-bold);
  color: var(--color-gray-160);
  line-height: var(--line-height-tight);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-lg);  /* 24px */
  margin-bottom: var(--spacing-xl);
}

.kpi-card {
  padding: var(--spacing-lg);
  background: var(--color-gray-10);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-gray-50);
  box-shadow: var(--shadow-sm);
}

.kpi-value {
  font-size: 32px;
  font-weight: var(--font-weight-bold);
  color: var(--color-blue-100);
}

.kpi-change--up {
  color: var(--color-green-100);
}

.kpi-change--down {
  color: var(--color-red-100);
}
```

---

## 📋 Specification Document Format

### JSON Design Spec
```json
{
  "design_id": "Q4_MBR_Deck_v2.1",
  "created_at": "2026-03-16T22:30:34",
  "design_tool": "pptx",
  "slides": [
    {
      "id": "slide_1",
      "title": "Executive Summary",
      "dimensions": {"width": 13.333, "height": 7.5, "unit": "inches"},
      "elements": [
        {
          "id": "title",
          "type": "text",
          "content": "Executive Summary: Q4 Performance",
          "position": {"x": 0.5, "y": 0.2},
          "size": {"width": 9, "height": 0.6},
          "typography": {
            "font": "Segoe UI",
            "size": 32,
            "weight": 700,
            "color": "#2E2F32"
          },
          "css_class": "slide__title",
          "html_tag": "h1"
        },
        {
          "id": "kpi_grid",
          "type": "group",
          "layout": "grid",
          "grid_cols": 4,
          "gap": "24px",
          "children": [/* KPI card specs */]
        }
      ]
    }
  ],
  "design_tokens": {
    "colors": { /* extracted colors */ },
    "typography": { /* extracted fonts */ },
    "spacing": { /* extracted spacing */ },
    "shadows": { /* extracted shadows */ },
    "border_radius": { /* extracted radius */ }
  },
  "component_library": {
    "button": { /* spec */ },
    "card": { /* spec */ },
    "kpi_metric": { /* spec */ }
  }
}
```

---

## 🔄 Design-to-Code Workflow

### Step 1: Extract
```bash
python extract_design.py input.pptx --format json
# Outputs: design_spec.json
```

### Step 2: Normalize
```bash
python normalize_spec.py design_spec.json --system walmart
# Outputs: design_spec_normalized.json (mapped to design system)
```

### Step 3: Generate Code
```bash
python generate_html.py design_spec_normalized.json --output html/
python generate_css.py design_spec_normalized.json --output css/
python generate_tokens.py design_spec_normalized.json --output tokens.css
# Outputs: HTML templates, CSS files, design tokens
```

### Step 4: Validate
```bash
python validate_output.py html/ css/
# Check:
# - All colors extracted
# - Typography matches system
# - Spacing uses 8px grid
# - Generated CSS passes linting
```

---

## 🎯 Measurement Baseline for QA

### Visual Regression Testing Setup
```python
def create_measurement_baseline(pptx_path, output_path):
    """
    Generate baseline measurements for visual regression testing
    Used to catch unintended design changes
    """
    baseline = {
        'design_file': pptx_path,
        'generated_at': datetime.now(),
        'measurements': extract_measurements(pptx_path),
        'colors': extract_colors(pptx_path),
        'typography': extract_typography(pptx_path),
    }
    
    with open(output_path, 'w') as f:
        json.dump(baseline, f, indent=2)
    
    return baseline

# Usage: pytest with baseline comparison
# if abs(actual_measurement - baseline_measurement) > 2:
#     raise AssertionError("Design changed unexpectedly")
```

---

## 🔗 Integration Points

- **pptx-expert**: Source for measurement extraction
- **design-system-validator**: Validate extracted tokens
- **layout-composition-analyzer**: Verify layout grid adherence
- **a11y-wcag-auditor**: Check generated CSS for a11y
- **Designer Orchestrator**: Final code generation pass
- **Task Rabbit**: Track specification documentation

---

## 📤 Output Deliverables

```
design_exports/
├── design_spec.json            # Complete specification
├── design_tokens.css           # CSS custom properties
├── components/
│   ├── button.html
│   ├── card.html
│   ├── kpi-metric.html
│   └── table.html
├── styles/
│   ├── base.css
│   ├── layout.css
│   ├── typography.css
│   ├── components.css
│   └── variables.css
├── measurements_baseline.json   # For regression testing
└── spec_report.html            # Human-readable spec doc
```

---

## 📝 Spec Report Template

```html
<!-- Spec Report: For developers implementing design -->
<div class="spec-container">
  <h1>Design Specification Report</h1>
  
  <section class="tokens">
    <h2>Design Tokens</h2>
    <table>
      <tr><th>Token</th><th>Value</th><th>CSS Variable</th></tr>
      <tr><td>blue-100</td><td>#0053E2</td><td>var(--color-blue-100)</td></tr>
      <!-- ... -->
    </table>
  </section>
  
  <section class="components">
    <h2>Components</h2>
    <!-- Component specs with visual examples -->
  </section>
</div>
```