from temp_class import TempSensor
from tds import TDSSensor
from tdss import TDSSensor

def temp():
    data_pin_temp = 2
    delay = 100
    sensor = TempSensor(data_pin_temp, delay)  # Use default delay of 750ms
    sensor.start_continuous_reading() #Start continuous reading with default 5 second delay

def tds():
    data_pin = 36           # GPIO pin number connected to the TDS sensor
    delay = 1.0             # Delay between readings in seconds
    calibration = 500.0     # Initial calibration factor (will be updated after calibration)
    average_readings = 5    # Number of readings to average
    
    # Initialize the TDS sensor
    tds_sensor = TDSSensor(pin_number=data_pin, delay=delay, calibration_factor=calibration, average=average_readings)
    
    # Perform calibration
    known_tds = 342.0  # Example known TDS value for calibration solution
    tds_sensor.calibrate(known_tds)
    
    # Start continuous reading with averaging
    tds_sensor.start_continuous_reading(use_average=True)

# tds()
# temp()

def tdss():
    # Configuration Parameters
    DATA_PIN = 34             # GPIO pin connected to the TDS sensor's analog output
    DELAY = 1.0               # Delay between readings in seconds
    CALIBRATION_FACTOR = 1.0  # Initial calibration factor (to be updated via calibration)
    AVERAGE_READINGS = 5      # Number of readings to average for stability

    # Initialize the TDS sensor
    tds_sensor = TDSSensor(
        pin_number=DATA_PIN,
        delay=DELAY,
        calibration_factor=CALIBRATION_FACTOR,
        average=AVERAGE_READINGS
    )

    # Perform Calibration
    KNOWN_TDS = 342.0  # Example known TDS value for calibration (ppm)
    tds_sensor.calibrate(KNOWN_TDS)

    # Start Continuous Reading
    tds_sensor.start_continuous_reading(use_average=True)

# if __name__ == "__main__":
#     main()
tdss()