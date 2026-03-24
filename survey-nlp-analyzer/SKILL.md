---
name: survey-nlp-analyzer
description: "Universalized NLP pipeline for analyzing any large body of open-ended human text. Handles anonymous feedback, open-door cases, idea submissions, survey verbatims, customer forms, office hour transcripts, support tickets, and more. Runs topic modeling (NMF), sentiment analysis, fallback clustering, quote extraction, dimensional breakdowns, sensitivity guardrails, and action implications."
version: 1.2.0
author: jac007x
tags:
  - nlp
  - topic-modeling
  - sentiment-analysis
  - text-mining
  - clustering
  - open-text
  - feedback-analysis
  - cross-platform
  - human-in-the-loop
---

# 🔬 Open-Text Insights Pipeline

A production-grade, universalized NLP pipeline for turning any large body of
open-ended human text into structured insights — topic clusters, sentiment
breakdowns, representative quotes, dimensional heatmaps, and executive summaries.

Works on anything people write: survey verbatims, anonymous pulse responses,
open-door case notes, idea submissions, customer feedback forms, meeting
transcripts, office hour recordings-to-text, support tickets, exit interviews,
and beyond. If humans wrote it and there's enough of it, this pipeline can
find the signal in the noise.

---

## 🧠 Core Philosophy

- **Topic-first, sentiment-second** — cluster by meaning, then overlay sentiment
- **Source agnostic** — the pipeline doesn't care if it's a survey, a transcript, or a Slack export; text is text
- **Anonymization-aware** — many sources are partially or fully anonymous; the pipeline never assumes attribution
- **Fallback clusters are features, not failures** — comments that don't fit a topic reveal blind spots
- **Dimensional cuts drive action** — raw topics are academic; topics × context dimension = actionable
- **Quote curation > quote quantity** — 3 perfect quotes beat 50 mediocre ones
- **Reproducibility** — same input + same config = same output, always

---

## 🚀 Intake: Customize This Skill

Before executing, the agent collects the following. Required fields must be
provided. Optional fields have defaults that work for most use cases.

### Required

| Variable | Description | Type | Notes |
|----------|-------------|------|-------|
| `{{CORPUS_FILE}}` | Path to the file (CSV, Excel, JSON, TXT) containing your text data | file-path | See Source Guide below |
| `{{TEXT_COLUMN}}` | Name of the column containing the text to analyze | string | Agent will auto-detect if unclear |
| `{{SOURCE_TYPE}}` | What kind of text this is | choice | Sets framing for reports & quote curation |
| `{{CONTEXT_DIMENSIONS}}` | Columns to cut results by (e.g., department, region, role, date) | list | What you want to compare across |

### Optional (with sensible defaults)

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `{{ID_COLUMN}}` | Unique row identifier | string | Auto-detected or row index |
| `{{ANONYMIZATION_LEVEL}}` | How attributed is the source? | choice | `"anonymous"` |
| `{{TOPIC_DICTIONARY}}` | Path to existing topic JSON, or `"auto"` | file-path | `"auto"` |
| `{{NUM_TOPICS}}` | NMF topic count when auto-discovering | int | `20` |
| `{{MIN_TEXT_LENGTH}}` | Minimum character count to include | int | `15` |
| `{{LANGUAGE_FILTER}}` | Languages to include | choice | `"all"` |
| `{{SAMPLE_SIZE}}` | Rows to process (null = all) | int | `null` |
| `{{OUTPUT_FORMAT}}` | Report format(s) | multi | `"html"` |
| `{{OUTPUT_DIR}}` | Where to write outputs | path | `"./outputs"` |
| `{{PROJECT_NAME}}` | Prefix for all output files | string | `"analysis"` |

---

## 📂 Corpus Source Guide

This pipeline is source-agnostic. The intake question `{{SOURCE_TYPE}}` sets
how the pipeline frames its outputs (report language, quote curation criteria,
sentiment calibration). Choose the closest match:

