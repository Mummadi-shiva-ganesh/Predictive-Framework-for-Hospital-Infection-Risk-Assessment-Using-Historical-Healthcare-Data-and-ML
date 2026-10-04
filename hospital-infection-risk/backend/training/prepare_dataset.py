"""
Dataset Preparation Script
============================
This script prepares the dataset for the Hospital Infection Risk Assessment project.

APPROACH:
---------
The primary dataset is the "Surgery Healthcare Dataset" from Kaggle
(https://www.kaggle.com/datasets/arunjangir245/surgery-healthcare-dataset)

If the user has downloaded the Kaggle dataset and placed it at:
    backend/data/kaggle_raw.csv
this script will load it, inspect it, and prepare it.

If the Kaggle dataset is NOT available, this script generates a synthetic
dataset that MIRRORS THE EXACT SCHEMA of the Kaggle Surgery Healthcare
Dataset, with clinically plausible distributions.

IMPORTANT TRANSPARENCY NOTES:
- The generated dataset is SYNTHETIC — it is NOT real patient data.
- The Kaggle Surgery Healthcare Dataset is itself a SYNTHETIC dataset
  created for educational and analytics purposes.
- Environmental/Operational variables are ALWAYS SIMULATED — no real
  hospital sensor measurements are used.
- All simulated data is clearly labeled as DEMO/SIMULATED.

Schema (14 columns from Kaggle dataset):
    1.  Surgery_ID           - Unique surgery identifier
    2.  Patient_ID           - Unique patient identifier
    3.  Age                  - Patient age (years)
    4.  Gender               - Patient gender (Male/Female)
    5.  Surgery_Type         - Type of surgery
    6.  Surgery_Duration_Min - Duration of surgery in minutes
    7.  Anesthesia_Type      - Type of anesthesia used
    8.  Pre_Op_Risk_Level    - Pre-operative risk level (Low/Medium/High)
    9.  Blood_Loss_ml        - Blood loss during surgery (ml)
    10. ICU_Required         - Whether ICU was needed (Yes/No)
    11. Complication_Risk     - Risk of complications (Low/Medium/High) [TARGET]
    12. Recovery_Time_Days   - Recovery time in days
    13. Surgeon_Experience_Years - Years of surgeon experience
    14. Hospital_ID          - Hospital identifier

Additional SIMULATED columns (added for the project):
    15. Room_Temperature_C        - [SIMULATED] Room temperature in Celsius
    16. Room_Humidity_Pct         - [SIMULATED] Room humidity percentage
    17. Room_CO2_ppm             - [SIMULATED] Room CO2 level in ppm
    18. Ventilation_Status        - [SIMULATED] Ventilation quality
    19. Room_Occupancy            - [SIMULATED] Number of patients in room
    20. Cleaning_Interval_Hours   - [SIMULATED] Hours since last cleaning
    21. Length_of_Stay_Days       - [SIMULATED/DERIVED] Total hospital stay

Run: python -m training.prepare_dataset
"""

import os
import sys
import json
import pandas as pd
import numpy as np

# ============================================================
# Configuration
# ============================================================
RANDOM_SEED = 42
NUM_RECORDS = 5000  # Reasonable size for a B.Tech project

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
KAGGLE_RAW_PATH = os.path.join(DATA_DIR, "kaggle_raw.csv")
OUTPUT_PATH = os.path.join(DATA_DIR, "dataset.csv")
METADATA_PATH = os.path.join(DATA_DIR, "dataset_metadata.json")


def check_kaggle_dataset() -> pd.DataFrame | None:
    """Check if the user has placed the Kaggle dataset."""
    # Check multiple possible file names
    possible_names = [
        "kaggle_raw.csv",
        "surgery_healthcare_dataset.csv",
        "Surgery_Healthcare_Dataset.csv",
        "archive.csv",
    ]
    
    for name in possible_names:
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path) and os.path.getsize(path) > 100:
            print(f"[OK] Found Kaggle dataset at: {path}")
            df = pd.read_csv(path)
            print(f"     Shape: {df.shape}")
            print(f"     Columns: {df.columns.tolist()}")
            return df
    
    return None


