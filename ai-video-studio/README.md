# 🎬 AI Video Studio — a multi-agent short-form video editor

> **Status: prototype / research preview.** This is a working proof-of-concept, not a
> production product. The agent pipeline runs end-to-end **offline with zero API keys**
> (mock mode), produces an **editable CapCut draft**, and can render a **finished MP4**
> directly with ffmpeg. Two example videos are included. Read the
> [Limitations](#-limitations--honesty) before expecting a polished broadcast reel.

You give it a **topic**. A team of cooperating agents — acting like a small post-production
house — researches it, writes a retention-first script, plans the shots, sources legally
usable assets, builds a timeline, QAs it, and hands you back either a **CapCut project to
finish by hand** or a **rendered vertical video**.

---

## ✨ What works today

| Capability | State |
|---|---|
| 10-role multi-agent pipeline (CEO → Research → … → QA → Export) | ✅ runs offline (mock LLM) |
| Swap mock → real model (OpenAI / Gemini / local Ollama) | ✅ one flag |
| Three asset modes: **User / Autonomous / Hybrid** | ✅ |
| Autonomous stock sourcing (Pexels) + offline generated B-roll | ✅ (key optional) |
| **CapCut draft export** — opens with clips, trims, transitions on the timeline | ✅ `tools/build_fifa_capcut.py` |
| **Direct MP4 render** (typography teaser, motion, crossfades, audio bed) | ✅ `tools/build_teaser.py`, `tools/build_cricket.py` |
| QA → re-edit feedback loop (the only truly "agentic" branch) | ✅ |
| Real footage edit (cut to a script behind titles) | ⛔ needs licensed footage / Pexels key |

---

## 🧩 The three asset modes

1. **User Assets** — you provide every clip, voiceover, image and track; agents only edit.
2. **Autonomous** — give just a topic; agents source legally-usable assets (Pexels stock, or
   fully-offline generated B-roll cards). Nothing unclearable can reach the timeline.
3. **Hybrid** *(preferred)* — you provide some assets; agents fill the gaps automatically.

```bash
python main.py "Sunset facts" --asset-mode hybrid --assets ./my_clips --capcut
```

---

## 🤖 The agent team

```
CEO ─► Research ─► Fact Checker ─► Story Architect ─► Visual Director
                                                          │
      ┌────────────────────────────────────────────────────┘
      ▼
Asset Manager ─► Music Director ─► Caption Director ─► Senior Editor ─► QA
                                                                        │
                                                ┌──────── pass ─────────┤
                                                ▼                       │ fail
                                             Export                 (loop back to
                                                                     Senior Editor,
                                                                     max 2 retries)
```

**A deliberate design choice:** not every box is an LLM. Reasoning roles (CEO, Research, Story
Architect, Visual/Music/Caption Director) use the model; mechanical roles (Asset Manager,
Senior Editor, QA, Export, caption *timing*) are plain, testable code. An LLM should never be
the thing deciding whether a file is 1080×1920. Every node is a `state -> state` callable, so
porting to LangGraph is mechanical.

---

## 🎞️ How a video actually gets made

Two output paths, both real:

- **CapCut draft** (`capcut.py`) — writes a CapCut *project on disk* (clips placed in order,
  trimmed, transitions between cuts). You open CapCut and it's there to finish by hand. This
  replaces fragile GUI automation: no clicking pixels, no breaking on UI updates.
- **Direct render** (`render.py` + the ffmpeg `tools/`) — renders a finished MP4
  deterministically (cuts, motion, captions, audio, platform presets).

---

## 🚀 Quickstart

```bash
# 1. Run the agent pipeline offline (no keys, no deps)
python main.py "Your topic here"

# 2. Render a typography hype teaser to MP4 (needs ffmpeg + a bold .ttf)
python tools/build_teaser.py        # FIFA World Cup 2026 example
python tools/build_cricket.py       # Cricket ground example

# 3. Generate an editable CapCut draft (Windows + CapCut installed)
python tools/build_fifa_capcut.py
```

Live model (optional):

```bash
pip install openai && export OPENAI_API_KEY=...   &&  python main.py "Topic" --real
# or --gemini (GEMINI_API_KEY) / --ollama (local, no key)
export PEXELS_API_KEY=...   # autonomous/hybrid real stock footage
```

---

## 🎥 Example outputs

Two finished 1080×1920 / 30 fps teasers rendered by this prototype live in [`examples/`](examples/):

- `FIFA_World_Cup_2026_Hype.mp4` — 24 s World Cup 2026 hype teaser.
- `Cricket_Ground_Hype.mp4` — 24 s cricket-ground hype teaser.

Both are **typography teasers** (animated titles on dynamic gradients) — the style that looks
professional *without* licensed footage. See [Limitations](#-limitations--honesty).

---

## 🗂️ Repo layout

```
ai-video-studio/
├── main.py              # entry point
├── orchestrator.py      # the dependency-free agent graph executor
├── agents.py            # all 10 agents + their prompts
├── state.py             # the VideoState passed between agents
├── llm.py               # Mock / OpenAI / Gemini / Ollama behind one interface
├── assets.py            # 3-mode asset sourcing (user / auto / hybrid)
├── render.py            # ffmpeg/moviepy render seam
├── capcut.py            # CapCut draft generator
├── tools/               # runnable demos (CapCut draft + ffmpeg teasers)
├── docs/                # system design + a full worked FIFA pre-production package
└── examples/            # rendered example MP4s
```

---

## 🧭 Roadmap

1. Make **Story Architect** real first — it decides whether the video is boring.
2. Make **Senior Editor** good — this is the actual product (retention rules → real craft).
3. Solve assets for **one** clearable vertical (stock/explainer/generated, not licensed sport).
4. Wire **real footage** rendering once 1–3 produce a timeline worth publishing.
5. Then scale to batch (20–50 videos/day).

---

## ⚠️ Limitations & honesty

- **Mock mode is generic.** Offline, the bundled `MockLLM` returns canned content; real scripts
  need a real model (`--real` / `--gemini` / `--ollama`).
- **No licensed footage.** Broadcast/sports footage is rights-locked and cannot be auto-sourced.
  Without a Pexels key or your own clips, autonomous mode falls back to generated B-roll cards;
  the included examples are therefore **typography teasers**, not footage reels.
- **CapCut draft schema is version-sensitive.** Targeted at CapCut 8.3.0 / draft v360000. A
  future CapCut may reject hand-built drafts; the reliable fix is to template from a known-good
  draft.
- This is a **prototype** — APIs, structure and prompts will change.

## 📄 License

MIT — see [LICENSE](LICENSE).
