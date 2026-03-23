# 📝 CheatCodes Skill Library — Roadmap & Working Notes

> This is the living working memory for the skill library.
> Updated by the skill owner. Committed after every planning session.

---

## 🔄 Universalization Backlog

Skills that exist but need to go through `skill-universalizer` before
they can be listed in the library as ready.

### Priority 1 — Consolidate into `review-cycle-manager`
Two removed skills that share the same underlying workflow.
Run `skill-universalizer` on both together to produce one universal skill.

| Skill (removed) | What it did | Target universal skill |
|-----------------|------------|------------------------|
| `fplus-tech-panel` | Tech panel nomination tracking, panelist email automation, calibration reporting | `review-cycle-manager` |
| `skyward-panel-status` | Poll system API for panel feedback status, update tracking spreadsheet | merge into `review-cycle-manager` |

**Design session goal:** Map the generalizable pattern. What is a "review cycle"?
Nomination → Assignment → Status tracking → Communications → Reporting.
What are the intake variables? (system API, spreadsheet schema, email sender, categories, statuses)

---

### Priority 2 — Universalize the `skills/` subfolder

Original curated skills that have internal content (policy YAML refs, `-people`
naming, tool-specific README examples). Each needs `skill-universalizer` run
before it can be listed in the main README.

| Skill | Current location | Target universal skill | Notes |
|-------|-----------------|----------------------|-------|
| `msgraph-people` | `skills/msgraph-people/` | `calendar-email-workflow` | Already generic functionality; just needs intake abstracted |
| `document-processing` | `skills/document-processing/` | `document-extraction` | Partially covered by `pptx-expert`; check for overlap |
| `confluence-people` | `skills/confluence-people/` | `knowledge-base-workflow` | Pattern: search → retrieve → surface |
| `jira-people` | `skills/jira-people/` | `work-management-workflow` | Pattern: create → track → report |
| `mbr-engine` | `skills/mbr-engine/` | reconcile with `mbr-deck-builder` | Python pipeline exists; SKILL.md exists; need to merge |

---

### Priority 3 — Repo Hygiene (not universalization, just cleanup)

Things that are in the repo but need review before the library is
fully clean for a broad Walmart audience.

| Item | Issue | Action |
|------|-------|--------|
| `docs/COMPLIANCE.md` | Has `one.walmart.com` internal URL and `AI-01-02` / `DG-01-ST-02` policy numbers | Update or move behind a note that says "internal reference" |
| `docs/SKILL-DISCOVERY.md` | Has `wibey.walmart.com/skills` internal URL | Genericize or note as internal |
| `designer-orchestrator/audit_results/` | Contains `audit_report.html` and `audit_report.json` that may have internal design data | Review contents; remove if contains internal artifacts |
| `skills/` subfolder (all 5 skills) | Not in README but still in repo; have internal content | Remove from repo once universalized versions are published |

---

## 🌳 Branch Model

```
main   ← public-facing. Only universalized, ladder-cleared skills.
           Associates discover skills here.
           Nothing merges without a PR.

dev    ← working space. Everything in progress, backlog, experiments.
           This is where skill-universalizer runs happen.
           Default branch for day-to-day work.
```

**The rule:** A skill graduates from `dev` → `main` only after it clears
Refine → Prove on the deployment ladder. Open a PR, review it, merge it.

---

## 🗓️ Planned Sessions

### Design Session — Tuesday March 24, 2026
**Location:** The Hub  
**Goal:** Walk through the universalization backlog. Prioritize what to tackle
first. Define "done" for each skill. Assign owners.

**Agenda:**
1. Branch model walkthrough — `main` / `dev` split, how PRs work
2. `review-cycle-manager` scoping — what is a review cycle universally? What are the intake variables?
3. `skills/` subfolder triage — fast-track vs. needs deeper work
4. Repo hygiene priority order
5. Owners + target versions per skill
6. Marketplace publish step — puppy.walmart.com/marketplace timing

---

## ✅ Completed

| Date | What |
|------|------|
| 2026-03-20 | Initialized git, connected remote to GitHub |
| 2026-03-20 | Added `skill-universalizer` and `skill-improver` meta-skills |
| 2026-03-20 | `survey-nlp-analyzer` v1.0.0 → v1.1.0 (universalized, scrubbed team refs) |
| 2026-03-20 | Removed `fplus-tech-panel` and `skyward-panel-status` (team-specific) |
| 2026-03-20 | Removed Curated Skills from README (not universalized) |
| 2026-03-20 | Purged 32 session artifact files from repo |
| 2026-03-20 | Full public-readiness audit across all skills |