def generate_base_clinical_data(n: int, rng: np.random.Generator) -> pd.DataFrame:
    """
    Generate synthetic clinical data matching the Kaggle Surgery Healthcare
    Dataset schema with clinically plausible distributions.
    
    TRANSPARENCY: This is SYNTHETIC data generated for the prototype.
    Distributions are based on published clinical statistics.
    """
    print(f"\n[INFO] Generating synthetic clinical data ({n} records)...")
    print("[INFO] This is SYNTHETIC data — NOT real patient data.")
    
    # Surgery types (common categories)
    surgery_types = [
        "Orthopedic", "Cardiac", "Neurological", "General",
        "Gynecological", "Urological", "Ophthalmic", "ENT"
    ]
    surgery_weights = [0.20, 0.12, 0.08, 0.25, 0.12, 0.10, 0.07, 0.06]
    
    # Anesthesia types
    anesthesia_types = ["General", "Regional", "Local", "Sedation"]
    anesthesia_weights = [0.45, 0.25, 0.20, 0.10]
    
    # Pre-operative risk levels
    pre_op_risk_levels = ["Low", "Medium", "High"]
    pre_op_weights = [0.50, 0.35, 0.15]
    
    # Generate features
    ages = rng.integers(18, 90, size=n)
    genders = rng.choice(["Male", "Female"], size=n, p=[0.52, 0.48])
    surgery_type = rng.choice(surgery_types, size=n, p=surgery_weights)
    anesthesia = rng.choice(anesthesia_types, size=n, p=anesthesia_weights)
    pre_op_risk = rng.choice(pre_op_risk_levels, size=n, p=pre_op_weights)
    
    # Surgery duration (minutes) - depends on surgery type
    base_duration = {
        "Orthopedic": 120, "Cardiac": 240, "Neurological": 180,
        "General": 90, "Gynecological": 100, "Urological": 80,
        "Ophthalmic": 60, "ENT": 70,
    }
    surgery_duration = np.array([
        max(20, int(rng.normal(base_duration[st], 30)))
        for st in surgery_type
    ])
    
    # Blood loss (ml) - correlated with surgery duration and type
    blood_loss = np.array([
        max(10, int(rng.normal(dur * 1.5 + (50 if risk == "High" else 0), dur * 0.3)))
        for dur, risk in zip(surgery_duration, pre_op_risk)
    ])
    
    # Surgeon experience (years)
    surgeon_experience = rng.integers(1, 30, size=n)
    
    # ICU required - influenced by risk level, surgery duration, age
    icu_probs = np.array([
        0.05 + (0.15 if risk == "High" else 0.05 if risk == "Medium" else 0)
        + (0.05 if age > 65 else 0) + (0.05 if dur > 180 else 0)
        for risk, age, dur in zip(pre_op_risk, ages, surgery_duration)
    ])
    icu_probs = np.clip(icu_probs, 0, 0.8)
    icu_required = rng.random(n) < icu_probs
    
    # Recovery time (days) - correlated with surgery complexity
    recovery_base = {
        "Orthopedic": 14, "Cardiac": 21, "Neurological": 18,
        "General": 7, "Gynecological": 10, "Urological": 8,
        "Ophthalmic": 3, "ENT": 5,
    }
    recovery_time = np.array([
        max(1, int(rng.normal(
            recovery_base[st] + (5 if icu else 0) + (3 if risk == "High" else 0),
            3
        )))
        for st, icu, risk in zip(surgery_type, icu_required, pre_op_risk)
    ])
    
    # Complication Risk (TARGET) - determined by multiple factors
    # This is the KEY target variable for our infection-risk model
    complication_scores = np.zeros(n)
    
    # Age factor
    complication_scores += np.where(ages > 70, 2.0, np.where(ages > 55, 1.0, 0))
    
    # Surgery duration factor
    complication_scores += np.where(surgery_duration > 200, 2.0,
                          np.where(surgery_duration > 120, 1.0, 0))
    
    # Blood loss factor
    complication_scores += np.where(blood_loss > 400, 2.0,
                          np.where(blood_loss > 200, 1.0, 0))
    
    # Pre-op risk factor
    risk_map = {"Low": 0, "Medium": 1.5, "High": 3.0}
    complication_scores += np.array([risk_map[r] for r in pre_op_risk])
    
    # Surgeon experience (inverse — less experience = higher risk)
    complication_scores += np.where(surgeon_experience < 5, 1.5,
                          np.where(surgeon_experience < 10, 0.5, 0))
    
    # ICU factor
    complication_scores += np.where(icu_required, 1.5, 0)
    
    # Add some noise
    complication_scores += rng.normal(0, 1.0, n)
    
    # Classify into Low/Medium/High based on percentiles
    p33 = np.percentile(complication_scores, 33)
    p66 = np.percentile(complication_scores, 66)
    
    complication_risk = np.where(
        complication_scores <= p33, "Low",
        np.where(complication_scores <= p66, "Medium", "High")
    )
    
    df = pd.DataFrame({
        "Surgery_ID": [f"S{str(i+1).zfill(5)}" for i in range(n)],
        "Patient_ID": [f"P{str(rng.integers(10000, 99999))}" for _ in range(n)],
        "Age": ages,
        "Gender": genders,
        "Surgery_Type": surgery_type,
        "Surgery_Duration_Min": surgery_duration,
        "Anesthesia_Type": anesthesia,
        "Pre_Op_Risk_Level": pre_op_risk,
        "Blood_Loss_ml": blood_loss,
        "ICU_Required": np.where(icu_required, "Yes", "No"),
        "Complication_Risk": complication_risk,
        "Recovery_Time_Days": recovery_time,
        "Surgeon_Experience_Years": surgeon_experience,
        "Hospital_ID": [f"H{str(rng.integers(1, 20)).zfill(3)}" for _ in range(n)],
    })
    
    return df


