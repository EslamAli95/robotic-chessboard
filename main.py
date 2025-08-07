from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import re, logging, traceback

app = FastAPI()

# ─── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://robotic-chess-frontend.onrender.com",
        "https://robotic-chessboard.onrender.com",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
# ────────────────────────────────────────────────────────────────────────────────

# Serial port mapping & validation
ROBOT_PORTS = {"white": "/dev/ttyUSB0", "black": "/dev/ttyUSB1"}
MOVE_REGEX   = re.compile(r"^[a-h][1-8]$")

class Move(BaseModel):
    from_square: str
    to_square:   str

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/robots/{robot_id}/make-move")
def make_move(robot_id: str, move: Move):
    if not (MOVE_REGEX.match(move.from_square) and MOVE_REGEX.match(move.to_square)):
        raise HTTPException(400, "Invalid square notation")
    port = ROBOT_PORTS.get(robot_id)
    if not port:
        raise HTTPException(404, f"Unknown robot '{robot_id}'")
    try:
        ok = __import__("robot_controller").send_move_to_robot(
            move.from_square, move.to_square, port
        )
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
    mv = __import__("robot_controller").get_last_detected_move(port)
    return mv or {"status": "waiting"}

# ─── Serve the React build & SPA fallback ──────────────────────────────────────
# This single mount will:
#   • serve /index.html
#   • serve /manifest.json, /favicon.ico, /robots.txt, /static/*, etc.
#   • fall back to index.html for any other path
app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="spa",
)
# ────────────────────────────────────────────────────────────────────────────────
