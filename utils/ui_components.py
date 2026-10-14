"""
Enterprise UI Components and Theme Styling Utilities for Streamlit.
Adheres strictly to MASTER.md design tokens, prominent contrast ratios,
and provides dynamic Dark/Light theme switching capabilities.
"""

import os
import html
import streamlit as st
from typing import Dict, Any, List, Optional

# Crisp inline Lucide-style SVG icons (Accessible: aria-hidden="true")
SVG_ICONS: Dict[str, str] = {
    "dashboard": '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>',
    "accessibility": '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="4" r="2"/><path d="M5 9h14"/><path d="M12 9v12"/><path d="m8 13 4 3 4-3"/></svg>',
    "readability": '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    "grade": '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
    "time": '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "voice": '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "jargon": '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a7 7 0 0 0-7 7c0 2.38 1.19 4.47 3 5.74V17a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-2.26c1.81-1.27 3-3.36 3-5.74a7 7 0 0 0-7-7z"/><path d="M9 21h6"/></svg>',
    "complexity": '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "violations": '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "critical": '<svg class="badge-svg-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    "high": '<svg class="badge-svg-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "medium": '<svg class="badge-svg-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "low": '<svg class="badge-svg-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    "recommendation": '<svg aria-hidden="true" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a7 7 0 0 0-7 7c0 2.38 1.19 4.47 3 5.74V17a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-2.26c1.81-1.27 3-3.36 3-5.74a7 7 0 0 0-7-7z"/><path d="M9 21h6"/></svg>'
}

# Mapping common legacy emojis to clean SVG icons
EMOJI_TO_SVG: Dict[str, str] = {
    "♿": SVG_ICONS["accessibility"],
    "📖": SVG_ICONS["readability"],
    "🎓": SVG_ICONS["grade"],
    "⏱️": SVG_ICONS["time"],
    "🗣️": SVG_ICONS["voice"],
    "🧠": SVG_ICONS["jargon"],
    "⚡": SVG_ICONS["complexity"],
    "🚨": SVG_ICONS["violations"],
    "📊": SVG_ICONS["dashboard"]
}

# High-Contrast Dynamic Light Theme Overrides
LIGHT_THEME_CSS = """
<style>
:root {
  --color-primary: #1D4ED8;
  --color-primary-hover: #1E40AF;
  --color-primary-active: #172554;
  --color-primary-muted: rgba(29, 78, 216, 0.12);
  --color-primary-border: #1D4ED8;
  --color-on-primary: #FFFFFF;

  --color-background: #F1F5F9;
  --color-surface: #FFFFFF;
  --color-surface-hover: #F8FAFC;
  --color-card: #FFFFFF;
  --color-card-hover: #F8FAFC;
  --color-card-border: #94A3B8;
  --color-sidebar: #FFFFFF;
  --color-sidebar-border: #CBD5E1;

  --color-foreground: #090D16;
  --color-foreground-muted: #1E293B;
  --color-foreground-subtle: #334155;
  --color-border: #CBD5E1;
  --color-border-subtle: rgba(0, 0, 0, 0.14);

  --color-critical: #DC2626;
  --color-critical-bg: #FEF2F2;
  --color-critical-border: #DC2626;
  --color-on-critical: #991B1B;

  --color-warning: #D97706;
  --color-warning-bg: #FFFBEB;
  --color-warning-border: #D97706;
  --color-on-warning: #854D0E;

  --color-success: #059669;
  --color-success-bg: #ECFDF5;
  --color-success-border: #059669;
  --color-on-success: #065F46;

  --color-info: #0284C7;
  --color-info-bg: #F0F9FF;
  --color-info-border: #0284C7;
  --color-on-info: #075985;
}

.stApp, [data-testid="stAppViewContainer"] {
  background-color: #F1F5F9 !important;
  color: #090D16 !important;
}

[data-testid="stSidebar"] {
  background-color: #FFFFFF !important;
  border-right: 1.5px solid #CBD5E1 !important;
}

[data-testid="stSidebar"] hr {
  border-color: #CBD5E1 !important;
}

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
  background-color: #FFFFFF !important;
  color: #090D16 !important;
  border: 1.5px solid #94A3B8 !important;
}

button[kind="secondary"], .stButton > button[kind="secondary"] {
  background-color: #FFFFFF !important;
  color: #090D16 !important;
  border: 1.5px solid #94A3B8 !important;
}

button[kind="secondary"]:hover, .stButton > button[kind="secondary"]:hover {
  background-color: #F8FAFC !important;
  border-color: #1D4ED8 !important;
  color: #1D4ED8 !important;
}

[data-testid="stExpander"] {
  background-color: #FFFFFF !important;
  border: 1.5px solid #CBD5E1 !important;
  color: #090D16 !important;
}

[data-testid="stFileUploader"] {
  background-color: #FFFFFF !important;
  border: 2px dashed #94A3B8 !important;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
  border-bottom: 2px solid #CBD5E1 !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
  color: #334155 !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
  color: #1D4ED8 !important;
  border-bottom: 2.5px solid #1D4ED8 !important;
  font-weight: 800 !important;
}

.issue-card {
  background: #FFFFFF !important;
  border-color: #CBD5E1 !important;
}

.issue-card-header {
  border-bottom-color: #E2E8F0 !important;
}

.issue-card-title {
  color: #090D16 !important;
}

.issue-point-item {
  background: #F8FAFC !important;
  border-color: #CBD5E1 !important;
}

.issue-point-tag-issue {
  background: #FEE2E2 !important;
  color: #991B1B !important;
  border-color: #DC2626 !important;
}

.issue-point-tag-evidence {
  background: #FEF3C7 !important;
  color: #92400E !important;
  border-color: #D97706 !important;
}

.issue-point-tag-recommendation {
  background: #D1FAE5 !important;
  color: #065F46 !important;
  border-color: #059669 !important;
}

.issue-point-content {
  color: #0F172A !important;
}

.issue-point-snippet {
  background: #F1F5F9 !important;
  color: #0F172A !important;
  border: 1px solid #CBD5E1 !important;
  border-left: 3px solid #D97706 !important;
}
</style>
"""

