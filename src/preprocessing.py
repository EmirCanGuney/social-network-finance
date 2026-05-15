import pandas as pd
import os


RAW_DATA_PATH = "data/raw/financial_prices_2014_2024.csv"


def load_price_data():
    df = pd.read_csv(
        RAW_DATA_PATH,
        index_col="Date",
        parse_dates=True
    )

    print("Ham veri yüklendi.")
    print(df.head())

    return df


def calculate_returns(df):
    returns = df.pct_change()

    print("\nGünlük getiriler hesaplandı.")
    print(returns.head())

    return returns


def clean_data(returns):
    print("\nEksik veri sayıları:")
    print(returns.isnull().sum())

    cleaned_returns = returns.dropna()

    print("\nTemizlenmiş veri:")
    print(cleaned_returns.info())

    return cleaned_returns


def save_processed_data(cleaned_returns):
    os.makedirs("data/processed", exist_ok=True)

    cleaned_returns.to_csv(
        "data/processed/returns_2014_2024.csv"
    )

    print("\nİşlenmiş veri kaydedildi.")


def create_period_datasets(cleaned_returns):

    pre_crisis = cleaned_returns.loc["2014":"2019"]
    post_crisis = cleaned_returns.loc["2020":"2024"]

    pre_crisis.to_csv(
        "data/processed/returns_pre_crisis.csv"
    )

    post_crisis.to_csv(
        "data/processed/returns_post_crisis.csv"
    )

    print("\nKriz öncesi ve sonrası datasetleri oluşturuldu.")


if __name__ == "__main__":

    df = load_price_data()

    returns = calculate_returns(df)

    cleaned_returns = clean_data(returns)

    save_processed_data(cleaned_returns)

    create_period_datasets(cleaned_returns)