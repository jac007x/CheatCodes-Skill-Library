# CheatCodes Skill Library — Governance

> **This document defines the enforcement rules, validation criteria, promotion
> pipeline, and CI mechanics for the library.**
> It implements the principles defined in [DOCTRINE.md](DOCTRINE.md).
> When in doubt, defer to the Doctrine.

---

## Quality Gates

All skills must pass quality gates before merging to this repository.
Gates are **tiered**: hard gates block the merge; soft gates produce warnings
that require human acknowledgment.

### HARD Gates (Block Merge)

These checks **must pass**. A PR cannot merge if any hard gate fails.

| # | Gate | What It Checks | Tool |
|---|------|---------------|------|
| H1 | **No PII** | Scans for names, emails, employee IDs, phone numbers, badge numbers | `validate_skill.py --pii` |
| H2 | **No Secrets** | Regex scan for API keys, tokens, passwords, connection strings, PATs | `validate_skill.py --secrets` |
| H3 | **No Internal URLs** | Scans for intranet domains, internal tool URLs, VPN-only endpoints | `validate_skill.py --internal-urls` |
| H4 | **SKILL.md Exists** | The primary skill file must be present | File existence check |
| H5 | **skill.yaml Exists** | Metadata file with required fields must be present | File + schema check |
| H6 | **skill.yaml Schema Valid** | Required fields: `name`, `version`, `description`, `origin`, `author`, `maturity_status`, `tags` | Schema validation |
| H7 | **Registered in registry.json** | Skill must have a corresponding entry in the central registry | Registry sync check |
| H8 | **Origin Declared** | `origin` field must be one of: `created`, `curated`, `forked`, `contributed` | Enum validation |
| H9 | **Attribution Present** | Based on origin type, required attribution fields must be populated | Conditional field check |
| H10 | **No Pre-Universalized Content** | No `skills/` subdirectory artifacts, no team-specific references | Structure + content scan |

### SOFT Gates (Warning Only)

These checks produce warnings. A human reviewer must acknowledge warnings
before approving the PR. They do not block merge.

| # | Gate | What It Checks | Why It's Soft |
|---|------|---------------|---------------|
| S1 | **Compliance Section** | SKILL.md has a compliance/governance section | New skills may document this differently |
| S2 | **≥4 Example Applications** | Example applications table has 4+ diverse entries | Some niche skills may have fewer valid examples |
| S3 | **Platform Notes in Footer** | Platform compatibility table exists | Not all skills have been tested on all platforms |
| S4 | **Intake Variables Documented** | `{{VARIABLES}}` are listed in an intake table | Some simple skills may not need intake |
| S5 | **Anti-Patterns Section** | Documented pitfalls and mistakes to avoid | May not apply to very simple skills |
| S6 | **Model Recommendation** | Suggested model tier (haiku/sonnet/opus) | Depends on platform |
| S7 | **Risk Level Documented** | Low/Medium/High risk assessment | Reviewer can assess during review |
| S8 | **PII Handling Documented** | If skill may touch PII, controls are documented | Only relevant for data-touching skills |

---

## Skill Metadata Schema (skill.yaml)

Every skill must include a `skill.yaml` file with the following fields:

### Required Fields

```yaml
# === Identity ===
name: skill-name                    # kebab-case, unique across registry
version: 1.0.0                      # semver
description: "One-line description" # What does this skill do?

# === Origin & Attribution ===
origin: created                     # created | curated | forked | contributed
author: author-handle               # Primary author (GitHub handle or name)
created: 2026-03-23                 # Date skill was created

# === Maturity ===
maturity_status: beta               # beta | stable | deprecated
tags:
  - tag1
  - tag2
```

### Conditional Fields (Required Based on Origin)

```yaml
# If origin: curated
source_url: "https://..."           # Where the original pattern was found
source_attribution: "Description of original source and its author"
curator: curator-handle             # Who adapted it

# If origin: forked
forked_from: original-skill-name    # Skill this was forked from
fork_author: fork-handle            # Who created the fork

# If origin: contributed
contributor: contributor-handle     # Who submitted the contribution
contributor_url: "https://..."      # Contributor's profile or repo (optional)
```

### Optional Fields

```yaml
# === Model & Risk ===
model_recommendation: sonnet        # haiku | sonnet | opus
risk_level: low                     # low | medium | high

# === Dependencies ===
requires:
  python: ">=3.10"
  packages:
    - package1>=1.0

# === Maturity Tracking ===
maturity_signals:
  total_uses: 0                     # Updated by skill-improver
  clean_completions: 0
  abandonment_rate: 0.0
  positive_signals: 0
  last_used: null
  promoted_to_stable: null          # Date of promotion (if stable)

# === Deprecation ===
deprecated: false
deprecated_by: null                 # Replacement skill name
deprecation_date: null
deprecation_reason: null
```

---

## Maturity Promotion Pipeline

### BETA → STABLE Promotion

A skill is promoted from BETA to STABLE when **all** of the following criteria
are met:

