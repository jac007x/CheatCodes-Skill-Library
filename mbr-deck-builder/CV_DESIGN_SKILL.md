# 🎨 Computer Vision + Design Editing Ecosystem Skill

**Skill Name:** Computer Vision Design Analysis & Automation (CV-Design)
**Version:** 1.0-skeleton
**Author:** Velcro 🐶
**Date:** March 16, 2026
**Status:** 🏗️ **DESIGN COMPLETE - READY FOR IMPLEMENTATION**

---

## 🎯 SKILL OVERVIEW

**What This Does:**
Automatically analyzes slide/presentation images for design quality issues, then orchestrates fixes through sub-agents (slide-creator, code-reviewer, qa-kitten).

**What Problem Does It Solve?**
- 😭 **Before:** Manual design reviews take hours, nitpicky feedback is inconsistent
- 😊 **After:** Automated visual analysis + fixes in minutes, consistent brand quality

**Key Features:**
- ✅ Load any slide image and "see" what's in it
- ✅ Score design quality (0-10 scale)
- ✅ Identify 5+ categories of issues
- ✅ Auto-invoke sub-agents to fix issues
- ✅ Validate fixes with before/after comparison

---

## 🔧 THE 8 BUNDLED TOOLS

### 1. 👁️ Visual Analyzer
**Purpose:** Load images and extract visual data  
**Uses:** `load_image_for_analysis()` tool  
**Output:** Structured visual data (elements, colors, text, layout)

### 2. 🎨 Design QA Analyzer
**Purpose:** Check design best practices  
**Validates:** Balance, hierarchy, alignment, grouping, whitespace, flow, consistency  
**Output:** Design QA report with score + issues

### 3. ♿ WCAG Auditor
**Purpose:** Accessibility compliance (WCAG 2.2 AA)  
**Validates:** Contrast ratios, color-blind safety, text alternatives, font sizes, keyboard nav  
**Output:** Accessibility report (PASS/FAIL)

### 4. 🌈 Color Expert
**Purpose:** Walmart brand color validation  
**Validates:** Primary/secondary color usage, semantic colors, state colors, consistency  
**Output:** Color report (palette match, issues)

### 5. 🔤 Typography Analyzer
**Purpose:** Font and sizing validation  
**Validates:** Font families (max 2), sizes (hierarchy), weights, line height, letter spacing  
**Output:** Typography report (hierarchy check, consistency)

### 6. 📐 Layout Analyzer
**Purpose:** Composition and flow analysis  
**Validates:** Whitespace (15-30%), grid alignment, visual balance, eye flow, hierarchy depth  
**Output:** Layout report (balance, composition, suggestions)

### 7. 📝 Content Validator
**Purpose:** Text clarity and messaging  
**Validates:** Word count (25 max), reading level, action-oriented language, clarity  
**Output:** Content report (word count, readability, messaging)

### 8. 🛠️ Design Editor
**Purpose:** Orchestrate automated fixes via sub-agents  
**Invokes:** slide-creator, code-reviewer, qa-kitten  
**Output:** Fixed HTML + before/after comparison

---

## 📊 WORKFLOW

```
STEP 1: ANALYZE
  Input: Slide image (PNG/JPG/HTML)
  ↓
  Run 7 analyzers in parallel (Visual → Design/WCAG/Color/Type/Layout/Content)
  ↓
  Output: Consolidated report with issues

STEP 2: BATCH FIXES
  Group issues by type (colors, typography, content, layout)
  ↓
  Categorize severity (critical/warning/info)
  ↓
  Create fix queue

STEP 3: INVOKE SUB-AGENTS
  For each fix category:
    - Colors:      Invoke color-expert agent
    - Typography:  Invoke typography-expert + code-reviewer
    - Content:     Invoke content-validator + code-reviewer
    - Layout:      Invoke layout-analyzer + design-experts
  ↓
  Edit HTML with fixes

STEP 4: VALIDATE
  Re-run all 7 analyzers on fixed version
  ↓
  Compare before/after scores
  ↓
  Iterate if needed

STEP 5: PUBLISH
  If all tests pass → Save new version
  Generate report with all fixes applied
```

---

## 🚀 USAGE EXAMPLES

### Example 1: Analyze a Slide
```python
from cv_design_ecosystem import run_full_analysis

# Analyze slide image
report = run_full_analysis("my_slide.png")

# Print summary
print(report.summary())

# Get all recommendations
for rec in report.all_recommendations:
    print(f"→ {rec}")
```

