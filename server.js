const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(express.json());
app.use(cors());

const AI_API_URL = "http://127.0.0.1:5001/predict"; // AI API URL

app.post("/api/recommend", async (req, res) => {
    try {
        console.log("Received data from frontend:", req.body); // Debugging

        const response = await axios.post(AI_API_URL, req.body);
        console.log("Received prediction from AI:", response.data); // Debugging

        res.json(response.data);
    } catch (error) {
        console.error("Error connecting to AI model:", error);
        res.status(500).json({ error: "AI model error" });
    }
});

app.listen(5000, () => {
    console.log("Backend running on http://127.0.0.1:5000");
});
