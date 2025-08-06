from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from robot_controller import send_move_to_robot, get_last_detected_move
import re, logging, traceback, os
from dotenv import load_dotenv
load_dotenv()

MOCK_MODE = os.getenv("ROBOT_MOCK", "false").lower() in ("1", "true", "yes")

app = FastAPI()

# ─── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://robotic-chess-frontend.onrender.com",],   
    allow_methods=["*"],
    allow_headers=["*"],
)
# ────────────────────────────────────────────────────────────────────────────────

# Serial port mapping
ROBOT_PORTS = {"white": "/dev/ttyUSB0", "black": "/dev/ttyUSB1"}

# Health check & API routes
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

MOVE_REGEX = re.compile(r"^[a-h][1-8]$")

class Move(BaseModel):
    from_square: str
    to_square:   str

@app.post("/robots/{robot_id}/make-move")
def make_move(robot_id: str, move: Move):
    if not (MOVE_REGEX.match(move.from_square) and MOVE_REGEX.match(move.to_square)):
        raise HTTPException(400, "Invalid square notation")
    port = ROBOT_PORTS.get(robot_id)
    if not port:
        raise HTTPException(404, f"Unknown robot '{robot_id}'")
    try:
        ok = send_move_to_robot(move.from_square, move.to_square, port)
    except Exception:
        logging.getLogger("robot_controller").error(traceback.format_exc())
        raise HTTPException(500, "Error sending move")
    if not ok:
        raise HTTPException(500, "Failed to send move")
    return {"status": "success"}

@app.get("/robots/{robot_id}/latest-move")
def latest_move(robot_id: str):
    port = ROBOT_PORTS.get(robot_id)
    if not port:
        raise HTTPException(404, f"Unknown robot '{robot_id}'")
    mv = get_last_detected_move(port)
    return mv or {"status": "waiting"}

# ─── Serve your React app ──────────────────────────────────────────────────────
# 1️⃣ First check that `static/index.html` exists
spa_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(spa_dir) and os.path.isfile(os.path.join(spa_dir, "index.html")):
    # 2️⃣ Mount all static assets under `/`
    app.mount(
        "/", 
        StaticFiles(directory=spa_dir, html=True),
        name="spa",
    )
# ────────────────────────────────────────────────────────────────────────────────
