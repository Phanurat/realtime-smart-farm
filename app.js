// server.js
const express = require("express");
const app = express();
const cors = require("cors");
app.use(cors());

let pumpStatus = false;

// ✅ ESP32 อ่านสถานะปั๊ม
app.get("/pump-status", (req, res) => {
  res.json({ pump: pumpStatus });
});

// ✅ เปิด/ปิดปั๊มจากเว็บ
app.get("/toggle-pump", (req, res) => {
  pumpStatus = !pumpStatus;
  res.json({ pump: pumpStatus });
});

app.listen(3000, () => console.log("✅ Server running on port 3000"));
