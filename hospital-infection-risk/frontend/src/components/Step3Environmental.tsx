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
        <div className="step-header-left">
          <span className="step-number">Step 03</span>
          <div>
            <div className="title-with-badge">
              <h2>Environmental Room Sensors</h2>
              <span className="simulated-badge">SIMULATED IOT</span>
            </div>
            <p className="step-subtitle">Inspect indoor climate metrics for pathogen viability and airborne risk</p>
          </div>
        </div>
      </div>

      <div className="preview-card">
        <div className="preview-card-header">
          <h3>Ambient Sensor Telemetry</h3>
          <span className="room-id-tag">Ward Room {data.room_id}</span>
        </div>

        <div className="form-grid">
          <div className="form-group-card">
            <div className="param-header">
              <span className="param-icon">🌡️</span>
              <label htmlFor="temp-input">Room Temperature</label>
            </div>
            <div className="input-with-unit">
              <input
                id="temp-input"
                type="number"
                name="temperature"
                min="15"
                max="40"
                step="0.1"
                value={data.temperature}
                onChange={handleInputChange}
              />
              <span className="unit-label">°C</span>
            </div>
            <span className="param-guide">Target: 20°C - 24°C</span>
          </div>

          <div className="form-group-card">
            <div className="param-header">
              <span className="param-icon">💧</span>
              <label htmlFor="humidity-input">Relative Humidity</label>
            </div>
            <div className="input-with-unit">
              <input
                id="humidity-input"
                type="number"
                name="humidity"
                min="0"
                max="100"
                value={data.humidity}
                onChange={handleInputChange}
              />
              <span className="unit-label">%</span>
            </div>
            <span className="param-guide">Target: 40% - 60%</span>
          </div>

          <div className="form-group-card">
            <div className="param-header">
              <span className="param-icon">🍃</span>
              <label htmlFor="co2-input">Carbon Dioxide (CO₂)</label>
            </div>
            <div className="input-with-unit">
              <input
                id="co2-input"
                type="number"
                name="co2_level"
                min="300"
                max="3000"
                value={data.co2_level}
                onChange={handleInputChange}
              />
              <span className="unit-label">ppm</span>
            </div>
            <span className="param-guide">Target: &lt; 700 ppm</span>
          </div>
        </div>
      </div>

      <div className="step-footer flex-between">
        <button type="button" className="btn-secondary" onClick={onPrev}>
          ← Previous
        </button>
        <button type="button" className="btn-primary" onClick={onNext}>
          <span>Continue to Operational</span>
          <span className="btn-arrow">→</span>
        </button>
      </div>
    </div>
  );
}
