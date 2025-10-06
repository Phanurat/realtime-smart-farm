import network, urequests
from machine import ADC, Pin
from time import sleep

# -----------------------------
# Config
# -----------------------------
SSID = "10_2.4G"                        # เปลี่ยนเป็น Wi-Fi ของคุณ
SERVER_URL = "http://192.168.1.108:5000/update"  # IP Node.js server

# -----------------------------
# LED
# -----------------------------
led = Pin(2, Pin.OUT)
led.off()

# -----------------------------
# Soil Moisture Sensor
# -----------------------------
soil = ADC(Pin(34))
soil.atten(ADC.ATTN_11DB)

# -----------------------------
# Wi-Fi connect + LED status
# -----------------------------
wlan = network.WLAN(network.STA_IF)

max_retry = 5  # retry connect
for attempt in range(max_retry):
    try:
        print("Connecting Wi-Fi, attempt", attempt+1)
        wlan.connect(SSID)
        timeout = 0
        while not wlan.isconnected() and timeout < 10:
            # LED กระพริบขณะเชื่อมต่อ
            led.on()
            sleep(0.5)
            led.off()
            sleep(0.5)
            timeout += 1
        if wlan.isconnected():
            print("Wi-Fi connected!", wlan.ifconfig())
            led.on()  # LED ติดค้าง
            break
    except OSError as e:
        print("Wi-Fi error:", e)
        sleep(2)

if not wlan.isconnected():
    print("Failed to connect Wi-Fi after", max_retry, "attempts")

# -----------------------------
# Main loop: read sensor & send to server
# -----------------------------
while True:
    if wlan.isconnected():
        value = soil.read()
        moisture = 100 - int((value / 4095) * 100)
        print("Soil moisture:", moisture)

        # ส่งค่าไป server
        try:
            urequests.post(SERVER_URL, json={'moisture': moisture}, headers={"Connection": "close"}).close()
        except Exception as e:
            print("Send error:", e)
    else:
        # Wi-Fi หลุด → LED กระพริบ + reconnect
        print("Wi-Fi disconnected, reconnecting...")
        while not wlan.isconnected():
            try:
                wlan.connect(SSID)
                led.on()
                sleep(0.5)
                led.off()
                sleep(0.5)
            except OSError as e:
                print("Reconnect error:", e)
                sleep(2)
    sleep(5)

