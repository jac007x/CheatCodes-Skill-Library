---
name: adaptive-workflow-architect
description: "Designs AI agent workflows using Adaptive Narrative Control Theory (ANCT) — an entropy-aware architecture engine that maps workflow phases to cognitive control modes (delegate, narrate, generate), builds pipelines that know when to expand and when to compress, and produces skills that match their control strategy to the uncertainty level of each phase."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - meta-skill
  - workflow-design
  - entropy-management
  - cognitive-architecture
  - skill-architecture
  - cross-platform
---

# 🧠 Adaptive Workflow Architect

A meta-skill that designs AI agent workflows grounded in **Adaptive Narrative
Control Theory (ANCT)** — the principle that optimal systems (cognitive or
computational) manage uncertainty by dynamically shifting between three control
modes: delegation, narration, and generation.

Most workflows are designed linearly: step 1, step 2, step 3. They don't
account for the fact that different phases of a workflow operate under
fundamentally different levels of uncertainty — and need fundamentally
different control strategies.

**This skill fixes that.**

It takes a workflow goal and produces an entropy-aware architecture where
every phase knows:
- What control mode it operates in
- Why that mode was chosen
- When to escalate to a higher-entropy mode
- When to compress back down
- What failure looks like if the mode is wrong

---

## 🔬 Theoretical Foundation: ANCT in 60 Seconds

### The Core Insight

Any system processing information — a human brain, an AI agent, a multi-phase
workflow — faces a continuous problem: **how much uncertainty to allow at any
given moment.**

Too little uncertainty → rigid, brittle, unable to adapt
Too much uncertainty → chaotic, incoherent, unable to converge

The solution is not a fixed strategy. It is **mode-switching** — dynamically
selecting a control architecture that matches the current entropy level.

### The Three Control Modes

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  MODE 1: DELEGATE              Low entropy, high efficiency     │
│  ┌─────────────────┐                                            │
│  │ Offload to rules │  "Follow the pattern. Don't deviate."    │
│  │ SOPs, templates  │  Fast. Predictable. Zero ambiguity.      │
│  │ Known solutions  │  Breaks when the pattern doesn't fit.    │
│  └─────────────────┘                                            │
│          │                                                       │
│          ▼  uncertainty rises                                    │
│                                                                  │
│  MODE 2: NARRATE              Medium entropy, coherence         │
│  ┌─────────────────┐                                            │
│  │ Construct story  │  "Here's what's happening and why."      │
│  │ Interpret, plan  │  Resolves competing inputs into a        │
│  │ Synthesize       │  coherent direction. Identity-forming.   │
│  └─────────────────┘                                            │
│          │                                                       │
│          ▼  uncertainty rises further                            │
│                                                                  │
│  MODE 3: GENERATE             High entropy, expansion           │
│  ┌─────────────────┐                                            │
│  │ Multiple models  │  "What if? What else? What's missing?"   │
│  │ Diverge, explore │  Temporarily increases uncertainty to    │
│  │ Create options   │  discover what the other modes can't.    │
│  └─────────────────┘                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The Control Loop

Every phase in a well-designed workflow runs this loop:

```
1. DETECT  → What is the entropy level of this phase?
2. SELECT  → Which control mode matches?
3. EXECUTE → Apply the mode
4. ASSESS  → Did entropy move in the right direction?
   ├─ Too high → shift toward structure (delegate/narrate)
   └─ Too low  → shift toward exploration (narrate/generate)
```

### Why This Matters for Workflow Design

Most AI workflows fail in predictable ways that map directly to ANCT failure modes:

| Failure | ANCT Diagnosis | What Went Wrong |
|---------|---------------|-----------------|
| Output is generic, obvious | Stuck in DELEGATE | Never entered GENERATE mode; no exploration |
| Output is creative but incoherent | Stuck in GENERATE | Never compressed back through NARRATE |
| Agent goes in circles | Mode rigidity | Can't switch strategies when one isn't working |
| User abandons mid-workflow | Wrong mode for the phase | High-uncertainty phase using DELEGATE (too rigid) |
| Agent produces volume, not insight | GENERATE without NARRATE compression | Expansion without synthesis |

