const express = require("express");
const cors = require("cors");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json());

let pumps = { pump1: false, pump2: false };
let temperature = 0;
let moisture = 0;

// ✅ ESP32 อ่านสถานะพร้อมค่า sensor
app.get("/pump-status", (req, res) => {
  res.json({ ...pumps, temperature, moisture });
});

// ✅ เว็บ toggle ปั๊ม
app.post("/toggle", (req, res) => {
  const pumpId = req.query.id;
  if (pumpId && pumps.hasOwnProperty(pumpId)) {
    pumps[pumpId] = !pumps[pumpId];
  }
  res.json({ ...pumps, temperature, moisture });
});

// ✅ ESP32 ส่งค่า sensor มาที่นี่
app.post("/update-sensor", (req, res) => {
  const { temperature: temp, moisture: moist } = req.body;

  if (typeof temp === "number") temperature = temp;
  if (typeof moist === "number") moisture = moist;

  console.log(`📥 Sensor Updated → Temp: ${temp}°C | Moisture: ${moist}%`);
  res.json({ message: "✅ Sensor data updated" });
});

// ✅ หน้าเว็บ dashboard
app.use(express.static(path.join(__dirname, "public")));

app.listen(3000, () => console.log("✅ Server running on http://localhost:3000"));
