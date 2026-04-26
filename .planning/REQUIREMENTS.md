# Requirements: MIA — Merger Intelligence Agent

**Defined:** 2026-04-26
**Core Value:** A clear, data-grounded GO / NO-GO merger recommendation that an analyst can trust and document.

---

## v1 Requirements (Phase 1 — GUI Framework)

### Foundation

- [ ] **FOUND-01**: App runs with `streamlit run app.py` — no additional config or arguments
- [ ] **FOUND-02**: Dark mode forced via `config.toml` (`base="dark"`, `backgroundColor="#0A0A0F"`, `secondaryBackgroundColor="#111118"`, `primaryColor="#00D4FF"`)
- [ ] **FOUND-03**: All default Streamlit chrome suppressed: hamburger menu, footer, deploy button, top header bar, toolbar
- [ ] **FOUND-04**: Google Fonts loaded via CSS `@import`: Inter (300/400/500/600/700) for UI labels, JetBrains Mono (400/500) for data values
- [ ] **FOUND-05**: Glassmorphism panel system: reusable `.glass-panel` CSS class with `backdrop-filter: blur(20px)`, `rgba(17,17,24,0.7)` background, `rgba(0,212,255,0.15)` border, `border-radius: 12px`
- [ ] **FOUND-06**: All CSS injected once at app startup from `core/styles.py` — never scattered across screen files
- [ ] **FOUND-07**: `requirements.txt` with pinned `streamlit==1.54.0` and `plotly`

### Navigation

- [ ] **NAV-01**: Left sidebar renders 5 navigation items: Landing, Market Analysis, Model & Data, Results & Decision, Prompt Log
- [ ] **NAV-02**: Active screen highlighted in sidebar: cyan `#00D4FF` left border + cyan text
- [ ] **NAV-03**: Sidebar nav switches active screen via `st.session_state.screen` + `st.rerun()` — no full page reload
- [ ] **NAV-04**: Default Streamlit file-based sidebar nav hidden (`showSidebarNavigation = false` in config.toml)

### Landing Screen

- [ ] **LAND-01**: Centered layout with AI Core orb as the visual focal point
- [ ] **LAND-02**: AI Core orb continuously animates via CSS `@keyframes`: pulsing concentric glow rings + orbiting particle dots at idle (3s cycle)
- [ ] **LAND-03**: AI Core orb pulses faster (0.8s cycle) when "START ANALYSIS" is clicked — CSS class toggle via session state
- [ ] **LAND-04**: Two text inputs: "Bank A" and "Bank B" with placeholder hints (e.g. "VR Bank Musterstadt")
- [ ] **LAND-05**: Mode toggle: "Forward Analysis" / "Backtesting" — stored in `st.session_state.mode`
- [ ] **LAND-06**: "START ANALYSIS" CTA button — full-width, primary style, neon cyan glow on hover
- [ ] **LAND-07**: Clicking "START ANALYSIS" sets `orb_active = True`, navigates to Market Analysis screen

### Market Analysis Screen

- [ ] **MARK-01**: Two-column layout — Bank A (left, cyan accent) and Bank B (right, violet accent)
- [ ] **MARK-02**: KPI cards per bank: Total Assets (€M), Tier-1 Capital (%), Cost/Income Ratio (%), NPL Ratio (%), ROE (%), Branch Count, Member Count — populated from mock data in `core/data.py`
- [ ] **MARK-03**: Bank names from session state displayed as column headers
- [ ] **MARK-04**: Placeholder Plotly radar chart below KPI cards — `go.Scatterpolar` with dark transparent background, showing both banks overlaid in their respective colors
- [ ] **MARK-05**: All KPI cards use glassmorphism panel style with bank-respective border color

### Model & Data Screen

