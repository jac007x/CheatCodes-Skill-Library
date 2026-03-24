---
name: request-scope-builder
description: "Transforms vague analytical or informational requests into clearly scoped, answerable briefs with defined success criteria."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - scoping
  - clarity
  - requirements
  - analytics
model_recommendation: sonnet
risk_level: low
---

# 🎯 Request Scope Builder

> Turn any vague ask into a precisely defined, answerable brief before a single byte of analysis runs.

## Core Philosophy

Most analytical failures happen before the analysis begins. Someone asks "what's happening with attrition?" and an analyst immediately opens a spreadsheet. Two hours later they surface a chart that answers a question nobody asked, built on assumptions that were never shared, and missing the data source the decision-maker actually trusts. The ask was never validated. The scope was never agreed upon. The answer lands wrong.

This skill exists to break that pattern. Before any analysis runs, before any data is pulled, before any model is called — the request must earn the right to proceed by surviving a scoping process. That process surfaces what the request is really asking, what data would answer it, what the decision-maker actually needs to make a decision, and whether the ask is even answerable with available resources.

The ANCT architecture maps directly to the reality of scoping work: intake is deterministic (just collect what's there), answerability assessment is analytical (requires interpretation and judgment about what's feasible), scope definition is analytical (requires synthesis across multiple constraints), and brief assembly is procedural (assemble what's been built into a structured output). Getting the modes right means the skill doesn't over-generate where it should execute, and doesn't under-think where it needs to reason.

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake Raw Request | E1 – Deterministic | DELEGATE | Structured extraction of stated facts; no interpretation needed yet |
| 2. Validate Answerability | E3 – Analytical | NARRATE | Requires judgment: is this feasible, what's missing, what's assumed? |
| 3. Define Scope | E3 – Analytical | NARRATE | Synthesis across request, data, constraints, and audience needs |
| 4. Produce Scope Brief | E2 – Procedural | DELEGATE | Assembly of resolved elements into a fixed-format output document |

---

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{REQUEST}}` | The raw, unedited ask exactly as stated by the requester | string | Yes | — |
| `{{OBJECTIVE}}` | The decision this analysis is meant to inform | string | Yes | — |
| `{{AUDIENCE}}` | Who receives the output and at what level of detail | string | Yes | — |
| `{{DEADLINE}}` | When the output is needed; drives feasibility constraints | string | No | — |
| `{{CONSTRAINTS}}` | Known limitations: budget, bandwidth, tools, data access | string | No | — |
| `{{SOURCE_MATERIAL}}` | Data sources, systems, or files that are available | string | No | — |
| `{{CONFIDENCE_LEVEL}}` | Required confidence threshold: directional, moderate, high | string | No | directional |

---

## ⚙️ Phases

### Phase 1: INTAKE RAW REQUEST
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Collect and parse every element of the raw request without interpretation. This phase is purely structural: extract what's been stated, note what's absent, and prepare the inputs for Phase 2's judgment.

**Process:**
1. Capture `{{REQUEST}}` verbatim. Do not rephrase, clean up, or interpret at this stage.
2. Extract the stated objective (`{{OBJECTIVE}}`). If the requester didn't distinguish between the ask and the objective, flag both as the same and note for Phase 2.
3. Record audience (`{{AUDIENCE}}`), deadline (`{{DEADLINE}}`), and constraints (`{{CONSTRAINTS}}`).
4. Inventory available source material from `{{SOURCE_MATERIAL}}`. If no source material was named, record as "unstated — to be addressed in Phase 2."
5. Note the confidence level requirement (`{{CONFIDENCE_LEVEL}}`). Default to "directional" if not specified.
6. Produce a clean intake summary. No opinions. No edits. Just the structure.

**Output:**
```
INTAKE SUMMARY
Raw request: [verbatim]
Stated objective: [verbatim or "same as request"]
Audience: [who, role, level]
Deadline: [when or "not specified"]
Constraints: [list or "none stated"]
Available sources: [list or "unstated"]
Confidence required: [directional / moderate / high]
```

---

### Phase 2: VALIDATE ANSWERABILITY
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

This is the hardest phase and where most scoping fails. A request can fail answerability in several ways: the question is too vague to operationalize, the data required doesn't exist or isn't accessible, the timeframe makes precision impossible, or the decision-maker's actual need differs from what they asked for. This phase surfaces all of it before work begins.

**Process:**
1. **Operationalize the question.** Can you write the exact metric, segment, or comparison that would answer this request? If not, state what's missing. Vague verbs ("understand," "assess," "look at") must be converted to specific measurable outputs or flagged as unresolvable.
2. **Assess data feasibility.** Does `{{SOURCE_MATERIAL}}` contain what would be needed to answer the scoped question? Identify: (a) what data would be needed, (b) what's confirmed available, (c) what's assumed available but unconfirmed, (d) what's clearly missing.
3. **Surface unstated assumptions.** Every request carries invisible assumptions: time period, population, exclusions, definitions of key terms, comparison baseline. List every assumption embedded in the request.
4. **Check for conflated objectives.** Does the stated `{{REQUEST}}` actually serve the stated `{{OBJECTIVE}}`? If the decision to be made requires X but the request asks for Y, flag the mismatch explicitly.
5. **Assess timeline feasibility.** Given `{{DEADLINE}}` and `{{CONSTRAINTS}}`, is it possible to answer the scoped question with adequate confidence? If not, state what level of confidence is achievable and what would be required to reach the stated threshold.
6. **Produce an answerability verdict**: Answerable as-stated / Answerable with clarification / Not answerable without additional resources / Reframe required.

**Output:**
```
ANSWERABILITY ASSESSMENT
Verdict: [Answerable as-stated / Answerable with clarification / Not answerable / Reframe required]

