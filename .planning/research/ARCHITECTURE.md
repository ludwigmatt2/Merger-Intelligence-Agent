# Architecture Patterns

**Project:** MIA (Merger Intelligence Agent) — Phase 1 GUI
**Researched:** 2026-04-26
**Confidence:** HIGH for Streamlit session-state patterns (stable, well-documented); MEDIUM for CSS injection edge cases (Streamlit internals can shift across minor versions)

---

## Recommended Architecture

**Single entry point, modular internals.** One `app.py` file bootstraps the app (CSS injection, session state init, screen routing). All screen logic lives in separate modules under `screens/`. Shared utilities (CSS, state schema, mock data) are isolated in `core/`. This gives a junior developer one obvious file to start reading (`app.py`) and one obvious place to swap data (`core/data.py`).

### File / Folder Layout

```
Merger Intelligence Agent/
├── app.py                    ← Entry point. Boot sequence only: CSS → state init → router
├── core/
│   ├── __init__.py
│   ├── state.py              ← Session state schema + init function
│   ├── styles.py             ← All CSS as Python string(s), inject_css() function
│   └── data.py               ← Mock data + data-access interface (swap point for Phase 2)
├── screens/
│   ├── __init__.py
│   ├── home.py               ← render_home()
│   ├── search.py             ← render_search()
│   ├── deal_overview.py      ← render_deal_overview()
│   ├── analysis.py           ← render_analysis()
│   └── settings.py           ← render_settings()
├── components/
│   ├── __init__.py
│   ├── sidebar.py            ← render_sidebar() — shared across screens
│   ├── deal_card.py          ← DealCard component function
│   └── loading.py            ← Animated loading states
├── assets/
│   └── fonts/                ← Any local font files (woff2 etc.)
├── requirements.txt
└── .planning/
    └── research/
        └── ARCHITECTURE.md   ← this file
```

**Why not one flat file?** At 5 screens with CSS, mock data, and animation state, a single `app.py` hits 800+ lines fast. Modular structure means a Phase 2 developer edits only `core/data.py` — they never touch screen logic.

**Why not Streamlit's native multipage (st.Page / pages/ folder)?** The requirement specifies session-state-driven screen switching, not URL-based page routing. `st.Page` reloads the entire script on navigation, which resets animation states and adds URL complexity. Session state switching gives full control over transitions.

---

## How Screens Are Rendered and Switched

### Screen Router (in app.py)

```python
# app.py — full boot sequence
import streamlit as st
from core.styles import inject_css
from core.state import init_state
from screens.home import render_home
from screens.search import render_search
from screens.deal_overview import render_deal_overview
from screens.analysis import render_analysis
from screens.settings import render_settings

st.set_page_config(
    page_title="MIA — Merger Intelligence Agent",
    page_icon="assets/favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Boot sequence — order matters
inject_css()      # 1. CSS first, before any rendering
init_state()      # 2. State defaults, idempotent

# Screen router — reads single source of truth
SCREENS = {
    "home":          render_home,
    "search":        render_search,
    "deal_overview": render_deal_overview,
    "analysis":      render_analysis,
    "settings":      render_settings,
}

current = st.session_state.screen
renderer = SCREENS.get(current, render_home)
renderer()
```

### Navigation (called from any screen or component)

```python
# Pattern for navigating between screens — used in screen modules and sidebar
def navigate(screen_name: str):
    st.session_state.screen = screen_name
    st.rerun()
```

This is the only way screens transition. No `st.switch_page`, no URL manipulation.

### Screen Module Structure

Each screen follows the same contract:

```python
# screens/deal_overview.py
import streamlit as st
from core.data import get_deal
from components.deal_card import render_deal_card

def render_deal_overview():
    """Render the Deal Overview screen. Reads from st.session_state.active_deal_id."""
    deal_id = st.session_state.get("active_deal_id")
    if not deal_id:
        st.error("No deal selected.")
        return

    deal = get_deal(deal_id)           # mock in Phase 1, real API in Phase 2
    render_deal_card(deal)
    # ... rest of screen UI
```

Screens are stateless functions. They read from `st.session_state`, call data functions, render UI. They do not hold data themselves.

---

## CSS Injection Pattern

### core/styles.py

