---
name: layout-composition-analyzer
description: "Visual composition expertise — golden ratio, rule of thirds, balance, visual flow, whitespace, alignment grids, Gestalt principles, S-curve patterns, Z-pattern reading paths, focal points, and layout scoring."
version: 1.0.0
author: jac007x
tags:
  - layout
  - composition
  - visual-design
  - balance
  - whitespace
  - gestalt
  - design-principles
---

# 🎯 Layout & Composition Analyzer — Visual Harmony Engine

Applies foundational design principles to evaluate and improve visual composition, balance, hierarchy, and user reading patterns.

---

## 📐 Grid Systems & Layout Foundations

### 12-Column Responsive Grid
```
Desktop (1200px):  12 columns @ 60px + 20px gutters
Tablet (768px):    8 columns @ 60px + 16px gutters
Mobile (375px):    4 columns @ 50px + 12px gutters

Margin: 32px (desktop), 24px (tablet), 16px (mobile)
Gutter: 20px (desktop), 16px (tablet), 12px (mobile)
```

### Slide Grid (PowerPoint 16:9 = 13.333" × 7.5")
```
Logical grid: 13 columns × 7.5 rows (1px = 0.1")
Safe area margins: 0.5" all sides
Content grid: 12.333" × 6.5" (inner area)
```

---

## ⚡ Golden Ratio & Divine Proportions

### The Phi (φ) Ratio: 1.618

```
Application in layout:
- Large element : Small element = 1.618 : 1
- Image width : Image height recommendations
- Primary content : Sidebar = 1.618 : 1

Example for 16:9 slide:
13.333" × φ = 21.6" (if full width)
Or: Primary content width = 8.5", sidebar = 3.5" (ratio 2.4:1, close to φ)
```

### Practical Golden Ratio Breakdown
- 60% / 40% split (close to golden)
- 70% / 30% split (common in presentations)
- 65% / 35% split ("sweet spot" for charts + callout)

---

## 🔲 Rule of Thirds & Focal Points

### Grid Overlay
```
┌───────┬───────┬───────┐
│       │  ◉    │       │  Divide space into 9 equal sections
├───────┼───────┼───────┤
│  ◉    │       │  ◉    │  Place important elements at intersections
├───────┼───────┼───────┤
│       │  ◉    │       │  Never center unless intentional symmetry
└───────┴───────┴───────┘
```

### Focal Point Hierarchy
1. **Primary focus** (top-left for Western readers, or top-center for symmetry)
2. **Secondary focus** (right-aligned for data, right-top for CTAs)
3. **Tertiary focus** (bottom callout or footer info)
4. **Supporting elements** (low visual weight, neutral spacing)

---

## ⚖️ Balance Types

### Symmetrical Balance
- **Use case:** Formal, trustworthy, structured (annual reports, executive decks)
- **Pattern:** Mirror left/right or top/bottom
- **Risk:** Can feel static or boring
```
    ┌─────────────┐
    │  Title      │  Centered title
    └─────────────┘
  ┌────┐       ┌────┐
  │ A  │       │ B  │  Two equal columns
  └────┘       └────┘
```

### Asymmetrical Balance
- **Use case:** Dynamic, modern, engaging (product decks, innovation)
- **Pattern:** Small heavy element ≈ large light element
- **Math:** Dense 30% + Whitespace 70% = Visual balance
```
  ┌──────────────┐
  │ Title        │  Large text block
  │ Long story   │
  │ here...      │
  └──────────────┘
                  ┌──┐
                  │  │  Small graphic
                  │  │
                  └──┘
```

### Radial Balance
- **Use case:** Focal point at center (rarely used in enterprise)
- **Pattern:** Elements radiating from center
- **Risk:** Distracting; use sparingly

---

## 👁️ Visual Flow & Reading Patterns

### Z-Pattern (Left-to-Right / Top-to-Bottom)
```
┌─→─→─→─→─→─→┐
│             │
│  Start      │
│             ↘
│          Middle
│             ↙
└─→─→─→─→─→─→┘
         End
```
**Best for:** Simple 2-3 element layouts, hero + content

### F-Pattern (Headline → Content → Sidebar)
```
┌──────────────────┐
│ HEADLINE ←── 1   │
├──────────────────┤
│ Content text... │
│ More text...    │← 2
│ Even more...    │
└──────────────────┘
```
**Best for:** Text-heavy layouts, blog posts

### S-Curve (Smooth, Playful)
```
  ┌─────────────┐
  │   Image     │
  │             │
  ├─────────────┤
        ↓
  ┌─────────────┐
  │   Content   │
  │             │
  └─────────────┘
```
**Best for:** Modern dashboards, storytelling decks

### Grid-Based (Modular)
```
┌────┬────┬────┐
│ 1  │ 2  │ 3  │
├────┼────┼────┤
│ 4  │ 5  │ 6  │
└────┴────┴────┘
```
**Best for:** KPI dashboards, image galleries, multi-story layouts

---

## 🤝 Gestalt Principles

| Principle | Definition | Application |
|---|---|---|
| **Proximity** | Elements close together are perceived as related | Group related KPIs, keep callouts near data |
| **Similarity** | Same color/shape/size = same meaning | Consistent button styling, data series coloring |
| **Continuity** | Eye follows smooth paths | Align elements on baseline grid, use flow lines |
| **Closure** | Brain completes incomplete forms | Charts don't need all gridlines; subtle icons work |
| **Figure-Ground** | Distinguish foreground from background | High contrast for primary content, gray.10 for bg |
| **Symmetry** | Balanced, mirrored layouts feel stable | Executive decks (symmetry), modern designs (asymmetry) |

