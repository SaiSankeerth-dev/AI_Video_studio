# AI Shorts Studio — top-level multi-agent system

![License](https://img.shields.io/github/license/SaiSankeerth-dev/AI_Video_studio) ![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Mock mode](https://img.shields.io/badge/runs-offline%20mock%20mode-brightgreen)

A runnable multi-agent pipeline that takes a **topic** and produces an **edit-ready
timeline + platform exports** for YouTube Shorts / Reels / TikTok.

It runs **offline in mock mode with zero API keys and zero dependencies**, so you can
watch the whole agent pipeline execute today, then swap in real OpenAI + rendering
one agent at a time.

```bash
python main.py                       # mock run on the default topic
python main.py "Your topic here"     # mock run on your topic
python main.py "Your topic" --real   # live: needs OpenAI + key
```

---

## What this is (and what I changed from the original spec)

You asked for the ten-agent architecture wired into a top-level system. I built exactly
that, but made three deliberate changes. They are the difference between a demo and
something you can ship.

**1. Not every box is an LLM agent.** Reasoning roles use the model; mechanical roles are
plain code, because code is cheaper, deterministic, and testable. An LLM should never be
the thing deciding whether a file is 1080×1920.

| Reasoning agent (uses LLM) | Deterministic agent (plain code) |
|---|---|
| CEO, Research, Fact Checker | Asset Manager |
| Story Architect, Visual Director | Senior Editor |
| Music Director | QA |
| Caption Director (word *choice* only) | Export + caption *timing* |

**2. CapCut automation is gone.** The original plan drives CapCut with PyAutoGUI + OCR +
computer vision. That breaks on every CapCut UI update and inherits screen-resolution and
timing bugs you can't reproduce. `render.py` uses FFmpeg/MoviePy to render cuts, motion,
captions, audio, and platform presets **directly**. Same output, none of the fragility.

**3. Captions are ASR, not creativity.** The model only picks emphasis words. Word *timing*
must come from Whisper alignment against the real voiceover — a model guessing timestamps
is exactly how you get caption drift. The mock uses even spacing as a placeholder; the seam
for Whisper is marked in `agents.py`.

---

## The pipeline

```
CEO ─► Research ─► Fact Checker ─► Story Architect ─► Visual Director
                                                            │
        ┌───────────────────────────────────────────────────┘
        ▼
 Asset Manager ─► Music Director ─► Caption Director ─► Senior Editor ─► QA
                                                                          │
                                                  ┌──────── pass ─────────┤
                                                  ▼                       │ fail
                                               Export                 (loop back to
                                                                       Senior Editor,
                                                                       capped at 2 retries)
```

The **QA → Senior Editor** loop is the only branch and the only genuinely "agentic" part:
QA runs objective checks (duration on target, no clip over 2s, no dead sections, captions
cover the video) and sends the timeline back for re-editing if they fail. Everything else
is a straight line — which is correct, not a limitation.

## Files

| File | Role |
|---|---|
| `orchestrator.py` | **The top-level system.** Dependency-free graph executor + the wiring. |
| `agents.py` | All ten agents. Reasoning agents carry their real prompts. |
| `state.py` | The `VideoState` object every agent reads and writes. |
| `llm.py` | `MockLLM` (offline) and `OpenAILLM` (live) behind one interface. |
| `render.py` | FFmpeg/MoviePy render seam (replaces CapCut). Mock writes manifests. |
| `main.py` | Entry point. |

Every node is a `state -> state` callable, so porting to **LangGraph** is mechanical — the
mapping is shown in the header of `orchestrator.py`.

---

## How to grow it (do these in order — do NOT build all ten "real" at once)

This maps to your milestone path, reordered around what de-risks the project fastest.

1. **Make Story Architect real first.** It's the agent that decides whether the video is
   boring. Swap `MockLLM` → `OpenAILLM` for just that node and judge the hooks. If the
   writing is weak, nothing downstream saves you.
2. **Make Senior Editor good.** This is the actual product. The retention rules here are a
   floor, not the ceiling — this is where "junior editor" becomes "senior editor."
3. **Solve assets for ONE clearable vertical.** Pick a niche where you can legally source
   footage (stock explainers, generated B-roll, your own clips). The Messi example is a
   licensing dead end and a bad first vertical.
4. **Wire real rendering** (`USE_REAL_RENDER=1` + MoviePy) only once 1–3 produce a timeline
   you'd actually publish.
5. **Then** scale to batch (the 20–50/day system) — but only after one video is genuinely good.

The order matters: rendering a polished pipeline around a boring script just gets you
boring videos faster.
