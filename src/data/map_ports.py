import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
import os

SHIPMENT_PATH = "data/processed/cleaned_shipments.csv"
PORT_PATH = "data/processed/port_reference.csv"
OUTPUT_PATH = "data/processed/shipments_with_ports.csv"

def map_ports():

    shipments = pd.read_csv(SHIPMENT_PATH)
    ports = pd.read_csv(PORT_PATH)

    geolocator = Nominatim(user_agent="chainguard_ml")

    # Cache to avoid repeated API calls
    city_cache = {}

    def get_coordinates(city, country):
        key = f"{city}, {country}"

        if key in city_cache:
            return city_cache[key]

        try:
            location = geolocator.geocode(key)
            if location:
                coords = (location.latitude, location.longitude)
                city_cache[key] = coords
                time.sleep(1)
                return coords
        except:
            return None

        return None

    mapped_ports = []

    for idx, row in shipments.iterrows():
        coords = get_coordinates(row["Order City"], row["Order Country"])

        if coords:
            min_distance = float("inf")
            nearest_port = None

            for _, port in ports.iterrows():
                port_coords = (port["lat"], port["lon"])
                distance = geodesic(coords, port_coords).km

                if distance < min_distance:
                    min_distance = distance
                    nearest_port = port["port_name"]

            mapped_ports.append(nearest_port)
        else:
            mapped_ports.append("Unknown")

        if idx % 100 == 0:
            print(f"Processed {idx} shipments")

    shipments["nearest_port"] = mapped_ports

    os.makedirs("data/processed", exist_ok=True)
    shipments.to_csv(OUTPUT_PATH, index=False)

    print("Port mapping complete.")
    print("Saved to:", OUTPUT_PATH)

if __name__ == "__main__":
    map_ports()
