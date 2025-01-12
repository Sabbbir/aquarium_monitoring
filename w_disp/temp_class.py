# temp_class.py
from machine import Pin
import onewire
import ds18x20
import time
from onewire import OneWireError

class TempSensor:
    def __init__(self, data_pin, delay):  # Default delay of 750ms
        self.data_pin = data_pin
        self.ow = onewire.OneWire(Pin(self.data_pin))
        self.ds = ds18x20.DS18X20(self.ow)
        self.delay = delay
        self.roms = self.ds.scan()
        if not self.roms:
            self.sensor_available = False
        else:
            # print("Found devices:", self.roms)
            self.sensor_available = True

    def read_temperature(self):
        if self.sensor_available:
            try:
                self.ds.convert_temp()
                time.sleep_ms(self.delay)
                if self.roms:
                    temp_c = self.ds.read_temp(self.roms[0])
                    return temp_c
                else:
                    return None
            except OneWireError as e:
                print(f"OneWireError during temperature read: {e}")
                return None
            except Exception as e:
                print(f"Unexpected error during temperature read: {e}")
                return None
        else:
            return None

    def start_continuous_reading(self):
        if self.sensor_available:
            try:
                while True:
                    temperature = self.read_temperature()
                    if temperature is not None:
                        print(f"Temperature: {temperature:.2f} C")
                        print("========================")
                    else:
                        print("Failed to read temperature.")
                    time.sleep_ms(self.delay)  # Use sleep in milliseconds
            except KeyboardInterrupt:
                print("Exiting temperature monitoring...")
            except Exception as e:
                print(f"Error in temperature monitoring thread: {e}")
        else:
            print("No temperature sensor found!")