| Source Type | Examples | Notes |
|-------------|---------|-------|
| `anonymous-survey` | Pulse survey verbatims, engagement survey comments | Fully anonymous; no attribution; high volume |
| `open-door-cases` | Ethics line submissions, HR case notes, escalations | May be partially attributed; handle with care |
| `idea-submissions` | Innovation portals, suggestion boxes, idea challenges | Action-oriented; positive framing common |
| `customer-feedback` | CSAT verbatims, product reviews, complaint forms | External voice; brand-sensitive |
| `support-tickets` | ServiceNow, Zendesk, email queues | Structured + unstructured mix; has metadata |
| `meeting-transcripts` | Office hours, town halls, Q&A sessions | Speaker turns; may need speaker-splitting first |
| `forms-and-submissions` | Application forms, intake forms, registration fields | Short-form; often semi-structured |
| `exit-interviews` | Departure surveys, off-boarding forms | Small N; high signal; treat with care |
| `social-listening` | Internal Slack/Teams threads, Viva Engage posts | Informal tone; emoji; sarcasm risk |
| `other` | Anything else with open-ended text | Auto-calibrate; review QA sample carefully |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  SURVEY NLP ANALYZER                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                │
│  │  INGEST   │──▶│  CLEAN   │──▶│  MODEL   │                │
│  │  & LOAD   │   │& NORMALIZE│   │  TOPICS  │                │
│  └──────────┘   └──────────┘   └────┬─────┘                │
│                                      │                       │
│                          ┌───────────┼───────────┐          │
│                          ▼           ▼           ▼          │
│                    ┌──────────┐ ┌──────────┐ ┌────────┐    │
│                    │ SENTIMENT│ │  QUOTES  │ │FALLBACK│    │
│                    │ OVERLAY  │ │ EXTRACT  │ │CLUSTERS│    │
│                    └────┬─────┘ └────┬─────┘ └───┬────┘    │
│                         └────────────┼───────────┘          │
│                                      ▼                       │
│                               ┌──────────┐                  │
│                               │DIMENSION │                  │
│                               │  CUTS    │                  │
│                               └────┬─────┘                  │
│                                    ▼                         │
│                          ┌─────────────────┐                │
│                          │ REPORT & SHARE  │                │
│                          └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Data Ingestion & Validation

**Goal:** Load the corpus, validate schema, and produce a clean starting DataFrame.

### Implementation Notes

```python
# Use pathlib, not os.path. Use polars or pandas with explicit dtypes.
# Always try multiple encodings: utf-8 → latin-1 → cp1252
# Log row counts at every stage for auditability.

from pathlib import Path
import pandas as pd

def load_corpus(path: Path, text_col: str, id_col: str) -> pd.DataFrame:
    """Load CSV/Excel with encoding fallback. Validate required columns exist."""
    encodings = ["utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc, dtype=str)
            break
        except (UnicodeDecodeError, Exception):
            continue
    else:
        raise ValueError(f"Could not read {path} with any encoding")

    missing = {text_col, id_col} - set(df.columns)
    if missing:
        raise KeyError(f"Missing columns: {missing}. Available: {list(df.columns)[:20]}")

    n_raw = len(df)
    df = df.dropna(subset=[text_col])
    df = df[df[text_col].str.strip().str.len() > 0]
    print(f"Loaded {n_raw:,} rows → {len(df):,} with non-empty text")
    return df
```

