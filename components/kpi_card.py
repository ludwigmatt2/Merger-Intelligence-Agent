"""KPI Card component — glassmorphism card for a single bank metric. Implemented in Phase 3."""
import streamlit as st

def render_kpi_card(label: str, value, unit: str = "", accent_color: str = "#00D4FF"):
    """Render a single KPI metric card with glassmorphism style."""
    st.markdown(
        f'<div class="glass-panel" style="border-color: {accent_color}33; padding: 1rem;">'
        f'<p style="color: #888; font-size: 0.75rem; margin: 0;">{label}</p>'
        f'<p class="mono" style="color: {accent_color}; font-size: 1.4rem; margin: 0;">{value}{unit}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )
