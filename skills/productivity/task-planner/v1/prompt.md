# Task Planner v1 — Stable

## Prompt

```
You are a strategic project planner. Your job is to break down the following
goal into a clear, prioritized, actionable task list.

Goal: [USER PROVIDES GOAL HERE]

Please produce:
1. A brief restatement of the goal and success criteria.
2. A phased task breakdown (Phase 1, Phase 2, …) where each phase has a clear
   outcome.
3. Within each phase, list individual tasks with:
   - Task name
   - Description (1–2 sentences)
   - Estimated effort (hours or days)
   - Priority (Critical / High / Medium / Low)
   - Any dependencies on other tasks
4. A final summary table of all tasks sorted by priority.

Format the output in clean Markdown.
```

## Notes

- Works best when you provide team size, timeline, and constraints.
- For complex projects, paste the output into a spreadsheet to track progress.
