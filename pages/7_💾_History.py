"""
Page 7: History & Saved Analysis Repository
Supports Online PostgreSQL & Local SQLite with Search & Management
"""

import os
import streamlit as st
import pandas as pd
from utils.ui_components import inject_custom_css, render_header_banner
from database.db_manager import (
    get_history,
    get_analysis_by_id,
    delete_analysis,
    clear_all_history
)

inject_custom_css()

render_header_banner(
    title="History & Saved Analysis Repository",
    subtitle="Search, filter, view, re-analyze, or delete historical cognitive & readability analysis runs."
)

col_h1, col_h2 = st.columns([3, 1])

with col_h1:
    search_query = st.text_input("🔍 Search History by Document Name or Keywords:", placeholder="Type to search...")
with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear All History", type="secondary", use_container_width=True):
        if clear_all_history():
            st.success("History cleared successfully!")
            st.rerun()

history_records = get_history(search_query=search_query, limit=50)

if not history_records:
    st.info("No saved analysis records found.")
else:
    st.markdown(f"Found **{len(history_records)}** saved analysis record(s):")
    
    # Table summary
    summary_list = []
    for rec in history_records:
        summary_list.append({
            "ID": rec["id"],
            "Timestamp": rec["timestamp"],
            "Document Name": rec["doc_name"],
            "Type": rec["file_type"],
            "Accessibility Score": rec["accessibility_score"],
            "Readability": rec["readability_score"],
            "Grade Level": rec["grade_level"],
            "Violations": rec["violations_count"]
        })
        
    df_hist = pd.DataFrame(summary_list)
    st.dataframe(df_hist, use_container_width=True)
    
    st.divider()
    
    st.markdown("### 📋 **Inspect, Re-Analyze, or Delete Record**")
    
    record_ids = [rec["id"] for rec in history_records]
    selected_id = st.selectbox(
        "Select Record ID:",
        options=record_ids,
        format_func=lambda x: f"ID #{x} - {next((r['doc_name'] for r in history_records if r['id']==x), 'Record')}"
    )
    
    selected_record = get_analysis_by_id(selected_id)
    
    if selected_record:
        col_rec1, col_rec2 = st.columns([3, 1])
        with col_rec1:
            st.markdown(f"#### **Record #{selected_record['id']}: {selected_record['doc_name']}**")
            st.caption(f"Analyzed on: {selected_record['timestamp']} | Type: {selected_record['file_type']}")
            st.markdown(f"**Accessibility Score:** `{selected_record['accessibility_score']} / 100` | **Violations:** `{selected_record['violations_count']}`")
            st.text_area("Original Content:", value=selected_record['input_text'][:600] + "...", height=100, disabled=True)
            
        with col_rec2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Load & Re-Analyze Record", type="primary", use_container_width=True):
                st.session_state.input_text = selected_record['input_text']
                st.session_state.doc_name = selected_record['doc_name']
                st.session_state.file_type = selected_record['file_type']
                st.session_state.current_analysis = {
                    "accessibility_score": selected_record['accessibility_score'],
                    "readability_score": selected_record['readability_score'],
                    "grade_level": selected_record['grade_level'],
                    "reading_time_seconds": selected_record['reading_time'],
                    "violations_count": selected_record['violations_count'],
                    "issues": selected_record['issues'],
                    "metrics": selected_record['metrics'],
                    "simplified_text": selected_record.get('simplified_text', '')
                }
                st.success("Loaded into active session! Redirecting to Dashboard...")
                st.switch_page("pages/1_📊_Dashboard.py")
                
            if st.button("❌ Delete Record", type="secondary", use_container_width=True):
                if delete_analysis(selected_id):
                    st.success(f"Record #{selected_id} deleted successfully.")
                    st.rerun()
