# Restaurant Business Rankings 2020 – Analytical Dashboard

Professional Python + Streamlit project for descriptive and light predictive analysis of the 2020 Restaurant Business rankings (Top 250, Independence 100, Future 50).

---

## Project structure

```
Restaurant_Business_Rankings_2020/
├── data/
│   ├── raw/                 # Original CSVs
│   ├── processed/           # Cleaned analysis-ready tables
│   └── external/
├── docs/                    # Charter, quality, cleaning, EDA, modelling, dashboard, handover
├── src/
│   ├── data/                # Cleaning scripts
│   ├── models/              # Training scripts
│   └── visualization/       # EDA scripts
├── app/                     # Streamlit dashboard
├── models/                  # Saved model artefacts
├── reports/                 # Charts and evaluation figures
├── requirements.txt
└── README.md
```

---

## Delivery status

| Phase | Name                        | Status  | Key output |
|-------|-----------------------------|---------|------------|
| 1     | Planning & Setup            | ✅ Done | Project charter + structure |
| 2     | Data Understanding          | ✅ Done | Data quality report |
| 3     | Data Cleaning & Preparation | ✅ Done | Clean CSVs in `data/processed/` |
| 4     | Exploratory Data Analysis   | ✅ Done | Insights + charts in `reports/` |
| 5     | Modelling                   | ✅ Done | Models + metrics in `models/` |
| 6     | Dashboard Development       | ✅ Done | Streamlit app with top nav |
| 7     | Documentation & Handover    | ✅ Done | User guide + handover pack |

---

## Run the dashboard

```bash
cd Restaurant_Business_Rankings_2020
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

### Dashboard features

- **Top navigation** (no left sidebar)
- **Consistent cards** and dark futuristic theme
- **Filters + downloads** on each ranking page
- **Growth & Models** view with aligned evaluation visuals
- **AI Assistant** with ready-made question dropdown + optional free text
- **Help Guide** explaining navigation, rankings, and every KPI in plain language
- **Export** of full cleaned datasets and an insight summary

---

## Data in scope

Only these three ranking files:

- **Top250** – Rank, Restaurant, Sales, YOY_Sales, Units, YOY_Units, Headquarters, Segment_Category  
- **Independence100** – Rank, Restaurant, Sales, Average Check, City, State, Meals Served  
- **Future50** – Rank, Restaurant, Location, Sales, YOY_Sales, Units, YOY_Units, Unit_Volume, Franchising  

---

## Documentation index

| Document | Path |
|----------|------|
| Project charter | `docs/01_PROJECT_CHARTER.md` |
| Data quality report | `docs/02_DATA_QUALITY_REPORT.md` |
| Cleaning log | `docs/03_DATA_CLEANING_LOG.md` |
| EDA insights | `docs/04_EDA_INSIGHTS.md` |
| Modelling report | `docs/05_MODELLING_REPORT.md` |
| Dashboard notes | `docs/06_DASHBOARD_NOTES.md` |
| **Handover & user guide** | `docs/07_HANDOVER_AND_USER_GUIDE.md` |

Start with **`docs/07_HANDOVER_AND_USER_GUIDE.md`** for run instructions, glossary, and limitations.

---

## Reproducibility

```bash
# Clean data
python src/data/clean_rankings.py

# EDA charts
python src/visualization/eda_rankings.py

# Models
python src/models/train_models.py

# Dashboard
streamlit run app/streamlit_app.py
```

---

**Project status: Complete and ready for use.**
