---
name: document-adaptor
description: "Adapts content from one or more source documents into the format, structure, and style of a target document. Automatically maps content to target slots, surfaces ambiguous mappings for user guidance, previews the adapted draft before final production."
version: 1.1.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - document-transformation
  - content-adaptation
  - format-conversion
  - human-in-the-loop
  - ANCT-designed
model_recommendation: sonnet
risk_level: low
---

# 📄 Document Adaptor

> Transform any source content into any target format — automatically where
> clear, collaboratively where ambiguous.

Most document transformation work fails the same way: either a blunt
find-and-replace that loses structure, or a manual line-by-line rewrite that
loses consistency. This skill does neither.

The Document Adaptor **deconstructs** the target document into named structural
slots, **catalogs** source content into mappable blocks, **automatically routes**
high-confidence matches, and **surfaces only the genuinely ambiguous cases** for
human judgment — before producing a previewed, reviewable draft.

**What this skill knows:**
- The same content block can serve multiple roles depending on the target format
- Not all source content belongs in the adapted output — some gets omitted
- Not all target slots can be filled from source — some require generation or flags
- A preview gate prevents wasted effort on a direction the user doesn't want

---

## 🔬 Core Philosophy

- **Structure before content** — decode the target format first; don't touch source content until you know where it could go
- **Confidence-gated automation** — route automatically when confidence is high; never guess silently on ambiguous placements
- **Minimal disruption** — preserve the source author's meaning; adapt the container, not the message
- **Human at the pivot points** — the two most important decisions (ambiguous placements + final approval) belong to the user
- **Preview is not optional** — the adapted document is always shown before it is produced in final form

---

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake | E1 – Deterministic | DELEGATE | Collecting known inputs; no interpretation needed |
| 2. Deconstruct | E3 – Analytical | NARRATE | Interpreting structure of both documents; requires judgment |
| 3. Auto-Map | E3→E4 – Analytical→Creative | NARRATE → GENERATE | Clear matches route automatically; uncertain matches need exploration |
| 4. Ambiguity Resolution | E3 – Analytical | NARRATE + Human Gate | Ambiguous slots surfaced; user decides; agent records and applies |
| 5. Preview | E2 – Procedural | DELEGATE | Assembling the draft from confirmed mappings; known process |
| 6. Final Production | E1 – Deterministic | DELEGATE | Applying user preview feedback; producing clean output |

**Circuit Breakers:**
- Phase 3: If > 40% of source blocks are unmatched → pause, surface a mapping summary to user before continuing
- Phase 4: If user rejects > 3 consecutive suggestions → offer to show the full target structure and let user assign manually
- Phase 5: Preview always shown before Phase 6 executes — Phase 6 cannot run without explicit user approval

