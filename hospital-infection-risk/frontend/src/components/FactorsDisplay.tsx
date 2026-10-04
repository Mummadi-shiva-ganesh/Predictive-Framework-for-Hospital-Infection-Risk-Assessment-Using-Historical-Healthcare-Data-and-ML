import React from 'react';
import { ImportantFactor } from '../types';

interface Props {
  factors: ImportantFactor[];
}

export default function FactorsDisplay({ factors }: Props) {
  if (!factors || factors.length === 0) return null;

  return (
    <div className="factors-card">
      <h3>Key Risk Factors</h3>
      <ul className="factors-list">
        {factors.map((factor, idx) => (
          <li key={idx} className="factor-item">
            <div className="factor-header">
              <span className="factor-name">{factor.feature}</span>
              <span className="factor-importance">
                Impact: {factor.importance.toFixed(1)}%
              </span>
            </div>
            <p className="factor-interpretation">{factor.interpretation}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
