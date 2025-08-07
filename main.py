from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import re, logging, traceback, os

app = FastAPI()

# ─── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                       # CRA dev server
        "https://robotic-chess-frontend.onrender.com",  # old prod frontend
        "https://robotic-chessboard.onrender.com",      # new prod domain
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
# ────────────────────────────────────────────────────────────────────────────────

# Serial port mapping
ROBOT_PORTS = {"white": "/dev/ttyUSB0", "black": "/dev/ttyUSB1"}

MOVE_REGEX = re.compile(r"^[a-h][1-8]$")

class Move(BaseModel):
    from_square: str
    to_square:   str

# --- Health check ---
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# --- API endpoints ---
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

# ─── Serve React build ─────────────────────────────────────────────────────────
# 1) Mount any static assets under /static
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

# 2) Catch-all route to return index.html (so React Router works)
@app.get("/{full_path:path}")
async def spa(full_path: str):
    index_path = os.path.join("static", "index.html")
    return FileResponse(index_path)
# ────────────────────────────────────────────────────────────────────────────────
