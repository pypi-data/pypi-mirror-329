"""
Author: Electromake
Website: https://electromake.pl/

Module for interfacing with a USB thermometer device.
"""

import time

import serial

from .exceptions import *
from .sensors import DS18B20
from .utils import *
from typing import List, Tuple


class USBThermometer:
    """
    Class representing a USB thermometer device using DS18B20 sensors.

    This class provides methods to discover devices, read and write data to sensors,
    and manipulate sensor settings over a serial connection.
    """

    def __init__(self, port: str) -> None:
        """
        Initialize the USBThermometer with a specified serial port.

        Args:
            port (str): The serial port to which the USB thermometer is connected.
        """
        self.__devices = []
        self.__port = port
        self.__serial_port = serial.Serial(
            self.__port,
            9600,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            timeout=1
        )
        self.__serial_port.dtr = True
        self.__serial_port.reset_input_buffer()
        self.__serial_port.reset_output_buffer()
        self.__reset()

    def __del__(self) -> None:
        """
        Destructor to close the serial port upon object deletion.
        """
        self.__serial_port.close()

    __SEARCH_ROM = 0xF0
    __READ_ROM = 0x33
    __MATCH_ROM = 0x55
    __SKIP_ROM = 0xCC
    __ALARM_SEARCH = 0xEC
    __CONVERT_T = 0x44
    __WRITE_SCRATCHPAD = 0x4E
    __READ_SCRATCHPAD = 0xBE
    __COPY_SCRATCHPAD = 0x48
    __RECALL_E2 = 0xB8
    __READ_POWER_SUPPLY = 0xB4

    def __set_baudrate(self, baud: int) -> None:
        """
        Set the baud rate for the serial port.

        Args:
            baud (int): The baud rate to be set.
        """
        self.__serial_port.baudrate = baud

    def __get_baudrate(self) -> int:
        """
        Get the current baud rate of the serial port.

        Returns:
            int: The current baud rate.
        """
        return self.serial_port.baudrate

    def __reset(self) -> None:
        """
        Reset the communication with the USB thermometer device.

        Raises:
            DevicePresenceNotDetected: If the device does not respond during reset.
        """
        self.__set_baudrate(9600)
        self.__serial_port.write(b'\xF0')
        received_byte = self.__serial_port.read(1)
        if received_byte:
            self.__set_baudrate(115200)
            return
        else:
            raise DevicePresenceNotDetected()

    def __write_one(self) -> None:
        """
        Write a logical one (1) to the serial port.
        """
        self.__serial_port.write(b'\xFF')

    def __write_zero(self) -> None:
        """
        Write a logical zero (0) to the serial port.
        """
        self.__serial_port.write(b'\x00')

    def __write_bit(self, bit) -> None:
        """
        Write a single bit to the serial port.

        Args:
            bit (int): The bit value to write (0 or 1).
        """
        self.__write_one() if bit == 1 else self.__write_zero()
        back = self.__serial_port.read(1)

    def __read_bit(self) -> int:
        """
        Read a single bit from the serial port.

        Returns:
            int: The bit read (0 or 1).
        """
        self.__serial_port.write(b'\xFF')
        received_byte = self.__serial_port.read(1)
        return 1 if received_byte[0] == 0xFF else 0

    def __write_byte(self, byte) -> None:
        """
        Write a byte to the serial port, bit by bit.

        Args:
            byte (int): The byte value to write.
        """
        for i in range(0, 8):
            bit = (byte >> i) & 1
            self.__write_bit(bit)

    def __read_byte(self) -> int:
        """
        Read a byte from the serial port, bit by bit.

        Returns:
            int: The byte value read.
        """
        byte = 0
        for i in range(0, 8):
            bit = self.__read_bit()
            byte = byte | (int(bit) << i)
        return byte

    def __add_device(self, bit_list: List[int]) -> None:
        """
        Add a new DS18B20 device based on its ROM bit list.

        Args:
            bit_list (List[int]): The ROM bit list of the device.
        """
        self.__devices.append(DS18B20(bit_list))

    def __write_ROM(self, n) -> None:
        """
        Write the ROM code of a device specified by its index.

        Args:
            n (int): The index of the device in the internal device list.
        """
        for b in self.__devices[n].get_ROM_bit_list():
            self.__write_bit(b)

    def discover_ROMs(self, alarm: bool = False) -> List[DS18B20]:
        """
        Discover devices on the bus by searching for their ROM codes.

        Args:
            alarm (bool, optional): If True, perform an alarm search. Defaults to False.

        Returns:
            List[DS18B20]: A list of discovered DS18B20 devices.
        """
        roms = []
        temp = []
        first_run = True
        while len(temp) > 0 or first_run:
            self.__reset()
            self.__write_byte(
                self.__ALARM_SEARCH if alarm else self.__SEARCH_ROM
            )
            current_rom = [] if first_run else temp.pop()
            current_rom_length = len(current_rom)

            for i in range(0, current_rom_length):
                b = self.__read_bit()
                b_neg = self.__read_bit()
                self.__write_bit(current_rom[i])

            for i in range(0, 64 - current_rom_length):
                b = self.__read_bit()
                b_neg = self.__read_bit()
                if b != b_neg:
                    self.__write_bit(b)
                    current_rom.append(b)
                elif b == 0 and b_neg == 0:
                    # Bus collision. There are both
                    # 0s and 1s in the current bit
                    # position of the participating
                    # ROM numbers. This is a discrepancy.
                    # Save other branch
                    temp.append(current_rom + [1])
                    # Choose branch with 0 at current position.
                    current_rom.append(0)
                    self.__write_bit(b)
                elif b == 1 and b_neg == 1:
                    raise NoDevicesParticipatingInSearch()
            roms.append(current_rom)

            if first_run:
                first_run = False
        if alarm:
            return [DS18B20(rom) for rom in roms]
        else:
            for rom in roms:
                self.__add_device(rom)
            return self.__devices

    def get_devices(self) -> List[DS18B20]:
        """
        Retrieve the list of discovered DS18B20 devices.

        Returns:
            List[DS18B20]: The list of devices.
        """
        return self.__devices

    def read_power_supply(self, n) -> int:
        """
        Read the power supply mode of a device.

        Args:
            n (int): The index of the device in the internal device list.

        Returns:
            int: The bit value indicating the power supply mode.
        """
        self.__reset()
        self.__(self.__MATCH_ROM)
        self.__write_ROM(n)
        self.__write_byte(self.__READ_POWER_SUPPLY)
        b = self.__read_bit()
        return b

    def write_scratchpad(self, n: int, b3: List[int]) -> None:
        """
        Write to the scratchpad memory of a device.

        Args:
            n (int): The index of the device in the internal device list.
            b3 (List[int]): A list of 3 integers to be written to the scratchpad.

        Raises:
            ValueError: If b3 does not contain exactly 3 integers.
        """
        if len(b3) != 3:
            raise ValueError("List must have 3 integers.")
        self.__reset()
        self.__write_byte(self.__MATCH_ROM)
        self.__write_ROM(n)
        self.__write_byte(self.__WRITE_SCRATCHPAD)
        for byte in b3:
            self.__write_byte(byte)

    def read_scratchpad(self, n: int) -> Tuple[float, int, int, int, int]:
        """
        Read the scratchpad memory of a device and compute related parameters.

        Args:
            n (int): The index of the device in the internal device list.

        Returns:
            Tuple[float, int, int, int, int]: A tuple containing the temperature (T),
            high temperature threshold (TH), low temperature threshold (TL),
            configuration register (CR), and CRC.
        """
        self.__reset()
        self.__write_byte(self.__MATCH_ROM)
        self.__write_ROM(n)
        self.__write_byte(self.__READ_SCRATCHPAD)
        ba = bytearray()
        for i in range(9):
            BYTE = self.__read_byte()
            ba.append(BYTE)
        T = calc_T(*ba[0:2])
        TH, TL = calc_TH_TL(*ba[2:4])
        CR = ba[4]
        CRC = ba[8]
        CRC_calc = CRC8(ba[0:-1])
        if CRC_calc != CRC:
            CRCError(CRC, CRC_calc)
        return T, TH, TL, CR, CRC

    def copy_scratchpad(self, n: int) -> None:
        """
        Copy the scratchpad memory to the device's EEPROM.

        Args:
            n (int): The index of the device in the internal device list.
        """
        self.__reset()
        self.__write_byte(self.__MATCH_ROM)
        self.__write_ROM(n)
        self.__write_byte(self.__COPY_SCRATCHPAD)
        time.sleep(0.010)  # 10 ms

    def recall_E2(self, n: int) -> None:
        """
        Recall the EEPROM data into the device's scratchpad.

        Args:
            n (int): The index of the device in the internal device list.
        """
        self.__reset()
        self.__write_byte(self.__MATCH_ROM)
        self.__write_ROM(n)
        self.__write_byte(self.__RECALL_E2)

    def set_precision(self, n: int, CR: int) -> None:
        """
        Set the precision (configuration register) of a device.

        Args:
            n (int): The index of the device in the internal device list.
            CR (int): The configuration register value representing the precision.

        Raises:
            ValueError: If CR is not a valid precision mode.
        """
        if CR not in DS18B20.CR_MODES:
            raise ValueError("No such precision mode!")
        T, TH, TL, _, CRC = self.read_scratchpad(n)
        self.write_scratchpad(n, [TH, TL, CR])

    def set_alarm(self, n: int, TH: int, TL: int) -> None:
        """
        Set the alarm thresholds for a device.

        Args:
            n (int): The index of the device in the internal device list.
            TH (int): The high temperature alarm threshold.
            TL (int): The low temperature alarm threshold.
        """
        T, _, _, CR, CRC = self.read_scratchpad(n)
        self.write_scratchpad(n, [TH, TL, CR])

    def read_temperature(self, n: int) -> float:
        """
        Read the temperature from a device.

        Args:
            n (int): The index of the device in the internal device list.

        Returns:
            float: The measured temperature.
        """
        self.__reset()
        self.__write_byte(self.__MATCH_ROM)
        self.__write_ROM(n)
        self.__write_byte(self.__CONVERT_T)
        while True:
            time.sleep(0.05)
            if self.__read_bit():
                break
        self.__reset()
        self.__write_byte(self.__MATCH_ROM)
        self.__write_ROM(n)
        self.__write_byte(self.__READ_SCRATCHPAD)
        T_LSB = self.__read_byte()
        T_MSB = self.__read_byte()
        T = calc_T(T_LSB, T_MSB)
        return T


