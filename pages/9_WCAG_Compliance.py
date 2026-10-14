"""
Page 9: WCAG 2.2 Compliance Audit & Standards Mapping
Evaluates active document analysis against WCAG 2.2 (Level A, AA, AAA),
U.S. Section 508, and European EN 301 549 accessibility specifications.
"""

import sys
import os
import site

user_site = site.USER_SITE
if user_site and os.path.exists(user_site) and user_site not in sys.path:
    site.addsitedir(user_site)

import html
import streamlit as st
import pandas as pd

from utils.ui_components import inject_custom_css, render_header_banner, render_kpi_card
from utils.wcag_mapping import evaluate_wcag_compliance
from utils.compliance_report import (
    generate_compliance_pdf_report,
    generate_compliance_docx_report,
    generate_compliance_csv_report,
    generate_compliance_json_report
)

inject_custom_css()

render_header_banner(
    title="WCAG 2.2 Compliance & Standards Mapping",
    subtitle="Evaluate cognitive accessibility violations against WCAG 2.2 (A / AA / AAA), Section 508, and EN 301 549 benchmarks."
)

current_res = st.session_state.get("current_analysis")
doc_name = st.session_state.get("doc_name", "Active Document")

if current_res is None:
    st.info("💡 No active document in the current session. Run a new analysis on the **Dashboard** or load saved data below:")
    
    col_act1, col_act2, col_act3 = st.columns(3)
    with col_act1:
        if st.button("👉 Go to Dashboard", type="primary", use_container_width=True):
            st.switch_page("pages/1_📊_Dashboard.py")
    with col_act2:
        if st.button("🔄 Load Latest Saved Record", type="secondary", use_container_width=True):
            from database.db_manager import get_history
            recent = get_history(limit=1)
            if recent and len(recent) > 0:
                rec = recent[0]
                st.session_state.input_text = rec["input_text"]
                st.session_state.doc_name = rec["doc_name"]
                st.session_state.file_type = rec["file_type"]
                st.session_state.current_analysis = {
                    "accessibility_score": rec["accessibility_score"],
                    "readability_score": rec["readability_score"],
                    "grade_level": rec["grade_level"],
                    "reading_time_seconds": rec["reading_time"],
                    "violations_count": rec["violations_count"],
                    "issues": rec["issues"],
                    "metrics": rec["metrics"]
                }
                st.rerun()
            else:
                st.warning("No historical analyses found.")
    with col_act3:
        if st.button("⚡ Load & Audit Sample Document", type="secondary", use_container_width=True):
            from utils.accessibility_rules import analyze_accessibility
            sample_copy = (
                "It is to be considered that utilization of aforementioned paradigms facilitates optimal synergy. "
                "Furthermore, the user must never disregard the statutory requirements stipulated herein without prior authorization. "
                "CLICK HERE TO READ MORE AND PROCEED TO ARBITRATION."
            )
            analysis_res = analyze_accessibility(sample_copy)
            st.session_state.input_text = sample_copy
            st.session_state.doc_name = "Sample_Terms_And_Conditions.docx"
            st.session_state.file_type = "Sample"
            st.session_state.current_analysis = analysis_res
            st.rerun()
            
    st.stop()

# Non-mutating WCAG evaluation
raw_issues = current_res.get("issues", [])
compliance = evaluate_wcag_compliance(raw_issues)

# --- 1. OVERALL CERTIFICATION BADGE & KPIS ---
st.markdown("### 🛡️ **WCAG 2.2 Compliance Certification Status**")

tier = compliance["overall_tier"]
badge_color = compliance["badge_color"]
badge_text = compliance["badge_text"]
pass_pct = compliance["compliance_score"]

# Hero Certification Card with High-Contrast Theming
st.markdown(f"""
<div style="background: rgba(255, 255, 255, 0.05); border: 2px solid {badge_color}; border-radius: 16px; padding: 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
    <div>
        <div style="display: flex; align-items: center; gap: 14px;">
            <span style="font-size: 2.4rem;">🏅</span>
            <div>
                <h2 style="margin: 0; font-size: 1.6rem; font-weight: 800; color: {badge_color};">{badge_text}</h2>
                <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.95rem;">Audited Document: <strong style="color: #334155;">{doc_name}</strong> • Conformance: WCAG 2.2 / Section 508 / EN 301 549</p>
            </div>
        </div>
    </div>
    <div style="background: {badge_color}18; border: 1.5px solid {badge_color}; border-radius: 12px; padding: 12px 28px; text-align: center;">
        <div style="font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Compliance Rate</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: {badge_color}; line-height: 1.1;">{pass_pct}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Three Tier Level Summary Cards
col_lvl1, col_lvl2, col_lvl3 = st.columns(3)
lvl_counts = compliance["level_counts"]

with col_lvl1:
    l_failed = lvl_counts["Level A"]["failed"]
    st_color = "#10b981" if l_failed == 0 else "#ef4444"
    st_status = "PASSED (100%)" if l_failed == 0 else f"FAILED ({l_failed} issue)"
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid {st_color}66; border-top: 4px solid {st_color}; border-radius: 14px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
        <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #64748b; display: flex; align-items: center; gap: 6px;">
            <span>🥇</span> WCAG Level A (Must Have)
        </div>
        <div style="font-size: 1.45rem; font-weight: 800; color: {st_color}; margin: 8px 0 4px 0;">{st_status}</div>
        <div style="font-size: 0.8rem; color: #64748b;">{lvl_counts['Level A']['passed']} of {lvl_counts['Level A']['total']} criteria met</div>
    </div>
    """, unsafe_allow_html=True)

