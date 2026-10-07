import React, { useState } from 'react';
import { CurrentPatient } from '../types';
import { parseUploadedFile } from '../utils/fileParser';

interface Props {
  patient: CurrentPatient;
  onChange: (patient: CurrentPatient) => void;
  onNext: () => void;
}

export default function Step1CurrentPatient({ patient, onChange, onNext }: Props) {
  const [fileName, setFileName] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setError(null);
    setFileName(file.name);

    try {
      const parsedData = await parseUploadedFile(file);
      const rawRecord = Array.isArray(parsedData) ? parsedData[0] : parsedData;

      if (!rawRecord) {
        throw new Error('No valid patient record found in uploaded file.');
      }

      // Map fields (handling different column casing)
      const mappedPatient: CurrentPatient = {
        patient_id: rawRecord.patient_id || rawRecord.Patient_ID || 'P001',
        age: Number(rawRecord.age || rawRecord.Age || 50),
        gender: rawRecord.gender || rawRecord.Gender || 'Male',
        surgery_type: rawRecord.surgery_type || rawRecord.Surgery_Type || 'General',
        surgery_duration_min: Number(rawRecord.surgery_duration_min || rawRecord.Surgery_Duration_Min || 120),
        anesthesia_type: rawRecord.anesthesia_type || rawRecord.Anesthesia_Type || 'General',
        pre_op_risk_level: rawRecord.pre_op_risk_level || rawRecord.Pre_Op_Risk_Level || 'Low',
        blood_loss_ml: Number(rawRecord.blood_loss_ml || rawRecord.Blood_Loss_ml || 150),
        surgeon_experience_years: Number(rawRecord.surgeon_experience_years || rawRecord.Surgeon_Experience_Years || 10),
        length_of_stay_days: Number(rawRecord.length_of_stay_days || rawRecord.Length_of_Stay_Days || 5),
        medical_history: rawRecord.medical_history || rawRecord.Medical_History || 'None',
        previous_infection: rawRecord.previous_infection || rawRecord.Previous_Infection || 'No',
      };

      // Validation
      if (mappedPatient.age < 0 || mappedPatient.age > 120) {
        throw new Error(`Invalid patient age: ${mappedPatient.age}. Must be between 0 and 120.`);
      }

      onChange(mappedPatient);
    } catch (err: any) {
      setError(err.message || 'Error processing uploaded file.');
    }
  };

  return (
    <div className="workflow-step-card">
      <div className="step-header">
        <div className="step-header-left">
          <span className="step-number">Step 01</span>
          <div>
            <h2>Current Surgical Patient</h2>
            <p className="step-subtitle">Upload clinical profile or review the active patient's surgical variables</p>
          </div>
        </div>
      </div>

      {error && (
        <div className="error-banner">
          <span className="error-icon">⚠️</span>
          <span>{error}</span>
        </div>
      )}

      <div className="upload-box">
        <input
          type="file"
          id="current-patient-upload"
          accept=".csv,.json,.xlsx"
          onChange={handleFileUpload}
          className="file-input"
        />
        <label htmlFor="current-patient-upload" className="upload-label">
          <div className="upload-icon-circle">📂</div>
          <div className="upload-text-group">
            <span className="upload-title">Click to upload patient record</span>
            <span className="upload-hint">Supports CSV, JSON, or XLSX (e.g., patient_P001_high_risk.csv)</span>
          </div>
        </label>
        {fileName && (
          <div className="uploaded-file-chip">
            <span className="chip-icon">📄</span>
            <span className="chip-name">{fileName}</span>
            <span className="chip-badge">Loaded</span>
          </div>
        )}
      </div>

      <div className="preview-card">
        <div className="preview-card-header">
          <h3>Active Patient Data Summary</h3>
          <span className="patient-id-tag">{patient.patient_id}</span>
        </div>
        <div className="preview-grid">
          <div className="data-metric">
            <span className="metric-label">Age & Gender</span>
            <strong className="metric-value">{patient.age} yrs • {patient.gender}</strong>
          </div>
          <div className="data-metric">
            <span className="metric-label">Procedure</span>
            <strong className="metric-value">{patient.surgery_type}</strong>
          </div>
          <div className="data-metric">
            <span className="metric-label">Surgery Duration</span>
            <strong className="metric-value">{patient.surgery_duration_min} mins</strong>
          </div>
          <div className="data-metric">
            <span className="metric-label">Pre-Op Risk Rating</span>
            <span className={`risk-badge-pill risk-${patient.pre_op_risk_level.toLowerCase()}`}>
              {patient.pre_op_risk_level}
            </span>
          </div>
          <div className="data-metric">
            <span className="metric-label">Blood Loss</span>
            <strong className="metric-value">{patient.blood_loss_ml} ml</strong>
          </div>
          <div className="data-metric">
            <span className="metric-label">Surgeon Experience</span>
            <strong className="metric-value">{patient.surgeon_experience_years} years</strong>
          </div>
          <div className="data-metric">
            <span className="metric-label">Length of Stay</span>
            <strong className="metric-value">{patient.length_of_stay_days} days</strong>
          </div>
          <div className="data-metric">
            <span className="metric-label">Medical History</span>
            <strong className="metric-value">{patient.medical_history || 'None'}</strong>
          </div>
        </div>
      </div>

      <div className="step-footer">
        <button type="button" className="btn-primary" onClick={onNext}>
          <span>Continue to Room Context</span>
          <span className="btn-arrow">→</span>
        </button>
      </div>
    </div>
  );
}
