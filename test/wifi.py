import network
import urequests as requests
import time

# -----------------------------
# Config
# -----------------------------
SSID = "10_2.4G" 
GOOGLE_SHEET_API_URL = "https://script.google.com/macros/s/AKfycbx12345abcdef/exec"

# -----------------------------
# Connect Wi-Fi
# -----------------------------
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("🔌 Connecting to Wi-Fi...")
        wlan.connect(ssid, password)
        timeout = 0
        while not wlan.isconnected() and timeout < 15:
            print(".", end="")
            time.sleep(1)
            timeout += 1
    
    if wlan.isconnected():
        print("\n✅ Wi-Fi connected!")
        print("IP:", wlan.ifconfig()[0])
    else:
        print("\n❌ Failed to connect Wi-Fi")
    
    return wlan.isconnected()

# -----------------------------
# Fetch JSON from Google Sheet
# -----------------------------
def fetch_google_sheet():
    try:
        response = requests.get(GOOGLE_SHEET_API_URL)
        if response.status_code == 200:
            data = response.json()  # แปลงเป็น JSON
            print("✅ Data from Google Sheet:")
            for item in data:
                print(item)
        else:
            print("⚠️ HTTP Error:", response.status_code)
    except Exception as e:
        print("❌ Request Error:", e)
    finally:
        try:
            response.close()
        except:
            pass

# -----------------------------
# Main
# -----------------------------
if connect_wifi(SSID):
    fetch_google_sheet()

