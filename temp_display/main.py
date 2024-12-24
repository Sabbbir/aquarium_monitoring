# main.py

from machine import Pin, SPI
import st7735  # Ensure this file is uploaded to your ESP32
from font5x8 import font as sysfont  # Import the font dictionary
from temp_class import TempSensor
import time

# =========================
# Initialize Display
# =========================

# Initialize SPI interface
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))

# Define pin connections for the display
cs = Pin(5, Pin.OUT)       # Chip Select (CS)
dc = Pin(15, Pin.OUT)      # Data/Command (DC or A0)
rst = Pin(4, Pin.OUT)      # Reset (RST)

# Initialize the display
tft = st7735.TFT(spi, dc, rst, cs)
tft.initr()          # Use initr() for red tab, initb() for blue tab, initg() for green tab
tft.rgb(True)        # Set color mode to RGB (set to False if colors are inverted)
tft.rotation(0)      # Set rotation (0-3)

# Add width and height if not available in tft
if not hasattr(tft, 'width'):
    tft.width = 128   # Replace with your display's width
if not hasattr(tft, 'height'):
    tft.height = 160  # Replace with your display's height

# Turn on the backlight (if connected via GPIO13)
# If your backlight is controlled via GPIO13, uncomment the following lines:
# led = Pin(13, Pin.OUT)
# led.value(1)  # Turn on backlight

# Clear the display with a black background
tft.fill(tft.BLACK)

# =========================
# Initialize Temperature Sensor
# =========================

# Create an instance of the TempSensor class (using GPIO2 for data pin)
temp_sensor = TempSensor(data_pin=2)

# Verify sensor availability
print(f"Sensor available: {temp_sensor.sensor_available}")

# Display initial message
if temp_sensor.sensor_available:
    tft.text((10, 10), "Sensor found", tft.WHITE, sysfont)
else:
    tft.text((10, 10), "No sensors!", tft.WHITE, sysfont)

# =========================
# Main Loop
# =========================

while True:
    temp_c = temp_sensor.read_temperature()
    if temp_c is not None:
        print(f"Temperature: {temp_c:.2f} C")

        # Clear the previous temperature display
        tft.fillrect((10, 30), (tft.width - 20, 20), tft.BLACK)

        # Display the temperature on the TFT display
        temp_text = f"Temp: {temp_c:.2f} C"
        tft.text((10, 30), temp_text, tft.WHITE, sysfont)
    else:
        print("No DS18B20 sensor available.")

        # Display error message on TFT
        tft.fillrect((10, 30), (tft.width - 20, 20), tft.BLACK)
        tft.text((10, 30), "Sensor not available!", tft.WHITE, sysfont)

    time.sleep(1)  # Delay between readings
