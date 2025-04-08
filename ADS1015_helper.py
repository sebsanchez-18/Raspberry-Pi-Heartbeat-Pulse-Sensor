import time
import board
import busio
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.analog_in import AnalogIn

class ADS1015Interface:
    def __init__(self, address=0x48, channel=0):
        """
        Initializes the ADS1015 ADC.

        :param address: I2C address of the ADS1015 (default is 0x48)
        :param channel: Analog input channel (0-3)
        """
        self.channel = channel

        # Setup I2C using board's default I2C pins
        i2c = busio.I2C(board.SCL, board.SDA)
        
        # Create the ADS1015 ADC object
        self.ads = ADS1015(i2c, address=address)
        # Configure the gain as needed (adjust depending on your voltage range)
        self.ads.gain = 1
        
        # Select the analog channel. ADS1015 channel labels are: P0, P1, P2, and P3.
        self.chan = AnalogIn(self.ads, getattr(ADS1015, f'P{channel}'))

    def read(self):
        """
        Reads the ADC conversion value from the selected channel.

        :return: ADC raw value (the library scales this value; refer to documentation for details)
        """
        return self.chan.value

    def voltage(self):
        """
        Reads the voltage at the selected channel.

        :return: Voltage reading from the channel.
        """
        return self.chan.voltage

    def close(self):
        """
        For ADS1015 via CircuitPython, no explicit close is required.
        This method is provided for compatibility.
        """
        pass

# Example usage for Python 3:
if __name__ == "__main__":
    adc = ADS1015Interface(address=0x48, channel=0)
    try:
        while True:
            raw_value = adc.read()
            voltage = adc.voltage()
            print(f"Raw value: {raw_value}, Voltage: {voltage:.3f} V")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        adc.close()
