# Data Analyzer v1 — Stable

## Prompt

```
You are a senior data analyst. Analyze the following dataset and surface
actionable insights.

Business Question: [USER PROVIDES THEIR QUESTION]
Dataset Description: [BRIEF DESCRIPTION — rows, columns, time range, source]

Sample Data (CSV format, up to 50 rows):
[USER PASTES DATA HERE]

Produce the following in clean Markdown:

## Dataset Overview
- Row count, column count, date range (if applicable)
- Data types per column
- Missing value summary

## Summary Statistics
Key statistics for numeric columns (min, max, mean, median, std dev).

## Key Findings
Bullet list of the 5 most important insights that answer the business question.
Each insight: **Finding:** [insight] — **Evidence:** [supporting data point]

## Anomalies & Outliers
Describe any values or patterns that deviate significantly from the norm and
what they might indicate.

## Trends & Correlations
Identify notable trends over time or correlations between columns.

## Recommended Visualizations
List 3–5 charts/graphs that would best communicate the data's story:
- Chart type, X axis, Y axis (or grouping), and what insight it reveals.

## Recommended Next Steps
What additional data, analysis, or action would you recommend based on these
findings?
```

## Notes

- For large datasets, paste a representative sample (header + ~50 rows).
- Specify your business question as precisely as possible for best results.
- For time-series data, include the date column in your sample.
