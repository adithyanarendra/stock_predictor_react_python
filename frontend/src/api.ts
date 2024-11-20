export const getStockPrediction = async () => {
    const response = await fetch('http://localhost:5000/predict');
    const data = await response.json();
    return data;
};
