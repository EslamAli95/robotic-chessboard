from serial.tools import list_ports
import serial
import numpy as np
import chess
import chess.svg
import webbrowser
# import tempfile
# import os
import berserk

###                         Setting up the arrays and the serial Commnuication                            ###

# Initialise the board
board = chess.Board()

# Initialize Lichess client with API token
API_TOKEN = "lip_FAySoEazSWRJUqXUrbGh"  # My Token for ChessRobotHSRW Account
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session)

# Generating a Game and Retrieving the ID
challenge = client.challenges.create_ai(level=1, clock_limit=300, clock_increment=2, color = "white")
game_id = challenge['id']
webbrowser.open('https://lichess.org/'+game_id)

# Set up Data Arrays
grid_size = (8,8)
data_arr = np.zeros(grid_size) #Analogue Data 
current_state =  np.zeros(grid_size) 
# original_board = np.array([
#     ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
#     ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
#     ['.', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '.', '.', '.', '.', '.'],
#     ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
#     ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
# ])
original_board = np.array([
    [-85, -65, -75, -95, -105, -75, -65, -85],
    [-55,-55,-55,-55,-55,-55,-55,-55],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [55,55,55,55,55,55,55,55],
    [85, 65, 75, 95, 105, 75, 65, 85]
])

previous_state = original_board

f = 0

# Identify the correct port and Open the Serial Com
ports = list_ports.comports()
for port in ports: print(port)
serialCom = serial.Serial('COM3',115200)

###                                     Defining our functions                                ###

# Function to convert an array of data to chess board array
# def array_to_chessboard(data_arr):
#     global original_board
#     chess_state = original_board
#     for r in range(grid_size[0]) :
#         for c in range(grid_size[1]) :
#             if (data_arr[r,c] > 0) :                                
#                 if (data_arr[r,c] > 100) :
#                     chess_state[r][c] = 'K'
#                 elif (data_arr[r,c] > 90) :
#                     chess_state[r][c] = 'Q'
#                 elif (data_arr[r,c] > 80) :
#                     chess_state[r][c] = 'R'
#                 elif (data_arr[r,c] > 70) :
#                     chess_state[r][c] = 'B'
#                 elif (data_arr[r,c] > 60) :
#                     chess_state[r][c] = 'N'
#                 elif (data_arr[r,c] > 50) : 
#                     chess_state[r][c] = 'P'
#                 else :
#                     chess_state[r][c] = '.'
#             else : 
#                 if (abs(data_arr[r,c]) > 100) :
#                     chess_state[r][c] = 'k'
#                 elif (abs(data_arr[r,c]) > 90) :
#                     chess_state[r][c] = 'q'
#                 elif (abs(data_arr[r,c]) > 80) :
#                     chess_state[r][c] = 'r'
#                 elif (abs(data_arr[r,c]) > 70) :
#                     chess_state[r][c] = 'b'
#                 elif (abs(data_arr[r,c]) > 60) :
#                     chess_state[r][c] = 'n'
#                 elif (abs(data_arr[r,c]) > 50) :
#                     chess_state[r][c] = 'p'
#                 else :
#                     chess_state[r][c] = '.'
#     return chess_state

# Function to Update the Data Array from the Arduino
def update_data():
    global data_arr
    global serialCom
    try:
        serialCom.write(b'g')                                     # Transmit the char 'g' to receive the Arduino data point
        line = serialCom.readline().decode('ascii').strip()
        data_values = list(map(int, line.split(' ')))             # Converts the decoded data into integers 
        #print("\n")
        data_arr = np.array(data_values).reshape(grid_size)
        #print(data_arr)
    except:
        print("Error encountered, line was not recorded.")

# Function to Convert from Algebraic Square name to the index of a 2D Array
def algebraic_to_index(square_name):
    square_number = chess.parse_square(square_name)
    file_index = chess.square_file(square_number)  
    rank_index = chess.square_rank(square_number)  
    return (7-rank_index, file_index)

def index_to_algebraic(index):
    square = chess.square(index[1],7-index[0])
    square_name = chess.square_name(square)
    return square_name

