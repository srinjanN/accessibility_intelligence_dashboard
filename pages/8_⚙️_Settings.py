"""
Page 8: Application Settings & Custom Preferences
Clean, production-grade configuration without exposing database internals or credentials.
"""

import os
import streamlit as st
from utils.ui_components import inject_custom_css, render_header_banner

inject_custom_css()

render_header_banner(
    title="Application Settings & Custom Preferences",
    subtitle="Configure cognitive accessibility audit thresholds, interface appearance, AI simplifier defaults, and user preferences."
)

# --- 1. AI SIMPLIFIER PREFERENCES ---
st.markdown("### **AI Simplifier & Rewrite Preferences**")
st.caption("Customize generative simplification behavior and default audience personas.")

col_ai1, col_ai2 = st.columns(2)

with col_ai1:
    current_model = st.session_state.get("selected_model", "Gemini 2.5 Flash (Fast, Recommended)")
    model_choice = st.selectbox(
        "AI Rewrite Architecture:",
        options=[
            "Gemini 2.5 Flash (Fast, Recommended)",
            "Gemini 1.5 Pro (Deep Contextual)",
            "Offline Rule-Based Engine (Zero Cloud Latency)"
        ],
        index=0 if "2.5" in current_model else (1 if "1.5" in current_model else 2),
        help="Select the AI architecture used to simplify complex language."
    )
    st.session_state["selected_model"] = model_choice

with col_ai2:
    default_persona = st.selectbox(
        "Default Simplification Persona:",
        options=[
            "Plain English (Simple vocabulary & active voice)",
            "Dyslexia-Friendly (Short sentences & bullet formatting)",
            "ADHD-Friendly (Bite-sized sections & bold keywords)",
            "Elderly-Friendly (Clear step-by-step & familiar terms)",
            "Child-Friendly (Grade 3-5 reading level)",
            "Inclusive Language (Gender-neutral & accessible phrasing)"
        ],
        help="The default target audience persona selected on the AI Simplifier page."
    )
    st.session_state["default_persona"] = default_persona

st.divider()

# --- 2. CUSTOM ACCESSIBILITY THRESHOLDS ---
st.markdown("### **Custom Accessibility Audit Thresholds**")
st.caption("Adjust sensitivity parameters for the cognitive inclusion rule engine:")

curr_thresholds = st.session_state.get("custom_thresholds", {
    "max_sentence_length": 20,
    "target_reading_level": 8.0,
    "max_passive_pct": 15.0
})

col_th1, col_th2, col_th3 = st.columns(3)

with col_th1:
    max_sent_len = st.slider(
        "Max Sentence Length (Words):",
        min_value=12,
        max_value=35,
        value=int(curr_thresholds.get("max_sentence_length", 20)),
        help="Sentences longer than this count will trigger an Overly Long Sentence violation."
    )

with col_th2:
    target_grade = st.slider(
        "Target Reading Grade Level:",
        min_value=4.0,
        max_value=12.0,
        value=float(curr_thresholds.get("target_reading_level", 8.0)),
        step=0.5,
        help="Reading grade level goal based on Flesch-Kincaid scale."
    )

with col_th3:
    max_passive = st.slider(
        "Max Passive Voice % Threshold:",
        min_value=5.0,
        max_value=30.0,
        value=float(curr_thresholds.get("max_passive_pct", 15.0)),
        step=1.0,
        help="Maximum acceptable percentage of passive voice sentences."
    )

if st.button("Save Custom Audit Thresholds", icon=":material/save:", type="primary", use_container_width=True):
    st.session_state.custom_thresholds = {
        "max_sentence_length": max_sent_len,
        "target_reading_level": target_grade,
        "max_passive_pct": max_passive
    }
    st.success("Settings saved successfully! Future analyses will use these custom thresholds.", icon=":material/check_circle:")

st.divider()

# --- 3. DISPLAY & ACCESSIBILITY PREFERENCES ---
st.markdown("### **Display & Visual Preferences**")

col_ui1, col_ui2, col_ui3 = st.columns(3)
with col_ui1:
    high_contrast = st.toggle("Enable High-Contrast Violation Highlighting", value=True, help="Use enhanced contrast borders on highlighted evidence cards.")
with col_ui2:
    show_reading_gauge = st.toggle("Show Speedometer Gauge on Main Dashboard", value=True, help="Render the interactive Plotly gauge chart on the Dashboard overview.")
with col_ui3:
    curr_theme = st.session_state.get("app_theme", "Dark")
    theme_choice = st.selectbox(
        "Interface Color Theme:",
        options=["Dark", "Light"],
        index=0 if curr_theme == "Dark" else 1,
        help="Switch between Dark and Light mode across all pages."
    )
    if theme_choice != curr_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()

st.divider()

# --- 4. SYSTEM INFORMATION ---
st.markdown("### **System Information & Compliance Standards**")
st.json({
    "Application Name": "DashDeck.io - AI-Powered Accessibility Intelligence",
    "Version": "2.5.0 Production Edition",
    "Cognitive NLP Engine": "spaCy 3.7 + TextBlob + Textstat + Scikit-Learn",
    "Simplifier Engine": "Generative AI & Multi-Persona NLP",
    "Supported Ingestion Formats": "Pasted Text, TXT, PDF, DOCX, CSV, Excel, Image OCR, Web URLs",
    "Compliance Guidelines": "WCAG 2.2 AAA / Section 508 / Plain Writing Act Standards"
})
