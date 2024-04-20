// FormPage.tsx
import React, {useState} from 'react';
import { v4 } from 'uuid';

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

    setSkillIds(formData.skills)

    let jobs = []

    for(const key of Object.keys(formData.job_data)) {
      let obj = formData.job_data[key]

      jobs.push(obj)
    }

    setJobIds(jobs)

  }

  getFormData()

  

  return (

    dataRead ? 

    <div className="form-page">
      <header className="form-header">
        <h1>JOB-GPT</h1>
      </header>
      <form onSubmit={(e) => e.preventDefault()}>
        <label>First Name: </label>
        <input id="firstName" type="text" defaultValue={formData.first_name}></input>
        <label>Last Name: </label>
        <input id="lastName" type="text" defaultValue={formData.last_name}></input>
        <label>Address: </label>
        <input id="address" type="text" defaultValue={formData.address}></input>
        <label>City: </label>
        <input id="city" type="text" defaultValue={formData.city}></input>
        <label>State</label>
        <input id="state" type="text" defaultValue={formData.state}></input>
        <label>Zipcode</label>
        <input id="zipcode" type="text" defaultValue={formData.zipcode} ></input>
        <label>Phone number</label>
        <input id="phone" type="text" defaultValue={formData.phone_number}></input>
        <label>School</label>
        <input id="school" type="text" defaultValue={formData.school}></input>
        <label>BS/MS</label>
        <input id="degree" type="text"></input>
        <label>Field of Study</label>
        <input id="field" type="text" defaultValue={formData.studying}></input>
        <label>Start Month</label>
        <input id="eduStartMonth" type="text" defaultValue={formData.school_start_month}></input>
        <label>Start Year</label>
        <input id="eduStartYear" type="text" defaultValue={formData.school_start_year}></input>
        <label>End Month</label>
        <input id="eduEndMonth" type="text" defaultValue={formData.school_end_month}></input>
        <label>End Year</label>
        <input id="eduEndYear" type="text" defaultValue={formData.school_end_year}></input>
        {jobIds.map((jobId) => {
          return <div key={jobId} id={jobId}>
            <label>Title</label>
            <input id={`jobTitle${jobId}`} defaultValue={jobId.position} type="text"></input>
            <label>Company</label>
            <input id={`jobCompany${jobId}`} defaultValue={jobId.company} type="text"></input>
            <label>Location</label>
            <input id={`jobLocation${jobId}`} defaultValue={jobId.location} type="text"></input> 
            <label>Start Month</label>
            <input id={`jobStartMonth${jobId}`} defaultValue={jobId.start_month} type="text"></input>
            <label>Start Year</label>
            <input id={`jobStartYear${jobId}`} defaultValue={jobId.start_year} type="text"></input>
            <label>End Month</label>
            <input id={`jobEndMonth${jobId}`} defaultValue={jobId.end_month} type="text"></input>
            <label>End Year</label>
            <input id={`jobEndYear${jobId}`} defaultValue={jobId.end_year} type="text"></input>
          </div>;
        })}
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
      </form>
    </div>
    :
    <div>Form data is loading from your resume submission ... </div>
  );
};

export default FormPage;
