# Document Processing Skill

📚 **Source**: Curated from Anthropic Cookbook + LangChain Unstructured
**Category**: Data Extraction, Document Processing

Process PDFs, PowerPoints, Forms, and other document types for AI workflows.

---

## Overview

This skill provides patterns for extracting and processing content from various document formats:
- **PDF** - Text extraction, summarization, form parsing
- **PowerPoint** - Slide content, charts, speaker notes
- **Forms** - Structured data extraction
- **Images** - Charts, diagrams, visual content

## Use Cases for People Function

| Document Type | People Function Use |
|---------------|---------------------|
| PDF | Policy documents, benefits guides, compliance docs |
| PowerPoint | MBR presentations, town hall decks, training materials |
| Forms | Surveys, intake forms, feedback forms |
| Images | Org charts, process diagrams, dashboards |

---

## PDF Processing

### Basic PDF Text Extraction

Claude can process PDFs natively. Upload via API:

```python
import anthropic
import base64

client = anthropic.Anthropic()

# Read PDF file
with open("document.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Summarize this document's key points."
                }
            ],
        }
    ],
)
```

### PDF Summarization Patterns

**Executive Summary**:
```
Provide a 3-paragraph executive summary of this document:
1. Main purpose and context
2. Key findings or recommendations
3. Action items or next steps
```

**Policy Extraction**:
```
Extract from this policy document:
1. Policy name and effective date
2. Who it applies to
3. Key requirements (bulleted)
4. Exceptions or exclusions
5. Contact for questions
```

**Benefits Guide Parsing**:
```
From this benefits document, extract:
- Plan options available
- Enrollment deadlines
- Cost comparisons (employee vs employer contribution)
- Key coverage details
```

---

## PowerPoint Processing

### Reading Slide Content

Claude can process PPTX files with vision:

```python
import anthropic
import base64

client = anthropic.Anthropic()

# For each slide exported as image
with open("slide_1.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Extract all text and data from this slide. Describe any charts or visuals."
                }
            ],
        }
    ],
)
```

### PowerPoint Analysis Patterns

**MBR Deck Analysis**:
```
Analyze this MBR presentation slide:
1. What metric is being shown?
2. What is the current value vs target?
3. What trend is indicated (improving/declining/stable)?
4. Any callouts or highlights?
```

**Training Material Extraction**:
```
From this training slide, extract:
- Learning objective
- Key concepts
- Action items or exercises
- Questions for discussion
```

**Chart/Graph Interpretation**:
```
Analyze this chart:
1. Chart type (bar, line, pie, etc.)
2. What data is being compared?
3. Key insights (highest, lowest, trends)
4. Any anomalies or notable patterns
```

---

## Form Data Extraction

### Structured Form Processing

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": form_image_data,
                    },
                },
                {
                    "type": "text",
                    "text": """Extract all form fields and values as JSON:
{
  "field_name": "value",
  ...
}
Include checkbox states as true/false."""
                }
            ],
        }
    ],
)
```

### Form Extraction Patterns

**Employee Intake Form**:
```
Extract from this intake form:
{
  "employee_name": "",
  "employee_id": "",
  "department": "",
  "start_date": "",
  "manager_name": "",
  "work_location": "",
  "equipment_needed": []
}
```

**Survey Response**:
```
Extract survey responses:
{
  "respondent_id": "",
  "date": "",
  "responses": [
    {"question": "", "answer": "", "scale": null}
  ],
  "comments": ""
}
```

**Feedback Form**:
```
Extract feedback:
{
  "feedback_type": "praise|concern|suggestion",
  "subject": "",
  "details": "",
  "submitted_by": "",
  "date": "",
  "priority": "low|medium|high"
}
```

---

## Unstructured Parser (Advanced)

For complex document processing at scale, use the `unstructured` library:

```python
from unstructured.partition.auto import partition

# Auto-detect and parse any document type
elements = partition(filename="document.pdf")

# Elements include:
# - Title, NarrativeText, ListItem
# - Table, Image, Header, Footer

for element in elements:
    print(f"{element.category}: {element.text[:100]}")
```

### Supported Formats

| Format | Extensions | Notes |
|--------|------------|-------|
| PDF | .pdf | Text and scanned (OCR) |
| Word | .docx, .doc | Full formatting preserved |
| PowerPoint | .pptx, .ppt | Slides as elements |
| Excel | .xlsx, .xls | Tables extracted |
| Email | .eml, .msg | Headers + body |
| HTML | .html | Cleaned text |
| Images | .png, .jpg | OCR extraction |
| Markdown | .md | Structured parsing |

### Installation

```bash
pip install unstructured[all-docs]

# For OCR support
pip install unstructured[ocr]
```

---

## People Function Workflows

### 1. Policy Document Processor

```python
def process_policy(pdf_path: str) -> dict:
    """Extract structured data from HR policy PDF."""

    # Use Claude for intelligent extraction
    prompt = """
    Extract from this HR policy document:
    {
      "policy_name": "",
      "policy_number": "",
      "effective_date": "",
      "applies_to": [],
      "summary": "",
      "key_requirements": [],
      "exceptions": [],
      "related_policies": [],
      "contact": ""
    }
    """
    # ... Claude API call
```

### 2. MBR Deck Analyzer

```python
def analyze_mbr_deck(pptx_path: str) -> dict:
    """Analyze MBR PowerPoint for metrics and insights."""

    # Export slides to images, then process each
    for slide in slides:
        prompt = """
        Analyze this MBR slide:
        - Metric name
        - Current value
        - Target/threshold
        - Status (green/yellow/red)
        - Trend
        - Key callout
        """
        # ... process
```

### 3. Survey Response Aggregator

```python
def aggregate_surveys(form_images: list) -> dict:
    """Process multiple survey forms and aggregate responses."""

    responses = []
    for form in form_images:
        # Extract individual response
        response = extract_form_data(form)
        responses.append(response)

    # Aggregate
    return {
        "total_responses": len(responses),
        "average_scores": calculate_averages(responses),
        "common_themes": extract_themes(responses),
        "action_items": identify_actions(responses)
    }
```

---

## Integration with MBR Engine

| MBR Phase | Document Processing Use |
|-----------|------------------------|
| Data Collection | Parse source Excel/CSV files |
| Context Gathering | Extract policy references |
| Slide Generation | Process template decks |
| Review | Analyze existing MBR decks |

---

## Best Practices

### Do's
- ✅ Use appropriate model for task (Sonnet for most, Haiku for simple extraction)
- ✅ Provide clear output format (JSON schema)
- ✅ Handle multi-page documents in chunks
- ✅ Validate extracted data
- ✅ Cache results for repeated processing

### Don'ts
- ❌ Process sensitive docs without proper handling
- ❌ Assume 100% accuracy - always validate
- ❌ Ignore document quality issues (blurry, rotated)
- ❌ Process huge files without chunking

---

## Attribution

- **PDF/Vision Patterns**: Anthropic Cookbook
- **Unstructured Parser**: LangChain ecosystem
- **Curated By**: @jac007x
- **Curation Date**: 2026-03-18
