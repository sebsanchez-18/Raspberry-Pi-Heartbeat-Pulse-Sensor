import time  # Import the time module
import threading
import matplotlib.pyplot as plt

class Pulsesensor:
    def __init__(self, address, channel):
        try:
            # Use the ADS1015Interface from ADS1015_helper.py
            self.adc = ADS1015Interface(address=address, channel=channel)
            print("ADS1015 initialized successfully.", flush=True)
        except Exception as e:
            print("Error initializing ADS1015Interface:", e, flush=True)
            self.adc = None

        self._stop_event = threading.Event()
        self.time_data = []  # Store time values
        self.voltage_data = []  # Store voltage values

    def getBPMLoop(self):
        """Continuously read voltage and calculate BPM."""
        start_time = time.time()  # Record the start time
        while not self._stop_event.is_set():
            if self.adc:
                try:
                    voltage = self.adc.voltage()  # Use the helper's voltage method
                    self.BPM = voltage * 10  # Dummy calculation; replace with actual logic

                    # Update time and voltage data
                    current_time = time.time() - start_time
                    self.time_data.append(current_time)
                    self.voltage_data.append(voltage)

                    # Limit the size of the data to avoid memory issues
                    if len(self.time_data) > 100:
                        self.time_data.pop(0)
                        self.voltage_data.pop(0)

                    print(f"Voltage: {voltage:.3f} V, BPM: {self.BPM:.1f}", flush=True)
                except Exception as e:
                    print("Error reading voltage:", e, flush=True)
            time.sleep(0.1)

    def plotData(self):
        """Plot the voltage as a function of time."""
        plt.plot(self.time_data, self.voltage_data, label="Voltage vs Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (V)")
        plt.title("Voltage as a Function of Time")
        plt.legend()
        plt.grid(True)
        plt.show()

    def startAsyncBPM(self):
        """Start the BPM calculation loop in a separate thread."""
        self._stop_event.clear()
        self.thread = threading.Thread(target=self.getBPMLoop)
        self.thread.daemon = True
        self.thread.start()

    def stopAsyncBPM(self):
        """Stop the BPM calculation loop."""
        self._stop_event.set()
        self.thread.join()
        self.plotData()  # Plot the data after stopping
