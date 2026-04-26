# Feature Landscape: MIA — Merger Intelligence Agent

**Domain:** Financial analytics SPA / AI-powered M&A decision tool
**Aesthetic target:** Futuristic AI instrument, not a generic BI dashboard
**Target users:** Banking analysts evaluating Volksbank/Raiffeisenbank mergers
**Researched:** 2026-04-26
**Confidence:** MEDIUM-HIGH (Streamlit + CSS patterns from training; no live doc access this session)

---

## Table Stakes

Features analysts expect. Missing = app feels unfinished or untrustworthy.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Dark background (true dark, not grey) | Financial terminal aesthetic; reduces eye strain in analysis sessions | Low | `#0a0a0f` or similar near-black, not Streamlit's default `#0e1117` grey which reads "demo" |
| Consistent color semantics per bank | Dual-bank comparison is core; users must never confuse Bank A/B | Low | Assign cyan (`#00d4ff`) to Bank A, violet (`#8b5cf6`) to Bank B — never swap |
| Responsive KPI cards with delta indicators | Analysts scan metrics first; cards without deltas feel like raw data dumps | Medium | Show current value + YoY or peer delta; color-code positive/negative |
| Readable data tables with alternating rows | Prompt log and comparison tables must be scannable at speed | Low | Zebra striping on dark backgrounds requires explicit CSS; Streamlit default is invisible |
| Loading/progress states | LLM calls take 2–10 seconds; blank screen breaks trust | Medium | Spinner or animated placeholder during API calls |
| Clear navigation between screens | 5-screen SPA needs orientation cues so analysts don't get lost | Medium | Sidebar or persistent top nav with active-state highlight |
| Input validation feedback | Bank name inputs must reject garbage; analysts need immediate feedback | Low | Inline error state on text inputs, not just st.error() at bottom |
| Sticky header / screen title | Analysts need to know which screen they're on at all times | Low | Fixed title bar with screen name + bank pair being analyzed |
| Export capability (PDF or CSV) | Analysis outputs must be shareable for internal memos | High | Even a basic st.download_button() for CSV satisfies this; PDF is harder |
| Audit trail (Prompt Log screen) | Compliance-adjacent users need to see what queries produced which outputs | Low (screen exists) | Already planned as Screen 5 — must be complete, not placeholder |

---

## Differentiators

Features analysts won't expect but that immediately signal "real product." These create the "futuristic AI tool" impression.

### Visual Identity

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Animated AI orb on landing | Signals AI-native product before user reads a word; sets premium tone | Medium | CSS radial-gradient sphere + `@keyframes` pulse + rotating conic-gradient halo; no canvas/WebGL needed for convincing effect |
| Glassmorphism card surfaces | Depth cue that separates content layers visually; looks expensive | Medium | `backdrop-filter: blur(20px)` + `background: rgba(255,255,255,0.04)` + `border: 1px solid rgba(255,255,255,0.08)` — the border is what separates real glass from fake |
| Dual-color ambient glow per bank | Instantly communicates Bank A vs Bank B ownership of data without reading labels | Medium | Box-shadow with bank color at low opacity (`box-shadow: 0 0 40px rgba(0,212,255,0.15)`) on Bank A cards |
| Particle background (subtle) | Reinforces "data-rich" and "AI processing" aesthetic | High | CSS-only particles are achievable but heavy; prefer 8–12 static `position:fixed` orbs with slow `@keyframes` float rather than JS particle libraries |
| Typed/revealed text on landing | "Analysiere Fusion..." feel; signals live AI computation | Low | CSS `@keyframes typing` on the subtitle line; 40-char limit for readability |

### Navigation & Structure

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Horizontal step-indicator navigation | Shows analysts where they are in the 5-screen workflow; feels like a tool, not a website | Medium | Custom CSS progress bar with numbered steps; active step glows in accent color |
| Smooth screen transitions | Eliminates the jarring Streamlit full-page reload feel | High | `st.session_state` + conditional rendering + CSS `opacity` fade-in on container mount; full SPA routing requires streamlit-router or manual state machine |
| Keyboard shortcut hints | Power users (analysts) prefer keyboard over mouse | Medium | Display `[→]` next hints in corners; actual hotkey binding requires st.components.v1 JS injection |