### Validation Checklist
- [ ] Required columns (`{{TEXT_COLUMN}}`, `{{ID_COLUMN}}`) exist
- [ ] At least 100 non-empty text rows (warn if fewer)
- [ ] Context dimension columns (`{{CONTEXT_DIMENSIONS}}`) exist if specified
- [ ] No duplicate IDs (warn, don't fail)
- [ ] Log: row count, column count, null rate per column

---

## Phase 2: Text Cleaning & Normalization

**Goal:** Normalize text without destroying meaning.

### Cleaning Pipeline (order matters)

```python
import re
import unicodedata

def clean_text(text: str) -> str:
    """Normalize a single text string. Idempotent."""
    if not isinstance(text, str) or not text.strip():
        return ""
    # 1. Unicode normalize (NFKD → recompose)
    text = unicodedata.normalize("NFKC", text)
    # 2. Fix mojibake (common in Excel exports)
    replacements = {"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
                    "\u2013": "-", "\u2014": "—", "\u2026": "...", "\xa0": " "}
    for old, new in replacements.items():
        text = text.replace(old, new)
    # 3. Strip control characters (keep newlines)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", " ", text)
    # 4. Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text
```

### What NOT to do
```
❌ Don't lowercase at this stage (preserve case for quote extraction)
❌ Don't remove stopwords yet (TF-IDF handles this implicitly)
❌ Don't stem/lemmatize the raw text (do it in a derived column)
❌ Don't strip non-English text unless explicitly requested
❌ Don't dedupe by text content (similar comments from different people matter)
```

### Derived Columns to Add

```python
df["clean_text"] = df[text_col].apply(clean_text)
df["text_lower"] = df["clean_text"].str.lower()
df["char_len"] = df["clean_text"].str.len()
df["word_count"] = df["clean_text"].str.split().str.len()
```

Filter: drop rows where `char_len < {{MIN_TEXT_LENGTH}}`.

---

## Phase 3: Topic Modeling (NMF)

**Goal:** Discover or assign topics to every comment.

### Two Modes

**Mode A: Dictionary-driven** (when `{{TOPIC_DICTIONARY}}` is provided)
- Load the JSON topic dictionary (format: `{topic_name: {tier1: [...], tier2: [...]}}`)
- Score each comment against each topic using keyword matching
- Assign the highest-scoring topic; ties go to the topic with more Tier 1 hits
- Comments matching no topic go to fallback clustering (Phase 5)

**Mode B: Auto-discovery** (when `{{TOPIC_DICTIONARY}}` is `"auto"`)
- Run TF-IDF → NMF with `{{NUM_TOPICS}}` components
- Extract top 15 words per topic as the topic fingerprint
- Name topics by their top 3 most distinctive words
- **Human review required before proceeding** — agent shows QA sample, you approve topic labels

### NMF Implementation

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def discover_topics(texts: list[str], n_topics: int = 20) -> tuple:
    """Run TF-IDF + NMF. Returns (topic_assignments, topic_words, model)."""
    tfidf = TfidfVectorizer(
        max_features=5000,
        min_df=5,
        max_df=0.85,
        ngram_range=(1, 2),
        stop_words="english",
    )
    tfidf_matrix = tfidf.fit_transform(texts)
    feature_names = tfidf.get_feature_names_out()

    nmf = NMF(n_components=n_topics, random_state=42, max_iter=400)
    doc_topics = nmf.fit_transform(tfidf_matrix)  # (n_docs, n_topics)

    # Extract top words per topic
    topic_words = {}
    for i, component in enumerate(nmf.components_):
        top_idxs = component.argsort()[-15:][::-1]
        topic_words[f"topic_{i}"] = [feature_names[j] for j in top_idxs]

    # Assign dominant topic per doc
    assignments = doc_topics.argmax(axis=1)
    strengths = doc_topics.max(axis=1)

    return assignments, strengths, topic_words, nmf, tfidf
```

### Topic Quality Check
- Flag topics where the mean strength < 0.05 (weak signal)
- Flag topics with < 10 comments assigned (likely noise)
- Generate a QA sample: 5 random comments per topic for human review

---

## Phase 4: Sentiment Analysis

**Goal:** Score every comment on sentiment. Overlay onto topic assignments.

### Method: VADER (preferred for informal/survey text)

```python
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def score_sentiment(texts: list[str]) -> list[dict]:
    """Return list of {neg, neu, pos, compound} dicts."""
    sia = SentimentIntensityAnalyzer()
    return [sia.polarity_scores(t) for t in texts]

def classify_sentiment(compound: float) -> str:
    """Classify compound score into Positive/Negative/Neutral."""
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    return "Neutral"
```

### Output Columns
```python
df["sentiment_compound"] = df["clean_text"].apply(lambda t: sia.polarity_scores(t)["compound"])
df["sentiment_label"] = df["sentiment_compound"].apply(classify_sentiment)
```

### Anti-Patterns
```
❌ Don't use TextBlob for survey data (it's trained on product reviews, not employee feedback)
❌ Don't classify "I love my job but hate my schedule" as simply Positive
    → Log mixed-sentiment comments for human review
❌ Don't average sentiment across topics (report per-topic distributions instead)
```

---

## Phase 5: Fallback Clustering

**Goal:** Handle comments that didn't match any topic strongly enough.

```python
from sklearn.cluster import MiniBatchKMeans

def cluster_fallbacks(texts: list[str], n_clusters: int = 8) -> tuple:
    """Cluster unassigned comments. Returns (labels, top_words_per_cluster)."""
    tfidf = TfidfVectorizer(max_features=2000, stop_words="english", ngram_range=(1, 2))
    matrix = tfidf.fit_transform(texts)
    features = tfidf.get_feature_names_out()

    km = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, batch_size=256)
    labels = km.fit_predict(matrix)

    top_words = {}
    for i in range(n_clusters):
        center = km.cluster_centers_[i]
        top_idxs = center.argsort()[-10:][::-1]
        top_words[i] = [features[j] for j in top_idxs]

    return labels, top_words
