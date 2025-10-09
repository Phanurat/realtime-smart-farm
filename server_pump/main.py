import network
import urequests
import time
from machine import Pin

# ===== CONFIG =====
SSID = "10_2.4G"
PASSWORD = ""  # ใส่รหัสผ่านถ้ามี
SERVER_URL = "https://cause-tokyo-involves-several.trycloudflare.com/pump-status"
CHECK_INTERVAL = 5
RELAY_PIN = 15  # ขารีเลย์ต่อกับ ESP32

# ===== CONNECT WIFI =====
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("🔌 Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1
        print()
    if wlan.isconnected():
        print("✅ Wi-Fi Connected:", wlan.ifconfig()[0])
        return True
    else:
        print("❌ Failed to connect Wi-Fi")
        return False

# ===== MAIN LOOP =====
def main():
    if not connect_wifi():
        return

    relay = Pin(RELAY_PIN, Pin.OUT)
    relay.value(1)  # ปิดไว้ก่อน (Active Low)

    while True:
        try:
            response = urequests.get(SERVER_URL)
            if response.status_code == 200:
                data = response.json()
                status = data.get("pump", False)
                print("🌐 Pump Status:", status)
                relay.value(0 if status else 1)  # Active-Low Relay
            else:
                print("⚠️ HTTP Error:", response.status_code)
            response.close()
        except Exception as e:
            print("❌ Error:", e)

        time.sleep(CHECK_INTERVAL)

# ===== RUN =====
main()
