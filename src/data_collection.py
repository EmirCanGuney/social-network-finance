import yfinance as yf
import pandas as pd
import os


TICKERS = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Brent_Oil": "BZ=F",
    "WTI_Oil": "CL=F",
    "Natural_Gas": "NG=F",

    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow_Jones": "^DJI",

    "DAX": "^GDAXI",
    "FTSE100": "^FTSE",
    "Nikkei225": "^N225",

    "BIST100": "XU100.IS",
    "USD_TRY": "TRY=X",
    "EUR_TRY": "EURTRY=X",

    "Bitcoin": "BTC-USD",

    "VIX": "^VIX",
    "US_10Y_Bond": "^TNX",
    "Dollar_Index": "DX-Y.NYB"
}


START_DATE = "2014-01-01"
END_DATE = "2024-12-31"


def download_price_data():
    os.makedirs("data/raw", exist_ok=True)

    price_data = pd.DataFrame()

    for asset_name, ticker in TICKERS.items():
        print(f"{asset_name} verisi çekiliyor...")

        data = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            progress=False
        )

        if data.empty:
            print(f"Uyarı: {asset_name} için veri gelmedi.")
            continue


        if "Adj Close" in data.columns:
            price_data[asset_name] = data["Adj Close"]
        elif "Close" in data.columns:
            price_data[asset_name] = data["Close"]
        else:
            print(f"Uyarı: {asset_name} için Close/Adj Close bulunamadı.")
            print(data.columns)
            continue

    price_data.to_csv("data/raw/financial_prices_2014_2024.csv")

    print("Veri çekme tamamlandı.")
    print(price_data.head())
    print(price_data.info())

    return price_data


if __name__ == "__main__":
    download_price_data()