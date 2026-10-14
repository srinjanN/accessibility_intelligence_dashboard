# ♿ AI-Powered Accessibility Intelligence Dashboard (AID)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![WCAG 2.2](https://img.shields.io/badge/WCAG-2.2%20Level%20AAA-059669.svg?logo=w3c&logoColor=white)](https://www.w3.org/WAI/standards-guidelines/wcag/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-336791.svg?logo=postgresql&logoColor=white)](https://supabase.com)
[![AI Engine](https://img.shields.io/badge/AI%20Engine-Gemini%202.5%20%2F%20Heuristic-8E75C4.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An enterprise-grade, cognitive accessibility and readability intelligence platform built with **Python, Streamlit, spaCy, Textstat, TextBlob, Scikit-learn, NetworkX, Plotly, Supabase/PostgreSQL, and Google Gemini API**.

The platform analyzes digital product copy, legal agreements, healthcare guidelines, and web content to detect cognitive friction, readability bottlenecks, and accessibility violations—mapping findings directly to **WCAG 2.2 (Level A, AA, AAA)**, **U.S. Section 508**, and **European EN 301 549** standards.

---

## 📑 Table of Contents

- [Executive Overview](#-executive-overview)
- [Key Features](#-key-features)
- [Design System & Interface](#-design-system--interface)
- [System Architecture](#-system-architecture)
- [Multi-Page Breakdown](#-multi-page-breakdown)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
  - [Running Locally](#running-locally)
- [Database Setup & Cloud Sync](#-database-setup--cloud-sync)
- [WCAG 2.2 & Multi-Standard Compliance](#-wcag-22--multi-standard-compliance)
- [NLP & Violation Detection Pipeline](#-nlp--violation-detection-pipeline)
- [AI Simplification Engine](#-ai-simplification-engine)
- [License & Attribution](#-license--attribution)

---

## 🎯 Executive Overview

Over 1.3 billion people experience significant disabilities globally. Beyond visual and auditory impairments, **cognitive, neurological, and language accessibility** (dyslexia, ADHD, memory limitations, processing differences, non-native comprehension) represents the largest barrier to understanding modern digital services.

The **Accessibility Intelligence Dashboard** bridges the gap between raw copy and universal digital inclusion:
- **Quantifies Cognitive Burden**: Evaluates sentence architecture, jargon density, and syntactic depth.
- **Explainable AI (XAI)**: Explains the root causes of score deductions with feature-importance rationale.
- **Actionable Remediation**: Transforms vague audit outputs into structured, clear points with evidence snippets.
- **Persona-Driven Simplification**: Adapts text for 6 distinct reader cognitive profiles.
- **Formal Compliance Evidence**: Generates audit-ready reports in PDF, DOCX, CSV, and JSON.

---

## ✨ Key Features

### 📊 Real-Time KPI Telemetry
- **Cognitive Accessibility Score** (0–100 weighted cognitive health metric)
- **Flesch Reading Ease** & **Flesch-Kincaid Grade Level**
- **Estimated Reading Time** (in seconds and minutes)
- **Syntactic Complexity Index** & **Passive Voice Ratio**
- **Jargon & Complex Vocabulary Density**
- **Actionable Violations Counter** categorized by severity

### 📥 Multi-Format Ingestion
- **Direct Copy Input**: Paste raw interface copy, legal text, or articles.
- **Document Files**: Plain Text (`.txt`), Adobe PDF (`.pdf` via `pypdf`), Microsoft Word (`.docx`).
- **Data Spreadsheets**: CSV (`.csv`), Excel (`.xlsx`, `.xls` via `pandas`).
- **Web URL Scraper**: Extract and sanitize readable text directly from live web pages.

### ♿ Accessibility & Inclusion Rules Engine
Automated rule-based and linguistic detection across 10+ critical dimensions:
1. **Overly Long Sentences** (>20 words baseline, customizable)
2. **Jargon & Complex Terminology** (syllable analysis + domain dictionary)
3. **Passive Voice Construction** (syntactic agent-action identification)
4. **Cognitive Syntactic Overload** (excessive comma splices, clauses, and semi-colons)
5. **Non-Inclusive & Ableist Phrasing** (respectful and gender-neutral suggestions)
6. **All-Caps & Visual Heading Issues**
7. **Redundant & Repeated Words**
8. **Ambiguous Call-to-Action (CTA) Labels** ("Click here", "Submit", "Learn more")
9. **Dense, Unsegmented Text Blocks**
10. **Reading Grade Mismatch**

### 🧠 Explainable AI (XAI) Score Rationale
- **Feature Importance Deductions**: Bar chart visualizing exact penalty contributions (sentence length, jargon, reading grade, passive voice).
- **Executive Rationale Summary**: Contextual narrative explaining why the score was assigned.
- **Confidence Metrics**: Algorithmic certainty percentage for each identified issue.
- **Itemized Issue Points**: Structured point-by-point presentation:
  - `📌 ISSUE`: Specific violation and cognitive impact explanation
  - `🔍 EVIDENCE`: Quoted excerpt from the audited text
  - `💡 ACTION`: Concrete, copy-pasteable remediation recommendation

### 🔄 Multi-Persona AI Simplifier
Rewrites complex copy into accessible alternatives using **Google Gemini 2.5 Flash** (or a smart heuristic rule engine when offline):
- **Plain English**: Active voice, everyday vocabulary, concise statements.
- **Dyslexia-Friendly**: Shorter phrasing, bulleted structures, high contrast formatting.
- **ADHD-Friendly**: Scannable, bite-sized sections with bold anchor keywords.
- **Elderly-Friendly**: Step-by-step clarity with zero technical jargon.
- **Child-Friendly**: Accessible Grade 3–5 reading vocabulary.
- **Inclusive Language**: Gender-neutral, bias-free, respectful terminology.

### 📈 Plotly Visual Analytics Suite
- Dynamic Accessibility Speedometer Gauge
- Sentence Length Distribution Histogram
- Part-of-Speech (POS) Distribution Chart
- Hierarchical Violations Treemap by Category & Severity
- TF-IDF Keyword Prominence Chart
- Interactive Semantic Co-occurrence Network Graph (`NetworkX` + `Plotly`)

### 📜 Enterprise Multi-Format Reporting
- **Executive PDF Report** (Styled with ReportLab: KPI summary, XAI rationale, issues list)
- **Editable Word Report** (`.docx` formatting with structured heading hierarchy)
- **Violation Matrix Spreadsheet** (`.csv` export for Jira/Asana import)
- **Developer Schema** (`.json` payload for CI/CD integration)

---

## 🎨 Design System & Interface

The dashboard follows modern enterprise design principles (inspired by Linear, Stripe Dashboard, and Vercel):

- **WCAG AAA Prominent Contrast**: High-contrast ratios (>18:1 for core text, >7:1 for interactive controls).
- **Dynamic Theme Switcher**: Toggle seamlessly between **Dark Mode** (`#080C14` canvas, `#0F172A` cards) and **Light Mode** (`#F1F5F9` canvas, `#FFFFFF` cards).
- **Synchronized Plotly Visuals**: Charts adapt their background, grid lines, fonts, and color scales instantly to the selected theme.
- **Clean SVG Iconography**: Crisp Lucide-style inline SVGs with `aria-hidden="true"` accessibility tags.
- **Zero Markdown Leakage**: Content is HTML-escaped and structured cleanly without unparsed tags or markdown code blocks.

---

## 🏗️ System Architecture

```
accessibility_intelligence_dashboard/
├── app.py                      # Main landing page & application router
├── requirements.txt            # Python dependencies manifest
├── .env.example                # Environment variables template
├── README.md                   # Comprehensive platform documentation
├── run.bat                     # Windows one-click startup script
│
├── assets/
│   └── style.css               # Tokenized enterprise CSS (colors, cards, typography)
│
├── .streamlit/
│   └── config.toml             # Streamlit server and dark base theme config
│
├── database/
│   ├── db_manager.py           # Dual database layer (PostgreSQL + SQLite fallback)
│   └── history.db              # Local SQLite database file
│
├── scripts/
│   ├── schema_supabase.sql     # PostgreSQL / Supabase table definition & RLS
│   ├── migrate_to_supabase.py  # 1-Click migration script: SQLite → PostgreSQL
│   └── run_supabase_sql.py     # Automated SQL runner via PostgreSQL URI
│
├── sample_data/                # Bundled test files for evaluation
│   ├── complex_legal_terms.txt
│   ├── medical_instructions.txt
│   └── ui_button_copy.csv
│
├── utils/
│   ├── ui_components.py        # Tokenized UI cards, theme switcher, safe HTML cards
│   ├── ui_theme.py             # Plotly dark/light template synchronization engine
│   ├── accessibility_rules.py  # 10+ violation detection algorithms & XAI scoring
│   ├── wcag_mapping.py         # WCAG 2.2, Section 508, EN 301 549 audit engine
│   ├── ai_service.py           # Gemini 2.5 API & heuristic simplification engine
│   ├── nlp_engine.py           # Tokenization, POS, NER, TF-IDF, N-grams, topics
│   ├── file_parsers.py         # PDF, Word, CSV, Excel, TXT, and Web URL parsers
│   ├── report_generator.py     # Baseline PDF, DOCX, CSV, JSON report engines
│   └── compliance_report.py    # WCAG compliance multi-format report generator
│
└── pages/
    ├── 1_📊_Dashboard.py        # Core ingestion, KPI telemetry, instant audit
    ├── 2_🔍_NLP_Pipeline.py     # POS tagging, NER, TF-IDF, N-grams, topic modeling
    ├── 3_♿_Accessibility_Audit.py # Point-by-point issues matrix & XAI rationale
    ├── 4_✨_AI_Simplifier.py    # 6-persona text simplification & side-by-side diff
    ├── 5_📈_Visual_Analytics.py # Interactive Plotly charts & semantic network graph
    ├── 6_📜_Reports.py          # Downloadable executive audit reports
    ├── 7_💾_History.py          # Audit log search, re-analysis, and export
    ├── 8_⚙️_Settings.py         # Rule thresholds, DB connection, API configuration
    └── 9_WCAG_Compliance.py    # WCAG 2.2 Level A/AA/AAA audit & certification
```

---

## 📱 Multi-Page Breakdown

| # | Page | Core Purpose |
|---|---|---|
| **0** | **Landing (`app.py`)** | Welcome portal, platform overview, system status, and module directory. |
| **1** | **Dashboard (`1_📊_Dashboard.py`)** | Main input engine (text/file/URL), sample document loader, and KPI cards. |
| **2** | **NLP Pipeline (`2_🔍_NLP_Pipeline.py`)** | Linguistic inspection: tokens, POS tags, named entities, TF-IDF, N-grams, topic clusters. |
| **3** | **Accessibility Audit (`3_♿_Accessibility_Audit.py`)** | Point-by-point violations matrix, severity filters, evidence snippets, and XAI penalty breakdown. |
| **4** | **AI Simplifier (`4_✨_AI_Simplifier.py`)** | Multi-persona plain language rewrites with side-by-side diff and readability improvements. |
| **5** | **Visual Analytics (`5_📈_Visual_Analytics.py`)** | Plotly charts, speedometer gauge, sentence histogram, and co-occurrence graph. |
| **6** | **Reports (`6_📜_Reports.py`)** | Executive PDF, Word DOCX, CSV matrix, and JSON developer exports. |
| **7** | **History (`7_💾_History.py`)** | Audited records table, search by title/content, 1-click re-analysis, and deletion. |
| **8** | **Settings (`8_⚙️_Settings.py`)** | Sensitivity sliders, Gemini API key, theme dropdown, and PostgreSQL connection testing. |
| **9** | **WCAG Compliance (`9_WCAG_Compliance.py`)** | Formal WCAG 2.2 (A/AA/AAA), Section 508, EN 301 549 evaluation and certification. |

---

## 🚀 Getting Started

### Prerequisites

- **Python**: Version `3.10` or higher (`3.11` recommended)
- **Package Manager**: `pip`
- **Optional**: [Google Gemini API Key](https://aistudio.google.com/) for AI simplification (smart offline fallback included)
- **Optional**: [Supabase](https://supabase.com) account for cloud database sync (local SQLite fallback included)

---

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/accessibility-intelligence-dashboard.git
   cd accessibility-intelligence-dashboard
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the spaCy English language model (optional, fallback included):**
   ```bash
   python -m spacy download en_core_web_sm
   ```

---

### Environment Configuration

Copy `.env.example` to create your local `.env`:

```bash
cp .env.example .env
```

Edit `.env` to configure your API keys and database connections:

```env
# Google Gemini API Key (Optional: for AI Simplification)
GEMINI_API_KEY=your_gemini_api_key_here
DEFAULT_MODEL=gemini-2.5-flash

# Option 1: Supabase Direct PostgreSQL URI (Recommended for cloud sync)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# Option 2: Supabase REST API (Alternative)
SUPABASE_URL=https://[PROJECT-REF].supabase.co
SUPABASE_KEY=your_supabase_anon_key
```

> [!NOTE]
> All external services are **strictly optional**. If no `.env` credentials are provided:
> - The application automatically uses **local persistent SQLite** (`database/history.db`).
> - The AI Simplifier switches to **Smart Offline Heuristic Mode**.

---

### Running Locally

Launch the application with Streamlit:

```bash
streamlit run app.py
```

The application will automatically open in your default browser at:
```
http://localhost:8501
```

*(On Windows, you can also double-click `run.bat` to launch immediately).*

---

## 🗄️ Database Setup & Cloud Sync

The platform uses a **hybrid dual-layer database architecture**:
1. **Primary**: Cloud PostgreSQL (Supabase, Neon, Render, AWS RDS).
2. **Fallback**: Local embedded SQLite (`database/history.db`) if offline or unconfigured.

### Setting up Supabase

1. Open your [Supabase Dashboard](https://supabase.com/dashboard) and create a project.
2. In the **SQL Editor**, execute the migration script located at:
   [`scripts/schema_supabase.sql`](file:///scripts/schema_supabase.sql)
3. Copy your database connection URI from **Project Settings → Database → Connection String (URI)** into `.env`:
   ```env
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```
4. Test the connection from **Page 8 (Settings)** or run:
   ```bash
   python scripts/run_supabase_sql.py
   ```

### 1-Click SQLite to PostgreSQL Migration

To migrate your existing local audit history into Supabase, run:

```bash
python scripts/migrate_to_supabase.py
```

---

## 🏛️ WCAG 2.2 & Multi-Standard Compliance

Audits are evaluated against the latest accessibility standards:

| Standard | Coverage / Success Criteria Evaluated |
|---|---|
| **WCAG 2.2 Level A** | `1.1.1` Non-text Content, `1.3.1` Info and Relationships, `2.4.4` Link Purpose, `3.3.2` Labels or Instructions. |
| **WCAG 2.2 Level AA** | `1.4.3` Contrast (Minimum), `2.4.6` Headings and Labels, `3.1.2` Language of Parts. |
| **WCAG 2.2 Level AAA** | `1.4.6` Contrast (Enhanced), `3.1.3` Unusual Words, `3.1.4` Abbreviations, `3.1.5` Reading Level. |
| **Section 508** | §1194.22 Web-based intranet and internet information and applications. |
| **EN 301 549** | Chapter 9 (Web Accessibility) European Standard for Public Procurement. |

Access formal audit results, filtering by criterion level and status, and export compliance reports from **Page 9 (`pages/9_WCAG_Compliance.py`)**.

---

## 🔬 NLP & Violation Detection Pipeline

```mermaid
graph TD
    A[Input Copy / Document / URL] --> B[Text Normalizer & Cleaner]
    B --> C[Sentence & Token Segmentation]
    C --> D[POS Tagging & NER Extraction]
    C --> E[Readability & Syllable Engines]
    C --> F[Syntax & Syntactic Depth Parser]
    
    D --> G[Accessibility Rule Evaluator]
    E --> G
    F --> G
    
    G --> H[Issue Matrix Generation]
    G --> I[XAI Penalty Contribution Score]
    H --> J[Itemized Structured Points]
    
    J --> K1[📌 Issue Explanation]
    J --> K2[🔍 Evidence Snippet]
    J --> K3[💡 Remediation Action]
```

---

## 💡 AI Simplification Engine

The simplifier adapts source copy across 6 persona targets:

```
[Raw Source Text]
       │
       ▼
[AI Simplifier Engine] ─── (Gemini 2.5 Flash / Smart Offline Heuristic)
       │
       ├─► 📖 Plain English        (Short sentences, active voice, 8th-grade readability)
       ├─► 🧩 Dyslexia-Friendly    (Bullet points, generous white space, visual anchoring)
       ├─► ⚡ ADHD-Friendly        (Bite-sized sections, bold highlights, action-first steps)
       ├─► 👓 Elderly-Friendly     (Step-by-step guidance, no jargon, direct clarity)
       ├─► 🎒 Child-Friendly       (Grade 3-5 vocabulary, relatable wording)
       └─► 🤝 Inclusive Language   (Gender-neutral, respectful, bias-free phrasing)
```

---

## 📄 License & Attribution

Distributed under the **MIT License**. See `LICENSE` for more information.

- **Design System**: Linear/Stripe-inspired token architecture (`design-system/accessibility-intelligence/MASTER.md`)
- **Linguistic Engine**: `spaCy`, `textstat`, `textblob`, `scikit-learn`
- **Visualization**: `Plotly Express` & `Graph Objects`
- **Generative AI**: `google-genai` (Gemini 2.5)

---

<div align="center">
  <sub>Built for universal cognitive accessibility and digital inclusion.</sub>
</div>
