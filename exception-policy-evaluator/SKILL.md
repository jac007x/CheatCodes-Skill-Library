---
name: exception-policy-evaluator
description: "Evaluates exception requests against documented policy, generates both sides of the argument before recommending APPROVE / DENY / ESCALATE, and drafts a professional response — preventing each request from becoming a one-off judgment call."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - policy
  - exceptions
  - promotions
  - decision-support
  - ANCT-designed
  - workflow-automation
---

# Exception Policy Evaluator

A decision-support skill for recurring exception requests. Instead of treating each request as a fresh judgment call, this skill applies a consistent, documented process: classify the reason, check the policy, generate both sides of the argument, produce a recommendation, and draft the response.

**Design target:** Every exception request gets the same quality of analysis — regardless of who's asking, how persistent they are, or how late in the cycle it arrives.

**Origin context:** Built for promotion cycle exception management at Walmart Global Tech. Representative cases include post-deadline nomination requests (e.g., a manager who did not nominate by the deadline) and tool access exceptions (e.g., a manager on leave who could not access the system). The pattern generalizes to any recurring exception workflow with documented policy.

---

## ANCT Architecture

This skill was designed using **Adaptive Narrative Control Theory (ANCT)**.
Exception evaluation requires fundamentally different control modes at each phase. Intake is deterministic. Classification requires interpretation. The "generate both sides" phase is explicitly creative — it must produce the strongest possible argument for each outcome before any recommendation is made. The approval gate halts before any response is sent when precedent risk is flagged.

```
Phase:     1        2        3        4         5         5.5       6
Entropy:   E1       E3       E3       E4        E2-E3     E2        E1-E2
Mode:      DELEGATE NARRATE  NARRATE  GEN→NAR   NARRATE   DELEGATE  DELEGATE

           intake   classify policy   generate  recommend ★APPROVE  draft
           request  reason   check    both       with      (gate)    response
                             +        sides      rationale
                             precedent
```

> **The Approval Gate (Phase 5.5)** is the primary safety mechanism.
> Any DENY recommendation where the reason could set a precedent **always halts here**
> and surfaces the decision for human review before the response is sent.

### Why This Entropy Map

| Phase | Why This Mode |
|-------|---------------|
| 1. Intake | E1 — structured data capture; no interpretation needed |
| 2. Classify reason | E3 — requires judgment: the stated reason is not always the operative reason |
| 3. Policy check | E3 — policy lookup is deterministic; precedent comparison requires interpretation |
| 4. Generate both sides | E4 — explicitly creative: produce the strongest possible case for each outcome before deciding |
| 5. Recommend | E2-E3 — analytical: apply policy + precedent to select outcome; one-sentence rationale required |
| 5.5 Approve | E2 — structured human gate; fires when DENY + precedent risk detected |
| 6. Draft response | E1-E2 — target is known; write the response to match the recommendation |

---

## Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{EXCEPTION_TYPE}}` | Category of exception being requested | choice: `nomination` / `access` / `process` | Yes | — |
| `{{REQUESTER}}` | Name and role of the person submitting the exception request | string | Yes | — |
| `{{ASSOCIATE}}` | Name of the associate the exception is on behalf of (may be same as requester) | string | Yes | — |
| `{{REASON}}` | The requester's stated reason for the exception | string | Yes | — |
| `{{POLICY_DOCS}}` | List of applicable policy documents or sections to check against | list of strings | Yes | — |
| `{{PRIOR_DECISIONS}}` | Path or reference to the precedent compendium for this exception type | path or string | No | — |
| `{{CYCLE}}` | Promotion cycle or process period this request is associated with | string | No | current cycle |
| `{{DEADLINE}}` | The official deadline that was missed or constraint that applies | string | No | — |
| `{{EVIDENCE}}` | Any supporting evidence provided (ticket numbers, screenshots, leave records, etc.) | string | No | — |
| `{{REVIEWER}}` | Name of the human reviewer who will receive flagged decisions at the approval gate | string | No | — |

---

## The 6-Phase Pipeline

---

### Phase 1: INTAKE EXCEPTION
**Control Mode: DELEGATE** | **Entropy: E1 (Deterministic)**

Pure capture. Zero interpretation. Collect every relevant fact about the exception request before any analysis begins.

#### Actions

1. Confirm all required variables are populated. If any required variable is missing, stop and request it before proceeding — do not infer missing facts.
2. Record the structured intake:

