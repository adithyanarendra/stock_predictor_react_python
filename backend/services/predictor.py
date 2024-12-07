import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from datetime import datetime

# Train the model using 4-5 years of stock data
def train_model(stock_data):
    """
    Train a machine learning model for stock predictions using the fetched stock data.
    """
    models = {}

    for symbol, df in stock_data.items():
        if "Close" not in df.columns:
            print(f"Warning: 'Close' column missing for {symbol}. Skipping model training.")
            continue
        
        # Example: Feature engineering (you can add more features as needed)
        df["Return"] = df["Close"].pct_change()  # Calculate daily returns
        
        # Remove missing values (NaN) caused by pct_change()
        df.dropna(inplace=True)

        # Train a simple model (For simplicity, using a basic linear regression here)
        # You can replace this with a more complex model
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        X = np.array(range(len(df))).reshape(-1, 1)  # Features: Time (index)
        y = df["Close"].values  # Target: Closing price
        
        model.fit(X, y)
        models[symbol] = model
        
    return models

# Predict the stock price for the next period
def predict_stock_price(symbol, stock_data, model):
    df = pd.DataFrame.from_dict(stock_data[symbol], orient="index")
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df["Close"] = pd.to_numeric(df["Close"])

    # Use the last 30 closes to predict the next price
    last_30_days = df['Close'][-30:].values.reshape(1, -1)
    predicted_price = model.predict(last_30_days)[0]
    
    # Get the actual price for comparison (last available price)
    actual_price = df["Close"].iloc[-1]
    
    return predicted_price, actual_price

# Calculate the accuracy (Mean Squared Error for now)
def calculate_accuracy(actual_price, predicted_price):
    mse = mean_squared_error([actual_price], [predicted_price])
    return round(mse, 4)  # Return MSE as the "accuracy" for simplicity
