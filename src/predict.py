import joblib
import pandas as pd

MODEL_PATH = "models/chainguard_delay_model.pkl"
FEATURES_PATH = "models/feature_columns.pkl"


def predict_delay(input_data: dict, threshold: float = 0.4):
    """
    Predict delay risk for a single shipment.

    input_data must contain:
    - weather_risk_score
    - temp_max
    - rainfall
    - wind_speed
    - port_congestion
    - one-hot fields like:
        Shipping Mode_<mode>
        nearest_port_<port>
    """

    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURES_PATH)

    df = pd.DataFrame([input_data])

    # One-hot encode and align with training features
    df = pd.get_dummies(df)
    df = df.reindex(columns=feature_columns, fill_value=0)

    probability = model.predict_proba(df)[0][1]
    prediction = int(probability > threshold)

    return {
        "delay_probability": round(probability, 4),
        "delay_prediction": prediction,
        "delay_risk": "HIGH" if prediction == 1 else "LOW"
    }


if __name__ == "__main__":
    # Example test input
    sample_input = {
        "weather_risk_score": 3.5,
        "temp_max": 32,
        "rainfall": 15,
        "wind_speed": 18,
        "port_congestion": 0.62,
        "Shipping Mode_Second Class": 1,
        "nearest_port_Port of Houston": 1
    }

    result = predict_delay(sample_input)
    print(result)
