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
        <span className="step-number">Step 2</span>
        <h2>Patients Currently in the Room</h2>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="upload-box">
        <input
          type="file"
          id="room-patients-upload"
          accept=".csv,.json,.xlsx"
          onChange={handleFileUpload}
          className="file-input"
        />
        <label htmlFor="room-patients-upload" className="upload-label">
          📁 <strong>Upload Room Patients File (room_patients.csv)</strong>
        </label>
        {fileName && <p className="uploaded-file-name">Uploaded: <strong>{fileName}</strong></p>}
      </div>

      <div className="occupancy-summary-bar">
        <span>Room ID: <strong>{roomId}</strong></span>
        <span className="occupancy-badge">Total Room Occupancy: <strong>{calculatedOccupancy} occupants</strong> (1 Current + {roomPatients.length} Room)</span>
      </div>

      <div className="preview-card">
        <h3>Other Patients in Room</h3>
        {roomPatients.length === 0 ? (
          <p className="muted-text">No other patients added to this room yet.</p>
        ) : (
          <table className="patients-table">
            <thead>
              <tr>
                <th>Patient ID</th>
                <th>Age</th>
                <th>Gender</th>
                <th>Surgery Type</th>
                <th>Length of Stay</th>
                <th>Medical History</th>
              </tr>
            </thead>
            <tbody>
              {roomPatients.map((p, i) => (
                <tr key={i}>
                  <td><strong>{p.patient_id}</strong></td>
                  <td>{p.age} yrs</td>
                  <td>{p.gender}</td>
                  <td>{p.surgery_type}</td>
                  <td>{p.length_of_stay_days} days</td>
                  <td>{p.medical_history || 'None'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="step-footer flex-between">
        <button className="btn-secondary" onClick={onPrev}>
          ← Back
        </button>
        <button className="btn-primary" onClick={onNext}>
          Next: Environmental →
        </button>
      </div>
    </div>
  );
}