```

### Fallback Cluster Log
Generate `{{PROJECT_NAME}}_fallback_clusters_log.csv` with:
- Cluster ID, top words, sample comments (3-5 per cluster)
- Flag clusters that might represent missed topics (human reviews these)

---

## Phase 6: Quote Extraction & Curation

**Goal:** For each topic × sentiment, extract the most representative quotes.

### Selection Criteria (ranked)
1. **Highest topic strength** (most on-topic)
2. **Moderate length** (50-300 chars preferred — not too short, not rambling)
3. **Clear sentiment signal** (|compound| > 0.3)
4. **No PII** (no names, emails, phone numbers — regex filter)
5. **Readable** (no garbled encoding, no single-word responses)

```python
def extract_quotes(df: pd.DataFrame, topic_col: str, sentiment_col: str,
                   text_col: str, n_per_cell: int = 3) -> dict:
    """Extract top N quotes per (topic, sentiment) cell."""
    quotes = {}
    for (topic, sent), group in df.groupby([topic_col, sentiment_col]):
        candidates = group[
            (group["char_len"].between(50, 300)) &
            (group["sentiment_compound"].abs() > 0.15)
        ].nlargest(n_per_cell * 2, "topic_strength")
        quotes[(topic, sent)] = candidates[text_col].head(n_per_cell).tolist()
    return quotes
```

### Output: `{{PROJECT_NAME}}_topic_quotes.json`

---

## Phase 7: Dimensional Analysis

**Goal:** Cross-tabulate topics and sentiment by `{{CONTEXT_DIMENSIONS}}`.

### Outputs per dimension

1. **Heatmap CSV** — rows = dimension values, cols = topics, values = comment count or % negative
2. **Rollup summary** — total responses, sentiment split, top 3 topics per dimension value
3. **Cluster summary by sentiment** — per sentiment label, top words and examples
4. **Low-N suppression** — cells with fewer than 5 responses are suppressed (privacy)

```python
def build_heatmap(df: pd.DataFrame, dimension: str, topic_col: str,
                  value: str = "count", min_n: int = 5) -> pd.DataFrame:
    """Pivot table: dimension × topic. Suppresses cells below min_n."""
    if value == "count":
        result = pd.crosstab(df[dimension], df[topic_col])
    elif value == "pct_negative":
        neg = df[df["sentiment_label"] == "Negative"]
        total = pd.crosstab(df[dimension], df[topic_col])
        neg_ct = pd.crosstab(neg[dimension], neg[topic_col]).reindex_like(total).fillna(0)
        result = (neg_ct / total.replace(0, float("nan")) * 100).round(1)
    # Suppress small cells
    counts = pd.crosstab(df[dimension], df[topic_col])
    result[counts < min_n] = None
    return result
```

### Output Files
```
{{PROJECT_NAME}}_rollup_summary.csv          # per dimension value
{{PROJECT_NAME}}_subtopic_summary.csv         # per dimension × topic cell
{{PROJECT_NAME}}_cluster_Positive_summary.csv
{{PROJECT_NAME}}_cluster_Negative_summary.csv
{{PROJECT_NAME}}_cluster_Neutral_summary.csv
{{PROJECT_NAME}}_topic_metadata.csv          # topic labels + top words
{{PROJECT_NAME}}_fallback_clusters_log.csv   # unassigned comments
{{PROJECT_NAME}}_topic_quotes.json           # curated quotes per topic
{{PROJECT_NAME}}_audit.log                   # row counts at every stage
```

---

## Phase 8: Report Generation & Distribution

**Goal:** Produce a human-readable report and share it.

### Default: HTML Dashboard (Tailwind + Chart.js)
- Executive insights at top (auto-generated observations)
- Topic distribution bar chart
- Sentiment breakdown (stacked bar by topic)
- Heatmap table per context dimension
- Representative quotes section (collapsible per topic)
- Methodology note at bottom
- Framing language adapts to `{{SOURCE_TYPE}}` (e.g., "respondents" vs "customers" vs "associates")
- Brand colors: parameterized via `{{BRAND_PRIMARY}}` / `{{BRAND_ACCENT}}` (defaults: neutral gray palette)

### Alternative Outputs
- **Slide deck** — invoke `slide-deck` agent with summary data
- **Podcast script** — invoke LLM to narrate the top findings as a 5-min script
- **CSV bundle** — just the raw output files, no visualization

### Share
```
invoke_agent('share-puppy', 'Share {{OUTPUT_DIR}}/{{PROJECT_NAME}}_report.html')
open {{OUTPUT_DIR}}/{{PROJECT_NAME}}_report.html   # macOS
```

---

## 🔒 Phase 8.5: Sensitivity Guardrails (NEW in v1.2.0)

**Goal:** Before generating or distributing any output, validate that no privacy thresholds are breached.

Run this phase automatically when `{{SENSITIVITY_LEVEL}}` is `medium`, `high`, or `restricted`, or when `{{SOURCE_TYPE}}` is `anonymous-survey`, `open-door-cases`, or `exit-interviews`.

### Small Cell Check

```python
SMALL_CELL_THRESHOLD = 10  # configurable; default is 10

