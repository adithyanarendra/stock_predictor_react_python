import yfinance as yf
import pandas as pd

def fetch_stock_data(stock_symbols):
    """
    Fetch historic stock data using yfinance.
    """
    data = {}
    for symbol in stock_symbols:
        print(f"Fetching data for {symbol}")
        try:
            ticker = f"{symbol}.NS"  # Use NSE suffix for Indian stocks
            stock = yf.Ticker(ticker)
            
            # Fetch historical intraday data for the last 7 days with a 30-minute interval
            df = stock.history(period="max", interval="30m")
            if not df.empty:
                # Ensure consistent column names
                df = df.rename(columns={
                    "Open": "Open",
                    "High": "High",
                    "Low": "Low",
                    "Close": "Close",
                    "Volume": "Volume"
                })
                data[symbol] = df
                print(f"Data fetched for {symbol}: {df.head()}")
            else:
                print(f"No data available for {symbol}")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    return data
