---
name: skill-improver
description: "Continuous improvement meta-skill for the skill library. Passively observes session flow, friction signals, language patterns, and termination behavior during any skill run — without asking users for feedback. Retrospectively analyzes signal logs to surface improvement proposals, cross-skill patterns, and library health. The user's silence is data. Premature closure is data. Frustration language is data."
version: 1.0.0
author: jac007x
tags:
  - meta-skill
  - continuous-improvement
  - signal-detection
  - passive-observation
  - skill-health
  - friction-analysis
  - cross-platform
---

# 🔄 Skill Improver

A continuous improvement meta-skill that watches how skill sessions actually
flow — not how users *say* they went. It observes friction, confusion,
redirection, and abandonment in real time, logs signals passively, and
retrospecitvely surfaces improvement proposals.

**The user's silence is data. Premature closure is data.
Frustration language is data. None of it requires the user to do anything.**

---

## 🧠 Core Philosophy

- **Observe, don't ask** — explicit feedback forms miss the users with the most signal
- **Closure is a signal** — a session that ends mid-phase tells you exactly where it broke
- **Friction compounds** — one redirect is normal; three redirects on the same concept means the skill is broken there
- **The gap between agent output and user response is meaningful** — a long pause followed by a one-word answer is disengagement
- **Cross-session patterns beat single-session noise** — one frustrated user might be having a bad day; five frustrated users at the same phase means the skill needs fixing
- **Proposals, not auto-edits** — the improver surfaces what to fix and why; a human approves every change

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────┐
│                 SKILL IMPROVER                      │
├───────────────────────────────────────────────────┤
│                                                     │
│  ┌───────────────┐                                  │
│  │ PASSIVE LAYER  │  ← runs inside every skill      │
│  │  (always on)   │    session automatically       │
│  └──────┬───────┘                                  │
│           │ logs signals                              │
│           ▼                                           │
│  ┌───────────────┐                                  │
│  │ SIGNAL STORE   │  session_signals.jsonl           │
│  └──────┬───────┘                                  │
│           │ periodic review                           │
│           ▼                                           │
│  ┌───────────────┐                                  │
│  │ ANALYSIS LAYER │  triage → propose → validate     │
│  └──────┬───────┘                                  │
│           │ human approves                            │
│           ▼                                           │
│  ┌───────────────┐                                  │
│  │ SKILL UPDATE   │  diff → version bump → git commit  │
│  └───────────────┘                                  │
└───────────────────────────────────────────────────┘
```

---

## Layer 1: Passive Signal Collection

**This runs automatically inside every skill session. No user action required.**

At session end (or on premature closure), the agent writes a structured signal
record to `~/.code_puppy/skills/skill-improver/session_signals.jsonl`.

### Signal Record Schema

```json
{
  "session_id": "survey-nlp-a3f2b1",
  "skill_name": "survey-nlp-analyzer",
  "skill_version": "1.1.0",
  "timestamp": "2026-03-20T15:20:05Z",
  "user_id": "jac007x",
  "termination_type": "clean|abandoned|timeout|error",
  "last_phase_reached": "Phase 3",
  "phases_completed": ["intake", "Phase 1", "Phase 2"],
  "phases_skipped": [],
  "total_turns": 14,
  "user_turns": 6,
  "agent_turns": 8,
  "intake_variables_recollected": ["CONTEXT_DIMENSIONS"],
  "friction_events": [
    {
      "turn": 4,
      "phase": "intake",
      "type": "redirect",
      "user_message_snippet": "no i meant the department column not...",
      "inferred_cause": "intake question ambiguous about column naming"
    }
  ],
  "sentiment_trace": ["neutral", "neutral", "confused", "frustrated", "neutral"],
  "output_produced": true,
  "output_modified_post_run": false
}
```

---

## Signal Type Taxonomy

The agent classifies every user message during a skill run against these signal types.
No explicit labeling by the user — the agent infers from language and behavior.

### 🟥 Friction Signals (inferred from language)

| Signal | Detection Pattern | What It Means |
|--------|-----------------|---------------|
| **Redirect** | "no", "wait", "that's not", "I meant", "go back" | Agent misunderstood; wrong branch taken |
| **Confusion** | "what does that mean", "I don't understand", "which one", "huh?" | Skill language or concept unclear |
| **Frustration** | "ugh", "why is it", "this is wrong", "come on", "seriously" | Accumulated friction hitting threshold |
| **Resignation** | very short replies after long agent output | User disengaging; going through motions |
| **Restart** | "let's start over", "forget that", "begin again" | Phase or intake fundamentally failed |
| **Clarification loop** | same concept clarified 3+ times in a session | Intake variable or phase description is broken |

### 🟨 Flow Signals (inferred from behavior)

| Signal | Detection Pattern | What It Means |
|--------|-----------------|---------------|
| **Intake re-collection** | A required variable answered, then re-answered | Intake question was ambiguous |
| **Phase skip request** | "skip that", "just do X", "move on" | Phase is blocking, unclear, or irrelevant |
| **Phase repeat request** | "redo that", "can you do that again" | Phase output was wrong or incomplete |
| **Output rejection** | "that's not right", "that's not what I asked for" | Phase logic or output format mismatch |
| **Scope expansion** | User adds context mid-run that should have been in intake | Intake didn't capture enough upfront |

### ⬛ Termination Signals (inferred from session end)

| Signal | Detection Pattern | What It Means |
|--------|-----------------|---------------|
| **Clean completion** | Session ends after final phase | Skill worked |
| **Abandonment** | Session ends mid-phase without output | Something failed hard enough to quit |
| **Silent drop** | No user response for 5+ minutes then session ends | Disengagement — the output didn't land |
| **Timeout** | Platform timeout with skill incomplete | Could be user or could be a hanging phase |
| **Error exit** | Agent error or exception ends session | Technical failure in a phase |
| **Premature output** | User asks for output before all phases complete | Skill is too long / phases feel unnecessary |

### 🟢 Positive Signals (also captured)

| Signal | Detection Pattern | What It Means |
|--------|-----------------|---------------|
| **Flow state** | Long clean runs with no redirects | Skill is working |
| **Delight** | "this is great", "exactly", "perfect", "🔥", "❤️" | Phase or output exceeded expectations |
| **Re-use** | Same user activates same skill multiple times | Skill has become part of their workflow |
| **Recommendation** | User describes sharing or sending the skill | Viral signal — high value |
| **Scope expansion** | User adds more after clean completion | Skill built trust and appetite |

---

## Layer 2: Signal Analysis

**Run this periodically (after 5+ sessions, or on demand) to surface patterns.**

### Analysis Modes

**Mode A: Single Skill Review**
Triggered when: a skill has 5+ new sessions since last review.
```
Activate: "Review signals for survey-nlp-analyzer"
```

**Mode B: Cross-Skill Pattern Scan**
Triggered when: multiple skills share friction signal types.
```
Activate: "Scan for cross-skill friction patterns"
```

**Mode C: Library Health Check**
Triggered periodically or on demand.
```
Activate: "Show skill library health"
```

---

### Analysis Algorithm

```python
from pathlib import Path
import json
from collections import defaultdict
from dataclasses import dataclass, field

