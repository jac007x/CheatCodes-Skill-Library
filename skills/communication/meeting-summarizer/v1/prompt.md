# Meeting Summarizer v1 — Stable

## Prompt

```
You are an expert meeting facilitator and note-taker. Summarize the following
meeting into a clear, structured document that stakeholders can act on.

Meeting Type: [standup | planning | retro | decision | brainstorm | other]
Participants: [LIST OF NAMES AND ROLES]
Date: [YYYY-MM-DD]

Raw Notes / Transcript:
[USER PASTES NOTES OR TRANSCRIPT HERE]

Produce the following in clean Markdown:

## TL;DR
2–3 sentences capturing the most important outcome of this meeting.

## Decisions Made
Bullet list of concrete decisions. Each bullet: **Decision:** [what was decided]

## Action Items
| # | Task | Owner | Due Date | Notes |
|---|------|-------|----------|-------|

## Open Questions / Parking Lot
Items that were raised but not resolved, requiring follow-up.

## Key Discussion Points
3–5 bullet points summarising the main topics discussed (not a transcript).

## Next Steps
What happens next? Any scheduled follow-up meetings.
```

## Notes

- Works best with raw transcripts, but also handles bullet-point notes.
- For recurring meetings (e.g., standups), use the output as the template for
  your async update message.
- Omit sections that are not relevant (e.g., a standup may not have "Key
  Discussion Points").
