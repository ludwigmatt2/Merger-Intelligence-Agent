# Roadmap: MIA — Merger Intelligence Agent

## Overview

MIA v1 delivers a fully visual, animated Streamlit shell for cooperative bank merger analysis. Starting from a blank repo, four phases build the app from the ground up: first the style system and project skeleton, then the animated landing screen, then the two analysis screens (Market Analysis and Model & Data), and finally the decision and audit screens. No backend, no real data — pure UI and mock data, ready for Phase 2 AI integration.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Scaffold & Style System** - Project skeleton, config.toml, CSS injection, glassmorphism system, fonts, sidebar nav
- [ ] **Phase 2: Landing Screen** - AI Core orb animation, bank inputs, mode toggle, START ANALYSIS CTA
- [ ] **Phase 3: Analysis Screens** - Market Analysis KPI cards + radar chart, Model & Data pipeline + synergy sliders
- [ ] **Phase 4: Decision & Log Screens** - GO/NO-GO hero, comparison table, bar charts, CSV-driven Prompt Log

## Phase Details

### Phase 1: Scaffold & Style System
**Goal**: A running Streamlit app with the complete visual foundation — dark theme, glassmorphism CSS system, typography, and sidebar navigation — so every subsequent screen can be built without touching config or styles again.
**Depends on**: Nothing (first phase)
**Requirements**: FOUND-01, FOUND-02, FOUND-03, FOUND-04, FOUND-05, FOUND-06, FOUND-07, NAV-01, NAV-02, NAV-03, NAV-04
**Success Criteria** (what must be TRUE):
  1. `streamlit run app.py` launches with no errors and renders a dark (#0A0A0F) background with no Streamlit chrome (no hamburger, footer, deploy button, or top bar)
  2. Left sidebar shows 5 nav items (Landing, Market Analysis, Model & Data, Results & Decision, Prompt Log); clicking any item highlights it with a cyan left border and switches the active screen without a full page reload
  3. A glassmorphism panel (`div.glass-panel`) rendered on any screen shows backdrop blur, rgba background, and cyan border glow — visually matching the design spec
  4. Inter and JetBrains Mono fonts load correctly (visible difference between UI labels and data values)
  5. All CSS is injected from a single `core/styles.py` call — no inline style blocks exist in any screen file
**Plans**: TBD
**UI hint**: yes

### Phase 2: Landing Screen
**Goal**: The landing screen is fully functional and animated — analysts see the pulsing AI Core orb, can enter bank names, choose analysis mode, and launch the workflow.
**Depends on**: Phase 1
**Requirements**: LAND-01, LAND-02, LAND-03, LAND-04, LAND-05, LAND-06, LAND-07
**Success Criteria** (what must be TRUE):
  1. Landing screen centers the AI Core orb as the visual focal point; concentric glow rings and orbiting particle dots animate continuously on a 3-second cycle without any user interaction
  2. Two text input fields accept bank names with placeholder hints ("VR Bank Musterstadt"); a mode toggle switches between "Forward Analysis" and "Backtesting"
  3. Clicking "START ANALYSIS" causes the orb to switch to a faster pulse (0.8s cycle) and navigates the user to the Market Analysis screen
  4. Bank names and selected mode entered on the landing screen are available in session state on subsequent screens
**Plans**: TBD
**UI hint**: yes

### Phase 3: Analysis Screens
**Goal**: Both analysis screens are populated with mock data and fully interactive — Market Analysis shows dual-bank KPI cards and a radar chart; Model & Data shows the 5-step pipeline and adjustable synergy sliders.
**Depends on**: Phase 2
**Requirements**: MARK-01, MARK-02, MARK-03, MARK-04, MARK-05, MODEL-01, MODEL-02, MODEL-03, MODEL-04, MODEL-05
**Success Criteria** (what must be TRUE):
  1. Market Analysis screen shows two columns — Bank A in cyan, Bank B in violet — each with 7 KPI cards (Total Assets, Tier-1 Capital, C/I Ratio, NPL Ratio, ROE, Branch Count, Member Count) drawn from mock data, all inside glassmorphism panels
  2. Bank names entered on the landing screen appear as column headers on the Market Analysis screen
  3. A Plotly radar chart renders below the KPI cards with both banks overlaid in their respective accent colors on a dark transparent background
  4. Model & Data screen displays a horizontal 5-step pipeline (Input → Preprocessing → Synergy Weighting → KI Evaluation → Output) with the active step highlighted in cyan
  5. Five synergy sliders (Cost Reduction, Revenue Enhancement, Capital Optimization, IT Consolidation, Member Retention) are interactive and their values persist in session state, wrapped in a glassmorphism panel
**Plans**: TBD
**UI hint**: yes

### Phase 4: Decision & Log Screens
**Goal**: The Results & Decision screen delivers a clear mock GO verdict with supporting charts; the Prompt Log screen reads and renders a CSV file with color-coded row styling — completing the full analyst workflow.
**Depends on**: Phase 3
**Requirements**: RES-01, RES-02, RES-03, RES-04, RES-05, LOG-01, LOG-02, LOG-03, LOG-04, LOG-05, LOG-06
**Success Criteria** (what must be TRUE):
  1. Results & Decision screen shows a large "GO" hero element in green (#00FF88) with matching glow as the visual centerpiece
  2. A mock comparison table and Plotly bar charts render below the hero element, all wrapped in glassmorphism panels on a dark background
  3. Prompt Log screen reads `prompt_log.csv` from the project root and renders all 7 columns as a styled HTML table (not default st.dataframe styling) inside a glassmorphism panel
  4. Table rows with `P-DEV-XX` IDs show an Electric Blue (#0066FF) left border; rows with `P-XX` IDs show an Electric Cyan (#00D4FF) left border
  5. Running `streamlit run app.py` and navigating all 5 screens completes without errors — the full v1 GUI shell is working end-to-end
**Plans**: TBD
**UI hint**: yes

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Scaffold & Style System | 0/TBD | Not started | - |
| 2. Landing Screen | 0/TBD | Not started | - |
| 3. Analysis Screens | 0/TBD | Not started | - |
| 4. Decision & Log Screens | 0/TBD | Not started | - |
