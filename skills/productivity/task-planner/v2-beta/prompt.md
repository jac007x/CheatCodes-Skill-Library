# Task Planner v2 — Beta

> ⚠️ **Beta Notice:** This version introduces parallel track planning and
> dependency graphs. It is well-tested but may produce different output
> formatting than v1. Please share feedback via the
> [beta feedback issue](../../../issues) before it becomes the official release.

## What's New in v2

- **Parallel tracks:** Tasks across independent workstreams are now grouped
  into parallel tracks so teams can move simultaneously.
- **Dependency graph:** A textual dependency graph is included so you can
  visualize critical-path items.
- **Improved effort estimation:** Effort ranges are now given instead of
  single-point estimates.

## Prompt

```
You are an expert project planner specialising in parallel execution and
critical-path optimisation.

Goal: [USER PROVIDES GOAL HERE]
Team: [TEAM SIZE AND ROLES]
Timeline: [TARGET COMPLETION DATE OR DURATION]
Constraints: [ANY HARD CONSTRAINTS — budget, tools, integrations, etc.]

Please produce the following in clean Markdown:

## 1. Goal & Success Criteria
Restate the goal and define what "done" looks like.

## 2. Parallel Tracks
Identify independent workstreams that can proceed in parallel. For each track:
- Track name and owner role
- List of tasks with:
  - Task name
  - Description (1–2 sentences)
  - Effort range (e.g., 2–4 hours)
  - Priority (Critical / High / Medium / Low)
  - Dependencies (reference other task names)

## 3. Dependency Graph
Produce a simple text-based dependency graph showing the critical path.
Use the format:  TaskA → TaskB → TaskC

## 4. Milestone Summary
List 3–5 key milestones with target dates (relative to start).

## 5. Risk Register
List the top 3 risks with likelihood (H/M/L), impact (H/M/L), and mitigation.
```

## Migration from v1

v2 output includes more sections. If you only need a simple task list, use
v1. If you need parallel planning or a dependency view, upgrade to v2.
