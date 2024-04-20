import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate

const WorkDayForm: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [season, setSeason] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate(); // Create navigate function

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
        navigate("/status"); // Redirect to the success page
      } else {
        setMessage(`Failed to save data: ${response.message}`);
      }
    } catch (error) {
      setMessage(`Error in saving data: ${error.message}`);
    }
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
        <button
          className="column is-5 button is-dark is-rounded"
          style={{ marginLeft: 25, marginTop: 10 }}
          type="submit"
        >
          Submit
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
