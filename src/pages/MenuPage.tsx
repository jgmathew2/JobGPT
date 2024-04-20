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
      <div className="column is-full has-text-centered">
        <Link to="/linkedin">
          <button className="button is-info">LINKEDIN EASY-APPLY</button>
        </Link>
      </div>
      <div className="column is-full has-text-centered">
        <Link to="/workday">
            <button className="button is-primary ">
                WORKDAY (TECH INTERNSHIPS)
            </button>
        </Link>
      </div>
    </div>
  );
};

export default MenuPage;
