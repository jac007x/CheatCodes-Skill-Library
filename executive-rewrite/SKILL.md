---
name: executive-rewrite
description: "Rewrites any draft communication to executive standards: bottom-line-up-front structure, precise language, calibrated tone, and audience-appropriate variants."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - writing
  - executive-comms
  - rewrite
  - communication
model_recommendation: sonnet
risk_level: low
---

# 🎯 Executive Rewrite

> Restructure any draft so the decision lands in the first sentence, not the last paragraph.

## Core Philosophy

Most draft communications earn a skim, not a read. The writer buries the ask in paragraph three because they want to "build context first." The executive reads the first two lines, decides this is not urgent, and moves on. The request dies in their inbox. This is not a failure of the executive's attention — it is a failure of the communication's structure.

Executive communication has one inviolable rule: the bottom line comes first. Not the context. Not the background. Not "I wanted to reach out about." The decision, the ask, the recommendation — whatever requires the executive's response — goes in line one. Everything else is supporting detail that the reader may or may not need, presented in descending order of importance so they can stop reading the moment they have what they need.

This skill applies that principle systematically. But rewriting for structure is only half the job. The other half is calibration: knowing this specific executive's communication style and ensuring the rewrite lands in their register, not a generic "professional" register. A data-first executive needs numbers in the headline, not narrative. A narrative-first executive needs the story frame, then the numbers. A direct communicator wants assertions, not hedges. Getting the calibration wrong produces a rewrite that is structurally correct but tonally off — and a tonally off communication from a team member lands as a signal about that person's judgment. This skill handles both.

## 🏗️ ANCT Architecture

**Entropy Profile:**

| Phase | Entropy | Control Mode | Why |
|-------|---------|--------------|-----|
| 1. Intake Source & Context | E1 – Deterministic | DELEGATE | Structured extraction of draft, audience, channel, and constraints |
| 2. Audit Weaknesses | E3 – Analytical | NARRATE | Requires diagnostic judgment: what structural and tonal problems exist? |
| 3. Rewrite | E4 – Creative | GENERATE → NARRATE | GENERATE produces draft; NARRATE validates it against the audit findings |
| 4. Calibrate Tone | E3 – Analytical | NARRATE | Applies known preferences and audience-specific adjustments |
| 5. Produce Variants | E4 → E1 | GENERATE → DELEGATE | GENERATE creates channel variations; DELEGATE formats and labels them |

---

## 📥 Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{DRAFT}}` | The source text to be rewritten, verbatim | string | Yes | — |
| `{{AUDIENCE}}` | Executive name/role/level and any known context about them | string | Yes | — |
| `{{CHANNEL}}` | Delivery format: email, memo, verbal briefing, one-pager, deck slide | string | Yes | email |
| `{{OBJECTIVE}}` | What this communication must accomplish: decision, approval, awareness, action | string | Yes | — |
| `{{KNOWN_PREFERENCES}}` | Executive's known communication preferences, if any | string | No | — |
| `{{SENSITIVITY_LEVEL}}` | Confidentiality level: public, internal, sensitive, restricted | string | No | internal |
| `{{CONSTRAINTS}}` | Word count limits, tone requirements, things not to say | string | No | — |

---

## ⚙️ Phases

### Phase 1: INTAKE SOURCE & CONTEXT
**Entropy Level:** E1 – Deterministic
**Control Mode:** DELEGATE

Collect and structure all inputs before any rewriting begins. This phase is extraction only — no edits, no opinions, no improvements yet. The draft is captured verbatim. All context variables are organized into a working brief that powers Phases 2-5.

**Process:**
1. Capture `{{DRAFT}}` verbatim. Note the approximate word count.
2. Parse `{{AUDIENCE}}`: executive name, role, seniority level, and any stated context about them.
3. Record `{{CHANNEL}}`, `{{OBJECTIVE}}`, `{{KNOWN_PREFERENCES}}`, `{{SENSITIVITY_LEVEL}}`, and `{{CONSTRAINTS}}`.
4. Identify the communication type: email, memo, verbal briefing, one-pager, or deck slide. Each has a different optimal length, format, and structure.
5. Identify the objective type: Is this requesting a decision, seeking approval, providing awareness, requesting an action, or delivering a recommendation? The objective type drives BLUF construction in Phase 3.
6. Produce a context summary. No edits. No improvements. Structure only.

