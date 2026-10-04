"""
Dataset Analysis Script
========================
Performs comprehensive exploratory data analysis (EDA) on the Surgery Healthcare Dataset.

This script:
1. Loads the dataset
2. Displays basic statistics (rows, columns, dtypes, missing values, duplicates)
3. Identifies possible target column for infection-risk prediction
4. Categorizes features as numerical/categorical
5. Analyzes target distribution
6. Generates a data report

Run: python -m training.data_analysis
"""

import os
import sys
import json
import pandas as pd
import numpy as np

# ============================================================
# Configuration
# ============================================================
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DATASET_PATH = os.path.join(DATA_DIR, "dataset.csv")
REPORT_PATH = os.path.join(DATA_DIR, "data_analysis_report.md")

# Reproducible random seed
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def load_dataset(path: str) -> pd.DataFrame:
    """Load the CSV dataset and return a DataFrame."""
    if not os.path.exists(path):
        print(f"\n[ERROR] Dataset not found at: {path}")
        print("Please run: python -m training.download_dataset")
        print("Or manually place the CSV at the path above.")
        sys.exit(1)
    
    df = pd.read_csv(path)
    print(f"[OK] Dataset loaded from: {path}")
    return df


def basic_info(df: pd.DataFrame) -> dict:
    """Display and return basic dataset information."""
    info = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "total_missing": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
    }
    
    print("\n" + "=" * 60)
    print("BASIC DATASET INFORMATION")
    print("=" * 60)
    print(f"  Number of rows:       {info['num_rows']:,}")
    print(f"  Number of columns:    {info['num_columns']}")
    print(f"  Total missing values: {info['total_missing']:,}")
    print(f"  Duplicate rows:       {info['duplicate_rows']:,}")
    print(f"  Memory usage:         {info['memory_usage_mb']} MB")
    
    print(f"\n{'Column':<35} {'Dtype':<15} {'Missing':<10} {'Missing %':<10}")
    print("-" * 70)
    for col in df.columns:
        dtype = str(df[col].dtype)
        missing = df[col].isnull().sum()
        pct = round(100.0 * missing / len(df), 2) if len(df) > 0 else 0
        print(f"  {col:<33} {dtype:<15} {missing:<10} {pct}%")
    
    return info


def identify_feature_types(df: pd.DataFrame) -> dict:
    """Identify numerical and categorical features."""
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    
    # Exclude ID-like columns from features
    id_like_cols = [c for c in df.columns if "id" in c.lower() and df[c].nunique() > 0.9 * len(df)]
    
    feature_numerical = [c for c in numerical_cols if c not in id_like_cols]
    feature_categorical = [c for c in categorical_cols if c not in id_like_cols]
    
    print("\n" + "=" * 60)
    print("FEATURE TYPE CLASSIFICATION")
    print("=" * 60)
    
    print(f"\n  ID-like columns (excluded from features):")
    for c in id_like_cols:
        print(f"    - {c} (nunique={df[c].nunique():,})")
    
    print(f"\n  Numerical features ({len(feature_numerical)}):")
    for c in feature_numerical:
        print(f"    - {c}  (min={df[c].min()}, max={df[c].max()}, mean={df[c].mean():.2f})")
    
    print(f"\n  Categorical features ({len(feature_categorical)}):")
    for c in feature_categorical:
        print(f"    - {c}  (nunique={df[c].nunique()}, values={df[c].unique()[:5].tolist()})")
    
    return {
        "id_columns": id_like_cols,
        "numerical_features": feature_numerical,
        "categorical_features": feature_categorical,
    }


