# Py_Chessv3/SerialReading.py
# Cleaned-up module to safely read sensor data via serial.

import serial
import platform
import time
import numpy as np
from typing import Optional, Tuple

# Determine default serial port based on OS
if platform.system() == "Windows":
    DEFAULT_PORT = "COM3"
else:
    DEFAULT_PORT = "/dev/ttyUSB0"  # adjust as needed for your system

BAUD_RATE = 115200
TIMEOUT = 1  # seconds


def read_array(port: Optional[str] = None, grid_size: Tuple[int, int] = (4, 4)) -> np.ndarray:
    """
    Reads a grid of integers from the Arduino board via serial.
    Sends 'g' to request data and parses the space-separated response.
    Returns a zero-filled array on error or no data.
    """
    use_port = port or DEFAULT_PORT
    try:
        with serial.Serial(use_port, BAUD_RATE, timeout=TIMEOUT) as ser:
            time.sleep(0.1)  # allow connection to settle
            ser.write(b'g')  # request data
            line = ser.readline().decode('ascii').strip()
            if not line:
                return np.zeros(grid_size, dtype=int)
            values = list(map(int, line.split()))
            return np.array(values, dtype=int).reshape(grid_size)
    except serial.SerialException as e:
        print(f"Serial read error on port {use_port}: {e}")
        return np.zeros(grid_size, dtype=int)


if __name__ == "__main__":
    # Demo loop
    while True:
        try:
            grid = read_array()
            print("Sensor Grid:\n", grid)
            time.sleep(2)
        except KeyboardInterrupt:
            print("Interrupted by user, exiting.")
            break
