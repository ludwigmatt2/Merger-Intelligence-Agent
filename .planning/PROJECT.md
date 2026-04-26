# MIA — Merger Intelligence Agent

## What This Is

MIA is a futuristic, web-based AI analysis application for evaluating German cooperative bank mergers (Volksbank/Raiffeisenbank), with support for general bank merger analysis. It guides analysts through a structured workflow — from bank data input through synergy modeling and KI evaluation — and delivers a clear GO / NO-GO recommendation. Built in Streamlit with a dark-mode glassmorphism UI and neon accent design language.

## Core Value

A clear, data-grounded GO / NO-GO merger recommendation that an analyst can trust and document.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Streamlit app runs with `streamlit run app.py` — no config beyond that
- [ ] Dark mode UI: background #0A0A0F, surfaces #111118 / #1A1A2E, neon accents Electric Cyan #00D4FF, Violet #7B2FBE, Electric Blue #0066FF
- [ ] Glassmorphism panel style: backdrop-filter blur, rgba backgrounds, glowing borders
- [ ] Typography: Inter for UI labels, JetBrains Mono for data values
- [ ] Left sidebar navigation — highlights active screen in cyan
- [ ] Landing screen: centered pulsing AI Core orb (CSS keyframe animation), two bank name inputs, mode toggle (Backtesting / Forward Analysis), "START ANALYSIS" CTA
- [ ] AI Core orb pulses faster when CTA is clicked
- [ ] Market Analysis screen: two-column KPI card layout (Bank A cyan / Bank B violet), placeholder radar chart
- [ ] Model & Data screen: horizontal 5-step pipeline (Input → Preprocessing → Synergy Weighting → KI Evaluation → Output), placeholder synergy sliders
- [ ] Results & Decision screen: large GO / NO-GO hero element (green / orange), placeholder comparison table and bar charts
- [ ] Prompt Log screen: table with 7 columns for prompt documentation
- [ ] All data is placeholder / mock — no backend calls

### Out of Scope

- Backend AI / LLM integration — Phase 2+
- Real financial data connectors — Phase 2+
- Authentication / multi-user — not in scope for v1
- Mobile layout — desktop-first tool

## Context

- Focus domain: German cooperative banks (Volksbank, Raiffeisenbank), secondary general M&A
- Two analysis modes: Backtesting (historical mergers) and Forward Analysis (prospective)
- The "Synergy Weighting" step reflects a configurable model where analysts adjust how much each synergy driver matters
- Prompt Log screen is likely for AI prompt documentation / auditability — relevant for regulated use cases
- Charts powered by Plotly; custom CSS injected via `st.markdown` to override Streamlit defaults

## Constraints

- **Tech Stack**: Python + Streamlit + custom CSS + Plotly — no framework changes
- **Entry Point**: Must run as `streamlit run app.py` with no additional config
- **Phase 1 Scope**: GUI and animations only — no real data, no API calls, no AI

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Streamlit over React/Next.js | Python-native, fast to build, analyst audience not web-app-first | — Pending |
| Custom CSS injection via st.markdown | Only way to apply glassmorphism and animations in Streamlit | — Pending |
| Plotly for charts | Streamlit-native integration, interactive out of the box | — Pending |

---
*Last updated: 2026-04-26 after initialization*