def flag_small_cells(df: pd.DataFrame, dimension: str, topic_col: str,
                     threshold: int = SMALL_CELL_THRESHOLD) -> list[dict]:
    """Return list of (dimension_value, topic) cells where n < threshold."""
    ct = pd.crosstab(df[dimension], df[topic_col])
    flags = []
    for dim_val, row in ct.iterrows():
        for topic, count in row.items():
            if 0 < count < threshold:
                flags.append({"dimension": dimension, "value": dim_val,
                              "topic": topic, "n": count})
    return flags
```

**Actions per flag:**
- `n < 5`: Suppress — do not include this cell in any output
- `5 ≤ n < 10`: Aggregate — merge with adjacent dimension value or report as "Other"
- Flag all suppressions in `{{PROJECT_NAME}}_audit.log`

### Quote PII Scan

Before including any quote in an output:

```python
import re

PII_PATTERNS = [
    r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",           # Proper names (heuristic)
    r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",  # Email
    r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",          # Phone
    r"\bmy (manager|boss|director|VP|lead)\b",  # Role references (identity risk)
]

def has_pii_risk(text: str) -> bool:
    """Return True if text contains patterns that may identify an individual."""
    for pattern in PII_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
```

Any quote flagged by `has_pii_risk` is excluded from output automatically. Log count of excluded quotes in audit log.

### Sensitivity Output Controls

| Sensitivity Level | Distribution Control |
|-------------------|---------------------|
| `low` | Standard sharing; no controls |
| `medium` | Confirm audience before generating HTML report; disable public share links |
| `high` | Output suppresses all small cells (n<10); disable quote section by default; require human review before sharing |
| `restricted` | No automated distribution; output to local file only; warn prominently in report header |

---

## 💡 Phase 9: Action Implications (NEW in v1.2.0)

**Goal:** Translate topic findings into specific, actionable implications — not just "here's what people said" but "here's what this means and what to do."

This phase runs after Phase 8 (Report Generation) and appends an **Action Implications** section to the executive summary.

### Implication Generation Logic

For each topic where a statistically notable finding exists (define notable as: negative sentiment > 40% OR topic volume > 15% of corpus OR significant variance across a dimension):

1. **State the pattern** — what did the data show? (fact-based, not interpretive)
2. **Name the implication** — what does this suggest about the underlying situation?
3. **Propose the action** — what specific action could address this?
4. **Flag confidence** — based on `{{CONFIDENCE_LEVEL}}` and n-size

```
Template:
**[TOPIC NAME]**
Pattern: [X]% of responses in this topic were negative, concentrated in [dimension value].
Implication: This suggests [interpretation], particularly for [affected group].
Suggested Action: [specific, owner-assignable action]
Confidence: [HIGH/MEDIUM/LOW] — based on n=[N] responses, [timeframe].
```

### Action Implication Output

Appended to the HTML report as a collapsible `Action Implications` section:

```
## Recommended Actions

