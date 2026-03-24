---
name: privacy-guardrail
description: "Scans analytical outputs and communications for privacy risks: small cell sizes, re-identification vectors, sensitive language, and inappropriate people data disclosure."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - privacy
  - compliance
  - people-analytics
  - guardrail
  - data-governance
model_recommendation: sonnet
risk_level: high
---

# 🎯 Privacy Guardrail

> Run this before you share any people analytics output. Every time. Without exception.

## Core Philosophy

Privacy risk in people analytics is not primarily about names. It is about inference. When you report that 33% of your 3-person finance team left in Q3, you have disclosed that one named person left — even though you never said their name. When you show a cross-tabulation of gender by department by tenure for a group with 6 women, you have created a re-identification risk for every individual in that intersection. The analyst who produced those numbers almost certainly did not intend to identify anyone. That is precisely the problem: privacy violations in people analytics are usually accidental, not malicious, and they are almost always preventable.

This skill exists to catch what human reviewers miss, not because humans are careless but because privacy risk is cognitively counterintuitive. We are wired to see the data and not the person behind it. We look at a percentage and see a statistic; we do not instinctively reverse-engineer it to the denominator that reveals an individual. We read a sentence about "high performers in technical roles who left in the first year" and see a pattern; we do not immediately ask "how many people are in this group in this team?" This skill applies the systematic, adversarial thinking that good privacy review requires — it asks how the content could be misused to identify an individual before that content reaches an audience that might do so.