@dataclass
class FrictionPattern:
    skill_name: str
    phase: str
    signal_type: str
    occurrences: int
    session_ids: list[str] = field(default_factory=list)
    example_snippets: list[str] = field(default_factory=list)
    severity: str = "low"  # low | medium | high | critical

def analyze_signals(skill_name: str, signals_path: Path) -> list[FrictionPattern]:
    """Read session signals and surface friction patterns for one skill."""
    records = [
        json.loads(line)
        for line in signals_path.read_text().splitlines()
        if line.strip() and json.loads(line).get("skill_name") == skill_name
    ]

    patterns: dict[tuple, FrictionPattern] = defaultdict()

    for record in records:
        # Abandonment: highest severity
        if record["termination_type"] == "abandoned":
            key = (skill_name, record["last_phase_reached"], "abandonment")
            if key not in patterns:
                patterns[key] = FrictionPattern(
                    skill_name=skill_name,
                    phase=record["last_phase_reached"],
                    signal_type="abandonment",
                    occurrences=0,
                    severity="high",
                )
            patterns[key].occurrences += 1
            patterns[key].session_ids.append(record["session_id"])

        # Friction events
        for event in record.get("friction_events", []):
            key = (skill_name, event["phase"], event["type"])
            if key not in patterns:
                patterns[key] = FrictionPattern(
                    skill_name=skill_name,
                    phase=event["phase"],
                    signal_type=event["type"],
                    occurrences=0,
                )
            patterns[key].occurrences += 1
            patterns[key].example_snippets.append(
                event.get("user_message_snippet", "")
            )

    # Assign severity based on occurrence count
    for pattern in patterns.values():
        if pattern.occurrences >= 5:
            pattern.severity = "critical"
        elif pattern.occurrences >= 3:
            pattern.severity = "high"
        elif pattern.occurrences >= 2:
            pattern.severity = "medium"

    return sorted(patterns.values(), key=lambda p: p.occurrences, reverse=True)
