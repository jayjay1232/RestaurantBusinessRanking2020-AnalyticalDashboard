# Project Charter  
**Restaurant Business Rankings 2020 – Analytical Dashboard**

**Project Name:** Restaurant Business Rankings 2020 Analytical Dashboard  
**Version:** 1.0  
**Date:** 2026-11-11  
**Status:** Planning / Initiation  

---

## 1. Project Objective (SMART)

Create a professional, well-documented, Streamlit-hosted analytical dashboard that:

- Provides **descriptive analytics** on the three official 2020 Restaurant Business rankings (Top 250, Independence 100, Future 50).
- Enables exploration of sales, growth (YOY), units, location, segment, franchising, and meal volume patterns.
- Delivers **light predictive modelling** where feasible (e.g., growth classification, segment prediction, or unit-volume forecasting) using clean, reproducible Python pipelines.
- Follows a rigorous, phase-based data-science process with full documentation so the work is auditable, reusable, and maintainable.

**Success Criteria:**
- Clean, documented data pipelines from raw CSVs → analysis-ready tables.
- Interactive Streamlit dashboard covering rankings, trends, comparisons, and model insights.
- Complete documentation of every phase (Planning → Understanding → Cleaning → EDA → Modelling → Dashboard → Deployment notes).
- Reproducible environment (requirements.txt + clear folder structure).

## 2. Scope

**In Scope**
- The three ranking datasets only:  
  - Top250  
  - Independence100  
  - Future50  
- Data understanding, quality assessment, cleaning & standardization.  
- Descriptive statistics, rankings, growth analysis, geographic & segment views.  
- Feature engineering suitable for the ranking data.  
- At least one predictive model (classification or regression) with evaluation.  
- Streamlit multi-page or single-page dashboard with filters, charts, and model section.  
- Professional documentation and project structure.

**Out of Scope**
- The unrelated HR / talent datasets (companies, employees, interviews, jobs, etc.).  
- Real-time data scraping or paid report content.  
- Full production MLOps (model registry, automated retraining, etc.).  
- Mobile-native app or non-Streamlit front-ends.

## 3. Data Sources

| File              | Key Fields                                                                 | Rows (approx) | Source                  |
|-------------------|----------------------------------------------------------------------------|---------------|-------------------------|
| Top250            | Rank, Restaurant, Sales, YOY_Sales, Units, YOY_Units, Headquarters, Segment_Category | ~250         | Restaurant Business 2020 |
| Independence100   | Rank, Restaurant, Sales, Average Check, City, State, Meals Served          | ~100         | Restaurant Business 2020 |
| Future50          | Rank, Restaurant, Location, Sales, YOY_Sales, Units, YOY_Units, Unit_Volume, Franchising | ~50     | Restaurant Business 2020 |

Raw files are expected in: `data/raw/`

## 4. High-Level Phases (Process We Will Follow)

1. **Planning & Setup** (current) – Charter, structure, environment  
2. **Data Understanding** – Schema, profiling, quality report  
3. **Data Cleaning & Preparation** – Standardization, missing values, feature engineering  
4. **Exploratory Data Analysis (EDA)** – Insights, visualizations, hypotheses  
5. **Modelling** – Descriptive + predictive models, evaluation  
6. **Dashboard Development** – Streamlit app with interactive views  
7. **Documentation & Handover** – Final reports, README, reproducibility notes  

## 5. Deliverables

- Clean project repository with the structure below  
- Data quality & understanding report  
- Cleaned / processed datasets  
- EDA notebook or scripts + key insights document  
- Trained model(s) + evaluation metrics  
- Working Streamlit dashboard (`app/`)  
- Updated README and phase documentation  

## 6. Constraints & Assumptions

- Data is already available locally with the user.  
- Work will be performed in a reproducible Python environment.  
- Focus remains strictly on the three ranking files to keep analysis coherent.  
- Predictive modelling will be kept realistic given the small sample sizes (especially Future50).  

## 7. Next Immediate Action

Copy the three ranking CSV files into:

```
Restaurant_Business_Rankings_2020/data/raw/
```

Then proceed to **Phase 2 – Data Understanding**.

---

**Prepared for:** Systematic, professional dashboard development process  
**Owner:** Project team  
