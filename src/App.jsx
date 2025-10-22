import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Welcome from "./pages/Welcome";
import Predict from "./pages/Predict";
import Results from "./pages/Results";
import "./styles.css"; // load global CSS once

export default function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  );
}


