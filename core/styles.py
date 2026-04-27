"""CSS injection for MIA. Call inject_css() exactly once at app startup in app.py.

All four CSS files are read from disk, combined, and injected via st.markdown.
Uses @st.cache_resource so file reads happen once per server process, not per rerun.
"""
import streamlit as st
from pathlib import Path

# Resolve the styles/ directory relative to this file
_STYLES_DIR = Path(__file__).parent.parent / "styles"


@st.cache_resource
def _load_css() -> str:
    """Read all 4 CSS files and return combined string. Cached at process level.

    Missing CSS files log a warning instead of raising an exception (T-1-06).
    """
    files = [
        "base.css",        # fonts + chrome suppression (load first)
        "components.css",  # glass-panel, .mono, kpi-card
        "sidebar.css",     # nav items, active state
        "animations.css",  # orb keyframes, screen transitions
    ]
    combined = ""
    for filename in files:
        css_path = _STYLES_DIR / filename
        if css_path.exists():
            combined += css_path.read_text(encoding="utf-8") + "\n"
        else:
            # Warn but do not crash — partial CSS is better than a broken app
            import warnings
            warnings.warn(
                f"MIA CSS file not found: {css_path}. Styles may be incomplete.",
                RuntimeWarning,
                stacklevel=2,
            )
    return combined


def inject_css() -> None:
    """Inject all application CSS. Call once at the top of app.py before any render.

    Uses @st.cache_resource on the file reader — inject_css() itself must be
    called every rerun (Streamlit needs the <style> tag re-emitted) but the
    file I/O is cached.
    """
    css = _load_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
