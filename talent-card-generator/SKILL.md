---
name: talent-card-generator
description: "Universalized pipeline for batch-generating personalized documents from data + templates. Ingests a data source (Excel/CSV/API), maps fields to template placeholders, populates one document per record, validates for completeness and correctness, and outputs a batch of formatted documents (PPTX, DOCX, PDF, HTML)."
version: 1.0.0
author: jac007x
tags:
  - document-generation
  - template-population
  - batch-processing
  - talent-cards
  - mail-merge
  - cross-platform
  - automation
---

# 🏆 Talent Card Generator

A universalized, batch document generation pipeline: take a data source,
map it to a template, populate one document per record, validate, and output.

Originally built for talent cards. Universally applicable to any
"data × template = batch of personalized documents" workflow.

---

## 🧠 Core Philosophy

- **Template is king** — the template defines the contract; data fills it
- **Validate before generate** — catch missing fields before producing garbage
- **One record = one document** — never merge multiple people into one card
- **Audit trail always** — log what was generated, what was skipped, and why
- **Idempotent** — running twice with the same data produces the same output

---

## 🚀 Intake: Customize This Skill

| Variable | Description | Type | Required | Default |
|----------|-------------|------|----------|---------|
| `{{TEMPLATE_FILE}}` | Path to template (PPTX/DOCX/HTML) | file-path | ✅ | — |
| `{{DATA_SOURCE}}` | Path to data file (CSV/XLSX) or API endpoint | string | ✅ | — |
| `{{FIELD_MAPPING}}` | Map of template placeholders → data columns | dict | ✅ | — |
| `{{ID_FIELD}}` | Column that uniquely identifies each record | string | ✅ | `"Employee ID"` |
| `{{OUTPUT_FORMAT}}` | Output document type | choice | ❌ | `"pptx"` |
| `{{OUTPUT_DIR}}` | Where to save generated documents | path | ❌ | `"./output"` |
| `{{BATCH_NAME}}` | Prefix for output filenames | string | ❌ | `"card"` |
| `{{VALIDATION_RULES}}` | Custom validation rules | dict | ❌ | `{}` |
| `{{ONE_FILE_PER_RECORD}}` | Separate file per record or all in one? | bool | ❌ | `false` |

### Output Format Options
- `pptx` — PowerPoint (python-pptx)
- `docx` — Word document (python-docx)
- `html` — HTML from Jinja2 template
- `pdf` — HTML → PDF via weasyprint or browser print

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────┐
│            TALENT CARD GENERATOR                    │
├───────────────────────────────────────────────────┤
│                                                     │
│  TEMPLATE   +   DATA   →  MAP  →  VALIDATE  →  GEN  │
│                                                     │
│  Analyze       Ingest     Field    Check for   Batch │
│  placeholders  & clean    mapping  missing/    write  │
│  in template   records    rules    bad data    docs   │
│                                       │              │
│                                  AUDIT TRAIL         │
└───────────────────────────────────────────────────┘
```

---

## Phase 1: Template Analysis

**Goal:** Parse the template to discover all placeholders.

### PPTX Templates
```python
from pptx import Presentation
import re

def extract_pptx_placeholders(template_path: str) -> set[str]:
    """Find all {{PLACEHOLDER}} patterns in a PPTX template."""
    prs = Presentation(template_path)
    placeholders = set()
    pattern = re.compile(r"\{\{(\w+)\}\}")

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    full_text = "".join(run.text for run in para.runs)
                    placeholders.update(pattern.findall(full_text))
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        placeholders.update(pattern.findall(cell.text))
    return placeholders
```

### DOCX Templates
```python
from docx import Document

def extract_docx_placeholders(template_path: str) -> set[str]:
    doc = Document(template_path)
    placeholders = set()
    pattern = re.compile(r"\{\{(\w+)\}\}")
    for para in doc.paragraphs:
        placeholders.update(pattern.findall(para.text))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                placeholders.update(pattern.findall(cell.text))
    return placeholders
```

### HTML/Jinja2 Templates
```python
from jinja2 import Environment, meta

def extract_jinja_placeholders(template_str: str) -> set[str]:
    env = Environment()
    ast = env.parse(template_str)
    return meta.find_undeclared_variables(ast)
