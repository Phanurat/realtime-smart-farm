import network
import urequests
import time
from machine import Pin, ADC

SSID = "10_2.4G"
PASSWORD = ""
SERVER_URL = "https://cause-tokyo-involves-several.trycloudflare.com/pump-status"
UPDATE_URL = "https://cause-tokyo-involves-several.trycloudflare.com/update-sensor"
CHECK_INTERVAL = 5

# ✅ ขา analog อ่านค่าความชื้น
soil = ADC(Pin(34))
soil.atten(ADC.ATTN_11DB)   # ขยายช่วงอ่านได้ถึง ~3.3V
soil.width(ADC.WIDTH_12BIT) # ความละเอียด 12 บิต (0–4095)

# ✅ ขารีเลย์
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

def read_moisture():
    analog = soil.read()
    moisture = 100 - int((analog / 4095) * 100)
    print(f"Analog: {analog} | ความชื้น: {moisture} %")
    return moisture

def main():
    if not connect_wifi():
        return

    relays = [Pin(pin, Pin.OUT) for pin in RELAY_PINS]
    for r in relays:
        r.value(1 if RELAY_ACTIVE_LOW else 0)

    while True:
        try:
            # อ่านค่า sensor
            moisture = read_moisture()
            temperature = 0  # ไม่มี sensor อุณหภูมิ ใช้ 0 ไว้ก่อน

            # ส่งข้อมูล sensor กลับไป Server
            try:
                urequests.post(UPDATE_URL, json={
                    "temperature": temperature,
                    "moisture": moisture
                })
                print(f"📡 Sent sensor → Temp: {temperature} °C | Moisture: {moisture}%")
            except Exception as e:
                print("⚠️ ส่งค่า sensor ไม่ได้:", e)

            # ดึงสถานะปั๊มจาก server
            response = urequests.get(SERVER_URL)
            if response.status_code == 200:
                data = response.json()
                for i, r in enumerate(relays):
                    status = data.get(f"pump{i+1}", False)
                    r.value(0 if status and RELAY_ACTIVE_LOW else 1)
                print("💧 Pump Status:", data)
            response.close()

        except Exception as e:
            print("❌ Error:", e)
        time.sleep(CHECK_INTERVAL)

main()
