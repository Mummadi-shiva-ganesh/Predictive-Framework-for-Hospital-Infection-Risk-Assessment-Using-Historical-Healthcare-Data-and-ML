import React, { useState } from 'react';
import { CurrentPatient, RoomPatient } from '../types';
import { parseUploadedFile } from '../utils/fileParser';

interface Props {
  currentPatient: CurrentPatient;
  roomPatients: RoomPatient[];
  onChange: (patients: RoomPatient[]) => void;
  onNext: () => void;
  onPrev: () => void;
}

export default function Step2RoomPatients({ currentPatient, roomPatients, onChange, onNext, onPrev }: Props) {
  const [fileName, setFileName] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setError(null);
    setFileName(file.name);

    try {
      const parsedData = await parseUploadedFile(file);
      const records = Array.isArray(parsedData) ? parsedData : [parsedData];

      if (!records || records.length === 0) {
        throw new Error('No patient records found in room patients file.');
      }

      const mappedPatients: RoomPatient[] = records.map((r, idx) => ({
        room_id: r.room_id || r.Room_ID || 'R101',
        patient_id: r.patient_id || r.Patient_ID || `P00${idx + 2}`,
        age: Number(r.age || r.Age || 60),
        gender: r.gender || r.Gender || 'Female',
        surgery_type: r.surgery_type || r.Surgery_Type || 'General',
        length_of_stay_days: Number(r.length_of_stay_days || r.Length_of_Stay_Days || 4),
        medical_history: r.medical_history || r.Medical_History || 'None',
        previous_infection: r.previous_infection || r.Previous_Infection || 'No',
        pre_op_risk_level: r.pre_op_risk_level || r.Pre_Op_Risk_Level || 'Medium'
      }));

      // Validation Rules
      const cpId = currentPatient.patient_id.trim().toUpperCase();
      const duplicateCP = mappedPatients.find(p => p.patient_id.trim().toUpperCase() === cpId);
      if (duplicateCP) {
        throw new Error(`Validation Error: Patient '${currentPatient.patient_id}' already exists as the current patient and cannot be included in the other-room-patients file.`);
      }

      onChange(mappedPatients);
    } catch (err: any) {
      setError(err.message || 'Error parsing room patients file.');
    }
  };

  const calculatedOccupancy = 1 + roomPatients.length;
  const roomId = roomPatients.length > 0 ? roomPatients[0].room_id : 'R101';

  return (
    <div className="workflow-step-card">
      <div className="step-header">
        <div className="step-header-left">
          <span className="step-number">Step 02</span>
          <div>
            <h2>Room Co-Occupancy Context</h2>
            <p className="step-subtitle">Inspect co-occupants in the same ward to assess cross-transmission risk</p>
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
          id="room-patients-upload"
          accept=".csv,.json,.xlsx"
          onChange={handleFileUpload}
          className="file-input"
        />
        <label htmlFor="room-patients-upload" className="upload-label">
          <div className="upload-icon-circle">🏥</div>
          <div className="upload-text-group">
            <span className="upload-title">Upload co-occupant patient list</span>
            <span className="upload-hint">Upload 5_patients_room_occupants.csv or other ward records</span>
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

      <div className="occupancy-summary-bar">
        <div className="occupancy-info">
          <span className="occupancy-label">Target Room:</span>
          <span className="occupancy-room-badge">{roomId}</span>
        </div>
        <div className="occupancy-pill">
          <span className="dot-indicator"></span>
          <span>Total Occupancy: <strong>{calculatedOccupancy} Patients</strong> (1 Current + {roomPatients.length} Co-occupants)</span>
        </div>
      </div>

      <div className="preview-card">
        <div className="preview-card-header">
          <h3>Other Patients in Room</h3>
          <span className="count-pill">{roomPatients.length} Records</span>
        </div>
        {roomPatients.length === 0 ? (
          <div className="empty-state">
            <p className="muted-text">No other patients currently mapped to this room.</p>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="patients-table">
              <thead>
                <tr>
                  <th>Patient ID</th>
                  <th>Age & Sex</th>
                  <th>Procedure</th>
                  <th>Pre-Op Risk</th>
                  <th>Stay Length</th>
                  <th>History</th>
                </tr>
              </thead>
              <tbody>
                {roomPatients.map((p, i) => (
                  <tr key={i}>
                    <td>
                      <span className="patient-id-cell">{p.patient_id}</span>
                    </td>
                    <td>{p.age} yrs • {p.gender}</td>
                    <td>{p.surgery_type}</td>
                    <td>
                      <span className={`risk-badge-pill-sm risk-${(p.pre_op_risk_level || 'low').toLowerCase()}`}>
                        {p.pre_op_risk_level || 'Low'}
                      </span>
                    </td>
                    <td>{p.length_of_stay_days} days</td>
                    <td>{p.medical_history || 'None'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="step-footer flex-between">
        <button type="button" className="btn-secondary" onClick={onPrev}>
          ← Previous
        </button>
        <button type="button" className="btn-primary" onClick={onNext}>
          <span>Continue to Environmental</span>
          <span className="btn-arrow">→</span>
        </button>
      </div>
    </div>
  );
}
