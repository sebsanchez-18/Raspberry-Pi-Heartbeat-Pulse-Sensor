from pulsesensor import Pulsesensor
import time

# Create an instance of Pulsesensor.
sensor = Pulsesensor(channel=0, address=0x48)

# To run the BPM loop asynchronously:
sensor.startAsyncBPM()

try:
    while True:
        # Access sensor.BPM updated in the background thread.
        print("Current BPM:", sensor.BPM)
        time.sleep(1)
except KeyboardInterrupt:
    sensor.stopAsyncBPM()
    print("Stopped BPM measurement.")