**Output:**
```
INTAKE CONTEXT
Draft word count: [N words]
Channel: [email / memo / verbal / one-pager / deck slide]
Objective type: [decision / approval / awareness / action / recommendation]
Audience: [name, role, level]
Known preferences: [stated preferences or "none provided"]
Constraints: [word limit, tone requirements, restrictions or "none"]
Sensitivity: [level]
```

---

### Phase 2: AUDIT WEAKNESSES
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Read the draft as the executive would. Diagnose every structural and language problem that would cause the executive to disengage, misunderstand, or delay action. Produce a specific diagnostic — not generic writing advice, but a precise analysis of what is wrong in this specific draft.

**Process:**
1. **Check for buried lede.** Where does the ask, decision, or recommendation first appear? If it's not in the first sentence, the lede is buried. Note the paragraph and sentence where it finally appears.
2. **Check for throat-clearing.** Count the sentences before the message starts: "I wanted to reach out," "As we've discussed," "Per our conversation," "I hope this finds you well." Each is a discard candidate.
3. **Check for passive voice.** Passive constructions remove ownership and urgency. Flag every passive construction ("it was decided," "the team was informed," "this has been reviewed").
4. **Check for hedging language.** Executives distrust excessive hedging. Flag: "it seems," "perhaps," "we believe," "it might be worth considering," "some would argue."
5. **Check for the missing ask.** Does the draft explicitly state what the executive needs to do? If the ask is implicit, flag it. The executive should never have to infer what's being asked of them.
6. **Check for excessive length.** Is there content in the draft that the executive doesn't need in order to take the required action? Flag every paragraph that exists to make the writer feel thorough rather than to serve the reader.
7. **Check for unsupported assertions.** Claims without numbers or attribution. Flag every assertion that requires evidence and lacks it.
8. **Check for jargon or acronyms.** Flag any term that requires shared context the executive may not have.
9. Produce a numbered diagnostic list. Each item names the problem, quotes the offending text, and states why it creates friction.

**Output:**
```
DRAFT AUDIT
Word count: [N] → Target: [N for channel]

Issues found:
1. [BURIED LEDE] Ask appears in paragraph 3, sentence 2: "[quote]" — Executive may stop reading before reaching it.
2. [THROAT-CLEARING] Opening 2 sentences have no informational value: "[quote]" — Cut entirely.
3. [PASSIVE VOICE] "[quote]" — Removes ownership; who decided this?
4. [MISSING ASK] Draft describes the situation but never states what executive must do.
5. [EXCESSIVE LENGTH] Paragraph 4 provides background context the executive already has. Cut.
6. [HEDGING] "[quote]" — Replace with a direct assertion or a quantified uncertainty.
7. [UNSUPPORTED ASSERTION] "[quote]" — Needs a number or source, or must be framed as a recommendation rather than a fact.

Severity summary:
  - Critical (blocks comprehension or action): [items #X, #X]
  - High (materially weakens): [items #X, #X]
  - Low (polish): [items #X, #X]
```

---

### Phase 3: REWRITE
**Entropy Level:** E4 – Creative
**Control Mode:** GENERATE → NARRATE

Produce the rewritten version. GENERATE creates the draft rewrite from scratch, applying BLUF structure, active voice, and the minimum viable length for the channel. NARRATE then validates: does the rewrite resolve every critical issue from the audit? Does it preserve the key caveats and nuances that must survive brevity?

**GENERATE Step (expand — produce the rewrite):**

Apply these principles in order:
1. **Line 1 = the bottom line.** The first sentence states the decision, the ask, the recommendation, or the finding. No context first. No background first. The bottom line, in plain language, in the active voice.
2. **Line 2-3 = the one essential context point.** What does the executive need to know to act on line 1? One point only. Not the full background — the one thing that changes the meaning of line 1.
3. **Supporting detail = descending importance.** Everything after lines 1-3 is optional reading. Organize it so the executive can stop at any paragraph and still have what they need.
4. **Cut to minimum viable length.** For email: 100 words or fewer unless complexity requires more (hard maximum: 250 words). For one-pager: 350 words. For verbal briefing: 90 seconds (approx. 200 words spoken). For deck slide: one headline sentence + 3 supporting bullets.
5. **Active voice throughout.** Every sentence has a clear subject taking an action. "The team will deliver X by Friday" — not "delivery of X is expected by Friday."
6. **Assertions, not hedges.** State what you believe to be true. If uncertainty exists, quantify it: "we have moderate confidence based on X" rather than "it seems possible that."

