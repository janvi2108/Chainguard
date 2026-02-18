from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import numpy as np

# -------------------------
# App initialization
# -------------------------
app = FastAPI(title="ChainGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Paths (absolute-safe)
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "chainguard_delay_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "models", "feature_columns.pkl")

# -------------------------
# Load model once (on startup)
# -------------------------
try:
    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURE_PATH)
except Exception as e:
    model = None
    feature_columns = None
    print("Model loading error:", e)

# -------------------------
# Request schema
# -------------------------
class PredictRequest(BaseModel):
    weather_risk_score: float
    temp_max: float
    rainfall: float
    wind_speed: float
    port_congestion: float
    shipping_mode: str
    nearest_port: str

# -------------------------
# Health check
# -------------------------
@app.get("/")
def root():
    return {"status": "ChainGuard backend running"}

# -------------------------
# Prediction endpoint
# -------------------------
@app.post("/predict")
def predict_delay(data: PredictRequest):
    if model is None or feature_columns is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Build feature vector (match training order)
    input_dict = {
        "weather_risk_score": data.weather_risk_score,
        "temp_max": data.temp_max,
        "rainfall": data.rainfall,
        "wind_speed": data.wind_speed,
        "port_congestion": data.port_congestion,
        f"shipping_mode_{data.shipping_mode}": 1,
        f"nearest_port_{data.nearest_port}": 1,
    }

    # Create aligned feature array
    X = np.zeros(len(feature_columns))
    for i, col in enumerate(feature_columns):
        X[i] = input_dict.get(col, 0)

    prob = model.predict_proba([X])[0][1]

    risk = "LOW"
    if prob > 0.65:
        risk = "HIGH"
    elif prob > 0.4:
        risk = "MEDIUM"

    return {
        "delay_probability": round(float(prob), 3),
        "delay_risk": risk
    }

# -------------------------
# Feature importance endpoint
# -------------------------
@app.get("/feature-importance")
def feature_importance():
    if model is None or feature_columns is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    if not hasattr(model, "feature_importances_"):
        raise HTTPException(
            status_code=500,
            detail="Model does not support feature importance"
        )

    importance = model.feature_importances_

    pairs = list(zip(feature_columns, importance))
    pairs.sort(key=lambda x: x[1], reverse=True)

    top = pairs[:8]

    return {
        "features": [f for f, _ in top],
        "importance": [round(float(i), 4) for _, i in top]
    }