---

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{SOURCE_DOCS}}` | Source document(s) to adapt content from. One or multiple. | file(s) / text | Yes | — |
| `{{TARGET_DOC}}` | The document whose format, structure, and style should be matched | file / text | Yes | — |
| `{{OBJECTIVE}}` | What is the adaptation for? (e.g., "submit to new stakeholder", "match company template") | string | Yes | — |
| `{{AUDIENCE}}` | Who will receive the final adapted document? | string | Yes | — |
| `{{ADAPTATION_SCOPE}}` | `full` (adapt all content) or `selective` (specify which sections) | choice | No | `full` |
| `{{STYLE_FIDELITY}}` | `strict` (match target style exactly) or `loose` (preserve source voice where appropriate) | choice | No | `strict` |
| `{{OMISSION_POLICY}}` | What to do with source content that has no target slot: `flag`, `omit`, or `append-as-supplement` | choice | No | `flag` |
| `{{GENERATION_POLICY}}` | What to do with target slots that have no source content: `flag-empty`, `generate-placeholder`, or `skip` | choice | No | `flag-empty` |
| `{{CHANNEL}}` | Output format: `markdown`, `plain-text`, `docx-structure`, `slide-outline` | choice | No | `markdown` |
| `{{CONSTRAINTS}}` | Any specific rules: length limits, sections to exclude, confidential content to redact | string | No | — |

---

## ⚙️ Phases

---

### Phase 1: INTAKE
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Collect all variables. Validate that both a source and a target document are
present. If multiple source documents are provided, label them `SOURCE_A`,
`SOURCE_B`, etc. for tracking through downstream phases.

**Process:**
1. Confirm `{{SOURCE_DOCS}}` — count, label, and acknowledge each
2. Confirm `{{TARGET_DOC}}` — note its format (length, visible structure, type)
3. Confirm `{{OBJECTIVE}}` and `{{AUDIENCE}}`
4. Apply defaults for any optional variables not provided
5. **Scan source documents for PII** (names, salaries, personnel decisions, contact info). If PII is present, invoke `privacy-guardrail` before proceeding to Phase 2.
6. Produce an **Intake Summary** before advancing — **this is a mandatory blocking output; do not proceed to Phase 2 without presenting it**:

```
INTAKE SUMMARY
─────────────────────────────────────────
Source documents:  [N] — [labels]
Target document:   [name/description]
Objective:         [{{OBJECTIVE}}]
Audience:          [{{AUDIENCE}}]
Adaptation scope:  [full / selective: ...]
Style fidelity:    [strict / loose]
Omission policy:   [flag / omit / append-as-supplement]
Generation policy: [flag-empty / generate-placeholder / skip]
Output channel:    [markdown / plain-text / etc.]
PII scan:          [clean / PII detected — privacy-guardrail invoked]
─────────────────────────────────────────
Proceeding to Phase 2: Deconstruct.
```

**Output:** Labeled source docs, confirmed target doc, resolved variable set

---

### Phase 2: DECONSTRUCT
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Deconstruct both the target document and the source document(s) independently.
The goal is not to match yet — only to understand what each contains.

**2A: Target Document Analysis**

Parse the target document to produce a **Slot Map** — every named structural
position that content can fill:

```
TARGET SLOT MAP
─────────────────────────────────────────
| Slot ID | Slot Name          | Type        | Notes                          |
|---------|-------------------|-------------|--------------------------------|
| T-01    | Executive Summary | text/prose  | Max ~3 paragraphs; leads doc   |
| T-02    | Background        | text/prose  | Context section                |
| T-03    | Data Table        | table       | Structured; column headers X   |
| T-04    | Recommendation    | bullets     | Action-oriented; owner fields  |
| T-05    | Appendix          | optional    | Supporting material            |
─────────────────────────────────────────
```

Also capture:
- **Style conventions** — tone (formal/informal), tense, person (first/third), heading format
- **Length norms** — approximate length per slot
- **Format rules** — any observed structural patterns (e.g., "every section ends with a summary sentence")
- **Implicit slots** — sections implied by the target structure that aren't explicitly labeled

**2B: Source Content Catalog**

For each source document, parse into a **Content Block Inventory**:

```
SOURCE CONTENT INVENTORY — SOURCE_A
─────────────────────────────────────────
| Block ID | Block Type  | Summary                        | Length  |
|----------|------------|--------------------------------|---------|
| A-01     | prose       | Overview of project goals      | 200w    |
| A-02     | table       | Q3 metrics by region           | 8 rows  |
| A-03     | bullets     | Key risks and mitigations      | 5 items |
| A-04     | prose       | Stakeholder background         | 150w    |
| A-05     | data/chart  | Trend line — monthly activity  | visual  |
─────────────────────────────────────────
```

**Output:** Target Slot Map + Source Content Inventory (one per source doc)

---

### Phase 3: AUTO-MAP
**Entropy Level:** E3→E4 – Analytical → Creative
**Control Mode:** NARRATE → GENERATE

Map source content blocks to target slots. Apply confidence scoring.
Route high-confidence matches automatically. Flag low-confidence for Phase 4.

**Confidence Classification:**

| Confidence | Criteria | Action |
|------------|---------|--------|
| **High (≥ 80%)** | Type match + semantic match + length-compatible | Map automatically |
| **Medium (50–79%)** | Type match but semantic ambiguity OR length mismatch | Flag for Phase 4 |
| **Low (< 50%)** | Type mismatch OR content fits multiple slots OR unclear relevance | Flag for Phase 4 |
| **No match** | Source block has no viable target slot | Apply `{{OMISSION_POLICY}}` |
| **Empty slot** | Target slot has no source candidate | Apply `{{GENERATION_POLICY}}` |

**NARRATE step:** Build the confident portion of the mapping table. **This table is a mandatory output — present it before advancing to Phase 4, even if all blocks auto-mapped at high confidence.** If zero blocks are ambiguous, still present the table to confirm the full mapping with the user:

```
AUTO-MAP RESULTS (High Confidence)
─────────────────────────────────────────
| Source Block | → | Target Slot | Confidence | Rationale                  |
|-------------|---|------------|------------|----------------------------|
| A-01         | → | T-01        | 92%        | Both are intro prose; topic aligns |
| A-02         | → | T-03        | 88%        | Table → table; column mapping confirmed |
| A-04         | → | T-02        | 85%        | Background content; length matches |
─────────────────────────────────────────
3 mappings auto-confirmed. Proceeding to Phase 4 for ambiguous cases.
```

**GENERATE step (if needed):** When a source block could plausibly go into
multiple target slots, generate the 2-3 most viable candidate placements with
rationale before flagging for user decision. This makes Phase 4 faster —
the user chooses from reasoned options, not a blank question.

**Circuit Breaker:** If > 40% of source blocks are unmatched at this stage,
pause and surface a **Mapping Gap Summary** to the user:

```
⚠️ MAPPING GAP ALERT
─────────────────────────────────────────
[N] of [total] source blocks could not be automatically matched.
This may indicate:
  • The source and target formats are fundamentally different in structure
  • The source contains domain content absent from the target's scope
  • The target has slots that require generated content, not adaptation

