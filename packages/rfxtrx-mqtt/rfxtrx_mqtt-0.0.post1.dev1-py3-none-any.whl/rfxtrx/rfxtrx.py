import serial
import time
import binascii

# Define known packet types
PACKET_TYPES = {
    "0x10": "Lighting1",
    "0x11": "Lighting2",
    "0x52": "TemperatureHumidity",
    "0x20": "Security",
    "0x1A": "Blinds"
}

# Define Lighting1 (ARC, X10) subtypes
LIGHTING1_SUBTYPES = {
    "0x00": "X10",
    "0x01": "ARC",
    "0x02": "ELRO",
    "0x03": "KlikAanKlikUit",
    "0x04": "Chacon"
}

# Define known Lighting1 commands
LIGHTING1_COMMANDS = {
    "00": "Off",
    "01": "On",
    "02": "Dim",
    "03": "Bright",
    "04": "Group Off",
    "05": "Group On"
}

class RFXtrx:
    """
    A class to interface with the RFXtrx device for reading and parsing data.
    """
    def __init__(self, device="/dev/ttyUSB0", baudrate=38400, timeout=1, readsize=16, callback=None):
        """
        Initialize the RFXtrx class.
        :param device: Serial port device path
        :param baudrate: Baud rate for serial communication
        :param timeout: Timeout for reading serial data
        :param readsize: Number of bytes to read at a time
        :param callback: Function to call with parsed data
        """
        self.device = device
        self.baudrate = baudrate
        self.timeout = timeout
        self.readsize = readsize
        self.callback = callback  # Function to handle received data
        self.serial_conn = None

    def parse_data(self, data):
        """
        Convert raw RFXtrx binary data into a JSON structure.
        :param data: Raw binary data from RFXtrx
        :return: JSON object containing parsed data
        """
        hex_data = binascii.hexlify(data).decode("utf-8")  # Convert binary to hex
        packet_type = f"0x{hex_data[2:4]}" if len(data) >= 2 else "Unknown"

        parsed_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "raw_data": hex_data,
            "packet_type": PACKET_TYPES.get(packet_type, "Unknown")
        }

        # Decode Lighting1 (X10, ARC, KlikAanKlikUit)
        if packet_type == "0x10" and len(data) >= 8:
            subtype = f"0x{hex_data[4:6]}"
            device_id = f"{hex_data[6:8]}{hex_data[8:10]}"  # Device ID (hex)
            unit_code = int(hex_data[10:12], 16)  # Convert unit code to int
            command = hex_data[12:14]  # Command byte

            parsed_data["subtype"] = LIGHTING1_SUBTYPES.get(subtype, "Unknown")
            parsed_data["device_id"] = device_id
            parsed_data["unit_code"] = unit_code
            parsed_data["command"] = LIGHTING1_COMMANDS.get(command, "Unknown")

        return parsed_data

    def start(self):
        """
        Start reading data from the RFXtrx device.
        """
        try:
            self.serial_conn = serial.Serial(self.device, self.baudrate, timeout=self.timeout)
            print(f"Listening on {self.device} at {self.baudrate} baud...")

            while True:
                raw_data = self.serial_conn.read(self.readsize)  # Read bytes from serial
                if raw_data:
                    parsed_data = self.parse_data(raw_data)
                    if self.callback:
                        self.callback(parsed_data)  # Send data to callback function

        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()
