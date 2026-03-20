---
name: powerbi-reports
description: Pull reports, query data, apply filters, and schedule report bundles from PowerBI dashboards using natural language. Supports DAX queries, CSV/HTML exports, scheduled delivery, and interactive exploration of Walmart PowerBI workspaces.
version: 1.1.0
author: jac007x
tags:
  - powerbi
  - reporting
  - data
  - analytics
  - scheduling
  - walmart
  - qa-kitten
  - browser-automation
---

# 📊 PowerBI Reports Skill

This skill teaches Velcro (and QA Kitten as fallback) how to pull reports, query data with filters, build HTML dashboards, and schedule report bundles from Walmart's PowerBI environment using natural language.

---

## 🧠 Core Philosophy

- **Tier 1 — PowerBI sub-agent (API):** Always try this first. Fast, structured, DAX-powered, no UI needed.
- **Tier 2 — QA Kitten (browser automation):** When the API is blocked (app consumer access, no Build permission, 401/404 on DAX), QA Kitten navigates PowerBI like a real human user — applying filters, clicking slicers, and using PowerBI's built-in Export Data feature to pull CSVs directly.
- **Natural language in → structured data out** — translate the user's request into DAX (Tier 1) or browser actions (Tier 2)
- **Always discover before querying** — understand the report structure before diving in
- **Output should be useful** — default to a beautiful HTML report with charts unless the user asks otherwise

---

## 🚀 Decision Tree: Which Tier To Use?

```
User requests PowerBI data
         │
         ▼
┌─────────────────────────────┐
│ Try PowerBI API sub-agent   │
│ - List workspaces/datasets  │
│ - Get dataset schema        │
│ - Execute DAX query         │
└────────────┬────────────────┘
             │
     DAX works? ──── YES ──→ 🟢 Tier 1: Return data, build HTML report
             │
            NO (401 / 403 / 404 on executeQueries)
             │
             ▼
┌─────────────────────────────┐
│ User has browser access?    │
│ (can see report in browser) │
└────────────┬────────────────┘
             │
            YES
             │
             ▼
  🐱 Tier 2: Invoke QA Kitten
  Navigate → Filter → Export
```

**Switch to QA Kitten (Tier 2) when:**
- DAX `executeQueries` returns 401/403/404 (app consumer access only)
- User is not a workspace member or doesn't have Build permission
- The visual uses custom/certified visuals that don't expose raw data via API
- User needs a screenshot of a specific visual exactly as it appears

---

## 🚀 Tier 1: PowerBI API Flow

### Step 1: Understand the Request
Parse the user's natural language request to identify:
- **What data** they want (roster, metrics, headcount, etc.)
- **What filters** to apply (L2 org, date range, region, store, etc.)
- **What format** they want (HTML report, CSV, summary, scheduled bundle)
- **What workspace/report** (extract IDs from any PowerBI URL they share)

### Step 2: Discover the Data
Always invoke the `powerbi` sub-agent to discover before querying:
```
1. powerbi_list_workspaces()                    → find the right workspace_id
2. powerbi_list_datasets(workspace_id)           → find the right dataset_id
3. powerbi_get_dataset_tables(dataset_id)        → see what tables exist
4. powerbi_get_table_columns(dataset_id)         → understand the schema
5. powerbi_get_measures(dataset_id)              → find pre-built measures
```

### Step 3: Query with DAX
Translate the user's request into a DAX query. All DAX must begin with `EVALUATE`.

### Step 4: Output the Results
Default output: **Build a flat HTML report** with Tailwind CSS + Chart.js and open it on their Mac.
Alternative outputs: CSV export, JSON, or written summary — follow user preference.

---

## 🗣️ Natural Language → DAX Translation Guide

### Date Filters
| User says | DAX pattern |
|---|---|
| "this week" | `FILTER('Table', 'Table'[D TODAY()-7)` |
| "last month" | `FILTER('Table', MONTH('Table'[Date]) = MONTH(TODAY())-1)` |
| "Q1 2025" | `FILTER('Table', 'Table'[Date] >= DATE(2025,1,1) && 'Table'[Date] <= DATE(2025,3,31))` |
| "year to date" | `FILTER('Table', YEAR('Table'[Date]) = YEAR(TODAY()))` |
| "last 30 days" | `FILTER('Table', 'Table'[Date] >= TODAY()-30)` |

