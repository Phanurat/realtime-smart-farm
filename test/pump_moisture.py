import network
import urequests
import time
from machine import ADC, Pin

# -----------------------------
# CONFIG
# -----------------------------
SSID = "10_2.4G"
PASSWORD = ""  # ถ้ามีรหัส ให้ใส่ตรงนี้
SERVER_URL = "https://cause-tokyo-involves-several.trycloudflare.com/pump-status"
CHECK_INTERVAL = 5
RELAY_PINS = [15, 22]
RELAY_ACTIVE_LOW = True  # ถ้ารีเลย์ทำงานเมื่อค่าเป็น 0 → True

# -----------------------------
# Soil Moisture Sensor
# -----------------------------
soil = ADC(Pin(34))
soil.atten(ADC.ATTN_11DB)   # อ่านแรงดันได้ถึง ~3.3V
soil.width(ADC.WIDTH_12BIT)

def check_moisture():
    value = soil.read()
    moisture = 100 - int((value / 4095) * 100)
    print("🌱 Soil moisture:", moisture, "%")
    return moisture

# -----------------------------
# Wi-Fi Connect
# -----------------------------
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

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    if not connect_wifi():
        return

    relays = [Pin(pin, Pin.OUT) for pin in RELAY_PINS]

    # ตั้งค่าเริ่มต้นของรีเลย์ให้ปิด
    for r in relays:
        r.value(1 if RELAY_ACTIVE_LOW else 0)

    while True:
        try:
            # อ่านค่าความชื้นทุกครั้งที่วนลูป
            check_moisture()

            # ดึงสถานะปั๊มจากเซิร์ฟเวอร์
            response = urequests.get(SERVER_URL)
            if response.status_code == 200:
                data = response.json()
                for i, r in enumerate(relays):
                    status = data.get(f"pump{i+1}", False)
                    r.value(0 if status and RELAY_ACTIVE_LOW else 1)
                print("🚰 Pump Status:", data)
            response.close()
        except Exception as e:
            print("❌ Error:", e)
        time.sleep(CHECK_INTERVAL)

main()
