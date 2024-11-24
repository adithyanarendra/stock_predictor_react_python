from flask import Flask
from utils.stock_data import fetch_and_store_top_5_stocks, fetch_historic_data
import os

app = Flask(__name__)

# Route to fetch live data for top 5 stocks
@app.route('/fetch_live_data')
def fetch_live():
    fetch_and_store_top_5_stocks()
    return "Live data fetched successfully", 200

# Route to fetch historical data (end-of-day update)
@app.route('/fetch_historic_data')
def fetch_historic():
    for symbol in ["RELIANCE.BSE", "TCS.BSE", "HDFC.BSE", "INFY.BSE", "ICICIBANK.BSE"]:
        fetch_historic_data(symbol)
    return "Historical data fetched successfully", 200

if __name__ == '__main__':
    app.run(debug=True)
