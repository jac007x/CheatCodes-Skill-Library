---
name: skill-universalizer
description: "Meta-skill for extracting, universalizing, and codifying reusable workflows from completed agent sessions. Analyzes a team-specific workflow, strips specifics, identifies parameterizable gaps, builds an intake step, and outputs a cross-platform SKILL.md that works in code-puppy, wibey, Codex, or any LLM."
version: 1.1.0
author: jac007x
origin: created
maturity_status: beta
tags: [meta-skill, workflow-extraction, universalization, skill-building, cross-platform, human-in-the-loop, refinement]
model_recommendation: sonnet
risk_level: low
---

# 🧬 Skill Universalizer

A meta-skill that transforms any completed agent workflow into a reusable,
cross-platform skill. It extracts the universal pattern, strips team-specific
details, inserts parameterizable gaps, and builds an intake step for
customization.

**This is the tool that builds tools.**

---

## 🧠 Core Philosophy

- **Workflows are patterns with context holes** — remove the context, leave the holes labeled
- **Universalization ≠ generalization** — don't make it vague; make it specific-but-parameterized
- **Human context review is mandatory** — the agent proposes, the human validates
- **Intake is the product** — a skill without an intake step is just documentation
- **Platform-agnostic by default** — SKILL.md is plain Markdown; any agent can consume it

---

## 🚀 When to Use This Skill

