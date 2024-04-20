// StatusPage.tsx
import React, { useState } from 'react';

const StatusPage: React.FC = () => {
  const [companyList, setCompanyList] = useState(['Google STEP', 'Meta University']);
  const [applicationCount, setApplicationCount] = useState(2);

  // Placeholder functions to mimic actions
  const handleStart = () => {
  };

  const handleStop = () => {
  };

  return (
    <div className="status-page">
      <header className="status-header">
        <h1>JOB-GPT</h1>
        <h2>Application Success!</h2>
      </header>
      <div className="company-list">
        {companyList.map((company, index) => (
          <div key={index}>{company}</div>
        ))}
      </div>
      <p className="applications-submitted">Applications submitted: {applicationCount}</p>
      <div className="actions">
        <button onClick={handleStart} className="action-button">START</button>
        <button onClick={handleStop} className="action-button">STOP</button>
      </div>
    </div>
  );
};

export default StatusPage;