---

## 🎨 Whitespace (Negative Space) Strategy

### Whitespace Ratios
```
High whitespace (60% empty): Luxury, premium, calm feeling
Moderate (40-50%): Balanced, professional, readable
Low (<30%): Dense, data-heavy, urgent/action-oriented
```

### Whitespace Rules
- **Breathing room:** 1-2 grid units around text blocks
- **Element separation:** 2-3 grid units between major sections
- **Card padding:** 1.5-2 grid units inside cards
- **Never jam:** If it feels crowded, add 20% more space

### Micro-Whitespace (Letter/Line/Word Spacing)
```python
LINE_HEIGHT = 1.5  # 50% extra space for readability
LETTER_SPACING = 0.5px  # For headlines only
WORD_SPACING = 0.25em  # Automatic in most tools
```

---

## 📊 Composition Scoring Rubric

```python
COMPOSITION_SCORE = {
    'balance': 0-20,           # Symmetry or intentional asymmetry
    'hierarchy': 0-20,         # Visual weight distribution
    'whitespace': 0-15,        # Breathing room, not cramped
    'alignment': 0-15,         # Grid adherence
    'focal_point': 0-15,       # Clear primary focus
    'reading_flow': 0-15,      # F/Z/S pattern logic
}

def score_layout(slide_or_design):
    """
    Returns:
    - composite_score (0-100)
    - breakdown by dimension
    - improvement suggestions
    """
    pass
```

### Scoring Guide
- **90-100 (A+):** Excellent balance, clear hierarchy, natural flow
- **80-89 (A):** Strong composition with minor tweaks possible
- **70-79 (B):** Decent layout but could improve whitespace or flow
- **60-69 (C):** Cramped, unclear hierarchy, needs rework
- **<60 (F):** Poor balance, illegible, needs major redesign

---

## ✅ Composition Audit Checklist

### Balance
- [ ] Visual weight distributed (either symmetric or intentionally off-center)
- [ ] Heavy elements (images, text) balanced by lighter areas
- [ ] No single corner dominates (unless rule of thirds focal point)

### Hierarchy
- [ ] Headline is largest and most prominent
- [ ] Supporting text clearly secondary (size, weight, color)
- [ ] Tertiary info (captions, footnotes) visually recessed
- [ ] Element size matches importance

### Whitespace
- [ ] Minimum 20% empty space (except data-heavy dashboards)
- [ ] Breathing room around text blocks (not pressed to edges)
- [ ] Consistent padding within containers
- [ ] No orphaned single words or awkward line breaks

### Alignment
- [ ] All elements snap to 8px grid
- [ ] Consistent left/right/center alignment within sections
- [ ] Vertical rhythm maintained (elements align top/middle/bottom)
- [ ] Tabular data right-aligned, text left-aligned

### Focal Point
- [ ] Clear primary focus area (top-left, center, or strategic position)
- [ ] Secondary elements support without competing
- [ ] Reading path obvious (F, Z, S, or Grid pattern)
- [ ] No visual conflicts (clashing colors, overlapping elements)

### Visual Flow
- [ ] Natural reading progression (matches Western left-to-right)
- [ ] Motion suggested by arrows, lines, or element arrangement
- [ ] Grouped related content (proximity principle)
- [ ] Chunking reduces cognitive load

---

## 🔧 Composition Improvement Patterns

### Problem: Elements Too Close
**Solution:** Add white space
- Increase margins: 8px → 16px → 24px
- Move elements further apart
- Use negative space intentionally

### Problem: Layout Feels Heavy/Cramped
**Solution:** Improve balance
- Reduce number of elements (cut non-essentials)
- Increase font size (gives room for whitespace)
- Use taller line height (more breathing room)
- Break into 2-3 shorter sections instead of 1 long block

### Problem: No Clear Focal Point
**Solution:** Create hierarchy
- Make headline 2-3x larger than body
- Use color to highlight key number
- Add subtle background shape to frame focal area
- Position at rule-of-thirds intersection

### Problem: Reading Path Unclear
**Solution:** Guide the eye
- Add subtle arrows or flow lines
- Use size/color to create progression
- Number steps if sequential
- Align elements to create visual pathway

---

## 🔗 Integration Points

- **pptx-expert**: Layout templates validated against composition rules
- **data-viz-expert**: Chart positioning and whitespace planning
- **slide-analyzer**: Visual QA includes composition scoring
- **Designer Orchestrator**: Second pass after design system validation
- **Task Rabbit**: Track layout debt and improvement opportunities

---

## 📋 Output Format

```json
{
  "slide_id": "MBR_Deck_Slide_03",
  "composition_score": 82,
  "grade": "A",
  "scores_by_dimension": {
    "balance": 18,
    "hierarchy": 19,
    "whitespace": 12,
    "alignment": 15,
    "focal_point": 14,
    "reading_flow": 14
  },
  "reading_pattern_detected": "Z-pattern",
  "whitespace_percentage": 35,
  "alignment_grid_adherence": 92,
  "issues": [
    {"dimension": "whitespace", "issue": "Bottom callout too close to footer", "fix": "Add 16px margin-top"}
  ],
  "suggestions": [
    "Consider larger headline for stronger hierarchy",
    "Chart callout could move to right for balance"
  ]
}
```