# High-Contrast Dynamic Dark Theme Overrides
DARK_THEME_CSS = """
<style>
:root {
  --color-primary: #3B82F6;
  --color-primary-hover: #2563EB;
  --color-primary-active: #1D4ED8;
  --color-primary-muted: rgba(59, 130, 246, 0.16);
  --color-primary-border: #3B82F6;
  --color-on-primary: #FFFFFF;

  --color-background: #080C14;
  --color-surface: #0F172A;
  --color-surface-hover: #19243C;
  --color-card: #0F172A;
  --color-card-hover: #162036;
  --color-card-border: #2B3A58;
  --color-sidebar: #0B101D;
  --color-sidebar-border: #25334E;

  --color-foreground: #FFFFFF;
  --color-foreground-muted: #CBD5E1;
  --color-foreground-subtle: #94A3B8;
  --color-border: #25334E;
  --color-border-subtle: rgba(255, 255, 255, 0.14);

  --color-success: #10B981;
  --color-success-bg: rgba(16, 185, 129, 0.16);
  --color-success-border: #10B981;
  --color-on-success: #6EE7B7;

  --color-warning: #F59E0B;
  --color-warning-bg: rgba(245, 158, 11, 0.16);
  --color-warning-border: #F59E0B;
  --color-on-warning: #FDE047;

  --color-critical: #EF4444;
  --color-critical-bg: rgba(239, 68, 68, 0.18);
  --color-critical-border: #EF4444;
  --color-on-critical: #FCA5A5;

  --color-info: #0EA5E9;
  --color-info-bg: rgba(14, 165, 233, 0.16);
  --color-info-border: #0EA5E9;
  --color-on-info: #7DD3FC;
}

.stApp, [data-testid="stAppViewContainer"] {
  background-color: #080C14 !important;
  color: #FFFFFF !important;
}

[data-testid="stSidebar"] {
  background-color: #0B101D !important;
  border-right: 1.5px solid #25334E !important;
}

[data-testid="stSidebar"] hr {
  border-color: #25334E !important;
}

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
  background-color: #0F172A !important;
  color: #FFFFFF !important;
  border: 1.5px solid #2B3A58 !important;
}

button[kind="secondary"], .stButton > button[kind="secondary"] {
  background-color: #0F172A !important;
  color: #FFFFFF !important;
  border: 1.5px solid #2B3A58 !important;
}

button[kind="secondary"]:hover, .stButton > button[kind="secondary"]:hover {
  background-color: #19243C !important;
  border-color: #3B82F6 !important;
  color: #FFFFFF !important;
}

[data-testid="stExpander"] {
  background-color: #0F172A !important;
  border: 1.5px solid #2B3A58 !important;
  color: #FFFFFF !important;
}

[data-testid="stFileUploader"] {
  background-color: #0F172A !important;
  border: 2px dashed #2B3A58 !important;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
  border-bottom: 2px solid #25334E !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
  color: #CBD5E1 !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
  color: #3B82F6 !important;
  border-bottom: 2.5px solid #3B82F6 !important;
  font-weight: 800 !important;
}
</style>
"""

