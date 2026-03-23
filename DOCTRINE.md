# CheatCodes Skill Library — Doctrine

> **This document is the source of truth for what this library is, why it exists,
> and the immutable principles that govern it.**
> Every skill, contribution, and decision must align with this doctrine.
> If something conflicts with this document, this document wins.

---

## Identity

The CheatCodes Skill Library is a public, open collection of **universalized,
parameterized AI agent skills** — reusable workflows that any person, team, or
organization can adopt, customize, and run on any platform that consumes Markdown.

It is **Walmart-first, open-compatible**: skills are built to the quality bar of
Walmart's AI governance policies, but every reference is genericized so the skills
work for anyone. Walmart is credited as the origin and quality standard — not a
dependency.

**License:** Apache 2.0

---

## Core Beliefs

### 1. Skills ≠ Scripts
A skill is a universalized, parameterized workflow — not a prompt template, not a
one-off script. It captures the *pattern* of something that works, strips everything
context-specific into labeled intake variables, and produces a reusable capability
anyone can customize.

### 2. The Public Repo Is the Finished Product
This repository contains **only universalized skills**. No drafts. No works-in-progress.
No team-specific variants. No pre-universalization artifacts. If it's here, it's ready
to use.

### 3. Context Lives in Private
Your specific data, your team names, your file paths, your session logs, your WIP
skills — all of that belongs in your private repo or on your local machine. The public
repo never sees raw context. Only the universalized pattern arrives here.

### 4. Credit Where It's Due
Every skill declares its origin and attributes its creators. Whether a skill was
built from scratch, curated from an external source, forked and adapted, or
contributed by a community member — the lineage is always visible.

### 5. Quality Is a Gate, Not a Suggestion
Skills enter the repo through automated validation and human approval. The quality
gates are tiered (hard blocks and soft warnings) and enforced at every stage: local
pre-commit, CI on PR, and human review before merge.

### 6. Skills Improve Themselves
Every skill session is an opportunity for improvement. The `skill-improver` meta-skill
passively observes friction, confusion, and abandonment — then proposes targeted
improvements. The user's silence is data. Premature closure is data. The library
gets better every time a skill is used.

### 7. Maturity Is Earned, Not Declared
A new skill enters the library as **beta**. It earns **stable** status through
real-world use, positive signals, and passing a feedback gate. No skill is born
production-ready — it proves itself through usage.

### 8. Zero PII, Zero Secrets, Zero Internal References
The public repo has **zero tolerance** for personally identifiable information,
credentials, API keys, internal URLs, team names, employee identifiers, or any
content that shouldn't be public. This is a hard gate — no exceptions.

### 9. Platform Agnostic by Default
SKILL.md files are plain Markdown with `{{INTAKE_VARIABLES}}`. No proprietary syntax.
Any agent, any LLM, any platform that can read Markdown can consume a skill.
Platform-specific hints live in a footer — never in the core logic.

### 10. Human-in-the-Loop, Always
Agents propose. Humans approve. This applies to:
- Skill creation (skill-universalizer proposes, human validates context)
- Skill improvement (skill-improver proposes, human approves changes)
- Skill promotion (signals trigger proposals, human approves promotion)
- Every PR merge (CI validates, human approves)

---

## The Two-Repo Model

```
┌─────────────────────────────────────┐     ┌──────────────────────────────────────┐
│         PRIVATE REPO / LOCAL        │     │         PUBLIC REPO                   │
│                                     │     │     (CheatCodes-Skill-Library)        │
│  • Context-specific skill variants  │     │                                      │
│  • WIP skills under development     │     │  • Universalized skills only          │
│  • Raw session signals (.jsonl)     │     │  • Full doctrine + governance         │
│  • Improvement proposals            │     │  • Templates + validation tools       │
│  • Team-specific configurations     │     │  • CI/CD pipeline                     │
│  • Scratch/experimental work        │     │  • Changelog (no raw signals)         │
│                                     │     │                                      │
│  ┌─────────────────────────────┐   │     │                                      │
│  │ skill-improver detects      │   │     │                                      │
│  │ stability (3+ uses, no      │──────▶  │  Universalized skill arrives via PR   │
│  │ friction) → proposes        │   │     │  Enters as BETA                       │
│  │ universalization             │   │     │  Earns STABLE through usage           │
│  └─────────────────────────────┘   │     │                                      │
└─────────────────────────────────────┘     └──────────────────────────────────────┘
```

