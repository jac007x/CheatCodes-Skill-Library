# CheatCodes Skill Library -- Roadmap & Working Notes

> This is the living working memory for the skill library.
> Updated by the skill owner. Committed after every planning session.

---

## Universalization Backlog

Skills that exist but need to go through `skill-universalizer` before
they can be listed in the library as ready.

### Priority 1 -- Consolidate into `review-cycle-manager`
Two removed team-specific skills that share the same underlying workflow.
Run `skill-universalizer` on both together to produce one universal skill.

| Skill (removed) | What it did | Target universal skill |
|-----------------|------------|------------------------|
| *(removed team-specific skill A)* | Review panel nomination tracking, panelist email automation, calibration reporting | `review-cycle-manager` |
| *(removed team-specific skill B)* | Poll system API for panel feedback status, update tracking spreadsheet | merge into `review-cycle-manager` |

**Design goal:** Map the generalizable pattern. What is a "review cycle"?
Nomination -> Assignment -> Status tracking -> Communications -> Reporting.
What are the intake variables? (system API, spreadsheet schema, email sender, categories, statuses)

---

### Priority 2 -- Universalize the `skills/` subfolder

Original curated skills that have internal content (policy YAML refs,
tool-specific naming, tool-specific README examples). Each needs `skill-universalizer` run
before it can be listed in the main README.

| Skill | Current location | Target universal skill | Notes |
|-------|-----------------|----------------------|-------|
| `msgraph-people` | `skills/msgraph-people/` | `calendar-email-workflow` | Already generic functionality; just needs intake abstracted |
| `document-processing` | `skills/document-processing/` | `document-extraction` | Partially covered by `pptx-expert`; check for overlap |
| `confluence-people` | `skills/confluence-people/` | `knowledge-base-workflow` | Pattern: search -> retrieve -> surface |
| `jira-people` | `skills/jira-people/` | `work-management-workflow` | Pattern: create -> track -> report |
| `mbr-engine` | `skills/mbr-engine/` | reconcile with `mbr-deck-builder` | Python pipeline exists; SKILL.md exists; need to merge |

---

### Priority 3 -- Repo Hygiene (not universalization, just cleanup)

Things that are in the repo but need review before the library is
fully clean for a broad audience.

| Item | Issue | Action |
|------|-------|--------|
| `docs/COMPLIANCE.md` | Had internal URLs and policy numbers | Genericized 2026-03-23 (done) |
| `docs/SKILL-DISCOVERY.md` | Had internal registry URL | Genericized 2026-03-23 (done) |
| `ROADMAP.md` | Had internal location and team references | Genericized 2026-03-23 (done) |
| `designer-orchestrator/audit_results/` | Contains `audit_report.html` and `audit_report.json` that may have internal design data | Review contents; remove if contains internal artifacts |
| `skills/` subfolder (all 5 skills) | Not in README but still in repo; have internal content | Remove from repo once universalized versions are published |
| `docs/search-party-reports/` | Contains Wibey and internal tool references | Review for genericization or move to private |

---

### Priority 4 -- New Doctrine-Aligned Work

Items identified during the 2026-03-23 doctrine alignment pass.

| Item | Description | Status |
|------|-------------|--------|
| **Universalize 3 curated skills** | Select the 3 strongest candidates from `skills/` subfolder and run `skill-universalizer` to produce public-ready SKILL.md + skill.yaml | Planned |
| **Move `session-memory` to root** | The `session-memory` capability is currently nested; relocate to a root-level skill directory per repo structure convention | Planned |
| **Archive 2 skills to private** | Two skills in the backlog are too team-specific to universalize; archive them to the private repo and remove from public | Planned |

---

## Completed

| Date | What |
|------|------|
| 2026-03-23 | Doctrine alignment pass: genericized COMPLIANCE.md, SKILL-DISCOVERY.md, ROADMAP.md to remove all internal URLs, policy numbers, location refs, and team-specific names |
| 2026-03-20 | Initialized git, connected remote to GitHub |
| 2026-03-20 | Added `skill-universalizer` and `skill-improver` meta-skills |
| 2026-03-20 | `survey-nlp-analyzer` v1.0.0 -> v1.1.0 (universalized, scrubbed team refs) |
| 2026-03-20 | Removed team-specific review panel skills (not universalizable as-is) |
| 2026-03-20 | Removed Curated Skills from README (not universalized) |
| 2026-03-20 | Purged 32 session artifact files from repo |
| 2026-03-20 | Full public-readiness audit across all skills |
