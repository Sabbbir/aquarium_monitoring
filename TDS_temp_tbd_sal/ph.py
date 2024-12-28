# phs.py

from machine import ADC, Pin
import time

class PHSensor:
    def __init__(self, delay=1.0, adc_pin=27, attenuation=ADC.ATTN_11DB, width=ADC.WIDTH_12BIT, calibration_a=1.0, calibration_b=0.0):
        """
        Initializes the pH Sensor.

        :param delay: Delay between samples in seconds.
        :param adc_pin: GPIO pin number connected to the sensor's analog output.
        :param attenuation: ADC attenuation setting.
        :param width: ADC resolution.
        :param calibration_a: Calibration coefficient 'a' for pH calculation.
        :param calibration_b: Calibration coefficient 'b' for pH calculation.
        """
        self.delay = delay
        self.calibration_a = calibration_a
        self.calibration_b = calibration_b

        # Initialize ADC
        self.adc = ADC(Pin(adc_pin))
        self.adc.atten(attenuation)
        self.adc.width(width)

    def read_voltage_average(self, samples=10, delay_between=0.01):
        """
        Reads the ADC value multiple times and returns the averaged voltage.

        :return: Averaged voltage in volts.
        """
        total = 0
        for _ in range(samples):
            total += self.adc.read()
            time.sleep(delay_between)
        average_raw = total / samples
        voltage = average_raw * 3.3 / 4095  # ESP32 ADC reference voltage is ~3.3V
        return voltage

    def convert_voltage_to_ph(self, voltage):
        """
        Converts the voltage reading to pH.

        :param voltage: Voltage in volts.
        :return: pH value.
        """
        ph = (self.calibration_a * voltage) + self.calibration_b
        return ph

    def start_continuous_reading(self):
        """
        Starts continuous reading of pH values with the specified delay.
        This method is intended to be run in a separate thread.
        """
        print("Starting pH Sensor Readings...")
        try:
            while True:
                voltage = self.read_voltage_average()
                ph = self.convert_voltage_to_ph(voltage)
                print(f"pH: {ph:.2f}")
                time.sleep(self.delay)
        except Exception as e:
            print(f"pH Sensor Error: {e}")