The go/no-go recommendation at the end of this skill is not advisory. It is a gate. Content that receives a high-risk rating should not be shared with the stated audience through the stated channel until specific remediations are applied. The purpose of having a named `{{OWNER}}` for every review is to ensure there is a human who accepts accountability for the decision to share or not share. Privacy is not a technical problem to be solved by suppression rules alone; it is a governance problem that requires named human accountability at the distribution decision point.

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake Content | E1 – Deterministic | DELEGATE | Structured collection of content, audience, channel, and declared sensitivity |
| 2. Small Cell Risk Check | E3 – Analytical | NARRATE | Requires calculation and reasoning about statistical disclosure risk |
| 3. Re-identification Risk Check | E3 – Analytical | NARRATE | Requires adversarial reasoning about attribute combination vectors |
| 4. Language Risk Check | E3 – Analytical | NARRATE | Requires semantic analysis for identifying vs. descriptive language |
| 5. Sensitivity Scoring | E3 – Analytical | NARRATE | Requires holistic judgment to produce overall risk rating and go/no-go |

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{SOURCE_MATERIAL}}` | The full content to be reviewed: analysis, narrative, report, table, visualization spec, or communication | string | Yes | — |
| `{{AUDIENCE}}` | The intended recipient group for this content | string | Yes | — |
| `{{CHANNEL}}` | How the content will be distributed (email, dashboard, presentation, Slack, printed report) | string | Yes | — |
| `{{SENSITIVITY_LEVEL}}` | The sensitivity classification declared by the content owner (low / medium / high / restricted) | string | Yes | — |
| `{{CONSTRAINTS}}` | Applicable regulatory context (GDPR, CCPA, applicable collective agreements), internal policies, or specific known risks to check | string | No | General best practice applied |

## ⚙️ Phases

### Phase 1: Intake Content
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Collect all required inputs before beginning the review. Do not begin analysis until all required fields are confirmed. The audience and channel fields are as important as the content itself: the same content may be appropriate for an HR leadership team and inappropriate for all-manager distribution, and the risk profile changes entirely based on that distinction.

Specifically confirm the declared `{{SENSITIVITY_LEVEL}}` from the owner — this is what the content owner believes the sensitivity to be, which may differ from what the review finds. Flagging that mismatch is a key output of this skill: if the owner declares "low" and the review finds "high," that gap itself is important information.

**Process:**
1. Collect all required intake fields; do not accept "TBD" for audience or channel
2. Identify data types present in `{{SOURCE_MATERIAL}}`: aggregate statistics, percentages, cross-tabulations, verbatim quotes, narrative describing groups, individual-level data (even anonymized), or combinations
3. Confirm small cell threshold to apply: default is n<10; note if regulatory context (e.g., GDPR, applicable census standards) requires a higher threshold
4. Record the owner's declared `{{SENSITIVITY_LEVEL}}` for comparison to the review finding
5. Flag immediately if `{{SOURCE_MATERIAL}}` contains any of: named individuals, employee IDs, national ID numbers, salary data at individual level, medical information, or disciplinary history — these require review escalation, not just guardrail scan

**Output:** A confirmed intake record with data types identified, threshold confirmed, declared sensitivity recorded, and any immediate escalation flags raised.

---

### Phase 2: Small Cell Risk Check
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Scan every statistic, percentage, and group-level result in the content for small cell risk. Small cell risk occurs when the denominator of a calculation is small enough that the statistic effectively identifies an individual. The standard threshold is n<10, but context matters: in a 12-person engineering team, n<5 is effectively identifying.

The most dangerous small cell cases are percentages with small denominators. "33% of the finance team left" sounds like a percentage; it is actually a statement that one specific person left. "Two of three directors in APAC are women" discloses the gender identity of every individual in that population. Every percentage must be reverse-engineered to its denominator — the denominator is what carries the risk, not the percentage itself.

**Process:**
1. Identify every numeric result in the content: counts, percentages, rates, ratios, averages with standard deviations, and any "n=" labels
2. For every percentage, estimate or calculate the denominator. If the source document contains population sizes (e.g., "out of our 8-person analytics team"), apply them directly. If the denominator is not stated, flag it as an unknown small cell risk.
3. Apply the threshold test: any group with n<10 (or context-adjusted threshold) is a small cell risk
4. For each flagged statistic, determine the specific risk: does knowing this statistic allow inference about a specific individual's behavior, status, or characteristic?
5. Produce a remediation recommendation for each flagged item:
   - Suppress: remove the statistic entirely if no safe aggregation is possible
   - Aggregate: combine with adjacent groups to bring n above threshold (e.g., combine departments, combine tenure bands)
   - Restate: replace the statistic with directional language ("fewer than 10 employees") or a threshold indicator ("below reportable threshold")
   - Disclose threshold: explicitly note "n<10, suppressed for privacy" so the audience knows data exists but is protected
6. Flag any chart or visualization where small cells could be read from visual elements (e.g., a stacked bar chart where one segment is visually tiny)

**Output:** A small cell risk register listing every flagged statistic, the identified risk, the estimated denominator, and the recommended remediation (suppress / aggregate / restate / disclose threshold).

---

### Phase 3: Re-identification Risk Check
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Re-identification risk arises when the combination of multiple attributes — each innocuous on its own — allows a reader to identify a specific individual. This is the most underestimated privacy risk in people analytics because each individual data point passes a privacy check, while the combination does not. Job title + location + tenure band + gender is four innocuous fields; in combination, it often uniquely identifies a person in a small organization.

The adversarial frame for this phase is: imagine a reader who knows the people in the organization. What combination of attributes in this content would allow that reader to say "that can only be one person"? Apply this frame to every cross-tabulation, every filtered sub-group, and every descriptive passage that specifies multiple attributes of a group.

**Process:**
1. Identify all cross-tabulations in the content: any table or analysis that shows results broken down by more than one attribute simultaneously
2. For each cross-tabulation, estimate the minimum cell size at the most granular intersection. If two attributes are crossed and one is very specific (e.g., director-level by department), the intersection may be very small even if the totals are not
3. Apply the quasi-identifier test: identify attributes in the content that function as quasi-identifiers — attributes that do not name a person but narrow the population to a small number. Common quasi-identifiers in workforce data: job title, location (office or city), gender, ethnicity, disability status, age band, tenure band, salary band, department, direct manager name
4. Flag any combination of 3 or more quasi-identifiers applied to a sub-group with n<20. Flag any combination of 2 quasi-identifiers applied to a sub-group with n<10.
5. For verbatim quotes: apply the small team test — if the quote could be attributed to one of fewer than 10 people in a given team or group, it carries re-identification risk regardless of whether the speaker is named
6. Flag demographic intersections: combinations of gender + ethnicity, or gender + age band, or ethnicity + job level applied to small populations are high-risk even at moderate group sizes (n<30)
7. Produce a remediation recommendation for each flagged item:
   - Collapse attributes: merge categories to reduce granularity (e.g., director + VP → senior leadership)
   - Suppress intersection: remove the cross-tab and report marginal totals only
   - Aggregate quotes: replace individual verbatims with synthesized themes
   - Apply k-anonymity: ensure no cell in any cross-tabulation has fewer than k individuals (k=5 minimum, k=10 recommended)

**Output:** A re-identification risk register listing every flagged cross-tabulation, attribute combination, or verbatim quote with the identified vector and recommended remediation.

---

### Phase 4: Language Risk Check
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Scan the narrative and descriptive language in the content for phrases that imply individual-level identification even when no names are used. This phase catches the cases that data checks miss: a sentence describing a pattern that, given the organizational context, can only describe one or two people; language that implies an individual's performance or behavior when presenting group-level findings; or descriptions of "outliers" that effectively name a person by their uniqueness.

Common high-risk language patterns: "the one engineer who..." (implying unique identification), "the team that lost two managers in six months" (identifying a specific team by a unique event), "our highest-scoring respondent" (identifying an individual by rank in a small group), "the pattern was driven by a single individual" (identifying the outlier), and "one leader in particular" (implying a named individual without naming them).

**Process:**
1. Read the entire narrative section of `{{SOURCE_MATERIAL}}` for implicit identification language
2. Flag any language that implies unique individual identification: phrases that describe a unique role, event, or characteristic that could only apply to one person in context
3. Flag any language that attributes behavior, performance, or characteristics to implied individuals: "the manager who failed to act," "the high-performer who left," "the team that resisted the change"
4. Flag any use of rank-based identification in small populations: "the top performer," "the lowest-scoring team," "the outlier"
5. Flag language that uses identifying specificity in combination: role + event + time period applied to a small organization creates identification risk even in narrative form
6. For each flagged phrase, recommend a specific revision:
   - Generalize: replace specific descriptors with category-level language ("a manager in a mid-size team" rather than "the Director of Analytics in Singapore")
   - Pluralize: reframe individual-implying language as pattern-implying language ("in cases where individual contributors reported limited growth opportunities" rather than "one engineer specifically mentioned")
   - Aggregate: replace individual-level narrative with group-level summary
   - Remove: when a point can only be made by identifying an individual, assess whether the point is necessary for the document's purpose; if not, remove it

**Output:** A language risk register listing each flagged phrase, the identification vector, and a specific recommended revision.

---

### Phase 5: Sensitivity Scoring
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Synthesize the findings from Phases 2, 3, and 4 into a holistic sensitivity assessment and a go/no-go recommendation for sharing the content with the stated audience through the stated channel. The sensitivity score is a function of both the inherent risk of the content and the breadth and nature of the audience.

The go/no-go recommendation has three outcomes: Go (share as reviewed, no changes required), Go with Remediations (share after applying all flagged remediations), or No-Go (content cannot be safely shared with this audience through this channel; recommend restricted distribution or content redesign). A No-Go finding does not mean the content cannot be shared with anyone; it means it cannot be safely shared with `{{AUDIENCE}}` as currently structured.

**Process:**
1. Aggregate findings from all three check phases: small cell risk items, re-identification risk items, language risk items
2. Classify each finding by severity: Critical (high probability of identifying a specific individual), Moderate (possible identification under specific conditions), Low (theoretical risk, low probability in practice)
3. Calculate the overall risk level:
   - Low: zero Critical findings, fewer than 3 Moderate findings, audience is restricted (HR leadership or above)
   - Medium: zero Critical findings, 3+ Moderate findings, or any finding with a broad audience
   - High: any Critical finding, OR 5+ Moderate findings, OR broad audience distribution with any Moderate finding
4. Compare the overall risk level to the owner's declared `{{SENSITIVITY_LEVEL}}`. If the review finding exceeds the declared level, flag the mismatch as a governance issue requiring owner acknowledgment before any distribution.
5. Produce the go/no-go recommendation with explicit conditions:
   - Go: list the findings addressed (even if trivial), confirm no material risks remain
   - Go with Remediations: list each required remediation, specify that distribution must not occur until remediations are confirmed applied
   - No-Go: explain the blocking finding(s), recommend either restricted distribution (to a named smaller audience) or content redesign (what must change structurally for the content to be shareable)
6. Produce a findings summary table for the owner: all findings organized by phase, severity classification, remediation recommendation, and status

**Output:** A sensitivity assessment with overall risk level, comparison to declared level, go/no-go recommendation with explicit conditions, and a complete findings summary table for the owner.

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Running the guardrail after sharing the content | This skill is a pre-distribution gate; it has no value as a post-hoc audit |
| Only checking for named individuals | Re-identification does not require names; quasi-identifiers are the primary risk |
| Treating 33% as a percentage rather than a denominator | Always reverse-engineer percentages to their implied denominator; the denominator carries the risk |
| Treating "anonymized" as automatically safe | Anonymization is a process, not a guarantee; re-identification is often possible from anonymized data |
| Approving verbatim quotes without checking group size | A quote from a team of 6 is not anonymous regardless of how it is attributed |
| Applying only a single check (e.g., only small cells) | Privacy risk is multi-layered; all three check types are required for every review |
| Delegating go/no-go to the model alone | The go/no-go recommendation requires human owner acknowledgment; the model identifies risk, a human accepts accountability |
| Assuming broad distribution is fine if the data is aggregate | Aggregate data for broad audiences is a higher risk profile than individual data for restricted audiences; audience scope matters |

## 💡 Example Applications

| Use Case | Input | Output |
|----------|-------|--------|
| Engagement survey results by team | Cross-tabulated results by team, department, and manager level; 3 teams with n<10 | Small cell: 3 suppressed teams, directional language applied; Re-ID: 2 manager-level × department cross-tabs collapsed; Language: 1 "outlier team" reference revised; Overall: Medium risk, Go with Remediations |
| Attrition analysis with gender by department | 12-month attrition analysis showing gender breakdown within each department; some departments have <5 women | Small cell: 4 gender × department intersections suppressed; Re-ID: gender + level + department combination flagged for 2 departments; Overall: High risk, No-Go for all-manager distribution, Go with Remediations for HR leadership only |
| Manager effectiveness narrative | Qualitative summary of upward feedback themes by manager tier; 2 phrases implying individual manager identity | Language: 2 phrases revised to pattern-level language; Small cell: 1 statistic restated; Re-ID: no flags; Overall: Low risk after language revisions, Go with Remediations |
| Compensation equity analysis | Pay gap analysis by gender, ethnicity, and level; prepared for board distribution | Small cell: 3 ethnicity × level intersections suppressed; Re-ID: gender + ethnicity + level cross-tab flagged for senior leadership population; Overall: High risk as submitted; revised to exec summary with marginal totals only for board; detailed analysis retained for restricted HR access only |
| Exit interview theme analysis | Verbatim quote compilation with 15 selected quotes, sourced from teams of varying sizes | Language: 4 verbatims from teams <8 flagged; 4 quotes revised to synthesized paraphrase; 1 quote removed (uniquely identifying); Re-ID: 2 role-specific quotes collapsed to functional category; Overall: Medium, Go with Remediations |

## 🖥️ Platform Notes

**CLI:** Can be run as a pre-commit hook in analytics pipelines that output people data reports. Flag output files for review before they enter distribution channels. Useful as a final quality gate in automated report generation workflows.

**Web:** Best format for interactive review where the analyst can walk through findings and confirm remediations in real time. The phased structure maps well to a conversation where each phase produces a findings set the analyst can respond to before proceeding.

**IDE:** Useful in data pipeline code review: checking analytical scripts that produce outputs for privacy risk in the output specification. Can be embedded in code review checklists for people analytics code.

**Any LLM:** This skill requires strong reasoning ability for Phase 3 (re-identification vector identification) and Phase 4 (implicit language analysis). These are not pattern-matching tasks; they require adversarial reasoning about how a reader with organizational knowledge could exploit the content. Haiku is not appropriate. Sonnet minimum; Opus recommended for complex analyses with multiple cross-tabulations.

## 📋 Compliance

**AI Governance Alignment:** Directly supports compliance with GDPR Article 5 (data minimization, purpose limitation), CCPA privacy rights, and applicable workforce data protection frameworks. The k-anonymity standard applied in Phase 3 is consistent with NIST SP 800-188 (De-Identifying Government Datasets) and ISO 29101. The small cell suppression standard (n<10) is consistent with ONS (UK) and Statistics Canada disclosure control guidelines.

**PII Risk Level:** high — This skill processes content that may contain sensitive workforce data. The skill itself does not store or transmit any data. All review findings are produced in-session and must be actioned by the human owner. The model processes content only within the active session context.

**Model Recommendation:** sonnet — Re-identification vector reasoning and implicit language analysis require strong contextual reasoning. The model must reason adversarially about how content could identify individuals — a task that requires understanding organizational context, inference chains, and quasi-identifier combinations. Haiku produces superficial checks that miss the most important risks.

**Data Handling:** No personal data or analytical outputs are retained between sessions. Content submitted for review should be treated as highly sensitive; do not submit raw individual-level data to this skill — aggregate outputs only. If the content owner needs to review individual-level data for privacy assessment, that review should occur in a secured, access-controlled environment with appropriate data handling protocols in place. The go/no-go recommendation produced by this skill must be recorded by the owner as part of the distribution decision audit trail.
