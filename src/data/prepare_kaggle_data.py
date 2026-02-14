import pandas as pd
import os

RAW_PATH = "data/raw/DataCoSupplyChainDataset.csv"
OUTPUT_PATH = "data/processed/cleaned_shipments.csv"

def prepare_data():
    print("Loading dataset...")
    df = pd.read_csv(RAW_PATH, encoding="latin1")

    print("Original shape:", df.shape)

    # Convert order date to datetime
    df['order date (DateOrders)'] = pd.to_datetime(
        df['order date (DateOrders)'],
        errors='coerce'
    )

    # Create week feature
    df['week'] = df['order date (DateOrders)'].dt.to_period('W')

    # Create delay target variable
    df['delay_days'] = (
        df['Days for shipping (real)'] -
        df['Days for shipment (scheduled)']
    )

    # Keep only relevant columns
    df = df[[
        'order date (DateOrders)',
        'Order City',
        'Order Country',
        'Shipping Mode',
        'delay_days',
        'week'
    ]]

    # Remove missing values
    df = df.dropna()

    print("Cleaned shape:", df.shape)

    # Save cleaned dataset
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Saved cleaned dataset to:", OUTPUT_PATH)


if __name__ == "__main__":
    prepare_data()

