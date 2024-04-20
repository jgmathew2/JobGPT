import React, { useState } from 'react';

const LinkedInForm: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // Create a JSON object with the email and password
        const jsonData = JSON.stringify({
            email: email,
            password: password
        });
        console.log("Data to be saved as JSON:", jsonData); // Log to verify the content of data

        // Define a filename for the JSON file
        const filename = 'LinkedInForm.json';

        try {
            // Send the JSON data with the filename
            const response = await window.ipcRenderer.invoke("save-file", {
                buffer: jsonData,
                filename: filename,
                contentType: 'application/json'
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
        <header className="form-header">
        <h1>JOB-GPT</h1>
        </header>
        <form onSubmit={handleSubmit}>
        <div>
            <label>LinkedIn Email:</label>
            <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            />
        </div>
        <div>
            <label>LinkedIn Password:</label>
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
    </div>
  );
};

export default LinkedInForm;
