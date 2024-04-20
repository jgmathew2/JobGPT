import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const WorkDayForm: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [season, setSeason] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const jsonData = JSON.stringify({
      email: email,
      password: password,
      role: role,
      location: location,
      season: season,
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
    <div className="columns is-multiline">
      <header className="column is-full has-text-centered">
        <h1>JOB-GPT</h1>
      </header>
      <form onSubmit={handleSubmit}>
        <div className="column is-full">
          <label style={{ margin: 15 }}>Preferred Login Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="column is-full">
          <label style={{ margin: 15 }}>Preferred Login Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="column is-full">
          <label style={{ margin: 15 }}>Role:</label>
          <input
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            required
          />
        </div>
        <div className="column is-full">
          <label style={{ margin: 15 }}>Location:</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            required
          />
        </div>
        <div className="column is-full">
          <label style={{ margin: 15 }}>Season:</label>
          <select
            value={season}
            onChange={(e) => setSeason(e.target.value)}
            required
          >
            <option value="">Select a season</option>
            <option value="Off Season">Off Season</option>
            <option value="Summer 2024">Summer 2024</option>
          </select>
        </div>
        <button
          className="column is-5 button is-dark is-rounded"
          style={{ marginLeft: 25, marginTop: 10 }}
          type="submit"
        >
          Submit
        </button>
        <button
          className="button is-light"
          type="button"
          onClick={handleBack}
          style={{ marginLeft: 10, marginTop: 10 }}
        >
          Back
        </button>
      </form>
      <div className="columns" style={{ margin: 5 }}>
        <div className="column" style={{ margin: 5 }}>
          {message && <p>{message}</p>}
        </div>
      </div>
    </div>
  );
};

export default WorkDayForm;
