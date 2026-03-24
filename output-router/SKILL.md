---
name: output-router
description: "Transforms content between formats optimized for the target channel and audience — from analysis to summary, narrative to bullets, or full report to deck."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - formatting
  - transformation
  - communication
  - routing
model_recommendation: haiku
risk_level: low
---

# 🎯 Output Router

> The same insight, restructured for the channel that will actually be read — not just reformatted, but rebuilt for how your audience processes information.

## Core Philosophy

Every format has a reading contract — an implicit agreement between the content and the reader about how the information will be structured, what the reader needs to bring, and how much time it demands. A five-page analysis report makes a reading contract that says: bring 20 minutes, follow the argument linearly, tolerate uncertainty as the logic builds. An executive summary makes a contract that says: give me 90 seconds and I will tell you the three things that matter. A slide deck makes a contract that says: each frame is one idea, and the logic connects across frames rather than within them.

Transforming content between formats is not a cosmetic operation. Cutting an analysis report down to a five-sentence summary is not the same as transforming it. True transformation requires identifying the structural logic of the source, then rebuilding that logic according to the target format's conventions. A good executive summary does not simply remove words from the analysis; it answers the question "what does the decision-maker need to act?" — which is a different question than the analysis was built to answer. A good slide deck does not extract sentences and put them on slides; it redesigns the argument as a series of single claims, each defensible on its own, that add up to a conclusion.

