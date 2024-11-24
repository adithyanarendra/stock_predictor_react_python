import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [stocks, setStocks] = useState([]);

  const fetchStockData = () => {
    axios
      .get("http://localhost:5000/fetch_live_data")
      .then((response) => {
        console.log("Live data fetched:", response);
      })
      .catch((error) => {
        console.error("There was an error fetching the data!", error);
      });
  };

  useEffect(() => {
    fetchStockData();
  }, []);

  return (
    <div className="App">
      <h1>Stock Data Fetcher</h1>
      <button onClick={fetchStockData}>Fetch Live Stock Data</button>
    </div>
  );
}

export default App;
