"""Pipeline visualization component — horizontal 5-step flow. Implemented in Phase 3."""
import streamlit as st

PIPELINE_STEPS = ["Input", "Preprocessing", "Synergy Weighting", "KI Evaluation", "Output"]

def render_pipeline(active_step: int = 0):
    """Render the 5-step analysis pipeline. active_step is 0-indexed."""
    steps_html = ""
    for i, step in enumerate(PIPELINE_STEPS):
        color = "#00D4FF" if i == active_step else "#444"
        steps_html += (
            f'<div style="text-align:center; color:{color}; flex:1;">'
            f'<div style="border: 1px solid {color}; border-radius:8px; padding:0.5rem;">{step}</div>'
            f'</div>'
        )
        if i < len(PIPELINE_STEPS) - 1:
            steps_html += '<div style="color:#444; align-self:center; padding:0 0.25rem;">&#x2192;</div>'

    st.markdown(
        f'<div style="display:flex; align-items:stretch; gap:0.25rem;">{steps_html}</div>',
        unsafe_allow_html=True,
    )