| Criterion | Threshold | How It's Measured |
|-----------|-----------|-------------------|
| **Successful uses** | ≥ 5 clean completions | skill-improver signal logs |
| **Abandonment rate** | < 20% | Abandoned sessions / total sessions |
| **Critical proposals** | 0 unresolved | skill-improver proposal queue |
| **Positive signals** | ≥ 1 | Delight, re-use, or recommendation signals |
| **Age** | ≥ 14 days since BETA entry | Calendar time (prevents premature promotion) |
| **Maintainer approval** | Required | Human sign-off on promotion PR |

### Promotion Process

1. **Signal accumulation:** skill-improver tracks maturity signals in private repo
2. **Threshold met:** When all criteria are satisfied, skill-improver generates
   a promotion proposal
3. **Maintainer review:** Proposal includes evidence (sanitized — no raw signals)
4. **PR submitted:** Updates `maturity_status: stable` in skill.yaml and registry.json
5. **Merge:** Maintainer approves and merges

### STABLE → BETA Demotion (Regression)

A stable skill can be **demoted back to BETA** if:

| Trigger | Threshold |
|---------|-----------|
| Abandonment rate spike | > 25% over a 10-session window |
| Critical proposals | 3+ unresolved critical proposals |
| Maintainer flag | Maintainer identifies a quality concern |
| Breaking change | Skill produces incorrect output in a new context |

Demotion is logged in the skill's changelog and the promotion criteria reset.

---

## The Private → Public Pipeline

### Signal-Driven Proposal Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  PRIVATE REPO                                                    │
│                                                                  │
│  1. You build a skill for a specific purpose                     │
│  2. You use it across sessions (signals accumulate)              │
│  3. skill-improver detects stability:                            │
│     • 3+ successful uses                                         │
│     • No repeated friction patterns                              │
│     • Positive signals present                                   │
│                                                                  │
│  4. skill-improver proposes: "This skill is ready to             │
│     universalize. Here's the evidence."                          │
│                                                                  │
│  5. You approve the proposal                                     │
│                                                                  │
│  6. skill-universalizer runs:                                    │
│     • Strips team-specific context                               │
│     • Creates {{INTAKE_VARIABLES}}                               │
│     • Generates SKILL.md + skill.yaml                            │
│     • Runs validation gates locally                              │
│                                                                  │
│  7. You review the universalized output                          │
│                                                                  │
│  8. Submit PR to public repo                                     │
│     └─────────────────────────────────────────┐                 │
└───────────────────────────────────────────────│─────────────────┘
                                                 │
┌───────────────────────────────────────────────│─────────────────┐
│  PUBLIC REPO                                   ▼                 │
│                                                                  │
│  9. CI runs: hard gates + soft gates                             │
│  10. Human reviewer approves                                     │
│  11. Skill enters as BETA                                        │
│  12. Maturity signals accumulate from public usage               │
│  13. Promoted to STABLE when criteria met                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## CI/CD Pipeline

### Architecture: Belt & Suspenders

Two layers of validation ensure nothing slips through:

1. **Pre-commit hook** — Fast local validation before push
2. **GitHub Actions** — Full validation on every PR

### Pre-commit Hook

Runs automatically before every commit. Fast (< 5 seconds).

**Checks:**
- No secrets in staged files (regex scan)
- No internal URLs in staged files (domain pattern scan)
- No PII patterns in staged files
- SKILL.md exists for any new skill directory
- skill.yaml exists for any new skill directory

**Behavior on failure:**
- Commit is blocked
- Specific violations are printed
- Developer fixes before re-committing

### GitHub Actions CI

Runs on every PR targeting `main`. Full validation suite.

**Jobs:**

```yaml
validate-skills:
  # Runs validate_skill.py on all changed skills
  # Enforces hard gates (blocks merge on failure)
  # Reports soft gate warnings as PR comments

registry-sync:
  # Verifies every skill directory has a registry.json entry
  # Verifies every registry.json entry has a skill directory
  # Blocks merge on mismatch

pii-scan:
  # Deep PII scan across all files in the PR
  # Checks for emails, names, IDs, phone numbers
  # Blocks merge on any detection

internal-url-scan:
  # Scans for internal/intranet URLs
  # Configurable domain blocklist
  # Blocks merge on any detection

structure-check:
  # Verifies repo structure matches expected layout
  # No files in skills/ subdirectory (pre-universalized)
  # All skill directories at root level
```

---

## Blocked Internal Domains

The following domain patterns are **blocked** by both pre-commit and CI.
Any file containing these patterns will fail the H3 (No Internal URLs) gate.

```
*.walmart.com (except in attribution/credit contexts)
*.wal-mart.com
*.service-now.com/*walmart*
one.walmart.com
dx.walmart.com
wibey.walmart.com
puppy.walmart.com
*.walmart.net
```

**Exception:** The string "Walmart" may appear in plain text for attribution
(e.g., "Built at Walmart" or "Aligned to Walmart AI governance standards").
Only URLs and system references are blocked.

---

## Feedback & Rating System

### How Feedback Is Collected

Feedback is **never** collected by asking users. It is inferred from signals:

