# VideoForge — Project Brain (Knowledge Base & Documentation)

Welcome to the **VideoForge Project Brain**. This directory serves as the centralized, authoritative knowledge repository for developers, system architects, and AI agents working on the VideoForge video generation automation platform.

---

## 🧭 Brain Index & Table of Contents

| Document | Title | Description |
| :--- | :--- | :--- |
| **[01_project_overview.md](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/01_project_overview.md)** | **Project Overview & Philosophy** | Core mission, design philosophy, competitive comparison, and target use cases. |
| **[02_system_architecture.md](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/02_system_architecture.md)** | **System Architecture & Data Flow** | High-level system diagram, data flow between services, storage models, and protocols. |
| **[03_pipeline_stages.md](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/03_pipeline_stages.md)** | **9-Stage Production Pipeline** | Complete walkthrough of all 9 stages: Research, Proposal, Script, Chapterize, Scene Plan, Assets, Edit, Compose, Publish. |
| **[04_backend_architecture.md](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/04_backend_architecture.md)** | **Backend Architecture (FastAPI & Celery)** | FastAPI API endpoints, Celery workers, Redis queues, SQLAlchemy data models, and CLI runners. |
| **[05_rendering_and_visual_engine.md](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/05_rendering_and_visual_engine.md)** | **Rendering & Visual Engine** | Native 1080p SVG `DiagramRenderer`, HyperFrames HTML-to-video runtime, Playwright capture, and FFmpeg stitching. |
| **[06_audio_and_tts_engine.md](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/06_audio_and_tts_engine.md)** | **Audio & TTS Engine** | Edge-TTS, StyleTTS2, ElevenLabs adapters, Whisper word-level alignment, audio ducking, and sound design. |
| **[07_frontend_studio.md](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/07_frontend_studio.md)** | **Frontend Studio (React & Vite)** | React 19, TypeScript, Tailwind CSS, Zustand stores, WebSocket real-time progress monitor, and video player. |
| **[08_skills_catalog.md](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/08_skills_catalog.md)** | **Motion & Animation Skills Catalog** | Overview of the 30 modular skills (HyperFrames, GSAP, Anime.js, Lottie, Three.js, etc.) used for creative video output. |
| **[09_operations_and_setup.md](file:///c:/D-Drive/Automation%20Utkarsh/video%20generation%20automation/brain/09_operations_and_setup.md)** | **Operations, Setup & Troubleshooting** | Installation guide, environment configurations, launcher scripts, port tables, and common troubleshooting tips. |

---

## 🎯 Quick Mental Model

VideoForge solves the fundamental limitation of standard AI video tools: rather than generating static "slide decks with robotic voiceovers", VideoForge orchestrates an automated digital animation studio capable of generating **40-50+ minute broadcast-quality educational masterclasses**.

```
User Prompt / Topic
         │
         ▼
┌────────────────────────────────────────────────────────┐
│              VideoForge 9-Stage Pipeline               │
│  Research ➔ Script ➔ Chapters ➔ Scenes ➔ Visuals/TTS  │
│          ➔ Edit Decision List ➔ Compose ➔ Publish      │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
   Visual Engine (Playwright)   Audio Engine (TTS + Whisper)
   - Dynamic SVG & HTML5        - Edge-TTS / StyleTTS2
   - Glassmorphism & Diagrams   - Sub-second timestamp sync
   - HyperFrames Animations     - Background music & ducking
             └─────────────┬─────────────┘
                           │
                           ▼
              FFmpeg Multi-Track Assembly
                           │
                           ▼
          Final Master 1080p MP4 + Captions + SRT
```

---

## 📂 Repository Directory Map

```
video generation automation/
├── brain/                       # Project Brain Knowledge Base (this directory)
├── skills/                      # 30 modular animation and motion design skills
│   ├── hyperframes-core/        # HyperFrames HTML video rendering contract
│   ├── gsap/                    # GSAP timeline choreographies
│   ├── animejs/                 # Lightweight DOM & SVG animations
│   ├── three/                   # 3D interactive graphics
│   └── ...                      # 26 other animation & video domain skills
├── video/                       # Sample outputs, solution documentation, reference videos
├── videoforge-backend/          # Python backend service
│   ├── app/                     # FastAPI core, routers, services, config
│   ├── pipeline/                # 9-stage pipeline orchestrators and stage runners
│   ├── renderers/               # Native SVG DiagramRenderer & HTML generators
│   ├── bin/                     # Local FFmpeg binaries
│   ├── projects/                # Generated project outputs (scripts, audio, scenes, mp4)
│   ├── generate_video_clips.py  # Standalone high-throughput clip generator (v2)
│   └── main.py                  # API server entrypoint
├── videoforge-studio/           # React 19 + TypeScript + Vite frontend
│   ├── src/pages/               # Dashboard, CreateProject, PipelineMonitor, VideoPlayer, Settings
│   ├── src/components/          # UI components (sidebar, modals, stage cards, timeline)
│   ├── src/services/            # REST and WebSocket API client
│   └── src/types/               # TypeScript data models and stage definitions
├── START_VIDEOFORGE.bat         # Windows Command Prompt launcher
├── START_VIDEOFORGE.ps1         # PowerShell one-click launcher
└── STOP_VIDEOFORGE.bat          # Graceful process terminator
```