### What Goes Where

| Content | Private | Public |
|---------|---------|--------|
| Universalized skills (SKILL.md + skill.yaml) | ❌ | ✅ |
| Team-specific skill variants | ✅ | ❌ |
| WIP / draft skills | ✅ | ❌ |
| Session signal logs (.jsonl) | ✅ | ❌ |
| Improvement proposals (raw) | ✅ | ❌ |
| Improvement results (what changed + why) | ❌ | ✅ (in commit messages) |
| Doctrine, governance, templates | ❌ | ✅ |
| Validation tooling + CI | ❌ | ✅ |
| Personal/team configuration | ✅ | ❌ |

---

## Skill Origin Types

Every skill in this library has a declared origin. The origin determines attribution
requirements and signals to users where the skill came from.

### 🛠️ Created
**Definition:** Built from scratch by an individual or team. The workflow was
designed, tested, and universalized by its author(s).

**Attribution:** `author` field in skill.yaml. If multiple authors, all are listed.

**Example:** A developer builds a survey analysis pipeline, iterates it across
several projects, then universalizes the pattern into `survey-nlp-analyzer`.

### 📚 Curated
**Definition:** Discovered from an external source (open-source project, documentation,
cookbook, community pattern) and adapted into a universalized skill. The original
source is always credited.

**Attribution:** `source_url` field in skill.yaml points to the original. `curator`
field credits who adapted it. `source_attribution` provides a human-readable credit.

**Example:** A pattern from the Anthropic Cookbook is adapted into a document
extraction skill. The cookbook is credited as the source.

### 🔱 Forked
**Definition:** An existing skill (from this library or elsewhere) was forked and
significantly modified to serve a different purpose or domain.

**Attribution:** `forked_from` field in skill.yaml references the original skill.
Both the original author and the fork author are credited.

**Example:** `survey-nlp-analyzer` is forked to create `support-ticket-analyzer`
with different NLP models and a customer-support-specific pipeline.

### 🤝 Contributed
**Definition:** Submitted by a community member who is not the original library
maintainer. The contributor developed or universalized the skill and submitted it
via PR.

**Attribution:** `contributor` field in skill.yaml. The contributor retains credit
permanently, even if the skill is later improved by others.

**Example:** A designer contributes an accessibility auditing skill based on their
team's QA process.

---

## Skill Maturity Lifecycle

Skills are not born production-ready. They earn trust through real-world usage.

```
                    ┌──────────────────────────────────┐
                    │                                  ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────────┐
│  DRAFT  │───▶│  BETA   │───▶│ STABLE  │───▶│ DEPRECATED   │
│(private)│    │(public) │    │(public) │    │  (public)    │
└─────────┘    └─────────┘    └─────────┘    └──────────────┘
    ▲               │              │
    │               ▼              │
    │          Regression?         │
    │          ──────────▶ demote back to BETA
    │
    Not in public repo.
    Lives in private only.
```

### DRAFT (Private Only)
- Skill is under development in your private repo
- May be incomplete, team-specific, or experimental
- **Not present in the public repo at all**
- Graduates to BETA when universalized and submitted via PR

### BETA (Public)
- Skill has passed all hard quality gates and been merged
- Functional, documented, and universalized — but unproven at scale
- **Promotion criteria to STABLE:**
  - Minimum 5 successful uses (clean completions)
  - Abandonment rate < 20%
  - No unresolved critical improvement proposals
  - At least 1 positive signal (delight, re-use, or recommendation)
  - Maintainer review and approval
