from sklearn.linear_model import LinearRegression
import pandas as pd

def train_model(stock_data):
    """Train a simple linear regression model."""
    X = stock_data['hour'].values.reshape(-1, 1)
    y = stock_data['stock_price'].values
    model = LinearRegression()
    model.fit(X, y)
    return model
