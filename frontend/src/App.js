import React, { useEffect, useState } from "react";
import "./App.css";

import {
  Button,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
} from "@mui/material";
import { initializeDb, trainModel, getPredictions } from "./services/api";

function App() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false); // Loading state for API calls
  const [message, setMessage] = useState(""); // Feedback message for user

  // Fetch predictions on component mount
  useEffect(() => {
    fetchPredictions();
  }, []);

  const fetchPredictions = async () => {
    setLoading(true);
    try {
      const data = await getPredictions();
      setPredictions(data);
    } catch (error) {
      console.error("Error fetching predictions:", error);
      setMessage("Failed to fetch predictions.");
    } finally {
      setLoading(false);
    }
  };

  const handleInitializeDb = async () => {
    setLoading(true);
    try {
      const response = await initializeDb();
      setMessage(response.message); // Display success message
    } catch (error) {
      console.error("Error initializing database:", error);
      setMessage("Failed to initialize database.");
    } finally {
      setLoading(false);
    }
  };

  const handleTrainModel = async () => {
    setLoading(true);
    try {
      const response = await trainModel();
      setMessage(response.message); // Display success message
    } catch (error) {
      console.error("Error training model:", error);
      setMessage("Failed to train the model.");
    } finally {
      setLoading(false);
      fetchPredictions(); // Refresh predictions after training
    }
  };
console.log(predictions);

  return (
    <>
      <Box sx={{ padding: "16px", maxWidth: "800px", margin: "0 auto" }}>
        <Typography variant="h4" align="center" gutterBottom>
          Stock Prediction Dashboard
        </Typography>

        {/* Feedback Message */}
        {message && (
          <Typography
            variant="body1"
            color="primary"
            align="center"
            gutterBottom
          >
            {message}
          </Typography>
        )}

        {/* Buttons for actions */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "16px",
          }}
        >
          <Button
            variant="contained"
            color="primary"
            onClick={handleInitializeDb}
            disabled={loading}
          >
            {loading ? <CircularProgress size={20} /> : "Initialize DB"}
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleTrainModel}
            disabled={loading}
          >
            {loading ? <CircularProgress size={20} /> : "Train Model"}
          </Button>
          <Button
            variant="contained"
            color="success"
            onClick={fetchPredictions}
            disabled={loading}
          >
            {loading ? <CircularProgress size={20} /> : "Refresh Predictions"}
          </Button>
        </Box>

        {/* Predictions List */}
        <Typography variant="h5" gutterBottom>
          Predictions
        </Typography>
        {loading ? (
          <CircularProgress />
        ) : predictions.length > 0 ? (
          <List>
            {predictions.map((prediction, index) => (
              <ListItem key={index} divider>
                <ListItemText
                  primary={`${
                    prediction.stock_symbol
                  } - Predicted: ₹${prediction.predicted_price.toFixed(2)}`}
                  secondary={`Actual: ₹${prediction.actual_price.toFixed(
                    2
                  )} | Accuracy: ${prediction.accuracy}% |  Accuracy: ${
                    prediction.accuracy
                  }% | ${new Date(prediction.timestamp).toLocaleString()}`}
                />
              </ListItem>
            ))}
          </List>
        ) : (
          <Typography>
            No predictions available. Train the model to generate predictions.
          </Typography>
        )}
      </Box>
      {/* <div className="heartContainer">
      <span className="heartHdr">Will you marry me?</span>
      <div className="heartImage">❤️</div>
      <div><button>Yes!</button>
      <button>Yessssssssssssssssss!</button>
      <button>Yessssssssssssssssssasssssssssssssssssssssssssssss!</button>
      </div>
    </div> */}
    </>
  );
}

export default App;
