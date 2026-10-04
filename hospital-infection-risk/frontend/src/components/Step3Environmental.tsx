import React from 'react';
import { EnvironmentalData } from '../types';

interface Props {
  data: EnvironmentalData;
  onChange: (data: EnvironmentalData) => void;
  onNext: () => void;
  onPrev: () => void;
}

export default function Step3Environmental({ data, onChange, onNext, onPrev }: Props) {
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    onChange({
      ...data,
      [name]: Number(value)
    });
  };

  return (
    <div className="workflow-step-card">
      <div className="step-header">
        <span className="step-number">Step 3</span>
        <h2>Environmental Conditions <span className="simulated-badge">[SIMULATED DATA]</span></h2>
      </div>

      <div className="preview-card">
        <h3>Environmental Parameters</h3>
        <div className="form-grid">
          <div className="form-group">
            <label>Room Temperature (°C)</label>
            <input
              type="number"
              name="temperature"
              min="15"
              max="40"
              value={data.temperature}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label>Room Humidity (%)</label>
            <input
              type="number"
              name="humidity"
              min="0"
              max="100"
              value={data.humidity}
              onChange={handleInputChange}
            />
          </div>
          <div className="form-group">
            <label>CO2 Level (ppm)</label>
            <input
              type="number"
              name="co2_level"
              min="300"
              max="3000"
              value={data.co2_level}
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
          Next: Operational →
        </button>
      </div>
    </div>
  );
}