Operationalized question: [the precise measurable question this reduces to]

Data status:
  - Confirmed available: [list]
  - Assumed available (unconfirmed): [list]
  - Missing: [list]

Unstated assumptions:
  - [assumption 1]
  - [assumption 2]
  - [assumption 3+]

Objective alignment:
  - The request [does / does not] directly serve the stated objective.
  - [If mismatch]: The decision requires [X]; the request asks for [Y]. Recommend [reframe].

Timeline feasibility:
  - [Achievable / Achievable with scope reduction / Not achievable]
  - At [confidence level], analysis requires [estimate].

Clarifications required before scoping:
  - [Question 1]
  - [Question 2]
```

---

### Phase 3: DEFINE SCOPE
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

With answerability resolved, this phase converts the validated request into a formal scope document. Every element must be specific, bounded, and agreed-upon before handoff. This is the contract between the requester and the analyst.

**Process:**
1. **Write the exact question.** One sentence. Answerable yes/no or with a specific metric. No vague verbs. If multiple questions exist, list each one. Maximum 3 questions per scope brief — if more exist, scope is too broad.
2. **Define data requirements.** List every data source, field, and time period required. Separate confirmed sources from assumed sources. Flag gaps explicitly.
3. **Define in-scope items.** What populations, time periods, metrics, segments, and comparisons are included.
4. **Define out-of-scope items.** Equally important as in-scope. What is explicitly excluded and why. This prevents scope creep in execution.
5. **State all assumptions.** Every assumption carried forward from Phase 2. No assumption travels silently.
6. **Define success criteria.** What does a complete, acceptable answer look like? At what level of confidence? In what format? By when? Who signs off?
7. **Identify risk factors.** What could cause this scope to fail? Missing data, shifting deadlines, stakeholder disagreement on definitions.

**Output:**
```
SCOPE DEFINITION
Exact question(s):
  1. [Precise, answerable question]
  2. [Additional question if applicable — max 3 total]

In scope:
  - Population: [who/what is included]
  - Time period: [start to end]
  - Metrics: [specific metrics/fields]
  - Segments/cuts: [breakdowns required]
  - Comparison baseline: [what is this measured against]

Out of scope:
  - [Item explicitly excluded + reason]
  - [Item explicitly excluded + reason]

Data requirements:
  - [Source] — [fields needed] — [confirmed / assumed / missing]

Assumptions:
  - [Assumption 1] — [basis for this assumption]
  - [Assumption 2]

Success criteria:
  - Output format: [table / chart / memo / dashboard / narrative]
  - Confidence level: [directional / moderate / high]
  - Deadline: [date/time]
  - Sign-off: [who approves the output]

Risk factors:
  - [Risk 1] — [mitigation]
  - [Risk 2] — [mitigation]
```

---

### Phase 4: PRODUCE SCOPE BRIEF
**Entropy Level:** E2 – Procedural
**Control Mode:** DELEGATE

Assemble the resolved outputs of Phases 1-3 into a clean, standalone scope brief document. This document is the handoff artifact — suitable for a stakeholder review, an analyst intake, or a data pull request. Format is fixed. No improvisation.

**Process:**
1. Combine the intake summary (Phase 1), answerability assessment (Phase 2), and scope definition (Phase 3) into the standardized brief format below.
2. Add a header block: project name, requester, date, and status (Draft / Pending Review / Approved).
3. Flag any unresolved items from Phase 2 in a clearly marked "Open Issues" section. The brief is not approved until all open issues are resolved.
4. Add a signature block for stakeholder sign-off if `{{AUDIENCE}}` includes an approver.
5. Output as a clean Markdown document suitable for direct sharing.

**Output:**

```markdown
# Scope Brief: [Project/Request Name]

