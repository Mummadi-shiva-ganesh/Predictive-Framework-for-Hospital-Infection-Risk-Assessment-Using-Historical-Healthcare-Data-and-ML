import React, { useState } from 'react';
import Header from '../components/Header';
import Step1CurrentPatient from '../components/Step1CurrentPatient';
import Step2RoomPatients from '../components/Step2RoomPatients';
import Step3Environmental from '../components/Step3Environmental';
import Step4Operational from '../components/Step4Operational';
import Step5Review from '../components/Step5Review';
import RiskResult from '../components/RiskResult';
import { predictRisk, fetchSampleDemoData } from '../services/api';
import { MultiStepPredictionRequest, PredictionResponse } from '../types';

const INITIAL_WORKFLOW_STATE: MultiStepPredictionRequest = {
  current_patient: {
    patient_id: 'P001',
    age: 58,
    gender: 'Male',
    surgery_type: 'Orthopedic',
    surgery_duration_min: 180,
    anesthesia_type: 'General',
    pre_op_risk_level: 'High',
    blood_loss_ml: 450,
    surgeon_experience_years: 12,
    length_of_stay_days: 7,
    medical_history: 'Diabetes',
    previous_infection: 'No',
  },
  room_patients: [
    {
      room_id: 'R101',
      patient_id: 'P002',
      age: 67,
      gender: 'Female',
      surgery_type: 'Gynecological',
      length_of_stay_days: 5,
      medical_history: 'Hypertension',
      previous_infection: 'No',
      pre_op_risk_level: 'Medium',
    },
    {
      room_id: 'R101',
      patient_id: 'P003',
      age: 45,
      gender: 'Male',
      surgery_type: 'General',
      length_of_stay_days: 3,
      medical_history: 'None',
      previous_infection: 'No',
      pre_op_risk_level: 'Low',
    },
    {
      room_id: 'R101',
      patient_id: 'P004',
      age: 72,
      gender: 'Female',
      surgery_type: 'Cardiac',
      length_of_stay_days: 10,
      medical_history: 'Diabetes',
      previous_infection: 'Yes',
      pre_op_risk_level: 'High',
    },
  ],
  environmental_data: {
    room_id: 'R101',
    temperature: 29,
    humidity: 75,
    co2_level: 1200,
  },
  operational_data: {
    room_id: 'R101',
    ventilation_status: 'Poor',
    cleaning_interval: 18,
  },
};

export default function Dashboard() {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [formData, setFormData] = useState<MultiStepPredictionRequest>(INITIAL_WORKFLOW_STATE);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleLoadDemoData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const demoData = await fetchSampleDemoData();
      setFormData(demoData);
      setCurrentStep(5); // Jump straight to review step for 1-click evaluation
    } catch (err: any) {
      setError(err.message || 'Failed to load demo sample data.');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePredict = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await predictRisk(formData);
      setResult(response);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred during prediction.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    setCurrentStep(1);
    setFormData(INITIAL_WORKFLOW_STATE);
  };

  return (
    <div className="dashboard-layout">
      <Header />

      <main className="main-content">
        {error && <div className="error-banner">{error}</div>}

        {!result ? (
          <>
            {/* Top Quick Actions & Stepper Navigation */}
            <div className="workflow-top-bar">
              <div className="stepper-pills">
                <button className={`step-pill ${currentStep === 1 ? 'active' : ''}`} onClick={() => setCurrentStep(1)}>1. Patient</button>
                <button className={`step-pill ${currentStep === 2 ? 'active' : ''}`} onClick={() => setCurrentStep(2)}>2. Room Patients</button>
                <button className={`step-pill ${currentStep === 3 ? 'active' : ''}`} onClick={() => setCurrentStep(3)}>3. Environment</button>
                <button className={`step-pill ${currentStep === 4 ? 'active' : ''}`} onClick={() => setCurrentStep(4)}>4. Operations</button>
                <button className={`step-pill ${currentStep === 5 ? 'active' : ''}`} onClick={() => setCurrentStep(5)}>5. Review & Predict</button>
              </div>

              <button className="btn-demo-quick" onClick={handleLoadDemoData} disabled={isLoading}>
                ⚡ Load Sample Demo Files (1-Click Test)
              </button>
            </div>

            {/* Step Components */}
            {currentStep === 1 && (
              <Step1CurrentPatient
                patient={formData.current_patient}
                onChange={(cp) => setFormData(prev => ({ ...prev, current_patient: cp }))}
                onNext={() => setCurrentStep(2)}
              />
            )}

            {currentStep === 2 && (
              <Step2RoomPatients
                currentPatient={formData.current_patient}
                roomPatients={formData.room_patients}
                onChange={(rpList) => setFormData(prev => ({ ...prev, room_patients: rpList }))}
                onNext={() => setCurrentStep(3)}
                onPrev={() => setCurrentStep(1)}
              />
            )}

            {currentStep === 3 && (
              <Step3Environmental
                data={formData.environmental_data}
                onChange={(env) => setFormData(prev => ({ ...prev, environmental_data: env }))}
                onNext={() => setCurrentStep(4)}
                onPrev={() => setCurrentStep(2)}
              />
            )}

            {currentStep === 4 && (
              <Step4Operational
                data={formData.operational_data}
                onChange={(op) => setFormData(prev => ({ ...prev, operational_data: op }))}
                onNext={() => setCurrentStep(5)}
                onPrev={() => setCurrentStep(3)}
              />
            )}

            {currentStep === 5 && (
              <Step5Review
                data={formData}
                onPredict={handlePredict}
                onPrev={() => setCurrentStep(4)}
                isLoading={isLoading}
              />
            )}
          </>
        ) : (
          <RiskResult result={result} onReset={handleReset} />
        )}
      </main>
    </div>
  );
}
