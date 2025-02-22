class DevicePresenceNotDetected(Exception):
    def __str__(self):
        return f"No device found on 1-Wire bus."


class NoDevicesParticipatingInSearch(Exception):
    def __str__(self):
        return f"No devices participating in search."


class CRCError(Exception):
    def __init__(self, CRC_received, CRC_calculated):
        super().__init__(
            f"Received data is corrupted. Received CRC 0x{CRC_received:02X}. Calculated CRC 0x{CRC_calculated:02X}."
        )
