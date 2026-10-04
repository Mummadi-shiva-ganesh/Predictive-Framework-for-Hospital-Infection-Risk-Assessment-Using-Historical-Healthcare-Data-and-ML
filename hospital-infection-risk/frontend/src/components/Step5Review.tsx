import React from 'react';
import { MultiStepPredictionRequest } from '../types';

interface Props {
  data: MultiStepPredictionRequest;
  onPredict: () => void;
  onPrev: () => void;
  isLoading: boolean;
}

export default function Step5Review({ data, onPredict, onPrev, isLoading }: Props) {
  const cp = data.current_patient;
  const rpList = data.room_patients;
  const env = data.environmental_data;
  const op = data.operational_data;

  const totalOccupancy = 1 + rpList.length;

  return (
    <div className="workflow-step-card">
      <div className="step-header">
        <span className="step-number">Step 5</span>
        <h2>Review Uploaded Data & Confirm</h2>
      </div>

      <div className="review-summary-grid">
        {/* Current Patient */}
        <div className="review-block">
          <h3>👤 Current Patient Details</h3>
          <p><strong>Patient ID:</strong> {cp.patient_id}</p>
          <p><strong>Age / Gender:</strong> {cp.age} yrs | {cp.gender}</p>
          <p><strong>Surgery:</strong> {cp.surgery_type} ({cp.surgery_duration_min} mins)</p>
          <p><strong>Pre-Op Risk:</strong> <span className={`risk-tag-${cp.pre_op_risk_level.toLowerCase()}`}>{cp.pre_op_risk_level}</span></p>
          <p><strong>Length of Stay:</strong> {cp.length_of_stay_days} days</p>
        </div>

        {/* Room Patients & Occupancy */}
        <div className="review-block">
          <h3>🏥 Room Occupancy & Patients</h3>
          <p><strong>Room ID:</strong> {env.room_id}</p>
          <p><strong>Total Occupants:</strong> <span className="highlight-tag">{totalOccupancy} Patients</span></p>
          <p><strong>Other Patients in Room:</strong> {rpList.length > 0 ? rpList.map(p => p.patient_id).join(', ') : 'None'}</p>
        </div>

        {/* Environment */}
        <div className="review-block">
          <h3>🌡️ Environmental Conditions <span className="simulated-badge">[SIMULATED]</span></h3>
          <p><strong>Temperature:</strong> {env.temperature} °C</p>
          <p><strong>Humidity:</strong> {env.humidity} %</p>
          <p><strong>CO2 Concentration:</strong> {env.co2_level} ppm</p>
        </div>

        {/* Operations */}
        <div className="review-block">
          <h3>🧹 Operational Conditions <span className="simulated-badge">[SIMULATED]</span></h3>
          <p><strong>Ventilation Status:</strong> {op.ventilation_status}</p>
          <p><strong>Cleaning Interval:</strong> {op.cleaning_interval} hours</p>
        </div>
      </div>

      <div className="step-footer flex-between">
        <button className="btn-secondary" onClick={onPrev} disabled={isLoading}>
          ← Edit Parameters
        </button>
        <button className="btn-primary btn-large" onClick={onPredict} disabled={isLoading}>
          {isLoading ? <span className="spinner"></span> : '🚀 Predict Infection Risk'}
        </button>
      </div>
    </div>
  );
}
