import os
from typing import Optional, List, Tuple, Dict

# Mock mode toggled via environment variable 'MOCK_ROBOT'
MOCK = os.getenv("MOCK_ROBOT", "false").lower() == "true"
print(f"[robot_controller] MOCK mode = {MOCK}")

# Import core serial I/O routines
from Py_Chessv3.SerialSending import read_array as read_string_array, send_array
from Py_Chessv3.SerialReading import read_array as read_sensor_grid

def get_sensor_array(port: Optional[str] = None, grid_size: Tuple[int, int] = (4, 4)) -> List[List[int]]:
    """
    Retrieve the latest sensor grid from the robotic chess board.
    In mock mode, returns a zero-filled grid.
    """
    if MOCK:
        rows, cols = grid_size
        return [[0 for _ in range(cols)] for _ in range(rows)]
    arr = read_sensor_grid(port, grid_size)
    if hasattr(arr, "tolist"):
        return arr.tolist()
    return arr


def send_sensor_array(array: List[int], port: Optional[str] = None) -> bool:
    """
    Send a flat sensor data array back to the board.
    In mock mode, logs and returns True.
    """
    if MOCK:
        print(f"[MOCK] send_sensor_array: {array}")
        return True
    return send_array(array, port)


def send_move_to_robot(from_sq: str, to_sq: str, port: Optional[str] = None) -> bool:
    """
    Send a chess move command to the robotic board.
    In mock mode, logs and returns True.
    In real mode, raises RuntimeError on any failure.
    """
    if MOCK:
        print(f"[MOCK] send_move_to_robot: {from_sq}-{to_sq}")
        return True

    move_str = f"{from_sq}-{to_sq}"
    # Attempt to send; wrap any exceptions
    try:
        ok = send_array([move_str], port)
    except Exception as e:
        # Serial I/O or protocol error
        raise RuntimeError(f"Error sending move '{move_str}': {e}")

    if not ok:
        # send_array succeeded without exception but indicated failure
        raise RuntimeError(f"Robot did not acknowledge move '{move_str}'")

    return True


def get_last_detected_move(port: Optional[str] = None) -> Optional[Dict[str, str]]:
    """
    Read the last detected chess move from the board sensors.
    In mock mode, returns None.
    """
    if MOCK:
        return None
    raw_list = read_string_array(port)
    if not raw_list:
        return None
    try:
        from_sq, to_sq = raw_list[0].split("-")
        return {"from_square": from_sq, "to_square": to_sq}
    except Exception:
        return None
