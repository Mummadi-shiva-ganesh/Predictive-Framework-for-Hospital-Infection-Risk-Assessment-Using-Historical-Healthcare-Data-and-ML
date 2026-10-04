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
        <span className="step-number">Step 4</span>
        <h2>Operational Conditions <span className="simulated-badge">[SIMULATED DATA]</span></h2>
      </div>

      <div className="preview-card">
        <h3>Operational Parameters</h3>
        <div className="form-grid">
          <div className="form-group">
            <label>Ventilation Status</label>
            <select
              name="ventilation_status"
              value={data.ventilation_status}
              onChange={handleInputChange}
            >
              <option value="Good">Good</option>
              <option value="Moderate">Moderate</option>
              <option value="Poor">Poor</option>
            </select>
          </div>
          <div className="form-group">
            <label>Cleaning Interval (Hours)</label>
            <input
              type="number"
              name="cleaning_interval"
              min="1"
              max="48"
              value={data.cleaning_interval}
              onChange={handleInputChange}
            />
          </div>
        </div>
      </div>

      <div className="step-footer flex-between">
        <button className="btn-secondary" onClick={onPrev}>
          ← Back
        </button>
        <button className="btn-primary" onClick={onNext}>
          Next: Review & Confirm →
        </button>
      </div>
    </div>
  );
}
