from machine import ADC, Pin
import time

class TDSSensor:
    """
    A class to interface with a TDS (Total Dissolved Solids) sensor using ADC.
    """
    
    def __init__(self, pin_number: int, delay: float = 1.0, calibration_factor: float = 500.0, average: int = 5):
        """
        Initializes the TDS sensor.
        
        :param pin_number: GPIO pin number connected to the TDS sensor.
        :param delay: Delay between readings in seconds.
        :param calibration_factor: Factor to convert voltage to TDS. Adjust based on calibration.
        :param average: Number of readings to average for stability.
        """
        self.pin_number = pin_number
        self.delay = delay
        self.calibration_factor = calibration_factor
        self.average = average
        
        # Initialize the ADC pin
        self.adc = ADC(Pin(self.pin_number))
        self.adc.atten(ADC.ATTN_11DB)  # Set attenuation to measure higher voltages if needed
        self.adc.width(ADC.WIDTH_12BIT)  # Set ADC resolution to 12 bits (0-4095)
        
        print(f"Initialized TDSSensor on pin {self.pin_number} with delay {self.delay}s.")
    
    def read_voltage(self) -> float:
        """
        Reads the raw ADC value and converts it to voltage.
        
        :return: Voltage in volts.
        """
        adc_value = self.adc.read()
        voltage = adc_value / 4095 * 3.3  # Assuming 3.3V reference
        return voltage
    
    def read_tds(self) -> float:
        """
        Reads the TDS value based on the voltage.
        
        :return: TDS value in ppm.
        """
        voltage = self.read_voltage()
        tds_value = voltage * self.calibration_factor
        return tds_value
    
    def read_tds_average(self) -> float:
        """
        Reads the TDS value multiple times and returns the average for stability.
        
        :return: Averaged TDS value in ppm.
        """
        total_tds = 0.0
        for _ in range(self.average):
            tds = self.read_tds()
            total_tds += tds
            time.sleep(0.2)  # Short delay between readings for stabilization
        average_tds = total_tds / self.average
        return average_tds
    
    def start_continuous_reading(self, use_average: bool = True):
        """
        Starts continuous reading of TDS values.
        
        :param use_average: Whether to use averaging for readings.
        """
        try:
            print("Starting continuous TDS readings. Press Ctrl+C to stop.")
            while True:
                if use_average and self.average > 1:
                    tds = self.read_tds_average()
                else:
                    tds = self.read_tds()
                
                if tds > 0:
                    print(f"TDS Value: {tds:.2f} ppm")
                # Removed the else clause to prevent printing when read fails
                
                time.sleep(self.delay)
        except KeyboardInterrupt:
            print("\nContinuous reading stopped by user.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def calibrate(self, known_tds: float):
        """
        Calibrates the sensor using a known TDS solution.
        
        :param known_tds: The known TDS value of the calibration solution in ppm.
        """
        print("Starting calibration...")
        print(f"Please immerse the sensor in a {known_tds} ppm calibration solution.")
        time.sleep(10)  # Wait for sensor to stabilize
        
        measured_tds = self.read_tds_average()
        if measured_tds == 0:
            print("Calibration failed: Measured TDS is zero.")
            return
        
        new_calibration_factor = known_tds / measured_tds
        self.calibration_factor = new_calibration_factor
        print(f"Calibration successful. New calibration factor: {self.calibration_factor:.2f}")
