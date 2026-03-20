---
name: a11y-wcag-auditor
description: "WCAG 2.2 Level AA design auditor — color contrast, text readability, motion/animation safety, color-blindness testing, font sizing, spacing for dyslexia, keyboard navigation, screen reader optimization, and accessibility compliance scoring."
version: 1.0.0
author: jac007x
tags:
  - accessibility
  - wcag
  - a11y
  - wcag2.2
  - inclusive-design
  - color-blindness
  - dyslexia
---

# ♿ A11Y WCAG Auditor — Inclusive Design Validator

Ensures all designs meet WCAG 2.2 Level AA accessibility standards for vision, motor, cognitive, and vestibular disabilities.

---

## 📏 WCAG 2.2 Level AA Standards

### 1. Contrast Ratios (Criterion 1.4.3)

#### Text Contrast (Foreground vs Background)
```python
CONTRAST_MINIMUMS = {
    'body_text': 4.5,      # Strict: 12px+ needs 4.5:1
    'large_text': 3.0,     # 18px+ or 14px bold needs 3:1
    'ui_components': 3.0,  # Buttons, icons, focus indicators
    'graphical_objects': 3.0, # Charts, maps
}

def calculate_contrast(rgb1, rgb2):
    """
    WCAG contrast formula:
    (L1 + 0.05) / (L2 + 0.05)
    Where L = relative luminance
    """
    def luminance(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        r = r/12.92 if r <= 0.03928 else ((r+0.055)/1.055) ** 2.4
        g = g/12.92 if g <= 0.03928 else ((g+0.055)/1.055) ** 2.4
        b = b/12.92 if b <= 0.03928 else ((b+0.055)/1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    l1 = luminance(rgb1)
    l2 = luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

# Examples
contrast(white, black)      # 21:1 ✓ Perfect
contrast(blue_100, white)   # 8.5:1 ✓ Excellent
contrast(gray_100, white)   # 5.2:1 ✓ Passes AA
contrast(gray_50, white)    # 3.0:1 ✗ Fails for body text
```

### 2. Text Sizing (Criterion 1.4.4)

```python
TEXT_SIZING = {
    'minimum_body': 12,  # Never below (except captions)
    'recommended_body': 14,  # Sweet spot for reading
    'minimum_labels': 10,  # Form labels, small UI
    'minimum_captions': 8,  # Chart labels, footnotes
}

# Scalability
# Designs must work at 200% zoom without horizontal scrolling
# Line height: 1.5x for body text minimum
# Letter spacing: 0.12em minimum for paragraphs
LINE_HEIGHT = 1.5
LETTER_SPACING = '0.12em'
```

### 3. Color Not Sole Indicator (Criterion 1.4.1)

**Red & Green Colorblindness Affects 8% of males, 0.5% of females**

```python
COLORBLINDNESS_TYPES = {
    'protanopia': 'Red-blind (missing long wavelengths)',
    'deuteranopia': 'Green-blind (missing medium wavelengths)',
    'tritanopia': 'Blue-yellow blind (rare)',
    'achromatopsia': 'Complete color blindness (very rare)',
}

# DO NOT use:
# Red + Green for status (use red + blue instead)
# Color alone to show success/failure (always pair with icons: ✓ ✗)
# Gradients as primary indicator

# DO use:
# Icon + color (✓ green, ✗ red, ℹ blue)
# Pattern + color (solid + striped)
# Text labels + color ("Success" + green)
# Symbol + color (arrow + red for down, arrow + green for up)
```

#### Safe Color Combinations
```python
SAFE_PAIRS = [
    ('blue', 'yellow'),     # High contrast, colorblind-safe
    ('blue', 'orange'),     # Good for protanopia/deuteranopia
    ('black', 'yellow'),    # Highest contrast
    ('white', 'dark blue'), # Standard accessibility
    ('green', 'magenta'),   # Deuteranopia friendly
]

# Test with Sim Daltonism or https://www.color-blindness.com/coblis/
```

---

## 👁️ Vision-Related Standards

### Font Choices for Readability

