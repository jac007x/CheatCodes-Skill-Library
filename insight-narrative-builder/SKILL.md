---
name: insight-narrative-builder
description: "Transforms raw analytical findings into compelling insight narratives with clear implications, logical flow, and executive-ready summaries."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - narrative
  - insights
  - analytics
  - storytelling
  - executive-comms
model_recommendation: sonnet
risk_level: low
---

# 🎯 Insight Narrative Builder

> From data to "so what" — the skill that turns findings into decisions.

## Core Philosophy

Most analytical work dies in the last mile. The data is right. The analysis is thorough. The findings are real. But the narrative is a bulleted list of observations with no through-line, no tension, and no clear ask. The decision-maker reads it, nods politely, and files it away. Nothing moves.

This skill exists to solve that problem. It treats narrative construction as a distinct technical discipline — not a writing task, but an architectural one. The sequence matters: evidence before implication, implication before recommendation, recommendation before executive summary. When findings are assembled in the wrong order, or at the wrong altitude for the audience, even strong analysis fails to land.

The governing principle is: **the insight is not the data point — it is what the data point means and what should change because of it.** Every sentence in the output must either carry evidence, draw an implication, or recommend an action. Anything else is noise.

---

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake Findings | E1 – Deterministic | DELEGATE | Structured data collection; no judgment required |
| 2. Validate Evidence | E3 – Analytical | NARRATE | Requires interpretation of evidence strength and directionality |
| 3. Build Narrative Structure | E3→E4 – Analytical→Creative | NARRATE→GENERATE | Choosing narrative type requires analysis; building arc requires generation |
| 4. Generate Storyline | E4 – Creative | GENERATE→NARRATE | Draft requires open generation; fact-tracing requires compression |
| 5. Compress to Exec Summary | E2 – Procedural | DELEGATE | Fixed format, clear rules, deterministic output |

### Mode Transition Diagram

```
┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐
│ DELEGATE  │→│ NARRATE   │→│ NARRATE       │→│ GENERATE      │→│ DELEGATE  │
│ Collect   │  │ Assess    │  │ → GENERATE    │  │ → NARRATE     │  │ Compress  │
│ findings  │  │ evidence  │  │ Choose arc +  │  │ Write draft + │  │ to exec   │
│ + context │  │ strength  │  │ structure it  │  │ trace claims  │  │ summary   │
│ E1        │  │ E3        │  │ E3→E4         │  │ E4→NARRATE    │  │ E2        │
└──────────┘  └──────────┘  └──────────────┘  └────────┬─────┘  └──────────┘
                                                         │
                                          ⚡ COMPRESSION CHECKPOINT
                                          Each claim must trace to a finding.
                                          Unsupported claims removed or flagged.
```

