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
        <span className="step-number">Step 1</span>
        <h2>Upload Current Patient Details</h2>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="upload-box">
        <input
          type="file"
          id="current-patient-upload"
          accept=".csv,.json,.xlsx"
          onChange={handleFileUpload}
          className="file-input"
        />
        <label htmlFor="current-patient-upload" className="upload-label">
          📁 <strong>Click to Upload Patient File</strong> (CSV, JSON, XLSX)
        </label>
        {fileName && <p className="uploaded-file-name">Uploaded: <strong>{fileName}</strong></p>}
      </div>

      <div className="preview-card">
        <h3>Patient Record Preview</h3>
        <div className="preview-grid">
          <div><span>Patient ID:</span> <strong>{patient.patient_id}</strong></div>
          <div><span>Age:</span> <strong>{patient.age} years</strong></div>
          <div><span>Gender:</span> <strong>{patient.gender}</strong></div>
          <div><span>Surgery Type:</span> <strong>{patient.surgery_type}</strong></div>
          <div><span>Duration:</span> <strong>{patient.surgery_duration_min} mins</strong></div>
          <div><span>Pre-Op Risk:</span> <strong className={`risk-tag-${patient.pre_op_risk_level.toLowerCase()}`}>{patient.pre_op_risk_level}</strong></div>
          <div><span>Blood Loss:</span> <strong>{patient.blood_loss_ml} ml</strong></div>
          <div><span>Surgeon Experience:</span> <strong>{patient.surgeon_experience_years} yrs</strong></div>
          <div><span>Length of Stay:</span> <strong>{patient.length_of_stay_days} days</strong></div>
          <div><span>Medical History:</span> <strong>{patient.medical_history || 'None'}</strong></div>
        </div>
      </div>

      <div className="step-footer">
        <button className="btn-primary" onClick={onNext}>
          Next: Room Patients →
        </button>
      </div>
    </div>
  );
}
