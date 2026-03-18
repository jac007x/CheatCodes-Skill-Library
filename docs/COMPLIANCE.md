# Walmart AI Compliance Framework

All skills in this library must comply with Walmart's Ethical AI principles and AI governance standards.

---

## Compliance Requirements

### 1. Ethical AI Principles

| Principle | Requirement | How We Comply |
|-----------|-------------|---------------|
| **Data Governance** | No sensitive data to external AI; unbiased data; no copyright infringement | Skills use Walmart-approved AI services only; no external data transmission |
| **Ethical Usage** | Comply with regulations; mitigate bias; controlled experiments | Skills include bias warnings; recommend sandbox testing |
| **Cost Control** | Monitor costs; clear goals; leverage open-source | Skills document cost implications; use efficient patterns |
| **Vendor Flexibility** | Avoid lock-in to single vendor | Skills designed to work with multiple LLM providers |
| **Stay Current** | Adapt to new practices and regulations | Regular skill reviews; version updates |
| **Collaboration** | Share best practices across teams | Open skill library; documentation |

### 2. AI-01-02 Technical Standards

| Standard | Requirement | How We Comply |
|----------|-------------|---------------|
| **Approved Services** | Use only Walmart-approved AI (Azure OpenAI, Vertex, Walmart LLM Gateway) | Skills specify approved service requirements |
| **Encryption** | Data encrypted in transit and at rest | Use HTTPS; leverage platform encryption |
| **RBAC** | Role-based access controls | Skills document access requirements |
| **Audit Logging** | Log all AI interactions | Skills include logging guidance |
| **Prompt Security** | Block banned content; enforce disallow lists | No hardcoded prompts with sensitive content |
| **PII Protection** | No PII in model training; de-identify per DG-01-ST-02 | Skills warn about PII handling; provide de-identification guidance |
| **Access Controls** | AAD principals; managed identities | Skills use Walmart auth patterns |

### 3. Governance Requirements

| Requirement | Status |
|-------------|--------|
| Use Case Submission | Required before production deployment |
| Sandbox Testing | Recommended for all skills |
| Legal Review | Required for sensitive/regulated data |
| InfoSec Review | Required for external data access |

---

## Skill Compliance Status

| Skill | Data Risk | PII Risk | External Access | Compliance Status |
|-------|-----------|----------|-----------------|-------------------|
| mbr-engine | Medium | ⚠️ Yes (HR data) | No | ✅ Compliant with controls |
| msgraph-people | Low | ⚠️ Yes (email/calendar) | Yes (M365) | ✅ Compliant - uses approved M365 |
| document-processing | Medium | ⚠️ Possible | No | ✅ Compliant with controls |
| confluence-people | Low | Low | No (internal) | ✅ Compliant |
| jira-people | Low | Low | No (internal) | ✅ Compliant |

---

## Compliance Checklist for New Skills

Before adding a skill to the library, verify:

### Data Handling
- [ ] No sensitive data sent to external/unapproved AI services
- [ ] PII handling documented with de-identification guidance
- [ ] Data sources are Walmart-approved
- [ ] No hardcoded credentials or secrets

### Security
- [ ] Uses Walmart-approved authentication (AAD, managed identities)
- [ ] Follows RBAC principles
- [ ] Includes audit logging guidance
- [ ] No banned content in prompts

### Governance
- [ ] Use case documented
- [ ] Risk level assessed (Low/Medium/High)
- [ ] Legal/InfoSec review completed (if required)
- [ ] Sandbox testing completed

### Ethical AI
- [ ] Bias risks documented and mitigated
- [ ] Human oversight preserved for critical decisions
- [ ] Output accuracy disclaimers included
- [ ] Cost implications documented

---

## Risk Levels

### Low Risk
- Internal documentation search
- Public information retrieval
- Non-sensitive data processing

**Requirements**: Standard compliance checklist

### Medium Risk
- HR data processing
- Employee information handling
- Document extraction with potential PII

**Requirements**: Standard checklist + PII controls + manager review

### High Risk
- Automated decisions affecting employees
- Compensation or performance data
- Legal or compliance documents

**Requirements**: Full review by Legal, InfoSec, and People leadership

---

## PII Handling Guidelines

When skills may process PII (names, employee IDs, performance data):

### Do's
- ✅ Process PII only in Walmart-approved environments
- ✅ Apply de-identification when storing/logging
- ✅ Limit PII access to authorized users
- ✅ Document what PII is processed and why
- ✅ Include data retention guidance

### Don'ts
- ❌ Send PII to external AI services
- ❌ Log PII in plain text
- ❌ Store PII beyond retention requirements
- ❌ Share PII without authorization
- ❌ Use PII for model training

---

## Compliance Review Schedule

| Review Type | Frequency | Owner |
|-------------|-----------|-------|
| Skill Compliance Audit | Quarterly | Skill Library Owner |
| Policy Alignment Check | Semi-annually | InfoSec liaison |
| New Skill Review | Per submission | Skill Reviewer |

---

## References

- [Using Gen AI at Walmart](https://dx.walmart.com/guides/dx/Using-Gen-AI-at-Walmart-D5d3ku0m53h)
- [Generative AI KB Article](https://walmartglobal.service-now.com/nav_to.do?uri=%2Fkb_view.do%3Fsysparm_article%3DKB1140910)
- Walmart De-Identification Standard DG-01-ST-02
- AI-01-02 Standards (internal policy library)

---

## Contact

For compliance questions:
- **GenAI Enablement Team**: For technical guidance
- **InfoSec**: For security reviews
- **Legal**: For regulatory questions
- **People Data Governance**: For HR data questions
