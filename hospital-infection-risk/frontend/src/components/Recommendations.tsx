import React from 'react';

interface Props {
  recommendations: string[];
}

export default function Recommendations({ recommendations }: Props) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="recommendations-card">
      <h3>Preventive Recommendations</h3>
      <ul className="recommendations-list">
        {recommendations.map((rec, idx) => (
          <li key={idx} className="recommendation-item">
            {rec}
          </li>
        ))}
      </ul>
    </div>
  );
}
