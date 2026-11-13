# Phase 4 – Exploratory Data Analysis Insights  
**Restaurant Business Rankings 2020**

**Date:** 2026-11-11  
**Data:** Cleaned tables in `data/processed/`  
**Charts:** `reports/future50_eda.png`, `independence100_eda.png`, `top250_eda.png`, `top250_segment_growth.png`  
**Script:** `src/visualization/eda_rankings.py`

---

## 1. Executive Snapshot

| Ranking | Universe | n | Sales range (approx) | Typical growth | Dominant theme |
|---------|----------|---|----------------------|----------------|----------------|
| **Future50** | Emerging / high-growth concepts | 50 | $20–49 M | Very high (median ~25% YOY) | Rapid expansion, many franchised |
| **Independence100** | Top independent restaurants | 100 | $11–39 M | N/A (no YOY in source) | High-volume, high-check locations in major metros |
| **Top250** | Largest US chains | 250 | $126 M – $40 B | Modest / mixed (many near 0 or negative) | Scale + a few high-growth stars |

The three lists describe **different populations** and should be analysed separately.

---

## 2. Future50 – Emerging Concepts

### Key numbers
- Average system sales: **$33.8 M**
- Average units: **~35**
- Average unit volume: **~$1,593**
- Median YOY sales growth: **~25.5%** (min 14.4%, max 130.5%)
- Franchising: **58% Yes**

### Growth profile
- **38 of 50** chains are in the “High (≥20%)” sales-growth band.
- Only one chain shows low single-digit unit growth; none are negative.
- Top growers: Evergreens (130.5%), Clean Juice (121.9%), Slapfish (81%), Clean Eatz (79.7%), Pokeworks (77.1%).

### Unit economics
Highest average unit volumes belong to more premium / limited-unit concepts:
- Bulla Gastrobar ($4,300), Boqueria ($4,260), Hawkers Asian Street Fare ($3,800).

### Franchising insight
Franchised concepts are the majority. Box-plot comparison shows both franchised and non-franchised groups achieve strong growth; the extreme outliers (Evergreens, Clean Juice) include both models.

**Story:** 2020’s “Future 50” is a list of fast-scaling, mostly franchised concepts that were still relatively small but growing extremely quickly — the opposite of the mature Top 250 universe.

---

## 3. Independence100 – Top Independents

### Key numbers
- Average sales: **$17.8 M**
- Average check: **$69**
- Average meals served: **~317 k**
- Sales range: $11.4 M – $39.1 M

### Geographic concentration
Top states by count of restaurants:
1. N.Y. – 21  
2. Ill. – 18  
3. Calif. – 12  
4. Nev. – 11  
5. Fla. / D.C. – 9 each  

Heavy presence of high-tourism / high-income metros (NYC, Chicago, Las Vegas, Washington DC, South Florida).

### Top performers
**By sales**
1. Carmine’s (Times Square) – $39.1 M  
2. The Boathouse Orlando – $35.2 M  
3. Old Ebbitt Grill – $29.1 M  

**By meals served** (volume play)
1. Zehnder’s of Frankenmuth – 959 k meals  
2. Junior’s (Times Square) – 915 k  
3. Frankenmuth Bavarian Inn – 899 k  

### Correlations
- Sales ↔ Meals Served: **+0.30** (moderate positive)
- Avg Check ↔ Meals Served: **–0.63** (strong inverse – higher-check restaurants serve fewer covers)
- Sales ↔ Avg Check: only **+0.19** (weak)

**Story:** The most successful independents either (a) drive enormous volume at moderate checks (classic American / tourist destinations) or (b) command premium checks with lower volume (steakhouses, fine-dining). Geography is highly concentrated in a handful of destination cities.

---

## 4. Top250 – Largest Chains

### Scale
- McDonald’s alone: **$40.4 B** system sales, 13.8 k units  
- Starbucks: $21.4 B, 15 k units  
- The distribution is extremely right-skewed; median sales ~$330 M, median units ~207.

### Growth distribution (Sales YOY)
| Band              | Count |
|-------------------|-------|
| High (≥20%)       | 11    |
| Moderate (5–20%)  | 65    |
| Low (0–5%)        | 88    |
| Negative          | 86    |

Almost one-third of the Top 250 recorded **negative** sales growth in the ranking year. Growth is highly concentrated among a small set of winners.