All CSS lives in one module. `inject_css()` is called exactly once in `app.py`, before any screen renders.

```python
# core/styles.py
import streamlit as st

# Fonts and base resets
_BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; }

.stApp {
    font-family: 'Inter', sans-serif;
    background-color: #0A0A0F;
    color: #E8E8F0;
}

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.block-container { padding-top: 1rem; }
"""

# Animation classes (toggled via JS/class injection)
_ANIMATION_CSS = """
.mia-card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px;
}

.mia-card.is-loading {
    opacity: 0.5;
    pointer-events: none;
}

.mia-card.is-entering {
    animation: slideInUp 0.4s ease-out forwards;
}

@keyframes slideInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.mia-screen-transition {
    animation: fadeIn 0.25s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
"""

# Screen-specific overrides (kept modular but injected together)
_SCREEN_CSS = """
/* Home screen */
.mia-home-hero { ... }

/* Search screen */
.mia-search-input { ... }

/* Deal overview */
.mia-deal-header { ... }
"""

def inject_css():
    """Inject all application CSS. Call once at app startup."""
    full_css = _BASE_CSS + _ANIMATION_CSS + _SCREEN_CSS
    st.markdown(f"<style>{full_css}</style>", unsafe_allow_html=True)
```

**Why one inject call?** `st.markdown` with CSS is re-executed on every Streamlit rerun. Injecting in one place (top of `app.py`) ensures CSS always loads before rendering, never duplicates, and is easy to audit. If CSS were scattered across screen files, the injection order becomes unpredictable on reruns.

**Animation classes approach:** Streamlit cannot directly toggle CSS classes on elements. The pattern is: store animation state in `st.session_state` → use that state to conditionally add class strings to `st.markdown()` HTML blocks. Example:

```python
# In a screen or component:
card_class = "mia-card is-entering" if st.session_state.get("deal_just_loaded") else "mia-card"
st.markdown(f'<div class="{card_class}">...</div>', unsafe_allow_html=True)
```

---

## Session State Schema

### core/state.py

```python
# core/state.py
import streamlit as st

# Canonical schema — document every key here
SESSION_STATE_SCHEMA = {
    # Navigation
    "screen":              "home",           # str: current screen name
    "previous_screen":     None,             # str | None: for back navigation

    # Deal context
    "active_deal_id":      None,             # str | None: currently viewed deal
    "search_query":        "",               # str: last search input
    "search_results":      [],               # list[dict]: last search results

    # Animation / UI state
    "deal_just_loaded":    False,            # bool: triggers enter animation on deal card
    "is_loading":          False,            # bool: triggers loading overlay
    "animation_tick":      0,               # int: increment to re-trigger animations

    # User preferences (Phase 1: no persistence)
    "theme":               "dark",           # str: "dark" | "light"
    "sidebar_open":        False,            # bool

    # Phase 2 placeholders (set but unused in Phase 1)
    "auth_token":          None,             # str | None: API auth token
    "user_id":             None,             # str | None: authenticated user
}

def init_state():
    """Initialize session state with defaults. Idempotent — safe to call on every rerun."""
    for key, default in SESSION_STATE_SCHEMA.items():
        if key not in st.session_state:
            st.session_state[key] = default
```

**Why define a schema dict?** It documents every key in one place. `init_state()` is idempotent — calling it on every rerun (which Streamlit does) only sets keys that don't exist yet, so existing state is never clobbered. Phase 2 devs can see every state key without reading screen code.

**Why include Phase 2 placeholders?** `auth_token` and `user_id` cost nothing to declare and signal to Phase 2 developers exactly where authentication slots in.

---

## Mock Data Pattern

### core/data.py — The Phase 2 Swap Point

This is the single file a Phase 2 developer replaces. The interface (function signatures) stays identical; only the implementation changes.