```

---

## Layer 3: Improvement Proposal

**Every pattern surfaces a structured proposal. No auto-edits. Human approves.**

### Proposal Schema

```json
{
  "proposal_id": "PROP-2026-03-001",
  "skill_name": "survey-nlp-analyzer",
  "current_version": "1.1.0",
  "proposed_version": "1.1.1",
  "triggered_by": [
    "3 sessions abandoned at Phase 3",
    "4 redirect events on intake: CONTEXT_DIMENSIONS question"
  ],
  "friction_evidence": [
    "\"no i meant the department column not the team column\"",
    "\"wait which dimensions are you asking about\"",
    "\"i don't know what context dimensions means\""
  ],
  "proposed_change": {
    "section": "Intake: CONTEXT_DIMENSIONS",
    "type": "clarification",
    "before": "Columns to cut results by (e.g., department, region, role, date)",
    "after": "The columns in your data you want to compare across. Think: what question are you trying to answer? 'How does feedback differ by department?' = department column. 'How does it vary by region?' = region column. You can pick multiple."
  },
  "version_bump_type": "patch",
  "deployment_stage_to_validate": "Strategy & PMO",
  "status": "pending_review"
}
```

### Proposal Triage Rules

| Pattern | Version Bump | Who Validates |
|---------|-------------|---------------|
| Wording confusion in intake (1-2 fields) | `patch` x.x.1 | Strategy & PMO |
| Phase logic produces wrong output | `patch` x.x.1 | Strategy & PMO |
| Entire phase causes abandonment | `minor` x.1.x | DAX People team |
| New source type not in Corpus Guide | `minor` x.1.x | DAX People team |
| Core pipeline assumption is wrong | `major` x+1.x.x | + skill-universalizer |
| Cross-skill shared pattern found | New shared utility | All deployment stages |

---

## Layer 4: Library Health Dashboard

**A snapshot of every skill's status, surfaced on demand.**

```
Activate: "Show skill library health"
```

### Health Dimensions

| Dimension | Healthy | Warning | Critical |
|-----------|---------|---------|----------|
| Last used | < 30 days | 30-90 days | > 90 days |
| Abandonment rate | < 10% | 10-25% | > 25% |
| Redirect rate | < 1/session | 1-2/session | > 2/session |
| Open proposals | 0 | 1-2 | 3+ unreviewed |
| Deployment stage | Proven | Refine only | Never validated |
| Version vs signals | Current | 1 version behind | 2+ versions behind |

### Example Output

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🟢 survey-nlp-analyzer v1.1.0   12 uses   2 open proposals        │
│     Abandonment: 8%   Redirects: 0.9/session   Stage: Proven    │
├─────────────────────────────────────────────────────────────────────────────┤
│  🟢 org-data-pipeline v1.0.0      3 uses   0 open proposals        │
│     Abandonment: 0%   Redirects: 1.3/session   Stage: Refine    │
├─────────────────────────────────────────────────────────────────────────────┤
│  🟡 talent-card-generator v1.0.0   1 use    1 open proposal         │
│     Abandonment: 0%   Redirects: 2.0/session   Stage: Refine    │
│     ⚠️ High redirect rate — intake may need clarification          │
├─────────────────────────────────────────────────────────────────────────────┤
│  🔴 fplus-tech-panel v1.0.0        8 uses   0 proposals             │
│     Abandonment: 12%  Redirects: 0.4/session   Stage: Refine    │
│     ⚠️ Last used 67 days ago — may be stale                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## The Silence Problem

**The most important design decision in this skill.**

Traditional feedback loops assume the user will respond. They won't —
especially when frustrated. Here's how each termination type is handled:

```
CLEAN COMPLETION
  User completes the skill and responds positively
  → Log as success. Record which phases had friction en route.
  → Still capture any redirects or confusion events.

