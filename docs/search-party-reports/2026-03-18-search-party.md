# Search Party Report - March 2026

**Date**: 2026-03-18
**Scout**: @jac007x (via Wibey)
**Focus**: People/HR function skills + General productivity
**Duration**: ~1 hour

---

## Executive Summary

Scanned 6 primary sources for skills relevant to People function and general productivity:
- ✅ Wibey Skills Registry (25 agents, 14 MCP servers)
- ✅ MCP Servers Directory (official + community)
- ✅ Anthropic Cookbook (patterns & recipes)
- ✅ GitHub HR Analytics repos
- ✅ GitHub Employee Engagement repos
- ✅ LangChain Tools ecosystem

**Results**:
- 6 skills recommended for curation
- 2 existing skills to document
- 2 high-priority skills to BUILD (Calendar, Email)

---

## Candidate Evaluation

### Scoring Criteria
| Score | Meaning |
|-------|---------|
| 5 | Excellent - perfect fit |
| 4 | Good - strong candidate |
| 3 | Acceptable - some limitations |
| 2 | Weak - significant gaps |
| 1 | Poor - not recommended |

**Pass Threshold**: Average ≥ 3.5

---

## Category A: People/HR Focused Skills

### 1. ✅ PEOPLE-API-AGENT (Wibey)
**Source**: Wibey Registry
**Type**: 📚 Curate (adapt for library)

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 5 | Direct People API integration |
| Quality | 4 | Already production-ready |
| Adaptability | 4 | Documented, patterns exist |
| License | 5 | Internal - no issues |
| **Average** | **4.5** | ✅ **RECOMMEND** |

**Use Cases**: Employee data lookup, org hierarchy, associate info

---

### 2. ✅ Horilla HR Platform
**Source**: GitHub (1.1k ⭐)
**URL**: https://github.com/horilla-opensource/horilla
**Type**: 🔱 Fork candidate

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 5 | Full HR/CRM platform |
| Quality | 4 | Active, well-documented |
| Adaptability | 3 | Large codebase, extract modules |
| License | 5 | Open source |
| **Average** | **4.25** | ✅ **RECOMMEND** |

**Modules to Extract**:
- Attendance tracking patterns
- Leave management workflows
- Recruitment pipeline logic
- Payroll calculation templates

---

### 3. ✅ Exit Narrative Generator
**Source**: GitHub (17 ⭐)
**Type**: 📚 Curate

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 5 | Attrition analysis - perfect for MBR |
| Quality | 3 | Smaller project, needs review |
| Adaptability | 4 | Focused scope, easy to integrate |
| License | 4 | Check required |
| **Average** | **4.0** | ✅ **RECOMMEND** |

**Value**: Counterfactual analysis for employee departures, retention dynamics

---

### 4. ⏸️ HR Analytics Dashboard (Tableau)
**Source**: GitHub (25 ⭐)
**Type**: 📚 Curate patterns

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 4 | HR dashboards, KPIs |
| Quality | 3 | Visualization focused |
| Adaptability | 3 | Tableau-specific |
| License | 4 | Check required |
| **Average** | **3.5** | ⏸️ **DEFER** - Extract patterns only |

---

### 5. ❌ HR Analytics KPI Dashboard (Power BI)
**Source**: GitHub (21 ⭐)

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 4 | Gender diversity metrics |
| Quality | 3 | Power BI specific |
| Adaptability | 2 | Platform locked |
| License | 3 | Unknown |
| **Average** | **3.0** | ❌ **PASS** |

---

## Category B: Document & Reporting Skills

### 6. ✅ PDF Processing (Anthropic Cookbook)
**Source**: Anthropic Cookbook
**Type**: 📚 Curate

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 5 | PDF upload/summarization |
| Quality | 5 | Official Anthropic pattern |
| Adaptability | 5 | Ready to use |
| License | 5 | MIT |
| **Average** | **5.0** | ✅ **RECOMMEND** |

**Skills to Extract**:
- PDF text extraction
- Multi-page summarization
- Form data extraction
- Chart/graph interpretation

---

