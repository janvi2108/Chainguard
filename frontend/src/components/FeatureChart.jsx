export default function FeatureImportanceChart({ data }) {
  // Handle empty / null / invalid data
  if (!data || typeof data !== "object") {
    return <p>No feature importance available</p>;
  }

  // Convert object → array
  const entries = Object.entries(data);

  if (entries.length === 0) {
    return <p>No feature importance available</p>;
  }

  return (
    <div className="feature-chart">
      {entries.map(([feature, value]) => (
        <div key={feature} className="feature-row">
          <span className="feature-name">
            {feature.replaceAll("_", " ")}
          </span>

          <div className="bar">
            <div
              className="fill"
              style={{
                width: `${Math.round(value * 100)}%`,
              }}
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
