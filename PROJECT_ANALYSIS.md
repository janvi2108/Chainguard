# ChainGuard - Frontend and Backend Analysis

## Project Overview
This is **ChainGuard**, an AI-powered Supply Chain Delay Predictor that uses machine learning to predict shipping delays based on weather conditions, port congestion, and shipping details.

---

## Backend (FastAPI)

**Location**: `backend/app.py`

### Technology Stack
- **Framework**: FastAPI
- **ML Library**: scikit-learn (via joblib)
- **Data Processing**: pandas

### Key Components

#### 1. Model Loading
```
python
model = joblib.load("models/chainguard_delay_model.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")
```
- Loads pre-trained delay prediction model
- Loads feature column configuration for proper input encoding

#### 2. Input Schema (ShipmentInput)
| Field | Type | Description |
|-------|------|-------------|
| weather_risk_score | float | Weather risk assessment (0-1 scale) |
| temp_max | float | Maximum temperature (°C) |
| rainfall | float | Rainfall amount (mm) |
| wind_speed | float | Wind speed (km/h) |
| port_congestion | float | Port congestion level (0-1) |
| shipping_mode | str | Shipping class (First Class, Second Class, Standard Class) |
| nearest_port | str | Destination port |

#### 3. API Endpoint
**POST `/predict`**
- Takes shipment input data
- One-hot encodes categorical variables (shipping_mode, nearest_port)
- Realigns features with training data columns
- Returns prediction with risk level

**Response Format**:
```
json
{
  "delay_probability": 0.356,
  "delay_risk": "LOW"  // or "HIGH" if probability > 0.4
}
```

#### 4. Risk Threshold
- THRESHOLD = 0.4 (40%)
- Risk is "HIGH" if probability > 0.4, otherwise "LOW"

---

## Frontend

**Location**: `frontend/`

### Files Structure

#### 1. index.html
User interface with:
- Title: "ChainGuard - AI-powered Supply Chain Delay Predictor"
- Input fields:
  - Weather Risk Score (number)
  - Max Temperature (°C) (number)
  - Rainfall (mm) (number)
  - Wind Speed (km/h) (number)
  - Port Congestion (0-1) (number)
  - Shipping Mode (dropdown: First Class, Second Class, Standard Class)
  - Nearest Port (dropdown: Port of Los Angeles, Port of Houston, Port of Seattle, Port of New York/New Jersey)
- "Predict Delay Risk" button
- Result display area

#### 2. script.js
JavaScript functionality:
- Collects form input values
- Constructs JSON payload
- Makes POST request to `http://127.0.0.1:8000/predict`
- Displays result in the result div

**API Call**:
```
javascript
const res = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
});
```

#### 3. style.css
Dark-themed UI styling:
- Background: #0f172a (dark blue)
- Container: #020617 (darker blue)
- Font: Inter, Arial, sans-serif
- Accent color: #2563eb (blue)
- Responsive centered layout

---

## Data Flow

```
User Input (Frontend)
       │
       ▼
JSON Payload (script.js)
       │
       ▼
POST /predict (Backend)
       │
       ▼
ML Model Prediction
       │
       ▼
JSON Response {delay_probability, delay_risk}
       │
       ▼
Display Result (Frontend)
```

---

## How to Run

1. **Start Backend**:
   
```
bash
   cd backend
   uvicorn app:app --reload
   
```
   Backend runs at `http://127.0.0.1:8000`

2. **Open Frontend**:
   - Open `frontend/index.html` in a browser
   - Or serve it with a local server:
   
```
bash
   cd frontend
   python -m http.server 8000
   
```

---

## Summary

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend | FastAPI | REST API with ML prediction |
| Frontend | HTML/CSS/JS | User interface for input/output |
| ML Model | scikit-learn | Delay probability prediction |
| Data | pandas | Input preprocessing & encoding |

The frontend collects shipment parameters from the user, sends them to the backend API, which uses a trained ML model to predict the probability of delay, and returns the risk level (HIGH/LOW) to be displayed to the user.
