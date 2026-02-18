import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier

# Paths
DATA_PATH = "data/processed/shipments_with_weather.csv"
MODEL_DIR = "models"


def build_and_train():

    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Original shape:", df.shape)

    # -------------------------------
    # Create classification target
    # -------------------------------
    df["delay_flag"] = (df["delay_days"] > 0).astype(int)

    # Drop missing values
    df = df.dropna()

    print("After cleaning:", df.shape)

    # -------------------------------
    # Port congestion feature
    # -------------------------------
    df["port_congestion"] = (
        df.groupby("nearest_port")["delay_flag"]
        .transform("mean")
    )

    # -------------------------------
    # Feature selection
    # -------------------------------
    feature_columns = [
        "weather_risk_score",
        "temp_max",
        "rainfall",
        "wind_speed",
        "port_congestion",
        "Shipping Mode",
        "nearest_port"
    ]

    X = df[feature_columns]
    y = df["delay_flag"]

    # -------------------------------
    # One-hot encoding
    # -------------------------------
    X = pd.get_dummies(
        X,
        columns=["Shipping Mode", "nearest_port"],
        drop_first=True
    )

    # -------------------------------
    # Train-test split
    # -------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # -------------------------------
    # Handle class imbalance
    # -------------------------------
    scale_pos_weight = y_train.value_counts()[0] / y_train.value_counts()[1]

    # -------------------------------
    # Train model
    # -------------------------------
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.08,
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        random_state=42
    )

    print("Training model...")
    model.fit(X_train, y_train)

    # -------------------------------
    # Save model and features
    # -------------------------------
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, f"{MODEL_DIR}/chainguard_delay_model.pkl")
    joblib.dump(X.columns.tolist(), f"{MODEL_DIR}/feature_columns.pkl")

    print("Model saved to models/chainguard_delay_model.pkl")
    print("Feature columns saved to models/feature_columns.pkl")

    # -------------------------------
    # Evaluation (threshold tuned)
    # -------------------------------
    y_probs = model.predict_proba(X_test)[:, 1]
    y_pred = (y_probs > 0.4).astype(int)

    print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    build_and_train()
