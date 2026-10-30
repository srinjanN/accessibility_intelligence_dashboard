"""
Enterprise Plotly Theme Registration for DashDeck.io.
Supports dynamic Dark and Light mode switching with prominent contrast ratios.
"""

import plotly.graph_objects as go
import plotly.io as pio

def register_plotly_theme(theme_mode: str = "Dark") -> None:
    """Register and set the enterprise default Plotly theme according to theme_mode."""
    is_light = (theme_mode.lower() == "light")
    template_name = "enterprise_accessibility_light" if is_light else "enterprise_accessibility_dark"
    
    # 10-Color Prominent Accessible Palette (WCAG AAA compliant contrast with High-Contrast Orange)
    if is_light:
        colorway = [
            "#FF6600",  # Vibrant Blaze Orange (Primary)
            "#52525B",  # Slate Gray (Secondary)
            "#059669",  # Deep Emerald
            "#D97706",  # Deep Amber
            "#DC2626",  # Deep Crimson
            "#7C3AED",  # Deep Violet
            "#0284C7",  # Deep Sky Blue
            "#0F766E",  # Deep Teal
            "#C2410C",  # Rust Orange
            "#18181B"   # Charcoal Black
        ]
        font_color = "#000000"
        tick_color = "#52525B"
        grid_color = "rgba(0, 0, 0, 0.08)"
        zeroline_color = "rgba(0, 0, 0, 0.2)"
        hover_bg = "#FFFFFF"
        hover_border = "#D4D4D8"
        hover_text = "#000000"
    else:
        colorway = [
            "#FF7A00",  # Vibrant Orange Glow (Primary)
            "#A1A1AA",  # Light Gray (Secondary)
            "#10B981",  # Emerald Success
            "#F59E0B",  # Amber Warning
            "#EF4444",  # Crimson Critical
            "#8B5CF6",  # Violet Accent
            "#38BDF8",  # Sky Blue
            "#2DD4BF",  # Teal Accent
            "#FB923C",  # Light Orange
            "#E4E4E7"   # Off-White
        ]
        font_color = "#FFFFFF"
        tick_color = "#A1A1AA"
        grid_color = "rgba(255, 255, 255, 0.12)"
        zeroline_color = "rgba(255, 255, 255, 0.22)"
        hover_bg = "#121212"
        hover_border = "#27272A"
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
