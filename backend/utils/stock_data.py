import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
from datetime import datetime

# Alpha Vantage API key and endpoint setup
ALPHA_VANTAGE_API_KEY = "TT39LTRJSY61TDPU"
BASE_URL = "https://www.alphavantage.co/query"
TOP_5_STOCKS = ["RELIANCE.BSE", "TCS.BSE", "HDFC.BSE", "INFY.BSE", "ICICIBANK.BSE"]

# PostgreSQL Database connection setup
DB_URI = 'postgresql://postgres:admin@localhost:5432/stockdb'
engine = create_engine(DB_URI)

# Function to fetch live stock data
def fetch_live_data(symbol):
    try:
        url = f"{BASE_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=30min&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "Time Series (30min)" in data:
            times = list(data["Time Series (30min)"].keys())
            latest_time = times[0]
            latest_data = data["Time Series (30min)"][latest_time]
            return {
                "symbol": symbol,
                "time": latest_time,
                "open": float(latest_data["1. open"]),
                "high": float(latest_data["2. high"]),
                "low": float(latest_data["3. low"]),
                "close": float(latest_data["4. close"]),
            }
        else:
            raise Exception("Invalid API response.")
    except Exception as e:
        print(f"Error fetching live data for {symbol}: {e}")
        return None

# Function to store stock data in CSV and PostgreSQL
def store_data_to_csv_and_db(data):
    # Store in CSV
    df = pd.DataFrame([data])
    df.to_csv("backend/data/historic_data.csv", mode="a", header=not os.path.exists("backend/data/historic_data.csv"), index=False)

    # Store in PostgreSQL
    df.to_sql('stock_data', engine, if_exists='append', index=False)
    print("Data saved to CSV and PostgreSQL.")

# Fetch and store data for top 5 stocks
def fetch_and_store_top_5_stocks():
    for symbol in TOP_5_STOCKS:
        data = fetch_live_data(symbol)
        if data:
            store_data_to_csv_and_db(data)

# Function to fetch and store historical data (end-of-day update)
def fetch_historic_data(symbol):
    try:
        url = f"{BASE_URL}?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "Time Series (Daily)" in data:
            df = pd.DataFrame(data["Time Series (Daily)"]).T
            df = df.rename(
                columns={
                    "1. open": "open",
                    "2. high": "high",
                    "3. low": "low",
                    "4. close": "close",
                    "5. adjusted close": "adjusted_close",
                    "6. volume": "volume",
                    "7. dividend amount": "dividend_amount",
                    "8. split coefficient": "split_coefficient",
                }
            )
            df['symbol'] = symbol
            df.to_csv("backend/data/historic_data.csv", mode="a", header=not os.path.exists("backend/data/historic_data.csv"), index=False)
            df.to_sql('historic_data', engine, if_exists='append', index=False)
            print(f"Historical data for {symbol} saved to CSV and PostgreSQL.")
        else:
            print(f"No historical data found for {symbol}")
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")