Recommended: Review the Target Slot Map and Source Inventory before proceeding.
Continue to ambiguity resolution? [Y / N / Show full maps]
─────────────────────────────────────────
```

**Output:** Confirmed auto-map table + flagged items list for Phase 4

---

### Phase 4: AMBIGUITY RESOLUTION
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE + **Human Gate**

Present each ambiguous mapping case to the user one at a time. For each:

1. Show the source block (full content or excerpt)
2. Show the candidate target slots (from the GENERATE step in Phase 3, or generate now)
3. State why it's ambiguous
4. Offer options including "omit", "appendix", or "let me place it manually"

**Ambiguity Resolution Card format — mandatory for every ambiguous case, no exceptions.** Never resolve an ambiguous mapping through conversational shorthand or inline text. Every case gets its own card:

```
AMBIGUITY CASE [N of M]
─────────────────────────────────────────
SOURCE BLOCK: [Block ID] — [Block Type]
Content preview: "[first 50 words of block...]"

TARGET CANDIDATES:
  Option A → T-04 (Recommendation): [rationale — fits if framed as action item]
  Option B → T-05 (Appendix): [rationale — supporting detail, not primary content]
  Option C → Omit: [rationale — may be out of scope for this target format]
  Option D → [I'll specify manually]

YOUR DECISION: ___
─────────────────────────────────────────
```

Record each decision and accumulate the complete mapping table.

**Circuit Breaker:** If user rejects ≥ 3 consecutive suggestions:

```
It seems the suggested placements aren't landing. Would you like to:
  1. See the full Target Slot Map and assign blocks manually
  2. Skip remaining ambiguous blocks and flag them for post-preview review
  3. Reconsider the adaptation scope ({{ADAPTATION_SCOPE}})
```

**Empty Slot Handling:**

For any target slots with no source candidate, apply `{{GENERATION_POLICY}}`:
- `flag-empty` → mark slot as `[EMPTY — no source content]` in preview
- `generate-placeholder` → draft a placeholder matching the target's style and length norm, clearly marked as generated
- `skip` → omit the slot from the adapted output

**Output:** Complete mapping table — every source block has a disposition (placed / omitted / appended), every target slot has a status (filled / empty / placeholder)

---

### Phase 5: PREVIEW
**Entropy Level:** E2 – Procedural
**Control Mode:** DELEGATE

Assemble the adapted document from the confirmed mapping table. Present it
as a **structured preview** — not yet the final document.

**Preview Format:**

Produce the full adapted document in `{{CHANNEL}}` format, with inline
annotations showing the provenance of each section:

```markdown
# [Target Document Title]

## Executive Summary  ← [T-01 ← A-01 | adapted: condensed from 200w to 120w]
[Adapted content here...]

## Background  ← [T-02 ← A-04 | adapted: tone adjusted to match target formal register]
[Adapted content here...]

## Data  ← [T-03 ← A-02 | adapted: column headers renamed to match target schema]
[Table here...]

## Recommendations  ← [T-04 ← A-03 | adapted: bullets reformatted; owner field added]
[Bullets here...]

## Appendix  ← [T-05 | EMPTY — no source content available]

---
ADAPTATION SUMMARY
─────────────────────────────────────────
Blocks placed:     [N]
Blocks omitted:    [N] (listed below)
Empty slots:       [N]
Generated placeholders: [N]
Style adjustments: [list of changes made to match target conventions]

OMITTED CONTENT:
  • [Block ID]: [reason omitted]

REVIEW THIS PREVIEW. To proceed to final production, confirm:
  → "Looks good — produce final"
  → "Changes needed: [specify]"
  → "Restart from Phase 4"
─────────────────────────────────────────
```

**Phase 6 is gated.** It does not run until the user explicitly approves
the preview or provides change instructions.

**Output:** Full annotated preview + adaptation summary + user gate

---

### Phase 6: FINAL PRODUCTION
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Apply any corrections from the preview review. Produce the clean final document
with no provenance annotations.

**Process:**
1. Apply user-specified changes from preview feedback
2. Remove all `← [provenance]` annotations
3. Apply style polish pass: ensure consistent tense, person, heading hierarchy, and length norms throughout
4. Produce final document in `{{CHANNEL}}` format
5. Append a **Production Log** — **mandatory, even for simple adaptations**. This is the audit trail that makes the skill's decisions traceable. Produce it as a separate block after the final document:

```
PRODUCTION LOG
─────────────────────────────────────────
Skill:             document-adaptor v1.1.0
Source docs:       [N] — [labels]
Target doc:        [name]
Objective:         [{{OBJECTIVE}}]
Audience:          [{{AUDIENCE}}]
PII handling:      [clean / redacted N items / privacy-guardrail invoked]

Mapping summary:
  Auto-mapped (high confidence):   [N] blocks
  User-resolved (ambiguous):       [N] blocks
  Omitted:                         [N] blocks
  Empty slots flagged:             [N] slots
  Placeholders generated:          [N] slots

Preview iterations:  [N]
Final changes from preview: [summary]
─────────────────────────────────────────
```

**Output:** Clean adapted document + production log

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Map content by position (first section → first slot) | Map by semantic role and content type |
| Silently drop source content that doesn't fit | Apply `{{OMISSION_POLICY}}`; always account for every block |
| Run Phase 6 without user preview approval | Preview gate is mandatory — never skip it |
| Ask the user about every mapping decision | Auto-route high-confidence (≥ 80%) mappings; only surface genuinely ambiguous cases |
| Adapt the meaning along with the format | Adapt the container; preserve the author's meaning |
| Treat all sources as equivalent | Track provenance per block; multi-source mappings must show which source each block came from |
| Ignore style conventions of the target | Capture tone, tense, person, heading style in Phase 2; apply throughout |
| Ignore length norms of the target | Content adapted to a shorter slot must be compressed; content in a longer slot may be expanded |
| Generate content without flagging it as generated | All generated/placeholder content must be visually distinct in the preview |
| Assume a slot must be filled | Empty slots are valid; surface them clearly rather than filling with irrelevant content |

---

## 💡 Example Applications

| Use Case | Source | Target | Key Behavior |
|----------|--------|--------|--------------|
| Reformat a research brief into an exec summary template | 8-page research report | 1-page exec summary template | Aggressive compression; multiple source sections → single summary slot; preview shows what was dropped |
| Adapt a team status update to a VP reporting template | 3 team status emails | Standardized VP status template | Merges 3 sources; auto-maps achievements/risks; flags missing "dependencies" field for user |
| Port content from an old proposal template to a new one | Proposal v1 (legacy format) | Proposal v2 (new company template) | High overlap; mostly auto-mapped; new required sections flagged as empty |
| Adapt a technical spec to a business requirements document | Engineering spec doc | Business requirements template | Low content overlap; many ambiguous mappings; Phase 4 is the core of the run |
| Consolidate multiple meeting notes into a single debrief format | 4 meeting notes files | Standard debrief template | Multi-source; deduplications surfaced as ambiguous; user confirms which source wins for each slot |
| Adapt a case study to a conference paper template | Internal case study | Academic conference paper template | Style fidelity shift (informal → formal); significant generation needed for abstract/methodology slots |

---

## 🔄 Multi-Source Behavior

When `{{SOURCE_DOCS}}` contains more than one document, additional rules apply:

**Conflict Resolution:** If two or more source blocks are candidates for the same
target slot at high confidence:

```
MULTI-SOURCE CONFLICT
─────────────────────────────────────────
Target slot T-02 (Background) has high-confidence candidates from two sources:

  SOURCE_A / A-04: [excerpt] (confidence: 87%)
  SOURCE_B / B-02: [excerpt] (confidence: 83%)

Options:
  1. Use SOURCE_A / A-04 (more recent)
  2. Use SOURCE_B / B-02 (more detailed)
  3. Merge both — combine into a single Background section
  4. I'll specify what to do
─────────────────────────────────────────
```

**Coverage Gap Detection:** After auto-mapping, report which source contributed
most and least content — useful signal that one source may be redundant or that
a required source is missing.

---

## 🖥️ Platform Notes

**CLI (Wibey/code-puppy):** Provide document paths as `{{SOURCE_DOCS}}` and `{{TARGET_DOC}}`. The skill reads file contents directly. Works best with markdown, plain text, or structured formats.

**Web/Chat LLM:** Paste document contents into the conversation. Label each clearly: "SOURCE_A:", "TARGET:", etc.

**IDE:** Useful for adapting code documentation, API specs, or README files to a different project's conventions.

**Any LLM:** The preview gate (Phase 5) requires you to explicitly say "produce final" — do not skip this confirmation.

---

## 📋 Compliance

**AI Governance Alignment:** Human gates at Phase 4 (ambiguity resolution) and Phase 5 (preview approval) ensure no adapted document is produced without user oversight of content placement decisions.

**PII Risk Level:** Depends entirely on source document content. The skill itself is format/structure focused — but if source documents contain PII (names, salaries, personnel decisions, health data, contact information), **run `privacy-guardrail` before Phase 2**. Do not catalog or map PII-bearing content without prior screening. PII discovered during Phase 2–6 must be redacted or placeholder-replaced before the production output is delivered — do not wait until Phase 6 to handle it.

**Model Recommendation:** Sonnet — Phase 2 (deconstruct) and Phase 3 (auto-map) benefit from strong analytical reasoning; Phase 4 requires nuanced judgment about semantic fit.

**Data Handling:** No content is generated without attribution to source. The production log provides a complete audit trail of every placement decision.

**Pairing recommendation:** Run `output-router` after this skill if the adapted document needs further format transformation (e.g., adapted markdown → slide outline).
