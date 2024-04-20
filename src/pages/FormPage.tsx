// FormPage.tsx
import React, { useState } from "react";
import { v4 } from "uuid";
import { Link, useNavigate } from "react-router-dom";

const FormPage = () => {
  const [skillIds, setSkillIds] = useState<string[]>([]);
  const [jobIds, setJobIds] = useState<any[]>([]);
  const [formData, setFormData] = useState<any | null>(null);
  const [dataRead, setFormRead] = useState<boolean>(false);
  const navigate = useNavigate(); // Hook to access navigate function

  let updateFormData = async () => {
    try {
      // Send the JSON data with the filename
      const response = await window.ipcRenderer.invoke("save-file", {
        buffer: JSON.stringify(formData),
        filename: "/../../user_info_table.json",
        contentType: "application/json",
      });
    } catch (e) {}
  };

  let getFormData = async () => {
    let json = null;
    while (json == null || json.data == "") {
      json = await window.ipcRenderer.invoke("form_data_from_json", {});
    }

    setFormData(JSON.parse(json.data));

    setSkillIds(formData.skills);

    let jobs = [];

    for (const key of Object.keys(formData.job_data)) {
      let obj = formData.job_data[key];

      obj.index = key

      jobs.push(obj);
    }
    setJobIds(jobs);
    setFormRead(true);
  };

  if (!dataRead) getFormData();

  return dataRead ? (
    <div>
      <div className="columns">
        <div className="column is-2"></div>
        <div className="column has-text-centered is-8">
          <header>
            <h1>JOB-GPT</h1>
          </header>
        </div>
        <div className="column has-text-right is-2" style={{ marginTop: 12 }}>
          <button className="button is-light" onClick={() => navigate(-1)}>
            Back
          </button>
        </div>
      </div>
      <form onSubmit={(e) => e.preventDefault()}>
        <div className="columns is-multiline is-vcentered has-text-centered">
          <div className="column is-3" style={{ margin: 10 }}>
            <label>First Name: </label>
            <input
              id="firstName"
              type="text"
              defaultValue={formData.first_name}
              onChange={(e) => {
                formData.first_name = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3">
            <label>Last Name: </label>
            <input
              id="lastName"
              type="text"
              defaultValue={formData.last_name}
              onChange={(e) => {
                formData.last_name = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3">
            <label>Address: </label>
            <input
              id="address"
              type="text"
              defaultValue={formData.address}
              onChange={(e) => {
                formData.address = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3">
            <label>City: </label>
            <input
              id="city"
              type="text"
              defaultValue={formData.city}
              onChange={(e) => {
                formData.city = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3" style={{ margin: 10 }}>
            <label>State</label>
            <input
              id="state"
              type="text"
              defaultValue={formData.state}
              onChange={(e) => {
                formData.state = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3">
            <label>Zipcode</label>
            <input
              id="zipcode"
              type="text"
              defaultValue={formData.zipcode}
              onChange={(e) => {
                formData.zipcode = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3">
            <label>Phone number</label>
            <input
              id="phone"
              type="text"
              defaultValue={formData.phone_number}
              onChange={(e) => {
                formData.phone_number = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3">
            <label>School</label>
            <input
              id="school"
              type="text"
              defaultValue={formData.school}
              onChange={(e) => {
                formData.school = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3" style={{ margin: 10 }}>
            <label>BS/MS</label>
            <input id="degree" type="text" defaultValue={ formData.degree ? formData.degree : ""}
            onChange={(e) => {formData.degree = e.target.value}}></input>
          </div>
          <div className="column is-3">
            <label>Field of Study</label>
            <input
              id="field"
              type="text"
              defaultValue={formData.studying}
              onChange={(e) => {
                formData.studying = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3">
            <label>Start Month</label>
            <input
              id="eduStartMonth"
              type="text"
              value={formData.school_start_month}
              onChange={(e) => {
                formData.school_start_month = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-3">
            <label>Start Year</label>
            <input
              id="eduStartYear"
              type="text"
              value={formData.school_start_year}
              onChange={(e) => {
                formData.school_start_year = e.target.value;
              }}
            ></input>
          </div>
          <div className="column is-half">
            <p>End Month</p>
            <input
              id="eduEndMonth"
              type="text"
              value={formData.school_end_month}
              onChange={(e) => {
                formData.school_end_month = e.target.value;
              }}
            ></input>
          </div>
          <div className="column">
            <p>End Year</p>
            <input
              id="eduEndYear"
              type="text"
              value={formData.school_end_year}
              onChange={(e) => {
                formData.school_end_year = e.target.value;
              }}
            ></input>
          </div>
        </div>
        <hr style={{ backgroundColor: "#454545", borderBottomWidth: 10 }}></hr>
        {jobIds.map((jobId) => {
          return (
            <div key={jobId} id={jobId}>
              <div className="columns is-multiline is-vcentered has-text-centered">
                <div className="column is-3" style={{ margin: 10 }}>
                  <label>Title</label>
                  <input id={`jobTitle${jobId}`} type="text" defaultValue={jobId.position}
                    onChange={(e) => {
                      formData.job_data[jobId.index].position = e.target.value
                      }}>
                        
                      </input>
                </div>
                <div className="column is-3">
                  <label>Company</label>
                  <input id={`jobCompany${jobId}`} type="text" defaultValue={jobId.company}
                    onChange={(e) => {formData.job_data[jobId.index].company = e.target.value}}></input>
                </div>
                <div className="column is-3">
                  <label>Location</label>
                  <input id={`jobLocation${jobId}`} type="text" defaultValue={jobId.location}
                  onChange={(e) => {formData.job_data[jobId.index].location = e.target.value}}></input>
                </div>
                <div className="column is-3">
                  <label>Start Month</label>
                  <input id={`jobStartMonth${jobId}`} type="text" defaultValue={jobId.start_month}
                    onChange={(e) => {formData.job_data[jobId.index].start_month = e.target.value}}></input>
                </div>
                <div className="column is-4" style={{ margin: 5 }}>
                  <p>Start Year</p>
                  <input id={`jobStartYear${jobId}`} type="text" defaultValue={jobId.start_year}
                    onChange={(e) => {formData.job_data[jobId.index].start_year = e.target.value}}></input>
                </div>
                <div className="column is-4">
                  <p>End Month</p>
                  <input id={`jobEndMonth${jobId}`} type="text" defaultValue={jobId.end_month}
                    onChange={(e) => {formData.job_data[jobId.index].end_month = e.target.value}}></input>
                </div>
                <div className="column is-4">
                  <p>End Year</p>
                  <input id={`jobEndYear${jobId}`} type="text" defaultValue={jobId.end_year}
                    onChange={(e) => {formData.job_data[jobId.index].end_year = e.target.value}}></input>
                </div>
                <div className="column is-2"></div>
                <div className="column is-8">
                  <p>Job Description</p>
                  <textarea
                    className="textarea"
                    style={{ backgroundColor: "#454545" }}
                    id={`jobDescription${jobId}`}
                    defaultValue={jobId.description}
                    onChange={(e) => {
                      formData.job_data[jobId.index].description = e.target.value
                    }}
                  ></textarea>
                </div>
              </div>
              <hr
                style={{ backgroundColor: "#454545", borderBottomWidth: 10 }}
              ></hr>
            </div>
          );
        })}
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
                    onChange={(e) => {
                      skillId = e.target.value;
                    }}
                  ></input>
                </div>
              </>
            );
          })}

          <button
            className="column is-12"
            onClick={() => {
              setSkillIds((currentSkillIds) => {
                return [...currentSkillIds, ""];
              });
            }}
          >
            Add Skill
          </button>
          <Link to="/menu" className="column is-full">
            <button
              type="submit"
              onClick={updateFormData}
              className="button is-fullwidth"
            >
              Submit
            </button>
          </Link>
        </div>
      </form>
    </div>
  ) : (
    <div className="columns is-centered">
      Form data is loading from your resume submission ...{" "}
    </div>
  );
};

export default FormPage;