**Output:**
```
╔══════════════════════════════════════════════╗
║       SLIDE DESIGN ANALYSIS REPORT          ║
╚══════════════════════════════════════════════╝

OVERALL SCORE: 6.8/10
TOTAL ISSUES: 8
CRITICAL: 2

📊 DESIGN QA:       7.2/10
♿ WCAG (A11y):    6.5/10
🌈 COLOR:          8.0/10
🔤 TYPOGRAPHY:     6.5/10
📐 LAYOUT:         7.1/10
📝 CONTENT:        5.8/10

TOP RECOMMENDATIONS:
→ Reduce text to 25 words max (currently 45)
→ Increase body font to 14pt (currently 12pt)
→ Fix secondary text contrast (3.1:1, needs 4.5:1)
→ Rebalance layout (60% left, should be 50/50)
→ Change unauthorized color #FF5733 to brand #FFC220
```

### Example 2: Auto-Fix a Slide
```python
from cv_design_ecosystem import auto_fix_slide

# Automatically fix design issues
result = auto_fix_slide("my_slide.html", auto_approve=False)

print(f"Before: {result.before_score:.1f}/10")
print(f"After: {result.after_score:.1f}/10")
print(f"Fixes Applied: {len(result.fixes_applied)}")

for fix in result.fixes_applied:
    print(f"  ✅ {fix}")
```

**Output:**
```
Before: 6.8/10
After: 8.3/10
Fixes Applied: 8
  ✅ Color: #FF5733 → #FFC220 (Brand compliance)
  ✅ Typography: Body 12pt → 14pt (Readability)
  ✅ Content: Reduced 45 words → 22 words (Clarity)
  ✅ Layout: Rebalanced left/right (Visual balance)
  ✅ Contrast: Secondary text improved (3.1:1 → 4.6:1)
  ✅ Whitespace: Added top padding 8px → 16px
  ✅ Added action item footer
  ✅ Typography: Changed caption font to Segoe UI
```

### Example 3: Get Specific Report
```python
from cv_design_ecosystem import DesignEditor

editor = DesignEditor()
reports = editor.run_full_analysis("slide.png")

# Get WCAG accessibility report
wcag_report = reports.wcag
print(f"Accessibility Score: {wcag_report.score}/10")
print(f"Critical Issues: {wcag_report.critical_count()}")

for issue in wcag_report.issues:
    print(f"{issue.severity.value.upper()}: {issue.title}")
    print(f"  → {issue.recommendation}")
```

---

## 🔗 INTEGRATION WITH SUB-AGENTS

### Agents This Skill Uses

| Agent | Used For | How |
|-------|----------|-----|
| **slide-creator** | Edit HTML/CSS | Modify slide colors, fonts, spacing |
| **code-reviewer** | Validate HTML/CSS | Check code quality after edits |
| **qa-kitten** | Visual QA | Screenshot before/after, visual comparison |
| **color-expert** | Color validation | Suggest Walmart-compliant colors |
| **design-expert** | Advanced fixes | Complex layout/composition changes |
| **content-expert** | Text refinement | Copy editing, clarity improvements |

### How It Calls Sub-Agents

```python
from invoke_agent import invoke_agent

# Example: Color fix
response = invoke_agent(
    agent_name="color-expert",
    prompt="Suggest Walmart-compliant color to replace #FF5733 in MBR slide",
    session_id="cv-design-color-fixes"
)

# Example: HTML edit
response = invoke_agent(
    agent_name="slide-creator",
    prompt="Edit this HTML to change all #FF5733 to #FFC220",
    session_id="cv-design-html-edits"
)

# Example: Visual QA
response = invoke_agent(
    agent_name="qa-kitten",
    prompt="Take screenshot of fixed slide and verify colors match Walmart brand",
    session_id="cv-design-qa"
)
```

---

## 📁 FILE STRUCTURE