**NARRATE Step (validate — check against audit):**
- Does the rewrite resolve every Critical and High severity issue from the audit?
- Does the rewrite preserve the essential meaning and necessary caveats from the draft?
- Does the length match the channel requirement?
- Is the ask explicit?
- If any audit issue remains unresolved, revise before proceeding to Phase 4.

**Output:**
```
REWRITE v1
[The rewritten text]

---
Audit resolution:
- [Issue #1]: Resolved — [how]
- [Issue #2]: Resolved — [how]
- [Issue #N]: [Note if any issue required a judgment call to preserve a caveat]
Word count: [N] (target: [N])
```

---

### Phase 4: CALIBRATE TONE
**Entropy Level:** E3 – Analytical
**Control Mode:** NARRATE

Apply audience-specific calibration. A technically correct rewrite in the wrong register still lands wrong. This phase adjusts for the specific executive's communication style, organizational context, and relationship dynamics.

**Process:**
1. Assess executive communication style from `{{KNOWN_PREFERENCES}}` and `{{AUDIENCE}}` context:
   - **Data-first** (wants numbers before narrative): Lead with the metric, then the story.
   - **Narrative-first** (wants the situation before the data): Lead with the decision frame, then the evidence.
   - **Direct** (short sentences, no softening): Match that register; no "I think," no "perhaps."
   - **Collaborative** (consensus-seeking, inclusive language): Reflect shared ownership where appropriate without diffusing accountability.
2. Adjust for sensitivity level (`{{SENSITIVITY_LEVEL}}`). Restricted or sensitive communications may require more careful framing of uncertainty or personnel-related content.
3. Apply any hard constraints from `{{CONSTRAINTS}}`: word limits, topics not to address, required inclusions.
4. Check that the tone is appropriate for the relationship dynamic: peer-to-peer, subordinate-to-leader, expert advisory. The wrong dynamic register is as damaging as the wrong structure.
5. Produce the tone-calibrated rewrite. Note what was changed from v1 and why.

**Output:**
```
REWRITE v2 (tone-calibrated)
[The tone-adjusted text]

---
Calibration applied:
- Style: [data-first / narrative-first / direct / collaborative — which and why]
- Adjustments from v1: [specific changes + rationale]
- Constraints applied: [any hard constraints from {{CONSTRAINTS}}]
```

---

### Phase 5: PRODUCE VARIANTS
**Entropy Level:** E4 → E1
**Control Mode:** GENERATE → DELEGATE

Produce 2-3 channel-specific variants of the calibrated rewrite. Different channels have fundamentally different requirements: an email and a verbal briefing of the same content require different structures, different lengths, and different relationships between the headline and the supporting detail. GENERATE creates each variant for its channel; DELEGATE formats, labels, and packages them for delivery.

**GENERATE Step (create variants):**

Determine which channels to produce based on `{{CHANNEL}}` and use case. Always produce the primary channel as Variant 1. Select 1-2 additional variants from:

- **Email variant:** BLUF subject line + 100-150 word body. Subject line is the bottom line, not a topic label.
- **Verbal briefing variant:** 90-second spoken structure. Open with the bottom line, one context sentence, key data point, ask, offer to discuss. Written as the words to be spoken aloud.
- **One-pager variant:** Titled section headers. Decision/recommendation first. Context second. Data third. Next steps fourth. Total: 300-350 words.
- **Deck slide variant:** Single-sentence headline (the finding or recommendation), 3 supporting bullets (evidence), one call-to-action sentence at the bottom.
- **Memo variant:** Formal structure: To/From/Date/Re header, executive summary paragraph (50 words max), supporting sections.

**DELEGATE Step (format and label):**
1. Label each variant: "Variant 1: [Channel] — [Use case]"
2. Include a one-line use case description for each variant.
3. Assemble in a clean, copy-paste-ready format.

