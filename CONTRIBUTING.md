# Contributing to CheatCodes Skill Library

## How to Contribute

### 1. Request a New Skill
Open an issue using the **Skill Request** template:
- Describe the problem you're trying to solve
- Explain expected inputs/outputs
- Share example use cases

### 2. Enhance an Existing Skill
Open an issue using the **Skill Enhancement** template:
- Reference the skill to enhance
- Describe the improvement
- Explain the value add

### 3. Submit a New Skill
1. Fork the repository
2. Create your skill in `skills/your-skill-name/`
3. Include required files (see [Skill Checklist](#skill-checklist))
4. Submit a PR using the **New Skill** template

### 4. Report Issues
Open an issue using the **Bug Report** template for:
- Broken functionality
- Documentation errors
- Compatibility issues

---

## Skill Checklist

Every skill submission must include:

- [ ] `README.md` - Overview, architecture, quick start, examples
- [ ] `skill.yaml` - Metadata (name, version, inputs, outputs, dependencies)
- [ ] `CHANGELOG.md` - Version history
- [ ] Working code or detailed pseudocode
- [ ] At least one usage example

### Quality Standards

| Criteria | Requirement |
|----------|-------------|
| Documentation | Complete README with examples |
| Metadata | Valid skill.yaml with all required fields |
| Dependencies | All dependencies listed with versions |
| Portability | Works across different environments |
| Testing | Test cases or validation approach documented |

---

## Skill Lifecycle

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Draft     │────▶│   Review    │────▶│   Beta      │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
┌─────────────┐     ┌─────────────┐           │
│ Deprecated  │◀────│   Stable    │◀──────────┘
└─────────────┘     └─────────────┘
```

| Status | Description |
|--------|-------------|
| `draft` | Initial development, not ready for use |
| `review` | Under review for quality and completeness |
| `beta` | Functional but may have rough edges |
| `stable` | Production-ready, fully documented |
| `deprecated` | No longer maintained, use alternative |

---

## Review Process

### New Skill Review Criteria

1. **Usefulness** - Does it solve a real problem?
2. **Uniqueness** - Is it different from existing skills?
3. **Quality** - Is it well-documented and tested?
4. **Portability** - Can others use it easily?
5. **Maintainability** - Is the code clean and extensible?

### Enhancement Review Criteria

1. **Value** - Does it meaningfully improve the skill?
2. **Compatibility** - Does it break existing functionality?
3. **Documentation** - Are changes documented?

---

## Code of Conduct

- Be respectful and constructive
- Focus on the skill, not the person
- Share knowledge generously
- Credit others' contributions
