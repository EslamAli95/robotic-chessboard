# Py_Chessv3/SerialSending.py

import serial
import platform
import time
from typing import Optional, List

# Determine default serial port based on OS
if platform.system() == "Windows":
    DEFAULT_PORT = "COM3"
else:
    DEFAULT_PORT = "/dev/ttyUSB0"  # adjust as needed

BAUD_RATE = 9600
TIMEOUT = 1  # seconds

def read_array(port: Optional[str] = None) -> List[int]:
    """
    Reads an array of integers sent by the Arduino board.
    Sends an optional 'READ' command, then parses the comma-separated response.
    Returns an empty list on failure or no data.
    """
    use_port = port or DEFAULT_PORT
    try:
        with serial.Serial(use_port, BAUD_RATE, timeout=TIMEOUT) as ser:
            ser.write(b'READ\n')
            time.sleep(0.1)
            data = ser.readline().decode('utf-8').strip()
            if not data:
                return []
            return list(map(int, data.split(',')))
    except serial.SerialException as e:
        print(f"Serial read error on port {use_port}: {e}")
        return []

def modify_array(array: List[int]) -> List[int]:
    """
    Example processing: increase each element by 10.
    """
    return [x + 10 for x in array]

def send_array(array: List[int], port: Optional[str] = None) -> bool:
    """
    Sends a list of integers back to the Arduino board as a comma-separated string.
    Returns True on success, False on failure.
    """
    use_port = port or DEFAULT_PORT
    data_str = ','.join(map(str, array)) + '\n'
    try:
        with serial.Serial(use_port, BAUD_RATE, timeout=TIMEOUT) as ser:
            ser.write(data_str.encode('utf-8'))
        return True
    except serial.SerialException as e:
        print(f"Serial write error on port {use_port}: {e}")
        return False

if __name__ == "__main__":
    # Demo loop
    while True:
        try:
            original = read_array()
            print(f"Original Array: {original}")
            modified = modify_array(original)
            print(f"Modified Array: {modified}")
            sent = send_array(modified)
            print(f"Sent successfully: {sent}")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Interrupted by user, exiting...")
            break
