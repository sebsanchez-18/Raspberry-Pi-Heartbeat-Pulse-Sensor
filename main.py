from pulsesensor import Pulsesensor
import time

if __name__ == "__main__":
    sensor = Pulsesensor(channel=0, address=0x48)
    try:
        sensor.startAsyncBPM()
        while True:
            print(f"Current BPM: {sensor.BPM}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sensor.stopAsyncBPM()
