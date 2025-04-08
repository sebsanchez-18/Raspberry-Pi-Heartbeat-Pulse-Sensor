from pulsesensor import Pulsesensor
import time

def main():
    p = Pulsesensor()
    p.startAsyncBPM()
    
    try:
        while True:
            bpm = p.BPM
            if bpm > 0:
                print("BPM: {}".format(bpm))
            else:
                print("No Heartbeat found")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        p.stopAsyncBPM()

if __name__ == '__main__':
    main()
