---
name: metric-spec-builder
description: "Formalizes loosely defined metric concepts into precise, implementation-ready metric specifications with formulas, sources, owners, and thresholds."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - metrics
  - analytics
  - specification
  - data-governance
model_recommendation: sonnet
risk_level: low
---

# 🎯 Metric Spec Builder

> Turn "we want to track engagement" into a calculation-ready, owner-assigned, conflict-checked metric specification in one pass.

## Core Philosophy

Metric sprawl is one of the most underestimated data governance problems in people analytics. When three teams define "attrition" three different ways — one using headcount at start of period, one using average headcount, one using headcount at end — every dashboard comparison becomes misleading. Decisions built on inconsistent metrics are decisions built on noise. The cost of that inconsistency compounds invisibly over time.

This skill exists to force the discipline of formalization at the point of metric creation, not after the damage is done. It does not let a metric concept leave the conversation without a numerator, a denominator, a named data source, a refresh cadence, and a named human owner. Every one of those fields is load-bearing: omit the owner and the metric goes stale; omit the data source and the spec is aspirational; omit the denominator and the number is ambiguous.

The conflict-check phase is deliberately uncomfortable. It asks whether this new metric should exist at all, or whether an existing metric should be extended, renamed, or retired. Most organizations do not need more metrics. They need fewer, better-defined metrics with actual accountability attached to them. This skill enforces that discipline without requiring a data governance committee meeting.

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake Metric Concept | E1 – Deterministic | DELEGATE | Structured collection of fixed fields; no ambiguity tolerated |
| 2. Validate Definition | E3 – Analytical | NARRATE | Requires reasoning about precision and completeness gaps |
| 3. Formalize Specification | E2 – Structured | DELEGATE | Applies a fixed spec template to validated inputs |
| 4. Check for Conflicts | E3 – Analytical | NARRATE | Requires judgment about overlap, distinction, and deprecation |
| 5. Produce Spec Sheet | E1 – Deterministic | DELEGATE | Formats validated spec into final table output |

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{METRIC_CONCEPT}}` | The metric idea or name as stated by the requester | string | Yes | — |
| `{{OBJECTIVE}}` | The business question this metric is intended to answer | string | Yes | — |
| `{{AUDIENCE}}` | Who uses this metric and for what decisions | string | Yes | — |
| `{{SOURCE_MATERIAL}}` | Existing definitions, data sources, or system references if known | string | No | None provided |
| `{{CONSTRAINTS}}` | Known calculation limitations, data gaps, or exclusion rules | string | No | None identified |
| `{{OWNER}}` | Named individual or role accountable for this metric | string | Yes | — |

## ⚙️ Phases

### Phase 1: Intake Metric Concept
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Collect all required input fields before any analysis begins. Do not attempt to guess missing fields — prompt for each one explicitly. The quality of the final specification is entirely dependent on the quality of the intake. A vague objective produces a vague spec that will fail in implementation.

Specifically probe for: the business question being answered (not the metric name), the decision this metric informs, how frequently the audience needs it, and whether any existing definition is already in circulation. If the requester says "we track this in Workday already," that is source material — capture it.

**Process:**
1. Present the intake variable set and request all required fields
2. Prompt for `{{SOURCE_MATERIAL}}` explicitly — ask whether any current definition or dashboard already tracks something similar
3. Confirm `{{OWNER}}` is a named individual, not a team or function (teams cannot own metrics; individuals do)
4. Validate that `{{OBJECTIVE}}` is a genuine business question, not a restatement of the metric name (e.g., "what is our attrition?" is not an objective; "are we losing talent faster in Q4 than our competitors can replace?" is)
5. Flag any required fields that remain unresolved before proceeding to Phase 2

**Output:** A complete, structured intake record with all required fields populated and any gaps explicitly flagged for resolution.

---

### Phase 2: Validate Definition
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Before building the formal spec, validate that the metric concept is actually specifiable. Many metric requests fail at this stage because the underlying concept is too ambiguous, unmeasurable with available data, or does not actually answer the stated business question. Surfacing these problems now is far cheaper than discovering them after the metric is in production.

Apply three validation tests: (1) Precision — can this metric be calculated unambiguously by two different analysts working independently and produce the same number? (2) Completeness — are both the numerator and denominator fully defined, or is one implied? (3) Alignment — does the metric actually answer `{{OBJECTIVE}}`? A metric that is precise and complete but answers the wrong question is still a bad metric.

**Process:**
1. Test for precision: identify any term in `{{METRIC_CONCEPT}}` that requires a judgment call to calculate. Flag each one. Example: "active employee" requires a definition — does someone on unpaid leave count? Does a new hire on day 1 count?
2. Test for completeness: explicitly identify what the numerator and denominator will be. If either cannot be stated, the metric is incomplete.
3. Test for alignment: restate `{{OBJECTIVE}}` and ask whether the metric as conceived would answer it, partially answer it, or answer a different question. Be direct if the metric will not answer the stated question.
4. Produce a validation summary: precision gaps (list), completeness gaps (list), alignment verdict (aligned / partially aligned / misaligned + explanation)
5. If gaps are found, recommend resolutions before proceeding. Do not proceed to Phase 3 with unresolved definitional gaps.

**Output:** A validation summary with precision gaps, completeness gaps, alignment verdict, and recommended resolutions for any identified issues.

---

### Phase 3: Formalize Specification
**Entropy Level:** E2 – Structured
**Control Mode:** DELEGATE

Apply the standard metric specification template to the validated inputs from Phases 1 and 2. Every field in the template is required. If a field cannot be populated from the available information, mark it as "TBD — [reason]" and flag it as a blocking gap that prevents the metric from being production-ready.

The formula field must be expressed in both plain language and symbolic notation. The calculation example must use real-looking numbers, not placeholders — showing the calculation with 847 employees and 23 separations is more useful than showing it with N and n.

**Process:**
1. Populate all spec fields from validated intake data
2. Write the formula in plain language first, then translate to symbolic notation
3. Construct a calculation example with realistic sample numbers that walks through the formula step by step
4. Define the refresh cadence as a specific frequency (weekly, monthly, quarterly) tied to the decision cycle of `{{AUDIENCE}}` — not as "as needed"
5. Assign `{{OWNER}}` and define what the owner is responsible for: keeping the data source current, validating calculation logic, and approving any future definition changes
6. Set threshold and target fields: green/yellow/red bands if the metric is used for status reporting, or directional target if used for goal-setting
7. Document known limitations in plain language — what this metric does NOT tell you, and under what conditions it becomes unreliable

**Output:** A fully populated metric specification covering all fields: name, plain-language definition, formula (plain + symbolic), numerator, denominator, data source, refresh cadence, owner, calculation example, thresholds/targets, and known limitations.

---

### Phase 4: Check for Conflicts
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Search the available context (source material provided, common metric library conventions, and stated existing definitions) for metrics that overlap with the new specification. Propose a resolution for each overlap: consolidate (adopt the new spec and retire the old), distinguish (define the difference explicitly and keep both with different names), or deprecate (retire the old definition and migrate users to the new one).

This phase will sometimes produce uncomfortable findings — including the recommendation that the new metric not be created because an existing metric already serves the need. That is a valid and valuable outcome. Metric sprawl grows through well-intentioned addition; it shrinks through disciplined consolidation.

**Process:**
1. List any similar metric names mentioned in `{{SOURCE_MATERIAL}}` or known to exist in the stated data environment
2. For each similar metric: compare the definition, formula, data source, and audience
3. Classify the overlap type: identical (same metric, different names), partial (same concept, different calculation), or adjacent (related but genuinely distinct)
4. Recommend resolution: consolidate, distinguish, or deprecate — with explicit rationale for each
5. If consolidation is recommended, propose a migration note: who needs to be notified, what dashboards need to be updated, and what the transition period should be

**Output:** A conflict analysis table listing each similar metric, the overlap classification, and the recommended resolution with rationale.

---

### Phase 5: Produce Spec Sheet
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Assemble the final metric specification into a clean, structured output ready for a data dictionary, internal wiki, or dashboard documentation. The spec sheet must be self-contained — a reader with no prior context should be able to understand, calculate, and validate the metric from the spec sheet alone.

Include the conflict resolution recommendations as a separate section if any conflicts were found in Phase 4. Include the validation gaps as a "Pre-Production Requirements" section if any remain unresolved.

**Process:**
1. Compile all Phase 3 spec fields into the standard table format
2. Add the calculation example as a standalone worked example block
3. Append conflict resolution notes if applicable
4. Append pre-production requirements if any TBD fields remain
5. Add a metadata footer: date created, created by, spec version, next review date

**Output:** A complete, formatted metric specification document ready for data dictionary entry or wiki publication, including all spec fields, worked example, conflict notes, and metadata.

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Accepting "attrition" as the metric name without defining voluntary vs. total vs. regrettable | Always decompose colloquial names into precise variants; name each separately |
| Defining the metric without specifying the data source | Every metric must name its source system, field, and any required filters |
| Creating a new metric without checking whether one already exists | Run the conflict check before finalizing; consolidate when possible |
| Omitting the calculation example from the spec | Every spec must include a worked example with realistic sample numbers |
| Assigning ownership to a team or function rather than a named individual | Metric ownership requires a named person; teams cannot be held accountable |
| Writing the formula only in symbolic notation | Always provide plain-language formula first; not all stakeholders read notation |
| Setting thresholds without tying them to a decision or action | Every threshold must be linked to a specific response: what happens when it turns red? |
| Marking a metric as "live" before the data source is validated | A spec with an unvalidated source is aspirational, not production-ready |

## 💡 Example Applications

| Use Case | Input | Output |
|----------|-------|--------|
| "We want to track engagement" | Metric concept: engagement; objective: understand whether employees feel connected to their work and team; audience: HR BP, quarterly; owner: CHRO | Formal eNPS spec: survey-based, formula = % promoters minus % detractors, annual Glint survey source, quarterly refresh, CHRO owner, target >30, flag if below 10 |
| "Monitor attrition" | Metric concept: attrition; objective: identify whether we are losing people faster than we can hire; existing definitions: 2 variants found in different dashboards | Three distinct specs produced (voluntary, total, regrettable); Phase 4 flags 2 conflicting existing definitions; consolidation recommended with migration note |
| "Measure manager effectiveness" | Metric concept: manager effectiveness; objective: identify which managers to prioritize for development investment | Composite metric spec with 3 sub-components (team engagement score, 90-day attrition on team, upward feedback score), weightings (40/30/30), individual data sources for each component, quarterly composite calculation |
| "Time-to-fill" | Metric concept: time-to-fill; objective: understand recruiting velocity by role level; audience: TA team, weekly | Spec defines start date as job approval date (not post date), end date as offer acceptance date (not start date), excludes internally transferred roles, weekly ATS refresh, TA Director owner, target <45 days for IC roles, <60 for manager+ |
| "Span of control" | Metric concept: span of control; objective: identify over-burdened managers for workforce planning | Spec defines as direct reports per manager (excludes dotted-line), calculated from HRIS as-of last business day of month, excludes managers in organizational transitions, monthly refresh, HRBP owner, flags managers >12 direct reports |

## 🖥️ Platform Notes

**CLI:** Pipe metric concept and objective as arguments; output spec to markdown or CSV for data dictionary import. Ideal for batch processing multiple metric concepts in sequence.

**Web:** Use the intake variable prompts as a structured form. The Phase 4 conflict check works best when the user can paste in existing metric definitions from their wiki or dashboard system.

**IDE:** Useful when building metric configuration files or dbt metric definitions. The formalized spec maps directly to dbt metric syntax fields (name, label, description, model, measure, dimensions).

**Any LLM:** The phase structure works with any capable model. Phase 2 validation and Phase 4 conflict checking require genuine reasoning ability — do not reduce to haiku for those phases. Sonnet or above recommended for accurate definitional gap detection.

## 📋 Compliance

**AI Governance Alignment:** Supports data governance frameworks (DAMA-DMBOK, DCAM) by enforcing metric standardization, owner assignment, and conflict resolution. Output spec format is compatible with most data catalog tools (Collibra, Alation, DataHub).

**PII Risk Level:** low — Metric specifications are definitional documents, not data extracts. No individual-level data is processed. If `{{SOURCE_MATERIAL}}` contains sample data with PII, prompt the requester to anonymize before providing.

**Model Recommendation:** sonnet — Phase 2 (validation) and Phase 4 (conflict detection) require analytical reasoning to identify subtle definitional gaps and overlap patterns. Haiku is insufficient for reliable precision and completeness testing.

**Data Handling:** No data is stored between sessions. Metric specifications produced should be saved by the user to their data dictionary or documentation system. The skill does not connect to live data sources; source validation must be performed by the metric owner.
