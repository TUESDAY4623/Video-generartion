# 06. Audio & TTS Engine

Sound is half of the video experience. VideoForge features a comprehensive audio engineering pipeline covering multi-engine text-to-speech synthesis, sub-second word-level timestamp alignment, dynamic music ducking, and broadcast loudness mastering.

---

## 🎙️ Speech Synthesis Architecture

Audio generation is abstracted through an extensible adapter pattern (`app/adapters/`), allowing the system to switch between local GPU models and cloud APIs seamlessly.

```
                  ┌────────────────────────────────────────┐
                  │       Audio Generation Interface       │
                  └───────────────────┬────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         ▼                            ▼                            ▼
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│     Edge-TTS     │         │    StyleTTS2     │         │    ElevenLabs    │
│  (Default/Free)  │         │  (Local Neural)  │         │  (Cloud Studio)  │
├──────────────────┤         ├──────────────────┤         ├──────────────────┤
│ - Zero API cost  │         │ - Runs on GPU    │         │ - Highest nuance │
│ - Microsoft      │         │ - Expressive     │         │ - Custom voice   │
│   Neural voices  │         │   prosody & pitch│   clones           │
│ - Ultra-fast     │         │ - Offline ready  │         │ - Premium cost   │
└──────────────────┘         └──────────────────┘         └──────────────────┘
```

### Supported TTS Providers

| Provider Key | Primary Voice / Model | Setup & Requirements | Best For |
| :--- | :--- | :--- | :--- |
| `edge` *(Recommended Default)* | `en-US-GuyNeural`, `en-US-JennyNeural` | Pre-installed via `edge-tts`. No API key or GPU required. | Rapid local development, cost-free batch rendering. |
| `styletts2` | StyleTTS2 PyTorch server on port 8000 | Requires local Python environment and NVIDIA GPU (CUDA). | Studio-grade human inflection with 100% offline privacy. |
| `seedvc` | SeedVC Voice Conversion server on port 8001 | Requires local PyTorch server. | Voice cloning and custom timbre adaptation. |
| `elevenlabs` | Turbo v2.5 / Multilingual v2 | Requires `ELEVENLABS_API_KEY`. | Production commercial releases and top-tier presentations. |

---

## ⏱️ Whisper Word-Level Alignment (`WhisperAligner`)

Generating audio alone is insufficient for high-retention video; animations and subtitles must trigger at the exact instant a word is uttered.

### How Whisper Alignment Works

1. **Input**: Scene narration script and the generated `.mp3` audio.
2. **Execution**: `app/adapters/whisper_aligner.py` runs `openai-whisper` in forced alignment mode.
3. **Output**: An ordered sequence of words with millisecond precision:
   ```json
   [
     { "word": "In", "start": 0.12, "end": 0.28, "confidence": 0.99 },
     { "word": "computer", "start": 0.30, "end": 0.74, "confidence": 0.98 },
     { "word": "science,", "start": 0.76, "end": 1.18, "confidence": 0.96 },
     { "word": "abstraction", "start": 1.34, "end": 1.98, "confidence": 0.99 }
   ]
   ```

### Downstream Uses for Word Timestamps

* **Kinetic Captions**: Highlighting spoken words on screen in real time (karaoke effect).
* **Code Line Highlighting**: Illuminating line 14 of code at the exact millisecond the narrator mentions that specific function.
* **Arrow & Connector Pulses**: Triggering data packets moving across SVG network diagrams in lockstep with the explanation.

---

## 🎚️ Audio Engineering & Mastering

Before final export, the audio pipeline applies a multi-track mixing chain using FFmpeg filtergraphs:

```
[Narration Track] ───┬───────────────────────────────────────────┐
                     │ (Detect voice energy)                     │
                     ▼                                           ▼
[Background Music] ──► [Sidechain Compressor: -18dB Ducking] ──► [Amix Multi-Track]
                                                                        │
                                                                        ▼
                                                         [EBU R128 Loudness Normalizer]
                                                                        │
                                                                        ▼
                                                             Final Master (-14 LUFS)
```

### 1. Dynamic Sidechain Music Ducking
Background music adds cinematic energy but must never drown out speech. When the narrator speaks, the background music volume automatically attenuates by **-18dB**. During pauses or chapter transitions, the music swells back up by **+12dB**.

```bash
ffmpeg -i speech.mp3 -i bgm.mp3 -filter_complex \
  "[1:a]volume=0.25[music]; \
   [music][0:a]sidechaincompress=threshold=0.1:ratio=4:attack=200:release=1000[ducked]; \
   [0:a][ducked]amix=inputs=2:duration=first[master_audio]" \
  -c:a aac -b:a 256k master_audio.m4a
```

### 2. Broadcast Loudness Normalization
All final exports are calibrated to **-14 LUFS (integrated loudness)** with a maximum true peak of **-1.0 dBTP**, adhering to YouTube and streaming platform standards via the `loudnorm` filter:

```bash
ffmpeg -i input.mp4 -af loudnorm=I=-14:TP=-1.0:LRA=7 -c:v copy output_normalized.mp4
```

### 3. Sound Effects (SFX) Integration
Subtle, high-frequency interface sounds (micro-whooshes, mechanical keyboard typing clicks, and pop-in chimes) are automatically mapped to visual entry and exit points to maximize viewer retention.