### Data Visualization

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Radar/spider chart with dual-bank overlay | Multi-dimensional comparison (capital ratios, cost efficiency, NPS, etc.) in one view; impossible to fake with bar charts | Medium | Plotly `go.Scatterpolar` with `fill='toself'`; use bank colors at 0.3 opacity fill; dark paper/plot bgcolor required |
| GO/NO-GO hero with animated reveal | Decision screen becomes a moment of truth; analysts remember it | Medium | Large centered badge with conditional color (`#00ff88` GO / `#ff4444` NO-GO) + CSS pulse ring animation; text should be the largest element on screen |
| Confidence score ring | Quantifies AI certainty; analysts distrust binary outputs without uncertainty metrics | Medium | SVG circle with `stroke-dasharray` animation from 0 to score%; pairs with GO/NO-GO |
| Synergy slider with live recalculation | Analysts need to stress-test assumptions; static outputs feel like black boxes | High | `st.slider()` + `st.session_state` reactive recompute; show EUR value updating in real-time |
| Horizontal pipeline visualization | 5-step data flow (Ingest → Clean → Score → Model → Output) should be visible, not assumed | Medium | Custom HTML/CSS horizontal stepper with connector lines; Streamlit has no native stepper component |

### Micro-interactions

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Hover glow on KPI cards | Tactile feedback; confirms the UI is alive | Low | CSS `:hover` with `box-shadow` transition on `.stMetric` override |
| CTA button shimmer on hover | Landing screen CTA should feel inviting, not static | Low | CSS `@keyframes` linear-gradient sweep across button background |
| Number counter animation on KPI reveal | Metric values that count up from 0 feel computed, not pasted | High | Requires JS via `st.components.v1.html()`; consider whether worth complexity |
| Pulsing status dot (AI processing indicator) | Shows system is working during LLM calls | Low | CSS `@keyframes` scale pulse on a 8px circle; pair with "Analysiere..." text |

---

## Anti-Features

Things to explicitly NOT build or deliberately suppress. These break the premium aesthetic or waste analyst time.

### Streamlit Defaults to Suppress via CSS

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Streamlit hamburger menu (top-right) | Exposes "Made with Streamlit" and deploy options; breaks the product illusion | Hide via `#MainMenu {visibility: hidden}` + `footer {visibility: hidden}` in `st.markdown()` |
| Default Streamlit footer | "Made with Streamlit · Manage app" reads as prototype, not product | Same CSS suppression as hamburger menu |
| Default metric widget styling | Gray background, left-aligned, no visual hierarchy — looks like a code demo | Override `.stMetric` container with custom card CSS via `st.markdown()` |
| Streamlit default blue button | `#FF4B4B` red primary or default blue both scream "Streamlit tutorial" | Override `.stButton > button` with brand accent color + border-radius + no box-shadow default |
| White/light sidebar | Streamlit sidebar in light themes breaks dark immersion if not explicitly styled | Force dark sidebar: `[data-testid="stSidebar"] {background: #0d0d14}` |
| `st.warning()` / `st.error()` yellow/red boxes | Default Streamlit alert boxes have rounded-rect borders that look like system alerts, not financial tool feedback | Use custom HTML alert components via `st.markdown()` with styled divs |
| Wide padding on mobile | Streamlit's default padding looks unfinished on narrow screens | Set `layout="wide"` + explicit padding overrides; MIA is desktop-only, so mobile degradation is acceptable |
| st.spinner() default grey spinner | Looks like a browser loading indicator, not an AI processing indicator | Replace with custom animated HTML component (pulsing dots or orbital animation) |

### UX Anti-Patterns

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Too many animations simultaneously | Analysts need to focus; five things moving at once is noise, not premium | Max 2 active animations at any moment; hero orb pulses while everything else is static |
| Neon overload (>3 accent colors) | Glassmorphism aesthetics collapse when every element is a different color | 2 bank colors (cyan, violet) + 1 neutral accent (white/grey) only; no green, orange, yellow accents |
| Particle effects that obscure text | Backgrounds must stay background | Particle opacity max 0.15; z-index strictly below content layer |
| Glassmorphism on glassmorphism (nested) | Two transparent layers stacked create illegible muddy backgrounds | Glass cards on solid dark background only; never glass-on-glass |
| Radar chart without reference polygon | Spider charts without a baseline are uninterpretable; analysts will distrust the output | Always show a gray "industry benchmark" polygon behind the bank polygons |
| GO/NO-GO without reasoning | Binary verdict with no rationale feels like a coin flip; kills analyst trust | GO/NO-GO badge must be paired with a bulleted rationale section (3–5 points minimum) |
| Horizontal scroll in data tables | Analysts won't discover hidden columns; truncation looks like data loss | Either fit all columns in viewport or paginate; 7-column Prompt Log needs responsive column sizing |
| Modal popups | Break the SPA flow and feel like web-1.0 in a futuristic tool | Use expandable sections (`st.expander()`) or inline reveal instead |
| Auto-refresh / polling without indicator | Silent refreshes confuse analysts who think they're looking at stale data | All data refreshes must be user-triggered with explicit timestamp |

