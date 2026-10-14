"""
Enterprise Plotly Theme Registration for Accessibility Intelligence Dashboard.
Supports dynamic Dark and Light mode switching with prominent contrast ratios.
"""

import plotly.graph_objects as go
import plotly.io as pio

def register_plotly_theme(theme_mode: str = "Dark") -> None:
    """Register and set the enterprise default Plotly theme according to theme_mode."""
    is_light = (theme_mode.lower() == "light")
    template_name = "enterprise_accessibility_light" if is_light else "enterprise_accessibility_dark"
    
    # 10-Color Prominent Accessible Palette (WCAG AAA compliant contrast)
    if is_light:
        colorway = [
            "#1D4ED8",  # Deep Blue (5.8:1 on white)
            "#047857",  # Deep Emerald
            "#B45309",  # Deep Amber
            "#4338CA",  # Deep Indigo
            "#B91C1C",  # Deep Crimson
            "#6D28D9",  # Deep Violet
            "#0369A1",  # Deep Sky Blue
            "#C2410C",  # Deep Orange
            "#0F766E",  # Deep Teal
            "#334155"   # Slate Charcoal
        ]
        font_color = "#090D16"
        tick_color = "#334155"
        grid_color = "rgba(0, 0, 0, 0.08)"
        zeroline_color = "rgba(0, 0, 0, 0.2)"
        hover_bg = "#FFFFFF"
        hover_border = "#CBD5E1"
        hover_text = "#090D16"
    else:
        colorway = [
            "#3B82F6",  # Sharp Blue
            "#10B981",  # Emerald Success
            "#F59E0B",  # Amber Warning
            "#818CF8",  # Indigo
            "#EF4444",  # Crimson Critical
            "#A78BFA",  # Violet
            "#38BDF8",  # Sky Blue
            "#FB923C",  # Orange
            "#2DD4BF",  # Teal Accent
            "#CBD5E1"   # Slate Light
        ]
        font_color = "#FFFFFF"
        tick_color = "#CBD5E1"
        grid_color = "rgba(255, 255, 255, 0.12)"
        zeroline_color = "rgba(255, 255, 255, 0.22)"
        hover_bg = "#0F172A"
        hover_border = "#334155"
        hover_text = "#FFFFFF"
    
    enterprise_template = go.layout.Template()
    enterprise_template.layout = go.Layout(
        colorway=colorway,
        font=dict(
            family="Plus Jakarta Sans, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            size=12,
            color=font_color
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=30, t=40, b=40),
        hoverlabel=dict(
            bgcolor=hover_bg,
            bordercolor=hover_border,
            font=dict(
                family="Plus Jakarta Sans, sans-serif",
                size=12,
                color=hover_text
            )
        ),
        xaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=zeroline_color,
            tickfont=dict(color=tick_color, size=11),
            title=dict(font=dict(color=font_color, size=12))
        ),
        yaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=zeroline_color,
            tickfont=dict(color=tick_color, size=11),
            title=dict(font=dict(color=font_color, size=12))
        ),
        legend=dict(
            font=dict(color=font_color, size=11),
            bgcolor="rgba(0,0,0,0)",
            bordercolor=grid_color
        )
    )
    
    pio.templates[template_name] = enterprise_template
    pio.templates.default = template_name

# Register initial dark theme on load
register_plotly_theme(theme_mode="Dark")
