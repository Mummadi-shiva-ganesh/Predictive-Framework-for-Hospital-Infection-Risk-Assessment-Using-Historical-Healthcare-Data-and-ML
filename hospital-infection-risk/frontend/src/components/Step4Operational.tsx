import React from 'react';
import { OperationalData } from '../types';

interface Props {
  data: OperationalData;
  onChange: (data: OperationalData) => void;
  onNext: () => void;
  onPrev: () => void;
}

export default function Step4Operational({ data, onChange, onNext, onPrev }: Props) {
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    onChange({
      ...data,
      [name]: name === 'cleaning_interval' ? Number(value) : value
    });
  };

  return (
    <div className="workflow-step-card">
      <div className="step-header">
        <div className="step-header-left">
          <span className="step-number">Step 04</span>
          <div>
            <div className="title-with-badge">
              <h2>Hospital Operational Safeguards</h2>
              <span className="simulated-badge">SIMULATED PROTOCOLS</span>
            </div>
            <p className="step-subtitle">Sanitation cycles and HVAC filtration parameters controlling surface and aerosol bacterial load</p>
          </div>
        </div>
      </div>

      <div className="preview-card">
        <div className="preview-card-header">
          <h3>Infection Control Protocols</h3>
          <span className="room-id-tag">Ward Room {data.room_id}</span>
        </div>

        <div className="form-grid">
          <div className="form-group-card">
            <div className="param-header">
              <span className="param-icon">💨</span>
              <label htmlFor="ventilation-select">Ventilation & Air Exchanges</label>
            </div>
            <div className="select-wrapper">
              <select
                id="ventilation-select"
                name="ventilation_status"
                value={data.ventilation_status}
                onChange={handleInputChange}
                className="custom-select"
              >
                <option value="Good">Good (HEPA / ≥12 ACH Standard)</option>
                <option value="Moderate">Moderate (6 - 11 ACH Normal)</option>
                <option value="Poor">Poor (&lt;6 ACH Insufficient)</option>
              </select>
            </div>
            <span className="param-guide">Optimal: Good Air Filtration</span>
          </div>

          <div className="form-group-card">
            <div className="param-header">
              <span className="param-icon">🧹</span>
              <label htmlFor="cleaning-input">Sanitization & Cleaning Interval</label>
            </div>
            <div className="input-with-unit">
              <input
                id="cleaning-input"
                type="number"
                name="cleaning_interval"
                min="1"
                max="48"
                step="0.5"
                value={data.cleaning_interval}
                onChange={handleInputChange}
              />
              <span className="unit-label">Hours</span>
            </div>
            <span className="param-guide">Target: ≤ 6 hours between disinfections</span>
          </div>
        </div>
      </div>

      <div className="step-footer flex-between">
        <button type="button" className="btn-secondary" onClick={onPrev}>
          ← Previous
        </button>
        <button type="button" className="btn-primary" onClick={onNext}>
          <span>Continue to Final Review</span>
          <span className="btn-arrow">→</span>
        </button>
      </div>
    </div>
  );
}
