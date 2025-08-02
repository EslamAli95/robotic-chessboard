import chess
import berserk

# Initialize Lichess client with API token
API_TOKEN = "lip_FAySoEazSWRJUqXUrbGh"
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session)

# Example: Replace with an actual ongoing Lichess game ID where you are a participant
game_id = "VXYe36Dcqih4"

# Function to make a move using the Lichess API
def make_lichess_move(game_id, move_uci):
    try:
        client.board.make_move(game_id, move_uci)
        print(f"Move {move_uci} made successfully in game {game_id}.")
    except berserk.exceptions.ResponseError as e:
        print(f"Failed to make the move: {e}")

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
        print(f"Invalid move: {move_san}")

# Function to stream live moves from a game on Lichess and update the local board
def update_board_with_lichess_moves(game_id, board):
    try:
        for event in client.board.stream_game_state(game_id):
            if 'moves' in event:
                move_list = event['moves'].split()
                board.reset()  # Reset the board to the starting position
                for move in move_list:
                    board.push(chess.Move.from_uci(move))
                print(f"Board after latest moves from Lichess:\n{board}")
    except Exception as e:
        print(f"Error streaming moves: {e}")





# Initialize the python-chess board (start with the standard opening position)
board = chess.Board()

# Example: Let's move white pawn from e2 to e4
move_san = "Nf3"  # Standard Algebraic Notation for the move
play_move_on_lichess(game_id, board, move_san)

# Call this function to sync the python-chess board with Lichess before making a move
update_board_with_lichess_moves(game_id, board)
