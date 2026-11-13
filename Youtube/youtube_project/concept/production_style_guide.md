# Production Style Guide: Forensic Documentary & Motion Narrative

**Origin Style Reference**: Fern Forensic Investigative Documentary Style  
**Production Target**: Original High-End Animated YouTube Documentary  
**Version**: 1.0  

---

## 1. Visual Identity & Artistic Direction

### The "Forensic Archive" Aesthetic
The visual philosophy blends physical archival realism with ultra-modern digital motion design.
* **Tactile Skeuomorphism**: Flat graphics are avoided. All primary objects (documents, physical artifacts, certificates, microchips, trading slabs) possess simulated physical weight, bevels, paper fiber textures, and directional lighting.
* **Forensic Overlays**: Digital crosshairs, millimeter measurement rules, optical zoom loupes, timestamp codes, and coordinate grids that make the viewer feel like they are inside a specialized laboratory or forensic workstation.
* **Contrast of Epochs**: High-contrast juxtaposition between retro analog artifacts (1990s retro screens, vintage dot matrix prints, VHS static) and high-precision modern forensic analysis (microscopic electron sweeps, 3D CAD models, digital waveforms).

---

## 2. Color Palette & Lighting Direction

### A. Primary Color Tokens
* **Void Charcoal (Canvas Base)**: `#0F1115` — Deep, neutral dark grey that gives maximum contrast without pure `#000000` clipping.
* **Archival Parchment (Physical Elements)**: `#F5EFEB` — Warm off-white for documents, casefiles, paper clippings, and cards.
* **Evidence Amber (Warning / Scam Alerts)**: `#FF9F1C` — High-intensity warm gold/amber used for fraudulent elements, warning boxes, and critical data points.
* **Forensic Cyan (Detection / Digital Wireframes)**: `#00E5FF` — Sharp, clinical cyan used for digital microscope reticles, laser lines, and measurements.
* **Ink Black (Typography & Linework)**: `#1A1D20` — Deep pigment black for printed text on parchment.

### B. Lighting & Atmosphere
* **Directional Studio Key Light**: Placed top-left (approx. -45° azimuth, 60° elevation) producing soft drop shadows (`rgba(0, 0, 0, 0.45)` with 24px blur and 12px offset).
* **Edge Rim Lighting**: Subtle top/right rim highlights on 3D elements and glass slabs to cleanly separate foreground evidence from the dark background.
* **Vignette & Focus Falloff**: 15–20% edge vignette on full-frame scenes to draw viewer gaze to the center thirds.

---

## 3. Cinematography & Camera Movement Language

### Camera Motion Principles
1. **Never Truly Static**: Every scene must have a camera move—either a slow 1.02x–1.08x scale push-in over 4 seconds, a lateral slow pan, or an isometric tilt.
2. **The "Macro Dive" (Signature Move)**:
   * Smooth zoom from wide context shot directly into microscopic detail (e.g., from an entire document down to a 50x zoom on halftone ink rosettes).
   * Accelerates smoothly (`cubic-bezier(0.25, 1, 0.5, 1)`) into the target detail.
3. **Parallax Depth Layers**:
   * **Foreground**: Floating dust particles, glass reflections, or magnifying reticle.
   * **Midground (Focus Plane)**: The primary evidence artifact.
   * **Background**: Desaturated, blurred forensic lab environment or grid plane with depth-of-field blur (`blur(8px)` to `blur(16px)`).

---

## 4. Typography & On-Screen Text

* **Display / Headline Font**: Clean, bold grotesque sans-serif (e.g., *Inter*, *Helvetica Neue*, or *Space Grotesk* Bold) set in ALL CAPS for major section titles and financial sums.
* **Forensic / Metadata Font**: Monospaced font (e.g., *JetBrains Mono*, *Courier Prime*, or *Space Mono*) for timestamps, serial numbers, coordinates, and technical printer specs.
* **Kinetic Text Animations**:
   * Numbers roll or count up with high-speed ticker easing.
   * Critical quotes appear with typewriter cadence and subtle cursor blink.
   * Key words highlight with an animated translucent marker brush stroke in amber (`rgba(255, 159, 28, 0.35)`).

---

## 5. Editing Rhythm & Pacing Architecture

* **The 2.5-Second Rule**: The eye must receive fresh visual stimulation every 1.5 to 2.8 seconds.
* **Pacing Taxonomy**:
  * *Setup & Premise*: Deliberate, suspenseful shot transitions (2.5s – 4s per shot).
  * *Investigation & Unraveling*: Quickening tempo (1.2s – 2.0s per shot), rapid montage of evidence documents, forum posts, and microscopic comparisons.
  * *The Reveal / Smoking Gun*: Sudden rhythm halt. A dramatic hold (3s) with stark silence or a single sub-bass pulse, letting the gravity of the discovery land.
* **Transitions**:
  * *Tactile Snap*: Quick hard cut coupled with an acoustic shutter click or paper flick.
  * *Optical Whip*: Fast directional blur transition (`motion_blur` / whip pan) between investigative threads.
  * *Light Leak / Lens Flash*: Subtle chromatic bloom when jumping between macro lens details.

---

## 6. Sound Design & Audio Architecture

### A. Loudness & Technical Target
* **Broadcast Standard**: Target integrated loudness **-14.0 LUFS** (±0.5 LUFS).
* **True Peak Ceiling**: **-1.0 dBFS** to prevent clipping across streaming codecs.
* **Loudness Range (LRA)**: 3.5 – 5.0 LU for consistent, effortless intelligibility.

### B. Audio Stems
1. **Narration (Dialogue)**:
   * Dry, intimate broadcast proximity effect.
   * High-pass filtered at 75 Hz (18 dB/oct) to eliminate rumble; gentle dip at 350 Hz to prevent muddiness; presence boost at 4.5 kHz.
2. **Foley & Diegetic SFX**:
   * Physical sounds: high-fidelity paper slides, heavy desk thuds, plastic slab clicks, camera shutter clicks.
   * Micro-mechanics: subtle ticking, typewriter strikes, tape-recorder whirrs.
3. **Sub-Bass & Drone Beds**:
   * Low-frequency sine/saw pulses (45 Hz – 60 Hz) underneath tension-building narrative sections.
4. **Music Bed**:
   * Minimalist dark ambient synth arpeggios, subtle pulsing basslines, rhythmic clockwork percussions.
   * Heavy dynamic ducking (-12 dB) whenever narration is active.

---

## 7. Pipeline Toolchain Implementation

| Requirement | Implementation Tool |
| :--- | :--- |
| **Motion Graphics & 2.5D Scenes** | Hyperframes / Canvas / SVG / HTML5 CSS motion engine |
| **Video Editing & Compositing** | FFmpeg with complex filtergraphs (zooms, pans, overlays, color grade) |
| **Audio Voiceover Synthesis** | Kokoro TTS / Python neural TTS engine (clean broadcast timbre) |
| **Sound Design & Foley Assembly**| Multi-channel audio mixer via FFmpeg `amix` & `apad` filter chains |
| **Audio Mastering** | FFmpeg `loudnorm` filter (dual-pass EBU R128 mastering to -14.0 LUFS) |
| **Quality Verification** | FFprobe stream inspection & automated perceptual quality scoring |
