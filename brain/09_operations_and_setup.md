# 09. Operations, Setup & Troubleshooting

This guide provides step-by-step instructions for installing, configuring, launching, and troubleshooting VideoForge on Windows development environments.

---

## 🛠️ Prerequisites

Ensure the following tools are installed on your workstation:

| Prerequisite | Minimum Version | Installation Source / Verification |
| :--- | :--- | :--- |
| **Python** | 3.11 or higher | [python.org](https://www.python.org/) (`python --version`) |
| **Node.js & npm** | Node 18+ / npm 9+ | [nodejs.org](https://nodejs.org/) (`node --version`, `npm --version`) |
| **FFmpeg** | 6.0 or higher | Bundled in `videoforge-backend/bin` or system PATH (`ffmpeg -version`) |
| **Playwright Chromium** | 1.40+ | Installed via `playwright install chromium` |
| **Docker Desktop** | Optional (for Redis/Postgres) | [docker.com](https://www.docker.com/) |

---

## 📦 Step-by-Step Installation

### Step 1: Set Up Backend (`videoforge-backend`)

Open PowerShell or Command Prompt in the repository root:

```powershell
cd "c:\D-Drive\Automation Utkarsh\video generation automation\videoforge-backend"

# 1. Create and activate virtual environment (optional but recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install Python dependencies in editable mode
pip install -e ".[dev]"

# 3. Install Playwright browser dependencies
playwright install chromium
```

### Step 2: Configure Environment Variables

Verify that `videoforge-backend/.env` exists and contains your API keys:

```ini
APP_NAME=VideoForge
HOST=0.0.0.0
PORT=8000
API_PREFIX=/api/v1

PROJECTS_DIR=./projects
STORAGE_DIR=./storage
COMPOSE_DIR=./compose

# Set your Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-your-key-here

# TTS Provider: 'edge' (free, no setup), 'styletts2', or 'elevenlabs'
TTS_PROVIDER=edge
EDGE_TTS_VOICE=en-US-GuyNeural

# Video defaults
DEFAULT_WIDTH=1920
DEFAULT_HEIGHT=1080
DEFAULT_FPS=30
DEFAULT_WORDS_PER_MINUTE=150
```

### Step 3: Set Up Frontend Studio (`videoforge-studio`)

```powershell
cd "c:\D-Drive\Automation Utkarsh\video generation automation\videoforge-studio"

# Install Node dependencies
npm install
```

---

## 🚀 Running VideoForge

### Method A: Manual Multi-Terminal Launch (Recommended for Development)

#### Terminal 1 — Backend API Server
```powershell
cd "c:\D-Drive\Automation Utkarsh\video generation automation\videoforge-backend"
uvicorn main:app --reload --port 8000 --host 0.0.0.0
```
* API runs at: `http://localhost:8000`
* Interactive API Docs (Swagger): `http://localhost:8000/docs`
* WebSocket endpoint: `ws://localhost:8000/ws/{project_id}`

#### Terminal 2 — Frontend Studio
```powershell
cd "c:\D-Drive\Automation Utkarsh\video generation automation\videoforge-studio"
npm run dev
```
* Studio UI runs at: `http://localhost:5173`

---

### Method B: Standalone High-Speed Clip Engine (CLI)

To test rendering without running the web UI:

```powershell
cd "c:\D-Drive\Automation Utkarsh\video generation automation"
python generate_video_clips.py
```
This script bypasses the web UI and directly executes the v2 Clip Engine: synthesizing narration via Edge-TTS, rendering 1080p SVG scenes via `DiagramRenderer`, recording animations via Playwright, and producing stitched MP4 clips.

---

## 🌐 Network Ports Reference

| Port | Service | Protocol | Description |
| :---: | :--- | :---: | :--- |
| **8000** | FastAPI Backend | HTTP / WS | REST API, WebSocket Hub, and Static Media Streamer |
| **5173** | VideoForge Studio | HTTP | Vite React Frontend User Interface |
| **6379** | Redis Server | TCP | Celery task message broker and result cache |
| **5432** | PostgreSQL | TCP | Project metadata and stage execution records |
| **8001** | StyleTTS2 / SeedVC | HTTP | Optional local GPU TTS inference server |

---

## ⚠️ Known Issues & Troubleshooting

### 1. Launcher Script Path Mismatch (`START_VIDEOFORGE.bat` / `.ps1`)
* **Problem**: The original launcher scripts contain hardcoded paths pointing to `D:\Coder_S3\video generation v3\...`.
* **Fix**: When using `START_VIDEOFORGE.bat` or `.ps1`, ensure the paths point to the current project location:
  `c:\D-Drive\Automation Utkarsh\video generation automation` or use dynamic `%~dp0` directory resolution.

### 2. FFmpeg Not Found
* **Problem**: Error stating `ffmpeg: command not found` or `WinError 2`.
* **Fix**: Ensure `videoforge-backend/bin` is in your Windows `PATH`, or install FFmpeg globally via Chocolatey / Scoop:
  ```powershell
  winget install Gyan.FFmpeg
  ```

### 3. Playwright Chromium Missing
* **Problem**: `playwright._impl._errors.Error: Executable doesn't exist at ...`
* **Fix**: Run:
  ```powershell
  playwright install chromium
  ```

### 4. Celery on Windows
* **Problem**: Celery workers crash on Windows with `ValueError: not enough values to unpack`.
* **Fix**: Windows does not support default Celery process forking. Always start Celery with the `solo` pool on Windows:
  ```powershell
  celery -A workers.celery_app worker --pool=solo --loglevel=info
  ```

### 5. Port Conflicts on 8000
* **Problem**: Port 8000 already in use by another service.
* **Fix**: Change `PORT=8005` in `videoforge-backend/.env` and update `API_BASE` in `videoforge-studio/src/services/api.ts`.
