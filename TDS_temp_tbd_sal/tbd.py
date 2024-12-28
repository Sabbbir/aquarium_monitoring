# tbd.py

from machine import ADC, Pin
import time

class TBD:
    def __init__(self, delay=1.0, adc_pin=14, attenuation=ADC.ATTN_11DB, width=ADC.WIDTH_12BIT, calibration_a=100.0, calibration_b=-100.0):
        """
        Initializes the Turbidity Sensor.

        :param delay: Delay between samples in seconds.
        :param adc_pin: GPIO pin number connected to the sensor's analog output.
        :param attenuation: ADC attenuation setting.
        :param width: ADC resolution.
        :param calibration_a: Calibration coefficient 'a' for turbidity calculation.
        :param calibration_b: Calibration coefficient 'b' for turbidity calculation.
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
        voltage = average_raw * 3.3 / 4095
        return voltage

    def convert_voltage_to_turbidity(self, voltage):
        """
        Converts the voltage reading to turbidity in NTU.

        :param voltage: Voltage in volts.
        :return: Turbidity in NTU.
        """
        turbidity = (self.calibration_a * voltage) + self.calibration_b
        return turbidity

    def start_continuous_reading(self):
        """
        Starts continuous reading of turbidity values with the specified delay.
        This method is intended to be run in a separate thread.
        """
        print("Starting Turbidity Sensor Readings...")
        try:
            while True:
                voltage = self.read_voltage_average()
                turbidity = self.convert_voltage_to_turbidity(voltage)
                print(f"Turbidity: {turbidity:.2f} NTU")
                time.sleep(self.delay)
        except Exception as e:
            print(f"Turbidity Sensor Error: {e}")