```python
# core/data.py

# ── MOCK DATA ──────────────────────────────────────────────────────────────
# Phase 1: static dicts. Phase 2: delete this section, implement functions below.

_MOCK_DEALS = {
    "deal_001": {
        "id": "deal_001",
        "target":        "Acme Corp",
        "acquirer":      "MegaCo Industries",
        "deal_value_bn": 4.2,
        "status":        "Announced",
        "sector":        "Technology",
        "announced_at":  "2026-03-15",
        "synergies_bn":  0.8,
        "premium_pct":   32.4,
        "sources":       [],          # Phase 2: list of news/filing URLs
    },
    "deal_002": { ... },
}

_MOCK_SEARCH_RESULTS = [
    {"id": "deal_001", "label": "Acme / MegaCo — $4.2B Technology"},
    {"id": "deal_002", "label": "..."},
]

# ── DATA ACCESS INTERFACE ───────────────────────────────────────────────────
# Phase 2 developer: replace implementations below. Signatures stay the same.

def get_deal(deal_id: str) -> dict | None:
    """Fetch a single deal by ID.
    Phase 1: returns mock dict.
    Phase 2: replace with API call, e.g. return api_client.get("/deals/{deal_id}")
    """
    return _MOCK_DEALS.get(deal_id)


def search_deals(query: str) -> list[dict]:
    """Search deals by query string.
    Phase 1: returns filtered mock list.
    Phase 2: replace with search API call.
    """
    q = query.lower()
    return [r for r in _MOCK_SEARCH_RESULTS if q in r["label"].lower()]


def get_deal_analysis(deal_id: str) -> dict | None:
    """Fetch LLM-generated analysis for a deal.
    Phase 1: returns hardcoded analysis stub.
    Phase 2: replace with LLM API call.
    """
    return {
        "summary": "Placeholder: strategic rationale analysis will appear here.",
        "synergy_breakdown": [],
        "risk_flags":        [],
        "comparable_deals":  [],
    }


def get_market_data(ticker: str) -> dict | None:
    """Fetch market data for a company.
    Phase 1: returns mock OHLCV stub.
    Phase 2: replace with Bloomberg / Yahoo Finance / proprietary feed.
    """
    return {
        "ticker":    ticker,
        "price":     142.50,
        "change_1d": 2.3,
        "volume":    1_240_000,
        "52w_high":  168.00,
        "52w_low":   98.50,
    }
```

**Why this pattern over a class?** Module-level functions are simpler for Streamlit. No instantiation needed, no `__init__` to mock in tests. If Phase 2 needs dependency injection (e.g. authenticated API client), the functions can become class methods without changing call sites in screen code.

**Why not put mocks in a separate `mocks/` folder?** Keeping them in `data.py` co-located with the interface means Phase 2 devs see the interface and the mock in the same file. They understand exactly what each function returns before replacing it.

---

## Component Pattern

Shared UI building blocks live in `components/`. They are pure render functions — they receive data as arguments, do not fetch data themselves, and do not navigate.

```python
# components/deal_card.py
import streamlit as st

def render_deal_card(deal: dict, animate: bool = False):
    """Renders a deal summary card. Pure UI — no data fetching, no navigation."""
    card_class = "mia-card is-entering" if animate else "mia-card"
    with st.container():
        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"### {deal['target']}")
            st.caption(f"Acquirer: {deal['acquirer']}")
        with col2:
            st.metric("Deal Value", f"${deal['deal_value_bn']}B")
            st.metric("Premium", f"{deal['premium_pct']}%")
        with col3:
            st.badge(deal['status'])
        st.markdown('</div>', unsafe_allow_html=True)
```

**Rule:** Components never call `data.py` functions. Screens call data functions, then pass results to components. This keeps components testable in isolation.

---

## Extensibility for Phase 2 Backend

### What Phase 2 Touches

| File | Phase 2 Change | UI Impact |
|------|---------------|-----------|
| `core/data.py` | Replace mock functions with real API calls | None — same signatures |
| `core/state.py` | Populate `auth_token`, `user_id` after login | Minimal — add login screen |
| `app.py` | Add auth gate before screen router | Small addition, no refactor |
| `screens/` | No changes needed for data swap | Zero |
| `components/` | No changes needed for data swap | Zero |
| `core/styles.py` | No changes needed | Zero |

### Auth Gate Pattern (Phase 2 addition)

```python
# app.py Phase 2 addition — drop in before SCREENS router
if not st.session_state.auth_token:
    render_login()   # new screens/login.py
    st.stop()        # halt rendering — prevents screens from showing
```

### LLM Integration (Phase 2)

`get_deal_analysis()` in `data.py` becomes an async LLM call. Because the function signature is already established in Phase 1, Phase 2 just replaces the body:

```python
# Phase 2 implementation
def get_deal_analysis(deal_id: str) -> dict | None:
    deal = get_deal(deal_id)
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Analyze merger: {deal}"}]
    )
    return parse_analysis_response(response)
```

Screens call `get_deal_analysis(deal_id)` identically in both phases.

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: CSS in Screen Files

**What:** `st.markdown("<style>...</style>", ...)` called inside `render_search()` or `render_home()`

**Why bad:** Streamlit reruns the entire script on every interaction. CSS fragments get injected in random order, some screens inject CSS that affects other screens, and you get specificity wars. The app becomes unpredictable to style.

**Instead:** All CSS in `core/styles.py`, injected once at the top of `app.py`.

### Anti-Pattern 2: Data Fetching in Components

**What:** `deal_card.py` calls `get_deal(deal_id)` directly

**Why bad:** Components become stateful, untestable, and coupled to the data layer. When Phase 2 makes API calls async or adds error handling, you have to touch every component.

**Instead:** Screens fetch data, pass dicts to components. Components are pure render functions.

### Anti-Pattern 3: `st.session_state` Keys Scattered Across Files

**What:** Each screen defines its own state keys (`st.session_state.search_query = ""` in `search.py`, etc.)

**Why bad:** No single source of truth. Keys conflict. Phase 2 developers have to grep the entire codebase to understand state shape.

**Instead:** All keys defined and initialized in `core/state.py`. Screens only read and write — they never create keys.

### Anti-Pattern 4: Using `st.Page` / `pages/` for This App

**What:** Splitting screens into `pages/home.py`, `pages/search.py` etc., using Streamlit's native multipage routing

**Why bad:** `st.Page` uses URL-based routing and reloads the full script on navigation. This resets animation state, disrupts the controlled boot sequence (CSS inject, state init), and prevents smooth transitions. The requirement explicitly calls for session-state-driven switching.

**Instead:** Manual router in `app.py` with `SCREENS` dict as shown above.

### Anti-Pattern 5: `st.experimental_rerun()` (deprecated)

**What:** Using `st.experimental_rerun()` for screen transitions

**Why bad:** Deprecated as of Streamlit 1.27. Will break in future versions.

**Instead:** `st.rerun()` (stable API since 1.27+).

---

## Scalability Considerations

| Concern | Phase 1 (5 screens, mock data) | Phase 2 (real API, LLM) |
|---------|-------------------------------|------------------------|
| Rerun cost | Negligible — all data is in-memory dicts | Add `@st.cache_data` to data functions with appropriate TTL |
| State complexity | 10-15 keys, all primitives | Add user context keys; consider `st.session_state` namespacing |
| CSS complexity | One `styles.py` file | Split `_SCREEN_CSS` into per-screen dicts if >500 lines |
| Component reuse | Functions, no state | Same — add `key=` params to Streamlit widgets inside components to avoid key collisions |

### Caching for Phase 2 (note for roadmap)

```python
# Phase 2 addition to data.py
@st.cache_data(ttl=300)   # 5-minute cache for deal data
def get_deal(deal_id: str) -> dict | None:
    return api_client.get(f"/deals/{deal_id}")
```

The `@st.cache_data` decorator is the correct Streamlit caching primitive for data fetched from external sources. `@st.cache_resource` is for persistent connections (DB connections, API clients). This distinction matters for Phase 2.

---

## Sources

- Streamlit session state documentation (stable API since v1.0, patterns consistent through v1.32+): https://docs.streamlit.io/develop/concepts/architecture/session-state
- Streamlit `st.rerun()` stable since v1.27: https://docs.streamlit.io/develop/api-reference/execution-flow/st.rerun
- Streamlit caching primitives (`cache_data` vs `cache_resource`): https://docs.streamlit.io/develop/concepts/architecture/caching
- Community pattern: single-file router with session state for screen management — HIGH confidence, widely used before `st.Page` existed and still preferred for animation-heavy apps
- CSS injection via `st.markdown` with `unsafe_allow_html=True`: official pattern, documented in Streamlit theming docs
- `st.Page` / multipage limitations for animation state: MEDIUM confidence — based on Streamlit execution model (full script rerun on page switch), not a specific doc statement