if __name__ == "__main__":
    usb_therm = USBThermometer("/dev/ttyUSB0")
    usb_therm.discover_ROMs(alarm=False)
    usb_therm.set_precision(0, DS18B20.CR_12BIT)
    
    
    # usb_therm.set_alarm(0, 125, -50)
    # usb_therm.set_alarm(1, 125, -50)
    # usb_therm.copy_scratchpad(0)
    # usb_therm.copy_scratchpad(1)

    # usb_therm.discover_ROMs(alarm=True)
    # print(usb_therm.get_devices())
    # print(usb_therm.read_scratchpad(0))
    # print(usb_therm.read_scratchpad(1))

    """
    devices = usb_therm.get_devices()
    print("Discovered devices:")
    for i, device in enumerate(devices):
        print(f"  Sensor {i}: {device} ")


    # print(usb_therm.read_scratchpad(0))
    # print(usb_therm.read_scratchpad(1))

    # print(devices[0].get_ROM_bit_list())
    # print(devices[0].get_ROM_bytes())
    # print(devices[0].get_CRC())
    usb_therm.set_precision(0, DS18B20.CR_12BIT)

    print("-"*40)
    while True:
        for i in range(len(devices)):
            T = usb_therm.read_temperature(i)
            print(f"Sensor {i}: {T:3.2f}°C")
        time.sleep(2)
    """
