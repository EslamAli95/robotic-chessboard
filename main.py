from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from robot_controller import send_move_to_robot, get_last_detected_move
import re, logging, traceback, os

app = FastAPI()

# ─── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # adjust to specific domains if you like
    allow_methods=["*"],
    allow_headers=["*"],
)
# ────────────────────────────────────────────────────────────────────────────────

# Serial ports mapping
ROBOT_PORTS = {
    "white": "/dev/ttyUSB0",
    "black": "/dev/ttyUSB1",
}

# Health check
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# Regex for chess notation
MOVE_REGEX = re.compile(r"^[a-h][1-8]$")

# --- Data Model ---
class Move(BaseModel):
    from_square: str
    to_square:   str

# --- POST /make-move ---
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

# --- GET /latest-move ---
@app.get("/robots/{robot_id}/latest-move")
def latest_move(robot_id: str):
    port = ROBOT_PORTS.get(robot_id)
    if not port:
        raise HTTPException(404, f"Unknown robot '{robot_id}'")
    mv = get_last_detected_move(port)
    return mv or {"status": "waiting"}

# ─── Static Files & SPA Fallback ────────────────────────────────────────────────
# serve files under ./static
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # any other GET path not matched above should serve index.html
    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_fallback(full_path: str, request: Request):
        index_file = os.path.join("static", "index.html")
        if os.path.isfile(index_file):
            return FileResponse(index_file)
        raise HTTPException(404, "Not Found")
# ────────────────────────────────────────────────────────────────────────────────