| Font Type | Accessibility | Use Case | Avoid |
|---|---|---|---|
| **Sans-serif** (Segoe UI, Arial, Helvetica) | Excellent | Body text, UI | Script fonts for body |
| **Serif** (Georgia, Times) | Good | Headings (optional) | Serif for small text |
| **Monospace** (Monaco, Courier) | Good | Code blocks | Avoid for body |
| **Dyslexia-friendly** (Dyslexie, OpenDyslexic) | Excellent | Long-form docs | Not for UI labels |

### Blur & Distortion
- No blur on text (especially small text)
- No extreme italics (>15° lean)
- No text on noisy backgrounds
- Solid backgrounds recommended

### Motion & Animation (Criterion 2.3.3)
```python
MOTION_SAFETY = {
    'flashing': 'Max 3 flashes per second (avoid seizures)',
    'animation': 'Provide pause/stop controls',
    'parallax': 'Disable if motion-reduce preference set',
    'auto_play': 'Never auto-play videos with sound',
    'prefers_reduced_motion': 'Respect CSS @media (prefers-reduced-motion)',
}

# CSS safety
# @media (prefers-reduced-motion: reduce) {
#   * { animation: none !important; transition: none !important; }
# }
```

---

## 🎮 Motor & Interaction (Criterion 2.1.1)

### Keyboard Navigation
- [ ] All interactive elements reachable via Tab key
- [ ] Logical tab order (left→right, top→bottom)
- [ ] Focus indicator always visible (min 2px border or outline)
- [ ] No keyboard traps (can Tab out of any element)
- [ ] Minimum click target: 44×44px (WCAG 2.5.5)

### Touch Targets
```python
TOUCH_TARGETS = {
    'minimum': (44, 44),  # pixels
    'recommended': (48, 48),
    'spacing': 8,  # minimum gap between targets
}

# Pointer-size adaptations
# coarse pointer (touch): 44×44px
# fine pointer (mouse): 24×24px minimum (but 44px better)
# stylus: 24×24px
```

### Mobile/Touch Considerations
- [ ] Links/buttons large enough for thumb (44px minimum)
- [ ] Spacing between interactive elements (8-16px)
- [ ] No hover-only functionality
- [ ] Avoid pinch-to-zoom blocking
- [ ] Responsive design scales properly

---

## 🧠 Cognitive (WCAG 2.0 + Best Practices)

### Language & Clarity
- [ ] Clear, simple language (8th-grade reading level)
- [ ] Short sentences (15-20 words max)
- [ ] Avoid jargon without explanation
- [ ] Define acronyms on first use
- [ ] Consistent terminology

### Dyslexia-Friendly Design
```python
DYSLEXIA_RULES = {
    'font_size': '14-16px minimum',
    'line_height': '1.5-2.0',
    'letter_spacing': '0.1-0.15em',
    'word_spacing': '0.16em',
    'column_width': '60-70 characters',
    'background': 'Non-white (off-white, light gray, cream)',
    'font_weight': '400-500 (not thin or heavy)',
    'alignment': 'Left-align (avoid justify)',
}

# Fonts: sans-serif preferred
# Use serif only for headings
# Avoid: Comic Sans (ironic!), Segoe Print, cursive styles
```

### ADHD-Friendly Design
- Chunked content (max 5 items per section)
- Clear visual hierarchy
- No distracting animations
- Predictable navigation
- Consistent layout patterns
- Strong affordances (obvious clickability)

---

## 🔍 Accessibility Audit Checklist

### Criterion 1.4.3: Contrast (Vision)
- [ ] Body text: 4.5:1 minimum contrast
- [ ] Large text (18px+): 3:1 minimum
- [ ] UI components (buttons, borders): 3:1 minimum
- [ ] Graphical objects (icons, data): 3:1 minimum
- [ ] No reliance on color alone (pair with icon/text/pattern)

### Criterion 1.4.4: Resize Text (Vision)
- [ ] Text resizable to 200% without loss of content
- [ ] Line height 1.5+ for body text
- [ ] Minimum font size 12px (preferably 14px)
- [ ] Letter spacing 0.12em in paragraphs

### Criterion 2.1.1: Keyboard (Motor)
- [ ] All interactive elements keyboard accessible
- [ ] Logical, visible focus indicator
- [ ] No keyboard traps
- [ ] Tab order makes sense

### Criterion 2.5.5: Touch Target Size (Motor)
- [ ] Buttons/links 44×44px minimum
- [ ] Spacing 8px+ between targets
- [ ] No accidental activation (adequate spacing)

