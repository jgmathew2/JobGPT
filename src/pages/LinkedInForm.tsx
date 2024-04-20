import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const LinkedInForm: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [experienceLevel, setExperienceLevel] = useState('');
    const [jobType, setJobType] = useState('');
    const [remote, setRemote] = useState('');
    const [location, setLocation] = useState('');
    const [message, setMessage] = useState('');

    const navigate = useNavigate(); // Create navigate function

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const jsonData = JSON.stringify({
            email: email,
            password: password,
            searchQuery: searchQuery,
            experienceLevel: experienceLevel,
            jobType: jobType,
            remote: remote,
            location: location
        });

        try {
            const response = await window.ipcRenderer.invoke("save-file", {
                buffer: jsonData,
                filename: 'LinkedInForm.json',
                contentType: 'application/json'
            });
            if (response.success) {
                setMessage('Data saved successfully!');
                navigate('/status'); // Redirect to the success page
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
                <div>
                    <label>Search Query:</label>
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>
                <div>
                    <label>Experience Level:</label>
                    <select value={experienceLevel} onChange={(e) => setExperienceLevel(e.target.value)} required>
                        <option value="">Select Experience Level</option>
                        <option value="Internship">Internship</option>
                        <option value="Entry level">Entry level</option>
                        <option value="Associate">Associate</option>
                        <option value="Mid-Senior level">Mid-Senior level</option>
                        <option value="Director">Director</option>
                        <option value="Executive">Executive</option>
                    </select>
                </div>
                <div>
                    <label>Job Type:</label>
                    <select value={jobType} onChange={(e) => setJobType(e.target.value)} required>
                        <option value="">Select Job Type</option>
                        <option value="Full-time">Full-time</option>
                        <option value="Part-time">Part-time</option>
                        <option value="Contract">Contract</option>
                        <option value="Temporary">Temporary</option>
                        <option value="Volunteer">Volunteer</option>
                        <option value="Internship">Internship</option>
                    </select>
                </div>
                <div>
                    <label>Remote:</label>
                    <select value={remote} onChange={(e) => setRemote(e.target.value)} required>
                        <option value="">Select Remote Option</option>
                        <option value="On-site">On-site</option>
                        <option value="Hybrid">Hybrid</option>
                        <option value="Remote">Remote</option>
                    </select>
                </div>
                <div>
                    <label>Location:</label>
                    <input
                        type="text"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                        placeholder="e.g., New York, NY"
                    />
                </div>
                <button type="submit">Submit</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default LinkedInForm;
