# 03. The 9-Stage Production Pipeline

The core engine of VideoForge is a sequential, checkpointed 9-stage video production pipeline. Each stage has defined contracts, strict quality validation gates, and checkpoint persistence to allow pausing, re-running, or fine-tuning without restarting the entire build.

---

## 📋 Pipeline Summary Table

| Stage # | Stage Name | Primary Function | Primary Engine / Tech | Core Artifact Output |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **RESEARCH** | Topic synthesis, knowledge extraction & curriculum structuring | Claude 3.7 Sonnet / Haiku | `raw_research.md`, `key_concepts.json` |
| **2** | **PROPOSAL** | High-level roadmap, duration budgeting, and visual archetype selection | Claude 3.7 Sonnet | `proposal.json`, `chapter_outline.md` |
| **3** | **SCRIPT** | Spoken narration authoring with interleaved visual markers `[VISUAL: ...]` | Claude 3.7 Sonnet | `full_script.txt`, `script_segments.json` |
| **4** | **CHAPTERIZE** | Logical division of script into timed chapters with scene assignments | Rule-based parser + Claude | `chapters_manifest.json` |
| **5** | **SCENE_PLAN** | Creation of detailed `VisualSceneSpec` instances per 10–15s clip | Pipeline Scene Planner | `scene_specs.json` |
| **6** | **ASSETS** | Batch TTS voice synthesis, Whisper word alignment & HTML/SVG generation | Edge-TTS/StyleTTS2 + DiagramRenderer | `.mp3` audio, `.json` timestamps, `.html` visuals |
| **7** | **EDIT** | Edit Decision List (EDL) assembly with transitions & audio envelopes | Audio/Video Matcher | `edit_decision_list.json` |
| **8** | **COMPOSE** | Headless browser animation capture, audio muxing, and video stitching | Playwright (Chromium) + FFmpeg | Rendered `.webm`/`.mp4` clips, stitched rough cut |
| **9** | **PUBLISH** | Final audio mastering (-14 LUFS), music ducking (-18dB), thumbnail generation | FFmpeg Filtergraph + Pillow | `final_master.mp4`, `thumbnail.jpg` |

---

## 🔍 Detailed Stage Breakdown

### Stage 1: RESEARCH
* **Objective**: Ingest the user's topic prompt, subtopics, and target audience, conducting deep pedagogical research to extract accurate concepts, mental models, code examples, and technical analogies.
* **Input**: Project prompt (`topic`, `subtopic`, `target_audience`, `user_explanation`).
* **Processing**:
  * Claude query with prompt engineering tuned for curriculum generation.
  * Extraction of technical prerequisites, common misconceptions, and core terminology.
* **Outputs**:
  * `01_research/raw_research.md`: Full theoretical knowledge base.
  * `01_research/key_concepts.json`: Ordered array of conceptual milestones.
* **Quality Gate**: Must identify at least 5 distinct sub-concepts and verify code syntax validity.

---

### Stage 2: PROPOSAL
* **Objective**: Transform research findings into a structured curriculum blueprint with a strict time budget.
* **Input**: `key_concepts.json` and `target_duration_minutes` (e.g., 45 minutes).
* **Processing**:
  * Mathematical time allocation per chapter (e.g., 5 chapters, ~8–10 minutes each).
  * Assignment of visual archetypes to avoid consecutive duplicate scene formats.
* **Outputs**:
  * `02_proposal/proposal.json`: Chapter names, timing allotments, and visual strategies.
* **Quality Gate**: Total calculated duration must stay within ±10% of the target duration.

---

### Stage 3: SCRIPT
* **Objective**: Write the actual verbatim spoken narration, calibrated to a natural conversational teaching pace (150 words per minute).
* **Visual Synchronization Rule**: Every 25–40 words (~10–15 seconds of speech), an explicit visual marker is inserted:
  ```text
  Computers do not understand English or Python directly. At the physical layer, everything is voltage.
  [VISUAL: diagram | "Transistor Logic Gates" | components: ["High Voltage (+5V)", "Low Voltage (0V)", "Transistor Switch"]]
  When a voltage passes a threshold, we represent it as a logical 1. Absence of voltage is a 0.
  ```
