// StatusPage.tsx
import React, { useState } from "react";

const StatusPage: React.FC = () => {
  const [companyList, setCompanyList] = useState([
    "Google STEP",
    "Meta University",
  ]);
  const [applicationCount, setApplicationCount] = useState(2);

  // Placeholder functions to mimic actions
  const handleStart = () => {};

  const handleStop = () => {};

  return (
    <div style={{ placeItems: "normal" }}>
      <header>
        <div className="container">
          <div className="columns">
            <h1 className="column has-text-centered">JOB-GPT</h1>
          </div>
        </div>
        <div className="container">
          <div className="columns is-centered">
            <h2 className="columns" style={{ fontSize: 25 }}>
              Application Success!
            </h2>
          </div>
        </div>
      </header>
      <div className="">
        {companyList.map((company, index) => (
          <div key={index}>{company}</div>
        ))}
      </div>
      <p>Applications submitted: {applicationCount}</p>
      <div>
        <button onClick={handleStart} className="action-button">
          START
        </button>
        <button onClick={handleStop} className="action-button">
          STOP
        </button>
      </div>
    </div>
  );
};

export default StatusPage;
