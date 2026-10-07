import React from 'react';
import { PredictionResponse } from '../types';
import FactorsDisplay from './FactorsDisplay';
import Recommendations from './Recommendations';

interface Props {
  result: PredictionResponse;
  onReset: () => void;
}

export default function RiskResult({ result, onReset }: Props) {
  const getRiskTheme = (level: string) => {
    switch (level) {
      case 'LOW':
        return {
          cardClass: 'theme-low',
          badgeClass: 'badge-low',
          icon: '🛡️',
          label: 'Low Risk of Infection',
          statusText: 'Clinical & environmental indicators reside within safe hospital baseline tolerances.',
        };
      case 'MEDIUM':
        return {
          cardClass: 'theme-medium',
          badgeClass: 'badge-medium',
          icon: '⚠️',
          label: 'Moderate Infection Risk',
          statusText: 'Surveillance advised. Several patient or environmental thresholds warrant proactive monitoring.',
        };
      case 'HIGH':
        return {
          cardClass: 'theme-high',
          badgeClass: 'badge-high',
          icon: '🚨',
          label: 'Elevated Infection Risk',
          statusText: 'High infection susceptibility detected. Immediate preventive precautions and hygiene protocol reinforcement recommended.',
        };
      default:
        return {
          cardClass: 'theme-low',
          badgeClass: 'badge-low',
          icon: '🛡️',
          label: 'Low Risk',
          statusText: 'Baseline tolerances met.',
        };
    }
  };

  const theme = getRiskTheme(result.risk_level);

  return (
    <div className="result-container animate-fade-in">
      <div className={`result-hero-card ${theme.cardClass}`}>
        <div className="result-hero-top">
          <div className="result-hero-title-area">
            <span className="result-kicker">ANALYSIS COMPLETE</span>
            <h2>Infection Risk Evaluation</h2>
          </div>
          <div className="result-patient-pill">
            <span className="pill-dot"></span>
            <span>Patient ID: <strong>{result.patient_id}</strong> (Room {result.room_id})</span>
          </div>
        </div>

        <div className="result-score-banner">
          <div className="score-badge-container">
            <div className={`score-badge ${theme.badgeClass}`}>
              <div className="score-badge-icon">{theme.icon}</div>
              <div className="score-badge-details">
                <span className="score-level-title">{result.risk_level} RISK</span>
                <span className="score-subtitle">{theme.label}</span>
              </div>
            </div>
          </div>

          <div className="probability-meter-card">
            <div className="meter-label-row">
              <span className="meter-title">Calculated ML Confidence</span>
              <span className="meter-percentage">{result.risk_probability.toFixed(1)}%</span>
            </div>
            <div className="progress-bar-track">
              <div
                className={`progress-bar-fill fill-${result.risk_level.toLowerCase()}`}
                style={{ width: `${Math.min(Math.max(result.risk_probability, 5), 100)}%` }}
              ></div>
            </div>
            <p className="meter-help-text">{theme.statusText}</p>
          </div>
        </div>

        <div className="result-metadata-grid">
          <div className="meta-box">
            <span className="meta-label">Target Patient</span>
            <strong className="meta-val">{result.patient_id}</strong>
          </div>
          <div className="meta-box">
            <span className="meta-label">Location</span>
            <strong className="meta-val">Room {result.room_id}</strong>
          </div>
          <div className="meta-box">
            <span className="meta-label">Room Density</span>
            <strong className="meta-val">{result.room_occupancy} Patients</strong>
          </div>
          <div className="meta-box">
            <span className="meta-label">Other Room Occupants</span>
            <strong className="meta-val">
              {result.other_patient_ids && result.other_patient_ids.length > 0
                ? result.other_patient_ids.join(', ')
                : 'None (Single Occupancy)'}
            </strong>
          </div>
        </div>
      </div>

      {/* Dynamic Risk Rationale & Reasoning Box */}
      {result.risk_rationale && (
        <div className="rationale-card">
          <div className="rationale-header">
            <div className="rationale-icon-box">💡</div>
            <div>
              <h3>Explainable AI Rationale & Clinical Attribution</h3>
              <p className="rationale-sub">Machine learning feature importance and environmental threshold triggers</p>
            </div>
          </div>
          <p className="rationale-text">{result.risk_rationale}</p>
        </div>
      )}

      <div className="result-details-grid">
        <FactorsDisplay factors={result.important_factors} />
        <Recommendations recommendations={result.recommendations} />
      </div>

      <div className="action-row">
        <button type="button" className="btn-primary btn-large btn-new-assessment" onClick={onReset}>
          <span>🔄 Conduct Another Assessment</span>
        </button>
      </div>
    </div>
  );
}
