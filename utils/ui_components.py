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
/* Light Mode: High-Contrast Orange & White */
:root {
  --color-primary: #FF6600; /* Vibrant Blaze Orange */
  --color-secondary: #52525B; /* Slate Gray for secondary text */
  --color-bg: #F4F4F5; /* Very subtle off-white to make pure white surfaces pop */
  --color-surface: #FFFFFF; /* Pure White */
  --color-text: #000000; /* Pure Black text for maximum contrast */
  --color-border: #D4D4D8; /* Crisp gray borders */

  --color-primary-hover: #E65C00;
  --color-primary-active: #CC5200;
  --color-primary-muted: rgba(255, 102, 0, 0.12);
  --color-primary-border: #FF6600;
  --color-on-primary: #FFFFFF;

  --color-background: #F4F4F5;
  --color-surface-hover: #FAFAFA;
  --color-card: #FFFFFF;
  --color-card-hover: #FAFAFA;
  --color-card-border: #D4D4D8;
  --color-sidebar: #FFFFFF;
  --color-sidebar-border: #D4D4D8;

  --color-foreground: #000000;
  --color-foreground-muted: #52525B;
  --color-foreground-subtle: #71717A;
  --color-border-subtle: rgba(0, 0, 0, 0.14);

  --color-ring: #FF6600;

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

/* 1. App Canvas & Containers in Light Mode */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
  background-color: #F4F4F5 !important;
  color: #000000 !important;
}

/* 2. Global Text & Markdown in Light Mode - Solid Black */
.stApp p,
.stApp span,
.stApp li,
.stApp div,
.stApp label,
.stApp strong,
.stApp b,
.stApp em,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] div,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {
  color: #000000 !important;
}

/* 3. Global Headings in Light Mode - Solid Black */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6 {
  color: #000000 !important;
  font-weight: 800 !important;
}

/* 4. Streamlit Sidebar in Light Mode - White Background & Solid Black Text */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
  background-color: #FFFFFF !important;
  color: #000000 !important;
  border-right: 1.5px solid #D4D4D8 !important;
}

[data-testid="stSidebar"] hr {
  border-color: #D4D4D8 !important;
}

/* Sidebar Navigation Items & Page Links */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNav"] * {
  color: #000000 !important;
}

[data-testid="stSidebarNav"] li a {
  color: #000000 !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  background-color: transparent !important;
}

[data-testid="stSidebarNav"] li a:hover {
  background-color: #F4F4F5 !important;
  color: #FF6600 !important;
}

[data-testid="stSidebarNav"] li a span {
  color: #000000 !important;
  font-weight: 600 !important;
}

[data-testid="stSidebarNav"] li a[aria-current="page"] {
  background-color: rgba(255, 102, 0, 0.12) !important;
  color: #FF6600 !important;
  font-weight: 800 !important;
}

[data-testid="stSidebarNav"] li a[aria-current="page"] span {
  color: #FF6600 !important;
  font-weight: 800 !important;
}

/* Sidebar Brand, Captions & User Content */
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] * {
  color: #000000 !important;
}

[data-testid="stSidebar"] .sidebar-title {
  color: #000000 !important;
  font-weight: 800 !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] small {
  color: #52525B !important;
  font-weight: 600 !important;
}

[data-testid="stCaptionContainer"] p,
.stCaption {
  color: #52525B !important;
}

/* 5. Form Widgets & Input Controls */
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
  color: #000000 !important;
  font-weight: 600 !important;
}

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
  background-color: #FFFFFF !important;
  color: #000000 !important;
  border: 1.5px solid #D4D4D8 !important;
}

[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
  border-color: #FF6600 !important;
}

/* BaseWeb Selectbox / MultiSelect in Light Mode */
[data-baseweb="select"] * {
  color: #000000 !important;
}

div[data-baseweb="select"] > div {
  background-color: #FFFFFF !important;
  border: 1.5px solid #D4D4D8 !important;
}

[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] * {
  background-color: #FFFFFF !important;
  color: #000000 !important;
}

/* 6. Buttons in Light Mode */
button[kind="secondary"],
.stButton > button[kind="secondary"] {
  background-color: #FFFFFF !important;
  color: #000000 !important;
  border: 1.5px solid #D4D4D8 !important;
  font-weight: 600 !important;
}

button[kind="secondary"] p,
.stButton > button[kind="secondary"] p,
button[kind="secondary"] span,
.stButton > button[kind="secondary"] span {
  color: #000000 !important;
}

