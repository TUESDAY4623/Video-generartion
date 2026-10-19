# 02. System Architecture & Data Flow

This document details the complete end-to-end architectural topography of VideoForge, including inter-service communication, data persistence, media pipelines, and storage layouts.

---

## 🏛️ System Topology Diagram

```mermaid
flowchart TB
    subgraph Frontend ["Frontend: VideoForge Studio (Port 5173)"]
        UI[React 19 + TypeScript + Vite]
        Store[Zustand State Store]
        Query[TanStack React Query]
        WS_Client[WebSocket Consumer]
    end

    subgraph Backend ["Backend: VideoForge Core (Port 8000)"]
        FastAPI[FastAPI Application]
        Router[REST Routers: /projects, /pipeline, /assets]
        WSHub[WebSocket Hub /ws/{project_id}]
        Orch[Pipeline Orchestrator]
    end

    subgraph Workers ["Task Execution & Broker"]
        Redis[(Redis: Port 6379)]
        Celery[Celery Distributed Workers]
        CLI[Standalone CLI Runners]
    end

    subgraph Engines ["Specialized Processing Engines"]
        Claude[Anthropic Claude API\nResearch, Scripting & Cues]
        TTS[Speech Synthesis\nEdge-TTS / StyleTTS2 / ElevenLabs]
        Whisper[Whisper Aligner\nWord-Level Timestamps]
        Diagram[DiagramRenderer\nNative SVG & Glassmorphism HTML]
        Playwright[Headless Chromium\n1080p WebM/Frame Capture]
        FFmpeg[FFmpeg Engine\nMulti-Track Audio & MP4 Concat]
    end

    subgraph Storage ["Persistent Storage"]
        DB[(PostgreSQL / SQLite Database)]
        ProjectsFS[File Storage: ./projects/{id}/]
    end

    %% Interactions
    UI -->|HTTP REST| Router
    UI -->|Live Progress| WS_Client
    WS_Client <-->|WebSocket Events| WSHub

    Router --> FastAPI
    FastAPI --> Orch
    FastAPI --> DB

    Orch -->|Enqueue Tasks| Redis
    Redis --> Celery
    Celery --> Orch
    CLI --> Orch

    Orch --> Claude
    Orch --> TTS
    Orch --> Whisper
    Orch --> Diagram
    Orch --> Playwright
    Orch --> FFmpeg

    Orch -->|Progress Events| WSHub
    Orch -->|State & Artifacts| DB
    Orch -->|Save Assets & MP4| ProjectsFS
```

---

## 🧩 Architectural Components

### 1. Studio Frontend (`videoforge-studio`)
* **Technology**: React 19, TypeScript 5, Vite, Tailwind CSS v4, Lucide icons, Framer Motion.
* **Responsibilities**:
  * Project creation wizard (topic selection, target audience, style, duration budgeting).
  * Real-time pipeline monitoring board showing state, active stage logs, error reporting, and progress bars via WebSockets.
  * Interactive video player with chapter jump marks and asset inspection.
  * System settings interface for credentials and service endpoints.

### 2. API & Orchestration Server (`videoforge-backend`)
* **Technology**: Python 3.11+, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2.0.
* **Responsibilities**:
  * REST API management for projects, pipeline control (`/start`, `/pause`, `/abort`), and asset downloading.
  * WebSocket broadcasting (`/ws/{project_id}`) distributing granular stage events.
  * State lifecycle management across the 9 pipeline stages.
  * Serving static project artifacts (rendered HTML, scene previews, MP4 files) via `/projects` mount.

### 3. Asynchronous Queue & Distributed Workers
* **Technology**: Celery + Redis 7.
* **Responsibilities**:
  * Offloading computationally heavy jobs (browser-based video rendering, audio synthesis, and video encoding).
  * Supporting stage checkpoints so long-running jobs can resume seamlessly upon server restart or failure.