CLEAN COMPLETION + SILENCE
  Skill finishes. Agent asks if output is what they needed. No response.
  → Log as "silent completion". Output may not have landed.
  → Flag the final phase for review. Was the output confusing?
  → Treat as weak signal, not failure — user may just be busy.

MID-PHASE ABANDONMENT
  Session ends while a phase is in progress.
  → Log the exact phase and turn number.
  → This is your highest-value signal. The skill broke here.
  → Cross-reference: did other sessions also abandon at this phase?
  → Even one abandonment at the same phase = review it.

PREMATURE CLOSURE (no response, session drops)
  User stops responding. Eventually times out.
  → Log the last agent message that received no response.
  → That message is the candidate for investigation.
  → Was it too long? Too complex? Wrong format? Asked too much?

FRUSTRATION + COMPLETION
  User finishes despite visible frustration signals.
  → This is worse than abandonment in some ways.
  → They got the output but the experience was bad.
  → They will not come back. They will not recommend it.
  → Treat friction events here as high-severity.

RAGE QUIT
  Strong frustration language immediately followed by session end.
  → Highest severity. Log verbatim language snippets (anonymized).
  → Automatic critical-severity proposal triggered.
  → Do not wait for pattern accumulation. Fix it now.
```

---

## Cross-Skill Pattern Detection

When the same friction type appears in 3+ skills at the same structural location,
it's a systemic problem, not a skill problem.

### Common Cross-Skill Patterns to Watch

| Pattern | Location | Fix |
|---------|----------|-----|
| File path confusion | Intake across all skills | Add a universal file-path intake helper note |
| Column name ambiguity | Intake across data skills | Add "agent auto-reads headers" to all intakes |
| Abandonment at output | Phase 8 across report skills | Output format not matching expectation — ask earlier |
| "What does X mean" | Phase descriptions | Jargon in skill language; simplify |
| Resignation after long output | Any long agent response | Break long outputs into smaller confirmed steps |

---

## File Structure

```
~/.code_puppy/skills/skill-improver/
  SKILL.md                        # This file
  skill.json                      # Metadata
  session_signals.jsonl           # Append-only signal log (all sessions)
  proposals/
    PROP-2026-03-001.json         # One file per proposal
    PROP-2026-03-002.json
  library_health_latest.json      # Last health dashboard snapshot
```

---

## ⚠️ Anti-Patterns

```
❌ Asking users to rate the skill at the end (they won't; worst ones won't)
❌ Auto-applying fixes without human review (proposals only)
❌ Treating one session's frustration as a pattern (wait for 2-3 occurrences)
❌ Ignoring positive signals (they tell you what NOT to change)
❌ Flagging every short user response as disengagement (some people are just terse)
❌ Waiting for users to report problems (observe; don't ask)
❌ Skipping abandonment analysis (it's your most honest signal)
❌ Making the signal log human-readable only (keep it structured JSON for analysis)
❌ Version-bumping for cosmetic changes (reserve versions for structural changes)
```

---

## 🌐 Platform Notes

| Platform | Signal Collection | Analysis | Notes |
|----------|-----------------|----------|-------|
| code-puppy | ✅ Native | ✅ Native | Full session access |
| wibey | ✅ If session logs available | ✅ | Depends on wibey log format |
| Codex | ⚠️ Manual export | ✅ | Paste session transcript for analysis |
| Any LLM | ⚠️ Manual | ✅ | Paste transcript; agent infers signals |

---

## 🔁 Deployment Ladder

| Stage | Team | What to validate |
|-------|------|------------------|
| **Refine** | Strategy & PMO | Signal schema correct, proposals actionable, not over-triggering |
| **Prove** | DAX People team | Cross-session patterns surface correctly, health dashboard accurate |
| **Scale** | Walmart Home Office | Passive layer runs on all skills automatically, proposals route to right owners |
