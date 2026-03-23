---
name: review-cycle-manager
description: "Universal review cycle management skill. Handles any structured nomination, assignment, status-tracking, and communication workflow — tech panels, performance calibrations, promotion cycles, award nominations, and more. Intake variables adapt it to any program."
version: 1.0.0
author: jac007x
tags:
  - review-cycle
  - nominations
  - calibration
  - status-tracking
  - email-automation
  - hr-workflow
  - cross-platform
---

# 🔄 Review Cycle Manager

A universal skill for managing any structured cycle of nominations, assignments,
reviews, and communications. The pattern is the same whether you’re running a
tech panel, a promotion calibration, an award nomination, or a performance review
cycle — only the names change.

```
Load roster → Poll statuses → Categorize → Draft communications
  → Review & send → Update tracking → Report
```

---

## 🧠 Core Philosophy

- **The roster is the source of truth** — everything starts from a list of people and assignments
- **Status polling is mechanical** — the skill checks the system; the human decides what to do
- **Communication categories drive action** — group people by their status, then communicate per group
- **Nothing sends without human review** — always show drafts; never auto-send
- **The tracking sheet is always current** — update it after every action, not at the end
- **Reporting closes the loop** — a cycle without a summary report didn’t happen

---

## 🚀 Intake

### Program Context
| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `{{PROGRAM_NAME}}` | Name of the review program | ✅ | `Tech Panel`, `Q2 Calibration` |
| `{{CYCLE_PERIOD}}` | Time period this cycle covers | ✅ | `Q1 2026`, `March 2026` |
| `{{REVIEW_TYPE}}` | Type: `panel`, `calibration`, `nomination`, `award`, `performance` | ✅ | |

### Roster & Tracking
| Variable | Description | Required |
|----------|-------------|----------|
| `{{ROSTER_FILE}}` | Path to CSV/Excel with nominees or participants | ✅ |
| `{{NAME_COLUMN}}` | Column containing participant name | ✅ |
| `{{EMAIL_COLUMN}}` | Column containing participant email | ✅ |
| `{{ASSIGNMENT_COLUMN}}` | Column for reviewer/panelist assignment | ❌ |
| `{{STATUS_COLUMN}}` | Column tracking current status | ✅ |
| `{{TRACKING_FILE}}` | Path to tracking spreadsheet to update | ❌ |

### Status System
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{STATUS_SOURCE}}` | Where to pull statuses: `file`, `api`, `manual` | ✅ | `file` |
| `{{API_ENDPOINT}}` | API URL if `{{STATUS_SOURCE}}` is `api` | ❌ | — |
| `{{API_AUTH_NOTE}}` | Auth instructions for API (no credentials stored here) | ❌ | — |
| `{{COMPLETE_STATUSES}}` | Status values that mean “done” | ✅ | `["Complete", "Submitted"]` |
| `{{PENDING_STATUSES}}` | Status values that mean “not yet” | ✅ | `["Pending", "Not Started"]` |
| `{{EXCEPTION_STATUSES}}` | Status values needing special handling | ❌ | `["N/A", "Withdrawn"]` |

### Communications
| Variable | Description | Required |
|----------|-------------|----------|
| `{{SENDER_NAME}}` | Name to send from | ✅ |
| `{{SENDER_EMAIL}}` | Email or shared mailbox to send from | ✅ |
| `{{EMAIL_CATEGORIES}}` | List of communication types for this cycle | ✅ |
| `{{COMMUNICATION_TONE}}` | `formal`, `warm`, `direct` | ❌ |

---

## 📧 Email Category System

Every review cycle has a set of communication categories. Define yours in
`{{EMAIL_CATEGORIES}}`. Common patterns:

| Category | Trigger | Typical Tone |
|----------|---------|-------------|
| `new-assignment` | Person just assigned | Warm + clear instructions |
| `reminder` | Status still pending after X days | Direct + helpful |
| `thank-you` | Status is complete | Warm + appreciative |
| `exception` | N/A, withdrawn, or special case | Neutral + clear |
| `deadline-warning` | N days before cycle closes | Urgent + specific |
| `cycle-close` | Cycle has ended | Summary + next steps |

The skill groups participants by their current status, maps each group to
a category, drafts the appropriate email, and presents all drafts for review
before sending.

---

## 🔄 Pipeline Phases

### Phase 1: Load & Validate Roster
```python
import pandas as pd
from pathlib import Path

