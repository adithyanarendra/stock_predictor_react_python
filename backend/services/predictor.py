import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
# from datetime import datetime

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
        
        # Feature engineering: Add daily returns (if needed)
        df["Return"] = df["Close"].pct_change()
        
        # Remove missing values caused by pct_change() and any other NaNs
        df.dropna(inplace=True)

        # Prepare features (X) and target (y)
        X = np.array(range(len(df))).reshape(-1, 1)  # Features: Index as a numeric range
        y = df["Close"].values  # Target: Closing prices
        
        # Train the model
        model = LinearRegression()  # Replace with RandomForestRegressor if needed
        model.fit(X, y)
        models[symbol] = model

        print(f"Model trained for {symbol}. Total data points: {len(df)}")

    return models

# Predict the stock price for the next period
def predict_stock_price(symbol, stock_data, model):
    df = stock_data[symbol]

    if "Close" not in df.columns or len(df) < 30:
        raise ValueError(f"Not enough data for {symbol} to make a prediction.")

    # Use the index as features for prediction
    X = np.array(range(len(df))).reshape(-1, 1)  # Numeric index

    # Predict the price for the next period (extrapolate)
    next_index = len(df)
    predicted_price = model.predict([[next_index]])[0]
    
    # Get the actual price for comparison (last available price)
    actual_price = df["Close"].iloc[-1]
    
    return predicted_price, actual_price

# Calculate the accuracy (Mean Squared Error for now)
def calculate_accuracy(actual_price, predicted_price):
    mse = mean_squared_error([actual_price], [predicted_price])
    return round(mse, 4)  # Return MSE as the "accuracy" for simplicity
