# Confluence for People Function

📚 **Source**: Wibey Confluence Agent
**Category**: Knowledge Management, Documentation

Leverage Confluence for People team knowledge management and documentation workflows.

---

## Overview

The Confluence Agent enables AI-powered search and interaction with Walmart's Confluence spaces. For People function, this means quick access to:

- HR policies and procedures
- Team documentation and playbooks
- Onboarding guides
- Process documentation
- Meeting notes and decisions

## Quick Start

```bash
# Invoke via Wibey
/confluence

# Or use the MCP tool directly
mcp__confluence__search "HR policy vacation"
```

---

## People Function Use Cases

### 1. Policy Lookup

**Scenario**: Quick answer about HR policy

```
"What's our policy on remote work?"
"How many vacation days do new hires get?"
"What's the process for requesting FMLA?"
```

**Confluence Search**:
```bash
# Search for policy content
confluence search "remote work policy"
confluence search "vacation PTO policy"
confluence search "FMLA leave process"
```

### 2. Onboarding Documentation

**Scenario**: Find onboarding resources for new hire

```
"Find the new hire checklist for Tech org"
"What's the 30-60-90 day plan template?"
"Where's the buddy program guide?"
```

**Confluence Search**:
```bash
confluence search "new hire onboarding checklist Tech"
confluence search "30 60 90 day plan template"
confluence search "buddy program guide"
```

### 3. Process Documentation

**Scenario**: Look up People processes

```
"How do we handle performance improvement plans?"
"What's the exit interview process?"
"Find the promotion criteria documentation"
```

### 4. Meeting Notes & Decisions

**Scenario**: Find historical context

```
"Find notes from last People Leadership meeting"
"What was decided about the new benefits plan?"
"Search for Q1 talent review notes"
```

---

## Search Patterns

### Effective Search Queries

| Goal | Query Pattern | Example |
|------|---------------|---------|
| Find policy | `[topic] policy` | "vacation policy" |
| Find process | `[action] process procedure` | "termination process" |
| Find template | `[type] template` | "offer letter template" |
| Find guide | `[topic] guide how to` | "onboarding guide" |
| Find meeting notes | `[meeting name] notes [date]` | "People sync notes March" |

### Filtering Results

```bash
# Search within specific space
confluence search "vacation policy" --space "HR-Policies"

# Search recent content
confluence search "benefits update" --updated-after "2026-01-01"

# Search by author
confluence search "org changes" --author "john.smith"
```

---

## Common People Confluence Spaces

| Space | Content Type |
|-------|--------------|
| HR-Policies | Official policies, compliance |
| People-Ops | Processes, procedures, playbooks |
| Onboarding | New hire resources, checklists |
| L&D | Training materials, development |
| Benefits | Benefits info, enrollment guides |
| People-Team | Team docs, meeting notes |

---

## Integration Workflows

### MBR Preparation

```
1. Search for previous MBR notes
2. Find org context documentation
3. Look up metric definitions
4. Reference threshold rationale
```

### New Hire Support

```
1. Find onboarding checklist
2. Locate team-specific guides
3. Search for buddy materials
4. Get policy quick-reference
```

### Policy Questions

```
1. Search for relevant policy
2. Find related procedures
3. Locate exception process
4. Identify policy owner
```

---

## Best Practices

### Search Tips
- ✅ Use specific keywords, not full sentences
- ✅ Include space names when known
- ✅ Combine topic + document type
- ✅ Use quotes for exact phrases

### Content Creation
- ✅ Tag pages with relevant labels
- ✅ Use consistent naming conventions
- ✅ Link related pages
- ✅ Keep content current

### Don'ts
- ❌ Search for sensitive data (PII, compensation)
- ❌ Assume search results are current policy
- ❌ Share Confluence links externally without permission

---

## Compliance

### Walmart AI Compliance Status: ✅ Compliant

| Requirement | Status | Notes |
|-------------|--------|-------|
| **Approved AI Services** | ✅ | Uses Wibey (Walmart-approved) |
| **Data Governance** | ✅ | Searches internal Confluence only |
| **PII Handling** | ✅ | Low PII risk - documentation content |
| **External Access** | ✅ | Internal Walmart system only |
| **Authentication** | ✅ | Uses Walmart SSO |

### Data Handling

- Input: Search queries to internal Confluence
- Processing: Wibey agent searches internal content
- Output: Documentation snippets and links
- Storage: No persistent storage

### Risk Level: Low

Internal documentation search with:
- Walmart authentication
- Internal content only
- No external data access

### Best Practices

- ✅ Search for documentation, not PII
- ✅ Verify content is current before relying on it
- ❌ Don't search for compensation/salary data
- ❌ Don't share Confluence links externally

See [COMPLIANCE.md](../../docs/COMPLIANCE.md) for full framework.

---

## Attribution

- **Original**: Wibey Confluence Agent
- **Documented By**: @jac007x
- **Documentation Date**: 2026-03-18
