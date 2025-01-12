from machine import Pin, SPI
from st7735 import TFT, TFTColor
import time

# SPI configuration
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))
cs = Pin(15, Pin.OUT)       # Chip Select pin
dc = Pin(2, Pin.OUT)        # Data/Command pin
reset = Pin(4, Pin.OUT)     # Reset pin

# Initialize the TFT display
tft = TFT(spi, dc, reset, cs)
tft.initr()                 # Initialize for "red tab" variant
tft.rgb(True)               # Set RGB color order

# Clear the screen
tft.fill(TFT.BLACK)

# Function to display a single frame
def display_frame(filename):
    with open(filename, "rb") as f:
        buffer = bytearray(128 * 2)  # Buffer for one row (128 pixels × 2 bytes per pixel)
        for y in range(160):         # Loop through each row
            f.readinto(buffer)       # Read one row of image data
            tft.image(0, y, 127, y, buffer)  # Draw the row on the screen

# List of frames (pre-converted RGB565 format files)
frames = [
    "frame0.raw", "frame1.raw", "frame2.raw", "frame3.raw", "frame4.raw", "frame5.raw"
]  # Add more frames as needed

# Display the GIF
while True:
    for frame in frames:
        display_frame(frame)  # Display each frame
        time.sleep(0.1)       # Delay between frames (adjust for speed)
