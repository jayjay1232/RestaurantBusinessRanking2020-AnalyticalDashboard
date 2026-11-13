# Phase 5 – Modelling Report  
**Restaurant Business Rankings 2020**

**Date:** 2026-11-11  
**Script:** `src/models/train_models.py`  
**Artefacts:** `models/`  
**Plots:** `reports/top250_confusion_matrices.png`, `top250_feature_importance.png`, `top250_roc_curve.png`

---

## 1. Modelling Objectives

| Model | Goal | Target definition | Why this target |
|-------|------|-------------------|-----------------|
| Top250 Binary | Identify chains likely to achieve strong sales growth | `High_Growth = YOY_Sales_pct ≥ 10%` | Separates clear growers from the large “flat / declining” majority |
| Future50 Exploratory | Understand drivers of very high growth | `High_Growth = YOY_Sales_pct ≥ 30%` | Future50 is already a high-growth list; 30% further separates the extreme outliers |

**Design principles**
- Keep models simple and interpretable (small sample sizes).
- Use only structural features available at ranking time (size, segment, franchising) – no leakage from the target-year growth itself beyond the engineered bands.
- Report honest performance; modest predictive power is an expected and useful finding.

---

## 2. Top250 – High Growth Classification

### Target balance
- High Growth (≥10%): **17.6%** (44 chains)
- Not High: **82.4%**

Strong class imbalance → models use `class_weight="balanced"`.

### Features used
- `log_Sales` (log1p of system sales in $M)
- `log_Units`
- `Sales_per_Unit` (Sales_M / Units)
- `Segment_Standard` (one-hot encoded)

### Results (25% hold-out test set)

| Model                | Accuracy | F1 (High Growth) | ROC-AUC |
|----------------------|----------|------------------|---------|
| Logistic Regression  | 0.635    | 0.303            | 0.652   |
| Random Forest        | 0.651    | 0.214            | 0.483   |
| RF 5-fold CV F1      | –        | 0.309 ± 0.059    | –       |

**Interpretation of performance**  
Predictive power is **modest**. Size and segment alone do not strongly determine which large chains will post ≥10% sales growth. This is itself an important business insight: growth in the Top 250 is driven by factors not captured in basic structural variables (brand strength, digital capability, menu innovation, private-equity ownership, regional trends, etc.).

### Most influential signals

**Logistic Regression coefficients (largest absolute values)**
- Negative association: Casual Dining & Italian/Pizza, Family Casual, Sandwich, Seafood, Varied Menu
- Positive association: Fast Casual & Burger, Fast Casual & Chicken, Fast Casual & Sandwich, Sales_per_Unit

**Random Forest feature importances**
1. Sales_per_Unit (0.27)
2. log_Units (0.26)
3. log_Sales (0.19)
4. Then segment indicators (QS Burger, Italian/Pizza, Steak, Pizza …)

Higher unit productivity and certain fast-casual / chicken / burger segments are the clearest structural correlates of higher growth probability.

### Artefacts saved
- `models/top250_rf_high_growth.joblib`
- `models/top250_lr_high_growth.joblib`
- `models/top250_scaler.joblib`
- `models/top250_feature_names.joblib`
- Confusion matrices, feature-importance plot, ROC curve in `reports/`

---

## 3. Future50 – Growth Driver Analysis

Because n = 50, modelling is treated as **exploratory only** (no reliable held-out evaluation).

### Observations
- Franchised concepts show higher average YOY sales growth (37% vs 29%) and much higher average unit counts (45 vs 20).
- Non-franchised concepts have substantially higher average unit volume ($2,381 vs $1,022) – consistent with more premium, limited-footprint brands.
- Strong correlation between YOY Sales and YOY Units (0.90) – growth is largely expansion-driven.
- Sales size itself is weakly or negatively correlated with growth rate (smaller concepts in this list grew faster).

### Simple logistic model (in-sample)
- Accuracy ≈ 0.74, F1 ≈ 0.70 (in-sample – optimistic)
- Coefficients suggest more units → higher probability of extreme growth; higher unit volume and larger sales → slightly lower probability of being in the ≥30% tail.

**Conclusion for Future50:** The dominant story remains descriptive – almost the entire list is high-growth. Structural variables explain only a modest additional slice of who is in the extreme tail.

---

## 4. Key Takeaways for the Dashboard & Business Story

1. **Growth is hard to predict from size and segment alone** in the Top 250. The model’s modest performance is a feature, not a bug – it tells us that the “winners” are differentiated by factors beyond basic scale and category.
2. **Unit productivity (Sales per Unit)** and membership in certain fast-casual / chicken / burger segments are the strongest structural signals we do have.
3. **Future50** is best presented descriptively (growth distribution, franchising split, unit-volume leaders) rather than with a high-stakes predictive model.
4. For the Streamlit app we can still surface:
   - Model-based “High Growth probability” score for Top250 chains (with clear caveats)
   - Feature-importance / coefficient view so users understand what the model is using
   - Side-by-side actual vs predicted for transparency

---

## 5. Limitations & Future Improvements

- Small number of positive High-Growth cases → F1 remains modest.
- Segment one-hot creates high dimensionality relative to n=250.
- No external features (demographics, digital scores, ownership type, same-store sales history).
- Possible next steps if more data becomes available: richer feature set, ordinal regression on growth bands, or survival-style analysis of sustained growers.

---

## 6. How to re-run

```bash
cd Restaurant_Business_Rankings_2020
python src/models/train_models.py
```

Metrics are also written to `models/model_metrics.json`.

---

**Phase 5 status: Complete.**  
Ready for **Phase 6 – Streamlit Dashboard Development**.
