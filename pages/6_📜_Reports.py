"""
Page 6: Multi-Format Downloadable Report Generator
"""

import streamlit as st
from utils.ui_components import inject_custom_css, render_header_banner
from utils.report_generator import (
    generate_pdf_report, generate_docx_report,
    generate_csv_report, generate_json_report
)

inject_custom_css()

render_header_banner(
    title="Report Generator & Multi-Format Exports",
    subtitle="Generate, preview, and download comprehensive accessibility compliance reports in PDF, DOCX, CSV, and JSON formats."
)

current_res = st.session_state.get("current_analysis")
doc_name = st.session_state.get("doc_name", "Accessibility Audit")

if current_res is None:
    st.info("💡 No active analysis found. Please run an analysis on the **Dashboard** page first!")
    if st.button("👉 Go to Dashboard"):
        st.switch_page("pages/1_📊_Dashboard.py")
    st.stop()

st.markdown(f"### 📥 **Download Reports for: `{doc_name}`**")

col_r1, col_r2, col_r3, col_r4 = st.columns(4)

# 1. PDF Download
with col_r1:
    st.markdown("#### 📄 **PDF Report**")
    st.caption("Formatted document with KPI tables, XAI notes, and issue list.")
    pdf_bytes = generate_pdf_report(current_res, doc_title=f"Audit Report: {doc_name}")
    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_bytes,
        file_name=f"{doc_name.replace(' ', '_')}_Accessibility_Report.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )

# 2. DOCX Download
with col_r2:
    st.markdown("#### 📝 **Word DOCX**")
    st.caption("Editable Microsoft Word document report.")
    docx_bytes = generate_docx_report(current_res, doc_title=f"Audit Report: {doc_name}")
    st.download_button(
        label="⬇️ Download DOCX Report",
        data=docx_bytes,
        file_name=f"{doc_name.replace(' ', '_')}_Accessibility_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )

# 3. CSV Download
with col_r3:
    st.markdown("#### 📊 **CSV Data**")
    st.caption("Spreadsheet table of all detected violations.")
    csv_str = generate_csv_report(current_res)
    st.download_button(
        label="⬇️ Download CSV Log",
        data=csv_str,
        file_name=f"{doc_name.replace(' ', '_')}_Issues.csv",
        mime="text/csv",
        use_container_width=True
    )

# 4. JSON Export
with col_r4:
    st.markdown("#### ⚙️ **JSON Data**")
    st.caption("Structured JSON schema for developer integrations.")
    json_str = generate_json_report(current_res)
    st.download_button(
        label="⬇️ Download JSON Schema",
        data=json_str,
        file_name=f"{doc_name.replace(' ', '_')}_Analysis.json",
        mime="application/json",
        use_container_width=True
    )

st.divider()

# Report Live Preview
st.markdown("### 👁️ **Live Report Executive Preview**")

with st.expander("📄 Click to Expand Executive Report Summary Preview", expanded=True):
    st.markdown(f"## **Accessibility Audit Report: {doc_name}**")
    st.markdown(f"**Overall Accessibility Score:** `{current_res['accessibility_score']} / 100`")
    st.markdown(f"**Readability (Flesch):** `{current_res['readability_score']}` | **Grade Level:** `Grade {current_res['grade_level']}`")
    st.markdown(f"**Total Violations Identified:** `{current_res['violations_count']}`")
    
    st.markdown("---")
    st.markdown("#### **Explainable AI Score Rationale:**")
    st.write(current_res.get("xai_explanation", "N/A"))
    
    st.markdown("---")
    st.markdown("#### **Top Detected Violations:**")
    for idx, iss in enumerate(current_res.get("issues", [])[:5], 1):
        st.markdown(f"**#{idx}. {iss.get('title')}** [{iss.get('severity')}]")
        st.markdown(f"*Category:* `{iss.get('category')}`")
        st.markdown(f"*Explanation:* {iss.get('explanation')}")
        if iss.get("suggestion"):
            st.markdown(f"*Recommendation:* {iss.get('suggestion')}")
        st.write("")
        
    if current_res.get("simplified_text"):
        st.markdown("---")
        st.markdown("#### **AI Simplified Revision:**")
        st.success(current_res["simplified_text"])
