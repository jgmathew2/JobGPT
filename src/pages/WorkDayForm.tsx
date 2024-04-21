import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const WorkDayForm: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const jsonData = JSON.stringify({
      email: email,
      password: password,
      role: role,
      location: location,
    });

    try {
      const response = await window.ipcRenderer.invoke("save-file", {
        buffer: jsonData,
        filename: "WorkDayForm.json",
        contentType: "application/json",
      });
      if (response.success) {
        // Run Python script after successful data saving
        const pythonResponse = await window.ipcRenderer.invoke('workdayscrape', 'arguments_if_any');
        console.log(pythonResponse); // Log or handle output from your Python script
        setMessage("Data saved successfully! Python script executed.");
        navigate("/statusworkday");
      } else {
        setMessage(`Failed to save data: ${response.message}`);
      }
    } catch (error) {
      setMessage(`Error in saving data: ${error.message}`);
    }
  };

  return (
    <div>
      <div style={{ position: "absolute", top: 10, right: 10 }}>
        <button className="button is-light" onClick={() => navigate(-1)}>
          BACK
        </button>
      </div>
      <div className="form-header has-text-centered" style={{ position: "absolute", top: 10, left: 280 }}>
        <header>
          <h1>Job-GPT</h1>
        </header>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="columns is-multiline" style={{ marginLeft: 10 }}>
          <div className="column is-full">
            <label>Preferred Login Email:</label>
            <input
              style={{ marginLeft: 5 }}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="column is-full">
            <label>Preferred Login Password:</label>
            <input
              style={{ marginLeft: 5 }}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="column is-full">
            <label>Role Query:</label>
            <input
              style={{ marginLeft: 5 }}
              type="text"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              required
            />
          </div>
          <div className="column is-full">
            <label>Location:</label>
            <input
              style={{ marginLeft: 5 }}
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              
            />
          </div>
        </div>
        <button
          className="column is-6 button is-dark is-rounded"
          style={{ margin: 17 }}
          type="submit"
        >
          SUBMIT
        </button>
      </form>
      <div className="columns" style={{ margin: 5 }}>
        <div className="column">{message && <p>{message}</p>}</div>
      </div>
    </div>
  );
};

export default WorkDayForm;
