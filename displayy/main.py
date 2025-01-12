from old_tft import *
import time

# Initialize the TFTDisplay object
# _____________________________
# | Display Pin  | ESP32 Pin  |
# |--------------|------------|
# | LED          | 3.3V       |
# | SCK          | D18        |
# | SDA (MOSI)   | D23        |
# | A0 (DC)      | D5         |
# | Reset        | D19        |
# | CS           | D21        |
# | GND          | GND        |
# | VCC          | 3.3V       |
# |___________________________|

tft_display = TFTDisplay()

# Rotate the display (By default it is 3)
# tft_display.tft.rotation(1)

ts = 2
fs = 1
stt = 20
dist = 15

tft_display.display((10, 10), "Hello, White!", TFT.WHITE, sysfont, ts)
stt+=dist
tft_display.display((10, stt), "Hello, RED!", TFT.RED, sysfont, fs)
stt+=dist

tft_display.display((10, stt), "Hello, GREEN!", TFT.GREEN, sysfont, fs)
stt+=dist

tft_display.display((10, stt), "Hello, BLUE!", TFT.BLUE, sysfont, fs)
stt+=dist

tft_display.display((10, stt), "Hello, YELLOW!", TFT.YELLOW, sysfont, fs)
stt+=dist

tft_display.display((10, stt), "Hello, GRAY!", TFT.GRAY, sysfont, fs)
stt+=dist

tft_display.display((10, stt), "Hello, GOLD!", TFT.GOLD, sysfont, fs)
