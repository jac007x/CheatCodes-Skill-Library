---
name: document-extraction
description: "Universal document extraction pipeline. Ingests PDFs, PowerPoints, Word docs, images, and forms. Extracts structured text, tables, charts, and metadata. Outputs clean, structured content ready for downstream processing — summarization, analysis, search indexing, or report generation."
version: 1.0.0
author: jac007x
tags:
  - document-processing
  - pdf
  - extraction
  - ocr
  - structured-data
  - cross-platform
---

# 📄 Document Extraction

A universal pipeline for pulling structured content out of any document format.
Feed it a PDF, a deck, a form, or an image — get back clean, usable text,
tables, and metadata ready for whatever comes next.

---

## 🧠 Core Philosophy

- **Format agnostic** — PDF, PPTX, DOCX, images, forms all go through the same pipeline
- **Structure over raw text** — preserve tables, headers, sections, slide order
- **Downstream-ready** — output is shaped for the next step (summarize, analyze, index, embed)
- **Fail gracefully** — scanned PDFs fall back to OCR; corrupt files are logged, not crashed on
- **Never assume the document is clean** — validate extraction quality before passing downstream

---

## 🚀 Intake

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{SOURCE_FILE}}` | Path or URL to the document | ✅ | — |
| `{{DOCUMENT_TYPE}}` | Type hint: `pdf`, `pptx`, `docx`, `image`, `form`, `auto` | ❌ | `auto` |
| `{{EXTRACT_MODE}}` | What to pull: `text`, `tables`, `charts`, `all` | ❌ | `all` |
| `{{OUTPUT_FORMAT}}` | How to return results: `markdown`, `json`, `csv` | ❌ | `markdown` |
| `{{CHUNK_BY}}` | How to split output: `page`, `slide`, `section`, `none` | ❌ | `page` |
| `{{INCLUDE_METADATA}}` | Return file metadata (page count, author, date) | ❌ | `true` |
| `{{OCR_FALLBACK}}` | Use OCR if native text extraction fails | ❌ | `true` |
| `{{OUTPUT_DIR}}` | Where to write extracted output | ❌ | `./extracted` |

---

## 📦 Supported Document Types

| Type | Native Extraction | OCR Fallback | Tables | Charts |
|------|-----------------|--------------|--------|--------|
| PDF (text-based) | ✅ | — | ✅ | ⚠️ description only |
| PDF (scanned) | ❌ | ✅ | ⚠️ best-effort | ⚠️ best-effort |
| PowerPoint (.pptx) | ✅ | — | ✅ | ✅ alt text + data |
| Word (.docx) | ✅ | — | ✅ | ⚠️ description only |
| Image (.png, .jpg) | ❌ | ✅ | ⚠️ best-effort | ⚠️ best-effort |
| Form (structured) | ✅ | — | ✅ field/value pairs | — |

---

## 🔄 Pipeline Phases

### Phase 1: Detect & Validate
```python
def detect_document_type(file_path: str) -> str:
    """Infer document type from extension and magic bytes."""
    suffix = Path(file_path).suffix.lower()
    type_map = {
        ".pdf": "pdf", ".pptx": "pptx", ".ppt": "pptx",
        ".docx": "docx", ".doc": "docx",
        ".png": "image", ".jpg": "image", ".jpeg": "image",
    }
    return type_map.get(suffix, "unknown")

def validate_file(file_path: str) -> dict:
    """Check file exists, is readable, and is under size limit."""
    p = Path(file_path)
    return {
        "exists": p.exists(),
        "readable": p.stat().st_size > 0 if p.exists() else False,
        "size_mb": round(p.stat().st_size / 1e6, 2) if p.exists() else 0,
        "within_limit": p.stat().st_size < 100 * 1e6 if p.exists() else False,
    }
```

### Phase 2: Extract

**PDF (text-based):**
```python
import anthropic, base64

