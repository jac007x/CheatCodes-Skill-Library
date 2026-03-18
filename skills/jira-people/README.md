# JIRA for People Function

📚 **Source**: Wibey JIRA Agent
**Category**: Work Management, Task Tracking

Leverage JIRA for People team work management, request tracking, and project coordination.

---

## Overview

The JIRA Agent enables AI-powered interaction with Walmart's JIRA. For People function, this means:

- Tracking People requests and tickets
- Managing People projects and initiatives
- Querying work status and progress
- Creating and updating tickets

## Quick Start

```bash
# Invoke via Wibey
/jira

# Search for issues
jira search "project = PEOPLE AND status = Open"
```

---

## People Function Use Cases

### 1. Request Tracking

**Scenario**: Track People team service requests

```
"Show me open People requests"
"What tickets are assigned to me?"
"Find blocked items in People Ops"
```

**JIRA Queries**:
```
# Open requests in People project
project = PEOPLE AND status in (Open, "In Progress")

# My assigned tickets
assignee = currentUser() AND status != Done

# Blocked items
project = PEOPLE AND status = Blocked
```

### 2. Initiative Tracking

**Scenario**: Monitor People initiatives and projects

```
"What's the status of the Benefits Refresh project?"
"Show Q1 People initiatives"
"Find overdue items in Onboarding epic"
```

**JIRA Queries**:
```
# Specific epic status
"Epic Link" = PEOPLE-123

# Q1 initiatives
project = PEOPLE AND labels = Q1-2026 AND type = Epic

# Overdue items
project = PEOPLE AND duedate < now() AND status != Done
```

### 3. Reporting & Metrics

**Scenario**: Generate People team metrics

```
"How many tickets did we close this week?"
"What's our average resolution time?"
"Show ticket volume by category"
```

**JIRA Queries**:
```
# Closed this week
project = PEOPLE AND resolved >= startOfWeek()

# By category/component
project = PEOPLE AND component = "Employee Relations"

# SLA tracking
project = PEOPLE AND "Time to Resolution" > 5d
```

### 4. Workload Management

**Scenario**: Balance team workload

```
"Show workload by team member"
"Who has capacity for new work?"
"Find unassigned tickets"
```

**JIRA Queries**:
```
# Unassigned tickets
project = PEOPLE AND assignee is EMPTY AND status = Open

# Team member workload
project = PEOPLE AND assignee = "john.smith" AND status in (Open, "In Progress")
```

---

## Common JQL Patterns for People

### Status Queries

| Need | JQL Pattern |
|------|-------------|
| Open items | `status in (Open, "To Do", "In Progress")` |
| Completed | `status in (Done, Closed, Resolved)` |
| Blocked | `status = Blocked OR labels = blocked` |
| Needs attention | `status = "Needs Info" OR status = "Waiting"` |

### Time-Based Queries

| Need | JQL Pattern |
|------|-------------|
| Created today | `created >= startOfDay()` |
| Due this week | `duedate >= startOfWeek() AND duedate <= endOfWeek()` |
| Overdue | `duedate < now() AND status != Done` |
| Updated recently | `updated >= -7d` |
| Stale (no updates) | `updated <= -14d AND status != Done` |

### People-Specific Queries

```jql
# HR Service Requests
project = PEOPLE AND type = "Service Request"

# Policy Change Requests
project = PEOPLE AND component = "Policy" AND type = "Change Request"

# Employee Relations Cases
project = PEOPLE AND component = "Employee Relations" AND priority in (High, Highest)

# Onboarding Tasks
project = PEOPLE AND labels = onboarding AND assignee is not EMPTY

# Exit/Offboarding
project = PEOPLE AND labels = offboarding AND status != Done
```

---

## Ticket Templates for People

### Service Request
```yaml
Type: Service Request
Summary: [Request Type] - [Brief Description]
Components: [People Ops | Benefits | ER | L&D]
Priority: [Based on urgency]
Labels: [category, urgency-level]
Description: |
  **Requestor**: [Name]
  **Request**: [Details]
  **Due Date Needed**: [Date]
  **Additional Context**: [Any relevant info]
```

### People Initiative
```yaml
Type: Epic
Summary: [Initiative Name] - [Timeframe]
Components: [Area]
Labels: [Q#-YYYY, initiative]
Description: |
  **Objective**: [What we're trying to achieve]
  **Success Metrics**: [How we'll measure]
  **Timeline**: [Start - End]
  **Stakeholders**: [Key people]
```

### Policy Change
```yaml
Type: Change Request
Summary: Policy Update - [Policy Name]
Components: Policy
Labels: [policy-change, compliance]
Description: |
  **Current State**: [What exists today]
  **Proposed Change**: [What needs to change]
  **Reason**: [Why the change]
  **Effective Date**: [When]
  **Approval Needed**: [Who needs to approve]
```

---

## Integration with Other Skills

### MBR Engine + JIRA

```
1. Query JIRA for People team metrics
2. Track initiative progress for MBR
3. Pull completed work for accomplishments
4. Monitor blockers for risk section
```

### Confluence + JIRA

```
1. Link JIRA tickets to Confluence docs
2. Reference policies in tickets
3. Link meeting notes to decisions
4. Connect processes to work items
```

### MS Graph + JIRA

```
1. Create tickets from email requests
2. Schedule meetings for ticket discussions
3. Send updates when tickets resolve
4. Calendar reminders for due dates
```

---

## Best Practices

### Creating Tickets
- ✅ Use clear, specific summaries
- ✅ Add appropriate components and labels
- ✅ Set realistic due dates
- ✅ Link related tickets
- ✅ Assign to correct person/team

### Managing Work
- ✅ Update status promptly
- ✅ Add comments for context
- ✅ Use @mentions for visibility
- ✅ Close tickets when done

### Reporting
- ✅ Use saved filters for recurring reports
- ✅ Create dashboards for visibility
- ✅ Track trends over time
- ✅ Share metrics with stakeholders

---

## Compliance

### Walmart AI Compliance Status: ✅ Compliant

| Requirement | Status | Notes |
|-------------|--------|-------|
| **Approved AI Services** | ✅ | Uses Wibey (Walmart-approved) |
| **Data Governance** | ✅ | Accesses internal JIRA only |
| **PII Handling** | ✅ | Low PII risk - work items |
| **External Access** | ✅ | Internal Walmart system only |
| **Authentication** | ✅ | Uses Walmart SSO |

### Data Handling

- Input: JQL queries to internal JIRA
- Processing: Wibey agent queries JIRA API
- Output: Ticket data and summaries
- Storage: No persistent storage

### Risk Level: Low

Internal work tracking with:
- Walmart authentication
- Internal JIRA projects only
- No external data access

### Best Practices

- ✅ Query work items and project status
- ✅ Create/update tickets as needed
- ❌ Don't include PII in ticket descriptions
- ❌ Don't query Employee Relations cases without authorization

See [COMPLIANCE.md](../../docs/COMPLIANCE.md) for full framework.

---

## Attribution

- **Original**: Wibey JIRA Agent
- **Documented By**: @jac007x
- **Documentation Date**: 2026-03-18
