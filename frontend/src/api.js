const BASE_URL = "http://127.0.0.1:8000";

/**
 * Call backend to predict delay
 */
export async function predictDelay(payload) {
  const res = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Prediction request failed");
  }

  return res.json();
}

/**
 * Fetch and normalize feature importance
 */
export async function getFeatureImportance() {
  const res = await fetch(`${BASE_URL}/feature-importance`);

  if (!res.ok) {
    throw new Error("Failed to fetch feature importance");
  }

  const data = await res.json();

  // 🔑 BACKEND → FRONTEND SHAPE FIX
  // Backend gives:
  // { features: [...], importance: [...] }
  // Frontend needs:
  // [{ feature: "...", importance: 0.12 }, ...]

  if (Array.isArray(data.features) && Array.isArray(data.importance)) {
    return data.features.map((feature, index) => ({
      feature,
      importance: Number(data.importance[index]),
    }));
  }

  return [];
}
