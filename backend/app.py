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
    allow_origins=["*"],   # restrict later if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Absolute-safe paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "chainguard_delay_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "models", "feature_columns.pkl")

# -------------------------
# Load model on startup
# -------------------------
try:
    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURE_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    model = None
    feature_columns = None
    print("❌ Model loading error:", e)

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
# Prediction + Feature Importance
# -------------------------
@app.post("/predict")
def predict_delay(data: PredictRequest):
    if model is None or feature_columns is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Build input feature dictionary
    input_dict = {
        "weather_risk_score": data.weather_risk_score,
        "temp_max": data.temp_max,
        "rainfall": data.rainfall,
        "wind_speed": data.wind_speed,
        "port_congestion": data.port_congestion,
        f"shipping_mode_{data.shipping_mode}": 1,
        f"nearest_port_{data.nearest_port}": 1,
    }

    # Align with training feature order
    X = np.zeros(len(feature_columns))
    for i, col in enumerate(feature_columns):
        X[i] = input_dict.get(col, 0)

    # Prediction
    prob = float(model.predict_proba([X])[0][1])

    if prob > 0.65:
        risk = "HIGH"
    elif prob > 0.4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # -------------------------
    # Feature importance
    # -------------------------
    feature_importance = {}

    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
        pairs = list(zip(feature_columns, importance))
        pairs.sort(key=lambda x: x[1], reverse=True)

        for f, v in pairs[:8]:   # top 8 features
            feature_importance[f] = round(float(v), 4)

    return {
        "delay_probability": round(prob, 3),
        "delay_risk": risk,
        "feature_importance": feature_importance
    }
