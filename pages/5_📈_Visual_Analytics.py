"""
Page 5: Visual Analytics & Interactive Plotly Charts
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx

from utils.ui_components import inject_custom_css, render_header_banner, ensure_active_analysis
from utils.nlp_engine import (
    get_sentences, get_tokens, extract_keywords_tfidf,
    build_cooccurrence_graph, extract_topics
)

inject_custom_css()

render_header_banner(
    title="Visual Analytics & Interactive Insights",
    subtitle="Interactive Plotly charts including accessibility gauge, sentence length histogram, word distribution, co-occurrence network, and issue treemaps."
)

current_res, input_text = ensure_active_analysis()

if not input_text or current_res is None:
    st.info("💡 No active document found. Please run an analysis on the **Dashboard** page first!")
    if st.button("👉 Go to Dashboard"):
        st.switch_page("pages/1_📊_Dashboard.py")
    st.stop()

# 1. Gauge Chart for Accessibility & Readability
st.markdown("### ⏱️ **Accessibility Speedometer Gauge**")
score = float(current_res.get("accessibility_score", 0.0))

bar_color = "#FF7A00" if score < 60 else ("#10B981" if score >= 80 else "#F59E0B")

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    number={'suffix': " / 100", 'font': {'size': 38, 'color': "#FFFFFF"}},
    title={'text': f"Accessibility Score: {st.session_state.get('doc_name', 'Document')}", 'font': {'size': 18, 'color': "#E4E4E7"}},
    gauge={
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#71717A"},
        'bar': {'color': bar_color, 'thickness': 0.35},
        'bgcolor': "rgba(255,255,255,0.06)",
        'bordercolor': "rgba(255,255,255,0.2)",
        'steps': [
            {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.4)'},
            {'range': [50, 75], 'color': 'rgba(234, 179, 8, 0.4)'},
            {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.4)'}
        ],
        'threshold': {
            'line': {'color': "#FF7A00", 'width': 5},
            'thickness': 0.75,
            'value': score
        }
    }
))
fig_gauge.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FFFFFF"),
    height=290,
    margin=dict(t=50, b=20, l=30, r=30)
)
st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# 2. Row 1: Sentence Length Histogram & POS Distribution
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown("#### 📏 **Sentence Length Histogram**")
    sentences = get_sentences(input_text)
    sent_lengths = [len(s.split()) for s in sentences]
    
    if sent_lengths:
        df_sent = pd.DataFrame({"Words_Per_Sentence": sent_lengths})
        fig_hist = px.histogram(
            df_sent,
            x="Words_Per_Sentence",
            nbins=12,
            title="Distribution of Sentence Lengths",
            color_discrete_sequence=["#818cf8"]
        )
        # Add threshold vertical line
        max_len_thresh = st.session_state.get("custom_thresholds", {}).get("max_sentence_length", 20)
        fig_hist.add_vline(x=max_len_thresh, line_dash="dash", line_color="#ef4444", annotation_text="Max Threshold")
        
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc")
        )
        st.plotly_chart(fig_hist, use_container_width=True)

with col_c2:
    st.markdown("#### 🏷️ **Part-of-Speech (POS) Distribution**")
    tokens_data = get_tokens(input_text)
    if tokens_data:
        pos_counts = pd.DataFrame(tokens_data)["pos"].value_counts().reset_index()
        pos_counts.columns = ["POS Tag", "Count"]
        
        fig_pos = px.pie(
            pos_counts,
            names="POS Tag",
            values="Count",
            title="Syntactic Word Categories",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pos.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc")
        )
        st.plotly_chart(fig_pos, use_container_width=True)

st.divider()

# 3. Row 2: Treemap of Violations & Keyword Frequency
col_c3, col_c4 = st.columns(2)

with col_c3:
    st.markdown("#### 🗺️ **Violations Treemap by Category & Severity**")
    issues = current_res.get("issues", [])
    if issues:
        df_iss = pd.DataFrame(issues)
        df_iss["Count"] = 1
        fig_tree = px.treemap(
            df_iss,
            path=["category", "severity", "title"],
            values="Count",
            color="severity",
            color_discrete_map={"Critical": "#ef4444", "High": "#f97316", "Medium": "#eab308", "Low": "#3b82f6"},
            title="Hierarchical Issues Breakdown"
        )
        fig_tree.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc")
        )
        st.plotly_chart(fig_tree, use_container_width=True)
    else:
        st.info("No violations to render in Treemap!")

with col_c4:
    st.markdown("#### 🔑 **Top Keyword TF-IDF Scores**")
    kw_data = extract_keywords_tfidf(input_text, top_k=10)
    if kw_data:
        df_kw = pd.DataFrame(kw_data, columns=["Keyword", "Score"])
        fig_kw = px.bar(
            df_kw,
            x="Score",
            y="Keyword",
            orientation="h",
            title="Key Information Density",
            color="Score",
            color_continuous_scale="Purples"
        )
        fig_kw.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc")
        )
        st.plotly_chart(fig_kw, use_container_width=True)

st.divider()

# 4. NetworkX Co-occurrence Graph (Plotly node network)
st.markdown("### 🕸️ **Word Co-Occurrence Network Graph**")
G = build_cooccurrence_graph(input_text, top_n_words=12)

if G.number_of_nodes() > 0:
    pos = nx.spring_layout(G, k=0.5, seed=42)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='rgba(255,255,255,0.2)'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node} ({G.nodes[node].get('size', 1)})")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[n for n in G.nodes()],
        textposition="top center",
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            color=[G.degree(n) for n in G.nodes()],
            size=22,
            line_width=2
        )
    )

    fig_net = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='Co-occurring Term Relationships',
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#f8fafc")
                ))
    st.plotly_chart(fig_net, use_container_width=True)
else:
    st.info("Insufficient terms to build network graph.")
