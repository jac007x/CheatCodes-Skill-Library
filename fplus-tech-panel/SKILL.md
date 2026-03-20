---
name: fplus-tech-panel
description: Manage F+ Tech Panel review cycles - track panelist assignments via Skyward, update status spreadsheets, generate browser-preview email drafts grouped by category (Thank You, Reminder, New Assignment, PPE Extension, System Access), and deploy emails via Outlook from DAXPromoTeam.
version: 2.0.0
author: jac007x
tags:
  - skyward
  - tech-panel
  - email
  - outlook
  - panelist-tracking
  - walmart
  - qa-kitten
  - browser-automation
  - email-automation
  - dashboard
---

# F+ Tech Panel Management Skill

---

## 🔥 EMAIL AUTOMATION PATTERN (Reusable)

This pattern applies to ANY bulk email workflow — not just F+ Tech Panel.

### Phase 1: Data Collection & Validation
```
1. Pull live data from source of truth (API, database, Skyward, etc.)
2. Cross-reference against tracking spreadsheet
3. Categorize recipients by email type (Thank You, Reminder, Escalation, etc.)
4. Validate:
   - No candidate/subject emails accidentally in recipient list
   - Status matches source of truth (complete vs pending)
   - No duplicates within same category
   - Multi-assigned recipients handled (same person, multiple contexts = separate emails)
5. Flag discrepancies BEFORE proceeding
```

### Phase 2: Browser Preview Dashboard
**Josh loves this — ALWAYS generate before sending**

```html
<!-- Structure -->
<div class="header">Title + timestamp</div>
<div class="stats">Count cards per category</div>
<div class="legend">Status explanations</div>

<!-- Per email category -->
<div class="section">
  <h2><badge color="#category-color">CATEGORY NAME</badge> X emails</h2>
  <details><summary>▶ Show/Hide X email drafts</summary>
    <!-- Email cards -->
    <div class="card">
      <div>TO: recipient@email.com</div>
      <div>Subject: ...</div>
      <div>Body (HTML preview)</div>
    </div>
  </details>
</div>
```

