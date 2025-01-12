from machine import ADC, Pin
import time

class Salinity:
    def __init__(self, pin, vref=3.3, resolution=4095):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)  # Set ADC range to 0-3.6V
        self.vref = vref
        self.resolution = resolution
        self.slope = None
        self.offset = None

    def calibrate(self, voltage_1413, voltage_12880):
        # Known values
        C1 = 1413  # µS/cm
        C2 = 12880  # µS/cm
        # Calculate slope and offset
        self.slope = (C2 - C1) / (voltage_12880 - voltage_1413)
        self.offset = C1 - (self.slope * voltage_1413)
        print(f"Calibration complete: Slope={self.slope:.2f}, Offset={self.offset:.2f}")

    def read_voltage(self):
        raw_value = self.adc.read()
        return (raw_value / self.resolution) * self.vref

    def read_ec(self, voltage, temperature):
        temp_coefficient = 1.0 + 0.0185 * (temperature - 25)
        compensated_voltage = voltage / temp_coefficient
        conductivity = (compensated_voltage * self.slope) + self.offset
        return conductivity

    @staticmethod
    def moving_average(new_value, buffer, size=10):
        buffer.append(new_value)
        if len(buffer) > size:
            buffer.pop(0)
        return sum(buffer) / len(buffer)

    def start_continuous_reading(self, delay, temperature, buffer_size=10):
        buffer = []
        while True:
            try:
                voltage = self.read_voltage()
                ec_value = self.read_ec(voltage, temperature)
                smoothed_ec = self.moving_average(ec_value, buffer, buffer_size)
                print(f"Voltage: {voltage:.3f} V, EC: {smoothed_ec:.2f} mS/cm")
                time.sleep(delay)
            except Exception as e:
                print(f"Error in salinity reading: {e}")
