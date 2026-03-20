---
name: email-automation-pattern
description: Bulletproof bulk email automation with browser preview dashboards, draft verification, batch sending, and stakeholder sharing. Reusable pattern for any email workflow.
version: 1.0.0
author: jac007x
tags:
  - email
  - automation
  - outlook
  - msgraph
  - dashboard
  - bulk-send
  - share-puppy
  - workflow
---

# 📧 Email Automation Pattern

A bulletproof, portable workflow for bulk email automation with tracking dashboards.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     EMAIL AUTOMATION FLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  SOURCE  │───▶│ VALIDATE │───▶│ PREVIEW  │───▶│  DRAFT   │  │
│  │  OF TRUTH│    │ & GROUP  │    │ DASHBOARD│    │  VERIFY  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │                                               │         │
│       │         ┌──────────┐    ┌──────────┐         │         │
│       │         │  SHARE   │◀───│  UPDATE  │◀────────┘         │
│       │         │ DASHBOARD│    │ & SEND   │                   │
│       │         └──────────┘    └──────────┘                   │
│       │              │                                          │
│       ▼              ▼                                          │
│  ┌──────────┐   ┌──────────┐                                   │
│  │ TRACKING │   │ PUPPY    │                                   │
│  │SPREADSHEET│  │ SHARING  │                                   │
│  └──────────┘   └──────────┘                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Phase 1: Data Collection

### Inputs Required
| Input | Source | Example |
|-------|--------|--------|
| Recipients | API/Database/Spreadsheet | Skyward, BQ, Excel |
| Status | Source of truth | Complete/Pending |
| Categories | Business logic | Thank You, Reminder, Escalation |
| Templates | User-provided .eml or spec | HTML email bodies |

### Validation Rules
```python
# ALWAYS validate before categorizing
validation_checks = [
    "recipient_emails_are_valid",           # No malformed emails
    "no_subject_emails_in_recipients",      # Don't email the person being discussed
    "status_matches_source_of_truth",       # Fresh API pull, not stale data
    "no_duplicates_within_category",        # Same email, same context = 1 email
    "multi_context_handled_separately",     # Same email, diff context = N emails
    "deadlines_match_category",             # Fri vs Mon vs extended
    "template_variables_resolved",          # No [FIRST] or [CANDIDATE] left
]
```

---

## 📊 Phase 2: Browser Preview Dashboard

**ALWAYS generate this before sending. User reviews in browser.**

### HTML Structure
```html
<!DOCTYPE html>
<html>
<head>
  <title>[Workflow] — Email Preview</title>
  <style>
    /* Walmart colors */
    :root {
      --wm-blue: #0053e2;
      --wm-green: #2a8703;
      --wm-red: #ea1100;
      --wm-yellow: #995213;
      --wm-purple: #7b2d8e;
      --wm-spark: #ffc220;
    }
    
    .header { background: linear-gradient(135deg, var(--wm-blue), #041f41); }
    .badge { padding: 2px 8px; border-radius: 10px; font-size: 11px; }
    .card { border-left: 4px solid var(--category-color); }
    details summary { cursor: pointer; } /* Collapsible */
  </style>
</head>
<body>
  <!-- Header with title + timestamp -->
  <div class="header">...</div>
  
  <!-- Stats cards -->
  <div class="stats">
    <div class="stat green">13 Complete</div>
    <div class="stat red">60 Pending</div>
  </div>
  
  <!-- Per category: collapsible section -->
  <div class="section">
    <h2><badge>CATEGORY</badge> X emails</h2>
    <details>
      <summary>▶ Show/Hide X emails</summary>
      <!-- Email cards -->
      <div class="card">
        <div>TO: email@domain.com</div>
        <div>Subject: ...</div>
        <div class="body">HTML preview</div>
      </div>
    </details>
  </div>
  
  <!-- Summary table -->
  <table>...</table>
</body>
</html>
```

### Category Color Coding
| Category | Color | Badge |
|----------|-------|-------|
| Complete/Thank You | Green #2a8703 | ✅ |
| Urgent/Due Today | Red #ea1100 | 🔴 |
| Extended/Warning | Yellow #995213 | 🟡 |
| New Assignment | Purple #7b2d8e | 🟣 |
| System/Info | Blue #0053e2 | 🔵 |

---

## ✏️ Phase 3: Draft Verification

**Create ONE draft of each email type for user review**

```python
# Using msgraph agent
for category in email_categories:
    sample = category.emails[0]
    create_draft(
        to=sample.recipient,
        subject=sample.subject,
        body=sample.html_body,
        # DO NOT SEND - draft only
    )
```

### What Drafts Catch
- ❌ Template rendering bugs
- ❌ Broken links
- ❌ Typos ("X for X" redundancy)
- ❌ Wrong deadlines for category
- ❌ Missing support contacts
- ❌ HTML formatting issues

