---
name: calendar-email-workflow
description: "Universal calendar and email workflow skill. Schedule meetings, check availability, draft and send emails, manage follow-ups, and automate recurring communication patterns. Works with any Microsoft 365 or Google Workspace account via the platform's native agent."
version: 1.0.0
author: jac007x
tags:
  - calendar
  - email
  - scheduling
  - microsoft-365
  - automation
  - productivity
  - cross-platform
---

# 📅 Calendar & Email Workflow

A universal skill for scheduling, communication, and follow-up automation.
Covers the full loop: check availability → schedule → draft → send → follow up.
Works with Microsoft 365 (via msgraph agent) or Google Workspace.

---

## 🧠 Core Philosophy

- **Availability before scheduling** — always check conflicts before proposing times
- **Draft before sending** — always show the draft; never auto-send without confirmation
- **Context carries** — meeting prep, agenda, and attendee context travel together
- **Follow-up is part of the workflow** — scheduling without follow-up tracking is half the job
- **Batch where possible** — 10 invites sent one-by-one is 10x the friction of a batch

---

## 🚀 Intake

### Scheduling
| Variable | Description | Required |
|----------|-------------|----------|
| `{{ATTENDEES}}` | Email addresses of attendees | ✅ |
| `{{MEETING_TYPE}}` | `1:1`, `group`, `skip-level`, `office-hours`, `recurring` | ✅ |
| `{{DURATION_MINUTES}}` | Length of meeting in minutes | ✅ |
| `{{PREFERRED_WINDOW}}` | Date range or week to schedule within | ✅ |
| `{{RECURRENCE}}` | Recurrence pattern if recurring: `weekly`, `biweekly`, `monthly` | ❌ |
| `{{AGENDA}}` | Meeting agenda or purpose | ❌ |
| `{{LOCATION}}` | Room, Teams link, or location | ❌ |

### Email
| Variable | Description | Required |
|----------|-------------|----------|
| `{{RECIPIENTS}}` | To, CC, BCC list | ✅ |
| `{{EMAIL_TYPE}}` | `announcement`, `follow-up`, `reminder`, `thank-you`, `template` | ✅ |
| `{{TONE}}` | `formal`, `warm`, `direct` | ❌ | 
| `{{CONTEXT}}` | What this email is about | ✅ |
| `{{SENDER_NAME}}` | Name to sign from | ❌ |
| `{{SEND_FROM}}` | Sending account or shared mailbox | ❌ |

---

## 🔄 Workflow Patterns

### Pattern 1: Schedule a Meeting
```
1. Collect {{ATTENDEES}}, {{DURATION_MINUTES}}, {{PREFERRED_WINDOW}}
2. Check availability for all attendees in the window
3. Identify top 3 open slots (avoid Mondays before 10am, Fridays after 3pm by default)
4. Present options to user — confirm slot
5. Create calendar event with agenda in body
6. Send invites
7. Log to tracking if {{TRACKING_SHEET}} provided
```

### Pattern 2: Batch Scheduling
```
1. Load attendee list from {{ROSTER_FILE}} (CSV or Excel)
2. For each attendee: check availability in {{PREFERRED_WINDOW}}
3. Generate schedule: earliest available slot per person
4. Present full schedule for review before sending
5. Confirm — then send all invites in batch
6. Output: schedule_log.csv with confirmed times
```

### Pattern 3: Draft & Send Email
```
1. Collect {{EMAIL_TYPE}}, {{RECIPIENTS}}, {{CONTEXT}}
2. Draft email using tone and context
3. Present draft — user reviews and edits
4. Confirm send — never auto-send
5. Log sent email to {{OUTPUT_DIR}} if specified
```

### Pattern 4: Follow-Up Workflow
```
1. Load previous meeting or email context
2. Identify action items, decisions, or open threads
3. Draft follow-up email with action item summary
4. Schedule follow-up meeting if needed
5. Set reminder at {{FOLLOWUP_DAYS}} days if no response
```

---

## 🌐 Platform Routing

| Platform | Calendar | Email | Agent |
|----------|----------|-------|-------|
| Microsoft 365 | Exchange/Outlook | Outlook | `msgraph` sub-agent |
| Google Workspace | Google Calendar | Gmail | Google Workspace agent |
| Generic (any) | Manual output | Draft only | No agent required |

**For Microsoft 365:** Invoke the `msgraph` sub-agent for all calendar and email actions.
```
Activate: "Use calendar-email-workflow"
Platform: Microsoft 365
Agent: msgraph
```

---

## 📊 Use Cases

| Use Case | Meeting Type | Email Type |
|----------|-------------|------------|
| Schedule 1:1s with direct reports | `1:1` recurring | `follow-up` after each |
| Skip-level listening sessions | `skip-levp | `announcement` before, `thank-you` after |
| Town hall prep | `group` | `announcement` |
| New hire onboarding meetings | `1:1` batch | `template` welcome |
| Project kickoff | `group` | `announcement` + `follow-up` |
| Office hours | `office-hours` recurring | `reminder` 24h before |

---

## ⚠️ Anti-Patterns

```
❌ Auto-sending emails without showing the draft first
❌ Scheduling without checking availability (causes double-booking)
❌ Hardcoding sender email or shared mailbox (always use {{SEND_FROM}})
❌ Sending batch invites one at a time (batch them)
❌ Forgetting to handle timezone differences for distributed teams
❌ Using the same email template for every type (tone matters)
```

---

## 🔁 Deployment Ladder

| Stage | Who | What to validate |
|-------|-----|------------------|
| **Refine** | Skill Owner | Availability check accuracy, draft quality, batch scheduling |
| **Prove** | Peer Teams | Works across different M365 tenants and team structures |
| **Scale** | Enterprise | Shared mailbox support, delegation, large attendee lists |
