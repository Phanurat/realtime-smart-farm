import network
import urequests
import time
from machine import Pin

# ===== CONFIG =====
SSID = 'YOUR_WIFI_SSID'
PASSWORD = 'YOUR_WIFI_PASSWORD'
SERVER_URL = 'https://esp32.yourdomain.com/led-status'  # เปลี่ยนให้ตรงกับ Cloudflare Tunnel
CHECK_INTERVAL = 5
LED_PIN = 2  # GPIO2 คือ LED บนบอร์ด ESP32

# ===== CONNECT WIFI =====
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Connected. IP =', wlan.ifconfig()[0])

# ===== MAIN LOOP =====
def main():
    connect_wifi()
    led = Pin(LED_PIN, Pin.OUT)

    while True:
        try:
            response = urequests.get(SERVER_URL)
            data = response.json()
            status = data.get("status", False)

            print("LED Status:", status)
            led.value(1 if status else 0)

            response.close()
        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL)

# ===== RUN =====
main()
