import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit
import ta

# Train the model using 4-5 years of stock data
def train_model(stock_data):
    """
    Train machine learning models for stock predictions using the fetched stock data.
    """
    models = {}
    scalers = {}

    for symbol, df in stock_data.items():
        if "Close" not in df.columns:
            print(f"Warning: 'Close' column missing for {symbol}. Skipping model training.")
            continue
        
        # Feature Engineering
        df["Return"] = df["Close"].pct_change()
        df["SMA_5"] = df["Close"].rolling(window=5).mean()
        df["SMA_20"] = df["Close"].rolling(window=20).mean()
        df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
        df["Lag_1"] = df["Close"].shift(1)
        df["Lag_2"] = df["Close"].shift(2)
        df["Lag_3"] = df["Close"].shift(3)

        # Drop rows with NaN after feature creation
        df.dropna(inplace=True)

        # Prepare Features (X) and Target (y)
        features = ["SMA_5", "SMA_20", "RSI", "Lag_1", "Lag_2", "Lag_3"]
        X = df[features].values
        y = df["Close"].values

        # Scale features
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        scalers[symbol] = scaler

        # Split Data for Validation
        tscv = TimeSeriesSplit(n_splits=5)
        best_model = None
        best_mse = float('inf')

        for train_index, test_index in tscv.split(X_scaled):
            X_train, X_test = X_scaled[train_index], X_scaled[test_index]
            y_train, y_test = y[train_index], y[test_index]

            # Train Random Forest Regressor
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            # Validate Model
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            if mse < best_mse:
                best_mse = mse
                best_model = model

        # Save the best model for the symbol
        models[symbol] = best_model
        print(f"Trained model for {symbol}. Best MSE: {best_mse:.4f}")

    return models, scalers

# Predict the stock price for the next period
def predict_stock_price(symbol, stock_data, model, scaler):
    """
    Predict the stock price for the next period using the trained model.
    """
    df = stock_data[symbol]
    
    # Ensure we have enough data and required features
    if len(df) < 30 or "Close" not in df.columns:
        raise ValueError(f"Not enough data for {symbol} to make a prediction.")
    
    # Feature Engineering (similar to training)
    df["Return"] = df["Close"].pct_change()
    df["SMA_5"] = df["Close"].rolling(window=5).mean()
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    df["Lag_1"] = df["Close"].shift(1)
    df["Lag_2"] = df["Close"].shift(2)
    df["Lag_3"] = df["Close"].shift(3)

    # Drop rows with NaN and ensure consistency
    df.dropna(inplace=True)

    # Use the most recent data to predict the next period
    features = ["SMA_5", "SMA_20", "RSI", "Lag_1", "Lag_2", "Lag_3"]
    latest_data = df[features].iloc[-1:].values
    latest_data_scaled = scaler.transform(latest_data)

    # Predict next price
    predicted_price = model.predict(latest_data_scaled)[0]

    # Get the actual price for comparison (last available price)
    actual_price = df["Close"].iloc[-1]

    return predicted_price, actual_price

# Calculate Accuracy (MAPE, RMSE)
def calculate_accuracy(actual_price, predicted_price):
    """
    Calculate accuracy metrics: MAPE and RMSE.
    """
    mse = mean_squared_error([actual_price], [predicted_price])
    mape = mean_absolute_percentage_error([actual_price], [predicted_price])
    rmse = np.sqrt(mse)

    return {"MAPE": round(mape * 100, 2), "RMSE": round(rmse, 2)}