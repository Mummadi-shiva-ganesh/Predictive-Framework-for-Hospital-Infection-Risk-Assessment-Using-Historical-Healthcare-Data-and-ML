import React from 'react';
import { ImportantFactor } from '../types';

interface Props {
  factors: ImportantFactor[];
}

export default function FactorsDisplay({ factors }: Props) {
  if (!factors || factors.length === 0) return null;

  return (
    <div className="factors-card">
      <div className="section-card-header">
        <div className="section-icon-pill blue">🎯</div>
        <div>
          <h3>Key Influencing Factors</h3>
          <p className="section-card-sub">Top features identified by the predictive model</p>
        </div>
      </div>

      <ul className="factors-list">
        {factors.map((factor, idx) => (
          <li key={idx} className="factor-item">
            <div className="factor-header">
              <div className="factor-name-wrapper">
                <span className="factor-rank-badge">#{idx + 1}</span>
                <span className="factor-name">{factor.feature}</span>
              </div>
              <span className="factor-importance-pill">
                Weight: {factor.importance.toFixed(1)}%
              </span>
            </div>
            <div className="factor-bar-track">
              <div
                className="factor-bar-fill"
                style={{ width: `${Math.min(factor.importance * 3, 100)}%` }}
              ></div>
            </div>
            <p className="factor-interpretation">{factor.interpretation}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