### Criterion 2.4.7: Focus Visible (Motor)
- [ ] Focus indicator obvious (2px+ border/outline)
- [ ] Contrast 3:1 against background
- [ ] Visible in all color modes

### Criterion 2.3.3: Animation (Vestibular)
- [ ] No content flashing >3x/second
- [ ] Pause controls for animations
- [ ] Respect `prefers-reduced-motion`
- [ ] No auto-playing video with sound

### Cognitive Best Practices
- [ ] Clear, simple language
- [ ] Consistent terminology
- [ ] Predictable navigation
- [ ] Error prevention (confirmations for destructive actions)
- [ ] Error recovery (clear error messages, undo options)

---

## 📊 Accessibility Scoring Model

```python
A11Y_CRITERIA = {
    'contrast': {
        'weight': 0.25,
        'body_text': {'points': 10, 'min': 4.5},
        'ui_elements': {'points': 10, 'min': 3.0},
    },
    'readability': {
        'weight': 0.20,
        'font_size': {'points': 10, 'min': 12},
        'line_height': {'points': 10, 'min': 1.5},
    },
    'motor': {
        'weight': 0.20,
        'touch_target': {'points': 15, 'min': 44},
        'keyboard_nav': {'points': 10, 'min': 100},
    },
    'cognition': {
        'weight': 0.15,
        'language_clarity': {'points': 15, 'min': 80},
        'chunking': {'points': 10, 'min': 100},
    },
    'motion': {
        'weight': 0.10,
        'no_seizure_risk': {'points': 15, 'min': 100},
        'reduced_motion': {'points': 10, 'min': 100},
    },
    'color_blindness': {
        'weight': 0.10,
        'not_sole_indicator': {'points': 20, 'min': 100},
    },
}

def audit_accessibility(design):
    """
    Returns compliance score, violations, and remediation guide.
    WCAG 2.2 Level AA = must meet all Criterion 1.4.3, 2.1.1, 2.3.3, etc.
    """
    pass
```

---

## 🎨 Accessible Color Palettes

### Walmart + WCAG AA Safe
```python
ACCESSIBLE_COMBOS = [
    # Text on white background
    ('blue.100', 'white'),      # 8.5:1 ✓ Great
    ('gray.160', 'white'),      # 14:1 ✓ Great
    ('red.100', 'white'),       # 5.3:1 ✓ Good
    ('green.100', 'white'),     # 6.8:1 ✓ Good
    
    # On colored backgrounds
    ('white', 'blue.100'),      # 8.5:1 ✓ Great
    ('white', 'gray.160'),      # 14:1 ✓ Great
    ('blue.100', 'cyan.50'),    # 4.5:1 ✓ Good
    
    # FAIL patterns
    ('spark.100', 'white'),     # 3.6:1 ✗ Fails (use dark text)
    ('gray.50', 'white'),       # 3.0:1 ✗ Fails for body (OK for UI)
]
```

---

## 🔗 Integration Points

- **design-system-validator**: Check colors meet WCAG before approval
- **layout-composition-analyzer**: Ensure whitespace aids readability
- **pptx-expert**: Validate slide text contrast and sizing
- **slide-analyzer**: Run a11y audit as part of visual QA
- **Designer Orchestrator**: Third pass, before finalization
- **Task Rabbit**: Log a11y debt and track remediation

---

## 📋 Output Format

```json
{
  "design_id": "Q4_MBR_Deck",
  "wcag_level": "AA",
  "compliance": "PASS",
  "overall_score": 94,
  "scores_by_criterion": {
    "contrast": 95,
    "readability": 92,
    "motor": 96,
    "cognition": 90,
    "motion": 100,
    "color_blindness": 88
  },
  "violations": [
    {"criterion": "1.4.3", "issue": "Chart legend gray text", "contrast": "3.2:1", "min": "4.5:1", "severity": "critical", "fix": "Use gray.160 instead"}
  ],
  "warnings": [
    {"criterion": "1.4.4", "issue": "Caption text 10px", "recommendation": "Increase to 12px for better readability"}
  ],
  "color_blindness_test": "PASS (protanopia/deuteranopia safe)",
  "remediation_priority": ["Fix chart legend contrast", "Increase caption font size"],
  "estimated_effort": "15 minutes"
}
```