| Signal Type | What It Means | Weight |
|-------------|---------------|--------|
| **Clean completion** | Skill worked as expected | +1 use count |
| **Re-use** | Same user activates the skill again | Strong positive |
| **Recommendation** | User describes sharing the skill | Strongest positive |
| **Delight** | "perfect", "exactly", "🔥" language | Positive signal |
| **Abandonment** | Session ends mid-phase | Negative signal |
| **Frustration + completion** | Finished despite friction | Negative signal |
| **Rage quit** | Strong frustration → immediate exit | Critical negative |

### Maturity Score

Each skill has a computed maturity score based on its signals:

```
maturity_score = (
    (clean_completions * 1.0) +
    (reuse_signals * 2.0) +
    (recommendation_signals * 3.0) +
    (delight_signals * 1.5)
    - (abandonments * 2.0)
    - (frustration_completions * 1.5)
    - (rage_quits * 5.0)
) / total_sessions
```

**Score thresholds:**
- `≥ 1.0` — Healthy, eligible for STABLE promotion (if other criteria met)
- `0.5 – 1.0` — Acceptable, monitor for improvement opportunities
- `< 0.5` — At risk, skill-improver should have active proposals
- `< 0.0` — Regression, consider demotion to BETA

---

## Review Process for PRs

### New Skill Submission

1. **CI validates** all hard + soft gates
2. **Reviewer checks:**
   - [ ] Skill solves a real, reusable problem (not too niche, not too vague)
   - [ ] Origin and attribution are accurate
   - [ ] Intake variables make sense for the stated use cases
   - [ ] Example applications demonstrate genuine universality
   - [ ] No team-specific language or context leaks
   - [ ] `maturity_status: beta` (never merge a new skill as stable)
3. **Reviewer approves or requests changes**
4. **Merge → skill enters registry as BETA**

### Skill Improvement

1. **CI validates** changes don't break hard gates
2. **Reviewer checks:**
   - [ ] Change is justified (commit message references improvement evidence)
   - [ ] Version bump follows semver (patch for wording, minor for logic, major for architecture)
   - [ ] No regression in existing capabilities
3. **Merge**

### Maturity Promotion

1. **Promotion PR** includes:
   - Updated `maturity_status: stable` in skill.yaml
   - Updated registry.json entry
   - Summary of evidence (sanitized)
2. **Maintainer reviews evidence** against promotion criteria
3. **Merge → skill is STABLE**

---

## Versioning Rules

### Semver for Skills

| Bump | When | Examples |
|------|------|---------|
| **Patch** (x.x.1) | Wording fixes, typo corrections, clarification of existing intake questions | Intake question reworded for clarity |
| **Minor** (x.1.0) | New phase added, new intake variable, new example applications, logic improvement | Added a validation phase; new source type supported |
| **Major** (x+1.0) | Core architecture change, pipeline redesign, breaking changes to intake | Replaced NMF with BERTopic; intake schema changed |

### Version in Multiple Places

Version must match across:
- `skill.yaml` → `version` field
- `SKILL.md` → YAML front matter `version` field
- `registry.json` → skill entry `version` field

CI validates version consistency.

---

## Registry Rules

### Single Source of Truth

`registry.json` is the authoritative list of all skills in the library.

**Rules:**
1. Every skill directory at root level **must** have an entry in registry.json
2. Every entry in registry.json **must** have a corresponding skill directory
3. CI validates bidirectional sync on every PR
4. No orphan directories. No phantom registry entries.

### Required Registry Fields

```json
{
  "id": "skill-name",
  "name": "Human-Readable Skill Name",
  "version": "1.0.0",
  "description": "One-line description",
  "origin": "created",
  "author": "author-handle",
  "maturity_status": "beta",
  "path": "skill-name",
  "tags": ["tag1", "tag2"],
  "category": "category-id"
}
```

---

## Compliance Alignment

This library aligns to Walmart's AI governance standards as a quality bar.
Public-facing documentation references the *principles* without linking to
internal policy documents.

### Principles We Align To

| Principle | What It Means for Skills |
|-----------|--------------------------|
| **Approved Services** | Skills document which AI services they work with; never hardcode to a single vendor |
| **Data Encryption** | Skills that handle data document encryption expectations |
| **PII Protection** | Skills that may touch PII document de-identification controls |
| **Human Oversight** | Every skill has human-in-the-loop checkpoints |
| **Cost Efficiency** | Model recommendations use minimum necessary power |
| **Bias Awareness** | Skills that analyze text document bias considerations |
| **Audit Logging** | Skills document what should be logged and what should not |

### What Changed from Internal to Public

| Before (Internal) | After (Public) |
|-------------------|---------------|
| Links to `one.walmart.com` policy docs | Principle descriptions without internal links |
| Policy numbers (AI-01-02, DG-01-ST-02) | Generic principle names |
| Internal tool URLs | Platform-agnostic references |
| `@walmart.com` email examples | `@example.com` email examples |
| Team-specific JIRA projects | Generic project references |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-23 | Initial governance — established by @jac007x |
