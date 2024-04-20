// MenuPage.tsx
import React from "react";

const MenuPage: React.FC = () => {
  return (
    <div className="menu-page has-text-centered">
      <header className="menu-header">
        <h1>JOB-GPT</h1>
        <p>Choose Application Type:</p>
      </header>
      <div className="columns is-vcentered is-variable is-multiline is-centered buttons-container">
        <div className="column is-3">
          <button className="menu-button button is-primary">WORKDAY</button>
        </div>
        <div className="column is-3">
          <button className="menu-button button is-link">GREENHOUSE</button>
        </div>
        <div className="column">
          <button className="menu-button long button is-info">LINKEDIN EASY-APPLY</button>
        </div>
      </div>
    </div>
  );
};

export default MenuPage;
