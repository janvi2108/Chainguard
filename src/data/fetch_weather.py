import pandas as pd
import requests
import os
from datetime import datetime

SHIPMENT_PATH = "data/processed/shipments_with_ports.csv"
PORT_PATH = "data/processed/port_reference.csv"
OUTPUT_PATH = "data/processed/shipments_with_weather.csv"

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


def get_week_start_date(week_str):
    """
    Convert pandas period week (e.g., 2024-01-01/2024-01-07)
    to start_date string format YYYY-MM-DD
    """
    return week_str.split("/")[0]


def fetch_weather_for_port(lat, lon, start_date):
    """
    Fetch daily weather from Open-Meteo for a specific date
    """

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": start_date,
        "daily": "temperature_2m_max,precipitation_sum,windspeed_10m_max",
        "timezone": "auto"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    if "daily" not in data:
        return None

    temp = data["daily"]["temperature_2m_max"][0]
    rain = data["daily"]["precipitation_sum"][0]
    wind = data["daily"]["windspeed_10m_max"][0]

    # Weather Risk Formula (tunable)
    weather_risk_score = (
        rain * 0.5 +
        wind * 0.3 +
        temp * 0.2
    )

    return temp, rain, wind, weather_risk_score


def fetch_weather():

    shipments = pd.read_csv(SHIPMENT_PATH)
    ports = pd.read_csv(PORT_PATH)

    # Unique combinations only
    unique_port_week = shipments[["nearest_port", "week"]].drop_duplicates()

    weather_records = []

    for idx, row in unique_port_week.iterrows():

        port_info = ports[ports["port_name"] == row["nearest_port"]]

        if port_info.empty:
            continue

        lat = port_info.iloc[0]["lat"]
        lon = port_info.iloc[0]["lon"]

        week_start = get_week_start_date(str(row["week"]))

        weather = fetch_weather_for_port(lat, lon, week_start)

        if weather:
            temp, rain, wind, risk = weather

            weather_records.append({
                "nearest_port": row["nearest_port"],
                "week": row["week"],
                "temp_max": temp,
                "rainfall": rain,
                "wind_speed": wind,
                "weather_risk_score": risk
            })

        if idx % 50 == 0:
            print(f"Processed {idx} port-week combinations")

    weather_df = pd.DataFrame(weather_records)

    # Merge back to shipments
    merged = shipments.merge(
        weather_df,
        on=["nearest_port", "week"],
        how="left"
    )

    os.makedirs("data/processed", exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)

    print("Weather integration complete.")
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    fetch_weather()
