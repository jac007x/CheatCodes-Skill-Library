# MBR Engine — v1 Prompt

> **Status:** Beta ⚠️ | Use for MBR preparation and org health analysis

## Prompt

```
You are an expert HR analytics partner preparing a Monthly Business Review.

Organisation: [ORG NAME]
Reporting Month: [MONTH]
Focus Areas: [KEY CONCERNS]

Produce the following in Markdown:

## Executive Summary
2–3 sentences on overall org health this month.

## Headcount Snapshot
Current HC, change vs prior month, vs AOP plan.

## Attrition Analysis
Voluntary/involuntary split, regrettable attrition rate, top exit reasons.

## Org Health Indicators
Flag any threshold breaches (e.g. attrition > 3%, span of control < 4).

## Recognition & Engagement
MADA budget utilisation, recognition rate vs target.

## Key Risks & Recommendations
Top 3 risks with recommended actions and owners.

## Next Month Focus
2–3 priorities for the coming month.
```

## Placeholders

| Placeholder | What to fill in | Example |
|-------------|----------------|---------|
| `[ORG NAME]` | Your organisation or team name | `Engineering`, `Sales EMEA` |
| `[MONTH]` | Reporting month in YYYY-MM format | `2026-03` |
| `[KEY CONCERNS]` | Any specific focus areas for this review | `attrition spike in APAC` |

## Notes

- For full automation (data extraction + PowerPoint generation), see the
  implementation details in [`../README.md`](../README.md).
- This prompt is the lightweight, AI-assistant version for quick MBR drafts.
- The automated v2 workflow requires Python ≥ 3.10 and the packages listed
  in [`../skill.yaml`](../skill.yaml).
