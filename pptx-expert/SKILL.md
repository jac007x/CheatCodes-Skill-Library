---
name: pptx-expert
description: "Expert python-pptx mastery + executive slide design principles — charts, tables, shapes, layouts, McKinsey rules, typography hierarchy, Walmart brand compliance, conditional formatting, and MBR engine integration."
version: 2.0.0
author: jac007x
tags:
  - pptx
  - powerpoint
  - charts
  - tables
  - shapes
  - design
  - layout
  - typography
  - walmart
  - mbr-engine
---

# 🎨 PPTX Expert — PowerPoint Mastery + Design Principles

Expert-level PowerPoint engineering via `python-pptx` combined with executive slide design rules.

---

## 🧠 The McKinsey Slide Rules

1. **One slide = one message** — single clear takeaway in the title
2. **Action titles, not topic titles** — “Revenue grew 12% QoQ driven by e-commerce” NOT “Q4 Revenue”
3. **3-second rule** — viewer grasps the point within 3 seconds
4. **Visual hierarchy** — size, weight, color, position create reading order
5. **Less is more** — every element earns its place or gets removed
6. **6×6 rule** — max 6 bullets, max 6 words per bullet
7. **No 3D effects** — ever. Flat design only.

---

## 📐 Layout System

### Slide Structure
```
┌─────────────────────────────────────────────────────┐
│  TITLE BAR (0.2–0.8")  │ Date │  Action title   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  CONTENT AREA (40-60px margins all sides)            │
│                                                     │
├─────────────────────────────────────────────────────┤
│  FOOTER: Source | Page X of Y | Date                 │
└─────────────────────────────────────────────────────┘
```

### Layout Templates

| Layout | When | Structure |
|---|---|---|
| Full Chart | Single viz tells story | Title + 1 chart filling area |
| Chart + Callout | Chart needs context | 70% chart, 30% insight |
| Two-Column | Comparison | 50/50 or 60/40 split |
| Dashboard Grid | Multiple KPIs | 2×2 or 2×3 grid |
| Big Number | Single KPI is story | Giant number + context |
| Table | Detailed comparison | Full-width header table |
| Section Divider | Topic transition | Full-bleed color + title |

### Position Constants (16:9 = 13.333×7.5")
```python
from pptx.util import Inches
TITLE_POS      = (Inches(0.5), Inches(0.2), Inches(9), Inches(0.6))
SUBTITLE_POS   = (Inches(0.5), Inches(0.7), Inches(9), Inches(0.4))
FULL_CHART     = (Inches(0.5), Inches(1.3), Inches(12.3), Inches(5.5))
HALF_LEFT      = (Inches(0.5), Inches(1.3), Inches(6), Inches(5.5))
HALF_RIGHT     = (Inches(6.8), Inches(1.3), Inches(6), Inches(5.5))
DATE_POS       = (Inches(9.5), Inches(0.3), Inches(3.3), Inches(0.3))
FOOTNOTE_POS   = (Inches(0.5), Inches(7.0), Inches(8), Inches(0.3))
```

---

## ✏️ Typography Hierarchy

