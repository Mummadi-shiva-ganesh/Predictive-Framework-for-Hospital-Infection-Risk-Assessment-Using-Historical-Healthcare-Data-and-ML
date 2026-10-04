import os
import json
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

app = FastAPI(
    title="Hospital Infection Risk Assessment API",
    description="Backend API supporting File-Upload Workflow for Patient, Room, Environmental, and Operational Risk Analysis",
    version="2.1.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model state
model = None
preprocessor = None
metadata = None
num_features = []
cat_features = []

# Data Schemas
class CurrentPatientSchema(BaseModel):
    patient_id: str = Field(default="P001", example="P001")
    age: int = Field(..., ge=0, le=120, example=58)
    gender: str = Field(..., example="Male")
    surgery_type: str = Field(..., example="Orthopedic")
    surgery_duration_min: float = Field(..., ge=10, le=600, example=180.0)
    anesthesia_type: str = Field(..., example="General")
    pre_op_risk_level: str = Field(..., example="High")
    blood_loss_ml: float = Field(..., ge=0, le=5000, example=450.0)
    surgeon_experience_years: int = Field(..., ge=0, le=50, example=12)
    length_of_stay_days: int = Field(..., ge=1, le=90, example=7)
    medical_history: Optional[str] = Field(default="None", example="Diabetes")
    previous_infection: Optional[str] = Field(default="No", example="No")

class RoomPatientSchema(BaseModel):
    room_id: str = Field(..., example="R101")
    patient_id: str = Field(..., example="P002")
    age: int = Field(..., ge=0, le=120, example=67)
    gender: str = Field(..., example="Female")
    surgery_type: str = Field(..., example="Gynecological")
    surgery_duration_min: Optional[float] = Field(default=120.0, example=120.0)
    anesthesia_type: Optional[str] = Field(default="General", example="General")
    pre_op_risk_level: Optional[str] = Field(default="Medium", example="Medium")
    blood_loss_ml: Optional[float] = Field(default=200.0, example=200.0)
    surgeon_experience_years: Optional[int] = Field(default=8, example=8)
    length_of_stay_days: int = Field(..., ge=1, le=90, example=5)
    medical_history: Optional[str] = Field(default="None", example="Hypertension")
    previous_infection: Optional[str] = Field(default="No", example="No")

class EnvironmentalSchema(BaseModel):
    room_id: str = Field(..., example="R101")
    temperature: float = Field(..., ge=15, le=40, example=29.0)
    humidity: float = Field(..., ge=0, le=100, example=75.0)
    co2_level: float = Field(..., ge=300, le=3000, example=1200.0)

class OperationalSchema(BaseModel):
    room_id: str = Field(..., example="R101")
    ventilation_status: str = Field(..., example="Poor")
    cleaning_interval: float = Field(..., ge=1, le=48, example=18.0)

class MultiStepPredictionRequest(BaseModel):
    current_patient: CurrentPatientSchema
    room_patients: List[RoomPatientSchema] = Field(default_factory=list)
    environmental_data: EnvironmentalSchema
    operational_data: OperationalSchema

class FeatureImportanceItem(BaseModel):
    feature: str
    importance: float
    interpretation: str

class RiskPredictionResponse(BaseModel):
    patient_id: str
    room_id: str
    room_occupancy: int
    other_patient_ids: List[str]
    risk_level: str
    risk_probability: float
    risk_rationale: str
    important_factors: List[FeatureImportanceItem]
    recommendations: List[str]
    disclaimer: str

@app.on_event("startup")
def load_artifacts():
    global model, preprocessor, metadata, num_features, cat_features
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "models")
    
    model_path = os.path.join(models_dir, "best_model.joblib")
    prep_path = os.path.join(models_dir, "preprocessor.joblib")
    meta_path = os.path.join(models_dir, "model_metadata.json")

    if not os.path.exists(model_path) or not os.path.exists(prep_path):
        print("Warning: Trained model missing. Run train_model.py first.")
        return

    model = joblib.load(model_path)
    preprocessor = joblib.load(prep_path)
    
    with open(meta_path, "r") as f:
        metadata = json.load(f)

    num_features = metadata.get("num_features", [])
    cat_features = metadata.get("cat_features", [])
    print(f"Loaded ML Model ({metadata.get('best_model_name')}) successfully!")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_type": metadata.get("best_model_name") if metadata else None
    }

