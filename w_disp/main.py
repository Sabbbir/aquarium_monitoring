from disp.old_tft import *
from thread_manager import start_thread
import time

# Initialize the TFTDisplay object
tft_display = TFTDisplay(spi, cs_pin=15, dc_pin=2, reset_pin=4)

# Rotate the display
tft_display.tft.rotation(1)

# Shared dictionary for sensor values
sensor_values = {
    "Temp": 0.0,
    "TDS": 0.0,
    "TBD": 0.0,
    "EC": 0.0,
    "pH": 7.0,
    "DO": 8.5,
}

# Flag to signal updates between threads
update_flag = False

def update_display(arg):
    """
    Update only the monitoring values on the TFT screen.
    """
    global sensor_values, update_flag
    
    # Display the title once
    tft_display.display((10, 10), "Aquarium Monitoring", color=TFT.CYAN, size=1)
    
    # Display static labels for monitoring values
    y_positions = {
        "Temp": 25,
        "TDS": 40,
        "TBD": 55,
        "EC": 70,
        "pH": 85,
        "DO": 100
    }
    for label, y in y_positions.items():
        tft_display.display((10, y), f"{label}:", color=TFT.WHITE, size=1)
    
    while True:
        if update_flag:  # Only update when the flag is set
            for label, value in sensor_values.items():
                y = y_positions[label]
                # Clear the previous value
                tft_display.tft.fillrect((70, y), (50, 10), TFT.BLACK)
                # Display the new value
                tft_display.display((70, y), f"{value:.2f}", color=TFT.GREEN, size=1)
            
            update_flag = False  # Reset flag after updating

        time.sleep(0.1)  # Reduce unnecessary looping

# Start the display update in a separate thread
start_thread(update_display, None)

# Sensor Functions to Update Shared Values
def temp_update(delay_temp):
    from temp_class import TempSensor
    sensor = TempSensor(data_pin=2, delay=delay_temp)
    sensor.start_continuous_reading()
    while True:
        sensor_values["Temp"] = sensor.get_temperature()
        global update_flag
        update_flag = True
        time.sleep(delay_temp / 1000)

def tds_update(delay_tds):
    from tdss import TDSSensor
    sensor = TDSSensor(adc_pin_num=12, calibration_factor=300.0, read_interval=delay_tds)
    sensor.start_monitoring()
    while True:
        sensor_values["TDS"] = sensor.read_tds()
        global update_flag
        update_flag = True
        time.sleep(delay_tds)

def tbd_update(delay_turbidity):
    from tbd import TBD
    sensor = TBD(delay=delay_turbidity, calibration_a=100, calibration_b=-100)
    sensor.start_continuous_reading()
    while True:
        sensor_values["TBD"] = sensor.get_turbidity()
        global update_flag
        update_flag = True
        time.sleep(delay_turbidity)

def salinity_update(delay_ec):
    from salinity import Salinity
    sensor = Salinity(pin=27)
    sensor.calibrate(voltage_1413=0.410, voltage_12880=1.990)
    sensor.start_continuous_reading(delay=delay_ec, temperature=25)
    while True:
        sensor_values["EC"] = sensor.get_ec()
        global update_flag
        update_flag = True
        time.sleep(delay_ec)

# Start sensor threads
start_thread(temp_update, 1000)    # Temp with 1-second delay
start_thread(tds_update, 2)       # TDS with 2-second delay
start_thread(tbd_update, 2)       # Turbidity with 2-second delay
start_thread(salinity_update, 2)  # Salinity (EC) with 2-second delay

# Keep the main thread alive to allow background threads to run
try:
    while True:
        time.sleep(1)  # Sleep to reduce CPU usage
except KeyboardInterrupt:
    print("Program terminated by user.")
