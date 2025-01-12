from machine import SPI, Pin
from old_tft import *
from temp_class import TempSensor
from tdss import TDSSensor
from st7735 import TFT
import _thread
import time



# Initialize the TFT display
try:
    # Initialize SPI before passing it to TFTDisplay
    tft_display = TFTDisplay(spi, cs_pin=15, dc_pin=21, reset_pin=4)
    tft_display.tft.rotation(3)  # Set rotation after initialization
    print("TFT Display initialized successfully.")
except Exception as e:
    print(f"Error initializing TFT Display: {e}")

# Define a lock for synchronized display updates
display_lock = _thread.allocate_lock()

def display_safe(position, text, color, size=1):
    """
    Safely update the TFT display.
    Ensures no overlapping updates from multiple threads.

    :param position: Tuple (x, y) for text location.
    :param text: Text to display.
    :param color: Color of the text in RGB565.
    :param size: Font size multiplier.
    """
    with display_lock:
        x, y = position
        try:
            tft_display.display((x, y), text, color, size=size)
            print(f"Displayed on TFT: '{text}' at {position} with color {color} and size {size}")
        except Exception as e:
            print(f"Error displaying text on TFT at position {position}: {e}")

def temp_thread(delay_temp):
    """
    Temperature monitoring function to be run in a separate thread.

    :param delay_temp: Delay between readings in milliseconds.
    """
    try:
        data_pin_temp = 2
        sensor = TempSensor(data_pin_temp, delay_temp)
        # Removed sensor.start_continuous_reading() to prevent potential blocking
        print("Temperature monitoring started.")

        while True:
            temp_value = sensor.read_temperature()
            if temp_value is not None:
                temp_text = f"Temp: {temp_value:.2f} C"
                print(f"Temperature: {temp_value} C")
                display_safe((10, 25), temp_text, color=TFT.WHITE, size=1)  # Adjusted y-position
            else:
                print("No temperature data available")
                display_safe((10, 25), "Temp: N/A", color=TFT.RED, size=1)
            time.sleep(delay_temp / 1000)  # Convert delay to seconds
    except Exception as e:
        print(f"Error in temperature thread: {e}")

def tds_thread(delay_tds):
    """
    TDS monitoring function to be run in a separate thread.

    :param delay_tds: Delay between readings in seconds.
    """
    try:
        ADC_PIN = 12
        CALIBRATION_FACTOR = 300.0

        tds_sensor = TDSSensor(
            adc_pin_num=ADC_PIN,
            calibration_factor=CALIBRATION_FACTOR,
            read_interval=delay_tds
        )
        # Removed tds_sensor.start_monitoring() to prevent potential blocking
        print("TDS monitoring started.")

        while True:
            tds_value = tds_sensor.read_tds()
            if tds_value is not None:
                tds_text = f"TDS: {tds_value:.2f} ppm"
                print(f"TDS Value: {tds_value} ppm")
                display_safe((10, 40), tds_text, color=TFT.CYAN, size=1)  # Adjusted y-position
            else:
                print("No TDS sensor found!")
                display_safe((10, 40), "TDS: N/A", color=TFT.RED, size=1)
            time.sleep(delay_tds)
    except Exception as e:
        print(f"Error in TDS thread: {e}")

# Initial display setup before starting threads
try:
    tft_display.tft.fill(TFT.BLACK)  # Clear the screen once at the start
    display_safe((10, 10), "Aquarium Monitoring", color=TFT.CYAN, size=1)  # Title with larger size
    display_safe((10, 25), "Temp: --.- C", color=TFT.WHITE, size=1)
    display_safe((10, 40), "TDS: --.- ppm", color=TFT.CYAN, size=1)
    print("Initial display setup complete.")
except Exception as e:
    print(f"Error during initial display setup: {e}")

# Start threads directly using _thread.start_new_thread
try:
    _thread.start_new_thread(temp_thread, (1000,))  # 1-second delay (1000 ms)
    _thread.start_new_thread(tds_thread, (2,))       # 2-second delay
    print("Threads started successfully.")
except Exception as e:
    print(f"Error starting threads: {e}")

# Keep the main thread alive to allow background threads to run
try:
    while True:
        time.sleep(1)  # Sleep to reduce CPU usage
except KeyboardInterrupt:
    print("Program terminated by user.")
