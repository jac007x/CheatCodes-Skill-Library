# Skyward Tech Panel Status Checker

## Description
Automated workflow to check F+ Tech Panel feedback status from Skyward and update tracking spreadsheets.

## Version
1.0.0

## Author
jac007x

## Tags
skyward, tech-panel, f-plus, promotion, panelist, feedback, qa-kitten, browser-automation, excel

## Prerequisites
- User must be logged into Skyward (PingFed SSO) — QA Kitten cannot authenticate
- openpyxl Python package for Excel manipulation
- QA Kitten sub-agent for browser automation

## Workflow

### Step 1: Read the Tracking Spreadsheet
- Open the Excel file (typically on OneDrive)
- Identify Column A (Candidate Names), Columns P-Y (Assigned Panelist Names & Emails)
- Identify Column F (Friday Morning Status) — target column for updates
- Count total candidates vs. ones already having status

### Step 2: Authenticate to Skyward
- Use QA Kitten to open https://skyward.walmart.com/settings/tech-panel-assignment#
- User must manually log in via PingFed SSO
- Wait for user confirmation before proceeding

### Step 3: Fetch Panel Status (API Method — Preferred)
QA Kitten discovered that Skyward exposes an API at:
```
/api/settings/tech-panel-assignment
```
This API returns ALL assigned nominations with panelist data in a single call, including:
- `isCompleted: true/false` — whether the panelist submitted feedback
- `recommendation: "recommend" | "recommend_with_reservations" | "do_not_recommend" | null`
- Panelist name, title, assigned date
- Full feedback text (when completed)

**This is dramatically faster than clicking through the UI one candidate at a time.**

### Step 3 (Alternative): UI Click-Through Method
If the API doesn't work:
1. Click the **"Assigned"** tab (shows count of assigned candidates)
2. For each candidate:
   a. Type candidate name in **"Search associates"** box (top-right)
   b. Click the **"2 members"** link in the **Panelists** column
   c. Read status from the modal:
      - 🟠 **Pending**: Orange text "Panelist yet to provide their review feedbacks."
      - 🟢 **Complete (Recommend)**: Green "Recommend" badge + full written feedback
      - 🟡 **Complete w/ reservations**: Yellow badge
      - 🔴 **Do not recommend**: Red badge
   d. Click **"Okay"** to close modal
   e. Clear search, repeat for next candidate

### Step 4: Update the Spreadsheet
Format for Column F follows this pattern:
```
{Panelist1 Name} - {Status} - {Panelist2 Name} - {Status}
```

Status values:
- `Complete [send thank you]` — Panelist submitted a "Recommend" review
- `Complete w/ reservations` — Panelist submitted with reservations
- `Complete [DO NOT RECOMMEND]` — Panelist gave negative recommendation
- `Pending` — Panelist has not yet submitted feedback

### Step 5: Backup & Save
- Always create a backup copy before modifying (append `_BACKUP` to filename)
- Only update rows where Column F is empty/None
- Preserve existing manually-entered statuses

## Page Layout Reference (Skyward Tech Panel Assignment)

### Navigation
- Left sidebar: Settings > Tech panel assignment
- Also available: "Tech panel members" page (different view)

### Tabs
- **Unassigned** — Candidates awaiting panelist assignment
- **Assigned** — Candidates with panelists assigned (main working tab)
- **Reviewed** — Completed reviews

### Table Columns
| Column | Description |
|--------|-------------|
| Associate | Avatar + Name + userId |
| Nominated for | Current → Target role |
| Nominated by | Manager/nominator name |
| Panelists | "N members" link (clickable) |
| Actions | Assign/Re-assign button |

### Panel Review Modal (clicking "N members")
Shows card for each panelist with:
- Name, title, avatar
- Assignment date
- Status indicator (pending/recommend/reservations/do-not-recommend)
- Full feedback text (when completed)
- "Okay" button to close

## Special Cases to Watch For
- **Duplicate panelist assignments** (e.g., same person listed twice)
- **3+ panelists** instead of the usual 2
- **"Do not recommend"** flags requiring immediate escalation
- **Reassignment notes** in Column G (Follow up Notes)
- **XLOOKUP formulas** in name columns (P, U) that reference external sheets

## Primitives Used
- `qa-kitten` — Browser automation and Skyward API access
- `openpyxl` — Excel file read/write
- `shutil` — File backup
- Python scripting for data transformation

## Efficiency Tips
- Use the API endpoint instead of UI clicks (1 call vs 41+ clicks)
- Search by panelist email for accuracy (emails are unique, names can be ambiguous)
- Batch all updates into a single Excel write operation
- Always backup before modifying