def identify_target(df: pd.DataFrame) -> dict:
    """
    Identify possible target column for infection-risk prediction.
    
    Looks for columns related to:
    - Infection / SSI / HAI
    - Complications
    - ICU required
    - Recovery / Outcome
    """
    target_keywords = [
        "infection", "ssi", "hai", "complication", "icu", 
        "outcome", "recovery", "risk", "result", "status",
        "post_op", "postop", "mortality"
    ]
    
    possible_targets = []
    
    for col in df.columns:
        col_lower = col.lower()
        for keyword in target_keywords:
            if keyword in col_lower:
                unique_vals = df[col].nunique()
                val_counts = df[col].value_counts().to_dict()
                possible_targets.append({
                    "column": col,
                    "keyword_match": keyword,
                    "dtype": str(df[col].dtype),
                    "nunique": unique_vals,
                    "value_counts": val_counts,
                    "sample_values": df[col].unique()[:10].tolist(),
                })
                break
    
    print("\n" + "=" * 60)
    print("TARGET VARIABLE ANALYSIS")
    print("=" * 60)
    
    if not possible_targets:
        print("\n  [WARNING] No columns found matching infection/complication keywords.")
        print("  Searched for: " + ", ".join(target_keywords))
        print("\n  All columns available:")
        for col in df.columns:
            print(f"    - {col} (dtype={df[col].dtype}, nunique={df[col].nunique()})")
    else:
        for t in possible_targets:
            print(f"\n  Candidate: {t['column']}")
            print(f"    Keyword match: '{t['keyword_match']}'")
            print(f"    Dtype: {t['dtype']}")
            print(f"    Unique values: {t['nunique']}")
            print(f"    Sample values: {t['sample_values']}")
            print(f"    Distribution:")
            for val, count in t['value_counts'].items():
                pct = round(100.0 * count / len(df), 1)
                print(f"      {val}: {count:,} ({pct}%)")
    
    return {
        "possible_targets": possible_targets,
        "has_infection_target": any("infection" in t["keyword_match"] for t in possible_targets),
        "has_complication_target": any("complication" in t["keyword_match"] for t in possible_targets),
        "has_icu_target": any("icu" in t["keyword_match"] for t in possible_targets),
    }


def summary_statistics(df: pd.DataFrame):
    """Display summary statistics for numerical columns."""
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS (NUMERICAL)")
    print("=" * 60)
    
    numerical_df = df.select_dtypes(include=[np.number])
    if len(numerical_df.columns) > 0:
        stats = numerical_df.describe().round(2)
        print(stats.to_string())
    else:
        print("  No numerical columns found.")


def display_first_rows(df: pd.DataFrame, n: int = 5):
    """Display the first N rows of the dataset."""
    print("\n" + "=" * 60)
    print(f"FIRST {n} ROWS")
    print("=" * 60)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    print(df.head(n).to_string(index=False))


def check_suitability(target_info: dict, df: pd.DataFrame) -> dict:
    """
    Check whether the dataset is suitable for infection-risk prediction.
    
    CRITICAL: This is the honest assessment of whether we can use this dataset.
    """
    print("\n" + "=" * 60)
    print("SUITABILITY ASSESSMENT FOR INFECTION-RISK PREDICTION")
    print("=" * 60)
    
    assessment = {
        "is_suitable": False,
        "recommended_target": None,
        "target_justification": None,
        "warnings": [],
        "action_required": None,
    }
    
    # Check for direct infection target
    if target_info["has_infection_target"]:
        infection_targets = [t for t in target_info["possible_targets"] if "infection" in t["keyword_match"]]
        best = infection_targets[0]
        assessment["is_suitable"] = True
        assessment["recommended_target"] = best["column"]
        assessment["target_justification"] = "Direct infection-related column found in dataset."
        print(f"\n  [OK] Direct infection target found: '{best['column']}'")
        print(f"       This column can be used as the target for infection-risk prediction.")
    
    # Check for complication target (can serve as proxy for infection risk)
    elif target_info["has_complication_target"]:
        comp_targets = [t for t in target_info["possible_targets"] if "complication" in t["keyword_match"]]
        best = comp_targets[0]
        assessment["is_suitable"] = True
        assessment["recommended_target"] = best["column"]
        assessment["target_justification"] = (
            "No direct infection column found. 'Complications' column used as proxy. "
            "Post-operative complications include infections among other outcomes. "
            "This is documented as a proxy target, NOT a direct infection measurement."
        )
        assessment["warnings"].append(
            "Using 'Complications' as a PROXY for infection risk. "
            "Not all complications are infections. This must be clearly documented."
        )
        print(f"\n  [PROXY] Complication target found: '{best['column']}'")
        print(f"         Can be used as a proxy for infection risk (with clear documentation).")
    
    # Check for ICU target
    elif target_info["has_icu_target"]:
        icu_targets = [t for t in target_info["possible_targets"] if "icu" in t["keyword_match"]]
        best = icu_targets[0]
        assessment["is_suitable"] = True
        assessment["recommended_target"] = best["column"]
        assessment["target_justification"] = (
            "No direct infection or complication column found. 'ICU_Required' used as proxy. "
            "ICU admission correlates with higher infection risk in post-surgical patients. "
            "This is documented as a proxy target."
        )
        assessment["warnings"].append(
            "Using 'ICU_Required' as a PROXY for infection risk. "
            "ICU requirement is not equivalent to infection. This must be clearly documented."
        )
        print(f"\n  [PROXY] ICU target found: '{best['column']}'")
        print(f"         Can be used as a proxy for infection risk (with clear documentation).")
    
    # No suitable target found
    else:
        assessment["is_suitable"] = False
        assessment["action_required"] = (
            "STOP: No suitable target column found for infection-risk prediction. "
            "Do NOT create a fake target by randomly assigning infection labels. "
            "Consider: (1) using a different dataset, or (2) deriving a target from "
            "multiple clinical indicators if medically justifiable and clearly documented."
        )
        print(f"\n  [STOP] No suitable target column found for infection-risk prediction!")
        print(f"         Do NOT create a fake target by randomly assigning labels.")
        print(f"         Review the dataset columns above and decide on next steps.")
    
    # Print all warnings
    for w in assessment["warnings"]:
        print(f"\n  [WARNING] {w}")
    
    if assessment["action_required"]:
        print(f"\n  [ACTION] {assessment['action_required']}")
    
    return assessment


