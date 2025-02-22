"""
Author: Electromake
Website: https://electromake.pl/

Module for unit testing the USBThermometer functionalities and utility functions.
Use to run: python -m unittest -v test.py
"""

import struct
import unittest
from typing import List, Tuple

from electromake.usb_thermometer.sensors import DS18B20
from electromake.usb_thermometer.utils import *
from electromake.usb_thermometer.thermometer import *


class TestUSBThermometer(unittest.TestCase):
    """
    Unit tests for the USBThermometer functionalities.
    """

    def setUp(self) -> None:
        self.port = "/dev/ttyUSB0"

    def test__read_temp(self) -> None:
        """
        Test reading temperature from sensors using USBThermometer.

        This test discovers sensors on the bus, prints the detected sensors, and
        reads the temperature from each sensor several times.
        """
        usb_therm = USBThermometer(self.port)
        usb_therm.discover_ROMs()
        devices = usb_therm.get_devices()
        print("\nSensors found:")
        for i, device in enumerate(devices):
            print(f"  Sensor {i}: {device} ")
        print("-"*40)
        for i in range(5):
            for i in range(len(devices)):
                T = usb_therm.read_temperature(i)
                print(f"Sensor {i}: {T:3.2f}°C")
        del usb_therm

    def test__write_read_scratchpad(self) -> None:
        """
        Test writing to and reading from the sensor's scratchpad.

        This test writes specific threshold and configuration register values to the scratchpad,
        reads them back, and verifies that the values match the expected ones.
        """
        usb_therm = USBThermometer(self.port)
        usb_therm.discover_ROMs()
        devices = usb_therm.get_devices()
        TH = 127
        TL = -128
        CR = DS18B20.CR_12BIT
        usb_therm.write_scratchpad(0, [TH, TL, CR])
        [T, TH_new, TL_new, CR_new, CRC] = \
            usb_therm.read_scratchpad(0)
        self.assertEqual(TH_new, TH)
        self.assertEqual(TL_new, TL)
        self.assertEqual(CR_new, CR)
        del usb_therm

    def test__write_read_scratchpad_from_E2(self) -> None:
        """
        Test writing to scratchpad, copying to EEPROM, modifying the scratchpad,
        and recalling EEPROM values back into the scratchpad.

        This test writes initial values to the scratchpad and copies them to EEPROM.
        Then it writes new values to the scratchpad, verifies them, recalls the EEPROM values,
        and checks that the recalled values match the original EEPROM values.
        """
        usb_therm = USBThermometer(self.port)
        usb_therm.discover_ROMs()
        devices = usb_therm.get_devices()
        TH_E2, TL_E2, CR_E2 = 10, -10, DS18B20.CR_09BIT
        usb_therm.write_scratchpad(0, [TH_E2, TL_E2, CR_E2])
        # SCRATCHPAD -> EEPROM
        usb_therm.copy_scratchpad(0)
        TH, TL, CR = 20, -20, DS18B20.CR_12BIT
        usb_therm.write_scratchpad(0, [TH, TL, CR])
        [T, TH_new, TL_new, CR_new, CRC] = \
            usb_therm.read_scratchpad(0)
        self.assertEqual(TH_new, TH)
        self.assertEqual(TL_new, TL)
        self.assertEqual(CR_new, CR)
        # EEPROM -> SCRATCHPAD
        usb_therm.recall_E2(0)
        [T, TH_new, TL_new, CR_new, CRC] = \
            usb_therm.read_scratchpad(0)
        self.assertEqual(TH_new, TH_E2)
        self.assertEqual(TL_new, TL_E2)
        self.assertEqual(CR_new, CR_E2)
        del usb_therm


class TestUtils(unittest.TestCase):
    """
    Unit tests for the utility functions.
    """

    def setUp(self) -> None:
        """
        Set up the test environment for utility function tests.
        """
        pass

    def test__CRC8(self) -> None:
        """
        Test the CRC8 function using a known ROM bit list.

        This test converts a known 64-bit ROM represented as a list of bits into a bytearray,
        calculates the CRC8 over all bytes except the last one, and compares the result with
        the expected CRC stored in the last byte.
        """
        # ROM: LSB,...,MSB
        ROM = [0, 0, 0, 1, 0, 1, 0, 0,
               0, 0, 0, 0, 1, 0, 0, 1,
               0, 1, 0, 0, 0, 0, 0, 1,
               0, 1, 0, 0, 0, 1, 1, 1,
               0, 0, 0, 1, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 1, 1, 0, 0, 0, 1]
        ba = bitlist2bytearray(ROM)
        CRC = CRC8(ba[0:-1])
        self.assertEqual(CRC, ba[-1])


if __name__ == "__main__":
    unittest.main()
