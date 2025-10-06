import requests
import json

# 🔹 URL ของ API (ของคุณเอง)
url = "https://script.googleusercontent.com/macros/echo?user_content_key=AehSKLh6jTWwkliH-qfBeGg_kGbka_GdtkN0GoItxJbA60K5YDL550AtKZKlBA15AFsyCb5AXdo9tDT6o5bVaZiSTRqmfAAsNO7Pvf25jYueA7zHixzL7dlRMUkVUFEY0FngKD2Zmilob66vUWveDee5n0xRNs8cTrifj8d37HYbCN2c07wbQmXRzCNOAABa2mi7RamfF7YgTRnhifKIcc3G2OdEi8qFfsqd0g23tXwoVI3r0x0ePiSAb0a4_7icMn02EqHHpYsVPBD1TM58vOQjJJvD8kkG7CGC_WyNVOBa&lib=MNM0diMGWIKsf2JqaG_sdg6aPRHpjJtzs"

# 🔹 ดึงข้อมูลจาก API
response = requests.get(url)

# 🔹 ตรวจสอบสถานะ
if response.status_code == 200:
    data = response.json()  # แปลงเป็น JSON (list หรือ dict)
    print(json.dumps(data, ensure_ascii=False, indent=2))  # แสดงสวยๆ ภาษาไทยไม่เพี้ยน
else:
    print("เกิดข้อผิดพลาด:", response.status_code)
