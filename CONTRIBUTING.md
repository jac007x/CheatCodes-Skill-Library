# Contributing to CheatCodes Skill Library

> **Before contributing, read [DOCTRINE.md](DOCTRINE.md) and [GOVERNANCE.md](GOVERNANCE.md).**
> This document tells you *how* to contribute. The Doctrine tells you *what we believe*.
> The Governance tells you *what the rules are*.

---

## Ways to Contribute

### 1. Submit a New Skill

You've built a workflow that works. You've universalized it. You want to share it.

**Requirements:**
- The skill must be **fully universalized** — no team-specific context, no internal references
- It must pass all **hard quality gates** (see [GOVERNANCE.md](GOVERNANCE.md#hard-gates-block-merge))
- It must include `SKILL.md` + `skill.yaml` at minimum
- It enters the library as **BETA** — no exceptions

**Process:**
1. Fork this repository
2. Create your skill directory at the root level: `your-skill-name/`
3. Add your `SKILL.md` and `skill.yaml` (see [Skill Checklist](#skill-checklist))
4. Add your skill to `registry.json`
5. Run `python tools/validate_skill.py your-skill-name/` locally
6. Fix any hard gate failures, acknowledge any soft gate warnings
7. Submit a PR using the **New Skill** template

### 2. Improve an Existing Skill

You've used a skill and found something that could be better — a confusing intake
question, a missing example, a logic gap.

**Process:**
1. Open an issue describing the improvement (or reference a skill-improver proposal)
2. Fork, make the change, bump the version (see [versioning rules](GOVERNANCE.md#versioning-rules))
3. Submit a PR referencing the issue

### 3. Report an Issue

Something's broken, unclear, or wrong.

**Process:**
- Open an issue using the **Bug Report** template
- Include: which skill, what you expected, what happened

### 4. Curate an External Skill

You found a great pattern in the wild (open-source project, cookbook, community post)
and want to bring it into the library.

**Process:**
1. Open an issue using the **Skill Curation Request** template
2. Include the source URL and a description of why it's valuable
3. Fork the repo, adapt the pattern into a universalized SKILL.md
4. Set `origin: curated` in skill.yaml with proper `source_url` and `source_attribution`
5. Submit a PR

---

## Skill Checklist

Every skill submission **must** include:

### Required Files

| File | Purpose | Required |
|------|---------|----------|
| `SKILL.md` | The full universalized skill — philosophy, intake, phases, examples, anti-patterns | **Yes** |
| `skill.yaml` | Metadata — name, version, origin, author, maturity, tags | **Yes** |

### Optional Files

| File | Purpose | When to Include |
|------|---------|----------------|
| `skill.json` | Extended metadata (capabilities, dependencies, scalability) | Complex skills with runtime dependencies |
| `*.py` | Implementation code | Skills that include executable components |
| `CHANGELOG.md` | Version history | After the first improvement (v1.0.1+) |

### SKILL.md Required Sections

| Section | Purpose |
|---------|---------|
| **YAML Front Matter** | `name`, `version`, `description`, `author`, `tags` |
| **One-Paragraph Description** | What this skill does, universally |
| **Core Philosophy** | Design principles guiding this skill |
| **Intake: Customize This Skill** | `{{VARIABLE}}` table with descriptions, types, defaults |
| **Architecture** | ASCII diagram of the pipeline/flow |
| **Phases** | Step-by-step execution with goals, implementation, validation |
| **Anti-Patterns** | Common mistakes to avoid (learned from real usage) |
| **Example Applications** | 4+ diverse use cases demonstrating universality |

### SKILL.md Recommended Sections

| Section | Purpose |
|---------|---------|
| **Bulletproofing Checklist** | Things to verify before sharing output |
| **Platform Notes** | Compatibility table (footer position) |
| **Deployment Ladder** | Refine → Prove → Scale stages |

### skill.yaml Required Fields

```yaml
name: skill-name
version: 1.0.0
description: "One-line description"
origin: created          # created | curated | forked | contributed
author: your-handle
created: 2026-03-23
maturity_status: beta    # Always beta for new submissions
tags:
  - tag1
  - tag2
```

See [GOVERNANCE.md](GOVERNANCE.md#skill-metadata-schema-skillyaml) for the full schema.

---

## Origin & Attribution Guide

Your skill's `origin` field determines what attribution is required.

| Origin | You... | Required Fields |
|--------|--------|----------------|
| `created` | Built it from scratch | `author` |
| `curated` | Adapted it from an external source | `author`, `source_url`, `source_attribution`, `curator` |
| `forked` | Forked and modified an existing skill | `author`, `forked_from`, `fork_author` |
| `contributed` | Are a community member submitting a skill | `author`, `contributor` |

**Credit is permanent.** Even if a skill is later improved by others, the original
author/contributor/curator retains attribution in skill.yaml.

---

## Quality Gates

Before submitting, run the local validator:

```bash
# Validate your skill
python tools/validate_skill.py your-skill-name/

# Validate all skills (to make sure you didn't break anything)
python tools/validate_skill.py --all
```

### Hard Gates (Must Pass)

Your PR will be **blocked** if any of these fail:
- No PII (names, emails, employee IDs)
- No secrets (API keys, tokens, passwords)
- No internal URLs (intranet links, internal tool URLs)
- SKILL.md exists
- skill.yaml exists with required fields
- Registered in registry.json
- Origin declared
- Attribution present

### Soft Gates (Warnings)

You'll see warnings for these — reviewer must acknowledge before approving:
- Compliance section present
- ≥4 example applications
- Platform notes
- Intake variables documented
- Anti-patterns section
- Model recommendation
- Risk level
- PII handling documented (if applicable)

---

## What Does NOT Belong in This Repo

| Content | Where It Goes |
|---------|--------------|
| Team-specific skill variants | Your private repo |
| WIP / draft skills | Your private repo |
| Session signal logs | Your private repo (or local machine) |
| Raw improvement proposals | Your private repo |
| Internal URLs or references | Nowhere public |
| PII of any kind | Nowhere public |
| API keys or credentials | Nowhere. Ever. |

---

## Review Criteria

Reviewers evaluate submissions against these criteria:

| Criterion | Question |
|-----------|----------|
| **Usefulness** | Does this solve a real, recurring problem? |
| **Universality** | Can someone outside your team/org use this? |
| **Quality** | Is the SKILL.md well-written, clear, and complete? |
| **Uniqueness** | Is this different enough from existing skills? |
| **Safety** | Is there any PII, secrets, or internal content? |
| **Attribution** | Is the origin and credit accurate? |
| **Portability** | Does it work on any platform that reads Markdown? |

---

## Code of Conduct

- Be respectful and constructive
- Focus on the skill, not the person
- Share knowledge generously
- Credit others' contributions — always
- If you find PII or secrets in the repo, report it immediately

---

## Questions?

Open a [Discussion](../../discussions) or file an [Issue](../../issues).
