"""
Author: Electromake
Website: https://electromake.pl/

Example 1: Discover sensors and continuously read temperatures until a key is pressed.
"""

import time
from .thermometer import USBThermometer  # Adjust import if needed

def main() -> None:
    port: str = "/dev/ttyUSB0"  # Adjust the port for your system
    usb_therm = USBThermometer(port)
    
    # Discover sensors
    sensors = usb_therm.discover_ROMs()
    print("Discovered sensors:")
    for i, sensor in enumerate(sensors):
        print(f"  Sensor {i} ROM: {sensor}")
    
    print("\nReading temperatures... (Press Ctrl+C to exit)")
    
    try:
        while True:
            for i in range(len(sensors)):
                temp = usb_therm.read_temperature(i)
                print(f"Sensor {i}: {temp:.2f}°C")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting temperature reading loop.")
    finally:
        del usb_therm

if __name__ == "__main__":
    main()
