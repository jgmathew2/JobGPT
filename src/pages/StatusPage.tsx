// StatusPage.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import SubmittedApplications from "@/components/SubmittedApplications";

interface StatusPageProps {
  isLinkedIn: boolean;
}

const StatusPage = (props: StatusPageProps) => {


  const isLinkedIn = props.isLinkedIn; 


  const navigate = useNavigate();

  // Placeholder functions to mimic actions
  const handleStart = () => {

    if(isLinkedIn) {
      window.ipcRenderer.invoke("run_linkedin", {});
    } else {
      window.ipcRenderer.invoke("run_workday", {})
    }
  };

  const handleStop = () => {

    if(isLinkedIn) {
      window.ipcRenderer.invoke("stop_process", {buffer: "linkedin.py"})

    } else {
      window.ipcRenderer.invoke("stop_process", {buffer: "workday.py"})
    }
  }

  const handleBack = () => {
    handleStop();
    navigate(-1); // Navigate back to the previous page
  };

  return (
    <div style={{ placeItems: "normal" }}>
      <div style={{position: 'absolute', top: 10, right: 10}}>
          <button className="button is-light" onClick={handleBack}>
            Back
          </button>
        </div>
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
            <button onClick={handleStart} className="button is-success" style={{width: 100}}>
              START
            </button>
          </div>
          <div className="column has-text-centered">
            <button onClick={handleStop} className="button is-danger" style={{width: 100}}>
              STOP
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatusPage;