button[kind="secondary"]:hover,
.stButton > button[kind="secondary"]:hover {
  background-color: #FAFAFA !important;
  border-color: #FF6600 !important;
  color: #FF6600 !important;
}

button[kind="primary"],
.stButton > button[kind="primary"] {
  background-color: #FF6600 !important;
  color: #FFFFFF !important;
  border: none !important;
  font-weight: 700 !important;
}

button[kind="primary"] p,
.stButton > button[kind="primary"] p,
button[kind="primary"] span,
.stButton > button[kind="primary"] span {
  color: #FFFFFF !important;
}

/* 7. Radio & Checkboxes */
[data-testid="stRadio"] label,
[data-testid="stRadio"] p,
[data-testid="stRadio"] span,
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] span,
[data-testid="stCheckbox"] p {
  color: #000000 !important;
  font-weight: 500 !important;
}

/* 8. Expanders */
[data-testid="stExpander"] {
  background-color: #FFFFFF !important;
  border: 1.5px solid #D4D4D8 !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
  color: #000000 !important;
  font-weight: 700 !important;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"],
[data-testid="stExpander"] [data-testid="stExpanderDetails"] * {
  color: #000000 !important;
}

/* 9. File Uploader */
[data-testid="stFileUploader"] {
  background-color: #FFFFFF !important;
  border: 2px dashed #D4D4D8 !important;
}

[data-testid="stFileUploader"] * {
  color: #000000 !important;
}

/* 10. Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  border-bottom: 2px solid #D4D4D8 !important;
}

[data-testid="stTabs"] [data-baseweb="tab"],
[data-testid="stTabs"] [data-baseweb="tab"] p,
[data-testid="stTabs"] [data-baseweb="tab"] span {
  color: #52525B !important;
  font-weight: 600 !important;
}

[data-testid="stTabs"] [aria-selected="true"],
[data-testid="stTabs"] [aria-selected="true"] p,
[data-testid="stTabs"] [aria-selected="true"] span {
  color: #FF6600 !important;
  border-bottom: 2.5px solid #FF6600 !important;
  font-weight: 800 !important;
}

/* 11. Header Banner */
.header-banner {
  background: #FFFFFF !important;
  border: 1.5px solid #D4D4D8 !important;
}

.header-title {
  color: #000000 !important;
}

.header-desc {
  color: #52525B !important;
}

/* 12. Feature Cards (Bento Grid) */
.feature-card {
  background: #FFFFFF !important;
  border: 1.5px solid #D4D4D8 !important;
}

.feature-card-title {
  color: #000000 !important;
  font-weight: 800 !important;
}

.feature-card-desc {
  color: #52525B !important;
}

/* 13. KPI Cards */
.kpi-card {
  background: #FFFFFF !important;
  border: 1.5px solid #D4D4D8 !important;
}

.kpi-title {
  color: #000000 !important;
  font-weight: 700 !important;
}

.kpi-subtitle {
  color: #52525B !important;
  font-weight: 500 !important;
}

/* 14. Issue Cards & Structured Points */
.issue-card {
  background: #FFFFFF !important;
  border-color: #D4D4D8 !important;
}

.issue-card-header {
  border-bottom-color: #E4E4E7 !important;
}

.issue-card-title {
  color: #000000 !important;
  font-weight: 800 !important;
}

.issue-card-category {
  background: #F4F4F5 !important;
  color: #000000 !important;
  border-color: #D4D4D8 !important;
}

.issue-point-item {
  background: #FAFAFA !important;
  border-color: #D4D4D8 !important;
}

.issue-point-tag-issue {
  background: #FEE2E2 !important;
  color: #991B1B !important;
  border-color: #DC2626 !important;
}

.issue-point-tag-evidence {
  background: #FFF7ED !important;
  color: #9A3412 !important;
  border-color: #EA580C !important;
}

.issue-point-tag-recommendation {
  background: #D1FAE5 !important;
  color: #065F46 !important;
  border-color: #059669 !important;
}

.issue-point-content,
.issue-point-content * {
  color: #000000 !important;
}

.issue-point-snippet {
  background: #F4F4F5 !important;
  color: #000000 !important;
  border: 1px solid #D4D4D8 !important;
  border-left: 3px solid #FF6600 !important;
}

/* 15. Tables & Dataframes */
[data-testid="stDataFrame"] *,
[data-testid="stTable"] * {
  color: #000000 !important;
}
</style>
"""

# High-Contrast Dynamic Dark Theme Overrides
DARK_THEME_CSS = """
<style>
/* Dark Mode: High-Contrast Orange & Black (Enhanced High-Visibility Text) */
:root {
  --color-primary: #FF7A00; /* Vibrant Orange Glow */
  --color-secondary: #E4E4E7; /* Crisp Light Gray for secondary text (13:1 contrast on black) */
  --color-bg: #000000; /* Pitch Black */
  --color-surface: #121212; /* Near-black for cards */
  --color-text: #FFFFFF; /* Pure White text */
  --color-border: #27272A; /* Subtle dark borders */

  --color-primary-hover: #FF8C1A;
  --color-primary-active: #E66E00;
  --color-primary-muted: rgba(255, 122, 0, 0.18);
  --color-primary-border: #FF7A00;
  --color-on-primary: #FFFFFF;

  --color-background: #000000;
  --color-surface-hover: #1A1A1A;
  --color-card: #121212;
  --color-card-hover: #1A1A1A;
  --color-card-border: #27272A;
  --color-sidebar: #121212;
  --color-sidebar-border: #27272A;

  --color-foreground: #FFFFFF;
  --color-foreground-muted: #E4E4E7;
  --color-foreground-subtle: #D4D4D8;
  --color-border-subtle: rgba(255, 255, 255, 0.16);

  --color-ring: #FF7A00;

  --color-success: #10B981;
  --color-success-bg: rgba(16, 185, 129, 0.18);
  --color-success-border: #10B981;
  --color-on-success: #6EE7B7;

  --color-warning: #F59E0B;
  --color-warning-bg: rgba(245, 158, 11, 0.18);
  --color-warning-border: #F59E0B;
  --color-on-warning: #FDE047;

  --color-critical: #EF4444;
  --color-critical-bg: rgba(239, 68, 68, 0.20);
  --color-critical-border: #EF4444;
  --color-on-critical: #FCA5A5;

  --color-info: #0EA5E9;
  --color-info-bg: rgba(14, 165, 233, 0.18);
  --color-info-border: #0EA5E9;
  --color-on-info: #7DD3FC;
}

/* 1. Canvas & App View in Dark Mode */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
  background-color: #000000 !important;
  color: #FFFFFF !important;
}

