# Robotic Chessboard

A full-stack robotic chessboard application featuring:

* **Frontend:** React 18 + TypeScript SPA, built with Vite and styled with Tailwind CSS.
* **Backend:** FastAPI + Pydantic, exposing REST and WebSocket endpoints, with USB-serial communication to chessboard hardware.
* **Controller Module:** `robot_controller.py` abstracts PySerial I/O and supports a mock mode for development without hardware.
* **Persistence:** In-memory state plus JSONL logs for replay and PGN export.
* **Testing & CI/CD:** Jest + React Testing Library on the frontend, pytest + pytest-asyncio on the backend, and a GitHub Actions workflow.

---

## Repository Structure

```
robotic-chess-backend/       # Backend project folder\ n├── main.py               # FastAPI entrypoint
├── models.py             # Pydantic schemas
├── robot_controller.py   # Serial I/O and mock logic
├── logs/                 # JSONL game logs
├── requirements.txt      # Python dependencies
├── venv/                 # (Optional) Python virtual environment
└── robotic-chess-ui/     # Frontend React app
    ├── package.json
    ├── src/
    ├── public/
    └── ...
```

## Prerequisites

* **Python 3.9+**
* **Node.js 18+** and **npm** or **yarn**
* (Optional) A physical robotic chessboard connected via USB to your machine.

## Backend Setup

1. **Create & activate a virtual environment** (if not included):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install --break-system-packages --user -r requirements.txt
   ```

3. **Environment variables** (optional):

   ```bash
   export ROBOT_PORT_ALPHA=/dev/ttyUSB0
   ```

4. **Run the server**:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Frontend Setup

1. **Navigate to the UI folder**:

   ```bash
   cd robotic-chess-ui
   ```

2. **Install packages** (npm or yarn):

   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the dev server**:

   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Build for production**:

   ```bash
   npm run build
   ```

##🚀 Live Deployments

Service

URL

Backend (FastAPI API)

https://robotic-chess-backend.onrender.com

Frontend (React SPA)

https://robotic-chess-frontend.onrender.com

You can find and copy these URLs from your Render dashboard under each service’s overview page.



## Testing

* **Backend**:

  ```bash
  pytest
  ```

* **Frontend**:

  ```bash
  cd robotic-chess-ui
  npm test
  # or
  yarn test
  ```

## CI/CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on push and pull requests:

* Checks out code
* Installs Python & Node
* Runs backend tests
* Runs frontend tests

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes & push: `git push origin feature/your-feature`.
4. Open a Pull Request.

## License

MIT © Eslam Ahmed Adly Yassin Ali
