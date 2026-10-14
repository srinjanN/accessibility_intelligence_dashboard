"""
Page 2: Deep Linguistic & NLP Pipeline Breakdown
"""

import html
import streamlit as st
import pandas as pd
from utils.ui_components import inject_custom_css, render_header_banner
from utils.nlp_engine import (
    get_tokens, get_sentences, extract_named_entities,
    extract_keywords_tfidf, extract_ngrams, extract_topics
)

inject_custom_css()

render_header_banner(
    title="Linguistic & NLP Processing Pipeline",
    subtitle="Deep tokenisation, POS tagging, Named Entity Recognition (NER), TF-IDF keyword extraction, N-grams, and topic modeling."
)

current_res = st.session_state.get("current_analysis")
input_text = st.session_state.get("input_text", "")

if not input_text or current_res is None:
    st.info("💡 No active document found. Please run an analysis on the **Dashboard** page first!")
    if st.button("👉 Go to Dashboard"):
        st.switch_page("pages/1_📊_Dashboard.py")
    st.stop()

st.markdown(f"### 🔍 **Linguistic Insights for: `{st.session_state.get('doc_name', 'Copy')}`**")

tab_tokens, tab_ner, tab_keywords, tab_ngrams, tab_topics = st.tabs([
    "🏷️ POS Tokens & Syntax", "🏷️ Named Entities (NER)", "🔑 TF-IDF Keywords",
    "🔤 N-Grams", "🧠 Topic Modeling"
])

with tab_tokens:
    st.markdown("#### **Tokenization, Lemmatization, & Part-of-Speech (POS) Tags**")
    tokens_data = get_tokens(input_text)
    if tokens_data:
        df_tokens = pd.DataFrame(tokens_data)
        
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            st.dataframe(df_tokens, height=350, use_container_width=True)
        with col_t2:
            st.markdown("##### **POS Distribution**")
            pos_counts = df_tokens["pos"].value_counts()
            st.dataframe(pos_counts, use_container_width=True)
    else:
        st.write("No tokens extracted.")

with tab_ner:
    st.markdown("#### **Named Entity Recognition (NER)**")
    entities = extract_named_entities(input_text)
    if entities:
        df_ner = pd.DataFrame(entities)
        st.dataframe(df_ner, use_container_width=True)
        
        st.markdown("##### **Entities Visual Badges:**")
        badge_htmls = []
        for ent in entities:
            badge_htmls.append(
                f'<span style="background: rgba(99, 102, 241, 0.2); border: 1px solid rgba(99, 102, 241, 0.4); padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; margin-right: 8px; display: inline-block; margin-bottom: 8px;">'
                f'{ent["text"]} <small style="color: #a855f7;">({ent["label"]})</small></span>'
            )
        st.markdown("".join(badge_htmls), unsafe_allow_html=True)
    else:
        st.info("No distinct named entities detected in text.")

with tab_keywords:
    st.markdown("#### **TF-IDF Top Extracted Keywords**")
    keywords = extract_keywords_tfidf(input_text, top_k=15)
    if keywords:
        df_kw = pd.DataFrame(keywords, columns=["Keyword", "TF-IDF Score"])
        st.dataframe(df_kw, use_container_width=True)

with tab_ngrams:
    st.markdown("#### **N-Gram Frequency Analysis**")
    col_n1, col_n2, col_n3 = st.columns(3)
    
    with col_n1:
        st.markdown("##### **Unigrams**")
        uni = extract_ngrams(input_text, n=1, top_k=8)
        if uni:
            st.dataframe(pd.DataFrame(uni, columns=["Unigram", "Count"]), use_container_width=True)
            
    with col_n2:
        st.markdown("##### **Bigrams**")
        bi = extract_ngrams(input_text, n=2, top_k=8)
        if bi:
            st.dataframe(pd.DataFrame(bi, columns=["Bigram", "Count"]), use_container_width=True)
            
    with col_n3:
        st.markdown("##### **Trigrams**")
        tri = extract_ngrams(input_text, n=3, top_k=8)
        if tri:
            st.dataframe(pd.DataFrame(tri, columns=["Trigram", "Count"]), use_container_width=True)

with tab_topics:
    st.markdown("#### **Semantic Topic Extraction & Clustering**")
    topics = extract_topics(input_text, num_topics=3)
    for top in topics:
        words_str = html.escape(', '.join(top['words']))
        topic_html = (
            f'<div style="background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;">'
            f'<h5 style="color: var(--color-primary); margin: 0 0 6px 0; font-weight: 700;">Topic Cluster #{top["topic_id"]}</h5>'
            f'<p style="margin: 0; color: var(--color-foreground);"><strong>Associated Keywords:</strong> {words_str}</p>'
            f'</div>'
        )
        st.markdown(topic_html, unsafe_allow_html=True)
