import { MultiStepPredictionRequest, PredictionResponse } from '../types';

const API_URL = 'http://localhost:8000';

export async function predictRisk(data: MultiStepPredictionRequest): Promise<PredictionResponse> {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const msg = errorData.detail || `Server error (${response.status}: ${response.statusText})`;
      throw new Error(msg);
    }

    return await response.json();
  } catch (error: any) {
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      throw new Error('Backend server is unavailable. Please ensure FastAPI server is running on http://localhost:8000');
    }
    throw error;
  }
}

export async function fetchSampleDemoData(): Promise<MultiStepPredictionRequest> {
  try {
    const response = await fetch(`${API_URL}/api/sample-demo`);
    if (!response.ok) {
      throw new Error(`Failed to load sample demo data (${response.status})`);
    }
    return await response.json();
  } catch (error: any) {
    throw new Error(`Error fetching demo data: ${error.message}`);
  }
}