| Priority | Topic | Pattern | Suggested Action | Confidence |
|----------|-------|---------|-----------------|------------|
| 1 | [Topic] | [Pattern] | [Action] | High |
...
```

**Prioritization rules:**
1. Topics with highest negative sentiment % AND highest volume → Priority 1
2. Topics where a specific dimension is a significant outlier → Priority 2
3. Topics with high volume but mixed sentiment (potential opportunity) → Priority 3
4. Topics with strong positive sentiment → Note as reinforcement actions only

### Anti-Patterns for Action Implications

```
❌ Don't prescribe actions beyond the evidence (correlation ≠ causation)
❌ Don't generate implications for low-N topics (< 30 comments)
❌ Don't imply individual accountability from group-level data
❌ Don't present implications as definitive — always caveat with confidence level
❌ Don't skip implications for positive topics — reinforce what works
```

---

## 🛡️ Bulletproofing Checklist

- [ ] Test with a 1,000-row sample before running full corpus
- [ ] Verify topic dictionary covers the domain (or use auto-discovery first)
- [ ] Review fallback clusters — they often reveal missed topics
- [ ] QA-check 5 quotes per topic for PII leakage before sharing
- [ ] Confirm context dimension columns have no excessive nulls (>30% = warn)
- [ ] If corpus > 500K rows, process in chunks of 50K to manage memory
- [ ] Always log row counts: raw → cleaned → length-filtered → topic-assigned → fallback
- [ ] Never commit the raw corpus to git (may contain PII)

---

## 🔧 Adapting This Skill

1. Answer the intake questions (agent will walk you through them)
2. `{{CORPUS_FILE}}` — point to your text file
3. `{{SOURCE_TYPE}}` — pick the closest match from the Source Guide
4. `{{TEXT_COLUMN}}` — confirm the right column (agent auto-detects)
5. `{{CONTEXT_DIMENSIONS}}` — what do you want to compare across?
6. `{{TOPIC_DICTIONARY}}` — bring your own or start with auto-discovery
7. Run Phase 1–2, review the QA sample with a human, then run Phases 3–8

---

## 📚 Example Applications

| Source Type | Text Column | Context Dimensions | Topics | N (typical) |
|-------------|------------|-------------------|--------|-------------|
| Anonymous pulse survey | Verbatim | Dept, Level, Region | auto ~15 | 500–50K |
| Open-door / ethics cases | Case Description | Category, Severity, Org | dictionary | 200–5K |
| Idea submission portal | Idea Text | Team, Quarter, Status | auto ~10 | 100–10K |
| Customer feedback forms | Comments | Product, Channel, Region | auto ~20 | 1K–500K |
| Office hour transcripts | Transcript | Session, Topic, Role | auto ~8 | 20–500 sessions |
| Support ticket queue | Description | Priority, Category, SLA | dictionary | 5K–1M |
| Exit interview responses | Open Text | Level, Dept, Tenure | auto ~12 | 50–5K |
| Social listening (internal) | Post Content | Team, Channel, Date | auto ~15 | 500–100K |

---

## 🐶 Agent / Tool Dependencies

| Agent/Tool | Purpose | Required? |
|------------|---------|----------|
| Python 3.10+ | Runtime | ✅ |
| scikit-learn | TF-IDF + NMF + KMeans | ✅ |
| nltk (VADER) | Sentiment analysis | ✅ |
| pandas | Data manipulation | ✅ |
| share-puppy | Publish HTML report | ❌ Optional |
| slide-deck | Generate slide deck from data | ❌ Optional |

---

## ⚠️ Anti-Patterns

```
❌ Running NMF on uncleaned text (garbage in → garbage out)
❌ Skipping the QA sample review (topics can be nonsensical without human check)
❌ Hardcoding column names or file paths (always parameterize)
❌ Using global variables for config (use dataclasses or a typed config dict)
❌ Processing the entire corpus without a sample dry-run first
❌ Averaging sentiment across all responses (always report per-topic distributions)
❌ Ignoring fallback clusters (they often reveal the most important emerging themes)
❌ Committing raw response data to git (may contain PII regardless of source type)
❌ Using pie charts to show topic distribution (bar charts only, please)
❌ Assuming the source is English-only (many corpora are multilingual)
❌ Referencing source-specific filenames or programs in the report output
❌ Treating low-N cells the same as high-N cells (always suppress below threshold)
```

---

## 🌐 Platform Notes

| Platform | Compatible | Notes |
|----------|-----------|-------|
| code-puppy | ✅ | Activate with `/skill survey-nlp-analyzer` |
| wibey | ✅ | Copy SKILL.md to `~/.wibey/skills/survey-nlp-analyzer/` |
| Codex | ✅ | Paste SKILL.md as system prompt prefix |
| Google Colab | ✅ | Install deps with `pip install scikit-learn nltk` |
| Any LLM | ✅ | Plain Markdown — paste as context |

---

## 🔁 Deployment Ladder

| Stage | Team | What to validate |
|-------|------|-------------------|
| **Refine** | Skill Owner | Pipeline correctness, output quality, quote curation |
| **Prove** | Peer Teams | Cross-org cuts work, topic dictionary generalizes |
| **Scale** | Walmart Home Office | Handles 500K+ rows, all BU dimensions, self-serve |
