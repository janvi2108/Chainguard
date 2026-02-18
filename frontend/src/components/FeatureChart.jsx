import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip);

export default function FeatureChart({ data }) {
  if (!data || !data.features || !data.importance) {
    return null;
  }

  const chartData = {
    labels: data.features,
    datasets: [
      {
        label: "Importance",
        data: data.importance,
        backgroundColor: "#2563eb",
        borderRadius: 6,
      },
    ],
  };

  const options = {
    plugins: { legend: { display: false } },
    scales: {
      x: {
        ticks: { color: "#e5e7eb" },
        grid: { color: "#1f2937" },
      },
      y: {
        ticks: { color: "#e5e7eb" },
        grid: { color: "#1f2937" },
      },
    },
  };

  return (
    <div className="card">
      <h2>Why this prediction?</h2>
      <Bar data={chartData} options={options} />
    </div>
  );
}
