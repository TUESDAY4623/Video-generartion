# 07. Frontend Studio (React & Vite)

The frontend application (`videoforge-studio`) is a modern web application built on **React 19**, **TypeScript**, and **Vite**, providing a dark-mode control room for configuring, monitoring, and previewing automated video production runs.

---

## 💻 Tech Stack & Architecture

```
videoforge-studio/
├── src/
│   ├── components/
│   │   ├── common/           # Button, Modal, Card, Input primitives
│   │   ├── dashboard/        # Stat cards, recent project lists
│   │   ├── layout/           # Sidebar navigation, App header
│   │   ├── pipeline/         # StageCard, StageTimeline, LogViewer
│   │   ├── project/          # ProjectForm, AudienceSelector
│   │   └── video/            # VideoPlayer controls, ChapterBar
│   ├── pages/
│   │   ├── Dashboard.tsx       # Route: /
│   │   ├── CreateProject.tsx   # Route: /create
│   │   ├── PipelineMonitor.tsx # Route: /project/:id
│   │   ├── VideoPlayer.tsx     # Route: /project/:id/watch
│   │   └── Settings.tsx        # Route: /settings
│   ├── services/
│   │   └── api.ts            # Axios REST client & video URL resolver
│   ├── stores/               # Zustand global state stores
│   ├── types/
│   │   └── index.ts          # TypeScript interfaces (Project, StageRun, etc.)
│   ├── App.tsx               # Root route definitions
│   └── main.tsx              # React DOM initialization
├── package.json              # React 19, Tailwind v4, TanStack Query
└── vite.config.ts            # Vite build configuration
```

---

## 📄 Application Views

### 1. Dashboard (`/`)
* **Purpose**: Mission control providing high-level operational visibility.
* **Key Components**:
  * Metric summary cards (Total Videos Created, Total Render Time, Active Jobs, GPU/Server Health).
  * Filterable project table and grid views.
  * Status badges: `draft`, `generating`, `rendering`, `complete`, `failed`.
  * Quick-action buttons: Create New Video, Resume Pipeline, Watch Video.

### 2. Project Creation Wizard (`/create`)
* **Purpose**: Multi-step configuration form translating human intent into pipeline parameters.
* **Configurable Fields**:
  * **Core Topic & Subtopic**: Main subject matter (e.g., "PostgreSQL Indexing Internals").
  * **User Explanation Prompt**: Specific areas, diagrams, and examples to emphasize.
  * **Duration Budget Slider**: Target runtime from 5 minutes to 60 minutes.
  * **Audience Calibration**: `beginner`, `intermediate`, `advanced` (alters explanation depth and vocabulary).
  * **Visual Style**: `cinematic`, `educational`, `minimal`, `corporate`.
  * **Speaking Pacing**: `slow` (130 WPM), `moderate` (150 WPM), `fast` (170 WPM).

### 3. Real-Time Pipeline Monitor (`/project/:id`)
* **Purpose**: Real-time visualization of the 9-stage pipeline execution.
* **Features**:
  * **WebSocket Ingestion**: Connects directly to `ws://localhost:8000/ws/{id}`.
  * **9-Stage Interactive Timeline**:
    * Each stage displays status (`pending`, `running`, `complete`, `failed`), execution duration, and live progress percentage.
  * **Live Log Stream**: Displays streaming stdout/stderr and progress events as Claude, TTS, and FFmpeg execute.
  * **Pipeline Controls**:
    * **Start**: Trigger pipeline from the first uncompleted stage.
    * **Pause**: Gracefully halt after current stage finishes.
    * **Abort**: Terminate active processing immediately.

### 4. Cinema Video Player (`/project/:id/watch`)
* **Purpose**: Dedicated high-fidelity player for reviewing completed video outputs.
* **Features**:
  * Integrated chapter navigation (scrub directly between chapters via timeline ticks).
  * Dual-track subtitle preview (SRT/VTT).
  * Media asset drawer: Download raw script, scene HTML previews, individual audio clips, or final 1080p master MP4.

### 5. Settings (`/settings`)
* **Purpose**: Environment and credentials management.
* **Settings Controlled**:
  * Anthropic API Key (`ANTHROPIC_API_KEY`).
  * ElevenLabs API Key and Voice ID selector.
  * Local TTS server URLs (`StyleTTS2`, `SeedVC`).
  * Video defaults (Resolution, Framerate, Words Per Minute).

---

## 🔌 API Client Architecture (`src/services/api.ts`)

The frontend interacts with the FastAPI backend through a typed Axios client:

```typescript
export const API_BASE = 'http://localhost:8000/api/v1';

// Projects
export async function fetchProjects(): Promise<Project[]>;
export async function fetchProject(id: string): Promise<Project>;
export async function createProject(payload: CreateProjectData): Promise<Project>;
export async function deleteProject(id: string): Promise<void>;

// Pipeline Control
export async function startPipeline(projectId: string): Promise<any>;
export async function pausePipeline(projectId: string): Promise<any>;
export async function abortPipeline(projectId: string): Promise<any>;
export async function fetchPipelineStatus(projectId: string): Promise<any>;
export async function fetchStageRuns(projectId: string): Promise<StageRun[]>;

// Media Resolution
export function getVideoUrl(path: string | null): string | null;
```
