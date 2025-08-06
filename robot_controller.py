import os
import logging
from typing import Optional, List, Tuple, Dict

# Mock mode toggled via environment variable 'MOCK_ROBOT'
MOCK = os.getenv("ROBOT_MOCK", "false").lower() in ("1","true","yes")
logging.getLogger("robot_controller").info(f"[robot_controller] MOCK mode = {MOCK}")

# Import core serial I/O routines
from Py_Chessv3.SerialSending import read_array as read_string_array, send_array
from Py_Chessv3.SerialReading import read_array as read_sensor_grid


class RobotController:
    def __init__(self, port: Optional[str], mock: bool = MOCK):
        """
        port: serial port path, e.g. '/dev/ttyUSB0'
        mock: if True, simulate hardware
        """
        self.port = port
        self.mock = mock
        self.logger = logging.getLogger("robot_controller")

    def get_sensor_array(
        self, grid_size: Tuple[int, int] = (4, 4)
    ) -> List[List[int]]:
        """
        Retrieve the latest sensor grid from the robotic chess board.
        In mock mode, returns a zero-filled grid.
        """
        if self.mock:
            rows, cols = grid_size
            return [[0 for _ in range(cols)] for _ in range(rows)]

        arr = read_sensor_grid(self.port, grid_size)
        # convert numpy arrays if necessary
        return arr.tolist() if hasattr(arr, "tolist") else arr

    def send_sensor_array(self, array: List[int]) -> bool:
        """
        Send a flat sensor data array back to the board.
        In mock mode, logs and returns True.
        """
        if self.mock:
            self.logger.debug(f"[MOCK] send_sensor_array: {array}")
            return True

        return send_array(array, self.port)

    def make_move(self, from_sq: str, to_sq: str) -> bool:
        """
        Send a chess move command to the robotic board.
        In mock mode, logs and returns True.
        In real mode, raises RuntimeError on any failure.
        """
        if self.mock:
            self.logger.info(f"[MOCK] send_move_to_robot: {from_sq}-{to_sq}")
            return True

        move_str = f"{from_sq}-{to_sq}"
        try:
            ok = send_array([move_str], self.port)
        except Exception as e:
            raise RuntimeError(f"Error sending move '{move_str}': {e}")

        if not ok:
            raise RuntimeError(f"Robot did not acknowledge move '{move_str}'")

        return True

    def latest_move(self) -> Optional[Dict[str, str]]:
        """
        Read the last detected chess move from the board sensors.
        In mock mode, returns None.
        """
        if self.mock:
            return None

        raw_list = read_string_array(self.port)
        if not raw_list:
            return None

        try:
            frm, to = raw_list[0].split("-")
            return {"from_square": frm, "to_square": to}
        except Exception:
            self.logger.warning(f"Could not parse sensor output: {raw_list}")
            return None


# Optional: if you still want top‐level convenience functions, you can alias them:
controller_instances: Dict[str, RobotController] = {}

def get_controller(port: Optional[str]) -> RobotController:
    """
    Returns a singleton RobotController for the given port.
    """
    if port not in controller_instances:
        controller_instances[port] = RobotController(port)
    return controller_instances[port]

def send_move_to_robot(from_sq: str, to_sq: str, port: Optional[str]) -> bool:
    return get_controller(port).make_move(from_sq, to_sq)

def get_last_detected_move(port: Optional[str]) -> Optional[Dict[str, str]]:
    return get_controller(port).latest_move()

def get_sensor_array(port: Optional[str] = None, grid_size: Tuple[int,int]=(4,4)):
    return get_controller(port).get_sensor_array(grid_size)

def send_sensor_array(array: List[int], port: Optional[str] = None):
    return get_controller(port).send_sensor_array(array)