```
Exception Intake Record
-----------------------
Exception Type:   {{EXCEPTION_TYPE}}
Requester:        {{REQUESTER}}
Associate:        {{ASSOCIATE}}
Cycle / Period:   {{CYCLE}}
Deadline:         {{DEADLINE}}
Stated Reason:    {{REASON}}
Evidence:         {{EVIDENCE}}
Policy Docs:      {{POLICY_DOCS}}
Prior Decisions:  {{PRIOR_DECISIONS}}
Received:         [timestamp]
```

3. Identify any factual ambiguities in the stated reason that will require clarification in Phase 2:
   - Is the reason a first-person account or secondhand?
   - Is evidence attached or only asserted?
   - Is the deadline miss confirmed or disputed?

#### Escalation Trigger
> If the stated reason contains claims that cannot be verified from the intake data alone (e.g., "there was a system error" with no ticket) — flag this as **UNVERIFIED_CLAIM** and carry it forward to Phase 3. Do not resolve it in intake.

#### Output
A complete, verbatim intake record with no editorial. Every ambiguity flagged, not resolved.

---

### Phase 2: CLASSIFY REASON
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

Interpret the stated reason and assign a classification. The classification determines which policy rules apply and whether precedent from prior decisions is directly relevant.

> **ANCT note:** The stated reason is not always the operative reason. A manager who "didn't know about the deadline" may actually have had notice but deprioritized it. A "system error" claim may be accurate or it may be a post-hoc framing. Classification requires judgment, not just label-matching.

#### Reason Classification Taxonomy

| Class | Definition | Policy Implication |
|-------|-----------|-------------------|
| **TECH_GLITCH** | A confirmed or credibly claimed system failure prevented the action (evidence exists or is verifiable) | Strongest basis for APPROVE under most policies |
| **HUMAN_ERROR** | The requester or associate made a mistake — missed the deadline, forgot, did not prioritize | Weakest basis for APPROVE; most common class |
| **PROCESS_GAP** | The process itself made compliance unreasonably difficult (e.g., system unavailable during leave, no delegated access) | Moderate basis for APPROVE; warrants process review note |
| **POLICY_GAP** | The policy did not anticipate this scenario (novel edge case with no prior precedent) | Basis for ESCALATE rather than APPROVE or DENY; requires human judgment |
| **INTENTIONAL_GAMING** | Evidence suggests the requester knowingly delayed and is now using the exception process as a workaround | Basis for DENY; flag for pattern monitoring |

#### Classification Actions

1. Apply the taxonomy to the stated reason. Assign one primary class.
2. If the stated reason contains elements of multiple classes, assign the **primary class** (most operative) and note the secondary.
3. Flag any `UNVERIFIED_CLAIM` carried forward from Phase 1 — note how it affects the classification confidence.

#### Classification Output

```
Classification: [CLASS]
Primary basis: [one sentence explaining why this class applies]
Secondary element (if any): [class + brief note]
Confidence: HIGH / MEDIUM / LOW
UNVERIFIED_CLAIM impact: [note if applicable, else "none"]
```

#### Escalation Trigger
> If the classification is `POLICY_GAP` → note this explicitly. Phase 5 will route this to ESCALATE regardless of the policy check outcome in Phase 3.

---

### Phase 3: POLICY CHECK
**Control Mode: NARRATE** | **Entropy: E3 (Analytical)**

Look up the applicable policy rules given the exception type and classification. Then check prior decisions for precedent. The output of this phase is the evidentiary foundation for Phase 4.

> **ANCT note:** Policy lookup is deterministic — the text either supports or does not support the exception. Precedent comparison is interpretive — prior decisions may differ in ways that are material or may be superficial. Distinguish between the two.

#### Actions

**Step 1 — Policy Rule Lookup**

For each document in `{{POLICY_DOCS}}`:
1. Identify the rule(s) that directly apply to this exception type and classification.
2. Note any explicit exception language in the policy (e.g., "deadline enforced unless confirmed tech glitch").
3. Note any ambiguities in the policy language that could support either outcome.

Policy Rule Summary:
```
Applicable Rule(s):
  - [Rule text or reference, one per line]

Exception Language (if any):
  - [Exact language from policy, or "none found"]

Policy Ambiguity (if any):
  - [Description of ambiguity, or "none"]
```

**Step 2 — Precedent Check**

