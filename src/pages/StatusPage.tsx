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
          <div className="columns is-centered"></div>
        </div>
      </header>
      <div>
        <div className="columns is-multiline mt-5">
          <div className="column is-12 has-text-centered">
            <SubmittedApplications />
          </div>
          <div className="column has-text-centered">
            <button onClick={handleStart} className="button is-success">
              START
            </button>
          </div>
          <div className="column has-text-centered">
            <button onClick={handleStop} className="button is-danger">
              STOP
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatusPage;
