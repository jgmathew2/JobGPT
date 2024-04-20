import React, { useState } from "react";

const LandingPage: React.FC = () => {
  const [resumeFile, setResumeFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // Access the files with event.target.files
    const file = event.target.files ? event.target.files[0] : null;
    if (file) {
      setResumeFile(file);
      // If you want to automatically upload the file when it's selected,
      // call your upload function here.
    }
  };

  const handleUploadClick = () => {
    if (resumeFile) {
      // Here you would handle the file upload to your server or cloud storage
      console.log("Uploading:", resumeFile);
    } else {
      console.log("No file selected.");
    }
  };

  return (
    <div className="landing-page-container">
      <header className="header">
        <h1>JOB-GPT</h1>
        <p style={{ fontFamily: "Ligconsolata" }}>
          Apply to dozens of jobs, instantly with the click of a button. Just
          upload your resume and Job-GPT will take care of the rest!
        </p>
      </header>
      <main className="upload-container">
        <input
          type="file"
          id="resume-upload"
          onChange={handleFileChange}
          accept=".pdf"
          hidden
        />
        <label
          htmlFor="resume-upload"
          className="upload-button"
          style={{ width: 100, height: 45 }}
        >
          UPLOAD
        </label>
        {resumeFile && <p className="file-info">{resumeFile.name} uploaded</p>}
        <button
          onClick={handleUploadClick}
          className="upload-confirm-button"
          style={{ width: 100, height: 45 }}
        >
          SUBMIT
        </button>
      </main>
    </div>
  );
};

export default LandingPage;
