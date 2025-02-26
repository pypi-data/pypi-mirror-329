#!/usr/bin/env python3
import argparse
import json
from rfxtrx.rfxtrx import RFXtrx

def print_callback(data):
    """
    Callback function to print received RFXtrx data.
    """
    print(json.dumps(data, indent=4))

def main():
    parser = argparse.ArgumentParser(description="Read and decode RFXtrx data from a serial device and print to console.")
    parser.add_argument("-d", "--device", type=str, default="/dev/ttyUSB0", help="Serial device path (default: /dev/ttyUSB0)")
    parser.add_argument("-b", "--baudrate", type=int, default=38400, help="Baud rate (default: 38400)")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout in seconds (default: 1)")
    parser.add_argument("-r", "--readsize", type=int, default=16, help="Number of bytes to read at a time (default: 16)")

    args = parser.parse_args()

    # Start the RFXtrx reader with print callback
    rfxtrx = RFXtrx(device=args.device, baudrate=args.baudrate, timeout=args.timeout, readsize=args.readsize, callback=print_callback)
    rfxtrx.start()

if __name__ == "__main__":
    main()
