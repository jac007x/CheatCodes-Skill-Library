# MS Graph for People Function

📚 **Source**: Curated from Wibey `msgraph` skill
**Category**: Productivity, Calendar, Email, People Workflows

A wrapper around the Wibey MS Graph skill, tailored for People function workflows.

---

## Overview

This skill leverages Microsoft Graph API to automate common People function tasks:
- Calendar management for meetings, 1:1s, skip-levels
- Email automation for communications, follow-ups
- Meeting analytics for time insights

## Prerequisites

- Wibey CLI with `msgraph` skill installed
- Microsoft 365 account with appropriate permissions

## Quick Start

```bash
# Invoke the skill
/msgraph

# Check authentication
NODE_PATH="$HOME/.local/lib/node_modules" bun ~/.wibey/skills/msgraph/scripts/auth.ts status

# Login if needed
NODE_PATH="$HOME/.local/lib/node_modules" bun ~/.wibey/skills/msgraph/scripts/auth.ts login
```

---

## People Function Workflows

### 1. Schedule 1:1 Meetings

**Use Case**: Schedule recurring 1:1s with direct reports or stakeholders

```bash
# Check availability first
bun ~/.wibey/skills/msgraph/scripts/calendar.ts availability \
  --emails "manager@example.com,report@example.com" \
  --start "2026-03-20T09:00:00" \
  --end "2026-03-20T17:00:00"

# Create recurring 1:1
bun ~/.wibey/skills/msgraph/scripts/calendar.ts create \
  --subject "Weekly 1:1: [Manager] & [Report]" \
  --start "2026-03-20T14:00:00" \
  --end "2026-03-20T14:30:00" \
  --attendees "report@example.com" \
  --teams \
  --timezone "America/Chicago"
```

### 2. Skip-Level Meeting Scheduler

**Use Case**: Schedule skip-level meetings across your org

```bash
# Find person's email from name
bun ~/.wibey/skills/msgraph/scripts/users.ts get-email --display-name "John Smith"

# Check mutual availability
bun ~/.wibey/skills/msgraph/scripts/calendar.ts availability \
  --emails "john.smith@example.com" \
  --start "2026-03-20T08:00:00" \
  --end "2026-03-20T18:00:00"

# Schedule with Teams link
bun ~/.wibey/skills/msgraph/scripts/calendar.ts create \
  --subject "Skip-Level: [Your Name] & John Smith" \
  --start "2026-03-20T10:00:00" \
  --end "2026-03-20T10:30:00" \
  --attendees "john.smith@example.com" \
  --body "Informal check-in. What's on your mind?" \
  --teams \
  --timezone "America/Chicago"
```

### 3. Team Communication Templates

**Use Case**: Send templated emails to team

```bash
# Send welcome email to new hire
bun ~/.wibey/skills/msgraph/scripts/mail.ts send \
  --to "newhire@example.com" \
  --subject "Welcome to the Team!" \
  --body "Hi [Name],

Welcome to [Team]! Here's what to expect in your first week:

1. Day 1: Orientation and laptop setup
2. Day 2-3: Meet the team (1:1s scheduled)
3. Day 4-5: Shadow sessions

Your buddy: [Buddy Name] ([buddy@example.com])

Looking forward to working with you!

Best,
[Your Name]" \
  --confirm
```

### 4. Meeting Prep - Today's Agenda

**Use Case**: Get today's meetings with details

```bash
# List today's meetings
bun ~/.wibey/skills/msgraph/scripts/calendar.ts today

# Get details for specific meeting
bun ~/.wibey/skills/msgraph/scripts/calendar.ts get EVENT_ID
```

### 5. Email Triage for People Inbox

**Use Case**: Review and process unread emails

```bash
# Get unread emails
bun ~/.wibey/skills/msgraph/scripts/mail.ts list --unread --limit 20

# Search for specific topics
bun ~/.wibey/skills/msgraph/scripts/mail.ts search --query "performance review" --limit 10

# Mark as read after review
bun ~/.wibey/skills/msgraph/scripts/mail.ts mark-read MESSAGE_ID

# Flag for follow-up
bun ~/.wibey/skills/msgraph/scripts/mail.ts flag MESSAGE_ID --status flagged
```

### 6. Bulk Meeting Scheduling

**Use Case**: Schedule same meeting with multiple people (town halls, all-hands prep)

