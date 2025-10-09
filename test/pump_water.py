from machine import Pin
import time

Relay1 = Pin(15, Pin.OUT)
Relay2 = Pin(22, Pin.OUT)

# เริ่มต้นปิดทั้งหมด
Relay1.value(1)
Relay2.value(1)

while True:
    value_open = int(input("เปิดกด 1 / ปิด 0 : "))
    if value_open == 1:
        Relay1.value(0)  # เปิด (Active Low)
        Relay2.value(0)
        print("รีเลย์เปิด")
    elif value_open == 0:
        Relay1.value(1)  # ปิด (Active Low)
        Relay2.value(1)
        print("รีเลย์ปิด")
    else:
        print("กรุณาเลือกใหม่ (0 หรือ 1)")