- [ ] **MODEL-01**: Horizontal 5-step pipeline visualization: Input → Preprocessing → Synergy Weighting → KI Evaluation → Output
- [ ] **MODEL-02**: Pipeline steps rendered as HTML/CSS — active step highlighted in cyan, inactive steps in muted gray
- [ ] **MODEL-03**: Synergy sliders: Cost Reduction, Revenue Enhancement, Capital Optimization, IT Consolidation, Member Retention — values 0.0–1.0, stored in `st.session_state.synergy_weights`
- [ ] **MODEL-04**: Sliders update UI only — no backend recalculation in Phase 1
- [ ] **MODEL-05**: Slider section wrapped in glassmorphism panel

### Results & Decision Screen

- [ ] **RES-01**: Large GO / NO-GO hero element as visual centerpiece — "GO" in green `#00FF88`, "NO-GO" in orange `#FF6B00`, with matching glow
- [ ] **RES-02**: Hero element uses placeholder mock verdict (GO) in Phase 1
- [ ] **RES-03**: Placeholder comparison table below hero (bank metrics side-by-side, styled dark table)
- [ ] **RES-04**: Placeholder Plotly bar charts (one per bank or grouped) with dark transparent background
- [ ] **RES-05**: All sections wrapped in glassmorphism panels

### Prompt Log Screen

- [ ] **LOG-01**: Reads `prompt_log.csv` from project root using `pandas.read_csv()`
- [ ] **LOG-02**: Renders all rows as a styled HTML table — not `st.dataframe()` default styling
- [ ] **LOG-03**: `P-DEV-XX` rows have Electric Blue `#0066FF` left border
- [ ] **LOG-04**: `P-XX` rows (no DEV) have Electric Cyan `#00D4FF` left border
- [ ] **LOG-05**: Table displays all 7 columns: Nr, Prompt_Originaltext, Zweck_Einsatzbereich, KI_Modell_Plattform, Datum_Uhrzeit, KI_Antwort_Kurzfassung, Wissenschaftliche_Validierung
- [ ] **LOG-06**: Table wrapped in glassmorphism panel, readable on dark background (alternating row shading)

---

## v2 Requirements

### Backend & AI Integration

- **AI-01**: LLM-powered analysis: submit bank names + mode to AI model, receive structured GO/NO-GO reasoning
- **AI-02**: Synergy scoring engine: compute weighted score from slider values + real bank data
- **AI-03**: Real bank data connector: fetch financial metrics from BVR data source or manual CSV upload
- **AI-04**: Prompt Log auto-populated from real AI calls (P-XX entries written by the app at analysis runtime)

### Export & Compliance

- **EXP-01**: PDF export of Results & Decision screen
- **EXP-02**: CSV export of full prompt log
- **EXP-03**: Audit trail: timestamp every analysis session with bank names, mode, and verdict

### UX Polish

- **UX-01**: Screen fade-in transitions (CSS opacity animation on screen change)
- **UX-02**: Loading animation during AI call (custom pulsing-dot component, not default st.spinner)
- **UX-03**: Number counter animation on KPI cards (count up from 0 to value on screen enter)
- **UX-04**: GO/NO-GO confidence ring: SVG stroke-dasharray ring showing model certainty percentage

---

## Out of Scope

| Feature | Reason |
|---------|--------|
| Authentication / login | Single-user analyst tool for v1; not required |
| Mobile / responsive layout | Desktop-only analyst tool |
| OAuth or SSO | Out of scope for v1 |
| Multi-language UI | German/English mixed labels are sufficient |
| Real-time data feeds | Deferred to v2 backend phase |
| `st.Page` / multipage file routing | URL routing resets animation state; custom session-state nav is better |
| Three.js / tsParticles for orb | Oversized dependency; CSS-only orb achieves the same effect |

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUND-01 to FOUND-07 | Phase 1 | Pending |
| NAV-01 to NAV-04 | Phase 1 | Pending |
| LAND-01 to LAND-07 | Phase 1 | Pending |
| MARK-01 to MARK-05 | Phase 1 | Pending |
| MODEL-01 to MODEL-05 | Phase 1 | Pending |
| RES-01 to RES-05 | Phase 1 | Pending |
| LOG-01 to LOG-06 | Phase 1 | Pending |

**Coverage:**
- v1 requirements: 34 total
- Mapped to phases: 34
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-26*
*Last updated: 2026-04-26 after initial definition*
