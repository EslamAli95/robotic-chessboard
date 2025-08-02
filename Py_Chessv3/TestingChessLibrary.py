import numpy as np
import chess
import chess.svg
import webbrowser
import tempfile
import os


board = chess.Board()
# Example 8x8 arrays representing the chessboard before and after a move
previous_state = np.array([
  [-85, -65, -75, -95, -105, -75, -65, -85],
  [-55,-55,-55,-55,-55,-55,-55,-55],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [55,55,55,55,55,55,55,55],
  [85, 65, 75, 95, 105, 75, 65, 85]
])

# A move is made: White pawn moves from e2 to e4
current_state = np.array([
  [-85, -65, -75, -95, -105, -75, -65, -85],
  [-55,-55,-55,-55,-55,-55,-55,-55],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 55, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [55,55,55,55,0,55,55,55],
  [85, 65, 75, 95, 105, 75, 65, 85]
])

def detect_move(previous_state, current_state):
    #Array to store our move
    # Find the indices where the two boards differ
    difference = np.where(previous_state != current_state)
    # There should be exactly two changes: one for the from position and one for the to position
    if len(difference[0]) == 2:
        # Get the from position (the square that became empty)
        from_square = (difference[0][1], difference[1][1])
        # Get the to position (the square that was filled with a new piece)
        to_square = (difference[0][0], difference[1][0])

        # Convert array indices to chess algebraic notation
        from_square_algebraic = chess.square_name(chess.square(from_square[1], 7 - from_square[0]))
        to_square_algebraic = chess.square_name(chess.square(to_square[1], 7 - to_square[0]))
        
        # Identify the type of piece on each square in the previous_state
        if (previous_state[from_square] > 0) :                                  # The piece that moved
            if (previous_state[from_square] > 100) :
                piece_moved = 'K'
            elif (previous_state[from_square] > 90) :
                piece_moved = 'Q'
            elif (previous_state[from_square] > 80) :
                piece_moved = 'R'
            elif (previous_state[from_square] > 70) :
                piece_moved = 'B'
            elif (previous_state[from_square] > 60) :
                piece_moved = 'N'
            elif (previous_state[from_square] > 50) :
                piece_moved = 'P'
            else :
                piece_moved = '.'
        else : 
            if (abs(previous_state[from_square]) > 100) :
                piece_moved = 'k'
            elif (abs(previous_state[from_square]) > 90) :
                piece_moved = 'q'
            elif (abs(previous_state[from_square]) > 80) :
                piece_moved = 'r'
            elif (abs(previous_state[from_square]) > 70) :
                piece_moved = 'b'
            elif (abs(previous_state[from_square]) > 60) :
                piece_moved = 'n'
            elif (abs(previous_state[from_square]) > 50) :
                piece_moved = 'p'
            else :
                piece_moved = '.'
        
        if (previous_state[to_square] > 0) :                                  # The piece that was there before
            if (previous_state[to_square] > 100) :
                piece_removed = 'K'
            elif (previous_state[to_square] > 90) :
                piece_removed = 'Q'
            elif (previous_state[to_square] > 80) :
                piece_removed = 'R'
            elif (previous_state[to_square] > 70) :
                piece_removed = 'B'
            elif (previous_state[to_square] > 60) :
                piece_removed = 'N'
            elif (previous_state[to_square] > 50) :
                piece_removed = 'P'
            else :
                piece_removed = '.'
        else : 
            if (abs(previous_state[to_square]) > 100) :
                piece_removed = 'k'
            elif (abs(previous_state[to_square]) > 90) :
                piece_removed = 'q'
            elif (abs(previous_state[to_square]) > 80) :
                piece_removed = 'r'
            elif (abs(previous_state[to_square]) > 70) :
                piece_removed = 'b'
            elif (abs(previous_state[to_square]) > 60) :
                piece_removed = 'n'
            elif (abs(previous_state[to_square]) > 50) :
                piece_removed = 'p'
            else :
                piece_removed = '.'
        
        if (piece_removed != '.'): # Capturing 
            if (piece_moved.upper() == 'P'):# Pawn capture 
                move = from_square_algebraic[0] + 'x' + to_square_algebraic
                print(f"{piece_moved} at {from_square_algebraic} captured {piece_removed} at {to_square_algebraic}")
            else:
                move = piece_moved.upper() + 'x' + to_square_algebraic
        else: # Just Normal Moves
            if (piece_moved.upper() == 'P'):# Pawn moves
                move = to_square_algebraic
                print(f"{piece_moved} moved from {from_square_algebraic} to {to_square_algebraic}")
            else :
                move = piece_moved.upper() + to_square_algebraic
                print(f"{piece_moved} moved from {from_square_algebraic} to {to_square_algebraic}")
        return move

    else:
        raise Exception("No valid move detected or multiple moves detected")


def open_svg_in_browser(svg_data):
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.svg') as f:
        f.write(svg_data)
        webbrowser.open('file://' + os.path.realpath(f.name))


move = detect_move(previous_state, current_state)
print(move)
try:
    board.push_san(move)
    print(board)
    print("\n")
    # board_svg = chess.svg.board(board)
    # open_svg_in_browser(board_svg)
except:
    print(f'Invalid move: {move}')