If `{{PRIOR_DECISIONS}}` is provided:
1. Identify prior decisions of the same `{{EXCEPTION_TYPE}}` and same or similar `{{REASON_CLASS}}`.
2. For each relevant precedent, note:
   - Outcome (APPROVE / DENY / ESCALATE)
   - Reason class
   - Whether evidence was provided
   - How similar it is to the current request

```
Precedent Summary:
  Prior decisions found: [N]
  Most relevant precedents:
    - [ID/date]: [EXCEPTION_TYPE] / [CLASS] / [OUTCOME] — similarity: HIGH/MEDIUM/LOW
    - [ID/date]: [EXCEPTION_TYPE] / [CLASS] / [OUTCOME] — similarity: HIGH/MEDIUM/LOW

  Precedent direction: TOWARD_APPROVE / TOWARD_DENY / MIXED / NO_PRECEDENT
  Inconsistency risk: [Note if prior decisions for same type are split, or "none"]
```

#### Escalation Trigger
> If precedent is MIXED for the same exception type in the same cycle — flag `CONSISTENCY_RISK`. Surface this in Phase 4 and Phase 5 — a decision that contradicts a same-cycle precedent must be explicitly justified, not silently issued.

---

### Phase 4: GENERATE BOTH SIDES
**Control Mode: GENERATE → NARRATE** | **Entropy: E4 (Creative judgment)**

Before any recommendation is made, generate the strongest possible argument for APPROVE and the strongest possible argument for DENY. This phase is explicitly creative — it must produce the most rigorous version of each case, not a strawman.

> **ANCT circuit breaker:** If this phase produces a recommendation without first completing both the APPROVE and DENY argument tables below — stop and expand. A recommendation without both sides is premature compression.

> **Anti-gaming note:** The purpose of this phase is not to create false balance. It is to prevent the recommendation in Phase 5 from being driven by the first argument that comes to mind, by requester persistence, or by default deference to the deadline. The strongest argument for the losing side must be visible and explicitly set aside.

#### Generate: Strongest Case for APPROVE

Construct the most rigorous argument that this exception should be approved. Do not hedge. Write it as an advocate would.

```
Strongest Case for APPROVE
--------------------------
Core argument:     [One sentence — the most compelling reason to approve]
Policy support:    [Which policy rule or exception language supports this]
Precedent support: [Most favorable prior decision, if any]
Equitable argument: [Why denying this would be unfair or inconsistent]
Risk of denying:   [What harm or cost follows from a denial]
Weaknesses:        [Where this argument is vulnerable — be honest]
```

#### Generate: Strongest Case for DENY

Construct the most rigorous argument that this exception should be denied. Do not hedge. Write it as a policy enforcer would.

```
Strongest Case for DENY
-----------------------
Core argument:     [One sentence — the most compelling reason to deny]
Policy support:    [Which policy rule directly supports holding the deadline]
Precedent support: [Most relevant prior denial, if any]
Systemic argument: [Why approving this sets a problematic precedent]
Risk of approving: [What harm or cost follows from an approval]
Weaknesses:        [Where this argument is vulnerable — be honest]
```

#### Escalation Trigger
> If the APPROVE and DENY arguments are genuinely equivalent in strength (no clear dominant case) → route Phase 5 to ESCALATE rather than attempting to pick APPROVE or DENY. Document why the case is unresolvable at this level.

---

### Phase 5: RECOMMEND
**Control Mode: NARRATE** | **Entropy: E2-E3 (Analytical)**

Apply the policy check and the two-sided argument to produce a recommendation. The recommendation must be traceable — every APPROVE cites the policy basis; every DENY cites the specific rule being enforced; every ESCALATE explains what information or authority is needed.

#### Recommendation Decision Logic

```
IF REASON_CLASS == POLICY_GAP
  → ESCALATE (policy does not cover this scenario; requires human authority)

ELSE IF REASON_CLASS == TECH_GLITCH AND evidence is verified
  → APPROVE (explicit exception language in most policies; highest defensibility)

ELSE IF REASON_CLASS == TECH_GLITCH AND evidence is UNVERIFIED_CLAIM
  → DENY unless evidence can be obtained, OR ESCALATE for evidence review

ELSE IF REASON_CLASS == PROCESS_GAP
  → Weigh: Was the gap foreseeable? Did the requester take any available mitigating action?
    If yes to both: DENY (gap was known; workaround existed)
    If no to either: ESCALATE or conditional APPROVE (document the process gap for remediation)

ELSE IF REASON_CLASS == HUMAN_ERROR
  → DENY (default; consistent with policy language "deadline enforced unless confirmed tech glitch")
    Exception: if CONSISTENCY_RISK flagged and same-cycle precedents favor APPROVE, ESCALATE

ELSE IF REASON_CLASS == INTENTIONAL_GAMING
  → DENY (document pattern; flag for monitoring)
```

