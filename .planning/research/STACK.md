# Stack Research — MIA Merger Intelligence Agent

**Domain:** Custom dark-mode glassmorphism Streamlit analytics app
**Date:** 2026-04-26
**Sources:** Context7 Streamlit docs (v1.54.0), official Streamlit GitHub

---

## Recommended Stack

| Layer | Choice | Version | Confidence |
|-------|--------|---------|------------|
| Framework | Streamlit | 1.54.0 | HIGH |
| Charts | Plotly | 6.x | HIGH |
| CSS delivery | `st.markdown(unsafe_allow_html=True)` | — | HIGH |
| Component isolation | `st.components.v2.component` | — | MEDIUM |
| Fonts | Google Fonts via `@import` in injected CSS | — | HIGH |
| Dark theme base | `config.toml` `[theme] base="dark"` | — | HIGH |
| Session nav | `st.session_state["screen"]` | — | HIGH |

---

## Key APIs

### Dark Theme Base (config.toml)
```toml
[theme]
base = "dark"
backgroundColor = "#0A0A0F"
secondaryBackgroundColor = "#111118"
primaryColor = "#00D4FF"
textColor = "#E0E0E0"
font = "sans serif"

[client]
showSidebarNavigation = false
```
Setting `showSidebarNavigation = false` suppresses the default file-based nav — **required** for custom sidebar navigation.

### CSS Injection Pattern
```python
def inject_css(css: str):
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
```
Call once at the top of `app.py` before any screen renders. All global styles go here — glassmorphism panels, typography, animations, sidebar overrides.

### CSS Variables Available (v1.54+)
Streamlit now exposes CSS custom properties you can reference in injected CSS:
- `var(--st-background-color)`
- `var(--st-secondary-background-color)`
- `var(--st-primary-color)`
- `var(--st-text-color)`
- `var(--st-font)`

For MIA's hardcoded palette, use literal hex values rather than CSS vars to guarantee exact color reproduction regardless of theme toggle.

### Session State Navigation
```python
if "screen" not in st.session_state:
    st.session_state.screen = "landing"

# In sidebar
screens = ["landing", "market_analysis", "model_data", "results", "prompt_log"]
for s in screens:
    if st.button(s, key=f"nav_{s}"):
        st.session_state.screen = s
        st.rerun()

# In main area
if st.session_state.screen == "landing":
    render_landing()
elif st.session_state.screen == "market_analysis":
    render_market_analysis()
# ...
```

### Plotly Dark Theme
```python
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(17,17,24,0.0)",  # transparent
    plot_bgcolor="rgba(17,17,24,0.0)",
    font_color="#E0E0E0",
    font_family="Inter",
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
```

### Google Fonts Loading
```python
FONT_IMPORT = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* { font-family: 'Inter', sans-serif; }
.data-value, .mono { font-family: 'JetBrains Mono', monospace !important; }
"""
```
Inject this before all other CSS. Font loading is async — `display=swap` prevents invisible text during load.

### HTML Animations (AI Core Orb)
CSS keyframe animations injected via `st.markdown` work reliably. For click-triggered animation state changes:
```python
# Use session state to toggle CSS class
if "orb_active" not in st.session_state:
    st.session_state.orb_active = False

orb_class = "orb-active" if st.session_state.orb_active else "orb-idle"
st.markdown(f'<div class="ai-core {orb_class}">...</div>', unsafe_allow_html=True)

if st.button("START ANALYSIS"):
    st.session_state.orb_active = True
    st.session_state.screen = "market_analysis"
    st.rerun()
```

### Suppress Default Streamlit Chrome
```css
/* Hide hamburger menu, footer, deploy button */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }
header[data-testid="stHeader"] { display: none; }

/* Remove default padding */
.block-container { padding-top: 1rem !important; max-width: 100% !important; }
```
**Note:** `data-testid` selectors are stable from v1.28+ but verify on upgrade.

---

## What NOT to Use

| Option | Reason to Avoid |
|--------|-----------------|
| `st.Page` / multipage files | Adds file-based nav overhead; custom sidebar is simpler for MIA |
| `streamlit-extras` | Adds dependency for features achievable with CSS injection |
| `st.components.v1.html()` | Deprecated path; use `st.markdown` or `st.iframe` |
| Streamlit's `st.color_picker` | Irrelevant to this stack |
| `st.set_page_config(layout="centered")` | Use `layout="wide"` for full-width glassmorphism panels |

---

## Setup Command
```bash
pip install streamlit plotly
streamlit run app.py
```
No additional config required beyond `config.toml`.