### Aggregation Patterns
| User says | DAX pattern |
|---|---|
| "total sales by region" | `SUMMARIZE('Sales', 'Sales'[Region], "Total", SUM('Sales'[Amount]))` |
| "count by category" | `SUMMARIZE('Table', 'Table'[Category], "Count", COUNTROWS('Table'))` |
| "top 10 stores" | `TOPN(10, SUMMARIZE(...), [Total], DESC)` |
| "average by month" | `SUMMARIZE(..., 'Date'[Month], "Avg", AVERAGE('Table'[Value]))` |

### Multi-Table Patterns
Use `SUMMARIZECOLUMNS` when joining across multiple tables:
```dax
EVALUATE
SUMMARIZECOLUMNS(
    'Product'[Category],
    'Date'[Year],
    'Store'[Region],
    "Revenue", [Total Revenue],
    "Units", [Total Units Sold]
)
```

---

## 🎛️ Filter Patterns

When a user specifies filters, layer them using `CALCULATETABLE` or `FILTER`:

```dax
EVALUATE
CALCULATETABLE(
    SUMMARIZE(
        'Sales',
        'Sales'[Category],
        "Total", SUM('Sales'[Amount])
    ),
    'Sales'[Region] = "Southeast",
    'Date'[Year] = 2025
)
```

For dynamic multi-value filters (e.g., "show me regions A, B, and C"):
```dax
EVALUATE
CALCULATETABLE(
    'Sales',
    'Sales'[Region] IN {"Southeast", "Midwest", "Northeast"}
)
```

---

## 📤 Output Formats

### HTML Report (Default)
Build a flat HTML file using:
- **Tailwind CSS** (CDN) for styling
- **Chart.js** (CDN) for visualizations
- **Walmart brand colors**: primary blue `#0053e2`, accent yellow `#ffc220`
- Wrap each `<canvas>` in a fixed-height container div (Chart.js ignores canvas height when responsive: true)
- Include: executive summary at top, daily/monthly/quarterly breakdowns, insights section at bottom
- Open on Mac with: `open /path/to/report.html`

```html
<!-- Example canvas wrapper pattern -->
<div style="height: 300px; position: relative;">
  <canvas id="myChart"></canvas>
</div>
```

### CSV Export
Use `powerbi_export_dax_query_to_csv(dataset_id, dax_query, output_path)`

### Share on puppy.walmart.com
After building HTML, invoke the `share-puppy` sub-agent to share it:
```
invoke_agent('share-puppy', 'Share this HTML report: /path/to/report.html')
```
Then give the user a clickable CLI link.

### Written Summary
Pull data via DAX, then write a concise executive summary with key insights, trends, and anomalies.

---

## 📅 Scheduled Report Bundles

Users can schedule a bundle of reports to run at regular intervals (daily, weekly, monthly).

### How to Set Up Scheduling
Use the `scheduler-agent` sub-agent:

```
invoke_agent('scheduler-agent', 'Schedule a daily report bundle at 8am:
- Sales summary by region (last 7 days)
- Top 10 stores by revenue
- Inventory levels by category
Build as HTML and share on puppy.walmart.com')
```

### Bundle Configuration Pattern
When a user asks to schedule reports, capture:
1. **Report list** — what reports/queries to run
2. **Filters** — standing filters for each report
3. **Frequency** — daily / weekly (which day?) / monthly (which date?)
4. **Time** — what time to run
5. **Output** — HTML + share, CSV, email, etc.

Save the bundle as a named prompt and register it with the scheduler.

### Example Bundle Prompt to Save
```
Run my weekly PowerBI bundle:
1. Pull Sales by Region for last 7 days from [workspace/dataset]
2. Pull Top 10 Stores by Revenue YTD
3. Pull Inventory Turns by Category for current month
Build a single combined HTML report with all three sections.
Share on puppy.walmart.com and give me the link.
```

---

## 🔗 PowerBI URL Parsing

If the user gives a PowerBI URL, extract IDs like this:

```
https://app.powerbi.com/groups/{workspace_id}/reports/{report_id}/...
https://app.powerbi.com/groups/{workspace_id}/datasets/{dataset_id}
```

- `groups/{uuid}` → `workspace_id`
- `reports/{uuid}` → `report_id`
- `datasets/{uuid}` → `dataset_id`

