import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function FeatureImportanceChart({ data }) {
  if (!data || data.length === 0) {
    return <p className="muted">No feature importance available</p>;
  }

  const formatted = [...data]
    .sort((a, b) => b.importance - a.importance)
    .slice(0, 8)
    .map((d) => ({
      ...d,
      feature: d.feature.replaceAll("_", " "),
      importance: Number(d.importance.toFixed(3)),
    }));

  return (
    <ResponsiveContainer width="100%" height={320}>
      <BarChart data={formatted} layout="vertical" margin={{ left: 30 }}>
        <XAxis type="number" />
        <YAxis
          type="category"
          dataKey="feature"
          width={220}
          tick={{ fill: "#cbd5f5", fontSize: 13 }}
        />
        <Tooltip
          contentStyle={{
            background: "#020617",
            border: "1px solid #1e293b",
            borderRadius: 8,
          }}
        />
        <Bar
          dataKey="importance"
          fill="#3b82f6"
          radius={[6, 6, 6, 6]}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}