---

## 🚀 When to Use This Skill

Activate when you need to:
- **Design a new multi-phase AI workflow** and want it to handle uncertainty intelligently
- **Diagnose why an existing workflow fails** at specific phases
- **Architect a skill** for the CheatCodes library with proper entropy management
- **Build a creative pipeline** that knows when to expand and when to converge
- **Design a decision-support system** that matches its approach to the user's uncertainty

---

## 🏗️ The 5-Phase Architecture Process

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: GOAL DECOMPOSITION                             │
│     What is the workflow trying to achieve?               │
│     What are the sub-problems?                            │
│                                                           │
│  Phase 2: ENTROPY MAPPING                                │
│     For each sub-problem: how uncertain is it?            │
│     What is known vs unknown vs unknowable?               │
│                                                           │
│  Phase 3: MODE ASSIGNMENT                                │
│     Match each phase to a control mode                    │
│     Design the transitions between modes                  │
│                                                           │
│  Phase 4: FAILURE MODE ANALYSIS                          │
│     What breaks if the wrong mode is used?                │
│     Build escape hatches and mode-switch triggers         │
│                                                           │
│  Phase 5: ARCHITECTURE OUTPUT                            │
│     Produce the workflow blueprint                        │
│     Map to SKILL.md structure if building a skill         │
└─────────────────────────────────────────────────────────┘
```

---

### Phase 1: GOAL DECOMPOSITION

**Control Mode: NARRATE** (medium entropy — we're organizing, not exploring)

**Goal:** Break the workflow objective into sub-problems, each of which
can be independently assessed for entropy.

#### Intake Questions

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| `{{WORKFLOW_GOAL}}` | What should this workflow accomplish? | string | Yes |
| `{{DOMAIN}}` | What domain does this operate in? | string | Yes |
| `{{USER_PROFILE}}` | Who runs this workflow? What's their expertise level? | string | Yes |
| `{{KNOWN_CONSTRAINTS}}` | What's already decided? (tools, platforms, formats) | list | No |
| `{{EXISTING_WORKFLOW}}` | Is there a current workflow to improve? | text | No |

#### Decomposition Method

For the stated goal, identify:

1. **Input acquisition** — Where does data/context come from?
2. **Transformation steps** — What changes between input and output?
3. **Decision points** — Where must a choice be made?
4. **Synthesis steps** — Where are multiple inputs combined?
5. **Output production** — What is the deliverable?

For each identified step, note:
- What is **known** before this step begins?
- What is **unknown** and must be discovered during this step?
- What is **unknowable** and requires generation/creativity?

---

### Phase 2: ENTROPY MAPPING

**Control Mode: NARRATE → GENERATE** (we may need to explore uncertainty
we didn't initially see)

**Goal:** Assign an entropy level to each sub-problem from Phase 1.

#### Entropy Classification

| Level | Signal | Description | Example |
|-------|--------|-------------|---------|
| **E1: Deterministic** | Known inputs, known transform, known output | Template filling, format conversion, lookup | "Convert CSV to JSON" |
| **E2: Procedural** | Known process, variable inputs | The steps are known but the data varies each time | "Run the same 5 SQL queries against new data" |
| **E3: Analytical** | Known goal, multiple valid approaches | Requires interpretation, judgment, weighting | "Analyze survey results for themes" |
| **E4: Creative** | Known domain, unknown output shape | Must generate options that don't yet exist | "Design a visualization that tells this story" |
| **E5: Exploratory** | Uncertain goal, unknown domain boundaries | The problem itself is unclear; must discover what to solve | "What should our strategy be?" |

#### Entropy Map Output

Produce a table:

```markdown
| Phase | Sub-Problem | Entropy Level | Known | Unknown | Unknowable |
|-------|-------------|---------------|-------|---------|------------|
| 1     | ...         | E2            | ...   | ...     | ...        |
| 2     | ...         | E4            | ...   | ...     | ...        |
| 3     | ...         | E1            | ...   | ...     | ...        |
```

---

### Phase 3: MODE ASSIGNMENT

**Control Mode: NARRATE** (we're making architectural decisions — organizing)

**Goal:** Assign a control mode to each phase and design the transitions.

#### Mode Selection Rules

| Entropy Level | Primary Mode | Secondary Mode | Rationale |
|--------------|-------------|----------------|-----------|
| **E1: Deterministic** | DELEGATE | — | Known pattern. Execute it. No judgment needed. |
| **E2: Procedural** | DELEGATE | NARRATE (on exception) | Follow process. Escalate to narrative if something unexpected appears. |
| **E3: Analytical** | NARRATE | GENERATE (if stuck) | Construct interpretation. If analysis stalls, expand to multi-model thinking. |
| **E4: Creative** | GENERATE → NARRATE | — | Diverge first (options), then converge (select and justify). Always ends in compression. |
| **E5: Exploratory** | GENERATE → NARRATE → GENERATE | DELEGATE (to test) | Cycle: explore → frame → explore deeper → validate with a concrete test. |

#### Transition Design

For each mode boundary in the workflow, define:

1. **Entry condition** — What triggers entering this mode?
2. **Exit condition** — What signals this mode is done?
3. **Escalation trigger** — What happens if this mode isn't working?
4. **Compression checkpoint** — How is output from GENERATE compressed before the next phase?

**Critical Rule:**

> **Every GENERATE phase must be followed by a NARRATE compression step.**
> Expansion without compression produces volume, not value.

#### Mode Architecture Output

```markdown
| Phase | Mode | Entry Condition | Exit Condition | Escalation | Compression |
|-------|------|-----------------|----------------|------------|-------------|
| 1     | DELEGATE | Data available | Data loaded + validated | → NARRATE if schema mismatch | N/A |
| 2     | GENERATE | Analysis goal stated | 3+ distinct options produced | → time-box after N minutes | NARRATE: select top 2 with rationale |
| 3     | NARRATE | Options available | Coherent recommendation formed | → GENERATE if all options rejected | N/A (already in compression) |
```

---

### Phase 4: FAILURE MODE ANALYSIS

**Control Mode: GENERATE** (we're deliberately exploring what could go wrong)

**Goal:** For each phase, identify what breaks if the wrong control mode is used.

#### ANCT Failure Modes Applied to Workflows

| Failure Mode | What It Looks Like | Root Cause | Fix |
|-------------|-------------------|------------|-----|
| **Over-Delegation** | Rigid output that misses nuance. Agent follows template even when it doesn't fit. | DELEGATE mode applied to E3+ entropy | Add entropy check: "Does this template fit the data? If not, escalate to NARRATE" |
| **Narrative Lock** | Agent commits to first interpretation and defends it against evidence. Self-reinforcing analysis. | NARRATE mode without GENERATE exploration first | Force a divergence step before analysis: "Generate 3 alternative interpretations before selecting one" |
| **Generative Overflow** | Agent produces 15 options, 8 frameworks, 4 analogies — but no conclusion. Creative but incoherent. | GENERATE mode without NARRATE compression | Add mandatory compression checkpoint: "Select the top 2 and state why in one sentence each" |
| **Mode Rigidity** | Agent uses the same approach regardless of phase. One-note workflow. | No mode-switching logic | Build explicit mode transitions with entry/exit conditions |
| **Premature Compression** | Agent jumps to a conclusion before exploring the problem space. First answer, not best answer. | NARRATE applied to E4/E5 entropy | Add an expansion gate: "Before concluding, generate at least 3 alternative approaches" |
| **Entropy Avoidance** | Agent reduces everything to simple templates. Loses complexity that matters. | DELEGATE applied to everything | Entropy mapping step forces honest assessment of what's actually uncertain |

#### Escape Hatches

For each phase, define a fallback:

```markdown
If Phase N is stuck for > [threshold]:
  → Current mode: DELEGATE? Escalate to NARRATE.
  → Current mode: NARRATE? Escalate to GENERATE.
  → Current mode: GENERATE? Force compression to NARRATE.
