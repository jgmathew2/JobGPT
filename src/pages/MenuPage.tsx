// MenuPage.tsx
import React from "react";

const MenuPage: React.FC = () => {
  return (
    <div className="menu-page has-text-centered">
      <header className="menu-header">
        <h1>JOB-GPT</h1>
        <p>Choose Application Type:</p>
      </header>
      <div className="columns has-text-centered buttons-container">
        <div className="column">
          <button className="menu-button">WORKDAY</button>
        </div>
        <div className="column">
          <button className="menu-button">GREENHOUSE</button>
        </div>
        <div className="column">
          <button className="menu-button long">LINKEDIN EASY-APPLY</button>
        </div>
      </div>
    </div>
  );
};

export default MenuPage;
