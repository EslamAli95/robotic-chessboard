import numpy as np
import chess
import time
import serial
import chess.svg
import webbrowser
import tempfile
import os


board = chess.Board()

# Initialize the matrix to represent the initial state of the board
previous_state = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
])

f = 0

# Initialize the serial connection
try:
    ser = serial.Serial('COM3', 115200)
except serial.SerialException:
    ser = None

def read_matrix():
    matrix = []
    if ser is not None:
        reading = False
        while True:
            line = ser.readline().decode().strip()
            if "<START>" in line:
                reading = True
                continue
            if "<END>" in line:
                break
            if reading:
                row = [int(x) for x in line.split()]
                # Convert each value in the row to 1 if it's >= 20 or <= -20, and to 0 otherwise
                row = [1 if abs(x) >= 20 else 0 for x in row]
                matrix.append(row)
    return matrix

def detect_changes(previous_state, current_state):
    # Compare the current state with the previous state to detect changes
    changes = np.where(previous_state != current_state)
    return list(zip(changes[0], changes[1]))

def convert_to_chess_notation(changes):

    moves = []
    for change in changes:
        row, col = change
        if 0 <= row < previous_state.shape[0] and 0 <= col < previous_state.shape[1]:
            # Convert the row to the chess library's coordinate system
            chess_row = 7 - row
            # Calculate the square number
            square = chess_row * 8 + col
            if previous_state[row, col] == 1 and current_state[row, col] == 0:
                print(f'Piece captured at {chess.SQUARE_NAMES[square]}')
                moves.append(f'{chess.SQUARE_NAMES[square]}')
            elif previous_state[row, col] == 0 and current_state[row, col] == 1:
                print(f'Piece moved to {chess.SQUARE_NAMES[square]}')
                moves.append(f'{chess.SQUARE_NAMES[square]}')
    return moves

def open_svg_in_browser(svg_data):
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.svg') as f:
        f.write(svg_data)
        webbrowser.open('file://' + os.path.realpath(f.name))


while True:
    
    matrix= read_matrix()
    current_state = np.array(matrix)
    #print(current_state)
    # Detect changes
    changes = detect_changes(previous_state, current_state)
    
    moves = convert_to_chess_notation(changes)

    # Update the board
    for move in moves:
        try:
            board.push_san(move)
            print(board) # Print the board
            print("\n")
            # Print the FEN notation
            print("FEN notation: ", board.fen())
            board_svg = chess.svg.board(board)
            open_svg_in_browser(board_svg)
        except ValueError:
            print(f'Invalid move: {move}')

    
    

    # Update the previous state
    previous_state = current_state

 