### Complexity Anti-Patterns

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Three.js / WebGL orbs | Massively oversized dependency for one hero element; breaks Streamlit's sandboxed iframe model | Pure CSS radial-gradient + conic-gradient orb achieves 90% of the visual at 0% of the dependency cost |
| External particle libraries (tsParticles, particles.js) | JS bundle size + iframe isolation issues in Streamlit; often breaks on re-render | CSS-only floating orbs (`position: fixed`, `border-radius: 50%`, slow `@keyframes` float) |
| D3.js for charts | Huge investment; Plotly covers all required chart types with better Streamlit integration | Use Plotly for all charts; reserve D3 only if Plotly provably cannot meet a requirement |
| Custom fonts via Google Fonts CDN | Network request fails in air-gapped bank environments; delays FCP | Bundle font files locally or use system fonts (Inter is available system-wide on modern macOS/Windows) |

---

## Feature Dependencies

```
Bank inputs validated → Market Analysis screen unlocks
Market Analysis screen → radar chart (requires both bank data)
Synergy sliders → Results recalculation (must be reactive)
Results calculation → GO/NO-GO verdict (depends on scoring model output)
GO/NO-GO verdict → Prompt Log entry (auto-logged on verdict generation)
CSS suppression (hamburger/footer) → All screens (must be applied globally, not per-screen)
Dark theme CSS injection → All screens (st.markdown() in app.py root)
```

---

## Implementation Complexity Summary

| Feature | Complexity | Streamlit-native? | Notes |
|---------|------------|-------------------|-------|
| Dark theme + CSS overrides | Low | Yes (st.markdown) | Single CSS block in root |
| Glassmorphism cards | Low-Medium | Yes (st.markdown) | Wrap metric content in styled div |
| AI orb animation | Medium | Yes (st.markdown + CSS) | No JS needed |
| Horizontal pipeline stepper | Medium | Partial (st.markdown HTML) | Custom HTML component |
| GO/NO-GO hero | Medium | Yes (st.markdown) | Conditional CSS class |
| Confidence ring (SVG) | Medium | Yes (st.markdown SVG) | Inline SVG with CSS animation |
| Radar chart (dual-bank) | Medium | Yes (plotly) | `go.Scatterpolar` |
| Typed text animation | Low | Yes (st.markdown CSS) | Pure CSS |
| Screen transition fade | High | Partial | session_state + JS injection |
| Synergy reactive sliders | High | Yes (st.slider + session_state) | Requires full recompute on change |
| Number counter animation | High | No (requires st.components.v1) | Consider cutting for V1 |
| Keyboard shortcuts | High | No (requires JS injection) | Cut for V1 |

---

## MVP Recommendation

**Build first (table stakes + highest visual impact differentiators):**
1. Global dark CSS injection (suppress hamburger, footer, fix sidebar) — affects every screen
2. Glassmorphism card component (reusable across all 5 screens)
3. Bank color system (cyan/violet) applied consistently everywhere
4. AI orb on landing (CSS only, single hero moment)
5. GO/NO-GO hero with reasoning bullets (trust anchor for the whole app)
6. Radar chart with dual-bank overlay + benchmark polygon
7. Horizontal pipeline stepper on Screen 3 (visual anchor for data flow)

**Defer to V2:**
- Screen transition animations (high complexity, low analyst value)
- Number counter animations (JS injection complexity)
- Keyboard shortcuts (analyst-friendly but non-blocking)
- PDF export (complex; CSV export satisfies compliance need for V1)
- Particle background (visually nice but adds render cost; ship orb first)

---

## Sources

- Streamlit theming documentation (training data, HIGH confidence for CSS injection patterns)
- Plotly Scatterpolar documentation (training data, HIGH confidence for radar chart API)
- Glassmorphism CSS patterns from ui.glass and Figma community (training data, MEDIUM confidence — verify `backdrop-filter` browser support in analyst's target browser)
- Financial dashboard UX patterns (training data, MEDIUM confidence — verified against analyst workflow expectations)
- Note: WebSearch, Bash, and WebFetch tools were unavailable this session. All findings are from training data (cutoff August 2025). CSS patterns should be smoke-tested against current Streamlit version before finalizing.
