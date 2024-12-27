from temp_class import TempSensor
from tdss import TDSSensor

def temp():
    data_pin_temp = 2
    delay = 100
    sensor = TempSensor(data_pin_temp, delay)  # Use default delay of 750ms
    sensor.start_continuous_reading() #Start continuous reading with default 5 second delay


# temp()


# Example usage
def tds():
    ADC_PIN = 12  # GPIO12 (D12)
    CALIBRATION_FACTOR = 300.0  # Example calibration factor (adjust as needed)
    READ_INTERVAL = 5  # Read every 5 seconds

    # Instantiate the TDSSensor class with desired parameters
    tds_sensor = TDSSensor(adc_pin_num=ADC_PIN,
                           calibration_factor=CALIBRATION_FACTOR,
                           read_interval=READ_INTERVAL)

    tds_sensor.start_monitoring()

tds()