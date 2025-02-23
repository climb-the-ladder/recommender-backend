const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(express.json());
app.use(cors());

const PYTHON_AI_URL = "http://127.0.0.1:5001/predict"; // This is the Python AI model API

app.post("/api/recommend", async (req, res) => {
    try {
        const response = await axios.post(PYTHON_AI_URL, req.body);
        res.json(response.data);
    } catch (error) {
        console.error("Error connecting to AI model:", error);
        res.status(500).json({ error: "AI model error" });
    }
});

app.listen(5000, () => {
    console.log("Backend running on http://127.0.0.1:5000");
});
