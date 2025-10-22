import React, { useMemo, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid
} from "recharts";
import "../styles.css";

const COLORS = {
  ni: "#4da6ff", // Nickel (blue)
  co: "#00bfa5", // Cobalt (teal)
  mn: "#ff9933", // Manganese (orange)
};

export default function Predict() {
  const [vals, setVals] = useState({ ni: 40, co: 35, mn: 25 });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const nav = useNavigate();

  const total = vals.ni + vals.co + vals.mn;

  const setValue = (key, value) => {
    const v = Number(value);
    if (Number.isNaN(v)) return;
    setVals((p) => ({ ...p, [key]: Math.max(0, Math.min(100, Math.round(v))) }));
  };

  const layers = useMemo(() => {
    const ni = Math.max(0, Math.min(100, vals.ni));
    const co = Math.max(0, Math.min(100, vals.co));
    const mn = Math.max(0, Math.min(100, vals.mn));
    return [
      { key: "mn", color: COLORS.mn, height: mn, bottom: 0 },         // bottom
      { key: "co", color: COLORS.co, height: co, bottom: mn },         // middle
      { key: "ni", color: COLORS.ni, height: ni, bottom: mn + co },    // top
    ];
  }, [vals]);

  const handlePredict = async () => {
    if (Math.abs(total - 100) > 0.01) {
      alert(`Total must be 100%. You entered ${total.toFixed(2)}%`);
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const res = await axios.post("http://127.0.0.1:5000/predict", {
        ni: Number(vals.ni),
        co: Number(vals.co),
        mn: Number(vals.mn),
      });
      setResult(res.data);
    } catch (err) {
      alert(err?.response?.data?.error || "Request failed. Is backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="header">
        <h2>Dopant Composition</h2>
        <p className="subtext">Adjust Nickel (Ni), Cobalt (Co) and Manganese (Mn) percentages. Sum must be 100%.</p>
      </div>

      <div className="layout-row">
        {/* Left - Inputs */}
        <div className="card input-card">
          <h3>Adjust Composition</h3>

          {/* Nickel */}
          <div className="slider-row">
            <label>Nickel (Ni)</label>
            <input type="range" min="0" max="100" value={vals.ni}
              onChange={(e) => setValue("ni", e.target.value)} />
            <div className="range-controls">
              <span className="pill">{vals.ni}%</span>
              <input className="num" type="number" min="0" max="100" value={vals.ni}
                onChange={(e) => setValue("ni", e.target.value)} />
            </div>
          </div>

          {/* Cobalt */}
          <div className="slider-row">
            <label>Cobalt (Co)</label>
            <input type="range" min="0" max="100" value={vals.co}
              onChange={(e) => setValue("co", e.target.value)} />
            <div className="range-controls">
              <span className="pill">{vals.co}%</span>
              <input className="num" type="number" min="0" max="100" value={vals.co}
                onChange={(e) => setValue("co", e.target.value)} />
            </div>
          </div>

          {/* Manganese */}
          <div className="slider-row">
            <label>Manganese (Mn)</label>
            <input type="range" min="0" max="100" value={vals.mn}
              onChange={(e) => setValue("mn", e.target.value)} />
            <div className="range-controls">
              <span className="pill">{vals.mn}%</span>
              <input className="num" type="number" min="0" max="100" value={vals.mn}
                onChange={(e) => setValue("mn", e.target.value)} />
            </div>
          </div>

          <div className="total">Total: <strong>{total}%</strong></div>

          <button className="btn" onClick={handlePredict} disabled={loading}>
            {loading ? "Calculating..." : "Calculate Optimization"}
          </button>
        </div>

        {/* Right - Battery visualization */}
        <div className="card battery-card">
          <div className="battery-visual">
            <div className="battery-body">
              {layers.map((L) => (
                <div
                  key={L.key}
                  className="battery-layer"
                  style={{
                    height: `${L.height}%`,
                    bottom: `${L.bottom}%`,
                    background: `linear-gradient(180deg, ${L.color}, ${shade(L.color, -20)})`,
                  }}
                />
              ))}
            </div>
            <div className="legend">
              <div><span className="legend-dot" style={{background: COLORS.ni}} /> Nickel</div>
              <div><span className="legend-dot" style={{background: COLORS.co}} /> Cobalt</div>
              <div><span className="legend-dot" style={{background: COLORS.mn}} /> Manganese</div>
            </div>
          </div>

          {result && (
  <div className="result-card">
    <h3>ML Prediction Results</h3>
    <div className="accuracy">
  {isNaN(result.accuracy) ? "—" : `${Number(result.accuracy).toFixed(2)}%`}
</div>
    <div className="confidence">
      Model confidence: <strong>{result.confidence}</strong>
    </div>

    {/* 🔹 Baseline Comparison */}
    {result.baseline && (
      <div className="baseline-comparison">
        <h4>Baseline vs Proposed Accuracy</h4>
        <div style={{ width: "100%", height: 250 }}>
          <ResponsiveContainer>
            <BarChart
              data={[
                { name: "Baseline (1:1:1)", Accuracy: result.baseline },
                { name: "Proposed", Accuracy: result.accuracy },
              ]}
              margin={{ top: 20, right: 30, left: 20, bottom: 10 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#555" />
              <XAxis dataKey="name" tick={{ fill: "#fff" }} />
              <YAxis domain={[0, 100]} tick={{ fill: "#fff" }} />
              <Tooltip
                contentStyle={{
                  background: "#222",
                  border: "none",
                  color: "#fff",
                }}
              />
              <Legend />
              <Bar dataKey="Accuracy" fill="#00e5ff" barSize={40} radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <p style={{ marginTop: 10, color: "#ccc" }}>
          Improvement:{" "}
          <strong style={{ color: "#0f6" }}>
            {(result.accuracy - result.baseline).toFixed(2)}%
          </strong>
        </p>
      </div>
    )}
  </div>
)}



        </div>
      </div>

      <div style={{ marginTop: 18 }}>
        <button className="btn ghost" onClick={() => nav("/results")}>See Model Comparison</button>
      </div>
    </div>
  );
}

/* small helper to darken color for gradient stop */
function shade(hex, percent) {
  // hex like "#rrggbb"
  const f = hex.slice(1);
  const r = parseInt(f.slice(0,2),16);
  const g = parseInt(f.slice(2,4),16);
  const b = parseInt(f.slice(4,6),16);
  const t = percent < 0 ? 0 : 255;
  const p = Math.abs(percent)/100;
  const R = Math.round((t - r)*p) + r;
  const G = Math.round((t - g)*p) + g;
  const B = Math.round((t - b)*p) + b;
  return `rgb(${R}, ${G}, ${B})`;
}
