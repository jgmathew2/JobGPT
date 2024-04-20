// StatusPage.tsx
import React, { useState } from "react";
import SubmittedApplications from "@/components/SubmittedApplications";

const StatusPage: React.FC = () => {
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
          </div>
        </div>
      </header>
      <div>
        <SubmittedApplications />
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