```

---

### Phase 5: ARCHITECTURE OUTPUT

**Control Mode: DELEGATE** (we're producing a structured document from
established patterns — this is template work)

**Goal:** Produce the final workflow architecture.

#### Output Format A: Workflow Blueprint

For any workflow design:

```markdown
# Workflow: {{WORKFLOW_NAME}}

## Goal
One sentence.

## Entropy Profile
Overall: E[level] — [description]

## Architecture

| Phase | Name | Mode | Entropy | Entry | Exit | Escalation |
|-------|------|------|---------|-------|------|------------|
| 1 | ... | DELEGATE | E1 | ... | ... | → NARRATE |
| 2 | ... | GENERATE | E4 | ... | ... | time-box |
| 3 | ... | NARRATE | E3 | ... | ... | → GENERATE |

## Mode Transitions
[Diagram showing flow between phases with mode labels]

## Failure Modes
[Table from Phase 4]

## Compression Checkpoints
[Where GENERATE output is compressed before next phase]
```

#### Output Format B: SKILL.md Blueprint

When the workflow is being designed as a skill for the CheatCodes library:

```markdown
# Skill: {{SKILL_NAME}}

## Phase-to-Mode Mapping

| SKILL.md Phase | ANCT Mode | Why |
|---------------|-----------|-----|
| Intake | DELEGATE | Known questions, known format. Collect variables. |
| Analysis | NARRATE → GENERATE | Interpret data (narrate), then explore alternatives (generate) |
| Synthesis | GENERATE → NARRATE | Produce options (generate), then compress to recommendation (narrate) |
| Output | DELEGATE | Known format. Produce deliverable. |

