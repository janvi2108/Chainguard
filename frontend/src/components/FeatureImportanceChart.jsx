export default function FeatureImportanceChart({ data }) {
  // ✅ HARD GUARANTEE: ONLY ARRAY IS ALLOWED
  if (!Array.isArray(data) || data.length === 0) {
    return <p>No feature importance available</p>;
  }

  return (
    <div className="feature-chart">
      {data.map(({ feature, value }) => (
        <div key={feature} className="feature-row">
          <span className="feature-name">
            {feature.replaceAll("_", " ")}
          </span>

          <div className="bar">
            <div
              className="fill"
              style={{ width: `${value * 100}%` }}
            />
          </div>

          <span className="value">
            {(value * 100).toFixed(1)}%
          </span>
        </div>
      ))}
    </div>
  );
}
