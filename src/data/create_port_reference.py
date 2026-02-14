import pandas as pd
import os

OUTPUT_PATH = "data/processed/port_reference.csv"

def create_port_reference():

    ports = [
        {"port_name": "Port of Los Angeles", "lat": 33.7405, "lon": -118.2775},
        {"port_name": "Port of Long Beach", "lat": 33.7701, "lon": -118.1937},
        {"port_name": "Port of New York/New Jersey", "lat": 40.6681, "lon": -74.0451},
        {"port_name": "Port of Savannah", "lat": 32.0809, "lon": -81.0912},
        {"port_name": "Port of Houston", "lat": 29.7604, "lon": -95.3698},
        {"port_name": "Port of Seattle", "lat": 47.6062, "lon": -122.3321}
    ]

    df = pd.DataFrame(ports)

    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print("Port reference created successfully.")
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    create_port_reference()
