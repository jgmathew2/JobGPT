// MenuPage.tsx
import React from 'react';

const MenuPage: React.FC = () => {
  return (
    <div className="menu-page">
      <header className="menu-header">
        <h1>JOB-GPT</h1>
        <p>Choose Application Type:</p>
      </header>
      <div className="buttons-container">
        <button className="menu-button">WORKDAY</button>
        <button className="menu-button">GREENHOUSE</button>
        <button className="menu-button long">LINKEDIN EASY-APPLY</button>
      </div>
    </div>
  );
};

export default MenuPage;
