# Compliance & AI Governance Framework

> **SUBMISSION REQUIREMENT**: All skills submitted to this library MUST be compliant with the governance principles below. Non-compliant skills will not be accepted. Use the [Skill Validation Checker](#skill-validation-checker) to verify compliance before submission.
>
> For the full tiered quality gates (hard blocks vs. soft warnings), see [GOVERNANCE.md](../GOVERNANCE.md).

---

## Governing Principles

This library aligns to enterprise-grade AI governance as a quality bar.
The principles below are genericized from production standards; the specific
policy documents are internal and not linked here.

| Principle | Description | Status |
|-----------|-------------|--------|
| **AI Governance Standard** | Technical guardrails for AI service usage, encryption, RBAC, audit logging, and prompt security | Active |
| **Data De-Identification Standard** | Requirements for classifying, de-identifying, and protecting PII in data flows | Active |
| **Ethical AI Principles** | Responsible use guidelines covering bias mitigation, cost efficiency, human oversight, and data governance | Active |

---

## Skill Compliance Review Status

All skills in this library have been reviewed against the governing principles.

| Skill | Review Date | Reviewer | Principles Checked | Model Rec | Status |
|-------|-------------|----------|-------------------|-----------|--------|
| mbr-engine | 2026-03-18 | @jac007x | AI Governance, De-Identification, Ethical AI | Sonnet | COMPLIANT |
| msgraph-people | 2026-03-18 | @jac007x | AI Governance, Ethical AI | Haiku | COMPLIANT |
| document-processing | 2026-03-18 | @jac007x | AI Governance, De-Identification, Ethical AI | Sonnet | COMPLIANT |
| confluence-people | 2026-03-18 | @jac007x | AI Governance, Ethical AI | Haiku | COMPLIANT |
| jira-people | 2026-03-18 | @jac007x | AI Governance, Ethical AI | Haiku | COMPLIANT |

### Review Attestation

> I attest that each skill listed above has been reviewed against the applicable AI governance principles and complies with all requirements. Any identified risks have appropriate controls documented.
>
> **Reviewer**: @jac007x
> **Date**: 2026-03-18
> **Next Review**: 2026-06-18 (Quarterly)

---

## Model Power Recommendations

Skills should use the **minimum model power necessary** for the task. This saves tokens, reduces cost, and improves response time.

| Model Tier | Use When | Examples |
|------------|----------|----------|
| **Haiku** (or equivalent fast/small model) | Simple lookups, search, formatting, basic extraction | Knowledge-base search, work-item queries, calendar checks, email listing |
| **Sonnet** (or equivalent mid-tier model) | Analysis, pattern detection, moderate complexity, document processing | Metric analysis, PDF extraction, feature detection, form parsing |
| **Opus** (or equivalent frontier model) | Strategic planning, complex reasoning, multi-step decisions, creative tasks | Architecture design, complex problem solving, executive summaries |

### Default Recommendation: Haiku

**Start with Haiku** and only escalate when:
- Task requires nuanced analysis
- Output quality is insufficient
- Multi-step reasoning is needed
- Document is complex/lengthy

### Skill Model Assignments

| Skill | Recommended Model | Rationale |
|-------|-------------------|-----------|
| **mbr-engine** | Sonnet | Pattern detection, metric analysis, slide generation |
| **msgraph-people** | Haiku | API calls, simple formatting, email drafting |
| **document-processing** | Sonnet | PDF/PPTX analysis, chart interpretation |
| **confluence-people** | Haiku | Search queries, result formatting |
| **jira-people** | Haiku | Query construction, ticket operations |

---

## Governance Principles Summary

### AI Governance Standard

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| **Approved Services** | Use only approved, vetted AI services for your organization | Check skill dependencies |
| **Encryption** | Data encrypted in transit and at rest | Uses HTTPS/platform encryption |
| **RBAC** | Role-based access controls in place | Document access requirements |
| **Audit Logging** | Log AI interactions appropriately | Include logging guidance |
| **Prompt Security** | Block banned or sensitive content in prompts | No sensitive content in prompts |
| **PII Protection** | No PII in training data; de-identify per your data governance standard | Document PII handling |

### Data De-Identification Standard

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| **Data Classification** | Identify PII in data flows | Document data types |
| **De-identification Methods** | Apply appropriate techniques (masking, tokenization, aggregation) | Specify when/how to de-identify |
| **Logging Restrictions** | No PII in plain-text logs | Logging guidance included |
| **Retention Limits** | Do not store data beyond need | Storage documentation |

### Ethical AI Principles

| Principle | Requirement | Verification |
|-----------|-------------|--------------|
| **Data Governance** | No sensitive data sent to unapproved external AI services | Check external access |
| **Ethical Usage** | Mitigate bias; maintain regulatory compliance | Bias warnings included |
| **Cost Control** | Efficient model usage; prefer smallest capable model | Model recommendations |
| **Human Oversight** | Human review for critical decisions; no fully autonomous actions on sensitive data | Review requirements documented |

---

## Skill Validation Checker

Before submitting a skill, run the validation checker to verify compliance.

### Usage

```bash
# From the skill library root
python tools/validate_skill.py skills/your-skill/

# Or validate all skills
python tools/validate_skill.py --all
```

### What It Checks

| Check | Description | Required |
|-------|-------------|----------|
| **skill.yaml exists** | Metadata file present | Yes |
| **README.md exists** | Documentation present | Yes |
| **Compliance section** | Compliance documented in README | Yes |
| **Model recommendation** | Model tier specified | Yes |
| **PII handling** | PII risks documented if applicable | Yes |
| **No secrets** | No hardcoded credentials | Yes |
| **Approved services** | Only vetted AI services referenced | Yes |
| **Risk level** | Risk assessment included | Yes |

### Validation Output

```
PASS: skill.yaml exists
PASS: README.md exists
PASS: Compliance section found
PASS: Model recommendation: Haiku
PASS: PII handling documented
PASS: No secrets detected
PASS: Uses approved services only
PASS: Risk level: Low

=======================================
  VALIDATION RESULT: COMPLIANT
  Ready for submission to library
=======================================
```

---

## New Skill Submission Checklist

All skills MUST complete this checklist before submission:

### Required Documentation
- [ ] `skill.yaml` with complete metadata
- [ ] `README.md` with usage documentation
- [ ] Compliance section in README
- [ ] Model recommendation specified

### Governance Compliance
- [ ] **AI Governance**: Uses only approved AI services for your organization
- [ ] **AI Governance**: Authentication via managed identities or secure credential store
- [ ] **De-Identification**: PII handling documented (if applicable)
- [ ] **Ethical AI**: Bias risks documented and mitigated

### Validation
- [ ] Ran `validate_skill.py` -- all checks pass
- [ ] Tested in sandbox environment
- [ ] Peer reviewed

### Submission
- [ ] Created PR with skill files
- [ ] Filled out PR template
- [ ] Requested review from library maintainer

---

## Risk Levels

### Low Risk
- Internal search/lookup (knowledge bases, work management tools)
- Public information retrieval
- Non-sensitive data formatting

**Requirements**: Standard checklist

### Medium Risk
- HR data processing
- Document extraction (possible PII)
- Email/calendar access

**Requirements**: Standard checklist + PII controls + model >= Sonnet for analysis

### High Risk
- Automated decisions affecting people
- Compensation/performance data
- Legal/compliance documents

**Requirements**: Full review by Legal, Security, and relevant data governance stakeholders

---

## Compliance Review Schedule

| Review Type | Frequency | Next Due | Owner |
|-------------|-----------|----------|-------|
| Skill Compliance Audit | Quarterly | 2026-06-18 | @jac007x |
| Governance Alignment Check | Semi-annually | 2026-09-18 | Security liaison |
| New Skill Review | Per submission | Ongoing | Skill Reviewer |

---

## Contact

| Question Type | Contact |
|---------------|---------|
| Technical guidance | Library maintainer (@jac007x) |
| Security review | Your organization's security team |
| Regulatory questions | Your organization's legal team |
| Data governance questions | Your organization's data governance team |

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-18 | Initial compliance framework | @jac007x |
| 1.1 | 2026-03-18 | Added model recommendations, validation checker, governance references | @jac007x |
| 2.0 | 2026-03-23 | Genericized for public repo: removed internal URLs, policy numbers, and team references per DOCTRINE.md | @jac007x |
