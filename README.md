# ChainGuard

AI-powered supply chain delay prediction system with explainable machine learning and a modern web dashboard.

ChainGuard predicts shipment delay risk using logistics, weather, and port congestion data.  
The project demonstrates an end-to-end ML workflow: data processing, model training, API deployment, and frontend visualization.

---

## Features

- Shipment delay risk prediction (Low / High)
- Weather and port congestion integration
- Explainable ML using feature importance
- REST API using FastAPI
- Modern dark-mode React dashboard
- End-to-end ML pipeline

---

## Machine Learning Overview

- Model: XGBoost Classifier  
- Problem Type: Binary Classification  
- Dataset Size: ~177,000 cleaned records  
- Accuracy: ~70%

### Important Features
- Shipping Mode
- Nearest Port
- Weather Risk Score
- Wind Speed
- Rainfall
- Maximum Temperature
- Port Congestion Index

Feature importance values are exposed to the frontend for transparency.

---

## Project Structure

```
chainguard-ml/
│
├── backend/
│   ├── app.py
│   ├── __init__.py
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── models/
│   └── chainguard_delay_model.pkl
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   └── index.css
│   └── vite.config.js
│
└── README.md
```

---

## Backend Setup (FastAPI)

### Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Start API Server
```bash
uvicorn backend.app:app --reload
```

API will run at:
```
http://127.0.0.1:8000
```

### API Endpoints
- `POST /predict` – Predict shipment delay
- `GET /feature-importance` – Model explainability data

---

## Frontend Setup (React + Vite)

### Install Dependencies
```bash
cd frontend
npm install
```

### Start Development Server
```bash
npm run dev
```

Frontend will run at:
```
http://localhost:5173
```

---

## Example Prediction Request

```json
{
  "weather_risk_score": 3.5,
  "temp_max": 32,
  "rainfall": 15,
  "wind_speed": 18,
  "port_congestion": 0.62,
  "shipping_mode": "Second Class",
  "nearest_port": "Port of Houston"
}
```

### Example Response

```json
{
  "delay_risk": "Low",
  "message": "Low likelihood of delay"
}
```

---

## Tech Stack

- Backend: Python, FastAPI, XGBoost
- Frontend: React, Vite
- Data Processing: Pandas, NumPy
- Visualization: Recharts
- ML: Scikit-learn, XGBoost

---

## Use Cases

- Supply chain risk assessment
- Logistics planning and optimization
- ML explainability demonstration
- Portfolio and academic projects

---

## License

MIT License

---

## Author

Developed as a full-stack machine learning project demonstrating real-world data pipelines, predictive modeling, and UI integration.