| Element | Size | Weight | Color | python-pptx |
|---|---|---|---|---|
| Slide Title | 24-28pt | Bold | gray.160 (#2E2F32) | `Pt(24)`, `.bold=True` |
| Subtitle | 14-18pt | Semi-bold | gray.140 | `Pt(14)` |
| Body | 10-12pt | Regular | gray.140 | `Pt(11)` |
| Table cells | 9pt | Regular | gray.160 | `Pt(9)` |
| Data labels | 7-8pt | Medium | gray.120 | `Pt(7)` |
| Footnotes | 7pt | Regular | gray.100 | `Pt(7)` |
| KPI Number | 36-48pt | Bold | blue.100 | `Pt(36)` |

**Rules:** Max 2 fonts per deck · Max 3 sizes per slide · Never all-caps body text · Line height 1.4-1.6 · Left-align body (center only titles)

---

## 🎨 Walmart Brand Palette (python-pptx)

```python
from pptx.dml.color import RGBColor

WMT_BLUE    = RGBColor(0x00, 0x53, 0xE2)  # Primary
WMT_SPARK   = RGBColor(0xFF, 0xC2, 0x20)  # Accent (never for text—fails contrast)
WMT_GREEN   = RGBColor(0x2A, 0x87, 0x03)  # Success
WMT_RED     = RGBColor(0xEA, 0x11, 0x00)  # Danger
WMT_CYAN    = RGBColor(0x00, 0x96, 0xD6)  # Info
GRAY_160    = RGBColor(0x2E, 0x2F, 0x32)  # Primary text
GRAY_100    = RGBColor(0x74, 0x76, 0x7B)  # Secondary text
GRAY_50     = RGBColor(0xD9, 0xD9, 0xD9)  # Borders
GRAY_10     = RGBColor(0xF5, 0xF5, 0xF5)  # Subtle backgrounds
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)

CHART_PALETTE = [WMT_BLUE, WMT_SPARK, WMT_GREEN, WMT_CYAN,
                 RGBColor(0x76, 0x23, 0x8C), WMT_RED]
RAG_RED_BG    = RGBColor(0xFC, 0xE4, 0xE1)
RAG_YELLOW_BG = RGBColor(0xFF, 0xF4, 0xD4)
RAG_GREEN_BG  = RGBColor(0xE7, 0xF5, 0xE2)
```

---

## 📊 Charts (python-pptx API)

```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_MARKER_STYLE
from pptx.util import Inches, Pt

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])  # blank

data = CategoryChartData()
data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
data.add_series('Revenue', (120, 135, 148, 162))
data.add_series('Target',  (130, 130, 140, 155))

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(0.5), Inches(1.5), Inches(9), Inches(5), data)
chart = chart_frame.chart
```

**Supported types:** `COLUMN_CLUSTERED/STACKED/STACKED_100`, `BAR_*`, `LINE/LINE_MARKERS/LINE_STACKED`, `PIE`, `DOUGHNUT`, `AREA/AREA_STACKED`, `XY_SCATTER/XY_SCATTER_LINES`, `BUBBLE`

**Essential styling:**
```python
# Legend
chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.BOTTOM
chart.legend.include_in_layout = False
chart.legend.font.size = Pt(9)

# Axes
va = chart.value_axis
va.minimum_scale = 0; va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = GRAY_50
va.major_gridlines.format.line.width = Pt(0.5)
va.tick_labels.font.size = Pt(8)
va.tick_labels.number_format = '#,##0'  # or '0.0%' for percentages
ca = chart.category_axis
ca.tick_labels.font.size = Pt(8)
ca.has_major_gridlines = False

# Series colors
for i, s in enumerate(chart.series):
    s.format.fill.solid()
    s.format.fill.fore_color.rgb = CHART_PALETTE[i % len(CHART_PALETTE)]
    s.has_data_labels = True
    s.data_labels.font.size = Pt(7)
    s.data_labels.number_format = '#,##0'
    s.data_labels.show_value = True
```

**Line with markers:** `series.format.line.width = Pt(2)`, `series.marker.style = XL_MARKER_STYLE.CIRCLE`, `series.marker.size = 8`

**Pie/Doughnut:** Use `XL_CHART_TYPE.DOUGHNUT`, max 5 slices, `point.format.fill.solid()` for slice colors.

**Replace existing chart data:** `chart.replace_data(new_chart_data)`

---

## 📝 Tables

```python
table_shape = slide.shapes.add_table(5, 4,
    Inches(0.5), Inches(1.5), Inches(9), Inches(4))
table = table_shape.table
table.columns[0].width = Inches(2.5)
```

**Cell styling utility:**
```python
from pptx.enum.text import PP_ALIGN

def style_cell(cell, text, bold=False, font_size=10,
               font_color=None, bg_color=None, alignment=None):
    cell.text = ""
    tf = cell.text_frame
    tf.word_wrap = True; tf.auto_size = None
    tf.margin_left = tf.margin_right = Pt(4)
    tf.margin_top = tf.margin_bottom = Pt(2)
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = str(text); run.font.size = Pt(font_size); run.font.bold = bold
    if font_color: run.font.color.rgb = font_color
    if alignment: p.alignment = alignment
    if bg_color: cell.fill.solid(); cell.fill.fore_color.rgb = bg_color
```

**Design rules:**
- Header row: blue.100 bg, white text, bold, centered
- Alternating rows: white / gray.10
- **Right-align numbers** (always) · Left-align text
- No vertical borders — horizontal rules only
- Max 8 columns × 12 rows per slide
- Consistent number formatting across columns

**Cell borders (XML):**
```python
from pptx.oxml.ns import qn
from lxml import etree

def set_cell_border(cell, color="D9D9D9", width=12700):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    for edge in ['lnL', 'lnR', 'lnT', 'lnB']:
        ln = etree.SubElement(tcPr, qn(f'a:{edge}'))
        ln.set('w', str(width))
        sf = etree.SubElement(ln, qn('a:solidFill'))
        etree.SubElement(sf, qn('a:srgbClr')).set('val', color)
```

**Merge cells:** `table.cell(0, 1).merge(table.cell(0, 3))`

**Conditional formatting patterns (HTML reports):**
```html
<span class="px-2 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700">On Track</span>
<span class="text-green-600">▲ 5.2%</span> | <span class="text-red-600">▼ 3.1%</span>
<td class="bg-green-50">98.5%</td>  <!-- heat-map cell -->
```

---

## 🔷 Shapes & Text Boxes

```python
from pptx.enum.shapes import MSO_SHAPE

# Text box
txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
tf = txBox.text_frame; tf.word_wrap = True
run = tf.paragraphs[0].add_run()
run.text = "Title"; run.font.size = Pt(24); run.font.bold = True
run.font.color.rgb = WMT_BLUE

# Callout box
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(6), Inches(4), Inches(0.8))
shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor(0xF0, 0xF7, 0xFF)
shape.line.color.rgb = WMT_BLUE; shape.line.width = Pt(1)

# RAG indicator
def add_rag_indicator(slide, left, top, color, label, value):
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, Inches(0.4), Inches(0.4))
    c.fill.solid(); c.fill.fore_color.rgb = color; c.line.fill.background()
    t = slide.shapes.add_textbox(left-Inches(0.3), top+Inches(0.45), Inches(1), Inches(0.5))
    r = t.text_frame.paragraphs[0].add_run()
    r.text = f"{label}\n{value}"; r.font.size = Pt(8)
```

**Shape usage rules:** Consistent border-radius · Subtle shadows only · Max 3 shape types/slide · Shapes must contain content (no decoration)

---

## 🖼️ Images & Logos

```python
slide.shapes.add_picture('chart.png', Inches(0.5), Inches(1.5), Inches(8), Inches(4.5))

# From matplotlib BytesIO
import io; buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=150, bbox_inches='tight'); buf.seek(0)
slide.shapes.add_picture(buf, Inches(0.5), Inches(1.5), Inches(8), Inches(4.5))
```

---

## 🔧 Slide Basics

```python
# Layouts: 0=Title, 1=Title+Content, 5=Blank, 6=Title Only
slide = prs.slides.add_slide(prs.slide_layouts[5])

# Dimensions (16:9 default)
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

# Find shape by name or text
def find_shape(slide, name=None, text_contains=None):
    for s in slide.shapes:
        if name and s.name == name: return s
        if text_contains and s.has_text_frame and text_contains.lower() in s.text_frame.text.lower(): return s

# Inventory all shapes
def inventory_slide(slide):
    return [{'name': s.name, 'type': s.shape_type, 'left': s.left, 'top': s.top,
             'has_table': s.has_table, 'has_chart': s.has_chart,
             'text': s.text_frame.text[:100] if s.has_text_frame else None} for s in slide.shapes]
```

---

## 🧩 MBR Slide Composition Patterns

### Executive Summary
```
┌───────────────────────────────────────────┐
│ Executive Summary: [Period] Performance    │
├───────┬───────┬───────┬─────────────────┤
│ KPI1  │ KPI2  │ KPI3  │ KPI4            │
│$14.2M │ 98.5% │ 1.2M  │ 4.3★            │
│▲12.3% │▲ 0.5% │▼ 2.1% │▲ 0.2            │
├───────┴───────┴───────┴─────────────────┤
│ Key Insights:                              │
│ • Insight 1 with supporting data             │
│ • Insight 2 with action required              │
└───────────────────────────────────────────┘
```

### MBR Engine Integration
- `src/slide_assembler.py` — scorecard table population
- `src/appendix_assembler.py` — appendix slides
- `src/pptx_analyzer.py` — design audit + chart generation
- `config.py` — RAG_COLORS, METRIC_THRESHOLDS

**When modifying MBR slides:**
1. Read template with `Presentation(template_path)`
2. Use dynamic shape discovery (don't hardcode indices)
3. Preserve threshold cells (cols 1-3 on detail slides)
4. Carry RAG colors from detail → overview
5. Update "Data as of:" with snapshot date
6. Add slide numbers + CONFIDENTIAL watermark

### Brand Compliance Checklist
- [ ] blue.100 for main data + headers
- [ ] spark.100 as accent only (never for text)
- [ ] Text contrast ≥4.5:1
- [ ] No gradients on data elements
- [ ] Source attribution on every data slide
- [ ] Date/period clearly labeled
- [ ] Consistent rounded corners
