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
        <div className="step-header-left">
          <span className="step-number">Step 05</span>
          <div>
            <h2>Review Holistic Multi-Source Variables</h2>
            <p className="step-subtitle">Verify patient clinical factors, ward occupancy, environmental readings, and sanitation metrics before ML execution</p>
          </div>
        </div>
      </div>

      <div className="review-summary-grid">
        {/* Current Patient */}
        <div className="review-block">
          <div className="review-block-header">
            <span className="block-icon">👤</span>
            <h3>Active Surgical Patient</h3>
          </div>
          <div className="review-block-body">
            <div className="review-row">
              <span className="label">Patient ID</span>
              <strong className="value">{cp.patient_id}</strong>
            </div>
            <div className="review-row">
              <span className="label">Age & Gender</span>
              <span className="value">{cp.age} yrs • {cp.gender}</span>
            </div>
            <div className="review-row">
              <span className="label">Surgical Procedure</span>
              <span className="value">{cp.surgery_type} ({cp.surgery_duration_min} mins)</span>
            </div>
            <div className="review-row">
              <span className="label">Pre-Operative Risk</span>
              <span className={`risk-badge-pill-sm risk-${cp.pre_op_risk_level.toLowerCase()}`}>
                {cp.pre_op_risk_level}
              </span>
            </div>
            <div className="review-row">
              <span className="label">Hospital Stay</span>
              <span className="value">{cp.length_of_stay_days} days</span>
            </div>
          </div>
        </div>

        {/* Room Patients & Occupancy */}
        <div className="review-block">
          <div className="review-block-header">
            <span className="block-icon">🏥</span>
            <h3>Ward Room & Co-Occupancy</h3>
          </div>
          <div className="review-block-body">
            <div className="review-row">
              <span className="label">Target Room</span>
              <strong className="value room-pill">{env.room_id}</strong>
            </div>
            <div className="review-row">
              <span className="label">Total Occupancy</span>
              <span className="highlight-tag">{totalOccupancy} Active Patients</span>
            </div>
            <div className="review-row">
              <span className="label">Co-Occupants in Room</span>
              <span className="value text-truncate">
                {rpList.length > 0 ? rpList.map((p) => p.patient_id).join(', ') : 'None'}
              </span>
            </div>
          </div>
        </div>

        {/* Environment */}
        <div className="review-block">
          <div className="review-block-header">
            <span className="block-icon">🌡️</span>
            <div>
              <h3>Indoor Climate</h3>
              <span className="simulated-badge-sm">SIMULATED</span>
            </div>
          </div>
          <div className="review-block-body">
            <div className="review-row">
              <span className="label">Room Temperature</span>
              <span className="value">{env.temperature} °C</span>
            </div>
            <div className="review-row">
              <span className="label">Relative Humidity</span>
              <span className="value">{env.humidity} %</span>
            </div>
            <div className="review-row">
              <span className="label">CO₂ Concentration</span>
              <span className="value">{env.co2_level} ppm</span>
            </div>
          </div>
        </div>

        {/* Operations */}
        <div className="review-block">
          <div className="review-block-header">
            <span className="block-icon">🧹</span>
            <div>
              <h3>Infection Control Operations</h3>
              <span className="simulated-badge-sm">SIMULATED</span>
            </div>
          </div>
          <div className="review-block-body">
            <div className="review-row">
              <span className="label">Air Ventilation Quality</span>
              <span className="value font-semibold">{op.ventilation_status}</span>
            </div>
            <div className="review-row">
              <span className="label">Cleaning Frequency</span>
              <span className="value font-semibold">{op.cleaning_interval} hours</span>
            </div>
          </div>
        </div>
      </div>

      <div className="step-footer flex-between">
        <button type="button" className="btn-secondary" onClick={onPrev} disabled={isLoading}>
          ← Modify Parameters
        </button>
        <button type="button" className="btn-predict-cta" onClick={onPredict} disabled={isLoading}>
          {isLoading ? (
            <span className="loading-state">
              <span className="spinner"></span>
              <span>Running Machine Learning Assessment...</span>
            </span>
          ) : (
            <>
              <span className="cta-icon">⚡</span>
              <span>Execute Risk Assessment</span>
              <span className="btn-arrow">→</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
