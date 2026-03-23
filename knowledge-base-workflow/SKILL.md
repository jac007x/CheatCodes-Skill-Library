---
name: knowledge-base-workflow
description: "Universal knowledge base search and retrieval skill. Search, retrieve, summarize, and surface relevant content from any wiki, intranet, or documentation platform. Works with Confluence, SharePoint, Notion, or any searchable knowledge store."
version: 1.0.0
author: jac007x
tags:
  - knowledge-management
  - search
  - confluence
  - sharepoint
  - documentation
  - cross-platform
---

# 📚 Knowledge Base Workflow

Search → retrieve → summarize → surface. A universal pattern for getting
the right information out of any knowledge platform and putting it in front
of the right person in a usable form.

---

## 🧠 Core Philosophy

- **Search before creating** — the answer probably already exists somewhere
- **Summarize, don’t dump** — return the relevant excerpt, not the whole page
- **Cite your sources** — always return the page title and URL alongside the answer
- **Escalate when not found** — if search returns nothing, say so and suggest next steps
- **Structure the output** — bullet points and headers beat walls of text

---

## 🚀 Intake

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{PLATFORM}}` | Knowledge platform: `confluence`, `sharepoint`, `notion`, `other` | ✅ | — |
| `{{SEARCH_QUERY}}` | Natural language question or keyword search | ✅ | — |
| `{{SPACE_OR_SITE}}` | Limit search to a specific space, site, or section | ❌ | all |
| `{{MAX_RESULTS}}` | Max pages to retrieve and consider | ❌ | `5` |
| `{{OUTPUT_FORMAT}}` | `summary`, `bullet-points`, `full-text`, `tldr` | ❌ | `summary` |
| `{{AUDIENCE}}` | Who will read this: `self`, `team`, `executive`, `new-hire` | ❌ | `self` |
| `{{INCLUDE_LINKS}}` | Return source page URLs | ❌ | `true` |

---

## 🔄 Workflow Phases

### Phase 1: Search
```
1. Translate {{SEARCH_QUERY}} into platform search terms
2. Search {{PLATFORM}} (use sub-agent if available)
3. Retrieve top {{MAX_RESULTS}} results
4. Score results by relevance to original query
5. If 0 results: surface related terms, suggest alternate query
```

### Phase 2: Retrieve & Read
```
1. For each relevant result: retrieve full page content
2. Identify the most relevant sections (not the whole page)
3. Flag if content is outdated (check last-modified date)
4. Flag conflicting information across pages
```

### Phase 3: Synthesize & Format
```python
def format_knowledge_response(
    results: list[dict],
    query: str,
    output_format: str,
    audience: str
) -> str:
    """
    Synthesize search results into a structured response.
    Always cite sources. Never fabricate information.
    """
    if not results:
        return (
            f"No results found for: '{query}'.\n\n"
            "Suggested next steps:\n"
            "- Try broader search terms\n"
            "- Check if this is documented elsewhere\n"
            "- This may need to be created"
        )

    if output_format == "tldr":
        # One sentence per result, with link
        lines = [f"- {r['title']}: {r['summary']} — [link]({r['url']})" for r in results]
        return "\n".join(lines)

    if output_format == "summary":
        intro = f"Found {len(results)} relevant pages for: '{query}'\n\n"
        sections = []
        for r in results:
            sections.append(f"### {r['title']}\n{r['excerpt']}\n[View page]({r['url']})")
        return intro + "\n\n".join(sections)

    return "\n\n".join(r['full_text'] for r in results)
```

### Phase 4: Escalate if Not Found
```
If no relevant results:
  1. Acknowledge the gap clearly
  2. Suggest: (a) alternate search terms, (b) who might know, (c) whether to create the page
  3. If {{CREATE_IF_MISSING}} is true: draft the missing page and prompt user to publish
```

---

## 🌐 Platform Routing

| Platform | Agent / Tool | Notes |
|----------|-------------|-------|
| Confluence | `confluence-search` sub-agent | Best for Walmart internal wikis |
| SharePoint | `msgraph` sub-agent (SharePoint search) | Works across M365 tenants |
| Notion | Notion API (if available) | Requires API key |
| Other | Generic web search or file search | Falls back to keyword matching |

---

## 📊 Use Cases

| Query Type | Space / Site | Output |
|------------|-------------|--------|
| "What is our vacation policy?" | HR policies space | `summary` with link |
| "How do I submit a budget request?" | Finance playbooks | `bullet-points` |
| "What did the team decide about X?" | Team meeting notes | `full-text` excerpt |
| "Onboarding checklist for new hires" | Onboarding space | `bullet-points` |
| "Who owns the data governance process?" | Org structure | `tldr` |

---

## ⚠️ Anti-Patterns

```
❌ Returning the full page when only a section is relevant
❌ Citing a page without checking it’s current (check last-modified)
❌ Fabricating an answer when search returns nothing (always say not found)
❌ Searching only one space when the answer might live elsewhere
❌ Ignoring conflicting information across pages (flag it explicitly)
```

---

## 🔁 Deployment Ladder

| Stage | Who | What to validate |
|-------|-----|------------------|
| **Refine** | Skill Owner | Search accuracy, citation quality, not-found handling |
| **Prove** | Peer Teams | Works across different spaces and content types |
| **Scale** | Enterprise | Multi-platform search, cross-space synthesis |
