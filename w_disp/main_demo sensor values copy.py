from machine import SPI, Pin, ADC
from old_tft import TFTDisplay, spi  # Import the TFTDisplay class directly
from temp_class import TempSensor
from tdss import TDSSensor
from tbd import TBD
from salinity import Salinity
from st7735 import TFT
import time
import _thread

# Initialize the SPI bus (Assuming 'spi' is already defined in old_tft)
# If not, initialize it here accordingly.

# Initialize the TFT display
try:
    tft_display = TFTDisplay(spi, cs_pin=15, dc_pin=21, reset_pin=4)
    tft_display.tft.rotation(3)
    print("TFT Display initialized successfully.")
except Exception as e:
    print(f"Error initializing TFT Display: {e}")

# Initial display setup
try:
    tft_display.display((10, 10), "Aquarium Monitoring", color=TFT.YELLOW)
    tft_display.display((10, 35), "Temp: --.- C", color=TFT.WHITE)
    tft_display.display((10, 50), "TDS: --.- ppm", color=TFT.CYAN)
    tft_display.display((10, 65), "Turbidity: --.- NTU", color=TFT.GREEN)
    tft_display.display((10, 80), "Salinity: --.- PSU", color=TFT.RED)
    print("Initial display setup complete.")
except Exception as e:
    print(f"Error during initial display setup: {e}")

# Shared sensor data
sensor_data = {
    "temperature": "Temp: --.- C",
    "tds": "TDS: --.- ppm",
    "turbidity": "Turbidity: --.- NTU",
    "salinity": "Salinity: --.- PSU"
}

# Locks for synchronization
data_lock = _thread.allocate_lock()
display_lock = _thread.allocate_lock()

def display_safe(position, text, color):
    """
    Safely update the TFT display.
    Ensures no overlapping updates from multiple threads.

    :param position: Tuple (x, y) for text location.
    :param text: Text to display.
    :param color: Color of the text in RGB565.
    """
    with display_lock:
        try:
            tft_display.display(position, text, color)
            print(f"Displayed on TFT: '{text}' at {position} with color {color}")
        except Exception as e:
            print(f"Error in display_safe: {e}")

def temp_thread(delay_temp):
    """
    Temperature monitoring function to be run in a separate thread.

    :param delay_temp: Delay between readings in milliseconds.
    """
    try:
        data_pin_temp = 2
        sensor = TempSensor(data_pin=data_pin_temp, delay=delay_temp)
        sensor.start_continuous_reading()
        print("Temperature sensor continuous reading started.")

        while True:
            temp_value = sensor.read_temperature()
            with data_lock:
                if temp_value is not None:
                    sensor_data["temperature"] = f"Temp: {temp_value:.2f} C"
                    print(f"Temperature updated to: {sensor_data['temperature']}")
                else:
                    sensor_data["temperature"] = "Temp: N/A"
                    print("Temperature data not available.")
            time.sleep(delay_temp / 1000)  # Convert delay to seconds
    except Exception as e:
        print(f"Error in temperature thread: {e}")

def tds_thread_func(delay_tds):
    """
    TDS monitoring function to be run in a separate thread.

    :param delay_tds: Delay between readings in seconds.
    """
    try:
        ADC_PIN = 12  # GPIO12 (D12)
        CALIBRATION_FACTOR = 300.0
        tds_sensor = TDSSensor(adc_pin_num=ADC_PIN, calibration_factor=CALIBRATION_FACTOR, read_interval=delay_tds)
        tds_sensor.start_monitoring()
        print("TDS sensor continuous monitoring started.")

        while True:
            tds_value = tds_sensor.read_tds()
            with data_lock:
                if tds_value is not None:
                    sensor_data["tds"] = f"TDS: {tds_value:.2f} ppm"
                    print(f"TDS updated to: {sensor_data['tds']}")
                else:
                    sensor_data["tds"] = "TDS: N/A"
                    print("TDS data not available.")
            time.sleep(delay_tds)
    except Exception as e:
        print(f"Error in TDS thread: {e}")

def turbidity_thread_func(delay_turbidity):
    """
    Turbidity monitoring function to be run in a separate thread.

    :param delay_turbidity: Delay between readings in seconds.
    """
    try:
        turbidity_sensor = TBD(delay=delay_turbidity, calibration_a=100, calibration_b=-100)
        turbidity_sensor.start_continuous_reading()
        print("Turbidity sensor continuous reading started.")

        while True:
            turbidity_value = turbidity_sensor.read_turbidity()
            with data_lock:
                if turbidity_value is not None:
                    sensor_data["turbidity"] = f"Turbidity: {turbidity_value:.2f} NTU"
                    print(f"Turbidity updated to: {sensor_data['turbidity']}")
                else:
                    sensor_data["turbidity"] = "Turbidity: N/A"
                    print("Turbidity data not available.")
            time.sleep(delay_turbidity)
    except Exception as e:
        print(f"Error in Turbidity thread: {e}")

def salinity_thread_func(delay_sal):
    """
    Salinity monitoring function to be run in a separate thread.

    :param delay_sal: Delay between readings in seconds.
    """
    try:
        salinity_sensor = Salinity(pin=27)  # GPIO27
        voltage_1413 = 0.410
        voltage_12880 = 1.990
        salinity_sensor.calibrate(voltage_1413, voltage_12880)
        print("Salinity sensor calibrated.")

        temperature_placeholder = 25  # Replace with actual temperature reading if available

        salinity_sensor.start_continuous_reading(delay=delay_sal, temperature=temperature_placeholder)
        print("Salinity sensor continuous reading started.")

        while True:
            salinity_value = salinity_sensor.read_salinity()
            with data_lock:
                if salinity_value is not None:
                    sensor_data["salinity"] = f"Salinity: {salinity_value:.2f} PSU"
                    print(f"Salinity updated to: {sensor_data['salinity']}")
                else:
                    sensor_data["salinity"] = "Salinity: N/A"
                    print("Salinity data not available.")
            time.sleep(delay_sal)
    except Exception as e:
        print(f"Error in Salinity thread: {e}")

def display_thread_func():
    """
    Display updating function to be run in a separate thread.
    """
    try:
        while True:
            with data_lock:
                temp_text = sensor_data.get("temperature", "Temp: --.- C")
                tds_text = sensor_data.get("tds", "TDS: --.- ppm")
                turbidity_text = sensor_data.get("turbidity", "Turbidity: --.- NTU")
                salinity_text = sensor_data.get("salinity", "Salinity: --.- PSU")
            print(f"Updating display with: {temp_text}, {tds_text}, {turbidity_text}, {salinity_text}")

            # Update the display
            display_safe((10, 35), temp_text, color=TFT.WHITE)
            display_safe((10, 50), tds_text, color=TFT.CYAN)
            display_safe((10, 65), turbidity_text, color=TFT.GREEN)
            display_safe((10, 80), salinity_text, color=TFT.RED)

            time.sleep(1)  # Update display every second
    except Exception as e:
        print(f"Error in display thread: {e}")

# Start sensor threads using _thread directly
try:
    _thread.start_new_thread(temp_thread, (1000,))          # 1-second delay (1000 ms)
    _thread.start_new_thread(tds_thread_func, (2,))        # 2-second delay
    _thread.start_new_thread(turbidity_thread_func, (2,))  # 2-second delay
    _thread.start_new_thread(salinity_thread_func, (2,))   # 2-second delay
    _thread.start_new_thread(display_thread_func, ())      # Display update thread (no args)
    print("All threads started successfully.")
except Exception as e:
    print(f"Error starting threads: {e}")

# Keep the main thread alive to allow background threads to run
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated by user.")
