---
name: skill-suggestor
description: "Meta-skill that detects when a repeating workflow pattern should become a reusable skill. Operates in two modes: passive observation during any session (detects repetition, manual multi-step patterns, and 'I wish I had a skill for this' moments) and on-demand invocation when you know you want to capture something. Produces structured skill proposals that feed directly into skill-universalizer."
version: 1.0.0
author: jac007x
origin: created
maturity_status: beta
tags:
  - meta-skill
  - skill-discovery
  - pattern-detection
  - workflow-capture
  - passive-observation
  - cross-platform
---

# 💡 Skill Suggestor

The third meta-skill. If **skill-universalizer** creates skills and
**skill-improver** makes them better, then **skill-suggestor** is the one
that notices you need a skill in the first place.

It operates in two modes:
- **Passive:** Always listening during any session, detecting repetition and manual labor patterns
- **On-demand:** Invoked explicitly when you think "this should be a skill"

**The best skill ideas come from friction you didn't consciously notice.**

---

## 🧠 Core Philosophy

- **Repetition is the signal** — if you did it twice manually, the third time should be a skill
- **The user doesn't always know they need a skill** — that's what passive mode is for
- **Proposals, not interruptions** — passive mode never breaks the user's flow; it queues proposals for later
- **Low threshold, high signal** — suggest early, validate later; a rejected proposal costs nothing
- **Feed the pipeline** — every accepted proposal flows into skill-universalizer automatically
- **On-demand is a conversation** — when invoked explicitly, the suggestor interviews you to extract the pattern

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   SKILL SUGGESTOR                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  MODE 1: PASSIVE (always on during sessions)             │
│  ┌────────────────────────────────────────────┐          │
│  │  Pattern Detectors                          │         │
│  │  • Repetition detector (same steps again)  │         │
│  │  • Manual labor detector (tedious patterns)│         │
│  │  • Wish detector ("I wish...", "every      │         │
│  │    time...", "again?")                      │         │
│  │  • Cross-session detector (same workflow    │         │
│  │    across different sessions)               │         │
│  └─────────────┬──────────────────────────────┘          │
│                │ trigger                                  │
│                ▼                                          │
│  ┌────────────────────────────────────────────┐          │
│  │  Proposal Queue (private repo)              │         │
│  │  proposals/{date}-{pattern-name}.md          │         │
│  └────────────────────────────────────────────┘          │
│                                                          │
│  MODE 2: ON-DEMAND (explicitly invoked)                  │
│  ┌────────────────────────────────────────────┐          │
│  │  Skill Interview                            │         │
│  │  • What are you doing?                      │         │
│  │  • How often?                               │         │
│  │  • What varies each time?                   │         │
│  │  • What stays the same?                     │         │
│  │  • Who else does this?                      │         │
│  └─────────────┬──────────────────────────────┘          │
│                │                                          │
│                ▼                                          │
│  ┌────────────────────────────────────────────┐          │
│  │  Skill Proposal (structured output)         │         │
│  │  → ready for skill-universalizer            │         │
│  └────────────────────────────────────────────┘          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Mode 1: Passive Detection

### How It Works

The passive layer runs inside every session, alongside skill-improver's
observation layer. While skill-improver watches for *friction in existing
skills*, skill-suggestor watches for *workflows that aren't skills yet*.

**It never interrupts.** It never asks "would you like to make this a skill?"
mid-session. It silently logs detection signals to the proposal queue in your
private repo. You review proposals on your own schedule.

### Detection Triggers

#### 1. Repetition Detector

Fires when the agent recognizes it's performing the same multi-step pattern
it has performed before — either in the current session or across sessions.

**Signals:**
- Same sequence of tool calls (read → transform → write → format) repeated 2+ times
- User provides the same type of instructions across sessions
  ("pull the data from X, slice by Y, build a chart")
- Copy-paste patterns: user pastes a previous output as a template for new work

**Threshold:** 2 repetitions in a single session OR 3 similar workflows across sessions

#### 2. Manual Labor Detector

Fires when the session involves tedious, mechanical work that follows a
predictable pattern.

**Signals:**
- Batch processing: user feeds items one at a time through the same transformation
- Format conversion: repeated "take X and make it Y" instructions
- Data wrangling: same column renames, same filter criteria, same aggregation pattern
- Template filling: "do the same thing but for [different input]" repeatedly

**Threshold:** 4+ instances of the same mechanical operation

#### 3. Wish Detector

Fires when the user's language reveals a latent skill need — even if they
don't explicitly ask for one.

**Language patterns:**
```
"I wish I could just..."       → user wants automation
"every time I have to..."      → user recognizes repetition
"this is tedious"              → user recognizes manual labor
"is there a faster way to..."  → user wants a shortcut
"I do this every [week/month]" → user recognizes cadence
"again?"                       → user frustrated by repetition
"same thing but for..."        → parameterization opportunity
"can you remember how we..."   → cross-session pattern
```

**Threshold:** 1 strong signal OR 2 weak signals in the same session

#### 4. Cross-Session Detector

Fires when patterns are detected across multiple sessions over time.
This is the most valuable detector because it catches workflows the
user considers "normal" — they don't realize it's a repeatable pattern
because they've always done it manually.

**Signals:**
- Same starting prompt structure across sessions
- Same tool usage patterns (even with different data)
- Same output format requested repeatedly
- Same error recovery pattern ("no, I meant X not Y" — same correction every time)

**Threshold:** 3 similar sessions within a 14-day window

### Passive Signal Log Format

Signals are logged to your **private repo only** at `signals/skill-suggestions.jsonl`:

```jsonl
{"timestamp": "2026-03-23T14:30:00Z", "detector": "repetition", "confidence": 0.85, "pattern_name": "data-slice-and-chart", "evidence": "Same 5-step sequence detected 3x across sessions", "suggested_intake_vars": ["DATA_SOURCE", "SLICE_DIMENSIONS", "CHART_TYPE"], "session_id": "abc123"}
```

**These logs never appear in the public repo.**

---

## Mode 2: On-Demand Invocation

### When to Use

Activate skill-suggestor directly when:
- You just finished a workflow and think "this should be reusable"
- You're about to start something you've done before and want to capture it first
- Someone asks you "how did you do that?" and you want to package the answer
- You're reviewing your proposal queue and want to flesh out a passive detection

### The Skill Interview (5 Questions)

When invoked on-demand, the suggestor conducts a structured interview to
extract the skill pattern. These five questions are designed to produce
everything skill-universalizer needs as input.

---

#### Question 1: "What are you doing?"

**Goal:** Name and describe the workflow in plain language.

**Follow-ups:**
- "What triggers this workflow? What makes you start it?"
- "What does 'done' look like? What's the output?"
- "Is there a name you'd give this if it were a tool?"

**What this produces:** Skill name, one-line description, trigger conditions, output specification.

---

#### Question 2: "How often do you do this?"

**Goal:** Establish frequency and cadence to validate skill-worthiness.

**Follow-ups:**
- "Is it on a schedule (daily/weekly/monthly) or event-driven?"
- "How long does it take each time?"
- "What happens if you don't do it? What breaks?"

**What this produces:** Frequency assessment, business criticality, time-saved-per-use estimate.

**Skill-worthiness rubric:**

| Frequency | Time per run | Verdict |
|-----------|-------------|---------|
| Daily | Any | Definitely a skill |
| Weekly | > 15 min | Definitely a skill |
| Weekly | < 15 min | Probably a skill |
| Monthly | > 30 min | Probably a skill |
| Monthly | < 30 min | Maybe (depends on complexity) |
| Quarterly+ | > 1 hour | Probably a skill (complex enough to forget between runs) |
| One-time | Any | Not a skill (unless others do it too) |

---

#### Question 3: "What varies each time?"

**Goal:** Identify the `{{INTAKE_VARIABLES}}` — the parameterizable gaps.

**Follow-ups:**
- "What inputs change between runs?"
- "What decisions do you make differently each time?"
- "Are there options or branches — 'sometimes I do A, sometimes B'?"

**What this produces:** Draft intake variable table with types and defaults.

---

#### Question 4: "What stays the same?"

**Goal:** Identify the universal logic — the invariant core of the skill.

**Follow-ups:**
- "What steps never change regardless of input?"
- "Are there rules or constraints that always apply?"
- "What quality checks do you always run at the end?"

**What this produces:** Phase structure, validation rules, quality gates.

---

#### Question 5: "Who else does this?"

**Goal:** Determine the deployment ladder and universalization scope.

**Follow-ups:**
- "Does anyone on your team do a version of this?"
- "Could someone in a completely different domain use this pattern?"
- "What would they need to know to do it themselves?"

**What this produces:** Deployment ladder (team → org → enterprise → universal), example applications for diverse contexts.

---

### On-Demand Output: Skill Proposal

After the 5-question interview, the suggestor produces a structured **Skill Proposal**:

```markdown
# Skill Proposal: {{SKILL_NAME}}

## Summary
- **Name:** {{SKILL_NAME}}
- **Description:** One-line description
- **Detector:** on-demand (or which passive detector fired)
- **Confidence:** high/medium/low
- **Frequency:** daily/weekly/monthly
- **Time saved per use:** estimated minutes
- **Deployment ladder:** team → org → enterprise

## Proposed Intake Variables

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{VAR_1}}` | ... | type | yes/no | default |

## Proposed Phases
1. Phase name — what happens
2. Phase name — what happens
3. ...

## Universal Logic (what stays the same)
- Rule 1
- Rule 2

## Context-Dependent (what varies)
- Input 1
- Decision point 1

## Example Applications (who else could use this)
| Context | How they'd use it | Key variable changes |
|---------|-------------------|---------------------|
| Original | ... | baseline |
| Adjacent team | ... | ... |
| Different domain | ... | ... |

## Next Step
→ Feed this proposal to `skill-universalizer` for full extraction
```

---

## The Three Meta-Skills Working Together

```
skill-suggestor                    skill-universalizer              skill-improver
(detects the need)        →        (builds the skill)      →       (makes it better)

  "You keep doing this               "Let me extract the             "Phase 3 has 40%
   manually. Want a                    pattern, create the             abandonment. The
   skill for it?"                      intake variables, and           intake question is
                                       write the SKILL.md"             confusing. Here's
                                                                       a clearer version."
         │                                    │                              │
         ▼                                    ▼                              ▼
   Skill Proposal              →       SKILL.md + skill.yaml    →    Improved SKILL.md
   (private repo)                      (public repo, BETA)           (version bump)
```

**The lifecycle:**
1. **Suggestor** detects a pattern and produces a proposal
2. **Universalizer** takes the proposal and builds a full skill
3. **Improver** watches the skill in use and proposes refinements
4. Goto 3 (continuous improvement loop)

---

## Signal Storage

**All suggestor signals and proposals live in your PRIVATE repo only.**

```
CheatCodes-Private/
├── signals/
│   └── skill-suggestions.jsonl     ← passive detection signals
├── proposals/
│   ├── 2026-03-23-data-slice-and-chart.md    ← proposals
│   ├── 2026-03-25-email-triage-pattern.md
│   └── ...
```

**The public repo never sees:**
- Raw detection signals
- Draft proposals
- Session context that triggered detection
- Rejected proposals

**The public repo only sees:**
- The finished, universalized skill (if you approve the proposal)
- A clean commit message referencing the skill-suggestor origin

---

## Configuration

The suggestor's sensitivity can be tuned per user. These settings live
in your private repo or local config:

```yaml
# skill-suggestor-config.yaml (private)
passive_mode:
  enabled: true
  detectors:
    repetition:
      enabled: true
      threshold: 2          # repetitions before firing (default: 2)
    manual_labor:
      enabled: true
      threshold: 4          # mechanical operations before firing (default: 4)
    wish:
      enabled: true
      threshold: 1          # strong signals before firing (default: 1)
    cross_session:
      enabled: true
      window_days: 14       # lookback window for cross-session patterns
      threshold: 3          # similar sessions before firing (default: 3)

  # Noise reduction
  ignore_patterns:
    - "git commit"          # don't suggest a skill for git workflows
    - "file read"           # basic file operations aren't skills
    - "search"              # search patterns are too generic

on_demand:
  interview_depth: full     # full (5 questions) | quick (3 questions)
  auto_feed_universalizer: false  # if true, accepted proposals auto-feed to universalizer
```

---

## Anti-Patterns

```
DON'T suggest skills for:
  ✗ One-time tasks (no repetition signal)
  ✗ Simple lookups ("what's the status of X")
  ✗ Basic file operations (read/write/search)
  ✗ Platform-specific commands (git, npm, docker)
  ✗ Conversational tasks (explain, teach, brainstorm)

DO suggest skills for:
  ✓ Multi-step workflows with predictable structure
  ✓ Data transformations that follow a pattern
  ✓ Report/document generation from templates
  ✓ Analysis pipelines with consistent phases
  ✓ Coordination workflows (notify → collect → reconcile → report)
  ✓ QA/validation workflows with defined criteria
```

---

## Example Suggestions

| Detected Pattern | Detector | Proposed Skill | Confidence |
|-----------------|----------|---------------|------------|
| User pulls org data, slices by 3 dimensions, builds a bar chart — 4th time this month | cross-session | `data-slice-reporter` | High |
| "Take this CSV and make it a formatted PPTX table" — 3rd time in one session | repetition | `csv-to-slide-formatter` | High |
| "Every Monday I have to check these 5 dashboards and summarize..." | wish | `dashboard-digest` | Medium |
| User manually reformats JSON → YAML → validates — batch of 12 files | manual-labor | `config-format-converter` | Medium |
| "I wish I could just paste a screenshot and get the CSS" | wish | `screenshot-to-css` | Medium |
| Same error-handling pattern applied to 3 different API integrations | repetition | `api-error-handler-pattern` | Low |

---

## Platform Notes

| Platform | How to Use |
|----------|------------|
| **Any LLM** | Paste this SKILL.md as context; invoke on-demand with "suggest a skill for what I just did" |
| **Custom agents** | Load as instruction set; passive mode requires session history access |
| **CLI tools** | Copy to skills directory; invoke with `/skill skill-suggestor` |
| **IDE extensions** | Reference in agent config; passive mode observes editor session |

---

## Compliance

- **PII Risk:** None in the skill itself. Passive signals may contain session
  context — stored only in private repo, never in public.
- **Model Recommendation:** Sonnet (pattern detection requires reasoning over
  multi-step sequences)
- **Human Oversight:** All proposals require human approval before feeding
  into skill-universalizer. Passive mode never auto-creates skills.
