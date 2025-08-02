import serial
import time

# Create a virtual serial port
ser = serial.Serial('COM1', 9600)
time.sleep(10)
# Define the 8x8 matrix
matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# Send the start signal
ser.write(b'<START>\n')

# Send the matrix over the serial port
for row in matrix:
    row_str = ' '.join(str(value) for value in row)
    ser.write(row_str.encode())
    ser.write(b'\n')

# Send the end signal
ser.write(b'<END>\n')

# Modify the matrix
matrix[1][1] = 0
matrix[1][2] = 1
time.sleep(5)
# Send the start signal
ser.write(b'<START>\n')

# Send the modified matrix over the serial port
for row in matrix:
    row_str = ' '.join(str(value) for value in row)
    ser.write(row_str.encode())
    ser.write(b'\n')

# Send the end signal
ser.write(b'<END>\n')

# Close the serial port
ser.close()
