import React from "react";
import { useNavigate } from "react-router-dom";

export default function Welcome() {
  const nav = useNavigate();
  return (
    <div className="page-container">
      <h1>NCM Dopant Composition Optimizer</h1>
      <p className="subtext">
        We help you to find the right Nickel–Cobalt–Manganese mix for your Li-ion battery to achieve the best use-case scenarios with the help of our advanced algorithms.
      </p>
      <div style={{ display: "flex", gap: "1rem", marginTop: 20 }}>
        <button className="btn" onClick={() => nav("/predict")}>Start Predicting</button>
        <button className="btn ghost" onClick={() => nav("/results")}>View Results</button>
      </div>
    </div>
  );
}