### 4. Specialized Engine Integrations

| Subsystem | Service / Library | Role |
| :--- | :--- | :--- |
| **Cognitive Engine** | Anthropic Claude (`claude-3-7-sonnet`, `claude-3-haiku`) | Domain topic synthesis, pedagogical structuring, script generation, and scene prompt drafting. |
| **Voice Synthesis** | `edge-tts`, `StyleTTS2`, `SeedVC`, `ElevenLabs` | Generating expressive voice tracks calibrated to 150 words per minute. |
| **Timestamp Alignment** | `openai-whisper` | Analyzing generated voice audio to extract millisecond timestamps per word for subtitles and motion triggering. |
| **Visual Scene Renderer** | `DiagramRenderer` & `HyperFrames` | Programmatically generating standalone 1920x1080 HTML/SVG documents with animated elements. |
| **Screen Recorder** | Playwright (Headless Chromium) | Emulating a 1080p viewport and capturing animations directly into WebM streams. |
| **Compositing & Mixing** | `FFmpeg` 6+ | Video clipping, audio normalization (-14 LUFS), dynamic music ducking (-18dB), subtitle burning, and stream concatenation. |

---

## 🗄️ Project File System Layout

Each project maintains an isolated directory structure under `videoforge-backend/projects/{project_id}/`:

```
projects/{project_id}/
├── metadata.json                 # Project configuration, parameters & timeline index
├── 01_research/
│   ├── raw_research.md          # Comprehensive topic research & reference materials
│   └── key_concepts.json        # Extracted pedagogical concepts and entities
├── 02_proposal/
│   ├── proposal.json            # Target durations, visual archetypes, outline
│   └── chapter_breakdown.md     # Chapter titles and synopses
├── 03_script/
│   ├── full_script.txt          # Complete narration with [VISUAL: ...] cues
│   └── script_segments.json     # Segmented text with cue tags
├── 04_chapters/
│   └── chapters_manifest.json   # Timed chapter segments & scene assignments
├── 05_scene_plan/
│   └── scene_specs.json         # Specifications for every individual scene/clip
├── 06_assets/
│   ├── audio/
│   │   ├── scene_01.mp3         # Spoken narration per scene
│   │   ├── scene_01_words.json  # Whisper word-level timestamp alignments
│   │   └── bgm_loop.mp3         # Background audio track
│   ├── visuals/
│   │   ├── scene_01_clip_01.html # Self-contained 1080p SVG/HTML animation
│   │   └── scene_01_clip_02.html # Additional visual variations
│   └── subtitles/
│       ├── subtitles.srt        # Generated SRT subtitle file
│       └── subtitles.vtt        # WebVTT subtitle track
├── 07_edit/
│   └── edit_decision_list.json  # EDL specifying transitions, cuts, and audio mixes
├── 08_compose/
│   ├── rendered_clips/
│   │   ├── clip_01.webm         # Raw Playwright captured clip
│   │   └── clip_01_audio.mp4    # Muxed clip with aligned narration
│   └── stitched_rough.mp4       # Concatenated draft video
└── 09_publish/
    ├── final_master.mp4         # Final 1080p master with music, ducking & intro/outro
    └── thumbnail.jpg            # Auto-generated high-resolution thumbnail
```

---

## 🔄 Inter-Service Communication Flow

```
[User Action in Studio]
        │
        ▼ (POST /api/v1/projects)
[FastAPI Router] ──── Creates Database Record ────► [PostgreSQL]
        │
        ▼ (POST /api/v1/pipeline/{id}/start)
[Pipeline Orchestrator] ──── Dispatches Tasks ────► [Redis Queue]
        │                                                  │
        │                                                  ▼
        │                                         [Celery Worker Thread]
        │                                                  │
        │ ◄──── Stage Progress Events (WebSockets) ────────┘
        ▼
[Broadcast to UI Clients via WebSocket Hub]
```