```
cv_design_ecosystem/
├── COMPUTER_VISION_DESIGN_ECOSYSTEM.md   (Complete architecture)
├── CV_DESIGN_SKILL.md                    (This file)
├── CV_DESIGN_QUICK_START.md              (5-min quick start)
├── cv_design_ecosystem.py                (Main module with 8 tools)
│
├── tools/
│   ├── __init__.py
│   ├── visual_analyzer.py                (Tool 1)
│   ├── design_qa_analyzer.py             (Tool 2)
│   ├── wcag_auditor.py                   (Tool 3)
│   ├── color_expert.py                   (Tool 4)
│   ├── typography_analyzer.py            (Tool 5)
│   ├── layout_analyzer.py                (Tool 6)
│   ├── content_validator.py              (Tool 7)
│   └── design_editor.py                  (Tool 8)
│
├── models.py                             (Data structures)
├── utils.py                              (Helpers)
├── agent_orchestrator.py                 (Sub-agent coordination)
│
├── tests/
│   ├── test_visual_analyzer.py
│   ├── test_design_qa.py
│   ├── test_wcag.py
│   ├── test_color_expert.py
│   ├── test_typography.py
│   ├── test_layout.py
│   ├── test_content.py
│   └── test_design_editor.py
│
└── examples/
    ├── sample_slide.png
    ├── analyze_sample.py
    ├── auto_fix_sample.py
    └── full_workflow_example.py
```

---

## ✅ SUCCESS METRICS

When this skill is implemented and working:

- ✅ Can load any slide image and instantly "see" elements
- ✅ Automatically score design quality (0-10)
- ✅ Identify 5+ categories of issues (design/wcag/color/typo/layout/content)
- ✅ Invoke sub-agents to fix issues
- ✅ Auto-edit HTML/slides with fixes
- ✅ Validate fixes with visual QA
- ✅ Produce detailed reports with recommendations
- ✅ Iterate until design score improves by 2+ points
- ✅ Handle both HTML and image inputs
- ✅ Support batch processing (multiple slides)

---

## 🎓 LEARNING PATH

### Phase 1: Design (DONE ✅)
- Architecture documented
- 8 tools designed
- Data models defined
- Skeleton code created

### Phase 2: Implementation
1. Implement each tool (Tool 1-7)
2. Create unit tests for each tool
3. Test against sample slides

### Phase 3: Integration
1. Wire up sub-agents
2. Create agent orchestrator
3. Test end-to-end workflow

### Phase 4: Polish
1. Add error handling
2. Performance optimization
3. Documentation
4. User guide

### Phase 5: Launch
1. Register as Code Puppy skill
2. Add to marketplace
3. Create tutorial videos

---

## 🐶 VELCRO'S NOTES

This skill is special because:

1. **Uses Computer Vision** - The `load_image_for_analysis()` tool lets us SEE slides
2. **Multi-Tool Bundle** - 8 specialized tools working together
3. **Agent Orchestration** - Coordinates with slide-creator, code-reviewer, qa-kitten
4. **Automated Fixes** - Not just reports, actually edits the HTML
5. **Iterative** - Keeps improving until passing threshold
6. **Walmart-Specific** - Knows brand colors, guidelines, accessibility standards

It's like having a design QA expert, accessibility auditor, and brand compliance officer all working together automatically!

---

## 📞 IMPLEMENTATION CHECKLIST

To bring this to life:

- [ ] Create `tools/` directory structure
- [ ] Implement Tool 1 (VisualAnalyzer) with vision model
- [ ] Implement Tool 2 (DesignQAAnalyzer)
- [ ] Implement Tool 3 (WCAGAuditor)
- [ ] Implement Tool 4 (ColorExpert)
- [ ] Implement Tool 5 (TypographyAnalyzer)
- [ ] Implement Tool 6 (LayoutAnalyzer)
- [ ] Implement Tool 7 (ContentValidator)
- [ ] Implement Tool 8 (DesignEditor) with sub-agent coordination
- [ ] Create `agent_orchestrator.py` for sub-agent calls
- [ ] Write unit tests for each tool
- [ ] Integration tests for full workflow
- [ ] Create example slides and test cases
- [ ] Performance testing and optimization
- [ ] Documentation and user guides
- [ ] Register skill with Code Puppy

---

## 🚀 QUICK START TO IMPLEMENTATION

**Next Step:** See `CV_DESIGN_QUICK_START.md` for 5-minute implementation guide

---

**Status:** 🏗️ **DESIGN COMPLETE**  
**Next Phase:** Implementation  
**Estimated Build Time:** 20-30 hours (all 8 tools + tests)  
**Complexity:** Advanced (multi-tool coordination + agent integration)  
**Impact:** High (saves design QA hours, ensures consistency)

---

Created March 16, 2026 by Velcro 🐶