def add_simulated_environmental_data(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Add SIMULATED environmental and operational variables.
    
    TRANSPARENCY: These are NOT real hospital measurements.
    All values are generated using clinically plausible ranges from
    published hospital environmental guidelines:
    
    - Temperature: ASHRAE Standard 170 recommends 20-24°C for operating rooms
    - Humidity: CDC recommends 30-60% RH for healthcare facilities
    - CO2: OSHA workplace limit is 5000 ppm; good ventilation < 800 ppm
    - Ventilation: WHO recommends 6-12 air changes per hour
    - Occupancy: Based on typical hospital room capacities
    - Cleaning: Based on hospital infection control protocols
    
    Sources:
    - ASHRAE Standard 170-2021: Ventilation of Health Care Facilities
    - CDC Guidelines for Environmental Infection Control in Health-Care Facilities
    - WHO Natural Ventilation for Infection Control in Health-Care Settings
    """
    n = len(df)
    print(f"\n[INFO] Adding SIMULATED environmental/operational variables ({n} records)...")
    print("[WARNING] These are DEMO/SIMULATED values — NOT real hospital sensor data.")
    
    # Determine complication risk for correlation
    is_high_risk = (df["Complication_Risk"] == "High").values
    is_medium_risk = (df["Complication_Risk"] == "Medium").values
    
    # --- SIMULATED: Room Temperature (°C) ---
    # Normal hospital range: 20-24°C
    # Higher temps correlate slightly with worse outcomes
    base_temp = rng.normal(22.0, 2.0, n)
    # Shift higher-risk cases toward slightly higher temps (correlation, not causation)
    base_temp += np.where(is_high_risk, rng.normal(2.0, 1.0, n),
                 np.where(is_medium_risk, rng.normal(0.5, 0.5, n), 0))
    temperature = np.clip(base_temp, 16.0, 38.0).round(1)
    
    # --- SIMULATED: Room Humidity (%) ---
    # Normal range: 30-60%; outside this range increases infection risk
    base_humidity = rng.normal(50.0, 12.0, n)
    base_humidity += np.where(is_high_risk, rng.normal(10.0, 5.0, n),
                    np.where(is_medium_risk, rng.normal(3.0, 3.0, n), 0))
    humidity = np.clip(base_humidity, 15.0, 95.0).round(1)
    
    # --- SIMULATED: CO2 Level (ppm) ---
    # Good: < 800 ppm; Moderate: 800-1200 ppm; Poor: > 1200 ppm
    base_co2 = rng.normal(600.0, 200.0, n)
    base_co2 += np.where(is_high_risk, rng.normal(300.0, 100.0, n),
                np.where(is_medium_risk, rng.normal(100.0, 50.0, n), 0))
    co2 = np.clip(base_co2, 300.0, 3000.0).round(0).astype(int)
    
    # --- SIMULATED: Ventilation Status ---
    # Good/Moderate/Poor — correlated with risk level
    vent_choices = ["Good", "Moderate", "Poor"]
    ventilation = np.where(
        is_high_risk,
        rng.choice(vent_choices, n, p=[0.20, 0.35, 0.45]),
        np.where(
            is_medium_risk,
            rng.choice(vent_choices, n, p=[0.40, 0.40, 0.20]),
            rng.choice(vent_choices, n, p=[0.65, 0.25, 0.10])
        )
    )
    
    # --- SIMULATED: Room Occupancy ---
    # Typical: 1-8 patients per room/ward
    base_occupancy = rng.integers(1, 5, n)
    base_occupancy += np.where(is_high_risk, rng.integers(0, 4, n),
                     np.where(is_medium_risk, rng.integers(0, 2, n), 0))
    occupancy = np.clip(base_occupancy, 1, 12).astype(int)
    
    # --- SIMULATED: Cleaning Interval (hours) ---
    # Best practice: every 4-8 hours; poor: > 12 hours
    base_cleaning = rng.normal(8.0, 3.0, n)
    base_cleaning += np.where(is_high_risk, rng.normal(6.0, 3.0, n),
                    np.where(is_medium_risk, rng.normal(2.0, 2.0, n), 0))
    cleaning_interval = np.clip(base_cleaning, 1.0, 48.0).round(1)
    
    # --- SIMULATED/DERIVED: Length of Stay (days) ---
    # Based on Recovery_Time_Days + additional factors
    los = df["Recovery_Time_Days"].values + rng.integers(0, 5, n)
    los = np.clip(los, 1, 60).astype(int)
    
    # Add all simulated columns
    df_enhanced = df.copy()
    df_enhanced["Room_Temperature_C"] = temperature
    df_enhanced["Room_Humidity_Pct"] = humidity
    df_enhanced["Room_CO2_ppm"] = co2
    df_enhanced["Ventilation_Status"] = ventilation
    df_enhanced["Room_Occupancy"] = occupancy
    df_enhanced["Cleaning_Interval_Hours"] = cleaning_interval
    df_enhanced["Length_of_Stay_Days"] = los
    
    return df_enhanced


def introduce_realistic_missing_values(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """
    Introduce a small percentage of missing values to simulate real-world data.
    This makes the preprocessing pipeline more realistic.
    """
    print("\n[INFO] Introducing realistic missing values (1-3% per applicable column)...")
    
    # Columns that can realistically have missing values
    cols_to_add_missing = [
        ("Blood_Loss_ml", 0.02),           # 2% — sometimes not recorded accurately
        ("Surgeon_Experience_Years", 0.01), # 1% — occasionally unknown
        ("Room_Temperature_C", 0.03),       # 3% — sensor failure
        ("Room_Humidity_Pct", 0.03),        # 3% — sensor failure
        ("Room_CO2_ppm", 0.03),             # 3% — sensor failure
        ("Cleaning_Interval_Hours", 0.02),  # 2% — record keeping gaps
    ]
    
    df_missing = df.copy()
    for col, pct in cols_to_add_missing:
        if col in df_missing.columns:
            mask = rng.random(len(df_missing)) < pct
            count = mask.sum()
            df_missing.loc[mask, col] = np.nan
            print(f"  {col}: {count} values set to NaN ({pct*100:.0f}%)")
    
    return df_missing


def save_dataset_metadata(df: pd.DataFrame, data_source: str):
    """Save dataset metadata as JSON."""
    metadata = {
        "project": "Hospital Infection Risk Assessment",
        "data_source": data_source,
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": {},
        "target_column": "Complication_Risk",
        "target_description": (
            "Risk of post-operative complications (Low/Medium/High). "
            "Used as a PROXY for infection risk in this prototype. "
            "Not all complications are infections — this is documented."
        ),
        "simulated_columns": [
            "Room_Temperature_C", "Room_Humidity_Pct", "Room_CO2_ppm",
            "Ventilation_Status", "Room_Occupancy", "Cleaning_Interval_Hours",
            "Length_of_Stay_Days"
        ],
        "transparency_note": (
            "Environmental and operational variables are SIMULATED using "
            "clinically plausible ranges from published guidelines (ASHRAE, "
            "CDC, WHO). They are NOT real hospital sensor measurements."
        ),
        "random_seed": RANDOM_SEED,
    }
    
    for col in df.columns:
        col_info = {
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum()),
            "unique": int(df[col].nunique()),
            "is_simulated": col in metadata["simulated_columns"],
        }
        if df[col].dtype in [np.float64, np.int64, np.int32, float, int]:
            col_info["min"] = float(df[col].min()) if not df[col].isnull().all() else None
            col_info["max"] = float(df[col].max()) if not df[col].isnull().all() else None
            col_info["mean"] = float(df[col].mean()) if not df[col].isnull().all() else None
        else:
            col_info["sample_values"] = df[col].dropna().unique()[:5].tolist()
        
        metadata["columns"][col] = col_info
    
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, default=str)
    
    print(f"\n[OK] Metadata saved to: {METADATA_PATH}")


def main():
    print("=" * 60)
    print("DATASET PREPARATION")
    print("Hospital Infection Risk Assessment Project")
    print("=" * 60)
    
    os.makedirs(DATA_DIR, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    
    # Step 1: Check for Kaggle dataset
    kaggle_df = check_kaggle_dataset()
    
    if kaggle_df is not None:
        print("\n[OK] Using downloaded Kaggle dataset as base.")
        data_source = "Kaggle Surgery Healthcare Dataset (downloaded)"
        base_df = kaggle_df
    else:
        print("\n[INFO] Kaggle dataset not found.")
        print("[INFO] Generating synthetic data matching the Kaggle schema.")
        print("[INFO] To use the real Kaggle dataset instead:")
        print(f"       1. Download from: https://www.kaggle.com/datasets/arunjangir245/surgery-healthcare-dataset")
        print(f"       2. Place the CSV as: {KAGGLE_RAW_PATH}")
        print(f"       3. Re-run this script.")
        data_source = (
            "Synthetic data generated to match the schema of the Kaggle "
            "Surgery Healthcare Dataset. NOT real patient data."
        )
        base_df = generate_base_clinical_data(NUM_RECORDS, rng)
    
    # Step 2: Display base dataset info
    print(f"\n  Base dataset shape: {base_df.shape}")
    print(f"  Columns: {base_df.columns.tolist()}")
    
    # Step 3: Add simulated environmental/operational variables
    enhanced_df = add_simulated_environmental_data(base_df, rng)
    
    # Step 4: Introduce realistic missing values
    final_df = introduce_realistic_missing_values(enhanced_df, rng)
    
    # Step 5: Save
    final_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n[OK] Dataset saved to: {OUTPUT_PATH}")
    print(f"     Shape: {final_df.shape}")
    
    # Step 6: Save metadata
    save_dataset_metadata(final_df, data_source)
    
    # Step 7: Summary
    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    print(f"  Total records: {len(final_df):,}")
    print(f"  Total columns: {len(final_df.columns)}")
    print(f"  Data source: {data_source}")
    print(f"\n  Target column: Complication_Risk")
    print(f"  Target distribution:")
    for val, count in final_df["Complication_Risk"].value_counts().items():
        pct = round(100.0 * count / len(final_df), 1)
        print(f"    {val}: {count:,} ({pct}%)")
    
    print(f"\n  Simulated columns (DEMO data):")
    for col in ["Room_Temperature_C", "Room_Humidity_Pct", "Room_CO2_ppm",
                "Ventilation_Status", "Room_Occupancy", "Cleaning_Interval_Hours",
                "Length_of_Stay_Days"]:
        missing = final_df[col].isnull().sum()
        print(f"    [SIMULATED] {col} (missing: {missing})")
    
    print(f"\n  Output files:")
    print(f"    {OUTPUT_PATH}")
    print(f"    {METADATA_PATH}")
    
    return final_df


if __name__ == "__main__":
    main()
