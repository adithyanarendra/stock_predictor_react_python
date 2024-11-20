import React, { useState, useEffect } from 'react';
import { getStockPrediction } from './api';

const StockData = () => {
    const [stockData, setStockData] = useState<any>(null);

    useEffect(() => {
        const fetchStockData = async () => {
            const prediction = await getStockPrediction();
            setStockData(prediction);
        };
        fetchStockData();
    }, []);

    return (
        <div>
            {stockData ? (
                <div>
                    <h2>Predicted Next Hour Stock Price: {stockData.prediction}</h2>
                </div>
            ) : (
                <p>Loading prediction...</p>
            )}
        </div>
    );
};

export default StockData;
