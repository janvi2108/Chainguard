const API_BASE_URL = "https://chainguard-2.onrender.com";


export async function predictDelay(payload) {
  const res = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    throw new Error("Prediction failed");
  }

  return res.json();
}

export async function getFeatureImportance() {
  const res = await fetch(`${API_BASE_URL}/feature-importance`);

  if (!res.ok) {
    throw new Error("Feature importance fetch failed");
  }

  return res.json();
}
