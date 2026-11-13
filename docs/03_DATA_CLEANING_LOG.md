# Phase 3 – Data Cleaning & Preparation Log  
**Restaurant Business Rankings 2020**

**Date:** 2026-11-11  
**Script:** `src/data/clean_rankings.py`  
**Input:** `data/raw/*.csv`  
**Output:** `data/processed/*_clean.csv`

---

## Transformations Applied

### Common
- Converted percentage strings (`YOY_Sales`, `YOY_Units`) → numeric columns `YOY_Sales_pct`, `YOY_Units_pct`
- Created growth-band categories: High (≥20%), Moderate (5–20%), Low (0–5%), Negative
- No rows were dropped; no imputation performed (data was already complete for core metrics)

### Future50
- Renamed `Sales` → `Sales_M` (already in $ millions)
- Renamed `Unit_Volume` → `Unit_Volume_Avg`
- Added `Is_Franchised` (boolean from “Yes”/“No”)
- Parsed `Location` → `City` + `State`
- Added `Sales_Growth_Band` and `Units_Growth_Band`

### Independence100
- Created `Sales_M` = Sales / 1 000 000 (for cross-dataset comparability)
- Renamed `Average Check` → `Avg_Check`, `Meals Served` → `Meals_Served`
- Stripped whitespace from City and State

### Top250
- Created `Sales_M` (alias of Sales – already in $ millions)
- Standardised `Segment_Category` → `Segment_Standard` using a mapping of short labels to full hierarchical labels
- Added growth-band columns
- Left `Content` and `Headquarters` unchanged (high missingness; kept for optional display only)

---

## Output Files

| File                              | Shape   | Key new columns                                      |
|-----------------------------------|---------|------------------------------------------------------|
| Future50_clean.csv                | 50 × 16 | YOY_*_pct, Is_Franchised, City, State, *_Growth_Band |
| Independence100_clean.csv         | 100 × 10| Sales_M, Avg_Check, Meals_Served                     |
| Top250_clean.csv                  | 250 × 14| YOY_*_pct, Segment_Standard, Sales_M, *_Growth_Band  |

---

## Validation Snapshot (post-clean)

**Future50** – first 3 YOY_Sales_pct values: 130.5, 121.9, 81.0 (correctly numeric)

**Top250 – Segment_Standard (top counts after standardisation)**
- Casual Dining & Varied Menu: 31
- Quick Service & Burger: 23
- Quick Service & Pizza: 17
- Family Dining & Family Style: 17
- Quick Service & Mexican: 16
- …

**Independence100 – Sales_M**
- Mean ≈ 17.83, Median ≈ 17.30, Min ≈ 11.39, Max ≈ 39.08

---

## Known Remaining Considerations

1. Segment mapping is pragmatic, not exhaustive – a few rare labels may still be imperfect.
2. Sales scale difference between Independence100 (full $) and the other two (millions) is now explicit via the `Sales_M` column.
3. Restaurant name remains the only potential cross-dataset key; overlap is expected to be low.
4. No outlier capping or log transforms applied yet (will be decided during EDA/modelling if needed).

---

## How to re-run

```bash
cd Restaurant_Business_Rankings_2020
python src/data/clean_rankings.py
```

---