**Key elements:**
- Collapsible sections (`<details><summary>`) — don't overwhelm
- Color-coded badges per category (green=complete, red=urgent, yellow=extended, purple=new)
- Full email preview in cards (TO, Subject, Body)
- Summary table at bottom with counts
- Walmart branding (blue #0053e2 header, proper colors)

### Phase 3: Draft Verification
**Before bulk send, create ONE draft of each email type**

```
1. Create drafts in user's mailbox (not send)
2. User reviews formatting, content, links
3. User approves → proceed with bulk send
4. Delete drafts after sending
```

This catches:
- Template rendering issues
- Broken links
- Typos ("Brad Kieffer F+ Panel Review for Brad Kieffer" → redundancy)
- Wrong deadlines
- Missing support contacts

### Phase 4: Bulk Send Execution
**Be autonomous — don't ask for approval on each batch**

```
1. Send from shared mailbox (SVC-DAXPromoTeam@email.wal-mart.com)
2. Process in batches (30 at a time if large)
3. Track success/failure per email
4. Continue on failures, report at end
5. Clean up drafts after completion
```

### Phase 5: Post-Send Dashboard
**Refresh dashboard with "Emails Sent" indicators**

```html
<div class="alert">
  📧 <b>82 emails sent</b> on March 13, 2026 at 11:10 AM
</div>

<!-- Per recipient row -->
<td><badge>Thank You Sent</badge></td>
<td><badge>Reminder Sent</badge></td>
```

**Also update:**
- Tracking spreadsheet with timestamps (Col E = sent time)
- Share to puppy.walmart.com for stakeholders
- Version the upload (v1 → v2)

### Phase 6: Stakeholder Sharing
**Use share-puppy to publish dashboard**

```
URL: https://puppy.walmart.com/sharing/jac007x/[dashboard-name]
Access: Business (Walmart associates)
Versioned: Auto-increments on re-upload
```

---

## 📧 Email Template Library

### Template 1: Thank You (Completed)
```
Subject: Thank You — F+ Tech Panel Review for [Candidate]
From: DAXPromoTeam

Hi [First],

Thank you for taking the time to complete your F+ Tech Panel review for [Candidate]...
[Support Contacts]
Thank you again for your participation!
```

### Template 2: Reminder (Standard Deadline)
```
Subject: Reminder: Action Required: F+ Tech Panel Assignment - [Candidate]
From: DAXPromoTeam

Hi [First],

This is a friendly reminder that you have been assigned...
If you have already completed — thank you! Disregard below.
[Required Next Steps & Deadlines]
[Support Contacts]
[F+ Tech Panelist Guide link]
```

### Template 3: New Assignment (Conflict Adjustment)
```
Subject: Action Required: F+ Tech Panel Assignment
From: Josh Cramblet (or DAXPromoTeam)

Hi [First],

You are receiving this note because you have been newly assigned...
Candidate: [Candidate]
[Required Next Steps - numbered]
[Extended deadline note]
[Support Contacts]
[Guide link]

Josh Cramblet
Senior Manager, People Analytics
```

### Template 4: System Access Issue
```
Subject: Action Required: F+ Tech Panel Assignment - [Candidate]
From: DAXPromoTeam

Hi [First],

Due to a system issue, you may not have had access... This has been resolved.
[Required Next Steps with extended deadline]
[Support Contacts]
```

### Template 5: PPE Extension
```
(Same as Reminder but with Monday deadline due to PPE error)
```

---

## 🛡️ Bulletproofing Checklist

- [ ] Pull fresh data from source of truth before categorizing
- [ ] Validate all email addresses exist and are formatted correctly
- [ ] Ensure candidate emails are EXCLUDED from recipient list
- [ ] Check for redundant text ("X for X" patterns)
- [ ] Verify deadlines match the category (Fri vs Mon vs Wed)
- [ ] Test one draft of each type before bulk send
- [ ] Track multi-assigned recipients (same email, multiple candidates)
- [ ] Update spreadsheet with sent timestamps
- [ ] Refresh dashboard after sending
- [ ] Share updated dashboard to stakeholders

---

## 🔧 Portability Notes

This pattern works for ANY email automation:
- HR notifications (offer letters, onboarding)
- Project status updates
- Event reminders
- Survey follow-ups
- Approval requests

**To adapt:**
1. Define your email categories (what types of emails?)
2. Define your source of truth (API, spreadsheet, database?)
3. Define your tracking mechanism (spreadsheet columns?)
4. Define your stakeholder dashboard needs
5. Use msgraph agent to send from appropriate mailbox
6. Use share-puppy to publish dashboard

---

## Overview
Manages the F+ Tech Panel review cycle — tracking panelist assignments, completion status, and follow-up communications via Skyward and Outlook.

## Key Workflow

### 1. Data Sources
- **Skyward**: `https://skyward.walmart.com/settings/tech-panel-assignment#` — source of truth for panelist assignments and completion status
- **Tracking Spreadsheet**: Josh maintains an Excel file (e.g., `F+ Tech Panelists_UD_<date>.xlsx`) on OneDrive with columns:
  - **Col A**: Candidate name (the associate being reviewed)
  - **Col B**: Panelist 1 name
  - **Col C**: Panelist 2 name  
  - **Col D**: Thursday reminder sent timestamp
  - **Col E**: Friday reminder sent timestamp
  - **Col F**: Friday morning status (Completed / Pending / Extended / New Assignment)
  - **Col G**: Follow-up notes (reassignment history, special cases)
  - **Cols Q+**: Panelist 1 email
  - **Cols V+**: Panelist 2 email
  - **Col I**: Candidate email

### 2. Status Check Process
1. Use **QA Kitten** to scrape Skyward tech-panel-assignment page
2. For each candidate, click the "# members" link in the Panelist column
3. Check if feedback has been entered (Recommend / Recommend w/ reservations / Do not recommend = **Complete**, Pending = **Pending**)
4. Cross-reference against the spreadsheet
5. Update Col F with status

### 3. Email Groups & Templates
Josh uses these email categories with specific templates:

#### ✅ Thank You (completed panelists)
- **Subject**: `Thank You — F+ Tech Panel Review for [Candidate]`
- **From**: DAXPromoTeam (SVC-DAXPromoTeam@email.wal-mart.com)
- Professional thank you with support contacts

#### 🔴 Reminder (standard deadline)
- **Subject**: `Reminder: Action Required: F+ Tech Panel Assignment - [Candidate]`
- **From**: DAXPromoTeam
- Friendly reminder with Required Next Steps & Deadlines, Support Contacts, link to F+ Tech Panelist Guide
- Acknowledges if they've already completed it

#### 🟣 New Assignment (reassignment/conflict adjustment)
- **Subject**: `Action Required: F+ Tech Panel Assignment`
- **From**: Josh Cramblet directly
- Explains this is a new assignment due to conflict adjustment
- Includes extended deadline note
- Signed by Josh Cramblet, Senior Manager, People Analytics

#### 🔵 System Access Issue
- Same as reminder but explains system access was restored
- Extended deadline

#### 🟡 PPE Extension
- Same as reminder but with Monday extension due to PPE error

### 4. Support Contacts (always included)
- **Process/Policy**: SVC-DAXPromoTeam@email.wal-mart.com
- **Tool Support**: SkywardTechSupport@email.wal-mart.com  
- **Conflicts/Escalations**: Joshua Cramblet (Joshua.Cramblet@walmart.com)

### 5. F+ Tech Panelist Guide
Link: `https://my.wal-mart.com/:b:/g/personal/jac007x_homeoffice_wal-mart_com/IQBNjP99ahbGRpmVdnvtIF99AduniMdbGe_uzpLcL8vz6Pg?e=g2DyNu`

### 6. Reassignment Tracking (Col G format)
```
Reassignment Request {Original Panelist} || Replacement {New Panelist} Reassigned in Skyward + Follow up Email sent with updated Timeline [deadline date]
```

## User Preferences
- **Browser preview of all emails**: Josh LOVES the HTML browser view that groups all emails by category (Thank You, Reminder, New Assignment, etc.) with expandable sections. Always generate this as the review step before sending.
- **Walmart branded**: Use Walmart blue (#0053e2) header, color-coded badges per group
- **Collapsible sections**: Use `<details><summary>` for each email group so Josh can expand/collapse
- **Email cards**: Show TO, Subject, and full HTML body for each email in a card format
- **Summary table**: Include counts at the bottom
- **Cross-validation**: Always do a final Skyward API pull to verify statuses before sending
- **Multi-assigned panelists**: Some panelists review 2 candidates — they get separate emails per candidate
- **Send from**: DAXPromoTeam shared mailbox for reminders/thank yous, Josh's personal for new assignments

## Typical Timeline
- **Monday**: Panels assigned, initial emails sent
- **Thursday**: First reminder wave
- **Friday**: Second reminder wave, status check for follow-up
- **Monday (next week)**: Extended deadline for reassignments
- Reassignments get +2-5 business days depending on timing

## Anti-Patterns to Avoid
- Never email candidates — only email panelists
- Never mark a panelist as "complete" unless Skyward shows Recommend/Do not recommend
- Don't send duplicate emails to multi-assigned panelists for the same candidate
- Don't mix up candidate names and panelist names in emails
