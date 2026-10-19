# 08. Motion & Animation Skills Catalog

The `skills/` directory contains **30 specialized animation, motion design, and video production skill modules**. These skills define technical contracts, design patterns, and code generation templates used by the AI agents and pipeline stages to author dynamic video scenes.

---

## 🗂️ Skills Taxonomy

The skills are organized into four core functional domains:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        VideoForge Skills Matrix                        │
├──────────────────────────┬─────────────────────────────────────────────┤
│ 1. HyperFrames Core      │ Framework composition contract, data-*      │
│    Standards             │ timing, deterministic browser capture.      │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 2. Animation & Graphics  │ GSAP, Anime.js, Three.js, Lottie, TypeGPU,  │
│    Runtimes              │ WAAPI, CSS Animations.                      │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 3. Narrative & Video     │ Faceless Explainer, Product Launch,         │
│    Archetypes            │ Motion Graphics, Slideshow, PR to Video.    │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 4. Media & Typography    │ Embedded Captions, Media Use, Tailwind,     │
│    Subsystems            │ Figma integration, Music to Video.          │
└──────────────────────────┴─────────────────────────────────────────────┘
```

---

## 📐 1. HyperFrames Core Standards

| Skill Folder | Description & Technical Scope |
| :--- | :--- |
| **`hyperframes-core`** | **The foundational video contract**. Defines how an HTML document becomes a renderable video. Covers `data-composition-id`, `data-track-index`, `data-in-ms`, `data-out-ms`, `class="clip"`, `<template>` sub-compositions, and deterministic frame seeking rules. |
| **`hyperframes-cli`** | Command-line toolset for initializing, validating, linting, and dry-run testing HyperFrames compositions. |
| **`hyperframes-animation`** | Adapter patterns connecting animation libraries (GSAP, Lottie, Three.js) into the HyperFrames seekable timeline hook (`window.__timelines`). |
| **`hyperframes-creative`** | Art direction rules, curated color palettes (dark glass, cyberpunk, editorial), and composition rhythm. |
| **`hyperframes-keyframes`** | Standard easing curves (`power2.inOut`, `expo.out`), duration conventions, and entrance/exit choreography. |
| **`hyperframes-media`** | Placement, trimming, volume curves, and playback ownership for `<video>` and `<audio>` DOM elements. |
| **`hyperframes-registry`** | Reusable component library for recurring UI components (callout cards, stat counters, quote blocks). |
| **`remotion-to-hyperframes`** | Migration recipes and concept mapping for developers transitioning from Remotion (React) to HyperFrames (HTML/DOM). |
| **`website-to-hyperframes`** | Tooling to convert existing live web applications and DOM elements into animated video scenes. |

---

## ⚡ 2. Animation & Graphics Runtimes

| Skill Folder | Runtime Library | Best Applied To |
| :--- | :--- | :--- |
| **`gsap`** | GreenSock Animation Platform | Complex, choreographed multi-element timeline sequences, SVG path morphing, and staggered entrances. |
| **`animejs`** | Anime.js | Lightweight DOM animations, spring physics, and kinetic text animations with minimal code overhead. |
| **`three`** | Three.js (WebGL) | 3D models, rotating isometric data centers, particle clouds, and interactive 3D cameras. |
| **`lottie`** | Lottie Web / Bodymovin | Vector After Effects animations (loaders, checkmarks, complex icon animations) rendered natively. |
| **`typegpu`** | WebGPU & Shaders | High-performance GPU shaders, procedural backgrounds, audio-reactive waveforms, and volumetric lighting. |
| **`waapi`** | Web Animations API | Pure browser-native keyframe animations requiring zero external JavaScript libraries. |
| **`css-animations`** | Pure CSS3 Keyframes | Hardware-accelerated pulse effects, glowing borders, and perpetual ambient background gradients. |

---

## 📽️ 3. Narrative & Video Archetypes

| Skill Folder | Production Format | Architectural Patterns |
| :--- | :--- | :--- |
| **`faceless-explainer`** | Long-form Educational Masterclass | The primary archetype used in VideoForge. Focuses on continuous visual progression without an on-camera host. |
| **`product-launch-video`** | SaaS / Hardware Product Announcement | High-tempo, high-contrast visual cuts highlighting key features, metrics, and call-to-actions. |
| **`motion-graphics`** | Lower Thirds & Dynamic Callouts | Animated banners, author titles, footnote callouts, and chapter bumper cards. |
| **`slideshow`** | Modern Dynamic Presentation | Clean, elevated slide layouts featuring animated bullet reveals, split screens, and quote highlights. |
| **`talking-head-recut`** | Hybrid Presentation | Interleaving webcam recordings with full-screen code walkthroughs and B-roll visuals. |
| **`pr-to-video`** | Developer Changelogs | Transforming GitHub Pull Requests, diffs, and release notes into automated video digests. |

---

## 🎨 4. Media & Subtitle Subsystems

| Skill Folder | Focus Area | Key Features |
| :--- | :--- | :--- |
| **`embedded-captions`** | Subtitles & Kinetic Typography | Safe-margin boundaries (avoiding YouTube UI overlaps), high-contrast outlines, word-by-word active glow styling. |
| **`media-use`** | Media Sourcing & Placement | Sizing constraints, aspect ratio containment (`cover` vs `contain`), and video overlay blend modes. |
| **`tailwind`** | Tailwind CSS v4 Integration | Rapid styling of video layouts using utility classes while respecting deterministic rendering bounds. |
| **`figma`** | Vector UI Ingestion | Converting exported Figma SVG component frames directly into clean, scalable HTML scene templates. |
| **`music-to-video`** | Beat Synchronization | Mapping animation keyframes to transient audio beat markers and tempo changes. |
