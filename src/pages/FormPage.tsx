// FormPage.tsx

import { useState } from "react";
import { v4 } from 'uuid';

const FormPage = () => {
  const [skillIds, setSkillIds] = useState<string[]>([]);
  const [jobIds, setJobIds] = useState<string[]>([]);

  return (
    <div className="form-page">
      <header className="form-header">
        <h1>JOB-GPT</h1>
      </header>
      <form onSubmit={(e) => e.preventDefault()}>
        <label>First Name</label>
        <input id="firstName" type="text"></input>
        <label>Last Name</label>
        <input id="lastName" type="text"></input>
        <label>Address</label>
        <input id="address" type="text"></input>
        <label>City</label>
        <input id="city" type="text"></input>
        <label>State</label>
        <input id="state" type="text"></input>
        <label>Zipcode</label>
        <input id="zipcode" type="text"></input>
        <label>Phone number</label>
        <input id="phone" type="text"></input>
        <label>School</label>
        <input id="school" type="text"></input>
        <label>BS/MS</label>
        <input id="degree" type="text"></input>
        <label>Field of Study</label>
        <input id="field" type="text"></input>
        <label>Start Month</label>
        <input id="eduStartMonth" type="text"></input>
        <label>Start Year</label>
        <input id="eduStartYear" type="text"></input>
        <label>End Month</label>
        <input id="eduEndMonth" type="text"></input>
        <label>End Year</label>
        <input id="eduEndYear" type="text"></input>
        {jobIds.map((jobId) => {
          return <div key={jobId} id={jobId}>
            <>{jobId}</>
            <label>Title</label>
            <input id={`jobTitle${jobId}`} type="text"></input>
            <label>Company</label>
            <input id={`jobCompany${jobId}`} type="text"></input>
            <label>Location</label>
            <input id={`jobLocation${jobId}`} type="text"></input>
            <label>Start Month</label>
            <input id={`jobStartMonth${jobId}`} type="text"></input>
            <label>Start Year</label>
            <input id={`jobStartYear${jobId}`} type="text"></input>
            <label>End Month</label>
            <input id={`jobEndMonth${jobId}`} type="text"></input>
            <label>End Year</label>
            <input id={`jobEndYear${jobId}`} type="text"></input>
          </div>;
        })}
        <button onClick={() => {
          setJobIds(currentJobIds => {
            return [...currentJobIds, v4()];
          })
        }}>Add Job</button>
        {skillIds.map((skillId) => {
          return <><label>Skill {skillId}</label><input key={skillId} id={skillId} type="text"></input></>;
        })}
        <button onClick={() => {
          setSkillIds(currentSkillIds => {
            return [...currentSkillIds, v4()];
          })
        }}>Add Skill</button>
      </form>
    </div>
  );
};

export default FormPage;
