# Dataset Analysis Report

## Basic Information

| Property | Value |
|---|---|
| Rows | 5,000 |
| Columns | 21 |
| Missing Values | 686 |
| Duplicate Rows | 0 |
| Memory Usage | 3.01 MB |

## Column Details

| Column | Dtype | Missing | Missing % |
|---|---|---|---|
| Surgery_ID | object | 0 | 0.0% |
| Patient_ID | object | 0 | 0.0% |
| Age | int64 | 0 | 0.0% |
| Gender | object | 0 | 0.0% |
| Surgery_Type | object | 0 | 0.0% |
| Surgery_Duration_Min | int64 | 0 | 0.0% |
| Anesthesia_Type | object | 0 | 0.0% |
| Pre_Op_Risk_Level | object | 0 | 0.0% |
| Blood_Loss_ml | float64 | 107 | 2.14% |
| ICU_Required | object | 0 | 0.0% |
| Complication_Risk | object | 0 | 0.0% |
| Recovery_Time_Days | int64 | 0 | 0.0% |
| Surgeon_Experience_Years | float64 | 45 | 0.9% |
| Hospital_ID | object | 0 | 0.0% |
| Room_Temperature_C | float64 | 127 | 2.54% |
| Room_Humidity_Pct | float64 | 155 | 3.1% |
| Room_CO2_ppm | float64 | 163 | 3.26% |
| Ventilation_Status | object | 0 | 0.0% |
| Room_Occupancy | int64 | 0 | 0.0% |
| Cleaning_Interval_Hours | float64 | 89 | 1.78% |
| Length_of_Stay_Days | int64 | 0 | 0.0% |

## Feature Classification

**ID columns:** Surgery_ID, Patient_ID

**Numerical features (11):** Age, Surgery_Duration_Min, Blood_Loss_ml, Recovery_Time_Days, Surgeon_Experience_Years, Room_Temperature_C, Room_Humidity_Pct, Room_CO2_ppm, Room_Occupancy, Cleaning_Interval_Hours, Length_of_Stay_Days

**Categorical features (8):** Gender, Surgery_Type, Anesthesia_Type, Pre_Op_Risk_Level, ICU_Required, Complication_Risk, Hospital_ID, Ventilation_Status

## Target Variable Assessment

**Suitable for infection-risk prediction:** YES

**Recommended target:** `Complication_Risk`

**Justification:** No direct infection column found. 'Complications' column used as proxy. Post-operative complications include infections among other outcomes. This is documented as a proxy target, NOT a direct infection measurement.

> **WARNING:** Using 'Complications' as a PROXY for infection risk. Not all complications are infections. This must be clearly documented.
