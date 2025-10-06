const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const fs = require('fs');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(express.json());

let dataStore = { moisture: 0 };

// ไฟล์ log
const logFile = path.join(__dirname, 'moisture.log');

// รับ POST จาก ESP32
app.post('/update', (req, res) => {
    const data = req.body; // { moisture: 78 }
    dataStore = { ...dataStore, ...data };
    io.emit('updateData', dataStore);

    // เขียน log
    const timestamp = new Date().toISOString();
    const logLine = `${timestamp} - moisture: ${data.moisture}\n`;
    fs.appendFile(logFile, logLine, (err) => {
        if (err) console.error("Error writing log:", err);
    });

    res.json({ status: 'ok' });
});

// Serve client static file
app.use(express.static('../client'));

// Socket.IO connection
io.on('connection', (socket) => {
    console.log('Client connected:', socket.id);
    socket.emit('updateData', dataStore);
});

server.listen(5000, () => {
    console.log('Server running on port 5000');
});
