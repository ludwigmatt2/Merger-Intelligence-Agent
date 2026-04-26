# Pitfalls Research — MIA Merger Intelligence Agent

**Domain:** Custom-styled Streamlit apps with CSS animations and glassmorphism
**Date:** 2026-04-26

---

## Pitfall 1: CSS Selectors Drift Between Streamlit Versions

**Warning signs:** Styles apply locally but break after `pip install --upgrade streamlit`.
**Root cause:** Streamlit uses generated class names (`.css-1d391kg`) that change between minor versions. The `data-testid` attribute API is more stable but still changes on major restructures.
**Prevention:**
- Prefer `data-testid` selectors over generated class names
- Use element type selectors where possible: `section[data-testid="stSidebar"]`
- Pin Streamlit version in `requirements.txt`: `streamlit==1.54.0`
- Test selectors with browser DevTools after every `pip upgrade`

**Most at risk:** Sidebar width override, block-container padding, stDeployButton hiding.

---

## Pitfall 2: CSS Animations Trigger Rerenders

**Warning signs:** App visibly flickers every few seconds; Streamlit spinner appears repeatedly.
**Root cause:** Streamlit reruns the entire script on any state change. If an animation modifies DOM elements that Streamlit tracks, it triggers another rerun, causing a loop.
**Prevention:**
- Keep animations **purely CSS** (`@keyframes`) — no JavaScript `setInterval`, no Python `time.sleep()` loops
- Never use `st.rerun()` inside a loop to animate — this is a rerender loop
- The AI Core orb must be a self-contained CSS animation block rendered once, not driven by Python

```css
/* CORRECT: Self-contained CSS animation — no Python involvement */
@keyframes orb-pulse {
    0% { box-shadow: 0 0 20px #00D4FF, 0 0 40px rgba(0,212,255,0.3); }
    50% { box-shadow: 0 0 60px #00D4FF, 0 0 100px rgba(123,47,190,0.5); }
    100% { box-shadow: 0 0 20px #00D4FF, 0 0 40px rgba(0,212,255,0.3); }
}
.orb { animation: orb-pulse 3s ease-in-out infinite; }
.orb.active { animation-duration: 0.8s; }
```

**Most at risk:** AI Core orb animation, any loading spinner.

---

## Pitfall 3: `backdrop-filter: blur()` Requires a Stacking Context

**Warning signs:** Glassmorphism panels appear solid black or transparent — no blur visible.
**Root cause:** `backdrop-filter` only blurs content *behind* the element in the same stacking context. If the element's parent doesn't create a stacking context, the filter has nothing to blur.
**Prevention:**
- Ensure parent containers have `position: relative` or `isolation: isolate`
- Test in Chrome — `backdrop-filter` is fully supported. Firefox requires `layout.css.backdrop-filter.enabled` flag (can be ignored for analyst tool)
- Add a fallback solid background: `background: rgba(17,17,24,0.85)` so the panel is still readable if blur fails

```css
.glass-panel {
    background: rgba(17, 17, 24, 0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);  /* Safari */
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 12px;
}
```

**Most at risk:** All 5 screen panels, sidebar panels.

---

## Pitfall 4: `st.markdown` Injected CSS Gets Duplicated on Rerun

**Warning signs:** Page slows down noticeably; browser DevTools shows `<style>` tags multiplying in `<head>`.
**Root cause:** Every Streamlit rerun re-executes `st.markdown(...)` and appends a new `<style>` block.
**Prevention:**
- Load all CSS in a single call at the top of `app.py`, wrapped in a function called once
- Streamlit deduplicates identical markdown blocks in many versions, but don't rely on it
- Use `st.cache_resource` if CSS loading is from file reads

```python
@st.cache_resource
def _load_css():
    # reads files and returns combined CSS string
    return combined_css

css = _load_css()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
```

**Most at risk:** Any screen that re-injects global styles.

---

## Pitfall 5: Google Fonts @import Causes Flash of Unstyled Text

**Warning signs:** On first load, text briefly renders in system font before Inter appears.
**Root cause:** `@import` in CSS is render-blocking but async — there's a small window where the font hasn't loaded yet.
**Prevention:**
- Add `display=swap` parameter to Google Fonts URL (already recommended)
- Define fallback font stack: `font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- For JetBrains Mono data values, fallback to `'Courier New', monospace`

---

## Pitfall 6: Plotly Charts Flash White on Dark Background

**Warning signs:** Charts render with a white rectangle around them for a split second on load.
**Root cause:** Plotly's default `paper_bgcolor` and `plot_bgcolor` are white. Streamlit renders the chart before the custom CSS overrides take effect.
**Prevention:**
- Always set both background colors to transparent in the figure layout:
```python
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    template="plotly_dark",
)
```
- Wrap chart in a `<div>` with the dark background class so the container is dark while chart loads

---

## Pitfall 7: Sidebar Width Cannot Be Set via `st.sidebar` API

**Warning signs:** Navigation labels truncate; sidebar too narrow for nav items.
**Root cause:** Streamlit doesn't expose sidebar width as a Python parameter.
**Prevention:**
- Override via CSS using the stable `data-testid` selector:
```css
section[data-testid="stSidebar"] {
    width: 260px !important;
    min-width: 260px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    width: 260px !important;
}
```

---

## Pitfall 8: `st.button` in Sidebar Loses Style After CTA Click

**Warning signs:** After `st.rerun()`, sidebar nav buttons reset to default styling.
**Root cause:** `st.rerun()` re-executes the full script. The active button state must be read from `st.session_state`, not from the button's own return value.
**Prevention:**
- Track active screen in `st.session_state.screen`
- Apply active CSS class conditionally in the HTML, not via button state:
```python
for screen_id, label in NAV_ITEMS.items():
    is_active = st.session_state.screen == screen_id
    active_class = "nav-active" if is_active else ""
    st.markdown(f'<div class="nav-item {active_class}">{label}</div>', unsafe_allow_html=True)
    if st.button(label, key=f"nav_{screen_id}", type="secondary"):
        st.session_state.screen = screen_id
        st.rerun()
```

---

## Pitfall 9: `layout="wide"` Still Has Padding

**Warning signs:** Glassmorphism panels don't reach the full width; there's white margin on the sides.
**Root cause:** Even in wide layout, `.block-container` has default padding.
**Prevention:**
```css
.block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-top: 0.5rem !important;
    max-width: 100% !important;
}
```

---

## Quick Reference: Suppress Default Streamlit Chrome

```css
/* Paste at top of base.css — verified stable as of v1.54 */
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
.stToolbar { display: none !important; }
```
