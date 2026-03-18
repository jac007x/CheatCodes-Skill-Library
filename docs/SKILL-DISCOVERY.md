# Skill Discovery & Curation Process

## Overview

The skills library grows through two channels:
- **Created** 🛠️ - Skills built in-house from scratch
- **Curated** 📚 - Skills discovered externally and adapted for our use
- **Forked** 🔱 - Open source skills customized for internal needs

This document defines how to systematically discover, evaluate, and curate skills from external resources.

---

## Skill Classification

| Source Type | Badge | Description | Example |
|-------------|-------|-------------|---------|
| **Created** | 🛠️ | Built from scratch internally | MBR Engine |
| **Curated** | 📚 | Discovered externally, adapted | Prompt templates from Anthropic Cookbook |
| **Forked** | 🔱 | Forked from OSS, customized | Modified LangChain tool |

### Registry Entry Format

```json
{
  "id": "skill-name",
  "name": "Skill Display Name",
  "source": "curated",           // created | curated | forked
  "source_url": "https://...",   // Original source (null for created)
  "curator": "jac007x",          // Who found/adapted it
  "curation_date": "2026-03-18",
  ...
}
```

---

## Discovery Sources

### Primary Sources (Check Monthly)

| Source | URL | What to Look For |
|--------|-----|------------------|
| **Wibey Registry** | wibey.walmart.com/skills | Official Walmart skills |
| **MCP Servers** | github.com/modelcontextprotocol/servers | Protocol-native tools |
| **Anthropic Cookbook** | github.com/anthropics/anthropic-cookbook | Patterns & recipes |
| **LangChain Tools** | python.langchain.com/docs/integrations/tools | AI agent tools |
| **GitHub Awesome Lists** | github.com/topics/awesome | Curated tool lists |

### Secondary Sources (Check Quarterly)

| Source | What to Look For |
|--------|------------------|
| **Hacker News** | Trending AI/automation tools |
| **Reddit r/LocalLLaMA** | Community tool discoveries |
| **Product Hunt** | New developer tools |
| **Internal Slack #ai-tools** | Team discoveries |

---

## Discovery Workflow

### Trigger: Monthly Search Party

**When**: Second week of each month (after monthly skill review)
**Duration**: 1-2 hours
**Who**: Any contributor

#### Step 1: Source Scan (30 min)

Run through each primary source looking for:
- [ ] New tools since last scan
- [ ] Updated versions of known tools
- [ ] Popular/trending items
- [ ] Tools matching our gap analysis

#### Step 2: Quick Evaluation (30 min)

For each candidate, score:

| Criteria | Score 1-5 | Notes |
|----------|-----------|-------|
| **Relevance** | | Does it solve a problem we have? |
| **Quality** | | Well-documented? Maintained? |
| **Adaptability** | | Easy to integrate/customize? |
| **License** | | Compatible with internal use? |

**Pass threshold**: Average score ≥ 3.5

#### Step 3: Document Candidates (30 min)

Create a GitHub issue using the "Curate Skill" template for each passing candidate.

---

## Curation Process

### Phase 1: Evaluation

```
Discovery → Quick Score → Deep Evaluation → Decision
```

**Deep Evaluation Checklist**:
- [ ] Test the tool/skill in isolation
- [ ] Review source code (if OSS)
- [ ] Check dependencies for conflicts
- [ ] Verify license compatibility
- [ ] Assess maintenance activity
- [ ] Estimate adaptation effort

### Phase 2: Adaptation

If approved for curation:

1. **Fork or Copy** - Bring into our repo
2. **Adapt** - Modify for internal standards
3. **Document** - Write our documentation
4. **Test** - Verify in our environment
5. **Register** - Add to registry.json

### Phase 3: Attribution

Always maintain attribution:

```markdown
## Attribution

This skill is curated from [Original Name](original_url).
- **Original Author**: @author_name
- **License**: MIT (or applicable)
- **Curated By**: @jac007x
- **Curation Date**: 2026-03-18
- **Modifications**: [List what was changed]
```

---

## Search Party Triggers

### Automatic Triggers

| Trigger | Action |
|---------|--------|
| **Monthly CI Review** | Run discovery workflow |
| **Gap identified in roadmap** | Targeted search for solutions |
| **User requests skill** | Check if exists externally first |
| **New source emerges** | Add to sources, initial scan |

### Manual Triggers

Anyone can trigger a search party by:

1. **Create issue** with label `search-party`
2. **Specify focus** - Category or problem area
3. **Assign scout** - Who will run the search
4. **Set deadline** - When findings are due

### Search Party Issue Template

```markdown
## Search Party Request

**Focus Area**: [e.g., "PDF manipulation tools"]
**Problem to Solve**: [What gap are we filling?]
**Sources to Check**:
- [ ] Source 1
- [ ] Source 2

**Scout**: @username
**Due Date**: YYYY-MM-DD
```

---

## Evaluation Rubric

### License Compatibility

| License | Compatible? | Notes |
|---------|-------------|-------|
| MIT | ✅ Yes | Preferred |
| Apache 2.0 | ✅ Yes | Preferred |
| BSD | ✅ Yes | Check variant |
| GPL | ⚠️ Maybe | Legal review needed |
| Proprietary | ❌ No | Cannot curate |
| No License | ❌ No | Cannot curate |

### Maintenance Health

| Indicator | Green | Yellow | Red |
|-----------|-------|--------|-----|
| Last commit | < 3 months | 3-12 months | > 1 year |
| Open issues | Actively triaged | Some stale | Abandoned |
| Contributors | 2+ active | 1 active | None |
| Documentation | Complete | Partial | Missing |

### Adaptation Effort

| Effort Level | Estimate | Examples |
|--------------|----------|----------|
| **Low** | < 4 hours | Config changes, wrapper |
| **Medium** | 4-16 hours | Significant customization |
| **High** | 16-40 hours | Major rewrite |
| **Very High** | 40+ hours | Consider creating instead |

---

## Curation Log

Track all discoveries and decisions:

```markdown
## Curation Log - Q1 2026

| Date | Candidate | Source | Score | Decision | Notes |
|------|-----------|--------|-------|----------|-------|
| 2026-03-18 | Tool A | MCP Servers | 4.2 | ✅ Curate | Good fit for reporting |
| 2026-03-18 | Tool B | Awesome Lists | 2.8 | ❌ Pass | Too specialized |
| 2026-03-18 | Tool C | LangChain | 3.5 | ⏸️ Defer | Wait for v2 |
```

---

## Integration Checklist

Before a curated skill goes live:

- [ ] **Legal Review** - License verified
- [ ] **Security Review** - Dependencies scanned
- [ ] **Adaptation Complete** - Customized for internal use
- [ ] **Documentation** - README, usage examples
- [ ] **Tests** - Basic validation passes
- [ ] **Registry Entry** - Added to registry.json with source metadata
- [ ] **Attribution** - Original source credited

---

## Best Practices

### Do's
- ✅ Credit original authors
- ✅ Document all modifications
- ✅ Check licenses before curating
- ✅ Test thoroughly before adding
- ✅ Keep original source URL for updates

### Don'ts
- ❌ Strip attribution from code
- ❌ Curate without license check
- ❌ Fork abandoned projects without plan
- ❌ Add untested skills to registry
- ❌ Ignore security scan results
