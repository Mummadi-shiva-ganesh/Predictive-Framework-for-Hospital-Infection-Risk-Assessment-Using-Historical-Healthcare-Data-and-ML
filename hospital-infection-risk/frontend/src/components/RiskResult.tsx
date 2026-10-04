import React from 'react';
import { PredictionResponse } from '../types';
import FactorsDisplay from './FactorsDisplay';
import Recommendations from './Recommendations';

interface Props {
  result: PredictionResponse;
  onReset: () => void;
}

export default function RiskResult({ result, onReset }: Props) {
  const getRiskColorClass = (level: string) => {
    switch (level) {
      case 'LOW':
        return 'risk-low';
      case 'MEDIUM':
        return 'risk-medium';
      case 'HIGH':
        return 'risk-high';
      default:
        return 'risk-low';
    }
  };

  return (
    <div className="result-container">
      <div className="result-header-card">
        <h2>INFECTION RISK ASSESSMENT</h2>
        <div className="result-metadata-strip">
          <div><span>Current Patient:</span> <strong>{result.patient_id}</strong></div>
          <div><span>Room ID:</span> <strong>{result.room_id}</strong></div>
          <div><span>Total Room Occupancy:</span> <strong>{result.room_occupancy} Patients</strong></div>
          {result.other_patient_ids && result.other_patient_ids.length > 0 && (
            <div><span>Other Occupants:</span> <strong>{result.other_patient_ids.join(', ')}</strong></div>
          )}
        </div>

        <div className={`risk-badge ${getRiskColorClass(result.risk_level)}`}>
          <span className="risk-level-text">{result.risk_level} RISK</span>
          <span className="risk-prob-text">{result.risk_probability.toFixed(1)}% Calculated Probability</span>
        </div>
      </div>

      {/* Dynamic Risk Rationale & Reasoning Box */}
      {result.risk_rationale && (
        <div className="rationale-card">
          <h3>💡 Risk Assessment Rationale & Clinical Explanation</h3>
          <p className="rationale-text">{result.risk_rationale}</p>
        </div>
      )}

      <div className="result-details">
        <FactorsDisplay factors={result.important_factors} />
        <Recommendations recommendations={result.recommendations} />
      </div>

      <div className="action-row">
        <button className="btn-primary btn-large" onClick={onReset}>
          🔄 Start New Patient Assessment
        </button>
      </div>
    </div>
  );
}