/* 2. Global Headings in Dark Mode - Solid High-Visibility Pure White */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6 {
  color: #FFFFFF !important;
  font-weight: 800 !important;
}

/* 3. Global Text, Paragraphs, Lists, Labels in Dark Mode - Crisp White */
.stApp p,
.stApp span,
.stApp li,
.stApp label,
.stApp div,
.stApp strong,
.stApp b,
.stApp em,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] div,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {
  color: #F4F4F5 !important;
}

/* 4. Streamlit Sidebar in Dark Mode - Crisp High Visibility */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
  background-color: #121212 !important;
  border-right: 1.5px solid #27272A !important;
  color: #FFFFFF !important;
}

[data-testid="stSidebar"] hr {
  border-color: #27272A !important;
}

/* Sidebar Navigation Items, Section Headers & Page Links in Dark Mode */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNav"] *,
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavItems"] * {
  color: #FFFFFF !important;
}

[data-testid="stSidebarNav"] [data-testid="stSidebarNavSeparator"],
[data-testid="stSidebarNav"] header,
[data-testid="stSidebarNav"] div:first-child {
  color: #E4E4E7 !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
}

[data-testid="stSidebarNav"] ul li a,
[data-testid="stSidebarNav"] li a,
[data-testid="stSidebarNav"] a {
  color: #FFFFFF !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  background-color: transparent !important;
  opacity: 1 !important;
}

[data-testid="stSidebarNav"] ul li a span,
[data-testid="stSidebarNav"] li a span,
[data-testid="stSidebarNav"] a span {
  color: #FFFFFF !important;
  font-weight: 600 !important;
  opacity: 1 !important;
}

[data-testid="stSidebarNav"] ul li a:hover,
[data-testid="stSidebarNav"] li a:hover,
[data-testid="stSidebarNav"] a:hover {
  background-color: #1F1F23 !important;
  color: #FF7A00 !important;
}

[data-testid="stSidebarNav"] ul li a:hover span,
[data-testid="stSidebarNav"] li a:hover span,
[data-testid="stSidebarNav"] a:hover span {
  color: #FF7A00 !important;
}

