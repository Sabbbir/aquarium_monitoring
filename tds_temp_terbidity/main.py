from temp_class import TempSensor
from tdss import TDSSensor
from thread_manager import start_thread  # Import the threading function
import time
from tbd import TBD  # from tbd import


def temp(delay_temp):
    """
    Temperature monitoring function to be run in a separate thread.

    :param delay_temp: Delay between readings in milliseconds.
    """
    data_pin_temp = 2
    # Initialize TempSensor with delay_temp
    sensor = TempSensor(data_pin_temp, delay_temp)
    sensor.start_continuous_reading()
    print("========================")  # Start continuous reading


def tds(delay_tds):
    """
    TDS monitoring function to be run in a separate thread.

    :param delay_tds: Delay between readings in seconds.
    """
    try:
        ADC_PIN = 12  # GPIO12 (D12)
        # Example calibration factor (adjust as needed)
        CALIBRATION_FACTOR = 300.0
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


def tbdt(delay_turbidity):
    """
    Turbidity monitoring function to be run in a separate thread.

    :param delay_turbidity: Delay between readings in seconds.
    """
    # Initialize the Turbidity Sensor with the desired delay and calibration constants
    # turbidity_sensor = TBD(delay=delay_turbidity,
    #                        calibration_a=1.0, calibration_b=0.0)
    # In main.py, within tbdt function
    turbidity_sensor = TBD(delay=delay_turbidity, calibration_a=100, calibration_b=-100)

    turbidity_sensor.start_continuous_reading()


# Start threads with appropriate delays

# adc pin = 2
start_thread(temp, 1000) 

# White sensor
# 5V VCC
# Gnd
# adc pin = 12
start_thread(tds, 2)

# 5V VCC
# Gnd
# adc_pin = 14
start_thread(tbdt, 2)





# Start TDS thread with 2-second delay
# Keep the main thread alive to allow background threads to run
try:
    while True:
        time.sleep(1)  # Sleep to reduce CPU usage
except KeyboardInterrupt:
    print("Program terminated by user.")