Use these directly in API calls — no need to search/list first.

---

## 🐱 Tier 2: QA Kitten Browser Extraction

When the PowerBI API is blocked, QA Kitten navigates PowerBI exactly like a human user would — logging in via PingFed SSO, clicking slicers, applying filters, and using PowerBI's built-in **"Export Data"** button to download CSVs directly from each visual.

### Standard QA Kitten PowerBI Extraction Prompt

When invoking QA Kitten for PowerBI extraction, always include ALL of the following context:

```
invoke_agent('qa-kitten', '''
Please extract data from a PowerBI report. Here is everything you need:

URL: [full PowerBI report URL]
Associate ID / Login: [user's ID]

Filters to apply:
- [Slicer name]: [value]   e.g. "L2 Org": "AI Product and Design"
- [Slicer name]: [value]   e.g. "Date": "Last 30 Days"

What to extract:
- [Describe the visual/table to extract, e.g. "the employee roster table"]
- [If multiple visuals, list each one]

Extraction method (in order of preference):
1. Use the "..." (More options) menu on each visual → click "Export data" → save as CSV
2. If export is disabled, read the table data directly from the DOM
3. If the data is in a chart (not a table), take a screenshot and transcribe visible values

Troubleshooting:
- If PingFed/SSO login appears, enter the associate ID and complete login
- If a new window or tab opens for a module/visual, switch to it and work there
- If language selection appears, choose English and continue
- If the page doesn't load or shows a spinner for >10 seconds, refresh and retry
- If a visual shows "Can't display the visual", scroll past it and continue with others
- After applying each filter/slicer, wait 3-5 seconds for the report to re-render

After extracting:
- Return the data as a structured table
- Note which filters were applied
- Note the "Last refreshed" timestamp shown in the report if visible
''')
```

### Step-by-Step: What QA Kitten Should Do

**1. Navigate & Authenticate**
```
- Go to the PowerBI URL
- If redirected to PingFed/SSO login, enter the associate ID
- Wait for the report to fully load (look for visuals rendering, not spinner)
```

**2. Apply Filters**
```
- Locate the slicer/filter panel (usually left side or top of report)
- Click the target slicer (e.g. "L2", "Org", "Date Range")
- Type or select the filter value
- Wait 3-5 seconds for the report to re-render after each filter
- Confirm the visual titles/counts update to reflect the filter
```

**3. Export Data from Each Visual**

For **table/matrix visuals** (the best case):
```
- Hover over the visual to reveal the "..." (More options) button in the top-right corner
- Click "..." → select "Export data"
- Choose "Underlying data" if offered (gets raw rows, not just summarized)
- Choose "Summarized data" as fallback
- Select CSV format → click Export
- The file downloads automatically to the Downloads folder
```

For **chart visuals** (bar, line, pie, etc.):
```
- Try "..." → "Export data" first (works for most standard charts)
- If export is disabled, use "..." → "Show as a table" to render data as a table, then export
- As a last resort, take a screenshot and transcribe the visible data values
```

For **card/KPI visuals** (single number tiles):
```
- Take a screenshot and read the displayed value
- Note the metric name from the visual title
```

**4. Handle Common Issues**

| Problem | Fix |
|---|---|
| Spinner won't stop | Refresh the page (F5), wait for reload, re-apply filters |
| New window opens | Switch to new window, complete action, come back |
| Language selection popup | Choose English, confirm |
| "Export data" greyed out | Report admin disabled it — use "Show as a table" instead |
| Visual won't render | Scroll past, note it as unavailable, continue with others |
| SSO redirect loop | Clear cookies for app.powerbi.com, log in fresh |
| Filter not applying | Click directly on a slicer value (not just the slicer header) |
| Page loads but no data | Check if another filter is conflicting — clear all filters, re-apply one at a time |

**5. Return & Build Report**

After QA Kitten extracts the data:
```
- Take all extracted CSVs / table data
- Build a flat HTML report with Tailwind + Chart.js (Walmart colors: #0053e2, #ffc220)
- Include the filter context ("Filtered to: L2 = AI Product and Design")
- Include data freshness note (last refresh timestamp from the report)
- Open the HTML report on the user's Mac with: open /path/to/report.html
```

