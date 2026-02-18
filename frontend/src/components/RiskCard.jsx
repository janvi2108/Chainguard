export default function RiskCard({ probability, risk }) {
  const percent = Math.round(probability * 100);

  return (
    <div className="card">
      <h2>Delay Risk</h2>

      <div className="progress-bar">
        <div
          className={`progress-fill ${risk.toLowerCase()}`}
          style={{ width: `${percent}%` }}
        />
      </div>

      <p className="risk-text">
        {risk} RISK — {percent}% probability of delay
      </p>
    </div>
  );
}