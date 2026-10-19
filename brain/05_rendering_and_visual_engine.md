# 05. Rendering & Visual Engine

VideoForge abandons traditional raster slide generation in favor of a **code-first, browser-rendered visual motion pipeline**. Graphics are compiled as 1080p HTML5, SVG, and CSS animations, then captured frame-accurately via headless Chromium and composed using FFmpeg.

---

## 🎨 DiagramRenderer: Pure Native SVG & Glassmorphism

The centerpiece of VideoForge's visual subsystem is `DiagramRenderer` (`renderers/diagram_renderer.py`), which dynamically compiles semantic conceptual structures into standalone, 1920x1080 HTML/SVG files.

### Design Principles of DiagramRenderer

1. **Zero External CDN Dependencies**:
   * No CDNs (such as Google Fonts or unpkg) are fetched at runtime.
   * Eliminates render freezes, network rate limits, and cross-origin security issues inside headless browser runners.
2. **Infinite Visual Scalability**:
   * All structural diagrams, connectors, arrows, and icons are pure vector SVG.
   * Text and diagrams render with pin-sharp clarity regardless of output resolution (1080p, 4K).
3. **Glassmorphism Aesthetic**:
   * Deep dark canvas (`#070a14` / `#0d1117`).
   * Translucent frosted glass containers (`backdrop-filter: blur(16px)`, `background: rgba(255,255,255,0.03)`).
   * Subtle glowing borders (`rgba(124, 131, 255, 0.25)`), dynamic pulse glows, and neon accents.

---

## 📐 Supported Scene Archetypes

`DiagramRenderer` supports five distinct semantic scene types:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DiagramRenderer Archetypes                      │
├─────────────────────┬──────────────────────────────────────────────────┤
│ 1. Architecture     │ Nodes, animated pulse connectors, layers, and    │
│    Diagram          │ subsystem boundaries (e.g., Client-Server-DB).   │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 2. Process Flow     │ Sequential workflow steps with animated step-by- │
│                     │ step badges, arrows, and active state highlights.│
├─────────────────────┼──────────────────────────────────────────────────┤
│ 3. Comparison Cards │ Side-by-side architectural evaluations (e.g.,    │
│                     │ REST vs GraphQL, Monolith vs Microservices).     │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 4. Code Walkthrough │ IDE-style dark code block, syntax highlighting,  │
│                     │ line numbers, and active glowing line callouts.  │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 5. Concept Card     │ High-impact executive summaries with animated    │
│                     │ badges, key takeaway lists, and accent glows.    │
└─────────────────────┴──────────────────────────────────────────────────┘
```

### VisualSceneSpec Data Structure

Every visual scene is defined by a strongly typed Python specification:

```python
@dataclass
class VisualSceneSpec:
    scene_id: str                      # Unique scene identifier (e.g., "s02_c03")
    visual_type: str                   # 'diagram' | 'process_flow' | 'comparison' | 'code_walkthrough' | 'concept_card'
    title: str                         # Header title
    subtitle: Optional[str] = None     # Explanatory subtitle
    diagram_code: Optional[str] = None # Mermaid or text flowchart syntax
    steps: List[Dict[str, str]]        # Sequential step list for process flows
    comparison_items: List[Dict]       # Columns & attributes for comparisons
    code_snippet: Optional[str] = None # Code block content
    code_language: str = "python"      # Syntax identifier
    highlight_lines: List[int]         # Lines to highlight with neon aura
    key_points: List[str]              # Bullet points or takeaways
    accent_color: str = "#7c83ff"      # Primary thematic accent color
    clip_index: int = 0                # Index within current scene
    total_clips: int = 1               # Total sub-clips in current scene
    narration_text: str = ""           # Associated narration for subtitle overlay
```

---

## 🎬 Browser Capture Pipeline (Playwright)

To convert dynamic HTML/CSS animations into video files, VideoForge employs **Playwright** controlling headless Chromium.

### Recording Mechanism

1. **Viewport Lock**: Chromium launches with strict parameters:
   ```python
   browser = await playwright.chromium.launch(headless=True)
   context = await browser.new_context(
       viewport={"width": 1920, "height": 1080},
       record_video_dir=output_dir,
       record_video_size={"width": 1920, "height": 1080}
   )
   ```
2. **Deterministic Playback**:
   * The page is loaded locally via `file://` URI.
   * The recorder waits for DOM animations to execute over the exact duration of the scene's narration audio.
   * Playwright closes the context, finalizing the `.webm` video stream.

---

## 🎞️ FFmpeg Compositing & Stitching

After the browser captures the raw visual clips, FFmpeg executes multi-stage post-processing:

### 1. Clip Muxing & Encoding
Each `.webm` capture is paired with its corresponding narration `.mp3`:
```bash
ffmpeg -y -i clip_01.webm -i narration_01.mp3 \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest clip_01_muxed.mp4
```

### 2. Concatenation Demuxing
Individual scene clips are concatenated without re-encoding quality degradation using the concat demuxer:
```bash
# filelist.txt contains:
# file 'clip_01_muxed.mp4'
# file 'clip_02_muxed.mp4'
ffmpeg -y -f concat -safe 0 -i filelist.txt -c copy stitched_rough.mp4
```

### 3. Crossfade Transitions (`xfade`)
Where smoother cinematic transitions are required between major chapters, the `xfade` filter is injected:
```bash
ffmpeg -i scene1.mp4 -i scene2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=11.5[v]" \
  -map "[v]" -c:v libx264 scene_transition.mp4
```

---

## ⚡ The HyperFrames Standard

In addition to `DiagramRenderer`, VideoForge supports the **HyperFrames specification** (documented in `skills/hyperframes-core/`):
* Compositions are declared via HTML DOM attributes (`data-composition-id`, `data-track-index`, `data-in-ms`, `data-out-ms`).
* Enables complex GSAP, Three.js, and Lottie animations to be seeked deterministically to exact frame indices during video rendering.