### 7. ✅ PowerPoint Reading (Anthropic Cookbook)
**Source**: Anthropic Cookbook
**Type**: 📚 Curate

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 5 | PPTX content extraction |
| Quality | 5 | Official pattern |
| Adaptability | 5 | Complements MBR Engine |
| License | 5 | MIT |
| **Average** | **5.0** | ✅ **RECOMMEND** |

---

### 8. ✅ Form Content Extraction (Anthropic Cookbook)
**Source**: Anthropic Cookbook
**Type**: 📚 Curate

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 5 | Structured data from forms |
| Quality | 5 | Official pattern |
| Adaptability | 5 | Survey/intake processing |
| License | 5 | MIT |
| **Average** | **5.0** | ✅ **RECOMMEND** |

---

## Category C: Collaboration & Productivity

### 9. ✅ Confluence Agent (Wibey)
**Source**: Wibey Registry + MCP Server
**Type**: Already available - document usage

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 5 | Team knowledge search |
| Quality | 5 | Production ready |
| Adaptability | 5 | MCP protocol |
| License | 5 | Internal |
| **Average** | **5.0** | ✅ **DOCUMENT USAGE** |

---

### 10. ✅ JIRA Agent (Wibey)
**Source**: Wibey Registry + MCP Server
**Type**: Already available - document usage

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 5 | Work item management |
| Quality | 5 | Production ready |
| Adaptability | 5 | MCP protocol |
| License | 5 | Internal |
| **Average** | **5.0** | ✅ **DOCUMENT USAGE** |

---

### 11. ✅ Memory/Knowledge Graph (MCP)
**Source**: MCP Servers Directory
**Type**: 📚 Curate

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 4 | Persistent context for agents |
| Quality | 5 | Official MCP reference |
| Adaptability | 4 | Protocol native |
| License | 5 | MIT |
| **Average** | **4.5** | ✅ **RECOMMEND** |

**Value**: Maintain context across sessions, remember user preferences

---

### 12. ⏸️ Sequential Thinking (MCP)
**Source**: MCP Servers Directory
**Type**: 📚 Curate candidate

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 3 | Problem-solving patterns |
| Quality | 5 | Official reference |
| Adaptability | 3 | Specialized use case |
| License | 5 | MIT |
| **Average** | **4.0** | ⏸️ **DEFER** |

---

## Category D: Data & Analytics

### 13. ✅ Unstructured (LangChain)
**Source**: LangChain Ecosystem
**Type**: 📚 Curate

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 5 | Multi-format document parsing |
| Quality | 5 | Well-maintained, popular |
| Adaptability | 4 | Python native |
| License | 5 | Apache 2.0 |
| **Average** | **4.75** | ✅ **RECOMMEND** |

**Formats**: PDF, DOCX, XLSX, HTML, images, emails

---

### 14. ⏸️ BigQuery MCP (Wibey)
**Source**: Wibey MCP Servers
**Type**: Available - assess relevance

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 3 | Data warehouse queries |
| Quality | 4 | Production MCP |
| Adaptability | 3 | Needs BigQuery access |
| License | 5 | Internal |
| **Average** | **3.75** | ⏸️ **ASSESS** if People data in BQ |

---

### 15. ❌ Private GPT (Employee Engagement)
**Source**: GitHub (60 ⭐)

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 3 | Internal chatbots |
| Quality | 3 | Azure specific |
| Adaptability | 2 | Heavy infrastructure |
| License | 3 | Unknown |
| **Average** | **2.75** | ❌ **PASS** |

---

## Category E: Engagement & Surveys

### 16. ⏸️ Alignify (Engagement Platform)
**Source**: GitHub
**Type**: Evaluate further

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 4 | AI-powered engagement |
| Quality | 2 | Limited documentation |
| Adaptability | 2 | Full platform, not modular |
| License | 3 | Unknown |
| **Average** | **2.75** | ❌ **PASS** |

---

### 17. ⏸️ PointD-Pal (Slack Recognition Bot)
**Source**: GitHub
**Type**: Pattern reference

