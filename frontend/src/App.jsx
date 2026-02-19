import { useState } from "react";
import { predictDelay } from "./api";
import FeatureImportanceChart from "./components/FeatureImportanceChart";
import ErrorBoundary from "./components/ErrorBoundary";
import "./index.css";

export default function App() {
  const [form, setForm] = useState({
    weather_risk_score: 63,
    temp_max: 45,
    rainfall: 10,
    wind_speed: 12,
    port_congestion: 0,
    shipping_mode: "Second Class",
    nearest_port: "Port of Houston",
  });

  const [result, setResult] = useState(null);
  const [features, setFeatures] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const payload = {
        weather_risk_score: Number(form.weather_risk_score),
        temp_max: Number(form.temp_max),
        rainfall: Number(form.rainfall),
        wind_speed: Number(form.wind_speed),
        port_congestion: Number(form.port_congestion),
        shipping_mode: form.shipping_mode,
        nearest_port: form.nearest_port,
      };

      const prediction = await predictDelay(payload);

      setResult(prediction);
      setFeatures(prediction.feature_importance); // ✅ FIX HERE
    } catch (err) {
      console.error("Prediction error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>ChainGuard</h1>
        <p>AI-powered supply chain delay intelligence</p>
      </header>

      {/* Shipment Parameters */}
      <section className="card">
        <h2>Shipment Parameters</h2>

        <div className="grid">
          {Object.keys(form).map((key) =>
            key === "shipping_mode" || key === "nearest_port" ? null : (
              <input
                key={key}
                type="number"
                value={form[key]}
                onChange={(e) =>
                  setForm({ ...form, [key]: e.target.value })
                }
                placeholder={key.replaceAll("_", " ")}
              />
            )
          )}

          <select
            value={form.shipping_mode}
            onChange={(e) =>
              setForm({ ...form, shipping_mode: e.target.value })
            }
          >
            <option>Second Class</option>
            <option>Standard Class</option>
            <option>First Class</option>
            <option>Same Day</option>
          </select>

          <select
            value={form.nearest_port}
            onChange={(e) =>
              setForm({ ...form, nearest_port: e.target.value })
            }
          >
            <option>Port of Houston</option>
            <option>Port of Los Angeles</option>
            <option>Port of Seattle</option>
          </select>
        </div>

        <button onClick={handlePredict} disabled={loading}>
          {loading ? "Analyzing..." : "Predict Delay"}
        </button>
      </section>

      {/* Prediction Result */}
      {result && (
        <section className="card result-card">
          <h2>Prediction</h2>

          <div
            className={`badge ${
              result.delay_risk === "HIGH" ? "high" : "low"
            }`}
          >
            {result.delay_risk} Risk
          </div>

          <div className="confidence">
            <span>Confidence</span>
            <div className="bar">
              <div
                className="fill"
                style={{
                  width: `${Math.round(
                    result.delay_probability * 100
                  )}%`,
                }}
              />
            </div>
            <span>
              {(result.delay_probability * 100).toFixed(1)}%
            </span>
          </div>
        </section>
      )}

      {/* Feature Importance */}
      <section className="card">
        <h2>Feature Importance</h2>
        <ErrorBoundary>
          <FeatureImportanceChart data={features} />
        </ErrorBoundary>
      </section>
    </div>
  );
}
