import network
import time
from old_tft import *

tft = TFTDisplay()

class WiFiConnect:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)

    def clear_display(self):
        # Clear the display by filling it with black
        tft.tft.fill(TFT.BLACK)

    def connect(self):
        # Display initial status
        self.clear_display()
        tft.display((10, 10), "Searching for WiFi", TFT.BLUE)
        time.sleep(2)  # Wait for 2 seconds to simulate searching
        
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        
        # Display WiFi found message
        self.clear_display()
        tft.display((10, 10), "WiFi Found!", TFT.GREEN)
        time.sleep(1)
        tft.display((10, 25), "Attempting connection...", TFT.GREEN)
        time.sleep(2)  # Simulate short delay
        
        # Attempt connection
        start_time = time.time()
        while not self.wlan.isconnected():
            if time.time() - start_time > 5:  # Timeout after 10 seconds
                self.clear_display()
                tft.display((10, 10), "Failed!", TFT.RED)
                tft.display((10, 25), "Can not connect to WiFi", TFT.YELLOW)
                return False
            time.sleep(1)
        
        # Connection successful
        self.clear_display()
        tft.display((10, 10), "Connected to WiFi!", TFT.GREEN)
        time.sleep(1)  # Display for 1 second
        
        # Show IP address
        self.clear_display()
        ip_address = self.wlan.ifconfig()[0]

        tft.display((10, 10), self.ssid, TFT.GOLD, size=2)
        tft.display((10, 50), f"IP: {ip_address}", TFT.BLUE)
        return True

    def get_ip(self):
        if self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        else:
            self.clear_display()
            tft.display((10, 10), "WiFi not connected", TFT.RED)
            return None
