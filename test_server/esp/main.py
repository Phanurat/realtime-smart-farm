import network
import urequests
import time
from machine import Pin

# ===== CONFIG =====
SSID = "10_2.4G"  # ชื่อ Wi-Fi ที่ต้องการเชื่อมต่อ
SERVER_URL = 'https://hitachi-names-drag-internal.trycloudflare.com/led-status'  # เปลี่ยนให้ตรงกับ Cloudflare Tunnel
CHECK_INTERVAL = 5
LED_PIN = 2  # GPIO2 คือ LED บนบอร์ด ESP32

# ===== CONNECT WIFI =====
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(SSID)  # ไม่มีรหัสผ่าน
        timeout = 10  # Timeout หลังจากพยายาม 10 วินาที
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if wlan.isconnected():
            print('Connected. IP =', wlan.ifconfig()[0])
        else:
            print('Failed to connect to WiFi')
            return False
    return True

# ===== MAIN LOOP =====
def main():
    if not connect_wifi():
        return  # ถ้าไม่สามารถเชื่อมต่อ Wi-Fi ให้หยุดการทำงาน

    led = Pin(LED_PIN, Pin.OUT)

    while True:
        try:
            # ส่งคำขอ GET ไปยัง Cloudflare Tunnel
            response = urequests.get(SERVER_URL)
            if response.status_code == 200:  # ตรวจสอบว่าเชื่อมต่อสำเร็จ
                data = response.json()
                status = data.get("status", False)

                print("LED Status:", status)
                led.value(1 if status else 0)
            else:
                print("Failed to get response. Status code:", response.status_code)

            response.close()
        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL)

# ===== RUN =====
main()

