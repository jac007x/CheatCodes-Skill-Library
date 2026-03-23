# 📝 CheatCodes Skill Library — Roadmap & Working Notes

> This is the living working memory for the skill library.
> Updated by the skill owner. Committed after every planning session.

---

## 🔄 Active Backlog

### Reconcile `mbr-engine` into `mbr-deck-builder`
The original Python pipeline in `skills/mbr-engine/` has been removed.
`mbr-deck-builder` has a SKILL.md. These need to be reconciled into one
complete skill with working code + SKILL.md aligned.

| Action | Owner | Target |
|--------|-------|--------|
| Reconcile mbr-engine pipeline into mbr-deck-builder | @jac007x | v2.1.0 |
| Validate mbr-deck-builder end-to-end with real data | @jac007x | v2.1.0 |

---

### Marketplace Publish Step
When skills are proven across ≥2 teams, publish to `puppy.walmart.com/marketplace`
so associates can discover them without visiting GitHub.

| Skill | Version | Ladder Stage | Marketplace |
|-------|---------|-------------|-------------|
| survey-nlp-analyzer | 1.1.0 | 🌐 Scale | ❌ Not published |
| org-data-pipeline | 1.0.0 | 🔬 Prove | ❌ Not published |
| mbr-deck-builder | 2.0.0 | 🧪 Refine | ❌ Not published |
| review-cycle-manager | 1.0.0 | 🧪 Refine | ❌ Not published |
| calendar-email-workflow | 1.0.0 | 🧪 Refine | ❌ Not published |
| knowledge-base-workflow | 1.0.0 | 🧪 Refine | ❌ Not published |
| work-management-workflow | 1.0.0 | 🧪 Refine | ❌ Not published |
| document-extraction | 1.0.0 | 🧪 Refine | ❌ Not published |

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
**Status:** Ready — all agenda items pre-completed. Session is now a review + sign-off.

**Pre-completed before session:**
- [x] Branch model: `main` / `dev` split live, protection rules pending
- [x] `review-cycle-manager` v1.0.0 — fully universalized SKILL.md
- [x] `calendar-email-workflow` v1.0.0 — replaces `msgraph-people`
- [x] `document-extraction` v1.0.0 — replaces `document-processing`
- [x] `knowledge-base-workflow` v1.0.0 — replaces `confluence-people`
- [x] `work-management-workflow` v1.0.0 — replaces `jira-people`
- [x] `skills/` subfolder removed from repo
- [x] `docs/COMPLIANCE.md` scrubbed (no internal URLs or policy numbers)
- [x] `designer-orchestrator/audit_results/` removed

**Remaining for session discussion:**
- [ ] Set `main` branch protection in GitHub UI
- [ ] Agree on PR review process and who approves
- [ ] `mbr-deck-builder` reconciliation scope
- [ ] Marketplace publish timing and process
- [ ] Assign peer teams for Prove stage

---

## ✅ Completed

| Date | What |
|------|------|
| 2026-03-20 | Initialized git, connected remote to GitHub |
| 2026-03-20 | Added `skill-universalizer` and `skill-improver` meta-skills |
| 2026-03-20 | `survey-nlp-analyzer` v1.0.0 → v1.1.0 (universalized, scrubbed team refs) |
| 2026-03-20 | Removed `fplus-tech-panel` and `skyward-panel-status` (team-specific) |
| 2026-03-20 | Removed Curated Skills section from README |
| 2026-03-20 | Purged 32 session artifact files from repo |
| 2026-03-20 | Full public-readiness audit across all skills |
| 2026-03-23 | `dev` branch created — branch model live |
| 2026-03-23 | `review-cycle-manager` v1.0.0 written and committed |
| 2026-03-23 | `calendar-email-workflow` v1.0.0 written and committed |
| 2026-03-23 | `document-extraction` v1.0.0 written and committed |
| 2026-03-23 | `knowledge-base-workflow` v1.0.0 written and committed |
| 2026-03-23 | `work-management-workflow` v1.0.0 written and committed |
| 2026-03-23 | `skills/` subfolder removed (all 5 skills replaced) |
| 2026-03-23 | `docs/COMPLIANCE.md` scrubbed — no internal URLs or policy numbers |
| 2026-03-23 | `designer-orchestrator/audit_results/` removed |