with col_lvl2:
    l_failed = lvl_counts["Level AA"]["failed"]
    st_color = "#10b981" if l_failed == 0 else "#ef4444"
    st_status = "PASSED (100%)" if l_failed == 0 else f"FAILED ({l_failed} issue)"
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid {st_color}66; border-top: 4px solid {st_color}; border-radius: 14px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
        <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #64748b; display: flex; align-items: center; gap: 6px;">
            <span>🥈</span> WCAG Level AA (Standard)
        </div>
        <div style="font-size: 1.45rem; font-weight: 800; color: {st_color}; margin: 8px 0 4px 0;">{st_status}</div>
        <div style="font-size: 0.8rem; color: #64748b;">{lvl_counts['Level AA']['passed']} of {lvl_counts['Level AA']['total']} criteria met</div>
    </div>
    """, unsafe_allow_html=True)

with col_lvl3:
    l_failed = lvl_counts["Level AAA"]["failed"]
    st_color = "#10b981" if l_failed == 0 else "#eab308"
    st_status = "PASSED (100%)" if l_failed == 0 else f"PARTIAL ({l_failed} failing)"
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid {st_color}66; border-top: 4px solid {st_color}; border-radius: 14px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
        <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #64748b; display: flex; align-items: center; gap: 6px;">
            <span>🥉</span> WCAG Level AAA (Enhanced)
        </div>
        <div style="font-size: 1.45rem; font-weight: 800; color: {st_color}; margin: 8px 0 4px 0;">{st_status}</div>
        <div style="font-size: 0.8rem; color: #64748b;">{lvl_counts['Level AAA']['passed']} of {lvl_counts['Level AAA']['total']} criteria met</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 2. FILTER CONTROLS ---
st.markdown("### 🔍 **Filter Success Criteria**")

col_f1, col_f2 = st.columns([1, 1])

with col_f1:
    level_filter = st.selectbox(
        "Filter by WCAG Level:",
        options=["All Levels", "Level A (Baseline)", "Level AA (Recommended Legal Standard)", "Level AAA (Enhanced Cognitive Inclusivity)"],
        index=0
    )

with col_f2:
    status_filter = st.selectbox(
        "Filter by Conformance Status:",
        options=["All Criteria", "Failed Only (Action Required)", "Passed Only"],
        index=0
    )

# Filter criteria list
all_criteria = compliance["criteria_results"]
filtered_criteria = []

for c in all_criteria:
    # Level filtering
    if level_filter == "Level A (Baseline)" and c["level"] != "Level A":
        continue
    elif level_filter == "Level AA (Recommended Legal Standard)" and c["level"] != "Level AA":
        continue
    elif level_filter == "Level AAA (Enhanced Cognitive Inclusivity)" and c["level"] != "Level AAA":
        continue
        
    # Status filtering
    if status_filter == "Failed Only (Action Required)" and c["passed"]:
        continue
    elif status_filter == "Passed Only" and not c["passed"]:
        continue
        
    filtered_criteria.append(c)

st.caption(f"Showing **{len(filtered_criteria)}** of **{len(all_criteria)}** evaluated success criteria:")

# --- 3. SUCCESS CRITERIA DETAILED CARDS & TABLE ---
for crit in filtered_criteria:
    is_pass = crit["passed"]
    status_badge = '<span style="background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.8rem;">🟢 PASS</span>' if is_pass else '<span style="background: rgba(239, 68, 68, 0.2); color: #f87171; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.8rem;">🔴 FAIL</span>'
    card_border = "rgba(16, 185, 129, 0.3)" if is_pass else "rgba(239, 68, 68, 0.4)"
    
    with st.expander(f"{'✅' if is_pass else '❌'} Criterion {crit['criterion']}: {crit['name']} [{crit['level']}] - {crit['status']}", expanded=not is_pass):
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            st.markdown(f"#### **WCAG {crit['criterion']} • {crit['name']}**")
            st.markdown(f"**Principle:** `{crit['principle']}` | **Guideline:** `{crit['guideline']}` | **Conformance:** `{crit['level']}`")
            st.caption(f"**U.S. Section 508:** {crit['section_508']} • **European Standard:** {crit['en_301_549']}")
        with col_c2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(status_badge, unsafe_allow_html=True)
            if not is_pass:
                st.markdown(f"<div style='margin-top: 6px; font-size: 0.85rem; color: #f87171;'><strong>{crit['violations_count']}</strong> violation(s) detected</div>", unsafe_allow_html=True)

        st.markdown("---")
        
        if is_pass:
            st.success("🟢 **Criteria Met:** No violations detected for this criterion in the analyzed copy.")
        else:
            st.error(f"🔴 **Action Required:** {crit['violations_count']} issue(s) violated this success criterion:")
            for issue_idx, iss in enumerate(crit["issues"], 1):
                safe_title = html.escape(str(iss.get('title', 'Violation')))
                safe_sev = html.escape(str(iss.get('severity', 'Medium')))
                safe_expl = html.escape(str(iss.get('explanation', '')))
                safe_snip = html.escape(str(iss.get('snippet', '')))
                safe_remed = html.escape(str(iss.get('wcag_remediation', '')))
                
                parts = [
                    '<div class="issue-card" style="border-left: 4px solid var(--color-critical);">',
                    '<div class="issue-card-header">',
                    f'<span class="issue-card-title">#{issue_idx}. {safe_title}</span>',
                    f'<span class="badge-medium">{safe_sev} Severity</span>',
                    '</div>',
                    '<div class="issue-points-list">',
                    f'<div class="issue-point-item"><span class="issue-point-tag issue-point-tag-issue">📌 Violation</span><div class="issue-point-content"><strong>Explanation:</strong> {safe_expl}</div></div>'
                ]
                if safe_snip:
                    parts.append(f'<div class="issue-point-item"><span class="issue-point-tag issue-point-tag-evidence">🔍 Evidence</span><div class="issue-point-content"><div class="issue-point-snippet">&ldquo;{safe_snip}&rdquo;</div></div></div>')
                if safe_remed:
                    parts.append(f'<div class="issue-point-item"><span class="issue-point-tag issue-point-tag-recommendation">💡 Fix</span><div class="issue-point-content"><strong>WCAG Action:</strong> {safe_remed}</div></div>')
                parts.extend(['</div>', '</div>'])
                st.markdown("".join(parts), unsafe_allow_html=True)

st.divider()

# --- 4. REGULATORY COMPARISON MATRIX ---
st.markdown("### 🌐 **Multi-Standard Regulatory Harmonization**")
st.caption("Cross-reference WCAG 2.2 criteria with federal and international digital accessibility mandates:")

matrix_rows = []
for c in compliance["criteria_results"]:
    matrix_rows.append({
        "WCAG 2.2 Criterion": f"{c['criterion']} {c['name']}",
        "Level": c["level"],
        "Audit Status": "PASS" if c["passed"] else "FAIL",
        "U.S. Section 508": c["section_508"],
        "European EN 301 549": c["en_301_549"]
    })

df_matrix = pd.DataFrame(matrix_rows)
st.dataframe(df_matrix, use_container_width=True)

st.divider()

# --- 5. COMPLIANCE EXPORTS ---
st.markdown(f"### 📥 **Download Compliance Audit Reports for: `{doc_name}`**")
st.caption("Generate formal audit evidence documents for accessibility compliance records and stakeholder sign-offs.")

col_exp1, col_exp2, col_exp3, col_exp4 = st.columns(4)

with col_exp1:
    st.markdown("#### 📄 **Compliance PDF**")
    st.caption("Formatted report with certification badge and criteria tables.")
    pdf_data = generate_compliance_pdf_report(compliance, doc_title=f"WCAG Compliance Audit: {doc_name}")
    st.download_button(
        label="⬇️ Download PDF Audit",
        data=pdf_data,
        file_name=f"{doc_name.replace(' ', '_')}_WCAG_Compliance_Report.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )

with col_exp2:
    st.markdown("#### 📝 **Word DOCX**")
    st.caption("Editable Word audit report with criteria matrices.")
    docx_data = generate_compliance_docx_report(compliance, doc_title=f"WCAG Compliance Audit: {doc_name}")
    st.download_button(
        label="⬇️ Download DOCX Audit",
        data=docx_data,
        file_name=f"{doc_name.replace(' ', '_')}_WCAG_Compliance_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )

with col_exp3:
    st.markdown("#### 📊 **Criteria CSV**")
    st.caption("Spreadsheet table of criteria pass/fail statuses.")
    csv_data = generate_compliance_csv_report(compliance)
    st.download_button(
        label="⬇️ Download CSV Log",
        data=csv_data,
        file_name=f"{doc_name.replace(' ', '_')}_WCAG_Criteria.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_exp4:
    st.markdown("#### ⚙️ **Compliance JSON**")
    st.caption("Full structured schema for CI/CD and automated pipelines.")
    json_data = generate_compliance_json_report(compliance, doc_title=f"WCAG Compliance Audit: {doc_name}")
    st.download_button(
        label="⬇️ Download JSON Data",
        data=json_data,
        file_name=f"{doc_name.replace(' ', '_')}_WCAG_Compliance.json",
        mime="application/json",
        use_container_width=True
    )
