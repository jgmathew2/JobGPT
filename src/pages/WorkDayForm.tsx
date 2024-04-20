import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const WorkDayForm: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('');
    const [location, setLocation] = useState('');
    const [season, setSeason] = useState('');
    const [message, setMessage] = useState('');

    const navigate = useNavigate(); // Create navigate function

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const jsonData = JSON.stringify({
            email: email,
            password: password,
            role: role,
            location: location,
            season: season
        });

        try {
            const response = await window.ipcRenderer.invoke("save-file", {
                buffer: jsonData,
                filename: 'WorkDayForm.json',
                contentType: 'application/json'
            });
            if (response.success) {
                setMessage('Data saved successfully!');
                navigate('/StatusPage'); // Redirect to the success page
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
                    <label>Preferred Login Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Preferred Login Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Role Query:</label>
                    <input
                        type="text"
                        value={role}
                        onChange={(e) => setRole(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Location Query:</label>
                    <input
                        type="text"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Season:</label>
                    <select
                        value={season}
                        onChange={(e) => setSeason(e.target.value)}
                        required
                    >
                        <option value="">Select Season</option>
                        <option value="Off Season">Off Season</option>
                        <option value="Summer 2024">Summer 2024</option>
                    </select>
                </div>
                <button type="submit">Submit</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default WorkDayForm;
