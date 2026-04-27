"""MIA — Merger Intelligence Agent
Entry point. Boot sequence: CSS → state → sidebar nav → screen router.
Run: streamlit run app.py
"""
import streamlit as st

# ── BOOT: Page config (must be first Streamlit call) ──────────────────────────
st.set_page_config(
    page_title="MIA — Merger Intelligence Agent",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── BOOT: CSS injection (before any rendering) ─────────────────────────────────
from core.styles import inject_css
inject_css()

# ── BOOT: Session state defaults (idempotent) ──────────────────────────────────
from core.state import init_state
init_state()

# ── SCREEN IMPORTS ─────────────────────────────────────────────────────────────
from screens.landing import render as render_landing
from screens.market_analysis import render as render_market_analysis
from screens.model_data import render as render_model_data
from screens.results import render as render_results
from screens.prompt_log import render as render_prompt_log

# Screen registry — add new screens here only
SCREENS = {
    "landing":          render_landing,
    "market_analysis":  render_market_analysis,
    "model_data":       render_model_data,
    "results":          render_results,
    "prompt_log":       render_prompt_log,
}

# Navigation items: (screen_id, display_label)
NAV_ITEMS = [
    ("landing",         "Landing"),
    ("market_analysis", "Market Analysis"),
    ("model_data",      "Model & Data"),
    ("results",         "Results & Decision"),
    ("prompt_log",      "Prompt Log"),
]

# ── SIDEBAR NAVIGATION ─────────────────────────────────────────────────────────
with st.sidebar:
    # Brand header
    st.markdown(
        '<div class="sidebar-brand">'
        '<h2>MIA</h2>'
        '<p>Merger Intelligence Agent</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Nav items — active state driven by st.session_state.screen (not button state)
    # Wrap each button in a styled div so the active CSS class applies (Pitfall 8)
    for screen_id, label in NAV_ITEMS:
        is_active = st.session_state.screen == screen_id
        css_class = "nav-item-active" if is_active else "nav-item"

        # Wrap button in a styled container div
        st.markdown(
            f'<div class="{css_class}" style="margin:0;padding:0;">',
            unsafe_allow_html=True,
        )
        clicked = st.button(label, key=f"nav_{screen_id}", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if clicked:
            st.session_state.screen = screen_id
            st.rerun()

    # Sidebar footer
    st.markdown(
        '<div style="position: absolute; bottom: 1rem; left: 1rem; '
        'color: rgba(255,255,255,0.2); font-size: 0.65rem; letter-spacing: 0.05em;">'
        "MIA v1 · Phase 1 Scaffold"
        "</div>",
        unsafe_allow_html=True,
    )

# ── SCREEN ROUTER ──────────────────────────────────────────────────────────────
current_screen = st.session_state.get("screen", "landing")
renderer = SCREENS.get(current_screen, render_landing)
renderer()
