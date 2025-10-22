import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-left">
        <h1 className="brand">NCM Dopant Composition Optimizer</h1>
      </div>
      <div className="nav-links">
        <Link to="/">Welcome</Link>
        <Link to="/predict">Predict</Link>
        <Link to="/results">Results</Link>
      </div>
    </nav>
  );
}
