"""
Author: Electromake
Website: https://electromake.pl/

Example 3: Configure sensor settings (precision and alarm thresholds).
This example discovers sensors, sets the precision to 12-bit, then updates the alarm thresholds,
and finally reads back the scratchpad values to verify the configuration.
"""

import time
from .sensors import DS18B20
from .thermometer import USBThermometer  # Adjust import as necessary

def main() -> None:
    port: str = "/dev/ttyUSB0"  # Adjust the port for your system
    usb_therm = USBThermometer(port)
    sensors = usb_therm.discover_ROMs()
    
    if not sensors:
        print("No sensors discovered!")
        return

    print("Configuring sensor settings for sensor 0:")
    print(f"Sensor 0: {sensors[0]}")

    # Set precision to 12-bit
    print("\nSetting precision to 12-bit...")
    usb_therm.set_precision(0, DS18B20.CR_12BIT)
    T, TH, TL, CR, CRC = usb_therm.read_scratchpad(0)
    print(f"Scratchpad after precision set: T={T:.2f}, TH={TH}, TL={TL}, CR={CR}")

    # Set alarm thresholds (example: TH=50, TL=10)
    print("\nSetting alarm thresholds: TH=50, TL=10...")
    usb_therm.set_alarm(0, 50, 10)
    T, TH, TL, CR, CRC = usb_therm.read_scratchpad(0)
    print(f"Scratchpad after alarm set: T={T:.2f}, TH={TH}, TL={TL}, CR={CR}")

    del usb_therm

if __name__ == "__main__":
    main()