### Highest growers (Top 10)
| Rank | Restaurant                  | YOY Sales | Sales ($M) | Segment                      |
|------|-----------------------------|-----------|------------|------------------------------|
| 215  | Chicken Salad Chick         | 39.5%     | 153        | Quick Service & Chicken      |
| 201  | Metro Diner                 | 36.3%     | 171        | Family Dining                |
| 82   | First Watch                 | 35.1%     | 558        | Family Dining                |
| 71   | Shake Shack                 | 31.8%     | 622        | Fast Casual & Burger         |
| 236  | Walk-On’s Sports Bistreaux  | 27.8%     | 133        | Sports Bar                   |
| 235  | Mission BBQ                 | 25.0%     | 136        | BBQ                          |
| 42   | Raising Cane’s              | 23.8%     | 1,466      | Fast Casual & Chicken        |
| 93   | MOD Pizza                   | 23.8%     | 483        | Fast Casual & Pizza          |
| 77   | Tropical Smoothie Cafe      | 21.8%     | 576        | Beverage                     |
| 166  | Lazy Dog                    | 21.3%     | 213        | Varied Menu                  |

### Steepest decliners (Bottom 10)
Houlihan’s (–21.2%), Old Country Buffet (–18.8%), Fuddruckers (–15.8%), McCormick & Schmick’s (–15.6%), Friendly’s (–15.3%), and several other casual / family / buffet concepts.

### Segment performance (segments with ≥5 chains)
Best average YOY sales growth:
1. Quick Service & Chicken – **+6.7%**
2. Fast Casual & Sandwich – **+6.3%**
3. Casual Dining & Steak – **+5.8%**
4. Casual Dining & Sports Bar – **+5.1%**
5. Quick Service & Coffee Cafe – **+4.7%**

Weakest:
- Quick Service & Family Casual – **–6.5%**
- Casual Dining & Italian/Pizza, Seafood, Frozen Desserts – roughly flat to slightly negative
- Many “Varied Menu” casual-dining chains also struggled.

**Story:** Scale does not equal growth. The largest chains grew modestly or declined, while a handful of mid-sized, focused concepts (chicken, breakfast/brunch, better-burger, BBQ, sports bars) delivered standout expansion. Family-casual and traditional buffet formats were under clear pressure.

---

## 5. Cross-Ranking Themes

1. **Growth is polarised**  
   Future50 is almost uniformly high-growth. Top250 is a mix of modest growers and a large negative cohort. The “winners” in Top250 look more like Future50 concepts that have already scaled further.

2. **Chicken is hot**  
   Raising Cane’s, Chicken Salad Chick, and the broader Quick Service / Fast Casual Chicken segment show strong momentum across lists.

3. **Geography of independents**  
   Success for independents is heavily tied to high-traffic destination cities rather than broad geographic coverage.

4. **Franchising as a growth lever**  
   Majority of Future50 concepts are franchised; many of the high-growth Top250 names also have significant franchise footprints.

5. **Check vs Volume trade-off**  
   Clear inverse relationship in Independence100 between average check and meals served — two viable independent strategies exist.

---

## 6. Implications for Dashboard & Modelling

**Dashboard should support:**
- Separate pages / tabs for each ranking
- Filters: Segment, Growth Band, Franchising (Future50), State/City (Independence100)
- Ranked tables + KPI cards (median growth, top movers, % negative)
- Scatter plots (Sales vs Growth, Units vs Sales, Check vs Meals)
- Segment performance bar charts

**Predictive modelling candidates (Phase 5):**
- Classify Top250 chains into growth bands (or binary high-growth vs not) using Segment, Units, Sales size, etc.
- Within Future50, explore drivers of extreme unit volume or growth (franchising, starting size).
- Keep models simple and interpretable given the modest sample sizes (especially Future50 = 50 rows).

---

## 7. Charts Produced

| File | Content |
|------|---------|
| `reports/future50_eda.png` | Sales vs growth scatter, growth bands, franchising boxplot, unit-volume hist |
| `reports/independence100_eda.png` | Check vs Sales scatter, state counts, meals distribution, sales by state |
| `reports/top250_eda.png` | Top 15 sales bars, YOY distribution, growth bands, Units vs Sales (log) |
| `reports/top250_segment_growth.png` | Average YOY sales growth by standardised segment |

---

**Phase 4 status: Complete.**  
Ready for **Phase 5 – Modelling** or to begin scaffolding the Streamlit dashboard (Phase 6) in parallel.