/* Active / Current Page Navigation Item */
[data-testid="stSidebarNav"] ul li a[aria-current="page"],
[data-testid="stSidebarNav"] li a[aria-current="page"],
[data-testid="stSidebarNav"] a[aria-current="page"] {
  background-color: rgba(255, 122, 0, 0.18) !important;
  border-left: 3.5px solid #FF7A00 !important;
  color: #FF7A00 !important;
  font-weight: 800 !important;
}

[data-testid="stSidebarNav"] ul li a[aria-current="page"] span,
[data-testid="stSidebarNav"] li a[aria-current="page"] span,
[data-testid="stSidebarNav"] a[aria-current="page"] span {
  color: #FF7A00 !important;
  font-weight: 800 !important;
}

/* Sidebar Brand, Captions & User Content */
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] * {
  color: #FFFFFF !important;
}

[data-testid="stSidebar"] .sidebar-title {
  color: #FFFFFF !important;
  font-weight: 800 !important;
}

.sidebar-logo {
  background: #FF7A00 !important;
  color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] small {
  color: #E4E4E7 !important;
  font-weight: 600 !important;
  opacity: 1 !important;
}

[data-testid="stCaptionContainer"] p,
.stCaption {
  color: #D4D4D8 !important;
  font-weight: 500 !important;
}

/* 5. Form Widgets & Input Controls in Dark Mode */
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
  color: #FFFFFF !important;
  font-weight: 700 !important;
}

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
  background-color: #121212 !important;
  color: #FFFFFF !important;
  border: 1.5px solid #3F3F46 !important;
}

[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
  border-color: #FF7A00 !important;
  box-shadow: 0 0 0 2px rgba(255, 122, 0, 0.3) !important;
}

[data-baseweb="select"] *,
[data-baseweb="popover"] *,
[data-baseweb="menu"] * {
  color: #FFFFFF !important;
  background-color: #121212 !important;
}

div[data-baseweb="select"] > div {
  background-color: #121212 !important;
  border: 1.5px solid #3F3F46 !important;
}

/* Radio & Checkbox Labels */
[data-testid="stRadio"] label,
[data-testid="stRadio"] p,
[data-testid="stRadio"] span,
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] span,
[data-testid="stCheckbox"] p {
  color: #FFFFFF !important;
  font-weight: 600 !important;
}

/* 6. Buttons in Dark Mode */
button[kind="secondary"], .stButton > button[kind="secondary"] {
  background-color: #18181B !important;
  color: #FFFFFF !important;
  border: 1.5px solid #3F3F46 !important;
  font-weight: 700 !important;
}

button[kind="secondary"] p,
.stButton > button[kind="secondary"] p,
button[kind="secondary"] span,
.stButton > button[kind="secondary"] span {
  color: #FFFFFF !important;
}

button[kind="secondary"]:hover, .stButton > button[kind="secondary"]:hover {
  background-color: #27272A !important;
  border-color: #FF7A00 !important;
  color: #FF7A00 !important;
}

button[kind="secondary"]:hover p,
.stButton > button[kind="secondary"]:hover p,
button[kind="secondary"]:hover span,
.stButton > button[kind="secondary"]:hover span {
  color: #FF7A00 !important;
}

button[kind="primary"], .stButton > button[kind="primary"] {
  background-color: #FF7A00 !important;
  color: #000000 !important;
  border: none !important;
  font-weight: 800 !important;
}

button[kind="primary"] p,
.stButton > button[kind="primary"] p,
button[kind="primary"] span,
.stButton > button[kind="primary"] span {
  color: #000000 !important;
  font-weight: 800 !important;
}

/* 7. Expanders in Dark Mode */
[data-testid="stExpander"] {
  background-color: #121212 !important;
  border: 1.5px solid #27272A !important;
  color: #FFFFFF !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
  color: #FFFFFF !important;
  font-weight: 700 !important;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"],
[data-testid="stExpander"] [data-testid="stExpanderDetails"] * {
  color: #F4F4F5 !important;
}

/* 8. File Uploader in Dark Mode */
[data-testid="stFileUploader"] {
  background-color: #121212 !important;
  border: 2px dashed #3F3F46 !important;
}

[data-testid="stFileUploader"] * {
  color: #FFFFFF !important;
}

/* 9. Tabs in Dark Mode */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  border-bottom: 2px solid #27272A !important;
}

[data-testid="stTabs"] [data-baseweb="tab"],
[data-testid="stTabs"] [data-baseweb="tab"] p,
[data-testid="stTabs"] [data-baseweb="tab"] span {
  color: #D4D4D8 !important;
  font-weight: 600 !important;
}

