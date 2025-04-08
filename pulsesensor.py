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

        # Initialize I2C and wait for the bus lock
        self.i2c = busio.I2C(board.SCL, board.SDA)
        while not self.i2c.try_lock():
            pass
        time.sleep(0.1)  # Allow the bus to settle
        
        # Initialize the ADS1015 at the specified address (default 0x48)
        self.ads = ADS.ADS1015(self.i2c, address=address)
        self.ads.gain = 1
        
        # Use getattr on the ADS module to access the channel constant, e.g. ADS.P0, ADS.P1, etc.
        self.chan = AnalogIn(self.ads, getattr(ADS, f'P{channel}'))
        self.i2c.unlock()  # Unlock after initialization
        
        self._stop_event = threading.Event()
        print("Pulsesensor initialized.")  # Debug message

    def getBPMLoop(self):
        print("Entering getBPMLoop...")  # Debug: confirm the thread has started
        # Dummy loop: reads the voltage and updates BPM (voltage * 10) every 0.1 second.
        while not self._stop_event.is_set():
            voltage = self.chan.voltage
            self.BPM = voltage * 10  # Dummy calculation: replace with your algorithm.
            print(f"Voltage: {voltage:.2f} V, Dummy BPM: {self.BPM:.1f}")  # Debug output in the thread
            time.sleep(0.1)

    def startAsyncBPM(self):
        self._stop_event.clear()
        self.thread = threading.Thread(target=self.getBPMLoop)
        self.thread.start()
        print("Async BPM thread started.")  # Debug message
    
    def stopAsyncBPM(self):
        self._stop_event.set()
        self.thread.join()
        self.BPM = 0.
        print("Async BPM thread stopped.")  # Debug message
