"""
Page 3: Comprehensive Accessibility Audit & Explainable AI (XAI)
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.ui_components import inject_custom_css, render_header_banner, render_issue_card, ensure_active_analysis

inject_custom_css()

render_header_banner(
    title="Accessibility Audit & Explainable AI (XAI)",
    subtitle="Detailed violation detection matrix, highlighted evidence snippets, concrete improvement suggestions, and feature importance rationale."
)

current_res, input_text = ensure_active_analysis()
if current_res is None:
    st.info("💡 No active document found. Please run an analysis on the **Dashboard** page first!")
    if st.button("👉 Go to Dashboard"):
        st.switch_page("pages/1_📊_Dashboard.py")
    st.stop()

issues = current_res.get("issues", [])
xai_explanation = current_res.get("xai_explanation", "")
feature_importance = current_res.get("feature_importance", {})

# Explainable AI (XAI) Summary Section
st.markdown("### 🧠 **Explainable AI (XAI) Score Rationale**")
st.info(xai_explanation, icon="ℹ️")

col_xai1, col_xai2 = st.columns([1, 1])

with col_xai1:
    st.markdown("#### **Score Penalty Drivers (Feature Importance)**")
    if feature_importance:
        df_feat = pd.DataFrame(list(feature_importance.items()), columns=["Factor", "Penalty Score"])
        fig_feat = px.bar(
            df_feat,
            x="Penalty Score",
            y="Factor",
            orientation="h",
            color="Penalty Score",
            color_continuous_scale="Reds",
            title="Deductions Dragging Down Accessibility Score"
        )
        fig_feat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_feat, use_container_width=True)

with col_xai2:
    st.markdown("#### **Violations Severity Distribution**")
    if issues:
        severities = [i.get("severity", "Low") for i in issues]
        sev_df = pd.DataFrame(pd.Series(severities).value_counts()).reset_index()
        sev_df.columns = ["Severity", "Count"]
        
        color_map = {"Critical": "#ef4444", "High": "#f97316", "Medium": "#eab308", "Low": "#3b82f6"}
        fig_pie = px.pie(
            sev_df,
            names="Severity",
            values="Count",
            color="Severity",
            color_discrete_map=color_map,
            hole=0.4,
            title="Issues by Severity Level"
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc")
        )
        st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# Violations Filter & Matrix
st.markdown(f"### 🚨 **Identified Issues ({len(issues)})**")

if not issues:
    st.success("🎉 No accessibility or cognitive inclusion violations detected in this copy!", icon="✅")
else:
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        selected_severity = st.multiselect(
            "Filter by Severity:",
            options=["Critical", "High", "Medium", "Low"],
            default=["Critical", "High", "Medium", "Low"]
        )
    with col_f2:
        categories = list(set([i.get("category", "General") for i in issues]))
        selected_categories = st.multiselect(
            "Filter by Category:",
            options=categories,
            default=categories
        )
        
    filtered_issues = [
        i for i in issues
        if i.get("severity") in selected_severity and i.get("category") in selected_categories
    ]
    
    st.markdown(f"Showing **{len(filtered_issues)}** of **{len(issues)}** issues:")
    for idx, issue in enumerate(filtered_issues, 1):
        render_issue_card(issue, index=idx)
