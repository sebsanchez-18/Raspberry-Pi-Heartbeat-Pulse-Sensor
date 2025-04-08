from pulsesensor import Pulsesensor
import time

def main():
    sensor = Pulsesensor(channel=0, address=0x48)
    sensor.startAsyncBPM()

    try:
        while True:
            # Print the current BPM value every second.
            print("Current BPM from main loop:", sensor.BPM, flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        sensor.stopAsyncBPM()
        print("Stopped BPM measurement.", flush=True)

if __name__ == '__main__':
    main()
