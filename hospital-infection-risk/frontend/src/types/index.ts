export interface CurrentPatient {
  patient_id: string;
  age: number;
  gender: string;
  surgery_type: string;
  surgery_duration_min: number;
  anesthesia_type: string;
  pre_op_risk_level: string;
  blood_loss_ml: number;
  surgeon_experience_years: number;
  length_of_stay_days: number;
  medical_history?: string;
  previous_infection?: string;
}

export interface RoomPatient {
  room_id: string;
  patient_id: string;
  age: number;
  gender: string;
  surgery_type: string;
  surgery_duration_min?: number;
  anesthesia_type?: string;
  pre_op_risk_level?: string;
  blood_loss_ml?: number;
  surgeon_experience_years?: number;
  length_of_stay_days: number;
  medical_history?: string;
  previous_infection?: string;
}

export interface EnvironmentalData {
  room_id: string;
  temperature: number;
  humidity: number;
  co2_level: number;
}

export interface OperationalData {
  room_id: string;
  ventilation_status: string;
  cleaning_interval: number;
}

export interface MultiStepPredictionRequest {
  current_patient: CurrentPatient;
  room_patients: RoomPatient[];
  environmental_data: EnvironmentalData;
  operational_data: OperationalData;
}

export interface ImportantFactor {
  feature: string;
  importance: number;
  interpretation: string;
}

export interface PredictionResponse {
  patient_id: string;
  room_id: string;
  room_occupancy: number;
  other_patient_ids: string[];
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  risk_probability: number;
  risk_rationale: string;
  important_factors: ImportantFactor[];
  recommendations: string[];
  disclaimer: string;
}
