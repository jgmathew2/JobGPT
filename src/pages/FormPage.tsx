// FormPage.tsx
import React, {useState} from 'react';
import { v4 } from 'uuid';

const FormPage = () => {


  const [skillIds, setSkillIds] = useState<string[]>([]);
  const [jobIds, setJobIds] = useState<string[]>([]);

  const [formData, setFormData] = useState<any | null>(null);
  const [dataRead, setFormRead] = useState<boolean>(false);


  let getFormData = async () => {
    const json = await window.ipcRenderer.invoke("form_data_from_json", {})
 
    setFormData(JSON.parse(json.data))
    setFormRead(true)

    setSkillIds(formData.skills)

    let jobs = [""]

    for(const key of Object.keys(formData.job_data)) {
      let obj = formData.job_data[key]

      console.log(obj)
    }

    setJobIds(jobs as string[])

    console.log(setJobIds)
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
        <input id="firstName" type="text" value={formData.first_name}></input>
        <label>Last Name: </label>
        <input id="lastName" type="text" value={formData.last_name}></input>
        <label>Address: </label>
        <input id="address" type="text" value={formData.address}></input>
        <label>City: </label>
        <input id="city" type="text" value={formData.city}></input>
        <label>State</label>
        <input id="state" type="text" value={formData.state}></input>
        <label>Zipcode</label>
        <input id="zipcode" type="text" value={formData.zipcode} ></input>
        <label>Phone number</label>
        <input id="phone" type="text" value={formData.phone_number}></input>
        <label>School</label>
        <input id="school" type="text"></input>
        <label>BS/MS</label>
        <input id="degree" type="text" value={formData.studying}></input>
        <label>Field of Study</label>
        <input id="field" type="text"></input>
        <label>Start Month</label>
        <input id="eduStartMonth" type="text" value={formData.school_start_month}></input>
        <label>Start Year</label>
        <input id="eduStartYear" type="text" value={formData.school_start_year}></input>
        <label>End Month</label>
        <input id="eduEndMonth" type="text" value={formData.school_end_month}></input>
        <label>End Year</label>
        <input id="eduEndYear" type="text" value={formData.school_end_year}></input>
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
