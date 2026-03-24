---
name: change-comms-architect
description: "Architects comprehensive change communication plans with audience-segmented message variants, channel strategy, timing, and Q&A sets for any organizational change."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - change-management
  - communication
  - stakeholders
  - planning
model_recommendation: sonnet
risk_level: medium
---

# 🎯 Change Comms Architect

> Architect the full communication plan for any organizational change — segmented by audience, sequenced by timing, and ready for the questions you know are coming.

## Core Philosophy

The most common failure mode in change communication is not bad writing — it is treating change communication as a single message broadcast problem when it is actually a multi-audience, multi-channel sequencing problem. A reorg announcement that lands well with the executive team can land catastrophically with frontline managers if it reaches them via rumor before it reaches them via leadership. The same facts, communicated in the wrong sequence to the wrong audiences, generate resistance that a well-sequenced plan would have neutralized.

This skill treats change communication as an architecture problem. The architect must map every affected audience before writing a single word. Each audience has a different relationship to the change, a different emotional stake, a different information need, and a different channel preference. A message that says "this change streamlines our structure for growth" communicates something entirely different to a manager who just lost headcount than to an executive who proposed the change. Acknowledging that difference — rather than pretending a single message can serve both — is the core discipline this skill enforces.

The Q&A anticipation set is not optional or supplementary. In every organizational change, the questions people ask are more revealing of their real concerns than anything in the announcement. Building the Q&A set before the communication lands means the communicator has done the empathy work: they have imagined themselves in each audience's position and anticipated the anxious, skeptical, and practical questions that any honest person would ask. Skipping this step is a form of wishful thinking that the real questions will not be asked.

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake Change Context | E1 – Deterministic | DELEGATE | Structured collection of fixed change parameters; no inference |
| 2. Map Audience Segments | E3 – Analytical | NARRATE | Requires reasoning about stakeholder relationships, reactions, and information needs |
| 3. Generate Message Variants | E4 – Generative + E3 | GENERATE then NARRATE | Drafts require creativity; validation requires consistency checking |
| 4. Validate Consistency | E3 – Analytical | NARRATE | Cross-audience fact-checking and sensitivity review require judgment |
| 5. Produce Comms Pack | E1 – Deterministic | DELEGATE | Assembles validated components into final structured output |

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{SOURCE_MATERIAL}}` | Full description of the change: what is happening, why, and what the decision is | string | Yes | — |
| `{{OBJECTIVE}}` | What this change is designed to achieve; the organizational rationale | string | Yes | — |
| `{{AUDIENCE}}` | All groups affected by this change (list all; err on the side of inclusion) | string | Yes | — |
| `{{CHANNEL}}` | Available communication channels (email, all-hands, Slack, 1:1, town hall, intranet, manager cascade) | string | Yes | — |
| `{{DEADLINE}}` | When communication must land; any hard announcement dates | string | Yes | — |
| `{{SENSITIVITY_LEVEL}}` | Confidentiality classification: open / restricted / confidential | string | Yes | — |
| `{{CONSTRAINTS}}` | What cannot be disclosed at each stage; any legal, HR, or regulatory restrictions on messaging | string | No | None specified |
| `{{OWNER}}` | Named individual responsible for executing and owning the comms plan | string | Yes | — |

## ⚙️ Phases

### Phase 1: Intake Change Context
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Collect all required context before any audience mapping or message drafting begins. The quality of the audience segmentation and message variants is entirely dependent on having a clear, complete picture of the change. Vague intake produces generic messages that fail every audience.

Specifically probe for the decision status — is this change decided, or still being socialized? Communicating a decided change as if it is still open for input destroys trust faster than any other error. Also probe for what the owner does and does not know at the time of announcement: there will always be unanswered questions (Who specifically is affected? What are the new reporting lines?), and the comms plan must account for communicating honestly under uncertainty.

**Process:**
1. Present the intake variable set and collect all required fields
2. Confirm whether the change is decided (communicate as fact) or proposed (communicate as direction)
3. Probe for what is known vs. unknown at announcement time — identify information gaps that will generate questions
4. Identify the hardest audience: the group most likely to react negatively. Name them explicitly.
5. Identify any regulatory or legal constraints on what can be said (e.g., pre-TUPE consultation requirements, securities quiet periods, labor relations rules)
6. Confirm `{{DEADLINE}}` includes both the internal and external (if applicable) announcement sequence

**Output:** A complete intake record with all required fields, a known/unknown matrix, hardest-audience identification, and any regulatory flags.

---

### Phase 2: Map Audience Segments
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Before writing any messages, build a complete audience map. For each audience segment identified in `{{AUDIENCE}}`, produce a structured profile: what changes for them specifically, their likely initial emotional reaction (supportive / cautious / resistant / unknown), their primary information need, their preferred channel, and when they need to hear it relative to other audiences.

The sequencing judgment — who hears first — is often the most consequential decision in the entire comms plan. The general principle is: inform before announce. Managers must be informed before their teams. Senior leadership must be aligned before all-company communication. People whose roles are materially affected must be personally informed before any group announcement. Violating this sequence is how rumors start.

**Process:**
1. List every audience segment named in `{{AUDIENCE}}`, then add any implied audiences the requester may have missed (e.g., if a reorg is described, ask whether the HR BP community is an audience, whether external vendors or partners are affected)
2. For each segment, complete the audience profile: what changes for them, expected emotional reaction, primary information need, channel preference, and sequence position
3. Identify any audiences with conflicting needs (e.g., an audience that is both a "recipient" of the change and a "communicator" to others — managers are the classic case)
4. Flag any audiences where the change has materially adverse implications (role elimination, reporting changes, scope reduction) — these require individual, private communication before group announcement
5. Produce the audience sequence: a ranked order for who receives communication, with rationale for the sequence

**Output:** A complete audience profile table for each segment, plus a recommended communication sequence with rationale.

---

### Phase 3: Generate Message Variants
**Entropy Level:** E4 – Generative then E3 – Analytical
**Control Mode:** GENERATE then NARRATE

Write a distinct message variant for each audience segment. GENERATE produces the draft; NARRATE then validates that each draft is appropriate for the audience's context and emotional position, uses the right channel conventions, and does not over- or under-disclose relative to `{{CONSTRAINTS}}`.

Each message variant must follow a consistent structure: (1) lead with what this means for this audience specifically — not with the org-level rationale, (2) explain the why at a level of detail appropriate to the audience, (3) acknowledge the likely concern or question this audience will have and address it directly, (4) state clearly what happens next and by when, (5) provide a specific action or contact for questions. Messages that lack a concrete "what happens next" create anxiety; people fill information vacuums with worst-case assumptions.

**Process:**
1. For each audience segment, draft a message variant using the five-element structure
2. Calibrate tone by audience: executive variants are direct and strategic; manager variants are instructional and empowering; employee variants are human and specific; external variants are formal and limited in scope
3. For manager variants, include talking points in addition to the message — managers need to be equipped to have conversations, not just receive communications
4. For any audience where the change has adverse implications, draft a separate sensitive conversation guide in addition to the group message
5. Apply channel conventions: an email variant has a subject line, a clear ask, and a signature; a Slack message is shorter with a link to detail; a town hall script has transitions and Q&A prompts; a 1:1 guide has opening lines and listening prompts
6. NARRATE validation: review each variant for appropriateness, disclosure level, and tone. Flag any that feel performative, overly corporate, or emotionally tone-deaf.

**Output:** A full set of audience-specific message variants with channel-appropriate formatting, manager talking points where applicable, and sensitive conversation guides where needed.

---

### Phase 4: Validate Consistency
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Cross-check all message variants for factual consistency, disclosure appropriateness, and absence of conflicting statements. This phase catches the common problem where the executive variant contains a detail that contradicts the employee variant, or where the manager talking points make a commitment that the HR team is not prepared to honor.

Consistency does not mean identical — audiences should receive different framing, different levels of detail, and different emphasis. Consistency means the facts are the same across all variants. The date is the same. The decision is described the same way. The "why" is compatible across all versions even if it is explained at different levels of abstraction. And no variant makes a promise — about timing, about process, about outcomes — that has not been confirmed with the relevant decision-maker.

**Process:**
1. Extract all factual claims from every message variant and list them in a consistency matrix
2. Check each factual claim across all variants: dates, decision descriptions, next steps, named owners
3. Flag any inconsistency: same fact stated differently, promise made in one variant not reflected in others, detail disclosed in one variant that is restricted in another
4. Check disclosure levels: verify no audience is receiving information designated confidential at their sensitivity level
5. Review for language that makes commitments the owner has not confirmed ("no further changes are planned," "this is the final structure," "no roles will be eliminated") — flag any such language for explicit confirmation or removal
6. Check tone for each variant against the audience's emotional position: a variant written for a resistant audience that reads as dismissive of their concerns will fail

**Output:** A consistency validation report with all flagged items and recommended corrections, plus a go/no-go recommendation for each variant.

---

### Phase 5: Produce Comms Pack
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Assemble all validated components into a single, structured change communications pack that the owner can use directly. The pack must be organized for operational use — not for reading but for doing. The person executing the comms plan should be able to open the pack and know exactly what to send, to whom, through which channel, and in what order, without having to reconstruct the logic.

The Q&A set is a mandatory component of the pack. Build a minimum of 10 questions, organized by audience (questions this audience will definitely ask). Include the recommended answer and any "hold for later" questions that cannot be answered at announcement time, with a note on when they will be answered.

**Process:**
1. Compile the audience map in table format: audience segment, what changes for them, channel, sequence position, timing
2. Build the message matrix: rows = audiences, columns = channel / timing / variant reference
3. Assemble all message variants in sequence order with channel labels
4. Build the Q&A set: minimum 10 questions, organized by audience segment, with recommended answers and "hold" flags
5. Add a rollout timeline: a day-by-day (or week-by-week for longer changes) sequence of what goes out, to whom, through which channel
6. Add an owner checklist: the specific actions `{{OWNER}}` must take before, during, and after the communication lands
7. Append a "what if" section: what to do if communication leaks before the planned sequence, what to do if a key leader is unavailable on announcement day, what to do if significant negative reaction occurs

**Output:** A complete, operationally ready change communications pack including: audience map, message matrix, all message variants, Q&A set, rollout timeline, owner checklist, and contingency guidance.

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Writing one message and sending it to all audiences | Segment every audience; what reassures one group concerns another |
| Announcing a decided change as if input is still welcome | State the decision as a decision; people respect honesty more than false consultation |
| Communicating to all audiences simultaneously | Sequence is strategy; managers must be informed before their teams, always |
| Omitting the "what happens next" from messages | Every message must end with a specific next step and timeline; ambiguity generates anxiety |
| Skipping the Q&A preparation | Anticipating questions is empathy work; every change comms plan must include it |
| Using organizational rationale as the message lead | Lead with what it means for this specific audience, not with why it is good for the company |
| Making commitments in messaging that haven't been confirmed | Every promise in a message must be explicitly cleared with the decision-maker before sending |
| Treating managers as just another employee audience | Managers are both a recipient audience and a communication channel; equip them separately |

## 💡 Example Applications

| Use Case | Input | Output |
|----------|-------|--------|
| Org restructure merging two HR functions | Source: 2 teams merging, 1 leader departing, reporting change for 12 people; sensitivity: confidential; deadline: Thursday | 5 audience variants (departing leader, affected employees, peer leaders, broader HR, exec), manager talking points, all-hands script, 15-question FAQ, 4-day rollout sequence, contingency for early leak |
| HR system migration from Workday to SAP | Change: new HRIS live in 90 days; audience: all employees, managers, HR team, IT, payroll | 4 variants by role, 90-day timeline with 4 comms milestones, manager enablement guide, IT coordination brief, employee FAQ on data and access, go-live week communication script |
| Benefits policy change — parental leave reduction | Change: leave policy changing; legally sensitive; audience: all employees, managers, legal, external comms | Employee plain-language version, manager briefing with talking points, exec summary, legal review flag embedded in pack, reactive statement for media if needed, 12 anticipated employee questions with approved answers |
| Senior leadership transition — VP People departing | Change: CHRO transition, 6-week overlap period; audience: HR team, exec peers, broader org, external | Internal team announcement (personal, written by CHRO), exec peer briefing (strategic, forward-looking), all-company announcement (appreciative, confident in transition), external LinkedIn-appropriate version, Q&A set for "what does this mean for us?" across 4 audience levels |

## 🖥️ Platform Notes

**CLI:** Best used as a single-session interactive workflow. Feed `{{SOURCE_MATERIAL}}` as a full briefing document. Output the comms pack as a structured markdown document that can be converted to PDF or loaded into a project management tool.

**Web:** Ideal format for this skill. The audience map and message matrix render well as tables; the rollout timeline renders as a checklist. Use Claude's web interface for iterative refinement of individual variants after the full pack is generated.

**IDE:** Useful for teams maintaining comms templates in a content management system. The message variants can be stored as template files with variable substitution for change-specific details.

**Any LLM:** Phase 3 (message generation) and Phase 4 (consistency validation) require strong instruction-following and contextual reasoning. The skill is not appropriate for models that struggle with multi-document consistency checking. Sonnet or above recommended.

## 📋 Compliance

**AI Governance Alignment:** Supports responsible change management practice aligned with PROSCI ADKAR and Kotter 8-step frameworks. The audience segmentation approach is consistent with organizational change management best practices for stakeholder communication.

**PII Risk Level:** medium — Change communications often reference named individuals (leaders, departing executives, role changes). Handle any named individual references with care; apply the principle of minimum necessary disclosure. Do not include more personal detail in any message than is necessary for the audience to understand the change.

**Model Recommendation:** sonnet — Phase 3 requires genuine creative writing ability to produce emotionally intelligent, audience-appropriate message variants. Phase 4 requires multi-document reasoning for consistency checking. Haiku produces messages that are technically correct but emotionally flat and fail resistant audiences.

**Data Handling:** No personal data should be included in `{{SOURCE_MATERIAL}}` beyond what is necessary to describe the change. Named individuals referenced in comms planning (e.g., a departing leader) should be treated with discretion. Comms pack outputs should be stored in secure, access-controlled locations given the confidential nature of pre-announcement change materials.