This skill also exists to prevent a common failure: over-engineering the format for the audience. A team update that goes out as a 12-slide deck when an email would do is not more rigorous — it is harder to read, less likely to be consumed, and signals poor judgment about the audience's time. The output-router includes a fit-check step precisely to guard against this: the goal is the most effective format for this audience and this purpose, not the most elaborate.

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake Content and Target | E1 – Deterministic | DELEGATE | Structured collection of source, target format, audience, and constraints |
| 2. Analyze Content Structure | E3 – Analytical | NARRATE | Requires reasoning about what must be preserved vs. compressed |
| 3. Transform and Adapt | E4 – Generative then E3 | GENERATE then NARRATE | Generation applies the transform; validation checks completeness |
| 4. Validate Fit | E3 – Analytical | NARRATE | Checks output is structurally correct for the target format conventions |
| 5. Produce Formatted Output | E1 – Deterministic | DELEGATE | Delivers final output in target format with optional source mapping |

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{SOURCE_MATERIAL}}` | The full content to be transformed | string | Yes | — |
| `{{CHANNEL}}` | Target output format (see supported transformations below) | string | Yes | — |
| `{{AUDIENCE}}` | Who will receive the output and in what context | string | Yes | — |
| `{{CONSTRAINTS}}` | Length limits, style requirements, brand voice guidelines, or forbidden elements | string | No | None specified |
| `{{OBJECTIVE}}` | The purpose of the transformed output — what action or understanding it should produce | string | Yes | — |

## Supported Transformations

| Source Format | Target Format | Key Structural Change |
|---------------|---------------|----------------------|
| Full analysis (2,000+ words) | Executive summary (3-5 sentences) | Compress to decision-relevant claims only; remove methodology |
| Narrative report | Slide deck structure | Decompose argument into single-claim frames with visual logic |
| Qualitative data (open text) | Structured table | Affinity-group themes; assign counts; surface top themes |
| Data findings narrative | Visualization specification | Define chart type, axes, labels, and key callout for each finding |
| Long email | Bullet summary | Extract asks, context, and decisions; remove narrative scaffolding |
| Bullet list | Flowing narrative | Add connective tissue, transitions, and context |
| Technical report | Plain language summary | Rewrite for non-technical audience; replace jargon with analogies |
| Full report | 1-page brief | Apply inverted pyramid; lead with finding, follow with evidence |
| Meeting notes | Action item register | Extract owners, actions, and deadlines; discard discussion context |
| Research synthesis | Board-ready summary | Lead with so-what; reduce to 3-5 strategic implications |

## ⚙️ Phases

### Phase 1: Intake Content and Target
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Collect the source material and transformation parameters before any analysis begins. The most critical intake field is `{{OBJECTIVE}}` — not just what format is wanted, but what the transformed output is supposed to do. "Turn this into bullets" is a format instruction; "turn this into bullets so a busy manager can action the key points in under 2 minutes" is an objective that will produce a meaningfully better output.

Also probe for `{{CONSTRAINTS}}` actively. Common constraints that significantly affect transformation: word or slide count limits, brand voice requirements (formal vs. conversational), specific claims that must be included verbatim (e.g., legal language, approved messaging), and elements that must be excluded (e.g., preliminary data, named individuals, sensitive sub-analysis).

**Process:**
1. Collect `{{SOURCE_MATERIAL}}`, `{{CHANNEL}}`, `{{AUDIENCE}}`, and `{{OBJECTIVE}}`
2. Identify the source format by examining the source material structure (narrative vs. structured vs. data-heavy vs. mixed)
3. Confirm the target format is in the supported transformations list, or ask for clarification if the request is non-standard
4. Probe for constraints: length limit? named style guide? any must-include or must-exclude elements?
5. Assess source material completeness: if the source is fragmentary, ambiguous, or clearly a draft, flag this — transformation of incomplete source produces incomplete output

**Output:** A confirmed intake record with source format identified, target format confirmed, audience defined, objective stated, and constraints captured.

---

### Phase 2: Analyze Content Structure
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Before transforming, understand what you have. Identify the source material's structural elements: key claims (the assertions the content is making), supporting evidence (the data or reasoning behind each claim), action items (specific asks or decisions), and context-setting (background that is needed to understand the claims but not the claims themselves).

This structural analysis drives the transformation decision: which elements must survive the transformation intact, which can be compressed, which can be merged, and which can be dropped. Action items always survive intact. Key claims survive, though they may be restructured. Supporting evidence is compressible — the level of detail kept depends on the target format and audience need. Context-setting is usually the most aggressively compressed element in summary transformations.

**Process:**
1. Read the entire source material before beginning analysis — do not analyze paragraph by paragraph
2. Extract and list all key claims (the things the content is asserting as true or important)
3. Extract and list all action items (explicit asks, decisions, owners, deadlines)
4. Identify the primary conclusion or so-what — the single most important thing the audience needs to know
5. Map supporting evidence to each key claim — note which claims are well-supported vs. asserted without evidence
6. Classify each structural element: must-preserve / can-compress / can-drop for the target format
7. Flag any gaps: claims in the source that lack supporting evidence, or questions the source raises but does not answer

**Output:** A content structure map showing key claims, action items, primary conclusion, evidence mapping, and a must-preserve / can-compress / can-drop classification for target format transformation.

---

### Phase 3: Transform and Adapt
**Entropy Level:** E4 – Generative then E3 – Analytical
**Control Mode:** GENERATE then NARRATE

Apply the transformation. GENERATE executes the format change using the structural map from Phase 2. NARRATE then validates completeness: every must-preserve element from Phase 2 must appear in the output; no action items may be lost; the primary conclusion must be present.

The most important principle in this phase: apply the target format's structural conventions, not just its visual conventions. A bullet list is not just a paragraph with hyphens added — it is a format that assumes parallel structure, equivalent level of abstraction across items, and an implicit claim that each item stands alone. A slide deck is not a report with images — it is a format where each slide must make one claim that is defensible on its own. An executive summary is not a short report — it is a format that answers "what should I know and what should I do?" before answering "why."

**Process:**
1. Apply the target format transformation using the content structure map as input
2. For each target format, apply its specific structural conventions:
   - Executive summary: BLUF (bottom line up front), maximum 5 sentences, no methodology, one recommendation
   - Slide deck: one claim per slide, visual logic (not just text), explicit "so what" on final slide
   - Structured table: consistent column headers, parallel row structure, counts where applicable
   - Plain language: active voice, no jargon, one idea per sentence, analogy for any technical concept
   - 1-page brief: inverted pyramid (finding → evidence → background), hard page constraint enforced
   - Action item register: owner / action / deadline format, no discussion context
3. NARRATE validation: cross-check output against the must-preserve list; flag any missing elements
4. Check that the transformed output answers `{{OBJECTIVE}}` — not just that it is in the right format

**Output:** A transformed version of the source content in the target format, with a completeness check confirming all must-preserve elements are present.

---

### Phase 4: Validate Fit
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Check that the output is genuinely optimized for the target format — not just reformatted but properly restructured. There is a common failure mode in format transformation where the output looks like the target format but retains the logical structure of the source format. A bullet list that is actually a series of sentence fragments from a paragraph is not transformed; it is truncated. A slide that contains three paragraphs of text is not a slide; it is a report displayed on a slide.

Also check fit for audience: does the level of detail, vocabulary, and assumed context match `{{AUDIENCE}}`? An executive summary written at analyst level will not serve a board audience. A plain-language summary that still uses acronyms has not been fully transformed. A deck built for async reading will fail if presented live without speaker notes.

**Process:**
1. Apply format-specific fit criteria to the output:
   - Executive summary: Does it answer "so what?" in the first sentence? Is it under 5 sentences? Does it contain any methodology or background?
   - Slide deck: Does each slide have exactly one claim? Are there any slides with more than 40 words of body text? Is there an explicit "so what" conclusion slide?
   - Bullet list: Are all bullets parallel in structure? Are any bullets actually mini-paragraphs?
   - Table: Are all columns meaningful? Are rows internally consistent? Are counts or frequencies included where useful?
   - Plain language: Is the Flesch-Kincaid reading level appropriate? Are all technical terms either explained or removed?
2. Check audience fit: vocabulary, assumed knowledge, level of detail
3. Check length fit against `{{CONSTRAINTS}}` — if a word or slide limit was specified, enforce it
4. Produce a fit assessment: pass / needs revision for each criterion, with specific revision recommendations for any failures

**Output:** A fit validation report with pass/fail assessment against format criteria and audience fit, plus specific revision recommendations.

---

### Phase 5: Produce Formatted Output
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Deliver the final transformed output in clean, channel-ready format. If the target is a document, apply appropriate heading structure, white space, and visual hierarchy. If the target is a slide deck, deliver the slide structure with title, body claim, and speaker notes for each slide. If the target is a table, deliver it with headers, sorted by frequency or priority, with a summary row where appropriate.

Include a source-to-output mapping note if the requester might need to audit the transformation — particularly useful when the source is long and the output is highly compressed, and the requester needs to verify that key claims survived intact.

**Process:**
1. Apply final formatting to the validated output from Phase 4
2. For slide deck outputs: deliver each slide as Title / Body Claim / Speaker Notes structure
3. For table outputs: sort by most meaningful dimension (frequency, priority, or chronology), include totals or summary rows, apply consistent column widths
4. For document outputs: apply heading hierarchy, ensure consistent paragraph length, add metadata (date, audience, source document reference)
5. If source-to-output mapping was requested: produce a side-by-side mapping showing which source element each output element corresponds to
6. Add a brief transformation note: what was preserved, what was compressed, what was dropped, and why

**Output:** Final formatted output in the target format, channel-ready, with optional source-to-output mapping and transformation notes.

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Truncating instead of transforming | Format change requires structural reorganization, not just shortening |
| Losing action items in compression | Map all action items before transformation; they always survive intact |
| Adding formatting to the wrong format conventions | Each format has structural rules — apply them, not just the visual style |
| Over-formatting simple content | A 3-point update does not need a 10-slide deck; match format to complexity |
| Treating all summaries as equivalent | Executive summary answers "what do I do?"; TL;DR answers "what is this about?"; abstract answers "what did this study find?" — they are different |
| Retaining methodology in executive summaries | Decision-makers do not need to read how you analyzed; they need the conclusion |
| Writing slide bullets as truncated sentences | Each slide bullet is a standalone claim, not a sentence fragment |
| Ignoring the reading context of the target format | Async reading (email, doc) and live presentation (deck) require different structures even for the same content |

## 💡 Example Applications

| Use Case | Input | Output |
|----------|-------|--------|
| 20-page HR analytics report → board deck | Full engagement report with 15 findings, methodology section, data appendix | 5-slide structure: context (1 slide), 3 key findings (1 slide each), recommendation (1 slide); speaker notes with supporting data for Q&A; methodology relegated to leave-behind doc |
| 50 open-text survey comments → table | Raw Qualtrics export of free-text responses to "what would you change about your manager?" | Affinity-grouped table: 8 themes, frequency count per theme, representative verbatim quote per theme, sorted by frequency descending |
| Complex attrition analysis → 5-sentence exec summary | 2,000-word analysis with 8 charts, 3 regression models, and 12 findings | BLUF sentence on regrettable attrition rate; 2 sentences on drivers (compensation gap + manager quality); 1 sentence on highest-risk segment; 1 sentence on recommended action |
| Slide deck → async email narrative | 10-slide deck from all-hands presentation | Flowing email narrative with section headers corresponding to slide topics; transitions added; speaker-context folded in; call-to-action at end; slide logic restructured for linear reading |
| Technical HRIS migration doc → manager guide | 30-page IT implementation spec | 2-page plain-language guide: what changes for managers, what managers need to do before go-live, what to do if something breaks, who to contact; all technical terms removed or replaced with plain equivalents |

## 🖥️ Platform Notes

**CLI:** Ideal for piping source documents into the transformation workflow and outputting structured formats (markdown, CSV for tables, JSON for visualization specs). Useful in automated content pipelines where report outputs need to be transformed for multiple audiences simultaneously.

**Web:** Best for interactive refinement. Generate the transformation, then iterate on specific sections. The fit validation in Phase 4 is particularly useful as an interactive conversation where the requester can confirm which must-preserve elements matter most.

**IDE:** Useful for teams maintaining content templates. The transformation logic can be embedded in documentation workflows where the same analysis automatically produces multiple output variants (report, summary, deck) from a single source document.

**Any LLM:** Haiku is appropriate for most straightforward transformations (bullets to narrative, narrative to bullets, table formatting). For transformations requiring strong structural reasoning (executive summary compression with claim preservation, slide deck logic design), sonnet is recommended.

## 📋 Compliance

**AI Governance Alignment:** Output transformation is a low-risk operation from a governance perspective. The key compliance consideration is fidelity: the transformation must not materially alter the meaning of source claims. The completeness validation in Phase 3 and the fit validation in Phase 4 are the primary controls for transformation fidelity.

**PII Risk Level:** low — The output-router transforms content structure, not content substance. However, if `{{SOURCE_MATERIAL}}` contains PII, that PII is present in both source and output unless the transformation explicitly removes it. The skill does not perform PII scrubbing; use privacy-guardrail for that purpose before or after transformation as needed.

**Model Recommendation:** haiku — for most format transformations (bullet ↔ narrative, table formatting, plain language rewrites). Upgrade to sonnet when the transformation requires strong claim-extraction reasoning (executive summary compression, slide deck logic design, or any transformation where the source is analytically complex).

**Data Handling:** No data is retained between sessions. If source material contains sensitive or confidential content, ensure the output format is appropriate for the sensitivity level of the audience — a highly compressed summary may be appropriate for a broader audience than the full source document.