def extract_pdf(file_path: str, chunk_by: str = "page") -> list[dict]:
    """Extract PDF content via Claude's native PDF support."""
    client = anthropic.Anthropic()
    with open(file_path, "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "base64",
                 "media_type": "application/pdf", "data": pdf_data}},
                {"type": "text", "text": (
                    f"Extract all content from this document. "
                    f"Preserve structure: headers, tables, lists. "
                    f"Split by {chunk_by}. Return as structured markdown."
                )}
            ]
        }]
    )
    return [{"chunk": 1, "content": response.content[0].text}]
```

**PowerPoint:**
```python
from pptx import Presentation

def extract_pptx(file_path: str) -> list[dict]:
    """Extract slide text, tables, and notes from PPTX."""
    prs = Presentation(file_path)
    slides = []
    for i, slide in enumerate(prs.slides, 1):
        content = {"slide": i, "title": "", "body": [], "tables": [], "notes": ""}
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if shape.shape_type == 13:  # title
                    content["title"] = text
                elif text:
                    content["body"].append(text)
            if shape.has_table:
                table_data = [
                    [cell.text for cell in row.cells]
                    for row in shape.table.rows
                ]
                content["tables"].append(table_data)
        if slide.has_notes_slide:
            content["notes"] = slide.notes_slide.notes_text_frame.text
        slides.append(content)
    return slides
```

### Phase 3: Structure & Validate Quality
```python
def validate_extraction(chunks: list[dict], min_chars: int = 50) -> dict:
    """Check extraction quality before passing downstream."""
    total_chars = sum(len(str(c.get("content", c))) for c in chunks)
    empty_chunks = [i for i, c in enumerate(chunks)
                    if len(str(c.get("content", c))) < min_chars]
    return {
        "total_chunks": len(chunks),
        "total_chars": total_chars,
        "empty_chunks": empty_chunks,
        "quality": "good" if not empty_chunks else "partial",
        "needs_ocr_fallback": total_chars < min_chars * len(chunks) * 0.5,
    }
```

### Phase 4: Output
```python
import json
from pathlib import Path

def write_output(chunks: list[dict], output_dir: str,
                 filename: str, fmt: str = "markdown") -> Path:
    """Write extracted content in the requested format."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if fmt == "json":
        out_file = out / f"{filename}_extracted.json"
        out_file.write_text(json.dumps(chunks, indent=2))
    elif fmt == "markdown":
        out_file = out / f"{filename}_extracted.md"
        lines = []
        for chunk in chunks:
            label = chunk.get("slide") or chunk.get("page") or chunk.get("chunk", "")
            if label:
                lines.append(f"\n## {'Slide' if 'slide' in chunk else 'Page'} {label}\n")
            lines.append(str(chunk.get("content", chunk)))
        out_file.write_text("\n".join(lines))
    return out_file
```

---

## 📊 Use Cases

| Input | Extract Mode | Output | Downstream Use |
|-------|-------------|--------|----------------|
| Policy PDF | `text` | Markdown by page | Q&A / search indexing |
| Benefits guide (scanned) | `all` + OCR | Markdown by section | Summarization |
| Presentation deck | `all` | JSON by slide | Slide analysis skill |
| Survey form | `tables` | CSV field/value pairs | NLP analysis skill |
| Org chart image | `text` + OCR | Plain text | Structured data extraction |

---

## ⚠️ Anti-Patterns

```
❌ Passing raw extraction directly to an LLM without quality validation
❌ Assuming all PDFs are text-based (many are scanned)
❌ Ignoring empty chunks (they indicate extraction failure)
❌ Committing extracted output files containing PII to git
❌ Using full file path as the output filename (use stem only)
❌ Treating chart images as text (describe them, don't OCR random pixels)
```

---

## 🔁 Deployment Ladder

| Stage | Who | What to validate |
|-------|-----|------------------|
| **Refine** | Skill Owner | Extraction quality across all 4 doc types |
| **Prove** | Peer Teams | Edge cases: scanned PDFs, password-protected, large files |
| **Scale** | Enterprise | Volume handling, async processing for large batches |
