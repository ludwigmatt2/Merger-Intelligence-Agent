## Vault Sync (Required)
The knowledge base for this project lives in the Obsidian vault at ~/my-second-brain/.
At the END of every session, before your final response, update:
  ~/my-second-brain/projects/mia-merger-intelligence-agent.md

Write or update these sections in that file:
- **Last session**: Date + 1-line summary of what was done
- **Status**: Current state of the project
- **Decisions**: Any architecture or implementation choices made this session
- **Next steps**: What to pick up next time

---

# MIA — Merger Intelligence Agent

## Prompt Log Rule (REQUIRED)

After every completed development task in this project, append one row to `prompt_log.csv` with these 7 columns:

| Column | Format / Notes |
|--------|---------------|
| `Nr` | `P-DEV-XX` (development prompts, zero-padded) or `P-XX` (AI analysis prompts) |
| `Prompt_Originaltext` | The exact prompt or task description |
| `Zweck_Einsatzbereich` | Purpose / use case (e.g. "GUI Setup", "Datenanalyse", "Synergiemodell") |
| `KI_Modell_Plattform` | Model name and platform (e.g. "claude-sonnet-4-6 / Claude Code") |
| `Datum_Uhrzeit` | ISO format: `YYYY-MM-DD HH:MM` |
| `KI_Antwort_Kurzfassung` | 1-2 sentence summary of what was built or decided |
| `Wissenschaftliche_Validierung` | Validation status: `Ausstehend` / `Validiert` / `Nicht anwendbar` |

**Trigger:** Append a row every time a task is marked complete — code written, file created, architectural decision made, or analysis run.

**Nr sequence:** P-DEV-XX increments across all dev sessions (check the last row in the CSV for the current counter). P-XX (analysis prompts) is separate and populated by the app at runtime.

**Git commit format (Method 2 — Seminar requirement):** Every commit MUST reference the P-DEV number in the message prefix:
```
git commit -m "[P-DEV-XX] <short description of what was built>"
```
Example: `[P-DEV-04] Write app.py: boot sequence, sidebar nav, screen router`
This makes the git log a reproducible development timeline for scientific documentation.

**Wissenschaftliche_Validierung values:**
- `Durch Team geprüft` — visual/manual review by Ludwig
- `Streamlit-Start erfolgreich` — app started without errors
- `Syntax-geprüft, Import-test OK` — Python import + no syntax errors
- `Ausstehend` — not yet reviewed
- `Nicht anwendbar` — infrastructure/config tasks with no testable output

---

## Prompt Log Screen

The Prompt Log screen (`screens/prompt_log.py`) reads `prompt_log.csv` from the project root and renders all rows as a styled table. Row color-coding by type:
- `P-DEV-XX` rows → Electric Blue `#0066FF` left border (development entries)
- `P-XX` rows (no DEV) → Electric Cyan `#00D4FF` left border (AI analysis entries)

---

## Project Overview

MIA (Merger Intelligence Agent) is a Streamlit-based AI analysis application for evaluating German cooperative bank (Volksbank/Raiffeisenbank) mergers. It guides analysts through a 5-screen workflow ending in a GO/NO-GO recommendation.

**Entry point:** `streamlit run app.py`

---

## Commands
```bash
# Run app
streamlit run app.py

# Install dependencies
pip install streamlit==1.54.0 plotly pandas

# Check prompt log
cat prompt_log.csv
```

---

## Source Architecture
```
Merger Intelligence Agent/
├── app.py                    ← Entry point: CSS, state init, router
├── screens/
│   ├── landing.py
│   ├── market_analysis.py
│   ├── model_data.py
│   ├── results.py
│   └── prompt_log.py         ← Reads prompt_log.csv
├── core/
│   ├── state.py              ← Session state schema
│   ├── styles.py             ← CSS loader
│   └── data.py               ← Mock data (Phase 2 swap point)
├── components/
│   ├── orb.py
│   ├── kpi_card.py
│   └── pipeline.py
├── styles/
│   ├── base.css
│   ├── components.css
│   ├── animations.css
│   └── sidebar.css
├── prompt_log.csv            ← Persisted prompt/development log
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── CLAUDE.md
```

---

## Current Status

### ✅ Complete
- Project initialized, .planning/ structure created
- Research complete (STACK, FEATURES, ARCHITECTURE, PITFALLS, SUMMARY)
- REQUIREMENTS.md and ROADMAP.md pending

### ⚠️ Needs Work / Known Gaps
- app.py and all screen files not yet created (Phase 1 execution pending)

---

## Coding Conventions

- All CSS injected via `st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)` from `core/styles.py` — never inline in screen files
- Screens are pure render functions with no arguments — read from `st.session_state` directly
- Mock data lives exclusively in `core/data.py` — never hardcoded in screen files
- Pin `streamlit==1.54.0` — CSS selectors are version-sensitive
- JetBrains Mono for all numeric/data values (CSS class `.mono`)
- Bank A always cyan `#00D4FF`, Bank B always violet `#7B2FBE` — never swap