### ARS Campus Specific Context (jac007x's Dashboard)

For the **Associate Reporting Suite for Campus** app:
- **App URL base:** `https://app.powerbi.com/groups/me/apps/f9b7a9d5-9cfd-466e-88d2-001fd5b863d3`
- **Daily Roster report:** append `/reports/235da2e2-7ef4-48fb-a4a1-8426108295dc`
- **Org Overview:** append `/reports/4562e1a4-443f-43e9-b7cd-4177b1571515`
- **Movement Summary:** append `/reports/059d57f0-e232-4a71-a0ec-ec9e461da177`
- **Compensation:** append `/reports/83d881d9-f665-43d9-a02b-a22c21512564`
- **Talent & Performance:** append `/reports/390ec7bd-4f51-4185-b60d-b113c0b13100`
- **Recognition:** append `/reports/78a44024-5f57-4ecf-850e-fe7a6f767ce9`
- **Workday Recruiting:** append `/reports/1e0a6e03-0912-4706-81ee-52153143e880`

Key slicers in the ARS Campus reports:
- **L2** — top-level org area (e.g. "AI Product and Design")
- **L3 / L4 / L5 / L6** — drill-down org levels
- **Management Level** — filter by IC vs manager level
- **Pay Rate Type** — Hourly vs Salary
- **Facility / Region / Market** — location filters

---

## 🔍 Schema Discovery Cheat Sheet

Always run these before writing DAX for an unfamiliar dataset:

```
# What tables exist?
EVALUATE INFO.VIEW.TABLES()

# What columns in each table?
EVALUATE INFO.COLUMNS()

# What measures are pre-built?
EVALUATE INFO.VIEW.MEASURES()

# What does this dataset connect to?
powerbi_get_datasources(dataset_id)

# When was data last refreshed?
powerbi_get_refresh_history(dataset_id)
```

---

## ⚡ Pro Tips

1. **Check refresh history first** — if the dataset hasn't refreshed recently, warn the user the data may be stale
2. **Use pre-built measures** — `powerbi_get_measures()` reveals calculated measures that are often more accurate than raw column aggregations
3. **Paginate big workspaces** — check `has_more` in responses and use `next_skip` to get all results
4. **Clone before modifying** — if a user wants to modify a report, clone it first to preserve the original
5. **DAX must start with EVALUATE** — always, no exceptions
6. **Prefer SUMMARIZECOLUMNS for multi-table** — more efficient than nested SUMMARIZE + RELATED
7. **Fix chart heights** — wrap every Chart.js canvas in a fixed-height div container
8. **Walmart colors** — always use `#0053e2` (blue) and `#ffc220` (spark yellow) in reports
9. **HIPAA data** — never export or share data containing HIPAA patient data
10. **VPN required** — all PowerBI API calls require Walmart VPN or Eagle WiFi

---

## 🎯 Example Invocations

### Simple Data Pull
> "Pull me the total sales by region for last month"
```
1. Find workspace + dataset
2. Check schema
3. Run DAX with date + groupby filters
4. Build HTML report and open it
```

### Filtered Report
> "Show me the top 20 stores by shrink rate in the Southeast region for Q1 2025"
```
1. Find dataset
2. DAX: TOPN(20, CALCULATETABLE(SUMMARIZE(...), Region="Southeast", Q1 filter), [Shrink Rate], DESC)
3. HTML table + bar chart
```

### Scheduled Bundle
> "Every Monday at 7am, pull my weekly ops dashboard and share it"
```
1. Clarify which reports/datasets to include
2. Capture standing filters
3. Build the bundle prompt
4. Register with scheduler-agent
```

### From a PowerBI Link
> "https://app.powerbi.com/groups/abc-123/reports/xyz-456 — pull me this data as CSV"
```
1. Parse workspace_id=abc-123, report_id=xyz-456
2. Get the report's dataset_id via powerbi_get_report()
3. Discover schema
4. Run DAX
5. Export to CSV
```

---

## 🔒 Security & Compliance

- All data stays inside Walmart's network via the Element LLM Gateway
- You can only access PowerBI content your account has permission to see
- 403 errors = missing permissions — check workspace roles
- Do NOT export or share HIPAA patient data
- Non-PII data files are fine to save and share
- When in doubt, ask the user to confirm the sensitivity of the data before exporting
