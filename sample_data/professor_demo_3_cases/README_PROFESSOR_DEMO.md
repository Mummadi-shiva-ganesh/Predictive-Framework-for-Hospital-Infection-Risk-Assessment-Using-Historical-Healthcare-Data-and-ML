# Professor Demonstration Guide: 3 Distinct Infection Risk Scenarios

This folder contains 3 patient files calibrated to produce **LOW**, **MEDIUM**, and **HIGH** risk outcomes when evaluated by the trained Gradient Boosting machine learning model.

---

## 🟢 Case 1: LOW INFECTION RISK (99.0% Confidence)

### Patient Profile: `Case_1_LOW_RISK_patient.csv`
- **Patient ID:** `P_LOW_101`
- **Demographics:** 28 years old, Female
- **Procedure:** Ophthalmic Surgery (35 minutes duration)
- **Clinical Indicators:** Local anesthesia, 25 ml blood loss, Surgeon experience = 20 years, Pre-op risk = **Low**, Length of stay = 1 day.
- **Room / Environmental Parameters (Steps 2–4 defaults):**
  - Room: `R101`
  - Temperature: `21°C - 22°C`
  - Humidity: `45% - 50%`
  - CO₂: `480 - 550 ppm`
  - Ventilation: **Good** (HEPA / high ACH)
  - Cleaning Interval: **2 - 4 hours**
- **Expected Prediction Result:** **LOW RISK** (`99.0%` probability)
- **Clinical Rationale:** Operating room hygiene and ventilation are optimal. Minimally invasive surgery with experienced surgeon and low patient vulnerability.

---

## 🟡 Case 2: MEDIUM INFECTION RISK (79.1% Confidence)

### Patient Profile: `Case_2_MEDIUM_RISK_patient.csv`
- **Patient ID:** `P_MED_202`
- **Demographics:** 54 years old, Male
- **Procedure:** General Abdominal Surgery (130 minutes duration)
- **Clinical Indicators:** Regional anesthesia, 260 ml blood loss, Surgeon experience = 11 years, Pre-op risk = **Medium**, Length of stay = 6 days.
- **Room / Environmental Adjustments:**
  - Room: `R202` (Can upload `Case_2_room_patients.csv` with 2 co-occupants)
  - Temperature: `23.5°C`
  - Humidity: `55%`
  - CO₂: `750 ppm`
  - Ventilation: **Moderate**
  - Cleaning Interval: **7 hours**
- **Expected Prediction Result:** **MEDIUM RISK** (`79.1%` probability)
- **Clinical Rationale:** Intermediate patient risk profile with moderate room ventilation and delayed cleaning interval. Warrants targeted monitoring and proactive HVAC adjustment.

---

## 🔴 Case 3: HIGH INFECTION RISK (99.8% Confidence)

### Patient Profile: `Case_3_HIGH_RISK_patient.csv`
- **Patient ID:** `P_HIGH_303`
- **Demographics:** 76 years old, Male
- **Procedure:** Cardiac Surgery (310 minutes duration)
- **Clinical Indicators:** General anesthesia, 750 ml blood loss, Surgeon experience = 7 years, Pre-op risk = **High**, Length of stay = 14 days, Previous Infection = Yes.
- **Room / Environmental Adjustments:**
  - Room: `R303` (Can upload `Case_3_room_patients.csv` with 4 co-occupants $\rightarrow$ high ward density)
  - Temperature: `27.5°C`
  - Humidity: `72%`
  - CO₂: `1150 ppm`
  - Ventilation: **Poor**
  - Cleaning Interval: **16 hours**
- **Expected Prediction Result:** **HIGH RISK** (`99.8%` probability)
- **Clinical Rationale:** Multi-factor escalation: prolonged invasive surgery, high blood loss, elderly patient with prior infection history, exacerbated by poor ventilation, delayed cleaning cycles, and crowded room conditions.

---

## 🚀 How to Demo in the UI (http://localhost:5173):
1. Navigate to **Step 1 (Patient Data)**.
2. Click **Upload Patient Record** and select `Case_1_LOW_RISK_patient.csv`.
3. Proceed through steps or adjust environmental parameters to match the table above.
4. Click **Execute Risk Assessment** on Step 5.
5. Click **Conduct Another Assessment** and repeat with Case 2 and Case 3!
