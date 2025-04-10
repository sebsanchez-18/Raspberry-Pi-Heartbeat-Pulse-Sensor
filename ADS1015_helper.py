from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1015 as ADS
import board
import busio
class ADS1015Interface:
    def __init__(self, address=0x48, channel=0):
        # Initialize the I2C bus and ADS1015
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1015(self.i2c, address=address)
        self.ads.gain = 1  # Set the gain (adjust as needed)

        # Map the channel number to the ADS1015 channel constant
        channel_map = {
            0: ADS.P0,
            1: ADS.P1,
            2: ADS.P2,
            3: ADS.P3
        }

        if channel not in channel_map:
            raise ValueError(f"Invalid channel: {channel}. Must be 0, 1, 2, or 3.")

        # Initialize the AnalogIn object for the specified channel
        self.chan = AnalogIn(self.ads, channel_map[channel])

    def read(self):
        """Read the raw ADC value."""
        return self.chan.value

    def voltage(self):
        """Read the voltage from the specified channel."""
        return self.chan.voltage
