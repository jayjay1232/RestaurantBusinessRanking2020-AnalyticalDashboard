"""
Phase 4 – Exploratory Data Analysis
Restaurant Business Rankings 2020
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Paths
ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 11

def load_data():
    f50 = pd.read_csv(PROCESSED / "Future50_clean.csv")
    ind = pd.read_csv(PROCESSED / "Independence100_clean.csv")
    top = pd.read_csv(PROCESSED / "Top250_clean.csv")
    return f50, ind, top


def eda_future50(df: pd.DataFrame):
    print("\n" + "=" * 60)
    print("FUTURE 50 – Emerging / High-Growth Chains")
    print("=" * 60)

    print("\n--- Basic Stats ---")
    print(df[["Sales_M", "Units", "Unit_Volume_Avg", "YOY_Sales_pct", "YOY_Units_pct"]].describe().round(1).to_string())

    print("\n--- Franchising ---")
    print(df["Is_Franchised"].value_counts(normalize=True).mul(100).round(1).to_string())

    print("\n--- Growth Bands ---")
    print("Sales Growth:")
    print(df["Sales_Growth_Band"].value_counts().to_string())
    print("\nUnits Growth:")
    print(df["Units_Growth_Band"].value_counts().to_string())

    print("\n--- Top 5 by YOY Sales Growth ---")
    print(df.nlargest(5, "YOY_Sales_pct")[["Rank", "Restaurant", "Sales_M", "YOY_Sales_pct", "Units", "Is_Franchised"]].to_string(index=False))

    print("\n--- Top 5 by Unit Volume ---")
    print(df.nlargest(5, "Unit_Volume_Avg")[["Rank", "Restaurant", "Unit_Volume_Avg", "Sales_M", "Units"]].to_string(index=False))

    # Plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Sales vs YOY Sales
    ax = axes[0, 0]
    sns.scatterplot(data=df, x="Sales_M", y="YOY_Sales_pct", hue="Is_Franchised", s=80, ax=ax)
    ax.set_title("Future50: Sales ($M) vs YOY Sales Growth %")
    ax.set_xlabel("System Sales ($M)")
    ax.set_ylabel("YOY Sales Growth %")

    # 2. Growth band counts
    ax = axes[0, 1]
    order = ["High (≥20%)", "Moderate (5–20%)", "Low (0–5%)", "Negative"]
    sns.countplot(data=df, x="Sales_Growth_Band", order=[o for o in order if o in df["Sales_Growth_Band"].values], ax=ax, hue="Sales_Growth_Band", legend=False)
    ax.set_title("Future50: Sales Growth Bands")
    ax.tick_params(axis="x", rotation=15)

    # 3. Franchising vs avg growth
    ax = axes[1, 0]
    sns.boxplot(data=df, x="Is_Franchised", y="YOY_Sales_pct", ax=ax)
    ax.set_title("Future50: YOY Sales Growth by Franchising")
    ax.set_xlabel("Is Franchised")
    ax.set_ylabel("YOY Sales %")

    # 4. Unit Volume distribution
    ax = axes[1, 1]
    sns.histplot(df["Unit_Volume_Avg"], bins=12, kde=True, ax=ax)
    ax.set_title("Future50: Unit Volume Distribution")
    ax.set_xlabel("Avg Unit Volume")

    plt.tight_layout()
    fig.savefig(REPORTS / "future50_eda.png", dpi=120, bbox_inches="tight")
    plt.close()
    print(f"\nSaved: reports/future50_eda.png")


def eda_independence100(df: pd.DataFrame):
    print("\n" + "=" * 60)
    print("INDEPENDENCE 100 – Top Independent Restaurants")
    print("=" * 60)

    print("\n--- Basic Stats ---")
    print(df[["Sales_M", "Avg_Check", "Meals_Served"]].describe().round(2).to_string())

    print("\n--- Top States by count ---")
    print(df["State"].value_counts().head(8).to_string())

    print("\n--- Top 5 by Sales ---")
    print(df.nlargest(5, "Sales")[["Rank", "Restaurant", "Sales_M", "Avg_Check", "City", "State"]].to_string(index=False))

    print("\n--- Top 5 by Meals Served ---")
    print(df.nlargest(5, "Meals_Served")[["Rank", "Restaurant", "Meals_Served", "Avg_Check", "City", "State"]].to_string(index=False))

    print("\n--- Correlation (Sales_M, Avg_Check, Meals_Served) ---")
    print(df[["Sales_M", "Avg_Check", "Meals_Served"]].corr().round(3).to_string())

    # Plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Sales vs Avg Check
    ax = axes[0, 0]
    sns.scatterplot(data=df, x="Avg_Check", y="Sales_M", size="Meals_Served", sizes=(40, 300), alpha=0.7, ax=ax)
    ax.set_title("Independence100: Avg Check vs Sales ($M)")
    ax.set_xlabel("Average Check ($)")
    ax.set_ylabel("Sales ($M)")

    # 2. Top states
    ax = axes[0, 1]
    top_states = df["State"].value_counts().head(8)
    sns.barplot(x=top_states.values, y=top_states.index, ax=ax, hue=top_states.index, legend=False)
    ax.set_title("Independence100: Top States by # of Restaurants")
    ax.set_xlabel("Count")

    # 3. Meals Served distribution
    ax = axes[1, 0]
    sns.histplot(df["Meals_Served"] / 1000, bins=15, kde=True, ax=ax)
    ax.set_title("Independence100: Meals Served (thousands)")
    ax.set_xlabel("Meals Served (000s)")

    # 4. Sales by State (top 6)
    ax = axes[1, 1]
    top6 = df["State"].value_counts().head(6).index
    subset = df[df["State"].isin(top6)]
    sns.boxplot(data=subset, x="State", y="Sales_M", ax=ax, order=top6)
    ax.set_title("Independence100: Sales ($M) by Top States")
    ax.tick_params(axis="x", rotation=30)

    plt.tight_layout()
    fig.savefig(REPORTS / "independence100_eda.png", dpi=120, bbox_inches="tight")
    plt.close()
    print(f"\nSaved: reports/independence100_eda.png")


def eda_top250(df: pd.DataFrame):
    print("\n" + "=" * 60)
    print("TOP 250 – Largest US Restaurant Chains")
    print("=" * 60)

    print("\n--- Basic Stats (Sales & Units) ---")
    print(df[["Sales_M", "Units", "YOY_Sales_pct", "YOY_Units_pct"]].describe().round(1).to_string())

    print("\n--- Top 10 by Sales ---")
    print(df.nlargest(10, "Sales_M")[["Rank", "Restaurant", "Sales_M", "YOY_Sales_pct", "Units", "Segment_Standard"]].to_string(index=False))

    print("\n--- Top 10 by YOY Sales Growth ---")
    print(df.nlargest(10, "YOY_Sales_pct")[["Rank", "Restaurant", "Sales_M", "YOY_Sales_pct", "Units", "Segment_Standard"]].to_string(index=False))

    print("\n--- Bottom 10 by YOY Sales Growth (decliners) ---")
    print(df.nsmallest(10, "YOY_Sales_pct")[["Rank", "Restaurant", "Sales_M", "YOY_Sales_pct", "Units", "Segment_Standard"]].to_string(index=False))

    print("\n--- Segment_Standard distribution (top 12) ---")
    print(df["Segment_Standard"].value_counts().head(12).to_string())

    print("\n--- Growth Band distribution ---")
    print(df["Sales_Growth_Band"].value_counts().to_string())

    # Average growth by segment (segments with ≥5 chains)
    seg_stats = (
        df.groupby("Segment_Standard")
        .agg(count=("Restaurant", "count"), avg_yoy=("YOY_Sales_pct", "mean"), median_sales=("Sales_M", "median"))
        .query("count >= 5")
        .sort_values("avg_yoy", ascending=False)
    )
    print("\n--- Segments (≥5 chains) sorted by avg YOY Sales Growth ---")
    print(seg_stats.round(1).to_string())

    # Plots
    fig, axes = plt.subplots(2, 2, figsize=(13, 11))

    # 1. Top 15 chains by Sales
    ax = axes[0, 0]
    top15 = df.nlargest(15, "Sales_M")
    sns.barplot(data=top15, y="Restaurant", x="Sales_M", ax=ax, hue="Restaurant", legend=False)
    ax.set_title("Top250: Top 15 Chains by System Sales ($M)")
    ax.set_xlabel("Sales ($M)")

    # 2. YOY Sales distribution
    ax = axes[0, 1]
    sns.histplot(df["YOY_Sales_pct"].dropna(), bins=25, kde=True, ax=ax)
    ax.axvline(0, color="red", linestyle="--", alpha=0.7)
    ax.set_title("Top250: Distribution of YOY Sales Growth %")
    ax.set_xlabel("YOY Sales %")

    # 3. Growth bands
    ax = axes[1, 0]
    order = ["High (≥20%)", "Moderate (5–20%)", "Low (0–5%)", "Negative"]
    present = [o for o in order if o in df["Sales_Growth_Band"].values]
    sns.countplot(data=df, x="Sales_Growth_Band", order=present, ax=ax, hue="Sales_Growth_Band", legend=False)
    ax.set_title("Top250: Sales Growth Bands")
    ax.tick_params(axis="x", rotation=15)

    # 4. Sales vs Units (log scale helpful)
    ax = axes[1, 1]
    sns.scatterplot(data=df, x="Units", y="Sales_M", hue="Sales_Growth_Band", alpha=0.7, s=50, ax=ax)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Top250: Units vs Sales ($M) – log scales")
    ax.set_xlabel("Units (log)")
    ax.set_ylabel("Sales $M (log)")
    ax.legend(title="Growth Band", fontsize=8, title_fontsize=9)

    plt.tight_layout()
    fig.savefig(REPORTS / "top250_eda.png", dpi=120, bbox_inches="tight")
    plt.close()
    print(f"\nSaved: reports/top250_eda.png")

    # Extra: Segment performance chart
    fig2, ax = plt.subplots(figsize=(10, 6))
    plot_df = seg_stats.reset_index().sort_values("avg_yoy")
    sns.barplot(data=plot_df, y="Segment_Standard", x="avg_yoy", ax=ax, hue="Segment_Standard", legend=False)
    ax.axvline(0, color="gray", linestyle="--")
    ax.set_title("Top250: Average YOY Sales Growth by Segment (≥5 chains)")
    ax.set_xlabel("Avg YOY Sales %")
    plt.tight_layout()
    fig2.savefig(REPORTS / "top250_segment_growth.png", dpi=120, bbox_inches="tight")
    plt.close()
    print(f"Saved: reports/top250_segment_growth.png")


def cross_dataset_notes(f50, ind, top):
    print("\n" + "=" * 60)
    print("CROSS-DATASET OBSERVATIONS")
    print("=" * 60)
    print("""
• The three lists represent different universes:
  - Top250  → large, mostly national chains (system sales in $M–$B)
  - Independence100 → single-location or small multi-unit independents (sales ~$11–39 M)
  - Future50 → emerging high-growth concepts (sales $20–49 M, very high YOY)

• Overlap on restaurant name is expected to be minimal; treat as separate analytic populations.

• Future50 shows dramatically higher growth rates than Top250 (many >20–100% YOY).
• Independence100 is dominated by high-check, high-volume locations in major metros
  (NYC, Chicago, Las Vegas, Washington DC, Florida).
• Within Top250, growth is highly skewed: a minority of chains drive most of the
  positive growth (Raising Cane’s, Shake Shack, First Watch, Wingstop, etc.).
""")


def main():
    f50, ind, top = load_data()
    eda_future50(f50)
    eda_independence100(ind)
    eda_top250(top)
    cross_dataset_notes(f50, ind, top)
    print("\n=== EDA complete. Charts saved to reports/ ===")


if __name__ == "__main__":
    main()