#### Recommendation Output

```
Recommendation: APPROVE / DENY / ESCALATE

Primary rationale (one sentence):
  [The single most important reason for this recommendation]

Policy basis:
  [Citation to specific policy rule or exception language]

Precedent alignment:
  CONSISTENT / INCONSISTENT / NO_PRECEDENT
  [If INCONSISTENT: explain why this decision diverges and why that is justified]

Argument set aside:
  [The strongest argument for the other outcome, and the specific reason it does not prevail here]

Precedent risk:
  NONE / LOW / HIGH
  [If HIGH: describe what this decision implicitly allows in future cycles]

Approval gate flag: YES / NO
  [YES if: DENY + precedent risk HIGH, or ESCALATE, or CONSISTENCY_RISK flagged]
```

#### Escalation Trigger
> If `Approval gate flag: YES` — do not proceed to Phase 6 until Phase 5.5 is completed. Surface the full recommendation for human review.

---

### Phase 5.5: APPROVE — HUMAN REVIEW GATE
**Control Mode: DELEGATE** | **Entropy: E2 (Procedural)**

> **This phase is the primary protection against precedent-setting decisions being sent without human review.**
> It fires automatically when `Approval gate flag: YES`. It cannot be bypassed.

#### When This Gate Fires

| Condition | Gate behavior |
|-----------|--------------|
| DENY + precedent risk HIGH | Always halt — DENY decisions that implicitly allow or deny future requests require explicit sign-off |
| ESCALATE | Always halt — ESCALATE means the decision exceeds automated authority |
| CONSISTENCY_RISK flagged | Always halt — a decision that contradicts same-cycle precedent must be intentional, not accidental |
| APPROVE with no precedent | Proceed without gate (low risk; no systemic impact) |
| APPROVE consistent with precedent | Proceed without gate |
| DENY with no precedent risk | Proceed without gate (clear policy enforcement, no systemic impact) |

#### Approval Gate Report Format

Present the following to `{{REVIEWER}}` and wait for explicit instruction:

```
Exception Policy Evaluator — Human Review Required
===================================================

Request:          {{EXCEPTION_TYPE}} exception for {{ASSOCIATE}}
Submitted by:     {{REQUESTER}}
Cycle:            {{CYCLE}}

Recommendation:   [APPROVE / DENY / ESCALATE]
Gate trigger:     [Which condition caused this gate to fire]

---

Recommendation Summary
-----------------------
[Full Phase 5 recommendation output — rationale, policy basis, precedent alignment, argument set aside]

---

Why Human Review is Required
------------------------------
[Specific explanation of the precedent risk, consistency issue, or authority gap
 that makes this decision inappropriate to send without sign-off]

---

Action Required
---------------
Reply with one of:
  CONFIRM — proceed with the recommended outcome and draft the response
  OVERRIDE APPROVE — override to APPROVE; provide rationale (required)
  OVERRIDE DENY — override to DENY; provide rationale (required)
  HOLD — do not send yet; additional information needed (specify what)
  ESCALATE — surface to next level of authority (specify who)
```

#### Response Handling

| Reviewer Response | Action |
|------------------|--------|
| `CONFIRM` | Proceed to Phase 6 with the recommended outcome |
| `OVERRIDE [outcome] + rationale` | Record the override and rationale; update the recommendation; proceed to Phase 6 with the override outcome |
| `HOLD` | Log the hold; stop processing; surface what is needed to resume |
| `ESCALATE` | Log the escalation target; stop processing; do not draft a response |
| No response | Log as unresolved; do not proceed; do not draft a response |

> **Record-keeping:** Every gate activation, reviewer response, and override is logged to the prior decisions compendium at `{{PRIOR_DECISIONS}}` (if provided) so it surfaces as precedent in future cycles.

---

### Phase 6: DRAFT RESPONSE
**Control Mode: DELEGATE** | **Entropy: E1-E2 (Procedural)**

The recommendation is finalized. Draft the response email. The response must be professional, clear, policy-grounded, and relationship-preserving — regardless of whether the outcome is APPROVE or DENY.

