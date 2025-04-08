import time
import threading
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class Pulsesensor:
    def __init__(self, channel=0, address=0x48):
        self.channel = channel
        self.BPM = 0

        try:
            # Initialize I2C bus
            self.i2c = busio.I2C(board.SCL, board.SDA)
        except Exception as e:
            print("Error initializing I2C:", e, flush=True)
            self.i2c = None

        if self.i2c:
            # Wait until the I2C bus is locked before proceeding
            timeout = time.time() + 5  # 5-second timeout
            while not self.i2c.try_lock():
                if time.time() > timeout:
                    print("Error: I2C bus lock timeout.", flush=True)
                    self.i2c = None
                    break
            time.sleep(0.1)  # Allow the bus to settle

            try:
                # Initialize the ADS1015 at the specified address (default 0x48)
                self.ads = ADS.ADS1015(self.i2c, address=address)
                self.ads.gain = 1
                # Access the module-level channel constant (e.g. ADS.P0)
                self.chan = AnalogIn(self.ads, getattr(ADS, f'P{channel}'))
            except Exception as e:
                print("Error initializing ADS1015:", e, flush=True)
                self.ads = None
                self.chan = None
            finally:
                self.i2c.unlock()
        else:
            print("I2C not initialized properly.", flush=True)
            self.ads = None
            self.chan = None

        self._stop_event = threading.Event()
