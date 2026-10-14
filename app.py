"""
AI-Powered Accessibility Intelligence Dashboard
Main Application Entry Point.
"""

import os
import sys
import site

# Register user site-packages directory
user_site = site.USER_SITE
if user_site and os.path.exists(user_site) and user_site not in sys.path:
    site.addsitedir(user_site)

import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Page Configuration with clean Material icon mark
st.set_page_config(
    page_title="Accessibility Intelligence Dashboard",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.ui_components import inject_custom_css, render_header_banner, render_theme_switcher
from database.db_manager import init_db

# Inject custom styling & enterprise Plotly theme (theme toggle rendered in sidebar below)
inject_custom_css(render_sidebar_toggle=False)

# Initialize DB Schema
init_db()

# Initialize Session State
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "doc_name" not in st.session_state:
    st.session_state.doc_name = "Untitled Copy"
if "file_type" not in st.session_state:
    st.session_state.file_type = "Pasted Text"
if "custom_thresholds" not in st.session_state:
    st.session_state.custom_thresholds = {
        "max_sentence_length": 20,
        "target_reading_level": 8.0,
        "max_passive_pct": 15.0
    }

# Sidebar Info, Prominent Theme Switcher & Navigation Overview
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-wrap">
        <div class="sidebar-logo">
            <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="4" r="2"/><path d="M5 9h14"/><path d="M12 9v12"/><path d="m8 13 4 3 4-3"/>
            </svg>
        </div>
        <div class="sidebar-title">Accessibility Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("v2.5 Production Edition • Multi-Engine NLP & AI")
    
    # Prominent Dark / Light Mode Switcher
    render_theme_switcher()
    
    st.divider()
    
    st.markdown("### **Navigation Overview**")
    st.markdown("""
    - **Dashboard**: Main text analysis & KPIs
    - **NLP Pipeline**: Deep linguistic & POS breakdown
    - **Accessibility Audit**: Issue highlights & XAI
    - **AI Simplifier**: 6 Persona Rewriters
    - **Visual Analytics**: Interactive Plotly charts
    - **Reports**: Downloadable PDF / DOCX / CSV / JSON
    - **History**: Saved analysis repository & inspection
    - **Settings**: Audit thresholds & user preferences
    - **WCAG Compliance**: Multi-standard Level A/AA/AAA verification
    """)

# Main Welcome / Header View
render_header_banner(
    title="Accessibility Intelligence Platform",
    subtitle="Evaluate, visualize, and simplify digital copy, documents, and UI text for cognitive accessibility, WCAG standards, and inclusion."
)

st.markdown("""
### **Platform Capabilities**

Use the sidebar navigation on the left to navigate through the multi-page suite:

<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-card-icon">
            <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>
        </div>
        <div class="feature-card-title">1. Dashboard & Analysis</div>
        <p class="feature-card-desc">Input text, documents, images (OCR), or URLs. View instant accessibility & readability KPIs.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">
            <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        </div>
        <div class="feature-card-title">2. NLP Pipeline</div>
        <p class="feature-card-desc">Examine POS tags, named entities, TF-IDF keywords, N-grams, and syntactic structure.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">
            <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="4" r="2"/><path d="M5 9h14"/><path d="M12 9v12"/><path d="m8 13 4 3 4-3"/></svg>
        </div>
        <div class="feature-card-title">3. Accessibility Audit & XAI</div>
        <p class="feature-card-desc">Identify 10+ violation types with highlighted evidence and Explainable AI (XAI) rationale.</p>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">
            <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/></svg>
        </div>
        <div class="feature-card-title">4. AI Simplifier</div>
        <p class="feature-card-desc">Rewrite text into Plain English, Dyslexia, ADHD, Elderly, Child, or Inclusive personas.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    st.info("Get Started: Select **Dashboard** from the sidebar to paste text or load a sample document.", icon=":material/info:")
with col2:
    if st.button("Go to Dashboard", icon=":material/arrow_forward:", type="primary", use_container_width=True):
        st.switch_page("pages/1_📊_Dashboard.py")
