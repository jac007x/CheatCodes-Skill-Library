# Contributing to CheatCodes Skill Library

Thank you for helping make the skill library better! This guide explains
exactly how to contribute — whether you're a first-timer or a regular.

---

## Ways to contribute

### 1. Request a new skill (no coding needed)
[Open a Skill Request issue](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=skill_request.yml)
and describe what you need. The team reviews requests 2–3 times a week.

### 2. Suggest an improvement (no coding needed)
[Open a Skill Recommendation issue](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=skill_recommendation.yml)
and describe your idea.

### 3. Submit a community-fortified version
Tested a better version of an existing skill?
[Open a Community Contribution issue](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=community_contribution.yml)
with your improved prompt.

### 4. Fix a bug
[Open a Bug Report issue](https://github.com/jac007x/CheatCodes-Skill-Library/issues/new?template=bug_report.yml)
or submit a PR with the fix.

### 5. Add a new skill via pull request
See the [Adding a new skill](#adding-a-new-skill) section below.

---

## Adding a new skill

### Step 1 — Copy the template

```bash
# Replace <category> and <skill-name> with your values
cp -r templates/skill-template skills/<category>/<skill-name>
```

Categories: `productivity`, `automation`, `communication`, `data`, `devops`, `security`, `custom`

### Step 2 — Fill in the manifest

Edit `skills/<category>/<skill-name>/skill.yaml` and replace every `<placeholder>`.

Key fields:
- `name` — kebab-case, unique within the category
- `version` — start at `1.0.0`
- `status` — start at `beta`; the maintainer will promote to `stable` after feedback

### Step 3 — Write the prompt

Create a versioned folder and add your prompt:

```
skills/<category>/<skill-name>/
├── skill.yaml
├── README.md
└── v1/
    └── prompt.md
```

The prompt should:
- Use `[PLACEHOLDER_NAME]` for every variable the user needs to fill in.
- Produce output in clean Markdown.
- Include a clear structure (e.g., numbered sections, tables).
- Be tested with at least 3 different inputs.

### Step 4 — Write the README

Edit `skills/<category>/<skill-name>/README.md` using the template.
Include at least one concrete example with input and expected output.

### Step 5 — Validate

```bash
pip install pyyaml
python scripts/validate_skills.py skills/<category>/<skill-name>
```

Fix any errors, then open a pull request.

---

## Skill quality standards

| Requirement | Detail |
|------------|--------|
| `skill.yaml` present and valid | All required fields filled in |
| `README.md` present | Includes description, usage, and at least one example |
| Versioned prompt folder | e.g. `v1/prompt.md` |
| Prompt tested | At least 3 different inputs tested before submitting |
| Output is structured Markdown | Clean, readable, actionable output |
| No hallucination traps | Prompt doesn't encourage the AI to make up specific facts |
| Beta warning if applicable | Include a beta notice if submitting a new/untested version |

---

## Versioning guidelines

- Start all new skills at `1.0.0` with status `beta`.
- Use `MINOR` bumps for additive changes (new sections, better structure).
- Use `MAJOR` bumps for breaking changes (different output format, renamed sections).
- Promote from `beta` → `stable` only after collecting feedback from real use.
- Never delete old version folders — they stay in the repo as the back-catalog.

---

## Review process

1. Submit a PR.
2. CI automatically validates your skill manifest and structure.
3. The maintainer reviews within 2–3 business days.
4. Approved PRs are merged and tagged with a release.

---

## Code of conduct

Be kind, constructive, and respectful. This library exists to help everyone.