## Built-In Entropy Checks
- Phase 2 includes: "Before proceeding, rate your confidence in this analysis (high/medium/low)"
  - If low → escalate to GENERATE mode: "Generate 3 alternative interpretations"
- Phase 3 includes: mandatory compression checkpoint after every divergent step

## Anti-Patterns (from ANCT Failure Modes)
- [ ] No GENERATE phase without a following NARRATE compression
- [ ] No DELEGATE phase for E3+ entropy sub-problems
- [ ] No NARRATE phase without considering alternatives first
```

---

## 🔄 The Creativity Cycle (Special Case)

When designing creative workflows, ANCT prescribes a specific oscillation:

```
1. DESTABILIZE (GENERATE)
   → Increase entropy intentionally
   → Multiple competing models
   → "What if? What else? What's weird?"

2. EXPLORE (GENERATE, sustained)
   → Hold the uncertainty open
   → Resist premature convergence
   → "Stay with it. Three more options."

3. COMPRESS (NARRATE)
   → Select from the expanded field
   → Justify the selection
   → "This one, because..."

4. STABILIZE (DELEGATE)
   → Execute the selected direction
   → Apply known patterns to produce output
   → "Now build it."
```

**This cycle can repeat within a single workflow.** A data visualization skill
might run: DELEGATE (load data) → GENERATE (explore chart types) → NARRATE
(select best chart) → DELEGATE (produce chart) → GENERATE (explore layout
options) → NARRATE (select layout) → DELEGATE (export final).

---

## 📊 Entropy Signatures for Common Workflow Types

These are pre-mapped entropy profiles for common skill categories.
Use as starting points, then adjust per Phase 2.

| Workflow Type | Typical Entropy Signature | Mode Pattern |
|--------------|--------------------------|--------------|
| **Data pipeline** | E1 → E2 → E1 | D → D → D (mostly delegation, low entropy throughout) |
| **Report generation** | E2 → E3 → E2 → E1 | D → N → N → D (narration for analysis, delegation for output) |
| **Creative design** | E2 → E4 → E3 → E1 | D → G→N → N → D (generate options, compress, produce) |
| **Strategic analysis** | E3 → E5 → E4 → E3 → E1 | N → G→N→G → G→N → N → D (heavy cycling) |
| **NLP/text analysis** | E2 → E3 → E4 → E3 → E1 | D → N → G→N → N → D (generate interpretations, compress) |
| **QA/validation** | E1 → E2 → E3 → E1 | D → D → N → D (mostly rules, narrate for edge cases) |
| **Onboarding/training** | E2 → E3 → E2 | D → N → D (narrate for context, delegate for action items) |

---

## ⚠️ Anti-Patterns

```
WORKFLOW DESIGN ANTI-PATTERNS:

