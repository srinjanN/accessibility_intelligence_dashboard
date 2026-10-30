"""
Page 4: AI Simplifier & Multi-Persona Rewriter Page
"""

import os
import streamlit as st
from utils.ui_components import inject_custom_css, render_header_banner, render_kpi_card, ensure_active_analysis
from utils.ai_service import simplify_text_gemini
from utils.nlp_engine import compute_readability_metrics

inject_custom_css()

render_header_banner(
    title="AI Simplifier & Multi-Persona Rewriter",
    subtitle="Transform complex copy into accessible, plain-English, dyslexia-friendly, ADHD-friendly, elderly-friendly, or child-friendly versions."
)

current_res, input_text = ensure_active_analysis()
if not input_text:
    st.info("💡 No input copy provided yet. Please enter or upload text on the **Dashboard** page first!")
    if st.button("👉 Go to Dashboard"):
        st.switch_page("pages/1_📊_Dashboard.py")
    st.stop()

# Persona Selector & Configuration
col_p1, col_p2 = st.columns([2, 1])

with col_p1:
    persona = st.selectbox(
        "🎯 Select Target Audience Persona:",
        options=[
            "Plain English (Simplified & Active Voice)",
            "Dyslexia-Friendly (Short sentences & Bullet points)",
            "ADHD-Friendly (Bite-sized sections & Bold key terms)",
            "Elderly-Friendly (Clear step-by-step & Simple terms)",
            "Child-Friendly (Grade 3-5 reading level & Friendly tone)",
            "Inclusive Language (Gender-neutral & Accessible phrasing)"
        ]
    )

with col_p2:
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        st.success("🤖 Generative Rewriter Active", icon="⚡")
    else:
        st.info("🧠 Smart Rewriter Active", icon="⚡")

if st.button("✨ Simplify & Rewrite Text Now", type="primary", use_container_width=True):
    with st.spinner("Rewriting copy for chosen persona..."):
        simplified_res = simplify_text_gemini(input_text, persona)
        st.session_state["simplified_text"] = simplified_res
        st.session_state["last_persona"] = persona
        
        # Update current analysis state with simplified text
        if st.session_state.get("current_analysis"):
            st.session_state.current_analysis["simplified_text"] = simplified_res

simplified_text = st.session_state.get("simplified_text", "")

if simplified_text:
    st.markdown("### 🔄 **Side-by-Side Content Comparison**")
    
    col_orig, col_new = st.columns(2)
    with col_orig:
        st.markdown("#### 📄 **Original Text**")
        st.info(input_text)
        metrics_orig = compute_readability_metrics(input_text)
        st.caption(f"Flesch Readability: **{metrics_orig['flesch_reading_ease']}** | Grade: **{metrics_orig['flesch_kincaid_grade']}**")
        
    with col_new:
        st.markdown(f"#### ✨ **Simplified Text ({st.session_state.get('last_persona', 'Plain')})**")
        st.success(simplified_text)
        metrics_new = compute_readability_metrics(simplified_text)
        st.caption(f"Flesch Readability: **{metrics_new['flesch_reading_ease']}** | Grade: **{metrics_new['flesch_kincaid_grade']}**")
        
    st.divider()
    
    # Readability Improvement Diff
    st.markdown("### 📊 **Readability Impact & Improvement**")
    diff_col1, diff_col2, diff_col3 = st.columns(3)
    
    fre_diff = round(metrics_new['flesch_reading_ease'] - metrics_orig['flesch_reading_ease'], 1)
    grade_diff = round(metrics_orig['flesch_kincaid_grade'] - metrics_new['flesch_kincaid_grade'], 1)
    time_diff = round(metrics_orig['reading_time_seconds'] - metrics_new['reading_time_seconds'], 1)
    
    with diff_col1:
        render_kpi_card("Readability Gain", f"+{fre_diff}" if fre_diff >= 0 else f"{fre_diff}", "Flesch Points Improved", "📈", value_color="#10b981")
    with diff_col2:
        render_kpi_card("Grade Reduction", f"-{grade_diff}" if grade_diff >= 0 else f"{grade_diff}", "School Grades Simpler", "🎓", value_color="#6366f1")
    with diff_col3:
        render_kpi_card("Time Saved", f"{time_diff}s", "Seconds Saved per Reader", "⏱️", value_color="#a855f7")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📜 Export & Generate Downloadable Report"):
        st.switch_page("pages/6_📜_Reports.py")
