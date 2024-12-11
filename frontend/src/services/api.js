import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000";

// Initialize Database
export const initializeDb = async () => {
  const response = await axios.get(`${BASE_URL}/init_db`);
  return response.data;
};

// Train Model
export const trainModel = async () => {
  const response = await axios.get(`${BASE_URL}/train_model`);
  return response.data;
};

// Fetch Predictions
export const getPredictions = async () => {
  const response = await axios.get(`${BASE_URL}/get_prediction`);
  return response.data;
};
