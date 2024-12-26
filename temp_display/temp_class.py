# temp_sensor.py

from machine import Pin
import onewire
import ds18x20
import time

class TempSensor:
    def __init__(self, data_pin, delay):
        self.data_pin = data_pin
        self.ow = onewire.OneWire(Pin(self.data_pin))
        self.ds = ds18x20.DS18X20(self.ow)
        self.delay = delay
        self.roms = self.ds.scan()
        if not self.roms:
            print("No sensors found!")
            self.sensor_available = False
        else:
            print("Found devices:", self.roms)
            self.sensor_available = True

    def read_temperature(self):
        if self.sensor_available:
            self.ds.convert_temp()
            time.sleep_ms(self.delay)  # Wait for temperature conversion (750ms for 12-bit resolution)
            temp_c = self.ds.read_temp(self.roms[0])  # Assuming only one sensor
            return temp_c
        else:
            return None
