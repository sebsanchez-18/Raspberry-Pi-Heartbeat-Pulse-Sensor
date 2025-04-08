import time
import threading
import board
import busio
import adafruit_ads1x15.ads1015 as ADS  # Import the module as ADS
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
            while not self.i2c.try_lock():
                pass
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
            self.i2c.unlock()
        else:
            print("I2C not initialized properly.", flush=True)
            self.ads = None
            self.chan = None

        self._stop_event = threading.Event()
        print("Pulsesensor initialized.", flush=True)

    def getBPMLoop(self):
        print("Entering getBPMLoop...", flush=True)
        # Dummy loop: updates BPM (voltage * 10) every 0.1 second.
        while not self._stop_event.is_set():
            if self.chan is not None:
                try:
                    voltage = self.chan.voltage
                except Exception as e:
                    print("Error reading voltage:", e, flush=True)
                    voltage = 0
            else:
                voltage = 0
            self.BPM = voltage * 10  # Dummy calculation; replace with actual BPM logic.
            print(f"Voltage: {voltage:.2f} V, Dummy BPM: {self.BPM:.1f}", flush=True)
            time.sleep(0.1)

    def startAsyncBPM(self):
        self._stop_event.clear()
        self.thread = threading.Thread(target=self.getBPMLoop)
        # Mark the thread as daemon so it will not block program exit.
        self.thread.daemon = True
        self.thread.start()
        print("Async BPM thread started.", flush=True)
    
    def stopAsyncBPM(self):
        self._stop_event.set()
        self.thread.join()
        self.BPM = 0
        print("Async BPM thread stopped.", flush=True)
