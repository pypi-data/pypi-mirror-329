"""
Author: Electromake
Website: https://electromake.pl/

Module for utility functions related to bit manipulation and sensor data processing.
"""

from typing import List, Tuple


def bit_list2hex_str(bit_arr: List[int]) -> str:
    """
    Convert a list of 64 bits into its corresponding hexadecimal string representation.

    Args:
        bit_arr (List[int]): A list of 64 integers (0 or 1) representing the bits.

    Raises:
        ValueError: If the input list does not contain exactly 64 elements.

    Returns:
        str: The hexadecimal string representation of the bit list.
    """
    if len(bit_arr) != 64:
        raise ValueError("Input list must have 64 elements.")
    byte_arr = []
    for i in range(0, 64, 8):
        BYTE = 0
        for b in reversed(bit_arr[i:i+8]):
            BYTE <<= 1
            BYTE += b
        byte_arr.append("{:02X}".format(BYTE))
    s = "".join(byte_arr)
    return s


def calc_T(T_LSB: int, T_MSB: int) -> float:
    """
    Calculate the temperature in degrees Celsius from the least and most significant bytes.

    Args:
        T_LSB (int): The least significant byte of the temperature reading.
        T_MSB (int): The most significant byte of the temperature reading.

    Returns:
        float: The calculated temperature in degrees Celsius.
    """
    T = (T_MSB << 8) | T_LSB
    if T & 0x8000:
        T -= 0x10000
    T /= 16.0
    return T


def calc_TH_TL(TH_reg: int, TL_reg: int) -> Tuple[int, int]:
    """
    Calculate the high and low temperature thresholds from their register values.

    Args:
        TH_reg (int): The high temperature register value.
        TL_reg (int): The low temperature register value.

    Returns:
        Tuple[int, int]: A tuple containing the high threshold (TH) and low threshold (TL).
    """
    TH, TL = TH_reg, TL_reg
    TH = TH - 256 if TH > 127 else TH
    TL = TL - 256 if TL > 127 else TL
    return TH, TL


def bitlist2bytearray(bit_list: List[int]) -> bytearray:
    """
    Convert a list of 64 bits into a bytearray.

    Args:
        bit_list (List[int]): A list of 64 integers (0 or 1) representing the bits.

    Raises:
        ValueError: If the input list does not contain exactly 64 elements.

    Returns:
        bytearray: The bytearray representation of the bit list.
    """
    if len(bit_list) != 64:
        raise ValueError("Input list must have 64 elements.")
    ba = bytearray()
    for i in range(0, 64, 8):
        eigth_bits = bit_list[i:i+8]
        BYTE = 0
        for b in reversed(eigth_bits):
            BYTE <<= 1
            BYTE += b
        ba.append(BYTE)
    return ba


def CRC8(data: bytearray) -> int:
    """
    Calculate the 8-bit CRC (Cyclic Redundancy Check) for the provided data.

    Args:
        data (bytearray): A bytearray containing the data over which to compute the CRC.

    Returns:
        int: The calculated 8-bit CRC value.
    """
    CRC = 0
    for byte in data:
        for i in range(0, 8):
            b = byte & 1
            in_xor_neg = ((CRC & 1) ^ b) - 1  # 0x00 or 0xFF
            CRC >>= 1
            CRC = ((CRC ^ 0x8C) & ~in_xor_neg) | CRC & in_xor_neg
            byte >>= 1
    return CRC
