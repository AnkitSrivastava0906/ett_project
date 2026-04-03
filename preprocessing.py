import re
import pandas as pd
import numpy as np


def is_date_column(series):
    """
    Detects if a column likely contains date values (string-based).
    """
    sample = series.dropna().astype(str).head(10)

    date_patterns = [
        r"\d{1,2}/\d{1,2}/\d{2,4}",   # 12/03/2019
        r"\d{4}-\d{1,2}-\d{1,2}",    # 2019-03-12
        r"\d{1,2}-\d{1,2}-\d{2,4}"   # 12-03-2019
    ]

    for pattern in date_patterns:
        if sample.str.contains(pattern, regex=True).any():
            return True

    return False

def preprocess_data(df):
    """
    Handles missing values in the dataset.
    Numerical columns -> mean
    Categorical columns -> mode
    """
    for col in list(df.columns):

        # --- MISSING VALUE HANDLING ---
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].mean())

    return df

def auto_feature_engineer(df):
    """
    Automatically detects and engineers features:
    - Date columns → day, month, year
    - Time columns → hour, minute
    """
    df = df.copy()
    actions = []

    for col in list(df.columns):

        # Only try feature engineering on object columns
        if df[col].dtype != "object":
            continue

        sample = df[col].dropna().astype(str).head(10)

        # ---------------- DATE ----------------
        if is_date_column(df[col]):
            parsed = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

            # Safety check: skip if parsing mostly failed
            if parsed.isna().mean() < 0.8:
                df[f"{col}_day"] = parsed.dt.day
                df[f"{col}_month"] = parsed.dt.month
                df[f"{col}_year"] = parsed.dt.year
                df.drop(columns=[col], inplace=True)
                actions.append(f"Extracted date features from {col}")
                continue

        # ---------------- TIME (HH:MM) ----------------
        time_match = sample.str.contains(r"^\d{1,2}:\d{2}$", regex=True).any()
        if time_match:
            parts = df[col].str.split(":", expand=True)
            if parts.shape[1] == 2:
                df[f"{col}_hour"] = pd.to_numeric(parts[0], errors="coerce")
                df[f"{col}_minute"] = pd.to_numeric(parts[1], errors="coerce")
                df.drop(columns=[col], inplace=True)
                actions.append(f"Extracted time features from {col}")
                continue

    return df, actions

def analyze_dataset(df):
    """
    Analyzes dataset structure, column semantics, and potential issues.
    DOES NOT modify data.
    Returns structured intelligence for agent reasoning.
    """

    analysis = {
        "dataset_summary": {},
        "columns": {},
        "warnings": [],
        "suggested_actions": []
    }

    
    # DATASET LEVEL SUMMARY
    
    n_rows, n_cols = df.shape

    analysis["dataset_summary"] = {
        "rows": n_rows,
        "columns": n_cols,
        "missing_cells_pct": round(df.isna().sum().sum() / (n_rows * n_cols) * 100, 2),
        "numeric_columns": int(df.select_dtypes(include="number").shape[1]),
        "categorical_columns": int(df.select_dtypes(include=["object", "category"]).shape[1])
    }

    if n_rows < 100:
        analysis["warnings"].append("Dataset has very few rows; statistical conclusions may be unreliable.")

    # -------------------------------
    # COLUMN LEVEL ANALYSIS
    # -------------------------------
    for col in df.columns:
        col_info = {}

        series = df[col]
        total = len(series)
        missing_pct = round(series.isna().mean() * 100, 2)
        unique_pct = round(series.nunique(dropna=True) / total * 100, 2)

        # ---- basic stats
        col_info["dtype"] = str(series.dtype)
        col_info["missing_pct"] = missing_pct
        col_info["unique_pct"] = unique_pct

        # ---- semantic role detection
        if series.dtype in ["int64", "float64"]:
            role = "numeric"
        elif series.dtype == "object":
            role = "categorical"
        else:
            role = "other"

        # ---- identifier detection (important)
        if unique_pct > 95 and total > 50:
            role = "identifier"
            analysis["suggested_actions"].append(f"Consider dropping '{col}' (likely an ID column).")

        col_info["role"] = role

        # ---- numeric diagnostics
        if role == "numeric":
            if (series == 0).mean() > 0.5:
                analysis["warnings"].append(f"Column '{col}' has many zeros (>50%).")

            if series.skew(skipna=True) > 1.5:
                analysis["suggested_actions"].append(f"Consider log-transforming '{col}' (high skew).")

        # ---- categorical diagnostics
        if role == "categorical":
            if unique_pct > 50:
                analysis["warnings"].append(
                    f"Column '{col}' has high cardinality ({series.nunique()} unique values)."
                )

        # ---- missing value warning
        if missing_pct > 30:
            analysis["warnings"].append(
                f"Column '{col}' has high missing rate ({missing_pct}%)."
            )

        analysis["columns"][col] = col_info

    return analysis
