# CheatCodes Skill Library

A library to collect, store, chain, and bundle AI agent skills for Wibey and other AI assistants.

## What is a Skill?

A **skill** is a reusable, documented capability that AI agents can leverage to accomplish specific tasks. Skills can be:
- **Standalone** - Complete workflows (e.g., MBR generation)
- **Composable** - Building blocks that chain together
- **Configurable** - Adaptable to different contexts and organizations

### Skill Sources

| Type | Badge | Description |
|------|-------|-------------|
| **Created** | 🛠️ | Built in-house from scratch |
| **Curated** | 📚 | Discovered externally and adapted |
| **Forked** | 🔱 | Forked from open source and customized |

## Library Structure

```
CheatCodes-Skill-Library/
├── skills/                    # Individual skill packages
│   ├── mbr-engine/           # Monthly Business Review automation
│   └── ...
├── templates/                 # Skill templates for creating new skills
├── docs/                      # Documentation and guides
└── registry.json             # Skill registry metadata
```

## Available Skills

| Skill | Source | Description | Status |
|-------|--------|-------------|--------|
| [mbr-engine](skills/mbr-engine/) | 🛠️ Created | Monthly Business Review automation with org health metrics, feature detection, and PowerPoint generation | In Development |
| [msgraph-people](skills/msgraph-people/) | 📚 Curated | Calendar & Email workflows for People function - 1:1 scheduling, email templates, meeting prep | Active |
| [document-processing](skills/document-processing/) | 📚 Curated | PDF, PowerPoint, and Form extraction patterns | Active |
| [confluence-people](skills/confluence-people/) | 📚 Curated | Knowledge management for People - policies, processes, documentation | Active |
| [jira-people](skills/jira-people/) | 📚 Curated | Work management for People - requests, initiatives, reporting | Active |

## Quick Start

### Using a Skill

```python
# Example: Using the MBR Engine skill
from mbr_engine import MBRWorkflow, MBRSourceFiles

sources = MBRSourceFiles(
    roster_file="path/to/roster.xlsx",
    mada_file="path/to/recognition.xlsx",
)

workflow = MBRWorkflow(sources=sources, month="2026-03")
result = workflow.run()
workflow.generate_slides(result, output_filename="MBR_March.pptx")
```

### Creating a New Skill

1. Copy the template: `cp -r templates/skill-template skills/my-skill`
2. Update `skill.yaml` with metadata
3. Implement the skill logic
4. Add documentation
5. Register in `registry.json`

## Skill Specification

Each skill should include:

```yaml
# skill.yaml
name: my-skill
version: 1.0.0
description: What this skill does
author: Your Name
tags: [category, type]

requires:
  python: ">=3.10"
  packages: [pandas, openpyxl]

inputs:
  - name: data_file
    type: file
    required: true

outputs:
  - name: report
    type: file
```

## Contributing

### Create a New Skill
1. Fork the repository
2. Create your skill in `skills/your-skill/`
3. Add documentation
4. Submit a PR

### Curate an External Skill
1. [Submit a curation request](../../issues/new?template=curate-skill.yml)
2. We'll evaluate and adapt it
3. Attribution is always maintained

### Request a Search Party
Need a tool we don't have? [Trigger a search party](../../issues/new?template=search-party.yml) to find external options.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/SKILL-DISCOVERY.md](docs/SKILL-DISCOVERY.md) for full guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
