# Phase 7 – Project Handover & User Guide  
**Restaurant Business Rankings 2020 Analytical Dashboard**

**Document version:** 1.0  
**Date:** 2026-11-11  
**Status:** Final handover

---

## 1. Purpose of this document

This package closes the project lifecycle. It records:

- What was delivered  
- How to run and use the system  
- How the data and models were prepared  
- Plain-language explanations of KPIs and fields  
- Known limitations and recommended next steps  

It is intended for analysts, stakeholders, and anyone who will operate or extend the dashboard.

---

## 2. Deliverables checklist

| Item | Location | Status |
|------|----------|--------|
| Project charter | `docs/01_PROJECT_CHARTER.md` | Done |
| Data quality report | `docs/02_DATA_QUALITY_REPORT.md` | Done |
| Cleaning log | `docs/03_DATA_CLEANING_LOG.md` | Done |
| EDA insights | `docs/04_EDA_INSIGHTS.md` | Done |
| Modelling report | `docs/05_MODELLING_REPORT.md` | Done |
| Dashboard notes | `docs/06_DASHBOARD_NOTES.md` | Done |
| This handover & user guide | `docs/07_HANDOVER_AND_USER_GUIDE.md` | Done |
| Raw data | `data/raw/` | Done |
| Cleaned data | `data/processed/` | Done |
| Cleaning script | `src/data/clean_rankings.py` | Done |
| EDA script | `src/visualization/eda_rankings.py` | Done |
| Modelling script | `src/models/train_models.py` | Done |
| Model artefacts | `models/` | Done |
| Charts | `reports/` | Done |
| Streamlit application | `app/streamlit_app.py` | Done |
| Requirements | `requirements.txt` | Done |
| Project README | `README.md` | Done |

---

## 3. How to run the dashboard

```bash
cd Restaurant_Business_Rankings_2020
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Open the local URL shown in the terminal (typically `http://localhost:8501`).

**Minimum packages:** pandas, numpy, streamlit, plotly, scikit-learn, joblib, matplotlib, seaborn.

---

## 4. Application structure (user-facing)

Navigation is a **top menu** (no left sidebar):

| Section | Purpose |
|---------|---------|
| **Overview** | KPI snapshot and key highlights |
| **Top 250** | Filterable table, charts, leaders, CSV download |
| **Independence 100** | State filter, table, charts, download |
| **Future 50** | Franchising filter, growth charts, download |
| **Growth & Models** | Segment performance, model metrics, evaluation visuals |
| **AI Assistant** | Guided questions (dropdown) + optional free text |
| **Export** | Full cleaned CSVs + insight summary text |
| **Help Guide** | How to use the app + glossary of fields and KPIs |

Design principles applied:

- Consistent metric cards and section spacing  
- Dark futuristic theme (navy + cyan accents)  
- Interactive Plotly charts  
- Equal treatment of model evaluation images  
- No internal process labels (e.g. “Phase 1–7”) in the UI  

---

## 5. Plain-language glossary (KPIs & fields)

| Term | Simple meaning |
|------|----------------|
| **Sales / Sales_M** | Total system sales. Shown in millions of dollars for easy comparison. |
| **YOY Sales %** | How much sales grew or fell compared with the previous year. Positive = growth; negative = decline. |
| **Units** | Number of restaurant locations. |
| **YOY Units %** | Change in the number of locations versus last year. |
| **Unit volume** | Approximate average sales per location (Future 50). Higher often means stronger single-store performance. |
| **Average check** | Typical spend per guest visit (Independence 100). |
| **Meals served** | Estimated number of covers / meals in the period — a volume measure. |
| **Segment** | Type of restaurant (e.g. Quick Service & Burger, Casual Dining & Steak). |
| **Growth band** | Grouped YOY sales growth: High ≥20%, Moderate 5–20%, Low 0–5%, Negative &lt;0%. |
| **Franchising** | Whether the brand uses franchise partners (Yes) or is mainly company-run (No). |
| **High growth (models)** | Label used in modelling: Top 250 chain with YOY sales ≥ 10%. |

---

## 6. Data pipeline (for maintainers)

1. **Raw** files in `data/raw/` (Top250, Independence100, Future50).  
2. **Cleaning** via `python src/data/clean_rankings.py` → writes `data/processed/*_clean.csv`.  
3. **EDA** via `python src/visualization/eda_rankings.py` → charts in `reports/`.  
4. **Models** via `python src/models/train_models.py` → artefacts in `models/` and evaluation plots in `reports/`.  
5. **Dashboard** reads only cleaned tables from `data/processed/`.

Re-run cleaning before EDA/models if raw files change.

---

## 7. Modelling summary (honest limits)

- Target: High growth = YOY sales ≥ 10% (Top 250).  
- Features: log sales, log units, sales per unit, segment.  
- Logistic regression ROC-AUC ≈ 0.65; random-forest CV F1 ≈ 0.31.  
- **Interpretation:** Size and segment alone do not strongly predict growth. That finding is intentional and useful — growth depends on brand, operations, digital capability, ownership, and market factors not in this dataset.

Future 50 modelling is exploratory only (n = 50).

---

## 8. AI Assistant behaviour

- No external LLM API required.  
- Answers are produced from the live dataframes in the app.  
- Primary UX: **dropdown of ready-made questions** + optional free-text / restaurant name.  
- Supported topics: top growers, decliners, largest by sales, segments, franchising, states, chicken chains, counts, restaurant lookup, overall highlights.

---

## 9. Known limitations

- Sales scale differs by source list (millions vs full dollars); cleaned tables expose a consistent `Sales_M` where relevant.  
- Segment labels in the original Top 250 were inconsistent; a pragmatic standardisation map was applied.  
- `Content` and `Headquarters` in Top 250 are mostly missing and are not used in models.  
- Predictive models are descriptive decision-support tools, not production scoring engines.  
- AI assistant is rule- and data-driven; it does not invent facts outside the loaded tables.

---

## 10. Recommended next steps (optional)

1. Add external features (region demographics, digital scores, ownership type) if available.  
2. Deploy Streamlit via Streamlit Community Cloud, Docker, or an internal server.  
3. Schedule a light refresh process if newer ranking years are published.  
4. Extend the AI assistant with additional scripted question templates as users request them.

---

## 11. Sign-off

| Role | Responsibility | Status |
|------|----------------|--------|
| Analytics / build | End-to-end pipeline, dashboard, documentation | Complete |
| Stakeholder review | Validate that KPIs and narratives match business needs | Pending user |
| Operations | Host and monitor the Streamlit app | Pending user |

**Project status: Ready for use and demonstration.**

---

*End of handover document.*