---

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{SOURCE_MATERIAL}}` | Raw findings, data points, analytical outputs, or summary statistics | text/list | Yes | — |
| `{{OBJECTIVE}}` | The decision or action this narrative is meant to inform | string | Yes | — |
| `{{AUDIENCE}}` | Who will read this — role, seniority, domain familiarity | string | Yes | — |
| `{{CHANNEL}}` | How it will be delivered — slide deck, memo, email, verbal brief | choice | Yes | memo |
| `{{CONFIDENCE_LEVEL}}` | Overall confidence in the underlying data: high / medium / low | choice | No | medium |
| `{{CONSTRAINTS}}` | Word count limits, sensitive topics to handle carefully, known audience biases | text | No | — |
| `{{KNOWN_FACTS}}` | Established context the audience already accepts — don't re-prove these | text | No | — |

---

## ⚙️ Phases

### Phase 1: INTAKE FINDINGS
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Parse and structure the incoming material. This phase does not interpret — it organizes. The goal is to convert raw inputs into a clean, flat list of discrete findings that subsequent phases can work with.

**Process:**
1. Read `{{SOURCE_MATERIAL}}` and extract every discrete finding as a single sentence.
2. Tag each finding with a type: `[METRIC]`, `[TREND]`, `[COMPARISON]`, `[ANOMALY]`, `[CORRELATION]`, or `[OBSERVATION]`.
3. Strip duplicate information — if two inputs say the same thing at different resolutions, keep the more specific one and note the overlap.
4. Capture `{{OBJECTIVE}}`, `{{AUDIENCE}}`, `{{CHANNEL}}`, `{{CONFIDENCE_LEVEL}}`, `{{CONSTRAINTS}}`, and `{{KNOWN_FACTS}}` as context fields for all downstream phases.
5. Count total findings. If fewer than 3, flag: "Sparse input — narrative may be thin. Consider supplementing with `{{KNOWN_FACTS}}` or asking for additional data."

**Output:** Flat numbered list of discrete findings with type tags. Example:
```
1. [METRIC] Employee engagement score declined from 74 to 68 over 12 months.
2. [TREND] Decline is steepest in the 12–24 months tenure band (−11 points).
3. [COMPARISON] Peer benchmark median held flat at 72 over the same period.
4. [ANOMALY] Operations team scores held steady; all other functions declined.
5. [CORRELATION] Managers with 3+ direct reports show no meaningful score difference from those with 8+.
```

---

### Phase 2: VALIDATE EVIDENCE
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Assess the quality of the evidence before building a narrative on top of it. A compelling story built on weak data is a liability, not an asset.

**Process:**
1. For each finding from Phase 1, assess:
   - **Evidence strength:** Is this a measured fact, an estimate, a self-reported data point, or an inference?
   - **Sample integrity:** Does the source represent the population being described, or is it a biased sample?
   - **Directionality:** Is the signal positive, negative, neutral, or ambiguous?
   - **Actionability:** Does this finding support a "so what"? Or is it context only?
   - **Conflict check:** Does this finding contradict another finding? If so, flag the tension — don't resolve it silently.

2. Assign each finding a weight tier:
   - **Tier 1 (Lead):** High evidence strength, clear directionality, supports a recommendation.
   - **Tier 2 (Support):** Moderate strength, adds context or reinforces a Tier 1 finding.
   - **Tier 3 (Context):** Low strength or low actionability; useful background but not a narrative driver.
   - **Tier 4 (Flag):** Weak evidence, potential bias, or contradicts another finding. Must be treated carefully or excluded.

3. For any Tier 4 finding, produce a caveat note: "This finding is [weak/potentially biased/contradictory] because [reason]. Recommend [exclude / present with explicit uncertainty / seek corroboration]."

**Output:** Annotated findings list with tier assignments and caveat notes. This is the input to Phase 3.

---

### Phase 3: BUILD NARRATIVE STRUCTURE
**Entropy Level:** E3→E4 – Analytical to Creative
**Control Mode:** NARRATE→GENERATE

Choose the narrative type best suited to the objective and audience, then arrange the validated findings into a logical arc.

**Process:**
1. **Choose narrative type** (NARRATE step — analytical selection based on `{{OBJECTIVE}}`):

   | Narrative Type | When to Use | Arc Pattern |
   |----------------|-------------|-------------|
   | **Problem-Solution** | When the findings reveal a specific problem with a known fix | Context → Problem evidence → Root cause → Recommendation |
   | **Trend Analysis** | When findings show a direction over time and the audience needs to act on trajectory | Baseline → Trend → Acceleration/deceleration → Implication → What to watch |
   | **Comparison** | When the value is in relative positioning (vs. benchmark, vs. prior period, vs. peers) | Reference point → Gap → Driver of gap → Stakes → Recommendation |
   | **Decision Support** | When the audience is weighing a specific choice and needs evidence to decide | Decision framing → Evidence for option A → Evidence for option B → Recommendation with confidence |

2. **Build the arc** (GENERATE step — creative arrangement):
   - Map Tier 1 findings to the "tension" or "problem" part of the arc. These are your lead evidence.
   - Map Tier 2 findings to the "support" section. These reinforce without duplicating.
   - Map Tier 3 findings to "context" — useful but not featured.
   - Tier 4 findings: either exclude or present as acknowledged limitations.
   - Identify the single "headline finding" — the one sentence that names the problem or insight at its most compelling.
   - Identify the single "recommendation" — what should change or be decided based on this evidence.

3. Draft the narrative skeleton: a 6–8 item outline with each section labeled (Context / Tension / Evidence / Implication / Recommendation / Caveats).

**Output:** Narrative type selection with rationale + structural skeleton with findings mapped to each section.

---

### Phase 4: GENERATE STORYLINE
**Entropy Level:** E4 – Creative
**Control Mode:** GENERATE→NARRATE

Write the full narrative. This is where data becomes language — and where the most common failures occur. The GENERATE step creates the draft; the NARRATE step verifies that every claim traces to evidence.

**Process:**

**GENERATE Step (write the draft):**
1. Write the full narrative following the arc from Phase 3.
2. Open with the headline finding — not "this report examines" or "we looked at data" — but the single most important thing the audience needs to know.
3. Build tension: what is the gap between current state and desired state? What is at stake if nothing changes?
4. Present evidence in plain language. For each data point, answer: "What does this number mean for someone who doesn't live in this data?" Translate.
5. Draw the implication explicitly: "This means..." or "The consequence of this pattern is..." Do not leave implications for the reader to infer — name them.
6. State the recommendation directly and specifically. Avoid "consider exploring" or "it may be worth investigating." Recommendations must specify: what, who, by when (if known).
7. Close with confidence calibration if `{{CONFIDENCE_LEVEL}}` is medium or low: acknowledge where the evidence is preliminary and what would sharpen the picture.

**NARRATE Step (trace and verify):**
1. Re-read every factual claim in the draft.
2. Map each claim back to a specific finding from Phase 2.
3. Flag any claim that cannot be traced to a finding: "Unsupported claim — either cut this or identify the source." Do not silently remove — show the flag so the user can decide.
4. Flag any place where the narrative implies a causal relationship that the data only shows as a correlation.
5. Confirm the recommendation is actionable given the evidence — if the evidence supports a diagnosis but not a specific fix, say so explicitly.

**Output:** Full narrative draft (typically 400–800 words for a standard memo) with claim-tracing annotations shown or cleared.

---

### Phase 5: COMPRESS TO EXEC SUMMARY
**Entropy Level:** E2 – Procedural
**Control Mode:** DELEGATE

Apply the fixed compression pattern. The executive summary is not a shorter version of the narrative — it is a standalone document with a specific structure. A reader who only reads the executive summary must understand the headline, the evidence basis, and the recommended action.

**Process:**
1. Extract the headline finding from Phase 4. This becomes sentence 1.
2. Select the 2–3 Tier 1 findings that most strongly support the headline. These become sentences 2–4 (one sentence each, plain language).
3. State the recommendation explicitly. This is sentence 5.
4. If `{{CONFIDENCE_LEVEL}}` is low or medium, add one sentence of confidence calibration: "These findings are based on [source/sample], and [limitation]."
5. Total length: 3–5 sentences. If it runs longer, cut — do not summarize by adding.

**Output format:**
```
EXECUTIVE SUMMARY