def resolve_icon(icon: str, default_svg_key: str = "dashboard") -> str:
    """Resolve an icon string (emoji or SVG) to an accessible SVG icon markup."""
    if not icon:
        return SVG_ICONS.get(default_svg_key, "")
    if icon in EMOJI_TO_SVG:
        return EMOJI_TO_SVG[icon]
    if "<svg" in icon:
        return icon
    return SVG_ICONS.get(default_svg_key, "")

def render_theme_switcher() -> None:
    """Render a prominent Theme Switcher (Dark <-> Light) in the sidebar."""
    if "app_theme" not in st.session_state:
        st.session_state.app_theme = "Dark"
    
    current_theme = st.session_state.app_theme
    
    with st.sidebar:
        st.markdown("""
        <div style="margin-top: 14px; margin-bottom: 6px;">
            <span style="font-size: 0.775rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-foreground-muted);">Interface Theme</span>
        </div>
        """, unsafe_allow_html=True)
        
        theme_options = ["Dark", "Light"]
        theme_idx = 0 if current_theme == "Dark" else 1
        
        if hasattr(st, "segmented_control"):
            selected_theme = st.segmented_control(
                "Interface Theme",
                options=theme_options,
                default=current_theme,
                key="global_theme_switcher_seg",
                label_visibility="collapsed"
            )
            if selected_theme and selected_theme != current_theme:
                st.session_state.app_theme = selected_theme
                st.rerun()
        else:
            selected_theme = st.radio(
                "Interface Theme",
                options=theme_options,
                index=theme_idx,
                horizontal=True,
                key="global_theme_switcher_radio",
                label_visibility="collapsed"
            )
            if selected_theme and selected_theme != current_theme:
                st.session_state.app_theme = selected_theme
                st.rerun()

def inject_custom_css(css_file_path: str = None, render_sidebar_toggle: bool = True) -> None:
    """Inject custom CSS stylesheet, register Plotly theme, and handle theme switching."""
    if "app_theme" not in st.session_state:
        st.session_state.app_theme = "Dark"
        
    theme_mode = st.session_state.app_theme
    
    # Register Plotly theme so all visual analytics adapt cleanly to Dark / Light
    try:
        from utils.ui_theme import register_plotly_theme
        register_plotly_theme(theme_mode=theme_mode)
    except Exception:
        pass

    if css_file_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        css_file_path = os.path.join(base_dir, "assets", "style.css")
    
    if os.path.exists(css_file_path):
        with open(css_file_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    
    # Inject prominent theme-specific overrides
    if theme_mode == "Light":
        st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)
    else:
        st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
        
    # Render theme switcher in sidebar
    if render_sidebar_toggle:
        render_theme_switcher()

def render_header_banner(title: str, subtitle: str, icon: str = "♿") -> None:
    """Render an enterprise, high-contrast page header banner."""
    svg_icon = resolve_icon(icon, default_svg_key="accessibility")
    html_content = f"""
    <div class="header-banner">
        <div>
            <div class="header-title-row">
                <div class="header-icon-wrap">{svg_icon}</div>
                <h1 class="header-title">{title}</h1>
            </div>
            <p class="header-desc">{subtitle}</p>
        </div>
        <div class="header-status-pill">
            <span class="status-dot"></span>
            <span class="status-pill-text">Engine Active</span>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def render_kpi_card(title: str, value: Any, subtitle: str = "", icon: str = "📊", value_color: str = "#ffffff") -> None:
    """Render a single KPI card with monospace/tabular value and prominent contrast."""
    svg_icon = resolve_icon(icon, default_svg_key="dashboard")
    
    # Adapt default white value to active theme for prominent contrast
    theme_mode = st.session_state.get("app_theme", "Dark")
    if not value_color or value_color.lower() in ["#ffffff", "white"]:
        val_color_style = "color: #FFFFFF;" if theme_mode == "Dark" else "color: #090D16;"
    else:
        val_color_style = f"color: {value_color};"
    
    html_content = f"""
    <div class="kpi-card">
        <div class="kpi-card-header">
            <span class="kpi-title">{title}</span>
            <span class="kpi-icon-wrap">{svg_icon}</span>
        </div>
        <div class="kpi-value" style="{val_color_style}">{value}</div>
        <div class="kpi-subtitle">{subtitle}</div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def get_severity_badge_html(severity: str) -> str:
    """Get accessible HTML string for a severity badge (Icon + Text Pill)."""
    sev_lower = severity.lower() if severity else "low"
    if sev_lower == "critical":
        return f'<span class="badge-critical">{SVG_ICONS["critical"]} Critical</span>'
    elif sev_lower == "high":
        return f'<span class="badge-high">{SVG_ICONS["high"]} High</span>'
    elif sev_lower == "medium":
        return f'<span class="badge-medium">{SVG_ICONS["medium"]} Medium</span>'
    else:
        return f'<span class="badge-low">{SVG_ICONS["low"]} Low</span>'