**User approves drafts → proceed to send**

---

## 🚀 Phase 4: Bulk Send

**Be autonomous — don't ask for approval on each batch**

```python
# Using msgraph agent
BATCH_SIZE = 30  # Send in batches

for batch in chunks(all_emails, BATCH_SIZE):
    for email in batch:
        send_mail(
            from_mailbox="SVC-SharedMailbox@email.wal-mart.com",
            to=email.recipient,
            subject=email.subject,
            body=email.html_body,
            content_type="HTML"
        )
    # Brief pause between batches if needed
```

### Shared Mailbox Sending
- Use `msgraph_send_mail` with shared mailbox
- Requires Send As or Send on Behalf permissions
- Falls back to user mailbox if needed

---

## 📈 Phase 5: Post-Send Dashboard

**Regenerate dashboard with sent indicators**

### Updates
1. Add "📧 X emails sent on [timestamp]" banner
2. Add "Sent" badges per recipient row
3. Update tracking spreadsheet with timestamps
4. Re-upload to share-puppy (auto-versions)

```html
<div class="alert">
  📧 <b>82 emails sent</b> on March 13, 2026 at 11:10 AM
</div>

<td><span class="badge sent">Reminder Sent</span></td>
```

---

## 🌐 Phase 6: Stakeholder Sharing

**Publish to puppy.walmart.com**

```
Agent: share-puppy
File: /path/to/dashboard.html
URL: https://puppy.walmart.com/sharing/[userid]/[dashboard-name]
Access: business (Walmart associates)
Versioning: Auto-increments on re-upload
```

Stakeholders get a live link to view status without needing file access.

---

## 🛡️ Bulletproofing Checklist

```markdown
## Pre-Send
- [ ] Fresh data pull from source of truth
- [ ] All emails validated (format, exists)
- [ ] Subject/candidate emails EXCLUDED
- [ ] No redundant text patterns
- [ ] Deadlines match categories
- [ ] One draft per type created and reviewed
- [ ] Multi-context recipients handled

## Send
- [ ] Batch processing (30 at a time)
- [ ] Sent from correct mailbox
- [ ] Success/failure tracked
- [ ] Drafts cleaned up

## Post-Send
- [ ] Spreadsheet updated with timestamps
- [ ] Dashboard refreshed with "Sent" indicators
- [ ] Dashboard re-uploaded to share-puppy
- [ ] Stakeholders notified of dashboard link
```

---

## 🔧 Adapting to New Workflows

### Step 1: Define Categories
```python
categories = [
    {"name": "Thank You", "color": "green", "template": "thank_you.html"},
    {"name": "Reminder", "color": "red", "template": "reminder.html"},
    {"name": "Escalation", "color": "purple", "template": "escalation.html"},
]
```

### Step 2: Define Source of Truth
```python
source = {
    "type": "api",  # or "spreadsheet", "bigquery", "skyward"
    "endpoint": "https://api.example.com/status",
    "status_field": "completion_status",
    "complete_values": ["done", "submitted"],
}
```

### Step 3: Define Tracking
```python
tracking = {
    "file": "tracking.xlsx",
    "sent_column": "E",
    "status_column": "F",
    "notes_column": "G",
}
```

### Step 4: Execute Pattern
```
1. Pull data → Validate → Categorize
2. Generate browser preview → User reviews
3. Create drafts → User approves
4. Bulk send → Track results
5. Update dashboard → Share to stakeholders
```

---

## 📚 Example Workflows

| Workflow | Categories | Source | Mailbox |
|----------|------------|--------|--------|
| F+ Tech Panel | Thank You, Reminder, New Assign | Skyward API | DAXPromoTeam |
| Onboarding | Welcome, Day 1, Week 1 | Workday API | HR Shared |
| Survey Follow-up | Thank You, Reminder, Final | Qualtrics | Research Team |
| Event RSVP | Confirmed, Pending, Waitlist | Eventbrite | Events Team |
| Approval Requests | Pending, Approved, Rejected | ServiceNow | Approvals |

---

## 🐶 Agent Dependencies

| Agent | Purpose |
|-------|--------|
| `msgraph` | Send emails, create drafts, access shared mailboxes |
| `qa-kitten` | Scrape web sources (Skyward, etc.) |
| `share-puppy` | Publish dashboards to puppy.walmart.com |
| `bigquery-explorer` | Pull data from BQ if needed |

---

## ⚠️ Anti-Patterns

- ❌ Sending without browser preview first
- ❌ Asking for approval on every single email
- ❌ Using stale data (always fresh pull)
- ❌ Emailing subjects/candidates instead of recipients
- ❌ Ignoring multi-context recipients
- ❌ Not updating dashboard after sending
- ❌ Not sharing dashboard with stakeholders
