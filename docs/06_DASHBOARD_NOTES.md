# Phase 6 – Streamlit Dashboard Notes

**Date:** 2026-11-11  
**App entry point:** `app/streamlit_app.py`

## Design principles applied

1. **Consistency of cards & layout**  
   - Shared CSS variables for background, border, accent, radius  
   - All KPI blocks use Streamlit `st.metric` styled uniformly  
   - Section headers and insight boxes follow the same pattern on every page  

2. **Color theme (futuristic dark)**  
   - Primary background: deep navy `#0a0e17`  
   - Cards: `#1a2332` with subtle border `#2a3a4f`  
   - Accent: cyan `#00e5ff` / teal `#64ffda`  
   - Semantic: success green, warning amber, danger red  

3. **Lively & professional**  
   - Gradient title text  
   - Hover glow on cards and buttons  
   - Plotly charts with transparent backgrounds matching the theme  
   - Glow divider lines under page titles  

4. **AI Assistant**  
   - Rule-based + data-aware agent (no external API required)  
   - Answers: top growers, decliners, segments, franchising, states, chicken chains, restaurant lookup, summary  
   - Chat history in session state; clearable  

5. **Downloads**  
   - Filtered CSV on each explorer page  
   - Full clean datasets + text insight summary in Export Center  

## How to run

```bash
streamlit run app/streamlit_app.py
```

## Status

Phase 6 complete. Dashboard is ready for interactive use and demonstration.
