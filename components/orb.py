"""AI Core orb component — CSS-animated pulsing orb. Implemented in Phase 2."""
import streamlit as st

def render_orb(active: bool = False):
    """Render the AI Core orb. active=True uses fast pulse (0.8s), False uses idle (3s)."""
    orb_class = "orb orb-active" if active else "orb orb-idle"
    st.markdown(f'<div class="{orb_class}">AI CORE</div>', unsafe_allow_html=True)
