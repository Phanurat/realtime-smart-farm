# boot.py - รันตอนบอร์ดเริ่มต้น
from machine import Pin
import network

# LED สำหรับแสดงสถานะ Wi-Fi
led = Pin(2, Pin.OUT)
led.off()  # ปิดตอนเริ่มต้น

# เปิด Wi-Fi interface (ไม่ connect ที่นี่)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("boot.py executed")


print("boot.py executed")

