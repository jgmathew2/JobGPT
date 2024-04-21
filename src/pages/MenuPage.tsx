// MenuPage.tsx
import React from "react";
import { Link, useNavigate } from "react-router-dom"; // Import useNavigate along with Link

const MenuPage: React.FC = () => {
  const navigate = useNavigate(); // Hook to access navigate function

  return (
    <div>
      <div style={{position: 'absolute', top: 10, right: 10}}>
          <button className="button is-light" onClick={() => navigate(-1)}>
            BACK
          </button>
        </div>
      <div className="columns is-multiline">
        <div className="column has-text-centered">
          <header>
            <h1>Job-GPT</h1>
            <p className="mt-16">Choose Application Type:</p>
          </header>
        </div>
        
        <div className="column is-full has-text-centered">
          <Link to="/linkedin">
            <button className="button is-info">LINKEDIN EASY-APPLY</button>
          </Link>
        </div>
        <div className="column is-full has-text-centered">
          <Link to="/workday">
            <button className="button is-primary">
              WORKDAY (TECH INTERNSHIPS)
            </button>
          </Link>
        </div>
        
      </div>
    </div>
  );
};

export default MenuPage;
