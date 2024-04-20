import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

const WorkDayForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Create a text string with the email and password
    const data = `Email: ${email}\nPassword: ${password}\n`;

    try {
      // Convert the data to a buffer
      const buffer = Buffer.from(data, 'utf-8');

      // Send the data as a buffer
      const response = await window.ipcRenderer.invoke("save-file", {
        buffer,
        filename: "credentials.txt",
      });
      if (response.success) {
        setMessage('Data saved successfully!');
      } else {
        setMessage(`Failed to save data: ${response.message}`);
      }
    } catch (error) {
      setMessage(`Error in saving data: ${error.message}`);
    }
  };

  return (
    <div>
      <h2>Login Form</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {message && <p>{message}</p>}
      {/* Add a Link component to navigate to another page */}
      <Link to="/form">
        <button>Go to Form</button>
      </Link>
    </div>
  );
};

export default WorkDayForm;