| Criteria | Score | Notes |
|----------|-------|-------|
| Relevance | 4 | Peer recognition |
| Quality | 3 | Slack-specific |
| Adaptability | 3 | Extract patterns |
| License | 4 | OSS |
| **Average** | **3.5** | ⏸️ **DEFER** - Pattern reference only |

---

## Summary Table

| # | Candidate | Source | Score | Decision |
|---|-----------|--------|-------|----------|
| 1 | PDF Processing | Anthropic | 5.0 | ✅ Curate |
| 2 | PowerPoint Reading | Anthropic | 5.0 | ✅ Curate |
| 3 | Form Extraction | Anthropic | 5.0 | ✅ Curate |
| 4 | Unstructured Parser | LangChain | 4.75 | ✅ Curate |
| 5 | People API Agent | Wibey | 4.5 | ✅ Curate |
| 6 | Memory/Knowledge Graph | MCP | 4.5 | ✅ Curate |
| 7 | Confluence Agent | Wibey | 5.0 | 📝 Document usage |
| 8 | JIRA Agent | Wibey | 5.0 | 📝 Document usage |
| 9 | MS Graph (Calendar/Email) | Wibey | - | 🔨 **BUILD** (High Priority) |
| 10 | Sequential Thinking | MCP | 4.0 | ⏸️ Defer |
| 11 | BigQuery MCP | Wibey | 3.75 | ⏸️ Assess |

**Removed from consideration:**
- Horilla HR Platform - Full platform overkill, patterns not unique
- Exit Narrative Generator - Too academic/niche for practical use

---

## Recommended Actions

### Immediate (This Week)
1. **Create curation issues** for top 8 candidates
2. **Document Confluence/JIRA** usage patterns for People function
3. **Test PDF/PPTX** patterns from Anthropic Cookbook

### Short-term (This Month)
4. **Evaluate Horilla modules** for extraction
5. **Prototype Exit Narrative** integration with MBR Engine
6. **Set up Unstructured** for document processing pipeline

### Backlog
7. Assess BigQuery MCP relevance for People data
8. Extract engagement patterns from PointD-Pal
9. Review HR Dashboard visualizations for inspiration

---

## Gaps Identified

| Gap | Priority | Notes |
|-----|----------|-------|
| **Calendar/Scheduling** | 🔴 HIGH | MS Graph available - needs skill wrapper |
| **Email automation** | 🔴 HIGH | Outlook integration critical for People workflows |
| **Survey/Pulse tools** | High | No good candidates found |
| **Learning/Training** | Medium | No candidates found |
| **Performance review** | Medium | Could build custom |

### Priority Skills to Build

#### 1. Calendar Skill (HIGH)
- Meeting scheduling and availability
- Calendar analytics (time in meetings, patterns)
- Recurring meeting management
- Integration with MS Graph API

#### 2. Email Skill (HIGH)
- Email drafting and templates
- Inbox triage and summarization
- Follow-up tracking
- Bulk communication for People workflows

---

## Code Puppy Learnings to Incorporate

> *@jac007x has Code Puppy running calendar/email automation. Capture learnings here.*

### What's Working Well
- [ ] TODO: Document successful patterns

### Pain Points / Gotchas
- [ ] TODO: Document issues encountered

### Feature Ideas
- [ ] TODO: List desired capabilities

### Architecture Notes
- [ ] TODO: How is it structured? What can we reuse?

---

## Next Search Party Focus

**Recommended for April 2026**:
1. Survey/feedback collection tools
2. Calendar management patterns
3. Learning management integrations
4. Performance review workflows

---

## Appendix: Sources Checked

| Source | URL | Items Found |
|--------|-----|-------------|
| Wibey Agents | Internal | 25 agents |
| Wibey MCP Servers | Internal | 14 servers |
| MCP Servers Directory | github.com/modelcontextprotocol/servers | 15+ servers |
| Anthropic Cookbook | github.com/anthropics/anthropic-cookbook | 20+ patterns |
| GitHub HR Analytics | github.com/topics/hr-analytics | 10+ repos |
| GitHub Employee Engagement | github.com/topics/employee-engagement | 8+ repos |
| LangChain Tools | docs.langchain.com | 15+ integrations |
