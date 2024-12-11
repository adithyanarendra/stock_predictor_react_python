import pandas as pd
import requests
from config import ALPHA_VANTAGE_API_KEY

def fetch_stock_data(stock_symbols):
    """
    Fetch historic stock data from Alpha Vantage.
    """
    base_url = "https://www.alphavantage.co/query?"
    data = {}

    for symbol in stock_symbols:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "30min",
            "apikey": ALPHA_VANTAGE_API_KEY,
            # "extended_hours":true,
        }
        response = requests.get(base_url, params=params)

        print(f"Fetching data for {symbol}: Status {response.status_code}")
        if response.status_code == 200:
            time_series = response.json().get("Time Series (30min)", {})

            print(f"Data for {symbol}: {time_series.keys() if time_series else 'No data returned'}") 
            if time_series:
                # Convert the data to a pandas DataFrame
                df = pd.DataFrame.from_dict(time_series, orient="index")
                df = df.rename(columns={
                    "1. open": "Open",
                    "2. high": "High",
                    "3. low": "Low",
                    "4. close": "Close",  # This is the key column for closing prices
                    "5. volume": "Volume"
                })
                df["Close"] = pd.to_numeric(df["Close"], errors='coerce')  # Coerce errors to NaN if conversion fails
                data[symbol] = df
            else:
                print(f"No data available for {symbol}")
        else:
            print(f"Failed to fetch data for {symbol}. Response: {response.text}")

    return data
