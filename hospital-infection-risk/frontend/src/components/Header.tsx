import React from 'react';

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-content">
        <div className="header-brand">
          <div className="header-logo-badge">
            <span className="logo-symbol">⚕️</span>
          </div>
          <div className="header-titles">
            <h1>InfectiGuard AI</h1>
            <p className="subtitle">Predictive Intelligence Framework for Hospital Infection Risk Assessment</p>
          </div>
        </div>
        <div className="header-meta-badge">
          <span className="badge-pulse"></span>
          <span className="badge-text">Clinical Decision Support System</span>
        </div>
      </div>
    </header>
  );
}