def generate_report(df: pd.DataFrame, info: dict, features: dict, 
                    target_info: dict, assessment: dict):
    """Generate a markdown data analysis report."""
    lines = []
    lines.append("# Dataset Analysis Report")
    lines.append("")
    lines.append("## Basic Information")
    lines.append("")
    lines.append(f"| Property | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Rows | {info['num_rows']:,} |")
    lines.append(f"| Columns | {info['num_columns']} |")
    lines.append(f"| Missing Values | {info['total_missing']:,} |")
    lines.append(f"| Duplicate Rows | {info['duplicate_rows']:,} |")
    lines.append(f"| Memory Usage | {info['memory_usage_mb']} MB |")
    lines.append("")
    
    lines.append("## Column Details")
    lines.append("")
    lines.append(f"| Column | Dtype | Missing | Missing % |")
    lines.append(f"|---|---|---|---|")
    for col in df.columns:
        dtype = str(df[col].dtype)
        missing = df[col].isnull().sum()
        pct = round(100.0 * missing / len(df), 2) if len(df) > 0 else 0
        lines.append(f"| {col} | {dtype} | {missing} | {pct}% |")
    lines.append("")
    
    lines.append("## Feature Classification")
    lines.append("")
    lines.append(f"**ID columns:** {', '.join(features['id_columns']) or 'None'}")
    lines.append(f"")
    lines.append(f"**Numerical features ({len(features['numerical_features'])}):** {', '.join(features['numerical_features'])}")
    lines.append(f"")
    lines.append(f"**Categorical features ({len(features['categorical_features'])}):** {', '.join(features['categorical_features'])}")
    lines.append("")
    
    lines.append("## Target Variable Assessment")
    lines.append("")
    lines.append(f"**Suitable for infection-risk prediction:** {'YES' if assessment['is_suitable'] else 'NO'}")
    lines.append(f"")
    if assessment["recommended_target"]:
        lines.append(f"**Recommended target:** `{assessment['recommended_target']}`")
        lines.append(f"")
        lines.append(f"**Justification:** {assessment['target_justification']}")
        lines.append("")
    
    for w in assessment.get("warnings", []):
        lines.append(f"> **WARNING:** {w}")
        lines.append("")
    
    if assessment.get("action_required"):
        lines.append(f"> **ACTION REQUIRED:** {assessment['action_required']}")
        lines.append("")
    
    # Write report
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"\n[OK] Report saved to: {REPORT_PATH}")


def main():
    print("=" * 60)
    print("HOSPITAL INFECTION RISK - DATASET ANALYSIS")
    print("=" * 60)
    
    # 1. Load dataset
    df = load_dataset(DATASET_PATH)
    
    # 2. Basic info
    info = basic_info(df)
    
    # 3. First few rows
    display_first_rows(df)
    
    # 4. Feature types
    features = identify_feature_types(df)
    
    # 5. Summary statistics
    summary_statistics(df)
    
    # 6. Target variable analysis
    target_info = identify_target(df)
    
    # 7. Suitability assessment
    assessment = check_suitability(target_info, df)
    
    # 8. Generate report
    generate_report(df, info, features, target_info, assessment)
    
    # 9. Final summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    if assessment["is_suitable"]:
        print(f"\n  Dataset IS suitable for infection-risk prediction.")
        print(f"  Recommended target: {assessment['recommended_target']}")
        print(f"\n  Next step: Proceed with preprocessing (Phase 3)")
    else:
        print(f"\n  Dataset is NOT suitable without modifications.")
        print(f"  STOP and review before proceeding.")
    
    return assessment


if __name__ == "__main__":
    main()
