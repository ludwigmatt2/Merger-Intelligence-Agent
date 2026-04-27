"""Session state schema for MIA. All keys defined here. init_state() is idempotent."""
import streamlit as st

# Every key the app uses — modify here, not in screen files
SESSION_STATE_SCHEMA = {
    # Navigation
    "screen": "landing",           # str: current screen key

    # Bank inputs (set on landing screen)
    "bank_a": "",                  # str: Bank A name
    "bank_b": "",                  # str: Bank B name

    # Analysis mode (set on landing screen)
    "mode": "Forward Analysis",   # str: "Forward Analysis" | "Backtesting"

    # Orb animation state
    "orb_active": False,           # bool: True after START ANALYSIS click

    # Synergy sliders (Model & Data screen)
    "synergy_weights": {
        "cost_reduction":       0.5,
        "revenue_enhancement":  0.5,
        "capital_optimization": 0.5,
        "it_consolidation":     0.5,
        "member_retention":     0.5,
    },
}

def init_state():
    """Initialize session state with defaults. Safe to call on every rerun."""
    for key, default in SESSION_STATE_SCHEMA.items():
        if key not in st.session_state:
            st.session_state[key] = default
