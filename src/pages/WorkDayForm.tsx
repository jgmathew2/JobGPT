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
        setMessage("Data saved successfully!");
        navigate("/status");
      } else {
        setMessage(`Failed to save data: ${response.message}`);
      }
    } catch (error) {
      setMessage(`Error in saving data: ${error.message}`);
    }
  };

  const handleBack = () => {
    navigate(-1); // Go back to the previous page
  };

  return (
    <div>
        <div style={{position: 'absolute', top: 10, right: 10}}>
          <button className="button is-light" onClick={() => navigate(-1)}>
            Back
          </button>
        </div>
    <div className="columns is-multiline">
      <div className="column is-full has-text-centered">
        <header>
          <h1>JOB-GPT</h1>
        </header>
      </div>
      <form onSubmit={handleSubmit}>
        <div style={{ margin: 15 }}>
          <div className="column is-full">
            <label>Preferred Login Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="column is-full">
            <label>Preferred Login Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="column is-full">
            <label>Role Query:</label>
            <input
              type="text"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              required
            />
          </div>
          <div className="column is-full">
            <label>Location:</label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g., Chicago, IL"  // Adding placeholder text
              required
            />
          </div>
        </div>
        <div className="column is-5" style={{margin: 12}}>
          <button className="button is-dark is-rounded" type="submit">
            Submit
          </button>
        </div>
      </form>
      <div className="columns" style={{ margin: 5 }}>
        <div className="column">
          {message && <p>{message}</p>}
        </div>
      </div>
    </div>
    </div>
  );
};

export default WorkDayForm;