```

### Output: Placeholder manifest
```json
{
  "template": "talent_card_template.pptx",
  "placeholders_found": ["EMPLOYEE_NAME", "TITLE", "LEVEL", "TENURE",
                          "STRENGTHS", "DEVELOPMENT_AREAS", "PHOTO_URL"],
  "count": 7
}
```

---

## Phase 2: Data Ingestion & Field Mapping

**Goal:** Load the data and map each column to a template placeholder.

```python
def build_field_mapping(
    placeholders: set[str],
    data_columns: list[str],
    explicit_mapping: dict[str, str] | None = None
) -> dict[str, str]:
    """
    Map placeholders to data columns.
    Uses explicit_mapping first, then fuzzy-matches unmatched placeholders.
    Returns {placeholder: column_name}.
    """
    mapping = dict(explicit_mapping or {})
    unmatched = placeholders - set(mapping.keys())

    # Attempt auto-mapping by normalized name
    col_lookup = {c.lower().replace(" ", "_"): c for c in data_columns}
    for ph in list(unmatched):
        normalized = ph.lower()
        if normalized in col_lookup:
            mapping[ph] = col_lookup[normalized]
            unmatched.discard(ph)

    if unmatched:
        print(f"⚠️ Unmapped placeholders: {unmatched}")
        print("  Provide explicit mapping or add matching columns to data.")

    return mapping
```

### Human Review Point
Show the mapping to the user before proceeding:
```
┌─────────────────────────────────────────┐
│        FIELD MAPPING REVIEW              │
├────────────────────┬────────────────────┤
│ Placeholder          │ Data Column          │
├────────────────────┼────────────────────┤
│ EMPLOYEE_NAME        │ Full Name            │
│ TITLE                │ Job Title            │
│ LEVEL                │ Career Band          │
│ TENURE               │ Hire Date (calc)     │
│ STRENGTHS            │ ⚠️ UNMAPPED           │
└────────────────────┴────────────────────┘
Confirm mapping? [y/n]
```

---

## Phase 3: Validation

**Goal:** Check every record against the mapping before generating documents.

```python
from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    record_id: str
    status: str  # "pass", "warn", "fail"
    issues: list[str] = field(default_factory=list)

def validate_record(
    record: dict,
    mapping: dict[str, str],
    rules: dict | None = None
) -> ValidationResult:
    """Validate a single record against the field mapping."""
    result = ValidationResult(record_id=str(record.get("id", "unknown")), status="pass")

    # Check for missing required fields
    for placeholder, column in mapping.items():
        value = record.get(column)
        if value is None or (isinstance(value, str) and not value.strip()):
            result.issues.append(f"Missing: {placeholder} (col: {column})")
            result.status = "warn"

    # Apply custom rules
    if rules:
        for field_name, rule in rules.items():
            value = record.get(mapping.get(field_name, ""))
            if rule.get("type") == "date" and value:
                try:
                    pd.to_datetime(value)
                except Exception:
                    result.issues.append(f"Bad date: {field_name}={value}")
                    result.status = "fail"
            if rule.get("max_length") and value and len(str(value)) > rule["max_length"]:
                result.issues.append(f"Too long: {field_name} ({len(str(value))} chars)")

    return result
```

### Validation Report
Generate `{{BATCH_NAME}}_validation.csv`:
```
record_id,status,issues
E12345,pass,
E12346,warn,"Missing: STRENGTHS"
E12347,fail,"Bad date: HIRE_DATE=not-a-date"
```

**Decision point:** Only records with `status != "fail"` proceed to generation.

---

## Phase 4: Batch Generation

**Goal:** Populate the template once per valid record.

### PPTX Generation
```python
from pptx import Presentation
from copy import deepcopy
import re

def populate_pptx(
    template_path: str,
    records: list[dict],
    mapping: dict[str, str],
    one_file_per_record: bool = False,
    output_dir: str = "./output",
    batch_name: str = "card"
) -> list[str]:
    """Generate populated PPTX files from template + records."""
    output_files = []
    pattern = re.compile(r"\{\{(\w+)\}\}")

    if one_file_per_record:
        for record in records:
            prs = Presentation(template_path)
            _replace_in_presentation(prs, record, mapping, pattern)
            rid = record.get(mapping.get("ID", ""), "unknown")
            out_path = f"{output_dir}/{batch_name}_{rid}.pptx"
            prs.save(out_path)
            output_files.append(out_path)
    else:
        # All records in one file (one slide set per record)
        prs = Presentation(template_path)
        template_slides = list(prs.slides)
        # Clone template slide layout for each subsequent record
        for i, record in enumerate(records):
            if i > 0:
                _duplicate_slide(prs, 0)  # duplicate first slide
            _replace_in_slide(prs.slides[i], record, mapping, pattern)
        out_path = f"{output_dir}/{batch_name}_all.pptx"
        prs.save(out_path)
        output_files.append(out_path)

    return output_files