**Output:**
```
---
VARIANT 1: EMAIL
Use case: [when to use this version]

Subject: [Bottom-line subject line]

[Email body — max 150 words]

---
VARIANT 2: VERBAL BRIEFING
Use case: [when to use this version]

[Spoken text — structured for 90-second delivery]

---
VARIANT 3: [THIRD CHANNEL]
Use case: [when to use this version]

[Channel-appropriate content]
```

---

## 🚫 Anti-Patterns

| ✗ Wrong | ✓ Right |
|---------|---------|
| Rewriting without reading the draft carefully first | Run the full audit (Phase 2) before touching a single word; the rewrite is only as good as the diagnostic |
| Producing a generic "professional rewrite" that ignores the specific executive | Always calibrate to `{{AUDIENCE}}` — data-first exec needs numbers in line 1, not narrative |
| Keeping the original structure and only improving sentences | BLUF requires structural reorganization — the ask moves to line 1 even if the draft buries it in paragraph 4 |
| Cutting all qualifications for brevity | Brevity does not mean oversimplification; if a caveat changes the meaning of the decision, it survives the cut |
| Producing a single rewrite without variants | Always produce 2-3 channel-specific versions; the right words in the wrong format land wrong |
| Softening an assertion because it feels uncomfortable | An executive rewrite preserves honest assessments; do not hedge a direct finding into vagueness |
| Writing for the writer's comfort instead of the reader's action | Every sentence earns its place by helping the executive take the required action faster |

---

## 💡 Example Applications

| Use Case | Input | Output |
|----------|-------|--------|
| Long email with buried ask | 500-word email; ask appears in paragraph 4; passive voice throughout; no subject line signal | 3 variants: 90-word BLUF email with active subject line, 90-second verbal, one-pager with recommendation first |
| Deck slide overloaded with bullets | Slide with 8 bullets, no clear headline, data buried in bullet 6 | Rewritten as single-sentence finding headline + 3 supporting data points + one CTA; visual hierarchy restored |
| Passive-voice status update | "It has been determined that delays were encountered..." — no owner, no date, no ask | "The [team] will deliver [X] by [date]. [One-sentence reason for delay.] No action required from you." — owner, date, clear non-ask |
| Data dump masquerading as a recommendation memo | 800-word memo that presents all data before any recommendation; executive must infer the ask | Rewritten as recommendation-first memo: recommendation in sentence 1, three supporting data points, implications, specific ask |
| Sensitive personnel communication | Draft discussing performance concerns; hedging language; passive constructions protect no one | Calibrated rewrite: direct, active, factual framing; sensitive tone appropriate to personnel context; clear next step with explicit owner |

---

## 🖥️ Platform Notes

**CLI:** Invoke with `/skill executive-rewrite`. Pass `{{DRAFT}}` as input along with audience and channel context. Output is copy-paste-ready Markdown variants.

**Web:** Paste SKILL.md as system context. Provide the draft text and audience/channel variables in the first message. Work through phases interactively if clarification is needed on `{{KNOWN_PREFERENCES}}`.

**IDE:** Reference in agent configuration for communications workflows. Pairs effectively with decision-memo-distiller as a downstream polishing step after a memo has been structured.

**Any LLM:** Copy SKILL.md contents into context. Provide draft and intake variables. The phase structure works across all instruction-following models; Sonnet is recommended for Phase 2 (audit) and Phase 3 (rewrite) where judgment quality materially affects output.

---

## 📋 Compliance

**AI Governance Alignment:** Rewrites preserve the factual content and intent of the original draft. The skill does not alter the substance of assertions, change ownership attribution, or introduce unsupported claims. All changes are structural and tonal. If the original draft contains inaccuracies, those are flagged in the audit — not silently corrected.

**PII Risk Level:** low — the skill processes draft text that may contain names and roles. If `{{DRAFT}}` contains sensitive personnel information, employee identifiers, or confidential business data, do not paste into a public LLM interface. Use a private or enterprise deployment.

**Model Recommendation:** sonnet — Phase 2 (audit) and Phase 3 (rewrite) require strong reasoning to identify structural problems and produce genuinely better prose, not just shorter prose. Haiku produces adequate Phase 1 output but under-performs on the diagnostic and creative rewrite phases.

**Data Handling:** Processes draft text and contextual metadata. Output is a set of Markdown-formatted communication variants. No draft content is stored or transmitted beyond the active session. Handle `{{DRAFT}}` content according to its stated `{{SENSITIVITY_LEVEL}}`.