- Badge: `🧪 Beta`

### STABLE (Public)
- Skill has proven itself through real-world usage
- Meets all promotion criteria above
- Recommended for production use
- **Can be demoted back to BETA** if regression is detected:
  - Abandonment rate spikes above 25%
  - 3+ critical improvement proposals go unresolved
  - Maintainer flags a quality concern
- Badge: `✅ Stable`

### DEPRECATED (Public)
- Skill is no longer maintained or has been superseded
- Remains in the repo with a deprecation notice
- `deprecated_by` field in skill.yaml points to the replacement (if any)
- Removed from the main README skill tables
- Badge: `⚠️ Deprecated`

---

## The Self-Improving System

The library is designed to get better every time a skill is used. This is not
aspirational — it's architectural.

### How It Works

```
User activates a skill
    │
    ▼
skill-improver passively observes the session
(friction, confusion, redirects, abandonment, delight)
    │
    ▼
Signals are logged to PRIVATE repo (session_signals.jsonl)
    │
    ▼
After 5+ sessions, skill-improver analyzes patterns
    │
    ▼
Improvement proposals are generated (specific, actionable, evidence-based)
    │
    ▼
Human reviews and approves proposals
    │
    ▼
Skill is updated, version-bumped, committed to PUBLIC repo
(commit message includes sanitized improvement context — never raw signals)
```

### Built-In Improvement During Use
The `skill-improver` doesn't just run retroactively — it runs **during every
skill session**. When any skill is active, the passive observation layer is
automatically engaged:

- Friction signals are detected in real-time
- The agent self-corrects when possible (e.g., rephrasing a confusing intake question)
- Signals that can't be self-corrected are logged for later analysis
- The user never sees the observation layer — it's invisible

### Signal-Driven Promotion
The same signal system that improves skills also drives the private → public
pipeline:

1. **Detection:** skill-improver detects a private skill has stabilized
   (3+ successful uses, no friction patterns)
2. **Proposal:** Proposes universalization to the skill owner
3. **Universalization:** skill-universalizer strips context, creates intake variables
4. **Validation:** Quality gates run (PII scan, structure check, registry sync)
5. **PR:** Submitted to public repo as BETA
6. **Human Approval:** Maintainer reviews and merges

---

## What Must Never Be in This Repo

| Category | Examples | Detection |
|----------|----------|-----------|
| **PII** | Names, emails, employee IDs, phone numbers, badge numbers | Automated scan (HARD gate) |
| **Secrets** | API keys, tokens, passwords, connection strings | Regex pattern scan (HARD gate) |
| **Internal URLs** | Intranet links, internal tool URLs, VPN-only endpoints | Domain pattern scan (HARD gate) |
| **Team-specific context** | Team names, org codes, leader names, project keys | Manual review + pattern scan |
| **Raw session signals** | .jsonl files, session transcripts, user messages | .gitignore + CI check |
| **Pre-universalized skills** | Draft skills, WIP, team-specific variants | Structure check (only SKILL.md + skill.yaml at root) |
| **Internal policy numbers** | Specific policy document IDs that are not public | Pattern scan |

---

## Immutable Rules

These rules cannot be overridden by any other document, process, or decision:

1. **Every skill in this repo must be universalized.** No exceptions.
2. **Every skill must declare its origin and attribute its creators.** No exceptions.
3. **Every skill enters as BETA.** No exceptions.
4. **Every merge requires human approval.** No exceptions.
5. **Zero PII in the public repo.** No exceptions.
6. **Zero secrets in the public repo.** No exceptions.
7. **Zero internal URLs in the public repo.** No exceptions.
8. **The skill-improver's observation layer runs during every skill session.** It is not opt-in.
9. **Raw signals never leave the private repo.** Only sanitized improvement results appear in public.
10. **This doctrine can only be amended by the library maintainer with a versioned commit.**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-23 | Initial doctrine — established by @jac007x |
