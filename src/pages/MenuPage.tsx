// MenuPage.tsx
import React from "react";

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
          <button className="button is-primary ">WORKDAY</button>
        </div>
        <div className="column">
          <button className="button is-link">GREENHOUSE</button>
        </div>
        <div className="column">
          <button className="button is-info">LINKEDIN EASY-APPLY</button>
        </div>
      </div>
    </div>
  );
};

export default MenuPage;
