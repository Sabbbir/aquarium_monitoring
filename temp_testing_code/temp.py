import machine
import onewire
import ds18x20
import time

# Define the pin where the DS18B20 is connected
DS_PIN = 2  # GPIO4 (D4)

# Initialize the 1-Wire bus
try:
    pin = machine.Pin(DS_PIN)
    print(f"Initializing OneWire on GPIO{DS_PIN}...")
    ow = onewire.OneWire(pin)
except Exception as e:
    print(f"Error initializing OneWire on GPIO{DS_PIN}: {e}")
    raise

# Initialize the DS18X20 sensor
# try:
ds = ds18x20.DS18X20(ow)
#     print("DS18X20 sensor initialized.")
# except Exception as e:
#     print(f"Error initializing DS18X20: {e}")
#     raise

# Scan for devices on the bus
try:
    roms = ds.scan()
    if not roms:
        print("No DS18B20 sensors found!")
        while True: # loop infinitely if no sensor is found
            time.sleep(1)
    else:
        print(f"Found {len(roms)} DS18B20 sensor(s):")
        for rom in roms:
            print(" -", rom.hex())
except Exception as e:
    print(f"Error scanning for sensors: {e}")
    raise

# Function to read temperatures
def read_temperatures():
    try:
        ds.convert_temp()
        time.sleep_ms(750)  # Wait for conversion
    except Exception as e:
        print(f"Error during temperature conversion: {e}")
        return {}
    
    temperatures = {}
    for rom in roms:
        try:
            temp = ds.read_temp(rom)
            if temp is not None:
                temperatures[rom.hex()] = temp
            else:
                print(f"Error: Could not read temperature from sensor {rom.hex()}") # more specific error message
                temperatures[rom.hex()] = "Error"
        except Exception as e:
            print(f"Error reading temperature from {rom.hex()}: {e}")
            temperatures[rom.hex()] = "Error"
    return temperatures

# Main loop
while True:
    temps = read_temperatures()
    if temps:
        for rom, temp in temps.items():
            if isinstance(temp, float): # check if the temperature is a float before formatting
                print(f"Temperature: {temp:.2f} C")  # Correct degree Celsius
            else:
                print(f"Sensor ROM: {rom} Temperature: {temp}") # Print the error message if the temperature is not a float
    else:
        print("No temperatures to display (conversion error?).")
    print("---------------------------")
    time.sleep(.1)