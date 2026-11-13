# Phase 2 – Data Quality & Understanding Report  
**Restaurant Business Rankings 2020**

**Date:** 2026-11-11  
**Files examined:**  
- `data/raw/Future50.csv`  
- `data/raw/Independence100.csv`  
- `data/raw/Top250.csv`

---

## 1. Summary Overview

| Dataset            | Rows | Columns | Missing Values | Duplicates | Notes |
|--------------------|------|---------|----------------|------------|-------|
| Future50           | 50   | 9       | 0              | 0          | Clean; YOY columns are strings with % |
| Independence100    | 100  | 7       | 0              | 0          | Clean; Sales & Meals Served are large numbers |
| Top250             | 250  | 9       | Content: 217<br>Headquarters: 198 | 0 | Content & HQ mostly empty; YOY columns are strings |

All three files loaded successfully with no duplicate rows and no completely empty columns of critical interest.

---

## 2. Schema & Column Details

### Future50
| Column        | Dtype  | Description / Notes |
|---------------|--------|---------------------|
| Rank          | int64  | 1–50 |
| Restaurant    | str    | Unique names |
| Location      | str    | City, State (e.g. "Seattle, Wash.") – 39 unique |
| Sales         | int64  | System sales (appears to be in $ millions) – range 20–49 |
| YOY_Sales     | str    | Growth % as string (e.g. "130.5%") – needs conversion |
| Units         | int64  | Number of units – range 7–105 |
| YOY_Units     | str    | Unit growth % as string – needs conversion |
| Unit_Volume   | int64  | Average unit volume – range 465–4300 |
| Franchising   | str    | "Yes" / "No" (29 Yes, 21 No) |

### Independence100
| Column         | Dtype   | Description / Notes |
|----------------|---------|---------------------|
| Rank           | int64   | 1–100 |
| Restaurant     | str     | 95 unique (some multi-location brands appear more than once) |
| Sales          | float64 | Absolute $ sales – range ~11.4M – 39.1M |
| Average Check  | int64   | $ – range 17–194 |
| City           | str     | 36 unique |
| State          | str     | 19 unique (N.Y. 21, Ill. 18, Calif. 12, Nev. 11, Fla. 9, D.C. 9 …) |
| Meals Served   | float64 | Volume – range ~87k – 959k |

### Top250
| Column           | Dtype  | Description / Notes |
|------------------|--------|---------------------|
| Rank             | int64  | 1–250 |
| Restaurant       | str    | Chain name |
| Content          | str    | Editorial text – **only 33 non-null** (mostly NaN) |
| Sales            | int64  | System sales (appears $ millions) – range 126 – 40,412 |
| YOY_Sales        | str    | Growth % string – needs conversion |
| Units            | int64  | Unit count – range 13 – 23,801 |
| YOY_Units        | str    | Unit growth % string – needs conversion |
| Headquarters     | str    | **Only 52 non-null** |
| Segment_Category | str    | High cardinality; mix of full labels (“Quick Service & Burger”) and short labels (“Burger”, “Steak”) |

---

## 3. Key Data Quality Issues Identified

1. **Percentage columns stored as strings**  
   - Future50: `YOY_Sales`, `YOY_Units`  
   - Top250: `YOY_Sales`, `YOY_Units`  
   → Must strip “%” and convert to float for analysis/modelling.

2. **Inconsistent Segment_Category labelling (Top250)**  
   - Some rows use full “Quick Service & Burger”, others just “Burger”, “Steak”, “Mexican”, etc.  
   → Needs standardization / mapping in cleaning phase.

3. **Sparse columns in Top250**  
   - `Content` (editorial) → 87% missing → keep for optional display only, do not use in models.  
   - `Headquarters` → 79% missing → low utility for most analyses.

4. **Sales scale difference**  
   - Future50 & Top250: Sales appear to be in **millions of dollars**.  
   - Independence100: Sales are full dollar amounts (millions already expanded).  
   → Important when comparing across datasets.

5. **Location parsing**  
   - Future50 `Location` and Independence100 `City`/`State` will benefit from consistent city/state extraction.

6. **Restaurant name as join key**  
   - Names are unique within Future50.  
   - Independence100 has a few repeated brand names (different locations).  
   - Top250 names are unique.  
   - Cross-dataset joins on exact name will have limited overlap (different universes: large chains vs independents vs emerging).

---

## 4. Basic Statistics Snapshot

**Future50**  
- Avg Sales: ~$33.8 M  
- Avg Units: ~35  
- Avg Unit Volume: ~1,593  
- Franchising: 58% Yes

**Independence100**  
- Avg Sales: ~$17.8 M  
- Avg Check: $69  
- Avg Meals Served: ~317 k  
- Strong concentration in N.Y., Illinois, California, Nevada, Florida, D.C.

**Top250**  
- Heavily right-skewed (McDonald’s $40 B+ dominates)  
- Median Sales ~$330 M, Median Units ~207  
- Top segments by count: Varied Menu, Mexican, Quick Service & Burger, Italian/Pizza, Burger, Family Style

---

## 5. Recommendations for Phase 3 (Cleaning)

1. Convert all `YOY_*` columns to numeric (remove “%”, handle any remaining non-numeric).  
2. Standardize `Segment_Category` into a consistent hierarchy (Service Type + Cuisine/Concept).  
3. Parse Location / City / State into clean columns.  
4. Add derived flags: `Is_Franchised`, `Sales_Millions`, growth categories (High/Medium/Low/Negative).  
5. Decide treatment of sparse columns (Content, Headquarters) – keep or drop for modelling.  
6. Create a unified “analysis-ready” view if cross-ranking analysis is desired, or keep the three tables separate with clear documentation.  
7. Save cleaned versions as Parquet or CSV in `data/processed/`.

---

## 6. Next Step

Proceed to **Phase 3 – Data Cleaning & Preparation**.

A cleaning script will be created under `src/data/` that:
- Loads the three raw files  
- Applies the transformations above  
- Writes clean tables to `data/processed/`  
- Produces a short cleaning log.

---

**Report status:** Complete – ready for cleaning phase.