[data-testid="stTabs"] [aria-selected="true"],
[data-testid="stTabs"] [aria-selected="true"] p,
[data-testid="stTabs"] [aria-selected="true"] span {
  color: #FF7A00 !important;
  border-bottom: 2.5px solid #FF7A00 !important;
  font-weight: 800 !important;
}

/* 10. Header Banner & Bento Cards in Dark Mode */
.header-banner {
  background: #121212 !important;
  border: 1.5px solid #27272A !important;
}

.header-title {
  color: #FFFFFF !important;
  font-weight: 800 !important;
}

.header-desc {
  color: #D4D4D8 !important;
  font-weight: 500 !important;
}

.feature-card {
  background: #121212 !important;
  border: 1.5px solid #27272A !important;
}

.feature-card-title {
  color: #FFFFFF !important;
  font-weight: 800 !important;
}

.feature-card-desc {
  color: #D4D4D8 !important;
}

/* 11. KPI Cards in Dark Mode */
.kpi-card {
  background: #121212 !important;
  border: 1.5px solid #27272A !important;
}

.kpi-title {
  color: #FFFFFF !important;
  font-weight: 700 !important;
}

.kpi-value {
  color: #FFFFFF !important;
  font-weight: 800 !important;
}

.kpi-subtitle {
  color: #D4D4D8 !important;
  font-weight: 500 !important;
}

/* 12. Issue Cards & Structured Points in Dark Mode */
.issue-card {
  background: #121212 !important;
  border-color: #27272A !important;
}

.issue-card-title {
  color: #FFFFFF !important;
  font-weight: 800 !important;
}

.issue-point-item {
  background: #18181B !important;
  border-color: #27272A !important;
}

.issue-point-content,
.issue-point-content * {
  color: #F4F4F5 !important;
}

.issue-point-snippet {
  background: #09090B !important;
  color: #FFFFFF !important;
  border: 1px solid #3F3F46 !important;
  border-left: 3.5px solid #FF7A00 !important;
}

/* 13. Tables & Dataframes in Dark Mode */
[data-testid="stDataFrame"] *,
[data-testid="stTable"] * {
  color: #FFFFFF !important;
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

def render_sidebar_brand() -> None:
    """Render the official DashDeck.io brand mark and title in the sidebar."""
    st.markdown("""
    <div class="sidebar-brand-wrap">
        <div class="sidebar-logo">
            <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/>
            </svg>
        </div>
        <div class="sidebar-title">DashDeck<span style="color: #FF7A00;">.io</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("AI Accessibility & Cognitive Inclusion")

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

        if st.session_state.get("current_analysis") is not None:
            active_name = st.session_state.get("doc_name", "Copy")
            st.markdown(f"""
            <div style="margin-top: 14px; margin-bottom: 4px; padding: 8px 10px; background: var(--color-background-elevated); border: 1px solid var(--color-border); border-radius: var(--radius-md);">
                <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-foreground-muted); margin-bottom: 2px;">Active Analysis</div>
                <div style="font-size: 0.8rem; font-weight: 600; color: var(--color-foreground); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">📄 {html.escape(active_name)}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 Start Fresh", key="sidebar_reset_active_analysis_btn", type="secondary", use_container_width=True):
                clear_active_session()
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
        
    # Render brand header and theme switcher in sidebar
    if render_sidebar_toggle:
        with st.sidebar:
            render_sidebar_brand()
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


def clear_active_session() -> None:
    """Clear all active analysis and document data from session state so the session starts fresh."""
    keys_to_clear = [
        "current_analysis", "input_text", "doc_name", "file_type",
        "uploaded_doc_text", "uploaded_doc_name", "uploaded_doc_type",
        "uploaded_data_text", "uploaded_data_name", "uploaded_data_type",
        "uploaded_img_text", "uploaded_img_name", "uploaded_img_type",
        "sample_loaded_text", "sample_loaded_name", "sample_loaded_type",
        "url_extracted", "url_title"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.current_analysis = None
    st.session_state.input_text = ""
    st.session_state.doc_name = "Untitled Copy"
    st.session_state.file_type = "Pasted Text"


def ensure_active_analysis():
    """Return the active current_analysis and input_text from session state.
    
    Does NOT auto-restore from database history so that every new session
    or page refresh starts completely fresh without considering the last uploaded file.
    """
    current_res = st.session_state.get("current_analysis")
    input_text = st.session_state.get("input_text", "")
    return current_res, input_text

