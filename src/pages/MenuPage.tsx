// MenuPage.tsx
import React from "react";
import { Link } from "react-router-dom"; // Import Link from react-router-dom

const MenuPage: React.FC = () => {
  return (
    <div>
      <div className="columns is-centered">
        <header className="columnn">
          <h1>JOB-GPT</h1>
          <p className="mt-16">Choose Application Type:</p>
        </header>
      </div>
      <div className="columns mt-4 has-text-centered">
        <div className="column">
            <Link to="/workday">
                <button className="button is-primary ">WORKDAY (TECH INTERNSHIPS)</button>
            </Link>
        </div>
        {/* <div className="column">
          <button className="button is-link">GREENHOUSE</button>
        </div> */}
        <div className="column">
            <Link to="/linkedin">
                <button className="button is-info">LINKEDIN EASY-APPLY</button>
            </Link>
        </div>
      </div>
    </div>
  );
};

export default MenuPage;
