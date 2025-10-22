import React from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid
} from "recharts";

const data = [
  { model: "Linear Regression", R2: 0.92, RMSE: 3.0 },
  { model: "Ridge Regression", R2: 0.92, RMSE: 3.0 },
  { model: "Decision Tree", R2: 0.88, RMSE: 4.4 },
  { model: "Random Forest", R2: 0.90, RMSE: 3.4 },
  { model: "Gradient Boosting", R2: 0.90, RMSE: 3.1 },
  { model: "XGBoost", R2: 0.90, RMSE: 3.4 },
  { model: "SVR", R2: 0.79, RMSE: 5.7 },
  { model: "KNN Regressor", R2: 0.82, RMSE: 5.1 },
];

export default function Results() {
  return (
    <div className="page-container">
      <h2>Model Comparison</h2>
      <p className="subtext">R² and RMSE for tested algorithms on the dataset.</p>

      <div className="chart-row">
        <div className="chart-card">
          <h4>R² Score</h4>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="model" tick={{ fill: "#cfd6e1" }} />
              <YAxis tick={{ fill: "#cfd6e1" }} />
              <Tooltip wrapperStyle={{ color: "#000" }} />
              <Legend />
              <Bar dataKey="R2" fill="#00e6b8" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h4>RMSE</h4>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="model" tick={{ fill: "#cfd6e1" }} />
              <YAxis tick={{ fill: "#cfd6e1" }} />
              <Tooltip wrapperStyle={{ color: "#000" }} />
              <Legend />
              <Bar dataKey="RMSE" fill="#00bfff" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="result-card" style={{ marginTop: 20 }}>
        <h3>Conclusion</h3>
        <p>On the current dataset, Linear / Ridge performed best. Future applications are right on the track. </p>
      </div>
    </div>
  );
}