```bash
# Check availability for multiple attendees
bun ~/.wibey/skills/msgraph/scripts/calendar.ts availability \
  --emails "person1@example.com,person2@example.com,person3@example.com" \
  --start "2026-03-25T08:00:00" \
  --end "2026-03-25T18:00:00"

# Create meeting with all attendees
bun ~/.wibey/skills/msgraph/scripts/calendar.ts create \
  --subject "Q1 People Review Prep" \
  --start "2026-03-25T14:00:00" \
  --end "2026-03-25T15:00:00" \
  --attendees "person1@example.com,person2@example.com,person3@example.com" \
  --location "Conference Room A / Teams" \
  --teams \
  --timezone "America/Chicago"
```

### 7. Follow-up Email Workflow

**Use Case**: Send follow-up after meetings

```bash
# Reply to existing thread
bun ~/.wibey/skills/msgraph/scripts/mail.ts reply MESSAGE_ID \
  --body "Thanks for the discussion today!

Action items:
1. [Action 1] - Owner: [Name] - Due: [Date]
2. [Action 2] - Owner: [Name] - Due: [Date]

Let me know if I missed anything.

Best,
[Your Name]" \
  --confirm
```

---

## Email Templates for People Function

### New Hire Welcome
```
Subject: Welcome to [Team]!
Body: Structured onboarding info with buddy assignment
```

### Performance Review Reminder
```
Subject: Reminder: Performance Review Due [Date]
Body: Instructions, links to forms, deadline
```

### Team Update / Newsletter
```
Subject: [Team] Weekly Update - [Date]
Body: Wins, focus areas, announcements, kudos
```

### Meeting Request
```
Subject: [Topic] Discussion - [Requester] & [Attendee]
Body: Purpose, agenda, prep items
```

### Exit Interview Scheduling
```
Subject: Exit Interview - [Employee Name]
Body: Scheduling request with People partner
```

---

## Calendar Analytics Patterns

### Time in Meetings Analysis

```bash
# Get all meetings for a week
bun ~/.wibey/skills/msgraph/scripts/calendar.ts list \
  --start "2026-03-17T00:00:00" \
  --end "2026-03-21T23:59:59" \
  --limit 100
```

**Analyze output for**:
- Total meeting hours
- Meeting-free blocks
- Back-to-back meetings
- Early morning / late evening meetings

### Availability Legend
- 🟢 Free
- 🟡 Tentative
- 🔴 Busy
- 🟣 Out of Office
- ⚪ Working Elsewhere

---

## Best Practices

### Calendar
1. **Always check availability** before scheduling
2. **Include Teams link** for remote/hybrid meetings (`--teams`)
3. **Set timezone explicitly** to avoid UTC confusion
4. **Add agenda in body** for productive meetings

### Email
1. **Preview before sending** - show draft, confirm with user
2. **Use search** to find related threads before composing
3. **Flag for follow-up** when action needed
4. **Batch operations** when processing multiple emails

### General
1. **Verify auth** before any operation
2. **Handle errors gracefully** - re-auth if 401
3. **Convert UTC to local time** for display

---

## Integration with MBR Engine

This skill can complement the MBR Engine:

| MBR Phase | MS Graph Integration |
|-----------|---------------------|
| Data Collection | Email search for context |
| Review Scheduling | Calendar availability + create |
| Distribution | Email send for MBR delivery |
| Follow-up | Reply tracking, action items |

---

## Compliance

### Walmart AI Compliance Status: ✅ Compliant

| Requirement | Status | Notes |
|-------------|--------|-------|
| **Approved AI Services** | ✅ | Uses Wibey (Walmart-approved) |
| **Data Governance** | ✅ | Accesses M365 via approved MS Graph API |
| **PII Handling** | ⚠️ | Email/calendar may contain PII - see controls |
| **External Access** | ✅ | M365 is Walmart-approved external service |
| **Authentication** | ✅ | Uses AAD OAuth (Walmart identity) |

### PII Controls

This skill accesses email and calendar which may contain PII.

**Controls:**
- ✅ Uses Walmart AAD authentication
- ✅ Accesses only user's own M365 data
- ✅ No data sent to external AI services
- ✅ Email content processed locally via Wibey

**Data Handling:**
- Input: M365 calendar/email via MS Graph API
- Processing: Local via Wibey CLI
- Output: Displayed locally or sent via M365
- Storage: No persistent storage of email content

### Risk Level: Low

M365 integration uses:
- Walmart-approved authentication
- User's own data scope
- No external AI processing

See [COMPLIANCE.md](../../docs/COMPLIANCE.md) for full framework.

---

## Attribution

- **Original Skill**: Wibey `msgraph` skill
- **Curated By**: @jac007x
- **Curation Date**: 2026-03-18
- **Modifications**: People function workflows, templates, patterns
