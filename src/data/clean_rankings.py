"""
Phase 3 – Data Cleaning & Preparation
Restaurant Business Rankings 2020

Cleans the three raw ranking CSVs and writes analysis-ready tables
to data/processed/.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import re

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def pct_to_float(series: pd.Series) -> pd.Series:
    """Convert strings like '130.5%' or '-2.0%' to float."""
    return (
        series.astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
        .replace({"nan": np.nan, "None": np.nan, "": np.nan})
        .astype(float)
    )


def parse_location(loc: str):
    """Simple split of 'City, State' style strings."""
    if pd.isna(loc):
        return pd.Series({"City": np.nan, "State": np.nan})
    parts = [p.strip() for p in str(loc).split(",")]
    if len(parts) >= 2:
        return pd.Series({"City": parts[0], "State": parts[1]})
    return pd.Series({"City": parts[0], "State": np.nan})


def growth_band(val: float) -> str:
    if pd.isna(val):
        return "Unknown"
    if val >= 20:
        return "High (≥20%)"
    if val >= 5:
        return "Moderate (5–20%)"
    if val >= 0:
        return "Low (0–5%)"
    return "Negative"


# Simple mapping to normalise the most common short labels in Top250
SEGMENT_MAP = {
    "Burger": "Quick Service & Burger",
    "Chicken": "Quick Service & Chicken",
    "Pizza": "Quick Service & Pizza",
    "Mexican": "Quick Service & Mexican",
    "Sandwich": "Quick Service & Sandwich",
    "Steak": "Casual Dining & Steak",
    "Seafood": "Casual Dining & Seafood",
    "Varied Menu": "Casual Dining & Varied Menu",
    "Family Style": "Family Dining & Family Style",
    "Bakery Cafe": "Quick Service & Bakery Cafe",
    "Coffee Cafe": "Quick Service & Coffee Cafe",
    "Frozen Desserts": "Quick Service & Frozen Desserts",
    "Snack": "Quick Service & Snack",
    "BBQ": "Casual Dining & BBQ",
    "Sports Bar": "Casual Dining & Sports Bar",
    "Italian/Pizza": "Casual Dining & Italian/Pizza",
    "Asian": "Casual Dining & Asian",
    "Asian/Noodle": "Fast Casual & Asian/Noodle",
    "Healthy": "Fast Casual & Healthy",
    "Ethnic": "Fast Casual & Ethnic",
    "Family Casual": "Quick Service & Family Casual",
}


def standardise_segment(seg: str) -> str:
    if pd.isna(seg):
        return "Unknown"
    seg = str(seg).strip()
    return SEGMENT_MAP.get(seg, seg)


# ---------------------------------------------------------------------------
# Clean Future50
# ---------------------------------------------------------------------------
def clean_future50(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["YOY_Sales_pct"] = pct_to_float(df["YOY_Sales"])
    df["YOY_Units_pct"] = pct_to_float(df["YOY_Units"])
    df["Is_Franchised"] = df["Franchising"].str.strip().str.lower().eq("yes")
    df["Sales_Growth_Band"] = df["YOY_Sales_pct"].apply(growth_band)
    df["Units_Growth_Band"] = df["YOY_Units_pct"].apply(growth_band)

    loc = df["Location"].apply(parse_location)
    df["City"] = loc["City"]
    df["State"] = loc["State"]

    # Keep original columns + new ones; drop the raw string % columns if desired
    # We keep both for transparency
    df = df.rename(columns={"Sales": "Sales_M", "Unit_Volume": "Unit_Volume_Avg"})
    return df


# ---------------------------------------------------------------------------
# Clean Independence100
# ---------------------------------------------------------------------------
def clean_independence100(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Sales are already full dollars – create a millions view for comparability
    df["Sales_M"] = df["Sales"] / 1_000_000
    df["Avg_Check"] = df["Average Check"]
    df["Meals_Served"] = df["Meals Served"]
    # Clean city names (some have trailing spaces)
    df["City"] = df["City"].str.strip()
    df["State"] = df["State"].str.strip()
    return df


# ---------------------------------------------------------------------------
# Clean Top250
# ---------------------------------------------------------------------------
def clean_top250(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["YOY_Sales_pct"] = pct_to_float(df["YOY_Sales"])
    df["YOY_Units_pct"] = pct_to_float(df["YOY_Units"])
    df["Sales_M"] = df["Sales"]  # already in millions
    df["Segment_Standard"] = df["Segment_Category"].apply(standardise_segment)
    df["Sales_Growth_Band"] = df["YOY_Sales_pct"].apply(growth_band)
    df["Units_Growth_Band"] = df["YOY_Units_pct"].apply(growth_band)
    # Content & Headquarters remain as-is (mostly missing)
    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Loading raw files...")
    f50_raw = pd.read_csv(RAW / "Future50.csv")
    ind_raw = pd.read_csv(RAW / "Independence100.csv")
    top_raw = pd.read_csv(RAW / "Top250.csv")

    print("Cleaning Future50...")
    f50 = clean_future50(f50_raw)
    print("Cleaning Independence100...")
    ind = clean_independence100(ind_raw)
    print("Cleaning Top250...")
    top = clean_top250(top_raw)

    # Write cleaned CSVs
    f50.to_csv(PROCESSED / "Future50_clean.csv", index=False)
    ind.to_csv(PROCESSED / "Independence100_clean.csv", index=False)
    top.to_csv(PROCESSED / "Top250_clean.csv", index=False)

    print("\n=== Cleaning complete ===")
    print(f"Future50_clean        : {f50.shape}")
    print(f"Independence100_clean : {ind.shape}")
    print(f"Top250_clean          : {top.shape}")
    print(f"\nFiles written to: {PROCESSED}")

    # Quick validation
    print("\n--- Validation ---")
    print("Future50 YOY_Sales_pct sample:", f50["YOY_Sales_pct"].head(3).tolist())
    print("Top250 Segment_Standard value counts (top 8):")
    print(top["Segment_Standard"].value_counts().head(8).to_string())
    print("Independence100 Sales_M describe:\n", ind["Sales_M"].describe().round(2).to_string())



if __name__ == "__main__":
    main()
