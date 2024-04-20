// FormPage.tsx
import React from 'react';

const FormPage: React.FC = () => {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    // Add the logic for what should happen when the form is submitted
  };

  return (
    <div className="form-page">
      <header className="form-header">
        <h1>JOB-GPT</h1>
      </header>
      <form className="job-form" onSubmit={handleSubmit}>
        <div className="form-row">
          <input type="text" placeholder="Field 1" />
          <input type="text" placeholder="Field 2" />
        </div>
        <div className="form-row">
          <input type="text" placeholder="Field 3" />
          <input type="text" placeholder="Field 4" />
        </div>
        <div className="form-row">
          <input type="text" placeholder="Field 5" />
          <input type="text" placeholder="Field 6" />
        </div>
        <div className="form-row">
          <button type="submit" className="submit-button">SUBMIT</button>
        </div>
      </form>
    </div>
  );
};

export default FormPage;
