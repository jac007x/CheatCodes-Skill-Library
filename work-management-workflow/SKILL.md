---
name: work-management-workflow
description: "Universal work management skill. Create, track, update, and report on tasks, tickets, and projects across any work management platform — JIRA, Planner, Asana, ServiceNow, or any task system. Covers request intake, status tracking, workload reporting, and escalation."
version: 1.0.0
author: jac007x
tags:
  - work-management
  - task-tracking
  - jira
  - planner
  - project-management
  - cross-platform
---

# ✅ Work Management Workflow

Create → track → update → report. A universal pattern for managing work items
across any platform. Whether it’s a JIRA ticket, a Planner task, or a ServiceNow
request — the workflow is the same.

---

## 🧠 Core Philosophy

- **One source of truth** — work lives in the system, not in someone’s head or inbox
- **Status is always current** — if it’s not updated, it doesn’t exist
- **Escalation is built in** — blocked items surface automatically, not when someone notices
- **Reports tell a story** — raw ticket counts are useless; velocity, blockers, and health matter
- **Intake captures everything upfront** — a good ticket description saves 3 clarifying conversations

---

## 🚀 Intake

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{PLATFORM}}` | Work system: `jira`, `planner`, `asana`, `servicenow`, `other` | ✅ | — |
| `{{ACTION}}` | `create`, `update`, `query`, `report`, `escalate` | ✅ | — |
| `{{PROJECT_KEY}}` | Project or board identifier | ❌ | all |
| `{{ASSIGNEE}}` | Person or team to assign to | ❌ | unassigned |
| `{{PRIORITY}}` | `low`, `medium`, `high`, `critical` | ❌ | `medium` |
| `{{LABELS}}` | Tags or labels for categorization | ❌ | — |
| `{{REPORT_PERIOD}}` | For reports: `this-week`, `this-month`, `this-quarter` | ❌ | `this-week` |
| `{{FILTER}}` | Status, assignee, or label filter for queries | ❌ | open items |

---

## 🔄 Workflow Patterns

### Pattern 1: Create a Work Item
```
1. Collect: title, description, assignee, priority, labels
2. Check for duplicates before creating
3. Draft item — show to user for review
4. Create in {{PLATFORM}}
5. Return item ID and URL
6. Set reminder for follow-up at {{FOLLOWUP_DAYS}} if provided
```

### Pattern 2: Query Work Items
```python
def build_query(platform: str, filters: dict) -> str:
    """Build a platform-appropriate query from filter dict."""
    if platform == "jira":
        parts = []
        if filters.get("project"):
            parts.append(f'project = "{filters["project"]}"')
        if filters.get("status"):
            parts.append(f'status = "{filters["status"]}"')
        if filters.get("assignee"):
            parts.append(f'assignee = "{filters["assignee"]}"')
        return " AND ".join(parts) if parts else "project is not EMPTY"
    # Add other platform query builders here
    return str(filters)
```

### Pattern 3: Status Report
```
1. Query all open items in {{PROJECT_KEY}} for {{REPORT_PERIOD}}
2. Group by: status, assignee, priority
3. Identify:
   - Blocked items (status = blocked or no update in >5 days)
   - At-risk items (due date within 3 days, not complete)
   - Completed this period
4. Build report:
   - Summary: X open, Y completed, Z blocked
   - Blocked items with owner and blocker description
   - Velocity: items closed vs. items opened this period
5. Output as markdown table or HTML if {{OUTPUT_FORMAT}} = html
```

### Pattern 4: Escalation
```
Trigger when:
  - Item is blocked for > {{ESCALATION_DAYS}} days (default: 5)
  - High/critical priority item has no update in > 2 days
  - Due date passed with status still open

Action:
  1. Identify blocked item and current owner
  2. Draft escalation message to {{ESCALATION_CONTACT}}
  3. Show draft — confirm before sending
  4. Add escalation note to the work item
  5. Log escalation to {{OUTPUT_DIR}}/escalation_log.csv
```

---

## 🌐 Platform Routing

| Platform | Agent / Tool | Notes |
|----------|-------------|-------|
| JIRA | `jira` sub-agent | JQL query support |
| Microsoft Planner | `msgraph` sub-agent | Part of M365 |
| ServiceNow | ServiceNow API | Requires instance URL |
| Asana | Asana API | Requires API key |
| Other | Generic REST | Use `{{API_BASE_URL}}` intake variable |

---

## 📊 Report Output Example

```
## Work Status Report — Week of Mar 23, 2026

**Summary:** 12 open │ 4 completed │ 2 blocked │ 1 at-risk

### 🔴 Blocked (action required)
| Item | Owner | Blocked Since | Blocker |
|------|-------|---------------|---------|
| PRJ-42 | Alex | Mar 18 | Waiting on legal review |
| PRJ-51 | Sam | Mar 20 | Dependency on PRJ-39 |

### ⚠️ At-Risk (due soon)
| Item | Owner | Due Date | Status |
|------|-------|----------|--------|
| PRJ-55 | Jordan | Mar 25 | In Progress |

### ✅ Completed This Week
PRJ-38, PRJ-44, PRJ-47, PRJ-50

**Velocity:** 4 closed / 3 opened = +1 net progress
```

---

## ⚠️ Anti-Patterns

```
❌ Creating tickets without checking for duplicates first
❌ Reporting raw counts without velocity or trend context
❌ Leaving blocked items unescalated (they don't resolve themselves)
❌ Assigning to a team instead of a person (no individual accountability)
❌ Using the same priority for everything (priority inflation kills triage)
❌ Building reports in a spreadsheet when the system already has the data
```

---

## 🔁 Deployment Ladder

| Stage | Who | What to validate |
|-------|-----|------------------|
| **Refine** | Skill Owner | Query accuracy, report format, escalation logic |
| **Prove** | Peer Teams | Works across different projects and assignee structures |
| **Scale** | Enterprise | Multi-project roll-ups, cross-platform aggregation |
