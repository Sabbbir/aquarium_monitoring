import utime
from old_tft import *
import urequests
from wifi import WifiConnection

class TimeDisplay:
    def __init__(self, display):
        self.display = display

    def fetch_time(self):
        """
        Fetch the current time in Bangladesh from an online API.
        """
        try:
            response = urequests.get("http://worldtimeapi.org/api/timezone/Asia/Dhaka")
            if response.status_code == 200:
                data = response.json()
                datetime_str = data["datetime"]
                return datetime_str.split("T")[1].split(".")[0]  # Extract HH:MM:SS
            else:
                return "Error: API Fail"
        except Exception as e:
            return "Error: No Time"

    def show_time(self):
        """
        Display the current time in Bangladesh, refreshing every second.
        """
        while True:
            current_time = self.fetch_time()
            self.display.tft.fill(TFT.BLACK)  # Clear the screen
            self.display.display((10, 10), f"Time: {current_time}", color=TFT.WHITE, size=2)
            utime.sleep(1)

# Example usage
if __name__ == "__main__":
    display = TFTDisplay()
    wifi = wifi.WifiConnection("Puzzled", "1111122222", display)
    wifi.connect_to_wifi()

    time_display = TimeDisplay(display)
    time_display.show_time()
