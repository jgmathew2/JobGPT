import React, { useState } from "react";

const LandingPage: React.FC = () => {
  const [resumeFile, setResumeFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // Access the files with event.target.files
    const file = event.target.files ? event.target.files[0] : null;
    if (file) {
      setResumeFile(file);
    }
  };

  const handleUploadClick = async () => {
    if (resumeFile) {
      try {
        const response = await window.ipcRenderer.invoke("save-file", {
          buffer: await readFileAsArrayBuffer(resumeFile),
          filename: resumeFile.name,
        });
        if (response.success) {
          console.log("File saved successfully:", response.filePath);
          alert(`File saved successfully at ${response.filePath}`);
        } else {
          console.error("Failed to save file:", response.message);
          alert("Failed to save file: " + response.message);
        }
      } catch (error) {
        console.error("Error in IPC call:", error);
        alert("Error in saving file: " + error);
      }
    } else {
      console.log("No file selected.");
      alert("No file selected.");
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
