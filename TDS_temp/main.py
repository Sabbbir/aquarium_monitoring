from temp_class import TempSensor
from tdss import TDSSensor
from thread_manager import start_thread  # Import the threading function
import time

def temp(delay_temp):
    """
    Temperature monitoring function to be run in a separate thread.
    
    :param delay_temp: Delay between readings in milliseconds.
    """
    data_pin_temp = 2
    sensor = TempSensor(data_pin_temp, delay_temp)  # Initialize TempSensor with delay_temp
    sensor.start_continuous_reading()
    print("========================")  # Start continuous reading

def tds(delay_tds):
    """
    TDS monitoring function to be run in a separate thread.
    
    :param delay_tds: Delay between readings in seconds.
    """
    try:
        ADC_PIN = 12  # GPIO12 (D12)
        CALIBRATION_FACTOR = 300.0  # Example calibration factor (adjust as needed)
        READ_INTERVAL = delay_tds  # Read interval in seconds

        # Instantiate the TDSSensor with desired parameters
        tds_sensor = TDSSensor(
            adc_pin_num=ADC_PIN,
            calibration_factor=CALIBRATION_FACTOR,
            read_interval=READ_INTERVAL
        )

        tds_sensor.start_monitoring()  # Start monitoring TDS
        while True:
            tds_value = tds_sensor.read_tds()
            if tds_value is not None:
                print(f"TDS Value: {tds_value} ppm")
            else:
                print("No TDS sensor found!")
            time.sleep(READ_INTERVAL)
    except Exception as e:
        print(f"Error in tds thread: {e}")


# Start threads with appropriate delays
start_thread(temp, 1000)  # Start temperature thread with 750ms delay
start_thread(tds, 2)      # Start TDS thread with 2-second delay

# Keep the main thread alive to allow background threads to run
try:
    while True:
        time.sleep(5)  # Sleep to reduce CPU usage
except KeyboardInterrupt:
    print("Program terminated by user.")
