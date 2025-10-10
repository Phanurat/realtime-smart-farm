import network
import urequests
import time
from machine import Pin

SSID = "10_2.4G"
PASSWORD = ""  # ใส่รหัส Wi-Fi
SERVER_URL = "https://cause-tokyo-involves-several.trycloudflare.com/pump-status"  # เปลี่ยนเป็น IP PC ของคุณ
CHECK_INTERVAL = 5
RELAY_PINS = [15, 22]
RELAY_ACTIVE_LOW = True

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("🔌 Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1
        print()
    if wlan.isconnected():
        print("✅ WiFi Connected:", wlan.ifconfig()[0])
        return True
    else:
        print("❌ Failed to connect WiFi")
        return False

def main():
    if not connect_wifi():
        return

    relays = [Pin(pin, Pin.OUT) for pin in RELAY_PINS]
    for r in relays:
        r.value(1 if RELAY_ACTIVE_LOW else 0)

    while True:
        try:
            response = urequests.get(SERVER_URL)
            if response.status_code == 200:
                data = response.json()
                for i, r in enumerate(relays):
                    status = data.get(f"pump{i+1}", False)
                    r.value(0 if status and RELAY_ACTIVE_LOW else 1)
                print("🌐 Pump Status:", data)
            response.close()
        except Exception as e:
            print("❌ Error:", e)
        time.sleep(CHECK_INTERVAL)

main()

