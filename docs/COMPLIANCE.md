# Walmart AI Compliance Framework

> All skills in this library must comply with Walmart's Ethical AI principles
> and applicable data governance standards before merging to `main`.
> Use the checklist below to verify compliance before opening a PR.

---

## Applicable Standards

| Standard | Description |
|----------|-------------|
| **Ethical AI Principles** | Walmart's principles for responsible use of generative AI |
| **AI Governance Standard** | Technical standards for AI systems at Walmart |
| **De-Identification Standard** | Requirements for handling and de-identifying personal data |

For current policy links, search **WalmartOne** or **ServiceNow Knowledge Base**
for "Generative AI" or contact your InfoSec team.

---

## Model Power Recommendations

Use the **minimum model tier necessary**. This saves cost and improves speed.

| Tier | Use When | Examples |
|------|----------|----------|
| **🟢 Fast** (Haiku / equivalent) | Lookups, search, formatting, basic extraction | Calendar checks, ticket queries, email listing |
| **🟡 Standard** (Sonnet / equivalent) | Analysis, pattern detection, document processing | Report generation, PDF extraction, topic modeling |
| **🔴 Advanced** (Opus / equivalent) | Complex reasoning, strategic planning, multi-step decisions | Architecture design, executive summaries |

**Default:** Start with Fast. Escalate only when output quality is insufficient.

---

## Compliance Checklist (per skill)

Before merging a new skill to `main`, verify:

- [ ] No hardcoded credentials, tokens, or internal URLs
- [ ] No PII committed to the repo (raw data files, sample exports)
- [ ] PII handling documented in SKILL.md if skill touches personal data
- [ ] Intake variables use `{{PLACEHOLDERS}}` — no team-specific defaults
- [ ] Skill has been tested end-to-end by the skill owner
- [ ] Skill has been validated by at least one peer team (Prove stage)
- [ ] Output does not expose data beyond the requesting user's access level
- [ ] Skill description is free of internal team names, program names, or policy numbers

---

## Skill Compliance Status

| Skill | Version | Reviewed | Status |
|-------|---------|----------|--------|
| survey-nlp-analyzer | 1.1.0 | 2026-03-20 | ✅ Compliant |
| org-data-pipeline | 1.0.0 | 2026-03-20 | ✅ Compliant |
| talent-card-generator | 1.0.0 | 2026-03-20 | ✅ Compliant |
| powerbi-reports | 1.0.0 | 2026-03-20 | ✅ Compliant |
| mbr-deck-builder | 2.0.0 | 2026-03-20 | ✅ Compliant |
| pptx-expert | 1.0.0 | 2026-03-20 | ✅ Compliant |
| a11y-wcag-auditor | 1.0.0 | 2026-03-20 | ✅ Compliant |
| data-viz-expert | 1.0.0 | 2026-03-20 | ✅ Compliant |
| design-system-validator | 1.0.0 | 2026-03-20 | ✅ Compliant |
| design-to-code-bridge | 1.0.0 | 2026-03-20 | ✅ Compliant |
| designer-orchestrator | 1.0.0 | 2026-03-20 | ✅ Compliant |
| layout-composition-analyzer | 1.0.0 | 2026-03-20 | ✅ Compliant |
| slide-analyzer | 1.0.0 | 2026-03-20 | ✅ Compliant |
| email-automation-pattern | 1.0.0 | 2026-03-20 | ✅ Compliant |
| task-rabbit | 1.0.0 | 2026-03-20 | ✅ Compliant |
| skill-universalizer | 1.0.0 | 2026-03-20 | ✅ Compliant |
| skill-improver | 1.0.0 | 2026-03-20 | ✅ Compliant |
| calendar-email-workflow | 1.0.0 | pending | ⏳ In progress |
| document-extraction | 1.0.0 | pending | ⏳ In progress |
| knowledge-base-workflow | 1.0.0 | pending | ⏳ In progress |
| work-management-workflow | 1.0.0 | pending | ⏳ In progress |
| review-cycle-manager | 1.0.0 | pending | ⏳ In progress |

---

## Quarterly Review Schedule

All skills should be re-reviewed quarterly to ensure continued compliance
as Walmart policies evolve.

| Quarter | Review Window |
|---------|---------------|
| Q1 2026 | March 2026 |
| Q2 2026 | June 2026 |
| Q3 2026 | September 2026 |
| Q4 2026 | December 2026 |
