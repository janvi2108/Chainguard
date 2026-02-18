import streamlit as st
import joblib
import pandas as pd

MODEL_PATH = "models/chainguard_delay_model.pkl"
FEATURES_PATH = "models/feature_columns.pkl"
THRESHOLD = 0.4

# Load model and features
model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURES_PATH)

st.set_page_config(page_title="ChainGuard Dashboard", layout="centered")

st.title("ChainGuard – Shipment Delay Risk Dashboard")
st.write("Simulate shipment conditions and predict delay risk.")

st.header("Shipment and Weather Inputs")

weather_risk = st.slider("Weather Risk Score", 0.0, 10.0, 3.0, step=0.1)
temp_max = st.slider("Max Temperature (°C)", 0, 50, 30)
rainfall = st.slider("Rainfall (mm)", 0, 100, 10)
wind_speed = st.slider("Wind Speed (km/h)", 0, 50, 15)
port_congestion = st.slider("Port Congestion (historical)", 0.0, 1.0, 0.5, step=0.01)

shipping_mode = st.selectbox(
    "Shipping Mode",
    ["First Class", "Second Class", "Standard Class"]
)

nearest_port = st.selectbox(
    "Nearest Port",
    [
        "Port of Los Angeles",
        "Port of Houston",
        "Port of Seattle",
        "Port of New York/New Jersey"
    ]
)

if st.button("Predict Delay Risk"):
    input_data = {
        "weather_risk_score": weather_risk,
        "temp_max": temp_max,
        "rainfall": rainfall,
        "wind_speed": wind_speed,
        "port_congestion": port_congestion,
        f"Shipping Mode_{shipping_mode}": 1,
        f"nearest_port_{nearest_port}": 1
    }

    df = pd.DataFrame([input_data])
    df = pd.get_dummies(df)
    df = df.reindex(columns=feature_columns, fill_value=0)

    probability = model.predict_proba(df)[0][1]

    st.subheader("Prediction Result")

    if probability > THRESHOLD:
        st.error(f"High delay risk (probability: {probability:.2%})")
    else:
        st.success(f"Low delay risk (probability: {probability:.2%})")
