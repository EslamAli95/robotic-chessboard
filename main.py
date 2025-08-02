from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from robot_controller import send_move_to_robot, get_last_detected_move
from fastapi.middleware.cors import CORSMiddleware
import re
import logging, traceback  

  

app = FastAPI()
ROBOT_PORTS = {
     "white": "/dev/ttyUSB0",
     "black": "/dev/ttyUSB1",
 }

# Enable CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Regex to validate chess square notation (a-h followed by 1-8)
MOVE_REGEX = re.compile(r"^[a-h][1-8]$")

# --- Data Models ---
class Move(BaseModel):
    from_square: str  # e.g., "e2"
    to_square: str    # e.g., "e4"

# --- POST /make-move Endpoint ---
@app.post("/robots/{robot_id}/make-move")
def make_move(robot_id: str,move: Move):
    # Validate chess notation
    if not (MOVE_REGEX.match(move.from_square) and MOVE_REGEX.match(move.to_square)):
        raise HTTPException(
            status_code=400,
            detail="Invalid square notation. Use letters a-h and numbers 1-8, e.g. 'e2', 'g8'."
        )
    port = ROBOT_PORTS.get(robot_id)
    if port is None:
             raise HTTPException(404, f"Unknown robot '{robot_id}'")

    # Send move to robot, catching and logging any exception
    try:
        success = send_move_to_robot(move.from_square, move.to_square, port)

    except Exception as e:
        logging.getLogger("robot_controller").error(traceback.format_exc())
        raise HTTPException(500, str(e))

    if not success:
        raise HTTPException(status_code=500, detail="Failed to send move to robot")

    return {"status": "success", "message": "Move executed"}


# --- GET /latest-move Endpoint ---
@app.get("/robots/{robot_id}/latest-move")
def latest_move(robot_id: str):
    """
    Returns the most recent move detected by the board’s sensors.
    If no move is detected, returns a waiting message.
    """
    # Look up which serial port to use for this robot
    port = ROBOT_PORTS.get(robot_id)
    if port is None:
        raise HTTPException(404, f"Unknown robot '{robot_id}'")

    move = get_last_detected_move(port)
    if move:
        return move
    return {"status": "waiting", "message": "No move detected yet."}

# --- Root Health Check ---
@app.get("/")
def root():
    """
    Simple health check to verify that the API is running.
    """
    return {"message": "Robotic Chess API is running!"}