* **Outputs**:
  * `03_script/full_script.txt`: Complete unparsed spoken script with visual tags.
  * `03_script/script_segments.json`: Machine-readable array of text blocks tied to cues.
* **Quality Gate**: Words-per-minute check; cue density must average 1 visual cue every 12 seconds of dialogue.

---

### Stage 4: CHAPTERIZE
* **Objective**: Segment the continuous script into discrete chapters and scenes, calculating exact expected audio runtimes based on word counts.
* **Outputs**:
  * `04_chapters/chapters_manifest.json`: Hierarchical structure: Chapter ➔ Scenes ➔ Visual Cues.

---

### Stage 5: SCENE_PLAN
* **Objective**: Translate raw visual cues into concrete, programmatic `VisualSceneSpec` objects that the rendering engine can execute.
* **Archetype Assignment**:
  * `diagram`: Interactive architecture or entity relationships.
  * `process_flow`: Step-by-step pipeline or execution lifecycle.
  * `comparison`: Side-by-side technical trade-off matrix.
  * `code_walkthrough`: Multi-line syntax block with active line highlight and explanation callout.
  * `concept_card`: High-impact summary cards with glassmorphism and animated badges.
* **Outputs**:
  * `05_scene_plan/scene_specs.json`: Fully hydrated specs ready for visual code generation.

---

### Stage 6: ASSETS (Dual-Track Generation)
This stage executes two parallel jobs:

#### Track A: Audio Synthesis & Word Alignment
1. **TTS Synthesis**: Generates studio-grade speech audio (`.mp3` or `.wav`) for every scene using Edge-TTS or local neural models.
2. **Whisper Forced Alignment**: The generated audio is processed through `openai-whisper` in timestamp mode to generate word-level boundaries:
   ```json
   {
     "word": "Transistor",
     "start": 1.24,
     "end": 1.82,
     "confidence": 0.98
   }
   ```
3. **Subtitles**: Exported to standard `.srt` and `.vtt` formats.

#### Track B: Programmatic HTML/SVG Generation
1. `DiagramRenderer` takes each `VisualSceneSpec` and compiles a standalone, self-contained `index.html` file.
2. Contains embedded inline CSS, native SVG graphics, and CSS keyframe animations.
3. Completely self-contained with **zero external CDN dependencies** (guaranteeing offline rendering and zero network failure risk).

---

### Stage 7: EDIT
* **Objective**: Compile the Edit Decision List (EDL). Synchronizes visual entrance and exit cues to the precise millisecond timestamps established by the audio track.
* **Transition Planning**: Assigns cinematic transitions between sub-clips:
  * Directional slides (left, right, up).
  * Smooth crossfades (0.5s duration).
  * Scale and blur morphs for code progression.
* **Outputs**:
  * `07_edit/edit_decision_list.json`: Master playback timetable.

---

### Stage 8: COMPOSE (Screen Capture & Initial Mux)
* **Objective**: Turn HTML visual specs into actual video streams and combine them with voice narration.
* **Execution**:
  1. Playwright opens headless Chromium configured to a strict viewport of 1920x1080.
  2. The page loads the scene's `index.html`.
  3. Chromium records the frame sequence at 30 fps or directly records WebM video.
  4. FFmpeg muxes the recorded visual clip with the corresponding scene narration audio.
  5. Individual clips are concatenated using the FFmpeg concat demuxer.
* **Outputs**:
  * `08_compose/rendered_clips/`: Directory of individual scene clips.
  * `08_compose/stitched_rough.mp4`: Rough stitched composite.

---

### Stage 9: PUBLISH (Mastering & Delivery)
* **Objective**: Elevate the rough cut into broadcast-ready media.
* **Processing**:
  * **Audio Ducking**: Combines ambient background music with narration. Music volume automatically drops to -18dB while speech is active, rising to -6dB during pauses.
  * **Audio Loudness**: Normalizes master audio to the industry standard **-14 LUFS (EBU R128)**.
  * **Subtitle Burn**: Optional burned-in karaoke-style kinetic captions or soft subtitle muxing.
  * **Thumbnail Generation**: Pillow/Canvas extracts key visual frame and overlays typography to produce a 1920x1080 thumbnail image.
* **Outputs**:
  * `09_publish/final_master.mp4`: Master release video.
  * `09_publish/thumbnail.jpg`: YouTube/LMS ready thumbnail.