Activate after any of these signals:
- You built a workflow that worked well and want to reuse it
- You notice yourself repeating the same multi-step process
- Someone on another team asks "how did you do that?"
- A workflow has been iterated 3+ times (it's stabilized)
- You want to share a capability across code-puppy, wibey, Codex, etc.

---

## 🏗️ The 6-Phase Universalization Process

```
┌───────────────────────────────────────────────────────┐
│  Phase 1: EXTRACT  →  Capture the raw workflow            │
│  Phase 2: DECOMPOSE →  Identify universal vs specific     │
│  Phase 3: CONTEXT REVIEW →  Human validates (mandatory)   │
│  Phase 4: PARAMETERIZE →  Create intake variables         │
│  Phase 5: CODIFY  →  Write the SKILL.md                   │
│  Phase 6: VALIDATE →  Test with a different context        │
└───────────────────────────────────────────────────────┘
```

---

### Phase 1: EXTRACT — Capture the Raw Workflow

**Goal:** Catalog everything the original workflow does.

**Inputs to analyze:**
- Agent conversation history (chat logs, session files)
- Generated code files (scripts, notebooks, configs)
- Output artifacts (reports, slides, dashboards, emails)
- External tools/APIs used
- Human decision points (where did the human intervene?)

**Produce a Workflow Manifest:**
```markdown
## Workflow Manifest
- **Name:** [descriptive name]
- **Trigger:** [what starts this workflow]
- **Steps:** [numbered list of n- **Inputs:** [files, data, credentials needed]
- **Outputs:** [what gets produced]
- **Tools used:** [agents, APIs, libraries]
- **Human touchpoints:** [where human judgment is needed]
- **Duration:** [how long it takes]
- **Frequency:** [how often it runs]
```

---

### Phase 2: DECOMPOSE — Separate Universal from Specific

**Goal:** Classify every element as universal, parameterizable, or discard.

**Classification Framework:**

| Category | Definition | Action |
|----------|-----------|--------|
| **Universal** | Same in every context | Keep as-is in skill |
| **Parameterizable** | Varies by context but follows a pattern | Create `{{VARIABLE}}` |
| **Team-specific** | Only applies to the original team | Strip from skill |
| **Incidental** | Artifact of how it was first built | Discard |

**Common Parameterizable Elements:**
- Data source paths/connections
- Column/field names in data schemas
- Org hierarchy dimensions
- Output file locations and formats
- Branding (colors, logos, team names)
- Notification recipients
- Thresholds and business rules
- API endpoints and auth methods

**Common Elements to Strip:**
- Hardcoded team names, leader names, org codes
- Specific file paths on someone's machine
- References to specific meetings or cadences
- Workarounds for bugs in specific tool versions
- Person-specific email templates

---

### Phase 3: CONTEXT REVIEW — Human Validates (Mandatory)

**This phase is non-negotiable.** The agent cannot universalize alone.

**Questions to Askhe Human:**

1. **"What is this workflow doing at the highest level?"**
   - Forces the human to articulate the pattern in plain language
   - Often reveals a simpler underlying pattern than what was implemented

2. **"Who else could benefit from this?"**
   - Maps the deployment ladder: team → org → company → industry
   - Identifies the right level of universalization

3. **"What would someone need to change to use this for their situation?"**
   - Directly identifies the parameterizable gaps
   - Human intuitively knows what's context-dependent

4. **"What's the 'golden path' vs. optional branches?"**
   - Identifies the core happy path vs. edge cases
   - Skills should nail the golden path; edge cases are documented but optional

5. **"What surprised you or went wrong when building this?"**
   - Anti-patterns and gotchas to include in the skill
   - These are often the most valuable parts of the skill

---

### Phase 4: PARAMETERIZE — Create the Intake Step

**Goal:** Define the `{{VARIABLES}}` that make the skill customizable.

**Intake Table Template:**
```markdown
## Intake: Customize This Skill

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{VAR_NAME}}` | What this controls | type | ✅/❌ | default |
```

**Variable Naming Conventions:**
- `SCREAMING_SNAKE_CASE` for all variables
- Prefix with domain: `DATA_`, `OUTPUT_`, `ORG_`, `AUTH_`
- Be descriptive: `{{DATA_SOURCE_PATH}}` not `{{PATH}}`
- Include type hints: `file-path`, `string`, `int`, `list`, `dict`, `choice`, `bool`

**The Intake Step is the Product:**
When someone activates this skill, the FIRST thing the agent does is
collect values for every required `{{VARIABLE}}` from the user.
This is the "customization gap" — the intentionally blank space that
makes the skill reusable.

---

### Phase 5: CODIFY — Write the SKILL.md

**Goal:** Produce the final, cross-platform skill file.

**Required SKILL.md Sections:**

```markdown
---
name: skill-name
description: "One-line description"
version: 1.0.0
author: author-id
tags: [tag1, tag2, tag3]
---

# Skill Name
One-paragraph description of what this skill does universally.

## Core Philosophy
Bullet list of principles that guide this skill's design.

## Intake: Customize This Skill
Variable table with all parameterizable gaps.

## Architecture
ASCII diagram of the pipeline/flow.

## Phase N: [Phase Name]
For each phase: Goal, Implementation, Validation, Anti-patterns.

## Bulletproofing Checklist
Things to verify before sharing the output.

## Example Applications
Table of 4-6 different contexts where this skill applies.

## Anti-Patterns
Common mistakes to avoid.

## Platform Notes
Table showing compatibility across platforms.

## Deployment Ladder
Refine → Prove → Scale stages with validation criteria.
```

**Quality Criteria:**
- [ ] No team-specific names, paths, or hardcoded values
- [ ] Every context-dependent element is a `{{VARIABLE}}`
- [ ] Intake table has sensible defaults where possible
- [ ] Code snippets use type hints, pathlib, dataclasses
- [ ] Anti-patterns section exists (learned from the original build)
- [ ] Example applications table has 4+ diverse use cases
- [ ] Platform notes confirm cross-platform compatibility
- [ ] File is under 600 lines

---

### Phase 6: VALIDATE — Test with a Different Context

**Goal:** Prove the skill works outside its original context.

**The "3 Context Test":**
- ✅ Original context (should work perfectly)
- ✅ Adjacent context (same domain, different team)
- ✅ Distant context (different domain entirely)

If any context reveals missing variables → iterate Phases 4-5.

---

## 💾 Output Structure

```
~/.code_puppy/skills/{{SKILL_NAME}}/
  SKILL.md        # The universal skill instructions
  skill.json      # Metadata (name, description, tags, version)
```

For cross-platform deployment:
```
# code-puppy (auto-detected)
~/.code_puppy/skills/{{SKILL_NAME}}/SKILL.md

# wibey
~/.wibey/skills/{{SKILL_NAME}}/SKILL.md

# Codex / Any LLM
Paste SKILL.md content as system prompt or conversation context
```

---

## ⚠️ Anti-Patterns for Skill Creation

```
❌ Making the skill too vague ("analyze data" is not a skill)
❌ Making the skill too specific (team names baked in)
❌ Skipping the human context review (Phase 3)
❌ Having zero anti-patterns section (you learned something, document it)
❌ Not including example applications (kills discoverability)
❌ Writing 1000+ line SKILL.md files (split into sub-skills)
❌ Using tool-specific syntax (keep it Markdown-first, code-second)
❌ Forgetting the intake step (a skill without customization is documentation)
```

---

## 📚 Example Universalizations

| Original Workflow | Universal Skill | Key Variables |
|-------------------|-----------------|---------------|
| AES comment analysis | survey-nlp-analyzer | corpus, text col, dimensions |
| Monthly HC reporting | org-data-pipeline | data source, metrics, cuts |
| Talent card generation | talent-card-generator | template, data, field map |
| Tech review cycle tracking | review-cycle-manager | platform, statuses, roster |
| Design QA pipeline | multi-skill-qa-orchestrator | skills, phases, thresholds |
| MBR slide creation | data-story-deck-builder | data, template, audience |

---

## 🧪 Phase 6.5: Test Cases (NEW in v1.1.0)

**Goal:** Before finalizing the skill, validate that the produced SKILL.md actually works across at least two different contexts.

The 3 Context Test from Phase 6 is necessary but not sufficient. This phase adds structured test cases that must be documented in the skill itself.

### Minimum Viable Test Suite

Every universalized skill must include at least 3 test cases in its `## Example Applications` table. Each test case must specify:

| Field | Description |
|-------|-------------|
| **Context** | Who is using it and for what purpose |
| **Inputs** | What variables are set and to what values |
| **Expected Output** | What the skill should produce |
| **Success Condition** | How you'd know the output is correct |
| **Failure Condition** | What would indicate the skill needs refinement |

### Test Case Template

```markdown
### Test Case: [Name]

**Context:** [Who is using this and what they're trying to do]

**Inputs:**
- `{{VAR_1}}` = [value]
- `{{VAR_2}}` = [value]

**Expected Output:**
[Description of what should be produced]

**Success Condition:**
[How a human would confirm the output is correct without seeing the original workflow]

**Failure Condition (skill needs refinement if):**
- [Condition 1 that would indicate the skill is too specific]
- [Condition 2 that would indicate missing parameterization]
```

### Validation Gate

Before marking the skill as `maturity_status: beta` or higher, all 3 test cases must pass. A test case passes when:
1. A human unfamiliar with the original workflow can run the skill using only the SKILL.md
2. The output is meaningfully useful (not generic advice)
3. No team-specific references or hardcoded values leak into the output

---

## 🚨 Exception Handling Guide (NEW in v1.1.0)

**Goal:** Document what to do when Phase 2 (DECOMPOSE) or Phase 3 (CONTEXT REVIEW) reveals that the workflow cannot be universalized as-is.

### Exception: The Workflow Is Too Specific

**Signal:** > 60% of elements classify as "team-specific" or "incidental" in Phase 2.

**Response:**
1. Ask the human: "Is there a higher-level pattern here that could generalize?"
2. If yes: Elevate the abstraction level. Document the higher-level pattern instead of the implementation details.
3. If no: Document as a *reference workflow* rather than a reusable skill. A reference workflow is a case study, not a parameterized skill.

**Do not force universalization** on workflows that are fundamentally one-off solutions.

### Exception: The Workflow Has Too Many Branches

**Signal:** Phase 2 identifies 5+ distinct decision paths, each with different tools, inputs, or outputs.

**Response:**
1. Identify the "golden path" (the most common successful execution).
2. Universalize the golden path only.
3. Document edge cases in an `## Edge Cases` section, not as core phases.
4. Optional: Split into sub-skills if the branches are large enough to stand alone.

### Exception: The Human Can't Articulate the Universal Pattern

**Signal:** Phase 3 Context Review — the human can describe what they did but cannot state what it does at a higher level.

**Response:**
1. Offer 3 candidate abstractions and ask which fits best.
2. Run a "5 Whys" on the workflow trigger: "Why do you do this? And why does that matter? And why does that matter?"
3. If still unclear after two attempts: record the workflow as-is, mark as `maturity_status: draft`, and return to universalization after the workflow has been run 2+ more times.

### Exception: Required Variables Have No Sensible Defaults

**Signal:** Phase 4 — more than 50% of variables have no possible default and are highly context-specific (e.g., org-specific business rules, legal thresholds).

**Response:**
1. Distinguish between *configuration* variables (set once per deployment) and *execution* variables (set each run).
2. Move configuration variables to a `## Configuration` section with deployment instructions.
3. Execution variables remain in the standard intake step.
4. Document that this skill requires a one-time setup before it can be used.

### Exception: Output Quality Is Context-Dependent

**Signal:** Phase 6 3 Context Test — the skill produces good output in the original context but weak output in distant contexts.

**Response:**
1. The skill is *partially universal*, not fully. That's acceptable.
2. Document the known-good contexts in `## Example Applications` and note the limitations.
3. Add a scope statement at the top of the skill: "Best suited for [context type]."
4. Do not claim universality that doesn't exist.

---

## 🌐 Platform Notes

| Platform | Compatible | Notes |
|----------|-----------|-------|
| code-puppy | ✅ | `/skill skill-universalizer` |
| wibey | ✅ | Copy to `~/.wibey/skills/` |
| Codex | ✅ | Paste as system prompt |
| Any LLM | ✅ | Plain Markdown context |
