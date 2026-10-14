"""
Page 1: Main Dashboard & Input Ingestion Page
"""

import os
import streamlit as st
from utils.ui_components import inject_custom_css, render_header_banner, render_kpi_card
from utils.file_parsers import parse_txt, parse_pdf, parse_docx, parse_csv_excel, parse_image_ocr, parse_url
from utils.accessibility_rules import analyze_accessibility
from database.db_manager import save_analysis

inject_custom_css()

render_header_banner(
    title="Dashboard & Multi-Format Text Analysis",
    subtitle="Ingest copy from pasted text, PDF, DOCX, CSV, Excel, Image OCR, or Web URLs for instant cognitive accessibility scoring.",
    icon="dashboard"
)

# Ingestion Options Tabs (labels strictly preserved for state continuity)
tab_paste, tab_doc, tab_data, tab_ocr, tab_url, tab_sample = st.tabs([
    "✍️ Pasted Text", "📄 Document (PDF/DOCX/TXT)", "📊 Data (CSV/Excel)",
    "🖼️ Image OCR", "🌐 Web URL", "📁 Sample Data"
])

input_text = ""
doc_name = "Untitled Copy"
file_type = "Pasted Text"

with tab_paste:
    text_input_val = st.text_area(
        "Paste UI copy, legal agreement, medical text, or web content:",
        value=st.session_state.get("input_text", ""),
        height=200,
        placeholder="Enter or paste text here to analyze for accessibility..."
    )
    if text_input_val:
        input_text = text_input_val
        file_type = "Pasted Text"
        doc_name = "Pasted Copy"

with tab_doc:
    uploaded_doc = st.file_uploader("Upload Document File", type=["pdf", "docx", "txt"])
    if uploaded_doc is not None:
        file_bytes = uploaded_doc.read()
        file_name = uploaded_doc.name
        doc_name = file_name
        file_type = file_name.split(".")[-1].upper()
        
        if file_name.endswith(".txt"):
            input_text = parse_txt(file_bytes)
        elif file_name.endswith(".pdf"):
            input_text = parse_pdf(file_bytes)
        elif file_name.endswith(".docx"):
            input_text = parse_docx(file_bytes)
            
        st.text_area("Extracted Document Text Preview:", value=input_text[:1000], height=120, disabled=True)

with tab_data:
    uploaded_data = st.file_uploader("Upload Data File", type=["csv", "xlsx", "xls"])
    if uploaded_data is not None:
        file_bytes = uploaded_data.read()
        file_name = uploaded_data.name
        doc_name = file_name
        file_type = "CSV/Excel"
        input_text = parse_csv_excel(file_bytes, file_name)
        st.text_area("Extracted Data Text Preview:", value=input_text[:1000], height=120, disabled=True)

with tab_ocr:
    uploaded_img = st.file_uploader("Upload Image containing text", type=["png", "jpg", "jpeg", "webp"])
    if uploaded_img is not None:
        file_bytes = uploaded_img.read()
        doc_name = uploaded_img.name
        file_type = "Image OCR"
        st.image(file_bytes, width=300, caption="Uploaded Image")
        with st.spinner("Extracting text via OCR..."):
            input_text = parse_image_ocr(file_bytes)
        st.text_area("OCR Extracted Text:", value=input_text, height=120)

with tab_url:
    url_val = st.text_input("Enter Webpage URL:", placeholder="https://example.com/terms")
    if st.button("Fetch Webpage Text", icon=":material/language:"):
        if url_val:
            with st.spinner("Fetching and stripping HTML text..."):
                title, extracted = parse_url(url_val)
                input_text = extracted
                doc_name = title
                file_type = "Web URL"
                st.session_state["url_extracted"] = extracted
                st.session_state["url_title"] = title
    if "url_extracted" in st.session_state:
        input_text = st.session_state["url_extracted"]
        doc_name = st.session_state.get("url_title", "Webpage")
        file_type = "Web URL"
        st.text_area("Extracted Webpage Text:", value=input_text[:1000], height=120, disabled=True)

with tab_sample:
    st.markdown("#### **Pre-Loaded Sample Datasets for 1-Click Testing**")
    col_s1, col_s2, col_s3 = st.columns(3)
    
    sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_data")
    
    with col_s1:
        if st.button("Sample Legal Terms", icon=":material/description:", use_container_width=True):
            file_path = os.path.join(sample_dir, "complex_legal_terms.txt")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    input_text = f.read()
                doc_name = "complex_legal_terms.txt"
                file_type = "Sample Legal"
                st.session_state.input_text = input_text
                
    with col_s2:
        if st.button("Sample UI Microcopy", icon=":material/smart_button:", use_container_width=True):
            file_path = os.path.join(sample_dir, "ui_button_copy.csv")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    input_text = f.read()
                doc_name = "ui_button_copy.csv"
                file_type = "Sample UI CSV"
                st.session_state.input_text = input_text
                
    with col_s3:
        if st.button("Sample Medical Directives", icon=":material/local_hospital:", use_container_width=True):
            file_path = os.path.join(sample_dir, "medical_instructions.txt")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    input_text = f.read()
                doc_name = "medical_instructions.txt"
                file_type = "Sample Medical"
                st.session_state.input_text = input_text

