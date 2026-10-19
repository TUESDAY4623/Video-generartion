# VideoForge — AI Video Generation Automation

> **Production-grade automated video generation platform that converts technical topics into 40–50+ minute broadcast-quality educational masterclasses.**

---

## 🧠 Project Brain & Knowledge Base

Complete architectural documentation, system specifications, pipeline designs, and operational guides have been compiled into the **[`brain/`](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/README.md)** directory:

1. **[01. Project Overview & Philosophy](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/01_project_overview.md)** — Core mission, target use cases, and quality-first comparative matrix.
2. **[02. System Architecture & Data Flow](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/02_system_architecture.md)** — High-level topology, component breakdown, and file system layout.
3. **[03. The 9-Stage Production Pipeline](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/03_pipeline_stages.md)** — Research, Proposal, Script, Chapterize, Scene Plan, Assets, Edit, Compose, and Publish.
4. **[04. Backend Architecture (FastAPI & Celery)](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/04_backend_architecture.md)** — API endpoints, WebSocket hub, database models, and background task queues.
5. **[05. Rendering & Visual Engine](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/05_rendering_and_visual_engine.md)** — Native SVG/HTML `DiagramRenderer`, Playwright Chromium recording, and FFmpeg stitching.
6. **[06. Audio & TTS Engine](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/06_audio_and_tts_engine.md)** — Multi-engine TTS (Edge-TTS, StyleTTS2, ElevenLabs), Whisper word alignment, and loudness mastering.
7. **[07. Frontend Studio (React & Vite)](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/07_frontend_studio.md)** — Studio views, real-time WebSocket pipeline monitor, and cinema video player.
8. **[08. Motion & Animation Skills Catalog](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/08_skills_catalog.md)** — Guide to the 30 visual animation and motion design skills in `skills/`.
9. **[09. Operations, Setup & Troubleshooting](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/09_operations_and_setup.md)** — Installation steps, environment variables, port maps, and troubleshooting.

---

## ⚡ Quick Start

### 1. Launch Backend (FastAPI)
```powershell
cd videoforge-backend
uvicorn main:app --reload --port 8000
```
* API Docs: `http://localhost:8000/docs`

### 2. Launch Studio Frontend (React + Vite)
```powershell
cd videoforge-studio
npm run dev
```
* Studio UI: `http://localhost:5173`

### 3. Run Standalone Clip Engine (CLI)
```powershell
python generate_video_clips.py
```