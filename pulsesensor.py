# PulseSensor using ADS1015 (I2C ADC)
import time
import threading
import board
import busio
from adafruit_ads1x15.ads1015 import ADS1015
from adafruit_ads1x15.analog_in import AnalogIn

class Pulsesensor:
    def __init__(self, channel=0):
        self.channel = channel
        self.BPM = 0

        # Setup I2C and ADS1015
        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS1015(i2c)
        self.ads.gain = 1

        # Channel selection (0–3)
        self.chan = AnalogIn(self.ads, getattr(ADS1015, f'P{channel}'))

        self._stop_event = threading.Event()

    def getBPMLoop(self):
        rate = [0] * 10
        sampleCounter = 0
        lastBeatTime = 0
        P = 512
        T = 512
        thresh = 525
        amp = 100
        firstBeat = True
        secondBeat = False

        IBI = 600
        Pulse = False
        lastTime = int(time.time() * 1000)

        while not self._stop_event.is_set():
            Signal = self.chan.value // 256  # scale 16-bit to 10-bit range roughly

            currentTime = int(time.time() * 1000)
            sampleCounter += currentTime - lastTime
            lastTime = currentTime
            N = sampleCounter - lastBeatTime

            if Signal < thresh and N > (IBI / 5.0) * 3:
                if Signal < T:
                    T = Signal

            if Signal > thresh and Signal > P:
                P = Signal

            if N > 250:
                if Signal > thresh and not Pulse and N > (IBI / 5.0) * 3:
                    Pulse = True
                    IBI = sampleCounter - lastBeatTime
                    lastBeatTime = sampleCounter

                    if secondBeat:
                        secondBeat = False
                        rate = [IBI] * len(rate)

                    if firstBeat:
                        firstBeat = False
                        secondBeat = True
                        continue

                    rate[:-1] = rate[1:]
                    rate[-1] = IBI
                    runningTotal = sum(rate)
                    runningTotal /= len(rate)
                    self.BPM = 60000 / runningTotal

            if Signal < thresh and Pulse:
                Pulse = False
                amp = P - T
                thresh = amp / 2 + T
                P = thresh
                T = thresh

            if N > 2500:
                thresh = 512
                P = 512
                T = 512
                lastBeatTime = sampleCounter
                firstBeat = True
                secondBeat = False
                self.BPM = 0

            time.sleep(0.005)

    def startAsyncBPM(self):
        self._stop_event.clear()
        self.thread = threading.Thread(target=self.getBPMLoop)
        self.thread.start()

    def stopAsyncBPM(self):
        self._stop_event.set()
        self.thread.join()
        self.BPM = 0

