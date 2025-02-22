"""
Author: Electromake
Website: https://electromake.pl/

Module for representing and handling DS18B20 sensor devices.
"""

import time
from typing import List, Tuple

import serial

from .exceptions import *
from .utils import *


class DS18B20:
    """
    A class representing a DS18B20 sensor device.

    The DS18B20 device is identified by a 64-bit ROM code. This class processes
    the bit list representing the ROM, computes its CRC, serial number, and family code,
    and provides methods to retrieve these values.
    """

    def __init__(self, bit_list: List[int]) -> None:
        """
        Initialize the DS18B20 sensor instance using a list of bits representing the ROM.

        Args:
            bit_list (List[int]): A list of 64 integers (0 or 1) representing the sensor's ROM code.

        Raises:
            ValueError: If the input list does not contain exactly 64 elements.
            CRCError: If the calculated CRC does not match the expected CRC.
        """
        if len(bit_list) != 64:
            raise ValueError("Input list must have 64 elements.")
        self.ROM_bytes = bitlist2bytearray(bit_list)
        CRC_calc = CRC8(self.ROM_bytes[0:-1])
        if CRC_calc != self.ROM_bytes[-1]:
            CRCError(self.ROM_bytes[-1], CRC_calc)
        # Convert Big Endian to Little Endian
        bit_list.reverse()  # bit_list - [MSB, ..., LSB]
        self.bit_list = bit_list
        self.CRC = 0
        self.FAMILY_CODE = 0
        self.SERIAL_NUMBER = 0
        self.hex_str = ""
        self.__calc()

    def __str__(self) -> str:
        """
        Return the hexadecimal string representation of the sensor's ROM.

        Returns:
            str: The hexadecimal string of the sensor's ROM.
        """
        return f"{self.hex_str}"

    def __repr__(self) -> str:
        """
        Return the official string representation of the DS18B20 sensor.

        Returns:
            str: The hexadecimal string of the sensor's ROM.
        """
        return f"{self.hex_str}"

    def __calc(self) -> None:
        """
        Calculate the sensor's CRC, serial number, and family code from the bit list.

        This method processes the reversed bit list to compute:
         - CRC from the first 8 bits.
         - Serial number from bits 8 to 55.
         - Family code from bits 56 to 63.
        It then restores the original bit list order and computes the hexadecimal string.
        """
        for i in range(0, 8):
            self.CRC <<= 1
            self.CRC += self.bit_list[i]
        for i in range(8, 56):
            self.SERIAL_NUMBER <<= 1
            self.SERIAL_NUMBER += self.bit_list[i]
        for i in range(56, 64):
            self.FAMILY_CODE <<= 1
            self.FAMILY_CODE += self.bit_list[i]
        self.bit_list.reverse()
        self.hex_str = bit_list2hex_str(self.bit_list)

    def get_ROM_bit_list(self) -> List[int]:
        """
        Retrieve the ROM code as a list of bits.

        Returns:
            List[int]: The ROM code bit list.
        """
        return self.bit_list

    def get_ROM_bytes(self) -> bytearray:
        """
        Retrieve the ROM code as a bytearray.

        Returns:
            bytearray: The ROM code bytes.
        """
        return self.ROM_bytes

    def get_serial_number(self) -> int:
        """
        Retrieve the sensor's serial number.

        Returns:
            int: The sensor's serial number.
        """
        return self.SERIAL_NUMBER

    def get_family_code(self) -> int:
        """
        Retrieve the sensor's family code.

        Returns:
            int: The sensor's family code.
        """
        return self.FAMILY_CODE

    def get_CRC(self) -> int:
        """
        Retrieve the CRC of the sensor's ROM code.

        Returns:
            int: The CRC value.
        """
        return self.CRC

    # CONFIGURATION REGISTER
    CR_09BIT = 0x1F  # 0.5000 deg
    CR_10BIT = 0x3F  # 0.2500 deg
    CR_11BIT = 0x5F  # 0.1250 deg
    CR_12BIT = 0x7F  # 0.0625 deg
    CR_MODES = {CR_09BIT, CR_10BIT, CR_11BIT, CR_12BIT}