# Function to detect Change in Arduino State and Find the Move Made   
def detect_move(previous_state, current_state):
    #Array to store our move
    # Find the indices where the two boards differ
    difference = np.where(previous_state != current_state)
    # There should be exactly two changes: one for the from position and one for the to position
    if len(difference[0]) == 2:
        if (current_state[(difference[0][1], difference[1][1])] == 0):         ### Update in new version
            # Get the from position (the square that became empty)
            from_square = (difference[0][1], difference[1][1])
            # Get the to position (the square that was filled with a new piece)
            to_square = (difference[0][0], difference[1][0])
        else:
            # Get the from position (the square that became empty)
            from_square = (difference[0][0], difference[1][0])
            # Get the to position (the square that was filled with a new piece)
            to_square = (difference[0][1], difference[1][1])

        # Convert array indices to chess algebraic notation
        from_square_algebraic = index_to_algebraic(from_square)
        to_square_algebraic = index_to_algebraic(to_square)
        
        # Identify the type of piece on each square in the previous_state
        # piece_moved = previous_state[from_square]
        # piece_removed = previous_state[to_square]
        
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
                move_san = from_square_algebraic[0] + 'x' + to_square_algebraic
            else:
                move_san = piece_moved.upper() + 'x' + to_square_algebraic
        else: # Just Normal Moves
            if (piece_moved.upper() == 'P'):  # Pawn moves
                move_san = to_square_algebraic
            else :
                move_san = piece_moved.upper() + to_square_algebraic
        return move_san

    elif (len(difference[0]) < 2):
        return ""    
    else:
        serialCom.close()        # Closes the serial port so it doesn't cause issues in the next run
        raise Exception("Multiple moves detected")

# Function to make a move using the Lichess API
def make_lichess_move(game_id, move_uci):
    try:
        client.board.make_move(game_id, move_uci)
        print(f"Move {move_uci} made successfully in game {game_id}.")
    except berserk.exceptions.ResponseError as e:
        serialCom.close()
        raise Exception(f"Failed to make the move: {e}")
        
        
# Function to simulate a move using python-chess and then make the move on Lichess
def play_move_on_lichess(game_id, board, move_san):
    try:
        # Convert SAN (Standard Algebraic Notation) to UCI
        move = board.parse_san(move_san)
        move_uci = move.uci()

        # Make the move on the python-chess board
        board.push(move)
        print(f"Board after {move_san}:")
        print(board)

        # Make the move on Lichess via the API
        make_lichess_move(game_id, move_uci)

    except ValueError:
        serialCom.close()
        raise Exception(f"Invalid move: {move_san}")
        

# Function to stream live moves from a game on Lichess and update the local board
def update_boards(game_id, board):
    global current_state
    try:
        for event in client.board.stream_game_state(game_id):
            if 'moves' in event:
                move_list = event['moves'].split()
                print(move_list)
                board.reset()  # Reset the board to the starting position
                for move in move_list:
                    print(move)
                    board.push(chess.Move.from_uci(move))  # Performs all moves to match LiChess version
                print(f"Board after latest moves from Lichess:\n{board}")
                
                # Convert the last move into indices for the array
                last_move = move_list[-1]
                from_index = algebraic_to_index(last_move[0:2])
                to_index = algebraic_to_index(last_move[2:4])
                
                # Move the piece in current_state array
                current_state[to_index] = current_state[from_index]
                current_state[from_index] = 0  # Change this is updated version
                break
    except Exception as e:
        serialCom.close()
        raise Exception(f"Error streaming moves: {e}")
        
        
# Function to Open PNG of Board after Each Move
# def open_svg_in_browser(svg_data):
#     with tempfile.NamedTemporaryFile('w', delete=False, suffix='.svg') as f:
#         f.write(svg_data)
#         webbrowser.open('file://' + os.path.realpath(f.name))



###                                           Execution                          ###
while True:
    # Read the Data from the Arduino and Store it
    update_data()
    #current_state = array_to_chessboard(data_arr)
    current_state = data_arr
    
    # Compare the current state with the previous state to detect the move made
    move_san = detect_move(previous_state,current_state)
    
    if (move_san != "") :
        # Make the Move on LiChess and Update the Board in PyChess
        play_move_on_lichess(game_id, board, move_san)
        update_boards(game_id, board)
            
    # Updates our previous state
    previous_state = current_state

