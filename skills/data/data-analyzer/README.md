# Data Analyzer

> **Status:** `v1 stable` | **Category:** `data`

## Overview

Analyzes a dataset and produces insights, summary statistics, anomaly
detection, trend identification, and visualization recommendations — answering
a specific business question with evidence from the data.

---

## Quick Start

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/jac007x/CheatCodes-Skill-Library/main/scripts/clone-skill.sh) data/data-analyzer
```

Or use the prompt directly: [v1/prompt.md](v1/prompt.md)

---

## Usage

1. Copy the prompt from [v1/prompt.md](v1/prompt.md).
2. State your business question clearly.
3. Paste a CSV sample (header + up to ~50 representative rows).
4. Review insights, anomalies, and visualization recommendations.

### Tips for Best Results

- Frame a specific business question (not "tell me about this data").
- Include a date column for time-series analysis.
- For large datasets, paste a stratified sample (include edge cases).

---

## Examples

### Monthly Sales Analysis

**Input:**
```
Business question: Which products are underperforming and why?
Dataset: Monthly sales by product, region, and rep (Jan–Dec 2023)
Sample: <CSV header + 50 rows>
```

**Output includes:**
- Dataset overview (row/column counts, types, missing values)
- Summary statistics per numeric column
- Top 5 findings answering the business question
- Anomalies and outliers
- Trends and correlations
- Recommended charts (type, axes, insight)
- Recommended next steps

---

## Versioning & Changelog

| Version | Status | Date | Notes |
|---------|--------|------|-------|
| `1.0.0` | ✅ stable | 2024-02-15 | Initial release |

---

## Contributing & Feedback

- 🐛 [Report a bug](../../issues/new?template=bug_report.yml)
- 💡 [Recommend an improvement](../../issues/new?template=skill_recommendation.yml)

---

## License

MIT — see [LICENSE](../../LICENSE)
