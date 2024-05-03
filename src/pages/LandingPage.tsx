import React, { useState } from "react";
import { Link } from 'react-router-dom';

const LandingPage: React.FC = () => {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState<boolean>(false); // State to track upload success

  const [API_KEY, setAPIKey] = useState<string | null>(null); 
  const [show_api_inputter, showAPIInputter] = useState<boolean>(false); 

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // Access the files with event.target.files
    const file = event.target.files ? event.target.files[0] : null;
    if (file) {
      setResumeFile(file);
    }
  };

  const handleUploadClick = async () => {
    if (resumeFile && API_KEY) {
      try {
        const response = await window.ipcRenderer.invoke("save-file", {
          buffer: await readFileAsArrayBuffer(resumeFile),
          filename: "resume.pdf",
        });
        if (response.success) {
          console.log("File saved successfully:", response.filePath);
          alert(`File saved successfully at ${response.filePath}`);
          setUploadSuccess(true); // Set upload success state to true
        } else {
          console.error("Failed to save file:", response.message);
          alert("Failed to save file: " + response.message);
        }
      } catch (error) {
        console.error("Error in IPC call:", error);
        alert("Error in saving file: " + error);
      }
      try {
        await window.ipcRenderer.invoke("save-file", {
          buffer: API_KEY,
          filename: "STORED_API_KEY.txt",
        });
        const response = await window.ipcRenderer.invoke("upload_resume", {});
      } catch (error) {
        console.error("Error in resume upload:", error);
        alert("Error in resume to chatgpt: " + error);
      }
    } else {
      if(!resumeFile) {
        console.log("No file selected.");
        alert("No file selected.");
      } else {
        console.log("No API Key entered.");
        alert("No API Key entered.");
      }
    }
  };

  // Helper function to read file as ArrayBuffer
  const readFileAsArrayBuffer = (file: File): Promise<ArrayBuffer> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        if (reader.result instanceof ArrayBuffer) {
          resolve(reader.result);
        } else {
          reject(new Error("Failed to read file as ArrayBuffer"));
        }
      };
      reader.onerror = () => {
        reject(reader.error || new Error("Unknown error while reading file"));
      };
      reader.readAsArrayBuffer(file);
    });
  };

  return (
      <div className="landing-page-container" style={{backgroundImage: 'linear-gradient(to bottom, rgba(0,0,0,1), rgba(135,131,131,1))'}}>
        <div style={{ position: "absolute", top: 10, right: 10 }}>
          <Link to="/form">
            <button className="button is-light">SKIP</button>
          </Link>
        </div>
        <header className="header">
          <h1 style={{fontWeight: 'lighter'}}>Job-GPT</h1>
          <p style={{ fontFamily: "Ligconsolata", margin: 40 }}>
            Apply to dozens of jobs, instantly with the click of a button. Just
            upload your resume and Job-GPT will take care of the rest!
          </p>
        </header>

        <main className="upload-container">
        <div className="columns has-text-centered is-centered">
            <div className="column is-12" style={{marginTop: "-20px"}}>
            <button style={{height: 40, width: 400}} onClick={()=>showAPIInputter(!show_api_inputter)}
              className="upload-confirm-button"
              >           
              ENTER CHATGPT API KEY
            </button>

            
            {show_api_inputter == true ? 
            
            <input
              id="key_inputter"
              type="text"
              style={{width: 300, marginTop: 20}}
              onChange={(e) => setAPIKey(e.target.value)}
            ></input> 
            :
              <></>      
             } 
            </div>
          </div>
          <div className="columns is-vcentered">
            <input
              type="file"
              id="resume-upload"
              onChange={handleFileChange}
              accept=".pdf"
              hidden
            />
            <label
              htmlFor="resume-upload"
              className="column upload-button has-text-centered"
              style={{ width: 100, height: 45 }}
            >
              RESUME FILE UPLOAD
            </label>
            <button
              onClick={handleUploadClick}
              className="column upload-confirm-button"
              style={{ width: 100, height: 45 }}
            >
              SUBMIT
            </button>
          </div>
          {resumeFile && (
            <p className="file-info has-text-centered">
              {resumeFile.name} uploaded
            </p>
          )}
          <div className="columns is-vcentered is-centered mt-4">
            {uploadSuccess && (
              <Link to="/form">
                <button
                  className="column upload-confirm-button"
                  style={{ width: 100, height: 45 }}
                >
                  NEXT
                </button>
              </Link>
            )}

          </div>

        </main>
      </div>
  );
};

export default LandingPage;
