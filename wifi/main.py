from old_tft import *
from wifi import WiFiConnect 

# Replace with your network credentials
SSID = "Puzzled"
PASSWORD = "1111122222"

# Initialize the display
tft_display = TFTDisplay()
# tft_display.display((10, 10), "Hello Rifat..", TFT.GOLD, size=2)
wifi = WiFiConnect(SSID, PASSWORD)
wifi.connect()