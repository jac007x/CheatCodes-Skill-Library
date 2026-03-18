# Walmart AI Compliance Framework

> **⚠️ SUBMISSION REQUIREMENT**: All skills submitted to this library MUST be compliant with the policies listed below. Non-compliant skills will not be accepted. Use the [Skill Validation Checker](#skill-validation-checker) to verify compliance before submission.

---

## Applicable Policies

| Policy | Name | Last Reviewed | Status |
|--------|------|---------------|--------|
| **AI-01-02** | AI Governance Standard | 2026-03-18 | ✅ Active |
| **DG-01-ST-02** | De-Identification Standard | 2026-03-18 | ✅ Active |
| **Ethical AI Principles** | Using Gen AI at Walmart | 2026-03-18 | ✅ Active |

**Policy Sources**:
- [Ethical AI Policy](https://one.walmart.com/content/uswire/en_us/work1/global-governance/technology-and-data-compliance/ethical-ai.html)
- [AI-01-02 Standards](https://one.walmart.com/content/uswire/en_us/work1/policies/non-people-policies/tdc/standards/ai-01-02.html)
- [Using Gen AI at Walmart](https://dx.walmart.com/guides/dx/Using-Gen-AI-at-Walmart-D5d3ku0m53h)
- [Generative AI KB](https://walmartglobal.service-now.com/nav_to.do?uri=%2Fkb_view.do%3Fsysparm_article%3DKB1140910)

---

## Skill Compliance Review Status

All skills in this library have been reviewed against applicable policies.

| Skill | Review Date | Reviewer | Policies Checked | Model Rec | Status |
|-------|-------------|----------|------------------|-----------|--------|
| mbr-engine | 2026-03-18 | @jac007x | AI-01-02, DG-01-ST-02, Ethical AI | Sonnet | ✅ COMPLIANT |
| msgraph-people | 2026-03-18 | @jac007x | AI-01-02, Ethical AI | Haiku | ✅ COMPLIANT |
| document-processing | 2026-03-18 | @jac007x | AI-01-02, DG-01-ST-02, Ethical AI | Sonnet | ✅ COMPLIANT |
| confluence-people | 2026-03-18 | @jac007x | AI-01-02, Ethical AI | Haiku | ✅ COMPLIANT |
| jira-people | 2026-03-18 | @jac007x | AI-01-02, Ethical AI | Haiku | ✅ COMPLIANT |

### Review Attestation

> I attest that each skill listed above has been reviewed against the applicable Walmart AI policies and complies with all requirements. Any identified risks have appropriate controls documented.
>
> **Reviewer**: @jac007x
> **Date**: 2026-03-18
> **Next Review**: 2026-06-18 (Quarterly)

---

## Model Power Recommendations

Skills should use the **minimum model power necessary** for the task. This saves tokens, reduces cost, and improves response time.

| Model Tier | Use When | Examples |
|------------|----------|----------|
| **🟢 Haiku** (or equivalent) | Simple lookups, search, formatting, basic extraction | Confluence search, JIRA queries, calendar checks, email listing |
| **🟡 Sonnet** (or equivalent) | Analysis, pattern detection, moderate complexity, document processing | MBR analysis, PDF extraction, feature detection, form parsing |
| **🔴 Opus** (or equivalent) | Strategic planning, complex reasoning, multi-step decisions, creative tasks | Architecture design, complex problem solving, executive summaries |

### Default Recommendation: Haiku

**Start with Haiku** and only escalate when:
- Task requires nuanced analysis
- Output quality is insufficient
- Multi-step reasoning is needed
- Document is complex/lengthy

### Skill Model Assignments

| Skill | Recommended Model | Rationale |
|-------|-------------------|-----------|
| **mbr-engine** | 🟡 Sonnet | Pattern detection, metric analysis, slide generation |
| **msgraph-people** | 🟢 Haiku | API calls, simple formatting, email drafting |
| **document-processing** | 🟡 Sonnet | PDF/PPTX analysis, chart interpretation |
| **confluence-people** | 🟢 Haiku | Search queries, result formatting |
| **jira-people** | 🟢 Haiku | JQL queries, ticket operations |

---

## Policy Requirements Summary

### AI-01-02 Technical Standards

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| **Approved Services** | Use only Walmart-approved AI (Wibey, Azure OpenAI, Vertex, LLM Gateway) | ✅ Check skill dependencies |
| **Encryption** | Data encrypted in transit and at rest | ✅ Uses HTTPS/platform encryption |
| **RBAC** | Role-based access controls | ✅ Document access requirements |
| **Audit Logging** | Log AI interactions | ✅ Include logging guidance |
| **Prompt Security** | Block banned content | ✅ No sensitive content in prompts |
| **PII Protection** | No PII in training; de-identify per DG-01-ST-02 | ✅ Document PII handling |

### DG-01-ST-02 De-Identification Standard

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| **Data Classification** | Identify PII in data flows | ✅ Document data types |
| **De-identification Methods** | Apply appropriate techniques | ✅ Specify when/how to de-identify |
| **Logging Restrictions** | No PII in plain-text logs | ✅ Logging guidance included |
| **Retention Limits** | Don't store beyond need | ✅ Storage documentation |

### Ethical AI Principles

| Principle | Requirement | Verification |
|-----------|-------------|--------------|
| **Data Governance** | No sensitive data to external AI | ✅ Check external access |
| **Ethical Usage** | Mitigate bias; regulatory compliance | ✅ Bias warnings included |
| **Cost Control** | Efficient model usage | ✅ Model recommendations |
| **Human Oversight** | Human review for critical decisions | ✅ Review requirements documented |

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
| **skill.yaml exists** | Metadata file present | ✅ Yes |
| **README.md exists** | Documentation present | ✅ Yes |
| **Compliance section** | Compliance documented in README | ✅ Yes |
| **Model recommendation** | Model tier specified | ✅ Yes |
| **PII handling** | PII risks documented if applicable | ✅ Yes |
| **No secrets** | No hardcoded credentials | ✅ Yes |
| **Approved services** | Only Walmart-approved AI services | ✅ Yes |
| **Risk level** | Risk assessment included | ✅ Yes |

### Validation Output

```
✅ PASS: skill.yaml exists
✅ PASS: README.md exists
✅ PASS: Compliance section found
✅ PASS: Model recommendation: Haiku
✅ PASS: PII handling documented
✅ PASS: No secrets detected
✅ PASS: Uses approved services only
✅ PASS: Risk level: Low

═══════════════════════════════════════
  VALIDATION RESULT: ✅ COMPLIANT
  Ready for submission to library
═══════════════════════════════════════
```

---

## New Skill Submission Checklist

All skills MUST complete this checklist before submission:

### Required Documentation
- [ ] `skill.yaml` with complete metadata
- [ ] `README.md` with usage documentation
- [ ] Compliance section in README
- [ ] Model recommendation specified

### Policy Compliance
- [ ] **AI-01-02**: Uses only Walmart-approved AI services
- [ ] **AI-01-02**: Authentication via AAD/managed identities
- [ ] **DG-01-ST-02**: PII handling documented (if applicable)
- [ ] **Ethical AI**: Bias risks documented and mitigated

### Validation
- [ ] Ran `validate_skill.py` - all checks pass
- [ ] Tested in sandbox environment
- [ ] Peer reviewed

### Submission
- [ ] Created PR with skill files
- [ ] Filled out PR template
- [ ] Requested review from library maintainer

---

## Risk Levels

### 🟢 Low Risk
- Internal search/lookup (Confluence, JIRA)
- Public information retrieval
- Non-sensitive data formatting

**Requirements**: Standard checklist

### 🟡 Medium Risk
- HR data processing
- Document extraction (possible PII)
- Email/calendar access

**Requirements**: Standard checklist + PII controls + model ≥ Sonnet for analysis

### 🔴 High Risk
- Automated decisions affecting employees
- Compensation/performance data
- Legal/compliance documents

**Requirements**: Full review by Legal, InfoSec, People leadership

---

## Compliance Review Schedule

| Review Type | Frequency | Next Due | Owner |
|-------------|-----------|----------|-------|
| Skill Compliance Audit | Quarterly | 2026-06-18 | @jac007x |
| Policy Alignment Check | Semi-annually | 2026-09-18 | InfoSec liaison |
| New Skill Review | Per submission | Ongoing | Skill Reviewer |

---

## Contact

| Question Type | Contact |
|---------------|---------|
| Technical guidance | GenAI Enablement Team |
| Security review | InfoSec |
| Regulatory questions | Legal |
| HR data questions | People Data Governance |

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-18 | Initial compliance framework | @jac007x |
| 1.1 | 2026-03-18 | Added model recommendations, validation checker, policy references | @jac007x |
