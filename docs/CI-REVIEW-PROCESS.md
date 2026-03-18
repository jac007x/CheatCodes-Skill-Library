# Continuous Improvement Review Process

## Overview

Regular reviews ensure the skills library stays:
- **Relevant** - Skills solve real problems
- **Quality** - Skills are well-documented and tested
- **Complete** - Gaps are identified and addressed
- **Current** - Skills evolve with changing needs

---

## Review Cadence

### Weekly Triage (15 min)
**When**: Every Monday
**Who**: Library maintainer

**Checklist**:
- [ ] Review new issues and label appropriately
- [ ] Respond to urgent bugs
- [ ] Merge ready PRs
- [ ] Update issue priorities

### Monthly Skill Review (1 hour)
**When**: First week of each month
**Who**: Library maintainer + stakeholders

**Agenda**:
1. **Usage Review** (15 min)
   - Which skills are being used?
   - Any adoption blockers?

2. **Gap Analysis** (15 min)
   - What's missing?
   - New requests to review?

3. **Enhancement Review** (15 min)
   - Pending enhancements
   - Prioritization decisions

4. **Roadmap Update** (15 min)
   - Adjust priorities
   - Update timelines

### Monthly Search Party (1-2 hours)
**When**: Second week of each month (after skill review)
**Who**: Any contributor (volunteer scout)

**Purpose**: Discover skills from external sources for curation

**Workflow**:
1. **Source Scan** (30 min) - Check primary discovery sources
2. **Quick Evaluation** (30 min) - Score candidates
3. **Document Candidates** (30 min) - Create issues for passing candidates

See [SKILL-DISCOVERY.md](./SKILL-DISCOVERY.md) for full process.

### Quarterly Retrospective (2 hours)
**When**: End of each quarter
**Who**: All contributors

**Agenda**:
1. **Metrics Review**
   - Skills shipped
   - Skills in use
   - User satisfaction

2. **What Worked**
   - Successful patterns
   - Good contributions

3. **What Didn't**
   - Blockers encountered
   - Skills that didn't land

4. **Roadmap Refresh**
   - Next quarter priorities
   - Resource planning

---

## Skill Health Checks

### Monthly Health Assessment

For each skill in the library, assess:

| Dimension | Questions | Score |
|-----------|-----------|-------|
| **Usage** | Is anyone using it? How often? | 1-5 |
| **Quality** | Any open bugs? Documentation gaps? | 1-5 |
| **Relevance** | Still solving a real problem? | 1-5 |
| **Maintenance** | Is it being maintained? Updates needed? | 1-5 |

**Health Score Interpretation**:
- **16-20**: Healthy - continue as-is
- **12-15**: Needs attention - schedule improvements
- **8-11**: At risk - major intervention needed
- **4-7**: Consider deprecation

### Skill Health Dashboard

```markdown
| Skill | Usage | Quality | Relevance | Maintenance | Total | Status |
|-------|-------|---------|-----------|-------------|-------|--------|
| mbr-engine | 4 | 4 | 5 | 4 | 17 | ✅ Healthy |
```

---

## Gap Analysis Framework

### 1. Identify Gaps

**Sources**:
- User feedback and requests
- Workflow analysis (what's still manual?)
- Industry trends (what are others automating?)
- Pain point surveys

**Questions**:
- What tasks take the most time?
- What tasks are error-prone?
- What tasks require specialized knowledge?
- What tasks are repetitive?

### 2. Evaluate Gaps

| Criteria | Weight | Score (1-5) |
|----------|--------|-------------|
| Time savings potential | 30% | |
| Error reduction potential | 20% | |
| Frequency of task | 20% | |
| Number of users affected | 15% | |
| Technical feasibility | 15% | |

**Priority Score** = Weighted sum of scores

### 3. Prioritize Gaps

```
High Priority (Score > 4.0)  → Q1 Roadmap
Medium Priority (3.0-4.0)    → Q2 Roadmap
Low Priority (< 3.0)         → Backlog
```

---

## Enhancement Identification

### Sources of Enhancement Ideas

1. **User Feedback**
   - Direct requests
   - Usage pattern analysis
   - Error/frustration reports

2. **Internal Review**
   - Code quality improvements
   - Performance optimizations
   - Documentation gaps

3. **External Trends**
   - New technologies
   - Industry best practices
   - Competitive analysis

### Enhancement Prioritization Matrix

```
                    High Value
                        │
           ┌────────────┼────────────┐
           │  SCHEDULE  │  DO NOW    │
           │            │            │
Low Effort ├────────────┼────────────┤ High Effort
           │  MAYBE     │  CONSIDER  │
           │            │            │
           └────────────┼────────────┘
                        │
                    Low Value
```

---

## New Skill Evaluation

### Intake Process

1. **Request Received** → Issue created
2. **Initial Triage** → Label + assign
3. **Feasibility Check** → Technical review
4. **Value Assessment** → Stakeholder input
5. **Decision** → Approve / Defer / Reject

### Evaluation Criteria

| Criteria | Questions | Weight |
|----------|-----------|--------|
| **Value** | How much time/effort does it save? | 25% |
| **Reach** | How many people will use it? | 20% |
| **Feasibility** | Can we build it? How hard? | 20% |
| **Uniqueness** | Does something similar exist? | 15% |
| **Alignment** | Does it fit our library's purpose? | 10% |
| **Maintainability** | Can we maintain it long-term? | 10% |

### Decision Framework

- **Score > 4.0** → Approve and schedule
- **Score 3.0-4.0** → Approve if contributor available
- **Score < 3.0** → Defer or reject

---

## Feedback Collection

### Channels

1. **GitHub Issues** - Formal requests and bugs
2. **Slack Channel** - Quick questions and feedback
3. **Monthly Survey** - Structured feedback collection
4. **Usage Analytics** - Implicit feedback

### Survey Questions (Monthly)

1. Which skills have you used this month?
2. Rate your satisfaction with each skill (1-5)
3. What's missing that would help you?
4. Any skills that aren't meeting your needs?
5. Suggestions for improvements?

### Feedback Loop

```
Collect → Analyze → Prioritize → Implement → Communicate
   ↑                                              │
   └──────────────────────────────────────────────┘
```

---

## Metrics Dashboard

### Key Metrics

| Metric | Definition | Target | How to Measure |
|--------|------------|--------|----------------|
| **Skill Count** | Total skills in library | 10+ | Count in registry |
| **Active Skills** | Skills used in past 30 days | 80% | Usage tracking |
| **Request Resolution** | % of requests addressed | 80% | Issue tracking |
| **Time to Ship** | Days from request to release | <14 | Issue timestamps |
| **User Satisfaction** | Avg rating across skills | 4.0+ | Survey |
| **Contributor Count** | Unique contributors | 5+ | Git history |

### Tracking Template

```markdown
## Monthly Metrics - [Month Year]

| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| Skill Count | 10 | | |
| Active Skills | 80% | | |
| Request Resolution | 80% | | |
| Time to Ship | <14 days | | |
| User Satisfaction | 4.0 | | |
| Contributors | 5 | | |

### Highlights
-

### Concerns
-

### Actions
-
```
