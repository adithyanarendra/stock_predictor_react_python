from flask import Flask, jsonify
from models.database import init_db, insert_prediction, fetch_accuracy
from services.data_fetcher import fetch_stock_data
from services.predictor import train_model, predict_stock_price, calculate_accuracy
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Stock Prediction API"

@app.route('/init_db', methods=['GET'])
def initialize_database():
    init_db()
    return jsonify({"message": "Database initialized successfully!"})

@app.route('/fetch_accuracy', methods=['GET'])
def get_accuracy():
    accuracy = fetch_accuracy()
    return jsonify(accuracy)

@app.route('/train_model', methods=['GET'])
def train_stock_model():
    stock_symbols = ['HDFCBANK', 'TCS', 'INFY', 'HINDUNILVR', 'RELIANCE.NSE', 'TATAMOTORS', 'RELIANCE.BSE']
    stock_data = fetch_stock_data(stock_symbols)
    
    # Train models and store them in a dictionary
    trained_models = train_model(stock_data)
    
    # Print out the trained models for verification
    for symbol, model in trained_models.items():
        print(f"Trained model for {symbol}: {model}")

    return jsonify({"message": "Model trained successfully!"})

@app.route('/get_prediction', methods=['GET'])
def get_prediction():
    stock_symbols = ['HDFCBANK', 'TCS', 'INFY', 'HINDUNILVR', 'RELIANCE.NSE', 'TATAMOTORS', 'RELIANCE.BSE']
    stock_data = fetch_stock_data(stock_symbols)
    
    # Train models to use for predictions
    trained_models = train_model(stock_data)

    predictions = []
    for symbol in stock_symbols:
        model = trained_models.get(symbol)  # Use the trained model for the symbol
        
        if model is None:
            continue
        
        predicted_price, actual_price = predict_stock_price(symbol, stock_data, model)
        accuracy = calculate_accuracy(actual_price, predicted_price)
        
        timestamp = datetime.now()
        insert_prediction(symbol, timestamp, actual_price, predicted_price, accuracy)
        
        predictions.append({
            "stock_symbol": symbol,
            "timestamp": timestamp,
            "actual_price": actual_price,
            "predicted_price": predicted_price,
            "accuracy": accuracy
        })

    return jsonify(predictions)

if __name__ == "__main__":
    app.run(debug=True)
