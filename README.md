# Robotic Chessboard

A full-stack framework for a cloud-enabled, physical chessboard with a React/TypeScript frontend and a FastAPI/Python backend driving serial communication with a chess-playing robot.

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)

  * [Backend](#backend)
  * [Frontend](#frontend)
* [Development Workflow](#development-workflow)
* [Testing](#testing)
* [Deployment](#deployment)
* [Project Structure](#project-structure)
* [License](#license)

## Features

* **Interactive SPA**: Real-time chessboard UI with drag-and-drop moves, move history, and timer support.
* **FastAPI Backend**: REST and WebSocket endpoints for move submission, history retrieval, and live updates.
* **Serial Communication**: Asynchronous USB-serial protocol to interface with the physical chess robot.
* **Mock Mode**: Run and test the full UI without hardware by toggling a mock flag.
* **Persistence**: In-memory and JSONL logging with replay capability and PGN export.
* **Testing & CI/CD**: Comprehensive unit, integration, and end-to-end tests with GitHub Actions.

## Prerequisites

* Python 3.9+
* Node.js 18+
* Yarn or npm
* USB access for the robot controller (optional if using mock mode)

## Getting Started

### Backend

1. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   ```bash
   export ROBOT_PORT=/dev/ttyUSB0
   export MOCK=true      # set to false to use real hardware
   ```

4. Run the server:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Explore API docs:

   * Swagger UI: `http://localhost:8000/docs`
   * ReDoc: `http://localhost:8000/redoc`

### Frontend

1. Navigate to the `robotic-chess-ui` directory:

   ```bash
   cd robotic-chess-ui
   ```

2. Install dependencies:

   ```bash
   yarn install
   # or npm install
   ```

3. Start the development server:

   ```bash
   yarn dev
   # or npm run dev
   ```

4. Open the app in your browser:
   `http://localhost:5173`

## Development Workflow

* **Backend**: Python, FastAPI, Pydantic models, PySerial for I/O.
* **Frontend**: React 18, TypeScript, Vite, Tailwind CSS.
* **Mock Mode**: Develop UI without hardware by enabling `MOCK=true`.
* **Logging**: View move logs in `logs/{robot_id}.jsonl`.

## Testing

### Backend tests

```bash
pytest
```

### Frontend tests

```bash
yarn test
# or npm run test
```

## Deployment

* Containerize with Docker:

  ```bash
  docker build -t robotic-chess-backend .
  docker run -e MOCK=true -p 8000:8000 robotic-chess-backend
  ```
* Frontend can be built with `yarn build` and served on any static host.

## Project Structure

```
/  
├─ backend/            # FastAPI application  
│  ├─ main.py  
│  ├─ robot_controller.py  
│  ├─ models.py  
│  ├─ logs/  
│  └─ requirements.txt  
├─ robotic-chess-ui/   # React SPA  
│  ├─ src/  
│  └─ package.json  
├─ chapters/           # LaTeX thesis chapters  
├─ figures/            # Diagrams and illustrations  
├─ main.tex            # LaTeX root document  
└─ README.md  
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
