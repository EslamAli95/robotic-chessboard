# Robotic Chessboard

A full-stack robotic chessboard application featuring:

* **Frontend:** React 18 + TypeScript SPA, built with Create React App and styled with CSS Modules.
* **Backend:** FastAPI + Pydantic, exposing REST and WebSocket endpoints, with USB-serial communication to chessboard hardware.
* **Controller Module:** `robot_controller.py` abstracts PySerial I/O and supports a mock mode via `ROBOT_MOCK=true`.
* **Persistence:** In-memory state plus JSONL logs for audit, replay, and PGN export.
* **Testing & CI/CD:** Jest + React Testing Library on the frontend; pytest + pytest-asyncio on the backend; GitHub Actions workflow.

---

## Repository Structure

```
robotic-chess-backend/          # Root of backend + static-serve for frontend
├── main.py                     # FastAPI entrypoint
├── models.py                   # Pydantic schemas
├── robot_controller.py         # Serial I/O and mock logic
├── logs/                       # JSONL game logs
├── static/                     # Compiled React `build/` output
├── requirements.txt            # Python dependencies
├── venv/                       # (Optional) Python virtual environment
└── robotic-chess-ui/           # Frontend React app (Create React App)
    ├── package.json
    ├── public/
    └── src/
```

---

## Prerequisites

* **Python 3.9+**
* **Node.js 18+**
* **npm** or **yarn**
* (Optional) A physical robotic chessboard connected via USB.

---

## Backend Setup

1. **(Optional) Create & activate venv**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies**

   ```bash
   pip install --break-system-packages --user -r requirements.txt
   ```
3. **Enable mock mode (if no hardware)**

   ```bash
   export ROBOT_MOCK=true
   ```
4. **Run the server**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## Frontend Setup

1. **Enter UI folder**

   ```bash
   cd robotic-chess-ui
   ```
2. **Install packages**

   ```bash
   npm install
   # or
   yarn install
   ```
3. **Start dev server**

   ```bash
   npm start
   # or
   yarn start
   ```
4. **Build for production**

   ```bash
   npm run build
   # or
   yarn build
   ```

---

## Serving the Frontend via the Backend

After building, copy your build artifacts:

```bash
cp -R robotic-chess-ui/build/* static/
```

into `robotic-chess-backend/static/`, then restart FastAPI so it serves the SPA at `/`.

---

## Live Deployments

* **Backend + SPA:** [https://robotic-chessboard.onrender.com](https://robotic-chessboard.onrender.com)
* **Standalone Frontend:** [https://robotic-chess-frontend.onrender.com](https://robotic-chess-frontend.onrender.com)

---

## Testing

* **Backend:**

  ```bash
  pytest
  ```
* **Frontend:**

  ```bash
  cd robotic-chess-ui
  npm test
  # or
  yarn test
  ```

---

## CI/CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs on push/PR:

1. Checks out code
2. Installs Python & Node
3. Runs backend tests
4. Runs frontend tests
5. (Optional) Builds & deploys

---

## Contributing

1. Fork the repo
2. Create a branch:

   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit & push your changes
4. Open a Pull Request

---

## License

MIT © Eslam Ahmed Adly Yassin Ali
