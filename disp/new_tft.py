from machine import Pin, SPI
from st7735 import TFT
from sysfont import sysfont

class TFTDisplay:
    def __init__(self, spi, cs_pin, dc_pin, reset_pin):
        self.tft = TFT(spi, Pin(dc_pin, Pin.OUT), Pin(reset_pin, Pin.OUT), Pin(cs_pin, Pin.OUT))
        self.tft.initr()  # Initialize for "red tab" variant
        self.tft.rgb(True)  # Set RGB color order
        self.tft.fill(TFT.BLACK)  # Clear screen with black background
        self.y_positions = {}  # Store Y positions for dynamic updates

    def display_title(self, title):
        """
        Display the title on the screen.
        """
        self.tft.fill(TFT.BLACK)  # Clear screen
        self.tft.text((10, 10), title, color=TFT.CYAN, font=sysfont, size=1)
        self.y_positions = {}  # Reset Y positions

    def display_labels(self, sensors):
        """
        Display static labels for the given sensors.
        
        :param sensors: List of sensor names to display.
        """
        for i, sensor in enumerate(sensors):
            y = 30 + i * 15
            self.tft.text((10, y), f"{sensor}:", color=TFT.WHITE, font=sysfont, size=1)
            self.y_positions[sensor] = y

    def update_value(self, sensor_name, value):
        """
        Update the value of a given sensor on the display.
        
        :param sensor_name: The name of the sensor (e.g., "Temp", "TDS").
        :param value: The value to display.
        """
        if sensor_name in self.y_positions:
            y = self.y_positions[sensor_name]
            self.tft.fillrect((70, y), (50, 10), TFT.BLACK)  # Clear previous value
            self.tft.text((70, y), f"{value:.2f}", color=TFT.GREEN, font=sysfont, size=1)
