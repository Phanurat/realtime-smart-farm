const express = require("express");
const cors = require("cors");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json());

let pumps = { pump1: false, pump2: false };

// ESP32 อ่านสถานะ
app.get("/pump-status", (req, res) => {
  res.json(pumps);
});

// เว็บสั่ง toggle
app.post("/toggle", (req, res) => {
  const pumpId = req.query.id;
  if (pumpId && pumps.hasOwnProperty(pumpId)) {
    pumps[pumpId] = !pumps[pumpId];
  }
  res.json(pumps);
});

// serve หน้าเว็บ
app.use(express.static(path.join(__dirname, "public")));

app.listen(3000, () => console.log("✅ Server running on http://localhost:3000"));
