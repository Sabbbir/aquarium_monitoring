from machine import Pin, SPI
from st7735 import *
from sysfont import sysfont  # Ensure sysfont.py is uploaded to your device

spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))

class TFTDisplay:
    def __init__(self, cs_pin=21, dc_pin=5, reset_pin=19):
        # Initialize TFT display with provided pins
        self.tft = TFT(spi, Pin(dc_pin, Pin.OUT), Pin(reset_pin, Pin.OUT), Pin(cs_pin, Pin.OUT))
        self.tft.initr()  # Initialize for "red tab" variant
        self.tft.rgb(True)  # Set RGB color order
        self.tft.fill(TFT.BLACK)  # Clear screen with black background
        self.tft.rotation(3)  # Rotate the screen (3 = 180 degrees rotation)

    def display(self, position, text, color=TFT.WHITE, font=sysfont, size=1):
        """
        Display text on the TFT screen.

        :param position: Tuple (x, y) for text location
        :param text: String to display
        :param color: Color of the text (default: TFT.WHITE)
        :param font: Font to use (default: sysfont)
        :param size: Font size scaling (default: 1)
        """
        self.tft.text(position, text, color, font, size)