[Headline finding — one sentence, most important thing first.]

[Supporting finding 1.] [Supporting finding 2.] [Supporting finding 3 if needed.]

[Recommendation — specific, actionable, owner-ready.]

[Confidence note if applicable — one sentence.]
```

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Opening with "This analysis examines..." | Open with the headline finding. The reader already knows what the analysis examined. |
| Listing all findings in numerical order regardless of importance | Tier findings. Lead with Tier 1. Bury or exclude Tier 3–4. |
| Writing for the analyst who built the model | Write for an intelligent reader who has not seen this data before. Translate every metric to meaning. |
| Burying the recommendation in the final paragraph | State the recommendation early and explicitly. Return to it in the exec summary. Never hide it. |
| Omitting confidence caveats when data is weak | Flag weak evidence explicitly. A narrative that overstates confidence is worse than no narrative. |
| Treating correlation as causation without flagging | Every causal claim must be labeled as such. If the data shows correlation, say "this is associated with" not "this causes." |
| Using the same narrative type for every analysis | Problem-solution narratives don't work for trend data. Match the type to the objective. |
| Writing the executive summary as a paragraph-count reduction | The executive summary is a standalone document. Structure it as: headline → evidence → recommendation. |

---

## 💡 Example Applications

| Use Case | Input | Output |
|----------|-------|--------|
| Employee survey with 15 findings | Survey response data, engagement scores by demographic and function, prior year comparison, benchmark data | 3-part problem-solution narrative: engagement decline → concentrated in specific cohorts → retention risk recommendation. Exec summary in 4 sentences. Confidence note flagging self-reported nature of source data. |
| Attrition data by tenure and department | Headcount, voluntary attrition rates by tenure band (0–1yr, 1–2yr, 2–3yr, 3–5yr), departmental breakdown, exit interview themes | Trend analysis narrative: "We are losing people in years 2–3, concentrated in Engineering. Here is why. Here is what to do." Tier 1 finding: year-2 attrition is 3.2x the year-1 rate. Recommendation: structured stay conversations at 18-month mark. |
| Performance distribution for HR and business leader audiences | Bell curve of performance ratings, manager variance analysis, correlation with engagement scores | Two versions of the same narrative — one for HR (population health framing, calibration implications), one for business leaders (talent risk framing, investment case). Same data, different narrative type and vocabulary. |
| Competitive benchmarking across 6 dimensions | Internal scores vs. industry median vs. top-quartile benchmark on talent, technology, customer experience, cost, speed, and culture dimensions | Comparison narrative structured as: "Where we lead / Where we lag / Where we must act." Three-tier prioritization of gaps by business impact. Recommendation focused on top two gap-close priorities. |
| Market research findings from customer interviews | 12 interviews, 8 recurring themes, 3 divergent signals | Decision-support narrative for a product team choosing between two feature directions. Evidence mapped to each option. Recommendation with explicit confidence level (medium — small sample). |

---

## 🖥️ Platform Notes

**CLI:** Paste this SKILL.md as context. Provide `{{SOURCE_MATERIAL}}` and intake variables inline. Request phases sequentially or all at once.

**Web (Claude, ChatGPT, Gemini):** Attach or paste this skill file. Include intake variables in your opening message. Ask for the exec summary first if you only need the output; ask for the full run if you want to see the evidence audit.

**IDE (Cursor, Continue, Copilot Chat):** Reference in agent context. Useful as a post-analysis step after data extraction or modeling work — pipe model output directly into `{{SOURCE_MATERIAL}}`.

**Any LLM:** This skill is platform-agnostic. Any model that can follow multi-phase instructions can run it. Sonnet recommended for Phase 4 (GENERATE→NARRATE) due to claim-tracing and causal reasoning requirements.

---

## 📋 Compliance

**AI Governance Alignment:** All claims in the output are traceable to explicit source material provided by the user. The skill does not introduce external data or assumptions without flagging them. Confidence calibration is built into Phase 5 to prevent overstatement.

**PII Risk Level:** low — The skill operates on analytical findings and summary statistics, not on individual-level data. Users should not paste raw individual records into `{{SOURCE_MATERIAL}}`. Aggregate data only.

**Model Recommendation:** sonnet — Phase 4 (GENERATE→NARRATE) requires strong causal reasoning and claim-tracing capability. The compression checkpoint in Phase 4 and the evidence-mapping in Phase 2 benefit from Sonnet's analytical depth. Haiku is sufficient for Phase 5 (exec summary compression) if running phases separately.

**Data Handling:** Session-local only. No findings are stored by the skill. Users working with sensitive or proprietary analytical outputs should use this skill in a private, compliant LLM environment — not in public web interfaces.