> **ANCT note:** This phase does not re-evaluate the decision. The decision is made. This phase only translates it into a response that a professional would be willing to sign and send.

#### Response Drafting Rules

| Rule | Requirement |
|------|------------|
| **Policy citation** | Every DENY must cite the specific policy rule being enforced — not just "policy says so" |
| **No editorial on requester intent** | Do not imply the requester was negligent, dishonest, or gaming the system — even if the classification was INTENTIONAL_GAMING |
| **No conditional language for firm decisions** | If the outcome is DENY, do not write "unfortunately we are unable to..." hedges that imply the decision could change. Be clear. |
| **Offer next steps** | For DENY: if there is a legitimate path forward (next cycle, alternative process), name it |
| **For APPROVE: state what is happening** | Do not make the requester guess whether the exception was granted |
| **Preserve the relationship** | The requester will work with you again. The tone must be professional and fair — firm decisions do not require cold language |

#### Response Format

```
Draft Response
--------------
To:       {{REQUESTER}}
Subject:  Re: [Exception Request] — {{ASSOCIATE}} / {{CYCLE}}

[Opening: acknowledge the request — one sentence]

[Decision: state the outcome clearly in the first substantive paragraph]

[Rationale: policy basis in plain language — one to two sentences; cite the rule, not the rule number]

[Next steps (if any): what the requester can do now]

[Closing: professional, brief]

[Signature]
```

#### Escalation Trigger
> If the recommendation is ESCALATE — do not draft a response to the requester. Draft an internal escalation summary for `{{REVIEWER}}` or the designated next-level authority instead. Label it clearly as an internal escalation memo, not a requester-facing response.

---

## Anti-Patterns

```
EXCEPTION POLICY EVALUATOR ANTI-PATTERNS:

DECISION INTEGRITY ANTI-PATTERNS:

✗ Approving because the requester is persistent
  Persistence is not a policy criterion. A request submitted for the fourth
  time is evaluated on the same facts as the first.
  Fix: Phase 4 generates the APPROVE case on its merits — if persistence is
  the only new argument, it does not change the recommendation.

✗ Denying without a clear policy citation
  "We can't make exceptions" is not a policy citation.
  Every DENY must name the specific rule that is being enforced.
  Fix: Phase 5 requires explicit policy basis for every recommendation.
  A DENY with no policy citation is not a valid output of this skill.

✗ Inconsistent decisions for the same exception type in the same cycle
  Approving a HUMAN_ERROR exception for one manager and denying the
  same exception for another in the same cycle, without documented justification.
  Fix: Phase 3 precedent check + CONSISTENCY_RISK flag + Phase 5.5 gate
  force same-cycle inconsistencies to surface before the response is sent.

✗ Treating a TECH_GLITCH claim as verified without evidence
  "I couldn't get in" is not a confirmed system error.
  Fix: Phase 1 flags UNVERIFIED_CLAIM; Phase 2 assigns TECH_GLITCH
  with LOW confidence; Phase 5 routes unverified TECH_GLITCH claims to
  DENY or conditional ESCALATE, not automatic APPROVE.

✗ Skipping Phase 4 when the answer "seems obvious"
  The whole point of Phase 4 is that it runs before the recommendation — not
  as a check after. The strongest argument for the losing side must be generated
  before deciding, not invented post-hoc to justify a conclusion.
  Fix: Phase 4 is never optional. No output from Phase 5 is valid without
  a completed Phase 4 output in the same session.

✗ Sending a precedent-setting DENY without human review
  A DENY that says "we enforce the deadline for everyone" is a policy statement
  that binds future cycles. It should not go out without a human signing it.
  Fix: Phase 5.5 gate fires automatically on DENY + HIGH precedent risk.

✗ Drafting a cold or adversarial response for a DENY
  The requester is a colleague. A DENY can be firm and relationship-preserving
  at the same time. Cold language is not "professionalism."
  Fix: Phase 6 drafting rules require professional tone for all outcomes.

✓ CORRECT PATTERNS:

✓ Classify the reason before checking policy — the classification determines which rules apply
✓ Generate both sides before recommending — the strongest losing argument must be visible and set aside
✓ Cite the specific policy rule in every DENY — not just "policy says so"
✓ Flag CONSISTENCY_RISK when same-cycle precedents point differently — do not resolve silently
✓ Gate every DENY with HIGH precedent risk — do not send policy-setting responses without human sign-off
✓ Log every decision to the prior decisions compendium — future cycles depend on this record
✓ Separate tone from outcome — a firm DENY and a professional DENY are not in conflict
✓ When the case is genuinely unresolvable — ESCALATE; do not force APPROVE or DENY
```