def render_issue_card(issue: Dict[str, Any], index: int = 1) -> None:
    """Render a detailed issue card formatted as structured points with zero markup leakage."""
    severity = issue.get("severity", "Low")
    badge_html = get_severity_badge_html(severity)
    category = issue.get("category", "General")
    issue_title = issue.get("title", f"Issue #{index}")
    snippet = issue.get("snippet", "")
    explanation = issue.get("explanation", "")
    suggestion = issue.get("suggestion", "")
    confidence = issue.get("confidence", 0.95)
    
    # Safely escape all text values to prevent literal HTML parsing bugs or tag breakages
    safe_title = html.escape(str(issue_title))
    safe_category = html.escape(str(category))
    safe_explanation = html.escape(str(explanation))
    safe_snippet = html.escape(str(snippet))
    safe_suggestion = html.escape(str(suggestion))
    conf_pct = int(confidence * 100) if isinstance(confidence, (int, float)) else 95
    
    # Build structured points with zero leading indentation to guarantee no Markdown code block triggers
    parts = [
        '<div class="issue-card">',
        '<div class="issue-card-header">',
        '<div class="issue-card-title-group">',
        f'<span class="issue-card-title">#{index}. {safe_title}</span>',
        f'<span class="issue-card-category">{safe_category}</span>',
        '</div>',
        '<div style="display: flex; align-items: center; gap: 8px;">',
        badge_html,
        f'<span style="font-size: 0.775rem; color: var(--color-foreground-subtle); font-family: var(--font-mono); font-weight: 700;">Conf: {conf_pct}%</span>',
        '</div>',
        '</div>',
        '<div class="issue-points-list">',
        '<div class="issue-point-item">',
        '<span class="issue-point-tag issue-point-tag-issue">📌 Issue</span>',
        f'<div class="issue-point-content"><strong>Violation:</strong> {safe_explanation}</div>',
        '</div>'
    ]
    
    if snippet:
        parts.extend([
            '<div class="issue-point-item">',
            '<span class="issue-point-tag issue-point-tag-evidence">🔍 Evidence</span>',
            f'<div class="issue-point-content"><div class="issue-point-snippet">&ldquo;{safe_snippet}&rdquo;</div></div>',
            '</div>'
        ])
        
    if suggestion:
        parts.extend([
            '<div class="issue-point-item">',
            '<span class="issue-point-tag issue-point-tag-recommendation">💡 Action</span>',
            f'<div class="issue-point-content"><strong>Actionable Recommendation:</strong> {safe_suggestion}</div>',
            '</div>'
        ])
        
    parts.extend([
        '</div>',
        '</div>'
    ])
    
    # Single contiguous string with zero leading indentation
    card_html = "".join(parts)
    st.markdown(card_html, unsafe_allow_html=True)

def render_empty_state(title: str = "No Active Document", description: str = "Upload or paste text in the Dashboard to begin evaluation.") -> None:
    """Render an accessible, high-finish empty state without markup leakage."""
    icon_svg = SVG_ICONS["accessibility"]
    safe_title = html.escape(str(title))
    safe_desc = html.escape(str(description))
    html_content = (
        f'<div class="empty-state-box">'
        f'<div class="empty-state-icon-wrap">{icon_svg}</div>'
        f'<div class="empty-state-title">{safe_title}</div>'
        f'<div class="empty-state-desc">{safe_desc}</div>'
        f'</div>'
    )
    st.markdown(html_content, unsafe_allow_html=True)