st.divider()

# Analyze Trigger Button
if st.button("Run Full Accessibility Analysis", icon=":material/bolt:", type="primary", use_container_width=True):
    if not input_text.strip():
        st.warning("Please provide or paste text before running the analysis!", icon=":material/warning:")
    else:
        with st.spinner("Processing NLP pipeline & evaluating accessibility rules..."):
            st.session_state.input_text = input_text
            st.session_state.doc_name = doc_name
            st.session_state.file_type = file_type
            
            thresholds = st.session_state.get("custom_thresholds")
            analysis_res = analyze_accessibility(input_text, custom_thresholds=thresholds)
            st.session_state.current_analysis = analysis_res
            
            # Save to Database History
            save_analysis(
                doc_name=doc_name,
                file_type=file_type,
                input_text=input_text,
                accessibility_score=analysis_res["accessibility_score"],
                readability_score=analysis_res["readability_score"],
                grade_level=analysis_res["grade_level"],
                reading_time=analysis_res["reading_time_seconds"],
                violations_count=analysis_res["violations_count"],
                issues=analysis_res["issues"],
                metrics=analysis_res["metrics"]
            )
            st.success("Analysis Complete! Saved to History.", icon=":material/check_circle:")

# Display Results & KPI Grid if analysis is available
current_res = st.session_state.get("current_analysis")
if current_res is not None:
    st.markdown(f"### **Accessibility KPIs: `{st.session_state.get('doc_name', 'Copy')}`**")
    
    score = current_res["accessibility_score"]
    score_color = "#10B981" if score >= 80 else ("#F59E0B" if score >= 60 else "#EF4444")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        render_kpi_card("Accessibility Score", f"{score} / 100", "Combined Cognitive Metric", "accessibility", value_color=score_color)
    with kpi_col2:
        render_kpi_card("Flesch Readability", f"{current_res['readability_score']}", "Reading Ease Index (0-100)", "readability", value_color="var(--color-primary)")
    with kpi_col3:
        render_kpi_card("Reading Grade Level", f"Grade {current_res['grade_level']}", "Flesch-Kincaid Scale", "grade", value_color="var(--color-foreground)")
    with kpi_col4:
        render_kpi_card("Reading Time", f"{current_res['reading_time_seconds']}s", "Estimated Adult Reading", "time", value_color="var(--color-foreground)")
        
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    kpi_col5, kpi_col6, kpi_col7, kpi_col8 = st.columns(4)
    with kpi_col5:
        render_kpi_card("Passive Voice %", f"{current_res['passive_voice_pct']}%", "Sentences in Passive Voice", "voice", value_color="#F59E0B")
    with kpi_col6:
        render_kpi_card("Jargon Words", f"{current_res['jargon_count']}", "Complex Technical Terms", "jargon", value_color="#F59E0B")
    with kpi_col7:
        render_kpi_card("Cognitive Index", f"{current_res['cognitive_complexity']} / 100", "Syntactic Memory Burden", "complexity", value_color="#EF4444")
    with kpi_col8:
        render_kpi_card("Total Violations", f"{current_res['violations_count']}", "Actionable Issues Found", "violations", value_color="#EF4444")

    st.divider()
    
    # Quick Navigation Prompt to detailed views
    col_nav1, col_nav2, col_nav3 = st.columns(3)
    with col_nav1:
        if st.button("Explore NLP Pipeline", icon=":material/analytics:", use_container_width=True):
            st.switch_page("pages/2_🔍_NLP_Pipeline.py")
    with col_nav2:
        if st.button("View Accessibility Violations", icon=":material/warning:", use_container_width=True):
            st.switch_page("pages/3_♿_Accessibility_Audit.py")
    with col_nav3:
        if st.button("Simplify with AI", icon=":material/auto_fix_high:", use_container_width=True):
            st.switch_page("pages/4_✨_AI_Simplifier.py")
else:
    st.markdown("""
    <div class="empty-state-box">
        <div class="empty-state-icon-wrap">
            <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/>
            </svg>
        </div>
        <div class="empty-state-title">No Analysis Generated Yet</div>
        <div class="empty-state-desc">Paste UI copy, upload a document, or choose a pre-loaded sample dataset above, then click <strong>Run Full Accessibility Analysis</strong>.</div>
    </div>
    """, unsafe_allow_html=True)
