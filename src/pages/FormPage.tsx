// FormPage.tsx
<<<<<<< HEAD
import React, {useState} from 'react';
import { v4 } from 'uuid';
import { Link } from 'react-router-dom';
=======
import React, { useState } from "react";
import { v4 } from "uuid";
>>>>>>> 4f63574c15be119a221297f6074cff0401143b39

const FormPage = () => {
  const [skillIds, setSkillIds] = useState<string[]>([]);
  const [jobIds, setJobIds] = useState<any[]>([]);

  const [formData, setFormData] = useState<any | null>(null);
  const [dataRead, setFormRead] = useState<boolean>(false);

  let getFormData = async () => {

    let json = null; 
    while(json == null || json.data == "") {
      json = await window.ipcRenderer.invoke("form_data_from_json", {})
    }
 
    setFormData(JSON.parse(json.data))
    setFormRead(true)

    setSkillIds(formData.skills);

    let jobs = []

    for (const key of Object.keys(formData.job_data)) {
      let obj = formData.job_data[key];

      jobs.push(obj)
    }

    setJobIds(jobs)

  }

  getFormData();

  return dataRead ? (
    <div>
      <header className="has-text-centered">
        <h1>JOB-GPT</h1>
      </header>
      <form onSubmit={(e) => e.preventDefault()}>
        <div className="columns is-multiline is-vcentered has-text-centered">
          <div className="column is-3" style={{ margin: 10 }}>
            <label>First Name: </label>
            <input
              id="firstName"
              type="text"
              defaultValue={formData.first_name}
            ></input>
          </div>
          <div className="column is-3">
            <label>Last Name: </label>
            <input id="lastName" type="text" defaultValue={formData.last_name}></input>
          </div>
          <div className="column is-3">
            <label>Address: </label>
            <input id="address" type="text" defaultValue={formData.address}></input>
          </div>
          <div className="column is-3">
            <label>City: </label>
            <input id="city" type="text" defaultValue={formData.city}></input>
          </div>
          <div className="column is-3" style={{ margin: 10 }}>
            <label>State</label>
            <input id="state" type="text" defaultValue={formData.state}></input>
          </div>
          <div className="column is-3">
            <label>Zipcode</label>
            <input id="zipcode" type="text" defaultValue={formData.zipcode}></input>
          </div>
          <div className="column is-3">
            <label>Phone number</label>
            <input id="phone" type="text" defaultValue={formData.phone_number}></input>
          </div>
          <div className="column is-3">
            <label>School</label>
            <input id="school" type="text"></input>
          </div>
          <div className="column is-3" style={{ margin: 10 }}>
            <label>BS/MS</label>
            <input id="degree" type="text"></input>
          </div>
          <div className="column is-3">
            <label>Field of Study</label>
            <input id="field" type="text" defaultValue={formData.studying}></input>
          </div>
          <div className="column is-3">
            <label>Start Month</label>
            <input
              id="eduStartMonth"
              type="text"
              value={formData.school_start_month}
            ></input>
          </div>
          <div className="column is-3">
            <label>Start Year</label>
            <input
              id="eduStartYear"
              type="text"
              value={formData.school_start_year}
            ></input>
          </div>
          <div className="column is-half">
            <p>End Month</p>
            <input
              id="eduEndMonth"
              type="text"
              value={formData.school_end_month}
            ></input>
          </div>
          <div className="column">
            <p>End Year</p>
            <input
              id="eduEndYear"
              type="text"
              value={formData.school_end_year}
            ></input>
          </div>
        </div>
        <hr style={{backgroundColor: '#454545', borderBottomWidth: 10}}></hr>
        {jobIds.map((jobId) => {
          return (
            <div key={jobId} id={jobId}>
              <div className="columns is-multiline is-vcentered has-text-centered">
                <div className="column is-3" style={{ margin: 10 }}>
                  <label>Title</label>
                  <input id={`jobTitle${jobId}`} type="text" defaultValue={jobId.position}></input>
                </div>
                <div className="column is-3">
                  <label>Company</label>
                  <input id={`jobCompany${jobId}`} type="text" defaultValue={jobId.company}></input>
                </div>
                <div className="column is-3">
                  <label>Location</label>
                  <input id={`jobLocation${jobId}`} type="text" defaultValue={jobId.location}></input>
                </div>
                <div className="column is-3">
                  <label>Start Month</label>
                  <input id={`jobStartMonth${jobId}`} type="text" defaultValue={jobId.start_month}></input>
                </div>
                <div className="column is-4" style={{margin: 5}}>
                  <label>Start Year</label>
                  <input id={`jobStartYear${jobId}`} type="text" defaultValue={jobId.start_year}></input>
                </div>
                <div className="column is-4">
                  <p>End Month</p>
                  <input id={`jobEndMonth${jobId}`} type="text" defaultValue={jobId.end_month}></input>
                </div>
                <div className="column is-4"> 
                  <p>End Year</p>
                  <input id={`jobEndYear${jobId}`} type="text" defaultValue={jobId.end_year}></input>
                </div>
              </div>
            </div>
          );
        })}
<<<<<<< HEAD
        <button onClick={() => {
          setJobIds(currentJobIds => {
            return [...currentJobIds, v4()];
          })
        }}>Add Job</button>
        {skillIds.map((skillId) => {
          return <><label>Skill: </label><input key={skillId} id={skillId} value={skillId} type="text"></input></>;
        })}
        <button onClick={() => {
          setSkillIds(currentSkillIds => {
            return [...currentSkillIds, v4()];
          })
        }}>Add Skill</button>
        <Link to="/menu">
          <button type="submit">Submit</button>
        </Link>
=======
        <hr style={{backgroundColor: '#454545', borderBottomWidth: 10}}></hr>
        <div className="columns is-centered">
          <button
            className="column is-12 mt-2"
            onClick={() => {
              setJobIds((currentJobIds) => {
                return [...currentJobIds, v4()];
              });
            }}
          >
            Add Job
          </button>
        </div>
        <div className="columns is-multiline is-vcentered has-text-centered">
          {skillIds.map((skillId) => {
            return (
              <>
                <div className="column is-one-fourth">
                  <label>Skill: </label>
                  <input
                    key={skillId}
                    id={skillId}
                    value={skillId}
                    type="text"
                  ></input>
                </div>
              </>
            );
          })}

          <button
            className="column is-12"
            onClick={() => {
              setSkillIds((currentSkillIds) => {
                return [...currentSkillIds, v4()];
              });
            }}
          >
            Add Skill
          </button>
        </div>
>>>>>>> 4f63574c15be119a221297f6074cff0401143b39
      </form>
    </div>
  ) : (
    <div>Form data is loading from your resume submission ... </div>
  );
};

export default FormPage;