---

## Representative Cases

The following cases illustrate the skill's intended behavior. They are not policy — they are worked examples that show how the phases interact.

### Case A: Post-Deadline Nomination (Human Error)
**Request:** Manager did not nominate an associate by the promotion cycle deadline. Exception submitted by the manager's skip-level.
**Intake:** EXCEPTION_TYPE=nomination, REASON="Manager was overwhelmed and missed the deadline", EVIDENCE=none

- Phase 2 Classification: HUMAN_ERROR (high confidence; no system failure; no process barrier)
- Phase 3 Policy: Policy states "deadline enforced unless confirmed tech glitch." No exception language for workload.
- Phase 4 Both Sides:
  - APPROVE case: Associate should not be penalized for manager error; talent impact is real; next cycle is 6 months away.
  - DENY case: Deadline was communicated; every other manager complied; approving here undermines the deadline for all.
- Phase 5 Recommendation: DENY. Policy basis: deadline enforcement rule. Argument set aside: associate impact is real but is caused by manager error, not system failure — the policy does not assign the cost to the organization.
- Phase 5.5: Precedent risk LOW (clear DENY per policy). Gate does not fire.
- Phase 6: Response acknowledges the situation professionally, states the decision, cites the deadline rule, and names the next cycle as the path forward.

### Case B: Tool Access During Leave (Process Gap)
**Request:** Manager was on approved leave during the nomination window and had no ability to delegate access in the tool.
**Intake:** EXCEPTION_TYPE=access, REASON="On approved leave; tool does not support delegation", EVIDENCE=leave approval record

- Phase 2 Classification: PROCESS_GAP (the tool's absence of a delegation feature is a structural barrier, not human error)
- Phase 3 Policy: Policy states deadline is enforced unless confirmed tech glitch. No explicit language for leave + no delegation.
- Phase 4 Both Sides:
  - APPROVE case: The manager complied with all obligations and was blocked by a process design failure. Denying penalizes compliance with HR leave policy.
  - DENY case: Leave is foreseeable; alternative arrangements should have been made before departing; the deadline is the deadline.
- Phase 5 Recommendation: ESCALATE. Rationale: PROCESS_GAP with evidence and no applicable exception language — this is a policy gap that requires human authority to resolve AND a process remediation note (tool should support delegation).
- Phase 5.5: Gate fires (ESCALATE). Surfaces to reviewer with full analysis.
- Phase 6: No requester-facing response until reviewer instruction received.

---

## Compliance

- **PII Risk:** Medium. This skill processes names of individuals and their exception circumstances. Outputs should not be stored in systems that expose them beyond the intended reviewer and requester. The prior decisions compendium should be treated as HR-adjacent data.
- **Model Recommendation:** Sonnet for all phases. Phase 4 (Generate Both Sides) benefits from maximum reasoning depth — if Opus is available and the case is high-stakes, it can be invoked for Phase 4 only.
- **Human Oversight:** Phase 5.5 (Approve) is the primary control. It fires automatically for DENY + HIGH precedent risk, ESCALATE, and CONSISTENCY_RISK. No response is drafted or sent from a gate-triggered session until a human provides explicit instruction. The skill does not default to proceeding on silence.
- **Consistency Assurance:** The precedent check in Phase 3 and the CONSISTENCY_RISK flag are specifically designed to surface same-cycle inconsistencies before they become permanent record. A decision that contradicts a prior same-cycle decision is not blocked — but it must be intentional and documented, not accidental.
- **Record-Keeping:** Every gate activation, override, and final decision should be logged to `{{PRIOR_DECISIONS}}`. This is what makes the skill self-improving across cycles — the precedent compendium is the organizational memory.

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| **adaptive-workflow-architect** | Designed this skill's ANCT architecture |
| **inbox-intelligence** | Identifies exception requests arriving in email; can route them to this skill for evaluation |
| **promo-cycle-monitor** | Tracks nomination and exception volumes across the cycle; exception patterns detected here feed into that monitor |
| **decision-memo-distiller** | Can be invoked after Phase 5 to produce a formal memo version of the recommendation for record-keeping |
