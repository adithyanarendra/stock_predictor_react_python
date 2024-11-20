import requests
from flask import Flask, jsonify
from model import train_model
from db import get_db_connection
import pandas as pd
import schedule
import time

app = Flask(__name__)

# Alpha Vantage API Key
API_KEY = '9VV82SEKR0JTH02Q'
BASE_URL = 'https://www.alphavantage.co/query'

def fetch_live_data(symbol='TCS.BO'):
    """Fetch live stock data for the given symbol from Alpha Vantage."""
    url = f"{BASE_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if 'Time Series (60min)' not in data:
        return None

    time_series = data['Time Series (60min)']
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df['hour'] = pd.to_datetime(df.index).hour
    df['stock_price'] = df['4. close'].astype(float)
    df = df[['hour', 'stock_price']]
    return df

def save_data_to_db(stock_data):
    """Save stock data to the database."""
    conn = get_db_connection()
    for _, row in stock_data.iterrows():
        query = """
            INSERT INTO stock_data (hour, stock_price) 
            VALUES (%s, %s)
            ON CONFLICT (hour) DO NOTHING
        """
        conn.cursor().execute(query, (row['hour'], row['stock_price']))
    conn.commit()

@app.route('/predict', methods=['GET'])
def predict():
    """Handle stock prediction."""
    symbol = 'TCS.BO'  # Change symbol as needed
    live_data = fetch_live_data(symbol)
    
    if live_data is not None:
        save_data_to_db(live_data)
        model = train_model(live_data)
        prediction = model.predict([[live_data['hour'].max() + 1]])
        return jsonify({"prediction": prediction.tolist()})

    return jsonify({"error": "Failed to fetch live data."})

def job():
    """Job to run every minute to fetch and store live data."""
    symbol = 'TCS.BO'
    live_data = fetch_live_data(symbol)
    if live_data is not None:
        save_data_to_db(live_data)
    else:
        print("Error fetching live data.")

# Schedule the live data fetching to run every minute between 9 AM and 4 PM
schedule.every().day.at("09:00").do(job)
schedule.every().day.at("16:00").do(lambda: schedule.clear())  # Stop after 4 PM

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(60)
