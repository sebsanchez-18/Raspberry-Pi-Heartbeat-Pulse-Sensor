from pulsesensor import Pulsesensor
import time

# Create an instance of Pulsesensor.
sensor = Pulsesensor(channel=0, address=0x48)

# Start the BPM measurement asynchronously.
sensor.startAsyncBPM()

try:
    while True:
        # Print the current BPM once per second.
        print("Current BPM from main loop:", sensor.BPM)
        time.sleep(1)
except KeyboardInterrupt:
    sensor.stopAsyncBPM()
    print("Stopped BPM measurement.")