@app.get("/api/sample-demo")
def get_sample_demo_data():
    """Returns sample datasets for 1-click UI testing."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_dir = os.path.join(base_dir, "sample_data")
    
    cp_path = os.path.join(sample_dir, "current_patient.csv")
    rp_path = os.path.join(sample_dir, "room_patients.csv")
    env_path = os.path.join(sample_dir, "environmental_data.csv")
    op_path = os.path.join(sample_dir, "operational_data.csv")

    try:
        current_patient = pd.read_csv(cp_path, comment='#').to_dict(orient="records")[0]
        room_patients = pd.read_csv(rp_path, comment='#').to_dict(orient="records")
        env_raw = pd.read_csv(env_path, comment='#').to_dict(orient="records")[0]
        op_raw = pd.read_csv(op_path, comment='#').to_dict(orient="records")[0]

        environmental_data = {
            "room_id": str(env_raw.get("room_id", "R101")),
            "temperature": float(env_raw.get("temperature", 29.0)),
            "humidity": float(env_raw.get("humidity", 75.0)),
            "co2_level": float(env_raw.get("co2_level", 1200.0))
        }

        operational_data = {
            "room_id": str(op_raw.get("room_id", "R101")),
            "ventilation_status": str(op_raw.get("ventilation_status", "Poor")),
            "cleaning_interval": float(op_raw.get("cleaning_interval", 18.0))
        }

        return {
            "current_patient": current_patient,
            "room_patients": room_patients,
            "environmental_data": environmental_data,
            "operational_data": operational_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load sample demo data: {str(e)}")

def validate_prediction_workflow(req: MultiStepPredictionRequest):
    """Validates structural integrity, room ID matching, and patient ID uniqueness."""
    cp = req.current_patient
    rp_list = req.room_patients
    env = req.environmental_data
    op = req.operational_data

    # Check Patient ID duplicates
    cp_id = cp.patient_id.strip()
    rp_ids = [p.patient_id.strip() for p in rp_list]

    if cp_id in rp_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Validation Error: Patient '{cp_id}' already exists as the current patient and cannot be included in the other-room-patients file."
        )

    if len(rp_ids) != len(set(rp_ids)):
        duplicates = [x for x in set(rp_ids) if rp_ids.count(x) > 1]
        raise HTTPException(
            status_code=400,
            detail=f"Validation Error: Duplicate patient IDs found in room patients list: {', '.join(duplicates)}"
        )

    # Check Room ID consistency
    room_ids_in_rp = set(p.room_id.strip() for p in rp_list)
    if room_ids_in_rp and any(rid != env.room_id.strip() for rid in room_ids_in_rp):
        raise HTTPException(
            status_code=400,
            detail=f"Validation Error: Room ID mismatch between room patients file ({', '.join(room_ids_in_rp)}) and environmental data ({env.room_id})."
        )

    if env.room_id.strip() != op.room_id.strip():
        raise HTTPException(
            status_code=400,
            detail=f"Validation Error: Room ID mismatch between environmental data ({env.room_id}) and operational data ({op.room_id})."
        )

def generate_risk_rationale(
    risk_level: str,
    risk_prob: float,
    cp: CurrentPatientSchema,
    env: EnvironmentalSchema,
    op: OperationalSchema,
    occupancy: int
) -> str:
    triggers = []
    
    # Clinical factors
    if cp.pre_op_risk_level.capitalize() == "High":
        triggers.append("high pre-operative risk status")
    if cp.blood_loss_ml > 400:
        triggers.append(f"significant intra-operative blood loss ({cp.blood_loss_ml} ml)")
    if cp.surgery_duration_min > 180:
        triggers.append(f"extended surgery duration ({cp.surgery_duration_min} min)")
    if cp.length_of_stay_days > 7:
        triggers.append(f"prolonged hospital stay ({cp.length_of_stay_days} days)")

    # Environmental factors
    if env.co2_level > 800:
        triggers.append(f"elevated room CO2 concentration ({env.co2_level} ppm [SIMULATED])")
    if env.humidity > 65 or env.humidity < 40:
        triggers.append(f"sub-optimal room humidity ({env.humidity}% [SIMULATED])")
    if env.temperature > 26:
        triggers.append(f"high room temperature ({env.temperature}°C [SIMULATED])")

    # Operational factors
    if op.cleaning_interval > 8:
        triggers.append(f"delayed room cleaning interval ({op.cleaning_interval} hours vs recommended ≤6 hrs [SIMULATED])")
    if op.ventilation_status.capitalize() in ["Moderate", "Poor"]:
        triggers.append(f"{op.ventilation_status.lower()} room ventilation quality [SIMULATED]")
    if occupancy > 3:
        triggers.append(f"high room occupancy density ({occupancy} occupants sharing Room {env.room_id})")

    if risk_level == "HIGH":
        if triggers:
            reasons = ", ".join(triggers[:4])
            return (
                f"Patient {cp.patient_id} is evaluated as HIGH INFECTION RISK ({risk_prob:.1f}% calculated probability) "
                f"due to a combination of: {reasons}. This combination of environmental stagnation, delayed cleaning, and patient vulnerability significantly increases infection susceptibility."
            )
        else:
            return f"Patient {cp.patient_id} is evaluated as HIGH INFECTION RISK ({risk_prob:.1f}% calculated probability) based on risk pattern matching across patient, room, environmental, and operational features."

    elif risk_level == "MEDIUM":
        if triggers:
            reasons = ", ".join(triggers[:3])
            return (
                f"Patient {cp.patient_id} is evaluated as MEDIUM INFECTION RISK ({risk_prob:.1f}% calculated probability) "
                f"attributable to: {reasons}. Targeted preventive steps (e.g. enhanced ventilation and timely cleaning) can reduce the risk level."
            )
        else:
            return f"Patient {cp.patient_id} is evaluated as MEDIUM INFECTION RISK ({risk_prob:.1f}% calculated probability) indicating moderate exposure to risk factors."

    else:
        return (
            f"Patient {cp.patient_id} is evaluated as LOW INFECTION RISK ({risk_prob:.1f}% calculated probability). "
            f"Operating room ventilation ({op.ventilation_status}), cleaning intervals ({op.cleaning_interval} hrs), and environmental readings are within healthy baseline bounds."
        )

def generate_recommendations(env: EnvironmentalSchema, op: OperationalSchema, cp: CurrentPatientSchema, occupancy: int) -> List[str]:
    recs = []
    
    if op.ventilation_status.capitalize() in ["Moderate", "Poor"]:
        recs.append("Improve ventilation airflow: Increase Air Exchanges Per Hour (ACH) and inspect HEPA filtration units.")
    if op.cleaning_interval > 8:
        recs.append(f"Prioritize cleaning: Reduce room cleaning interval from {op.cleaning_interval} hours to <= 6 hours.")
    if env.co2_level > 800:
        recs.append(f"High CO2 detected ({env.co2_level} ppm): Increase fresh air supply to bring room CO2 below 700 ppm.")
    if env.humidity > 60:
        recs.append(f"High room humidity ({env.humidity}%): Adjust HVAC dehumidification to target 40% - 60%.")
    if occupancy > 4:
        recs.append(f"Review room occupancy: Room currently has {occupancy} occupants. Consider redistributing patients to reduce cross-exposure risk.")
    if cp.pre_op_risk_level.capitalize() == "High":
        recs.append("Monitor high-risk conditions: Patient has High Pre-Op risk; enforce strict infection surveillance protocols.")
    if cp.blood_loss_ml > 500:
        recs.append("Administer prophylactic antimicrobial therapy per surgical site guidelines due to elevated blood loss.")
    
    if not recs:
        recs.append("Standard operating room hygiene and routine patient monitoring protocols apply.")

    return recs

@app.post("/predict", response_model=RiskPredictionResponse)
def predict_risk(req: MultiStepPredictionRequest):
    if model is None or preprocessor is None:
        load_artifacts()
        if model is None or preprocessor is None:
            raise HTTPException(status_code=500, detail="Model is not loaded. Ensure train_model.py has executed successfully.")

    # 1. Validate Workflow Integrity
    validate_prediction_workflow(req)

    cp = req.current_patient
    rp_list = req.room_patients
    env = req.environmental_data
    op = req.operational_data

    # 2. Derive Room Occupancy
    calculated_occupancy = 1 + len(rp_list)

    # 3. Construct Input Dataframe matching exact features expected by ML model
    input_df = pd.DataFrame([{
        "Age": cp.age,
        "Gender": cp.gender.capitalize(),
        "Surgery_Type": cp.surgery_type.capitalize(),
        "Surgery_Duration_Min": cp.surgery_duration_min,
        "Anesthesia_Type": cp.anesthesia_type.capitalize(),
        "Pre_Op_Risk_Level": cp.pre_op_risk_level.capitalize(),
        "Blood_Loss_ml": cp.blood_loss_ml,
        "Surgeon_Experience_Years": cp.surgeon_experience_years,
        "Room_Temperature_C": env.temperature,
        "Room_Humidity_Pct": env.humidity,
        "Room_CO2_ppm": env.co2_level,
        "Ventilation_Status": op.ventilation_status.capitalize(),
        "Room_Occupancy": calculated_occupancy,
        "Cleaning_Interval_Hours": op.cleaning_interval,
        "Length_of_Stay_Days": cp.length_of_stay_days
    }])

    # 4. Transform through Scikit-Learn Pipeline
    try:
        proc_input = preprocessor.transform(input_df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data preprocessing error: {str(e)}")

    # 5. Predict Risk Class & Probability
    pred_class_idx = int(model.predict(proc_input)[0])
    probs = model.predict_proba(proc_input)[0]

    target_map = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
    risk_level = target_map.get(pred_class_idx, "LOW")
    risk_probability = float(probs[pred_class_idx] * 100.0)

    # 6. Model-derived Feature Importances
    top_factors = []
    if hasattr(model, "feature_importances_"):
        cat_encoder = preprocessor.named_transformers_["cat"].named_steps["encoder"]
        cat_feature_names = cat_encoder.get_feature_names_out(cat_features).tolist()
        all_feature_names = num_features + cat_feature_names

        importances = model.feature_importances_
        sorted_indices = np.argsort(importances)[::-1][:4]

        feature_display_map = {
            "Cleaning_Interval_Hours": "Cleaning Interval [SIMULATED]",
            "Pre_Op_Risk_Level_Low": "Pre-Operative Risk Level (Low)",
            "Pre_Op_Risk_Level_High": "Pre-Operative Risk Level (High)",
            "Room_CO2_ppm": "Room CO2 Concentration [SIMULATED]",
            "Blood_Loss_ml": "Blood Loss Volume",
            "Age": "Patient Age",
            "Room_Occupancy": f"Derived Room Occupancy ({calculated_occupancy} occupants)",
            "Surgery_Duration_Min": "Surgery Duration",
            "Room_Temperature_C": "Room Temperature [SIMULATED]",
            "Room_Humidity_Pct": "Room Humidity [SIMULATED]",
            "Surgeon_Experience_Years": "Surgeon Experience",
            "Length_of_Stay_Days": "Length of Stay"
        }

        for idx in sorted_indices:
            feat_name = all_feature_names[idx]
            clean_name = feature_display_map.get(feat_name, feat_name.replace("_", " ").title())
            imp_val = float(importances[idx] * 100.0)
            
            top_factors.append(FeatureImportanceItem(
                feature=clean_name,
                importance=round(imp_val, 1),
                interpretation=f"Contributes significantly to risk calculation ({round(imp_val, 1)}% relative importance)."
            ))

    risk_rationale = generate_risk_rationale(risk_level, risk_probability, cp, env, op, calculated_occupancy)
    recommendations = generate_recommendations(env, op, cp, calculated_occupancy)
    disclaimer = ""

    other_ids = [p.patient_id for p in rp_list]

    return RiskPredictionResponse(
        patient_id=cp.patient_id,
        room_id=env.room_id,
        room_occupancy=calculated_occupancy,
        other_patient_ids=other_ids,
        risk_level=risk_level,
        risk_probability=round(risk_probability, 1),
        risk_rationale=risk_rationale,
        important_factors=top_factors,
        recommendations=recommendations,
        disclaimer=disclaimer
    )
