import machine
import time

class TDSSensor:
    def __init__(self, adc_pin_num=12, calibration_factor=1.0, read_interval=2):
        """
        Initializes the TDS Sensor.

        :param adc_pin_num: GPIO pin number connected to the TDS sensor's analog output (default: 12)
        :param calibration_factor: Factor to convert voltage to TDS (ppm) (default: 1.0)
        :param read_interval: Time between readings in seconds (default: 2)
        """
        self.adc_pin_num = adc_pin_num
        self.calibration_factor = calibration_factor
        self.read_interval = read_interval

        # Initialize ADC
        self.adc = machine.ADC(machine.Pin(self.adc_pin_num))
        self.adc.atten(machine.ADC.ATTN_11DB)  # ~0 - 3.6V
        self.adc.width(machine.ADC.WIDTH_12BIT)  # 12-bit resolution

    def read_adc_value(self):
        """
        Reads the raw ADC value from the TDS sensor.

        :return: Raw ADC value (integer)
        """
        adc_value = self.adc.read()
        return adc_value

    def convert_adc_to_voltage(self, adc_value):
        """
        Converts ADC value to voltage.

        :param adc_value: Raw ADC value
        :return: Voltage in volts (float)
        """
        max_adc = 4095  # 12-bit ADC
        max_voltage = 3.6  # Maximum voltage corresponding to ADC max value
        voltage = (adc_value / max_adc) * max_voltage
        return voltage

    def calculate_tds(self, voltage):
        """
        Converts voltage to TDS (ppm).

        :param voltage: Voltage in volts
        :return: TDS value in ppm (float)
        """
        tds = voltage * self.calibration_factor
        return tds

    def get_tds_reading(self):
        """
        Performs a single TDS reading.

        :return: Tuple containing (adc_value, voltage, tds)
        """
        adc_value = self.read_adc_value()
        voltage = self.convert_adc_to_voltage(adc_value)
        tds = self.calculate_tds(voltage)
        return adc_value, voltage, tds

    def start_monitoring(self):
        """
        Starts continuous TDS monitoring and prints the readings to the serial console.
        """
        print("Starting TDS Monitoring...")
        try:
            while True:
                adc_value, voltage, tds = self.get_tds_reading()
                # print(f"ADC Value: {adc_value} | Voltage: {voltage:.2f} V | TDS: {tds:.2f} ppm")
                print(f"TDS: {tds:.2f} ppm")
                time.sleep(self.read_interval)
        except KeyboardInterrupt:
            print("\nTDS Monitoring Stopped.")
            