✗ "All DELEGATE" pipeline
  Every phase follows a template. No room for uncertainty.
  → Produces rigid, generic output that misses context.

✗ "All GENERATE" exploration
  Every phase diverges. Nothing converges.
  → Produces volume without direction. User drowns in options.

✗ "GENERATE without NARRATE exit"
  Expansion phase with no compression checkpoint.
  → The most common failure in creative AI workflows.

✗ "NARRATE before GENERATE"
  Interpreting/judging before exploring.
  → Locks into first hypothesis. Confirmation bias baked in.

✗ "Flat entropy assumption"
  Treating every phase as the same uncertainty level.
  → Over-engineers simple steps, under-engineers hard ones.

✗ "Missing escalation paths"
  No fallback when a mode isn't working.
  → Agent gets stuck; user intervenes or abandons.

CORRECT PATTERNS:

✓ GENERATE → NARRATE (expand then compress)
✓ Entropy level determines mode (not habit or convention)
✓ Every phase has an escalation trigger
✓ Compression checkpoints after every divergent phase
✓ Mode transitions are explicit, not accidental
```

---

## 📚 Example Applications

| Domain | Workflow Goal | Entropy Signature | Key ANCT Insight |
|--------|--------------|-------------------|------------------|
| **Survey analysis pipeline** | Extract themes from open-text responses | E2→E4→E3→E1 | Topic discovery is GENERATE (E4), not DELEGATE. Let models compete before selecting themes. |
| **Presentation builder** | Turn data into a narrative deck | E2→E3→E4→E2→E1 | Story angle is GENERATE. Slide layout is DELEGATE. Don't template the story. |
| **Code review assistant** | Review PR for quality and suggest improvements | E1→E3→E4→E3 | Lint rules are DELEGATE. Design feedback is NARRATE. Alternative approaches are GENERATE. |
| **Incident response** | Diagnose and remediate a production issue | E5→E3→E2→E1 | Starts exploratory (what's wrong?), compresses as diagnosis clarifies. Over-delegation here kills you. |
| **Hiring/talent evaluation** | Assess candidate fit across dimensions | E2→E3→E4→E3→E1 | Data collection is DELEGATE. Holistic assessment is NARRATE. "Who else could this person be?" is GENERATE. |
| **Knowledge synthesis** | Combine multiple sources into a coherent summary | E3→E4→E3→E1 | The synthesis step is GENERATE (what connections exist?), not NARRATE (don't interpret prematurely). |

---

## 🌐 Platform Notes

| Platform | How to Use |
|----------|------------|
| **Any LLM** | Paste this SKILL.md as context. Ask: "Design a workflow for [goal] using ANCT principles" |
| **Custom agents** | Load as instruction set for a workflow-design agent |
| **CLI tools** | Copy to skills directory; invoke with `/skill adaptive-workflow-architect` |
| **IDE extensions** | Reference in agent config for architectural design sessions |

---

## Compliance

- **PII Risk:** None. This skill designs workflows; it does not process data.
- **Model Recommendation:** Opus for full architectural design sessions (E5 exploratory
  work benefits from maximum reasoning depth). Sonnet for applying pre-mapped
  entropy signatures to known workflow types.
- **Human Oversight:** All architecture outputs are proposals. The human reviews
  the mode assignments, approves the entropy mapping, and validates the failure
  mode analysis before any workflow is built.

---

## Relationship to Other Meta-Skills

| Meta-Skill | Relationship |
|------------|-------------|
| **skill-suggestor** | Suggests *what* to build. Adaptive-workflow-architect designs *how* to build it. |
| **skill-universalizer** | Universalizes existing workflows. AWA can design the architecture *before* the workflow exists. |
| **skill-improver** | Improves skills after use. AWA failure mode analysis anticipates problems *before* use. |

> **skill-suggestor** finds the need → **adaptive-workflow-architect** designs the architecture → **skill-universalizer** codifies it → **skill-improver** refines it.