def load_roster(file_path: str, required_cols: list[str]) -> pd.DataFrame:
    """Load roster file and validate required columns exist."""
    df = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) \
         else pd.read_csv(file_path)

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    initial_count = len(df)
    df = df.dropna(subset=[required_cols[0]])  # drop rows with no name
    print(f"Loaded {len(df)} records ({initial_count - len(df)} dropped as blank)")
    return df
```

### Phase 2: Poll Statuses
```python
def poll_statuses(
    df: pd.DataFrame,
    source: str,
    status_col: str,
    api_endpoint: str | None = None
) -> pd.DataFrame:
    """Refresh status column from source system."""
    if source == "file":
        # Status already in the file — no action needed
        return df

    if source == "api" and api_endpoint:
        # For each row, call the API and update status
        # Auth must be handled externally (no credentials in skill)
        import requests
        for i, row in df.iterrows():
            try:
                resp = requests.get(
                    f"{api_endpoint}/{row['id']}",
                    timeout=10
                )
                if resp.ok:
                    df.at[i, status_col] = resp.json().get("status", "Unknown")
            except Exception as e:
                df.at[i, status_col] = f"Error: {e}"
        return df

    raise ValueError(f"Unknown status source: {source}")
```

### Phase 3: Categorize Participants
```python
def categorize(
    df: pd.DataFrame,
    status_col: str,
    complete: list[str],
    pending: list[str],
    exceptions: list[str]
) -> dict[str, pd.DataFrame]:
    """Split roster into communication categories by status."""
    cats = {
        "complete": df[df[status_col].isin(complete)],
        "pending": df[df[status_col].isin(pending)],
        "exception": df[df[status_col].isin(exceptions)],
        "unknown": df[~df[status_col].isin(complete + pending + exceptions)],
    }
    for name, group in cats.items():
        print(f"  {name}: {len(group)} records")
    return cats
```

### Phase 4: Draft Communications
```
For each {{EMAIL_CATEGORIES}} entry:
  1. Get the participant group for that category
  2. Draft the email using tone and context from intake
  3. Personalize: insert name, assignment, deadline, program name
  4. Present all drafts grouped by category
  5. User reviews and edits each draft
  6. Confirm before sending any
```

### Phase 5: Send & Update Tracking
```python
def update_tracking(
    df: pd.DataFrame,
    tracking_file: str,
    status_col: str,
    sent_categories: list[str]
) -> None:
    """Write updated statuses and communication log back to tracking file."""
    from datetime import datetime
    df["last_communication"] = datetime.now().strftime("%Y-%m-%d")
    df["communication_type"] = df[status_col].apply(
        lambda s: next((c for c in sent_categories if s in c), "none")
    )
    if tracking_file.endswith('.xlsx'):
        df.to_excel(tracking_file, index=False)
    else:
        df.to_csv(tracking_file, index=False)
    print(f"Tracking updated: {tracking_file}")
```

### Phase 6: Cycle Summary Report
```
Output a markdown summary:
  - Total participants
  - Status breakdown: X complete, Y pending, Z exception
  - Communications sent: N emails across M categories
  - Completion rate: X%
  - Open items: who still needs to act
  - Next actions: recommended follow-up timing
```

---

## 📊 Example Applications

| Program | Review Type | Status Source | Categories |
|---------|------------|---------------|------------|
| Tech panel nominations | `panel` | API | new-assignment, reminder, thank-you |
| Promotion calibration | `calibration` | File | reminder, complete, exception |
| Award nominations | `nomination` | File | thank-you, deadline-warning, cycle-close |
| Performance check-ins | `performance` | File | reminder, complete |
| Training completion | `compliance` | API | reminder, thank-you, deadline-warning |

---

## ⚠️ Anti-Patterns

```
❌ Sending any email without showing the draft first
❌ Hardcoding program names, statuses, or email text (everything is a variable)
❌ Updating the tracking sheet before emails are confirmed
❌ Treating "unknown" status as "pending" (they need separate handling)
❌ Running the full cycle without a dry-run on a small sample first
❌ Storing API credentials in the skill or tracking file
❌ Closing a cycle without a summary report
```

---

## 🔁 Deployment Ladder

| Stage | Who | What to validate |
|-------|-----|------------------|
| **Refine** | Skill Owner | Categorization logic, draft quality, tracking update accuracy |
| **Prove** | Peer Teams | Works for different program types and status vocabularies |
| **Scale** | Enterprise | Multi-cycle tracking, cross-program reporting, API status sources |
