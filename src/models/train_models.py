"""
Phase 5 – Predictive Modelling
Restaurant Business Rankings 2020

Models:
1. Top250 – Binary classification: High Growth (YOY_Sales ≥ 10%) vs Not
2. Top250 – Multi-class growth band (simplified)
3. Future50 – Simple analysis of growth drivers (franchising, size)

All models kept intentionally simple and interpretable given sample sizes.
"""

from pathlib import Path
import json
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score,
    roc_auc_score,
    RocCurveDisplay,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"
REPORTS = ROOT / "reports"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42


def load_data():
    top = pd.read_csv(PROCESSED / "Top250_clean.csv")
    f50 = pd.read_csv(PROCESSED / "Future50_clean.csv")
    return top, f50


# ---------------------------------------------------------------------------
# Feature engineering helpers
# ---------------------------------------------------------------------------
def prepare_top250(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Target: High growth = YOY Sales ≥ 10%
    df["High_Growth"] = (df["YOY_Sales_pct"] >= 10).astype(int)

    # Simplified growth band for multi-class (collapse Low + Negative)
    def band(v):
        if v >= 20:
            return "High"
        if v >= 5:
            return "Moderate"
        return "Low/Negative"

    df["Growth_Band_3"] = df["YOY_Sales_pct"].apply(band)

    # Features
    df["log_Sales"] = np.log1p(df["Sales_M"])
    df["log_Units"] = np.log1p(df["Units"])
    # Sales per unit (rough productivity)
    df["Sales_per_Unit"] = df["Sales_M"] / df["Units"].clip(lower=1)

    # Keep only rows with valid target
    df = df.dropna(subset=["YOY_Sales_pct", "Segment_Standard"])
    return df


# ---------------------------------------------------------------------------
# Model 1 & 2: Top250 Classification
# ---------------------------------------------------------------------------
def train_top250_models(df: pd.DataFrame):
    print("\n" + "=" * 60)
    print("TOP250 – HIGH GROWTH CLASSIFICATION")
    print("=" * 60)

    feature_cols = ["log_Sales", "log_Units", "Sales_per_Unit", "Segment_Standard"]
    X = df[feature_cols]
    y_bin = df["High_Growth"]
    y_multi = df["Growth_Band_3"]

    print(f"\nBinary target distribution (High_Growth ≥10%):")
    print(y_bin.value_counts(normalize=True).mul(100).round(1).to_string())
    print(f"\nMulti-class target distribution:")
    print(y_multi.value_counts().to_string())

    # Preprocessing: scale numeric, one-hot segment
    numeric_features = ["log_Sales", "log_Units", "Sales_per_Unit"]
    categorical_features = ["Segment_Standard"]

    # For simplicity we use LabelEncoder + one-hot via pandas get_dummies for RF,
    # and a pipeline for LogisticRegression.
    X_enc = pd.get_dummies(X, columns=["Segment_Standard"], drop_first=True)
    feature_names = list(X_enc.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X_enc, y_bin, test_size=0.25, random_state=RANDOM_STATE, stratify=y_bin
    )

    results = {}

    # ----- Logistic Regression -----
    print("\n--- Logistic Regression (Binary High Growth) ---")
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE)
    lr.fit(X_train_s, y_train)
    y_pred_lr = lr.predict(X_test_s)
    y_prob_lr = lr.predict_proba(X_test_s)[:, 1]

    acc_lr = accuracy_score(y_test, y_pred_lr)
    f1_lr = f1_score(y_test, y_pred_lr)
    auc_lr = roc_auc_score(y_test, y_prob_lr)

    print(f"Accuracy : {acc_lr:.3f}")
    print(f"F1       : {f1_lr:.3f}")
    print(f"ROC-AUC  : {auc_lr:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_lr, target_names=["Not High", "High Growth"]))

    # Coefficients (interpretable)
    coef_df = pd.DataFrame({
        "feature": feature_names,
        "coefficient": lr.coef_[0]
    }).sort_values("coefficient", key=abs, ascending=False)
    print("\nTop coefficients (by absolute value):")
    print(coef_df.head(12).to_string(index=False))

    results["logistic_regression"] = {
        "accuracy": float(acc_lr),
        "f1": float(f1_lr),
        "roc_auc": float(auc_lr),
        "coefficients": coef_df.head(15).to_dict(orient="records"),
    }

    # ----- Random Forest -----
    print("\n--- Random Forest (Binary High Growth) ---")
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_prob_rf = rf.predict_proba(X_test)[:, 1]

    acc_rf = accuracy_score(y_test, y_pred_rf)
    f1_rf = f1_score(y_test, y_pred_rf)
    auc_rf = roc_auc_score(y_test, y_prob_rf)

    print(f"Accuracy : {acc_rf:.3f}")
    print(f"F1       : {f1_rf:.3f}")
    print(f"ROC-AUC  : {auc_rf:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_rf, target_names=["Not High", "High Growth"]))

    # Feature importance
    imp = pd.DataFrame({
        "feature": feature_names,
        "importance": rf.feature_importances_
    }).sort_values("importance", ascending=False)
    print("\nTop feature importances:")
    print(imp.head(12).to_string(index=False))

    results["random_forest"] = {
        "accuracy": float(acc_rf),
        "f1": float(f1_rf),
        "roc_auc": float(auc_rf),
        "feature_importances": imp.head(15).to_dict(orient="records"),
    }

    # Cross-validation (more robust estimate)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(rf, X_enc, y_bin, cv=cv, scoring="f1")
    print(f"\nRF 5-fold CV F1: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
    results["random_forest"]["cv_f1_mean"] = float(cv_scores.mean())
    results["random_forest"]["cv_f1_std"] = float(cv_scores.std())

    # Save artefacts
    joblib.dump(rf, MODELS_DIR / "top250_rf_high_growth.joblib")
    joblib.dump(lr, MODELS_DIR / "top250_lr_high_growth.joblib")
    joblib.dump(scaler, MODELS_DIR / "top250_scaler.joblib")
    joblib.dump(feature_names, MODELS_DIR / "top250_feature_names.joblib")

    # Confusion matrix plot
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, pred, title in zip(
        axes,
        [y_pred_lr, y_pred_rf],
        ["Logistic Regression", "Random Forest"],
    ):
        cm = confusion_matrix(y_test, pred)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                    xticklabels=["Not High", "High"], yticklabels=["Not High", "High"])
        ax.set_title(title)
        ax.set_ylabel("Actual")
        ax.set_xlabel("Predicted")
    plt.tight_layout()
    fig.savefig(REPORTS / "top250_confusion_matrices.png", dpi=120, bbox_inches="tight")
    plt.close()

    # Feature importance plot
    fig, ax = plt.subplots(figsize=(9, 6))
    top_imp = imp.head(12)
    sns.barplot(data=top_imp, y="feature", x="importance", ax=ax, hue="feature", legend=False)
    ax.set_title("Random Forest – Top Feature Importances (High Growth ≥10%)")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    fig.savefig(REPORTS / "top250_feature_importance.png", dpi=120, bbox_inches="tight")
    plt.close()

    # ROC curve
    fig, ax = plt.subplots(figsize=(6, 5))
    RocCurveDisplay.from_predictions(y_test, y_prob_lr, name="Logistic Regression", ax=ax)
    RocCurveDisplay.from_predictions(y_test, y_prob_rf, name="Random Forest", ax=ax)
    ax.set_title("ROC Curve – High Growth Classification")
    plt.tight_layout()
    fig.savefig(REPORTS / "top250_roc_curve.png", dpi=120, bbox_inches="tight")
    plt.close()

    print("\nSaved model artefacts to models/ and plots to reports/")
    return results, feature_names


# ---------------------------------------------------------------------------
# Future50 – Driver analysis (descriptive + simple model)
# ---------------------------------------------------------------------------
def analyse_future50(df: pd.DataFrame):
    print("\n" + "=" * 60)
    print("FUTURE50 – GROWTH DRIVER ANALYSIS")
    print("=" * 60)

    # Very small sample – keep it simple and descriptive + one logistic model
    df = df.copy()
    df["High_Growth"] = (df["YOY_Sales_pct"] >= 30).astype(int)  # stricter threshold for this list

    print(f"\nHigh Growth (≥30% YOY) distribution:")
    print(df["High_Growth"].value_counts().to_string())

    print("\n--- Mean metrics by Franchising ---")
    print(
        df.groupby("Is_Franchised")[["YOY_Sales_pct", "YOY_Units_pct", "Sales_M", "Units", "Unit_Volume_Avg"]]
        .mean()
        .round(1)
        .to_string()
    )

    # Simple correlation
    print("\n--- Correlations with YOY_Sales_pct ---")
    corr_cols = ["Sales_M", "Units", "Unit_Volume_Avg", "YOY_Units_pct"]
    print(df[corr_cols + ["YOY_Sales_pct"]].corr()["YOY_Sales_pct"].sort_values(ascending=False).round(3).to_string())

    # Tiny logistic model: predict High_Growth from size + franchising
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    X = df[["Sales_M", "Units", "Unit_Volume_Avg", "Is_Franchised"]].astype(float)
    y = df["High_Growth"]

    # With n=50 we report in-sample + leave-one-out style caution
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    lr = LogisticRegression(class_weight="balanced", random_state=RANDOM_STATE)
    lr.fit(Xs, y)
    y_pred = lr.predict(Xs)
    acc = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    print(f"\nSimple Logistic (in-sample) – Accuracy: {acc:.3f}, F1: {f1:.3f}")
    print("(Note: small sample – treat as exploratory only)")

    coef = pd.DataFrame({
        "feature": ["Sales_M", "Units", "Unit_Volume_Avg", "Is_Franchised"],
        "coefficient": lr.coef_[0]
    })
    print("\nCoefficients:")
    print(coef.to_string(index=False))

    joblib.dump(lr, MODELS_DIR / "future50_lr_high_growth.joblib")
    joblib.dump(scaler, MODELS_DIR / "future50_scaler.joblib")

    return {
        "in_sample_accuracy": float(acc),
        "in_sample_f1": float(f1),
        "coefficients": coef.to_dict(orient="records"),
        "note": "Exploratory only – n=50, no held-out test set",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    top, f50 = load_data()
    top_prep = prepare_top250(top)

    results_top, feat_names = train_top250_models(top_prep)
    results_f50 = analyse_future50(f50)

    # Save combined metrics
    summary = {
        "top250_binary_high_growth": results_top,
        "future50_exploratory": results_f50,
        "target_definition_top250": "High_Growth = YOY_Sales_pct >= 10",
        "target_definition_future50": "High_Growth = YOY_Sales_pct >= 30",
        "features_top250": ["log_Sales", "log_Units", "Sales_per_Unit", "Segment_Standard (one-hot)"],
    }
    with open(MODELS_DIR / "model_metrics.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n=== Modelling complete ===")
    print(f"Metrics saved to: {MODELS_DIR / 'model_metrics.json'}")


if __name__ == "__main__":
    main()