**Requester:** [from {{AUDIENCE}} or inferred]
**Date:** [today]
**Status:** Draft — Pending Review

---

## The Ask
[{{REQUEST}} verbatim]

## The Objective
[What decision this informs]

## The Exact Question(s)
1. [Precise question from Phase 3]
2. [Additional if applicable]

## In Scope
- Population: [defined]
- Time period: [defined]
- Metrics: [defined]
- Segments: [defined]
- Baseline: [defined]

## Out of Scope
- [Item + reason]

## Data Requirements
| Source | Fields Needed | Status |
|--------|--------------|--------|
| [source] | [fields] | Confirmed / Assumed / Missing |

## Assumptions
- [Assumption + basis]

## Success Criteria
- Format: [output format]
- Confidence: [level]
- Deadline: [date]
- Sign-off: [who]

## Open Issues
- [ ] [Unresolved item from Phase 2, if any]

---
**Approved by:** _______________  **Date:** _______________
```

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Accepting "what's happening with X?" and running analysis immediately | Run Phase 2 first — operationalize the question before opening any data |
| Assuming data is available because the requester named it | Confirm source availability explicitly; mark assumed sources as unconfirmed |
| Scoping in everything remotely related to the topic | Write explicit out-of-scope items; every scope brief must have exclusions |
| Producing an output without defined success criteria | Every scope must define what "done" looks like before work starts |
| Carrying assumptions silently through the analysis | All assumptions surface in the scope brief; none travel without acknowledgment |
| Writing one combined "question" that is actually three questions | Separate multi-part asks into discrete, independently answerable questions |
| Treating a deadline as fixed when confidence requirements are impossible to meet | Flag timeline feasibility in Phase 2; negotiate scope reduction before starting |

---

## 💡 Example Applications

| Use Case | Input | Output |
|----------|-------|--------|
| Attrition inquiry | "What's happening with attrition?" — no data sources named, no time period | Scoped brief: Q3 voluntary attrition rate by department vs. prior year, excludes involuntary separations, uses HRIS exit data, 3-day turnaround, directional confidence |
| Manager effectiveness | "How are our managers doing?" — goal is upcoming calibration prep | Scoped brief: Manager effectiveness index from last engagement cycle, top/bottom quartile distribution, flagged managers below threshold, excludes managers with fewer than 5 direct reports |
| Feedback summarization | "Summarize the feedback" — 847 open-text survey responses available | Scoped brief: Top 5 themes from Q3 engagement open-text, sentiment distribution, excludes verbatim quotes in shared output due to sensitivity, theme extraction only |
| Hiring health check | "Is our hiring on track?" — decision is Q3 workforce plan review | Scoped brief: Time-to-fill and offer acceptance rate vs. approved headcount plan, by role family and level band, current quarter only, excludes backfills already in-flight |
| Compensation equity ask | "Are we paying people fairly?" — too broad, no segment defined | Phase 2 returns: reframe required — scope to specific job family or level band; full equity analysis requires compensation band data not yet confirmed available |

---

## 🖥️ Platform Notes

**CLI:** Invoke with `/skill request-scope-builder`. Provide intake variables inline or via a structured prompt block. Output scope brief as a Markdown file ready for sharing.

**Web:** Paste the SKILL.md as system context. Provide `{{REQUEST}}` and supporting variables in the first message. The skill will work through phases sequentially and produce the scope brief.

**IDE:** Reference in agent configuration for analytics projects. Especially effective when paired with org-data-pipeline or metric-spec-builder as a pre-flight scoping gate.

**Any LLM:** Copy the SKILL.md contents into context. Provide the raw request and any available intake variables. The structured phase outputs work across all models that support instruction-following.

---

## 📋 Compliance

**AI Governance Alignment:** Supports responsible analytics by requiring explicit assumption documentation, data provenance acknowledgment, and stakeholder sign-off before analysis begins. Reduces the risk of analysis running on unvalidated assumptions that produce misleading outputs.

**PII Risk Level:** low — the skill processes request descriptions and data source names, not the underlying data itself. If `{{REQUEST}}` or `{{SOURCE_MATERIAL}}` contains employee names or PII, those should be anonymized before passing to a public LLM interface.

**Model Recommendation:** sonnet — Phase 2 (answerability) and Phase 3 (scope definition) require strong reasoning to identify conflicts between the stated request and the actual decision objective. Haiku is sufficient for Phase 1 and Phase 4 in isolation but underpowered for the full skill.

**Data Handling:** Processes request text, objective descriptions, and data source metadata. No underlying data is consumed by this skill. Output is a structured Markdown document. No data is stored or transmitted by the skill itself beyond the active session context.