def _replace_in_presentation(prs, record, mapping, pattern):
    for slide in prs.slides:
        _replace_in_slide(slide, record, mapping, pattern)

def _replace_in_slide(slide, record, mapping, pattern):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    for match in pattern.finditer(run.text):
                        placeholder = match.group(1)
                        col = mapping.get(placeholder, "")
                        value = str(record.get(col, ""))
                        run.text = run.text.replace(f"{{{{{placeholder}}}}}", value)
```

---

## Phase 5: Audit & Output

**Goal:** Produce the final output bundle with full audit trail.

### Output Structure
```
{{OUTPUT_DIR}}/
  {{BATCH_NAME}}_all.pptx          # (or individual files)
  {{BATCH_NAME}}_validation.csv    # Validation results
  {{BATCH_NAME}}_audit.json        # Generation metadata
  {{BATCH_NAME}}_warnings.csv      # Records with warnings
```

### Audit JSON
```json
{
  "template": "talent_card_template.pptx",
  "data_source": "talent_data_q1.xlsx",
  "total_records": 145,
  "generated": 140,
  "skipped_fail": 3,
  "skipped_warn": 2,
  "timestamp": "2026-03-20T15:20:00Z",
  "field_mapping": {"EMPLOYEE_NAME": "Full Name", "...": "..."}
}
```

---

## 🛡️ Bulletproofing Checklist

- [ ] Always backup the template before running (never modify the original)
- [ ] Validate the field mapping with a human before batch generation
- [ ] Run on 3 records first, visually inspect, then run full batch
- [ ] Check for PII in output filenames (don't use SSN as filename!)
- [ ] Handle PPTX run-splitting (Word/PPT splits `{{PLACEHOLDER}}` across runs)
- [ ] Log every generated file path for traceability
- [ ] Never commit generated documents with PII to git

---

## 📚 Example Applications

| Context | Template | Data Source | Output |
|---------|----------|-------------|--------|
| Talent Cards | PPTX with photo+stats | Workday export | One PPTX per person |
| Offer Letters | DOCX with salary/title | HRIS + comp data | One DOCX per candidate |
| Performance Reviews | PPTX 3-slide template | Perf review export | All-in-one deck |
| Onboarding Packets | HTML Jinja2 template | New hire CSV | One PDF per hire |
| Sales Proposals | PPTX branded template | CRM export | One PPTX per deal |
| Compliance Certs | DOCX certificate | Training completion | One PDF per associate |

---

## ⚠️ Anti-Patterns

```
❌ Skipping the validation step (you WILL generate garbage)
❌ Hardcoding column names in the generator (use the mapping dict)
❌ Generating all 500 documents before checking one visually
❌ Using employee SSN/PII in filenames
❌ Modifying the original template file (always work on a copy)
❌ Ignoring the run-splitting problem in PPTX ({{NAME}} becomes {{N + AME}})
❌ Not handling missing photo/image placeholders gracefully
```

---

## 🔧 PPTX Run-Splitting Fix

PowerPoint often splits `{{PLACEHOLDER}}` across multiple XML runs.
This is the #1 source of bugs. Always consolidate runs before replacing:

```python
def consolidate_runs(paragraph):
    """Merge all runs into the first run, preserving first run's formatting."""
    if len(paragraph.runs) <= 1:
        return
    full_text = "".join(run.text for run in paragraph.runs)
    # Keep first run's formatting, clear the rest
    paragraph.runs[0].text = full_text
    for run in paragraph.runs[1:]:
        run.text = ""
```

---

## 🌐 Platform Notes

| Platform | Compatible | Notes |
|----------|-----------|-------|
| code-puppy | ✅ | Activate with `/skill talent-card-generator` |
| wibey | ✅ | Copy SKILL.md to `~/.wibey/skills/talent-card-generator/` |
| Codex | ✅ | Paste as system prompt prefix |
| Any LLM | ✅ | Plain Markdown — paste as context |

---

## 🔁 Deployment Ladder

| Stage | Team | What to validate |
|-------|------|-------------------|
| **Refine** | Skill Owner | Template parsing, field mapping UX, run-splitting fix |
| **Prove** | Peer Teams | Multiple template types, validation rule coverage |
| **Scale** | Walmart Home Office | Self-serve template upload, 500+ record batches, multi-format |
