import React from 'react';

interface Props {
  recommendations: string[];
}

export default function Recommendations({ recommendations }: Props) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="recommendations-card">
      <div className="section-card-header">
        <div className="section-icon-pill green">📋</div>
        <div>
          <h3>Actionable Clinical Recommendations</h3>
          <p className="section-card-sub">Infection control & surveillance mitigation strategies</p>
        </div>
      </div>

      <ul className="recommendations-list">
        {recommendations.map((rec, idx) => (
          <li key={idx} className="recommendation-item">
            <span className="rec-check-icon">✓</span>
            <span className="rec-text">{rec}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
