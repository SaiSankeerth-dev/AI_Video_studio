# Multi-Agent Video Editor — System Design

A specification for an autonomous "senior video editor" built as a team of cooperating agents.
It asks for the **theme first**, confirms the **collection mode**, gathers everything a real
editor needs, then assembles an edit plan ready to build in **CapCut**.

> **Reality check (read this once).** No agent can pull broadcast/copyrighted match footage and
> render a finished film unattended — that footage is legally off-limits and there is no headless
> video renderer in this setup. What this system *does* deliver is a complete, drag-and-drop-ready
> CapCut package: script, timestamped shot list, transitions, music, overlays, plus **legally
> usable** sourced clips. Final assembly is a ~20-minute job in CapCut, not a research project.

---

## 1. The three collection modes

| Mode | You provide | Agent provides | Use when |
|------|-------------|----------------|----------|
| **User Assets** | All clips, voiceover, script, images, audio | Editing, sequencing, transitions, export plan | You already shot/own everything |
| **Autonomous** | Just the theme | Everything, sourced from legal/free libraries only | You have nothing and want a fast draft |
| **Hybrid** ⭐ *(default)* | Some assets (e.g. your VO, a few clips) | Fills every gap from legal/free libraries | Most real projects |

**Default = Hybrid.** Before sourcing anything, the system lists what it plans to fetch and asks
for a yes/no. Nothing is downloaded without that confirmation.

---

## 2. Standard workflow (theme-first)

```
1. ASK THEME      → "What's the video about?"  (+ length, platform, tone, deadline)
2. CONFIRM MODE   → default Hybrid; show what you'll supply vs. what I'll source
3. ASK PERMISSION → list assets to be collected + their licences → wait for yes
4. COLLECT        → b-roll, music, SFX, stills, captions (legal sources only)
5. PLAN THE EDIT  → script, shot list, transitions, overlays, music sync
6. ASSEMBLE GUIDE → exact CapCut steps (import order, trims, effects, export)
7. QA            → licence check, pacing, audio levels, caption accuracy
```

---

## 3. The agent team (how the work is divided)

Each agent owns one job, mirrors how a real post-production team is split, and hands a clean
artifact to the next. The **Director** is the only one that talks to you.

### 🎬 Director / Producer  *(orchestrator)*
- Asks the theme and the clarifying questions; locks the brief.
- Confirms collection mode and gets sourcing permission.
- Delegates to the specialists, resolves conflicts, owns the final timeline.
- **Output:** the locked brief + final edit blueprint.

### 🔎 Research & Asset-Collection Agent
- Researches the theme (facts, key moments, current status).
- Sources b-roll, stills, music, SFX **from legal libraries only** (CC0, Creative Commons,
  public domain, licensed stock).
- Logs every asset with its source URL and licence in `ASSET_LICENCES.md`.
- **Output:** populated `03_Assets/` folder + licence ledger.

### ✍️ Script & Story Agent
- Writes the narrative arc, voiceover script, and on-screen text.
- Times each line so the shot list can sync to it.
- **Output:** `Script_and_VO.md`.

### ✂️ Editor Agent
- Builds the timestamped shot list / EDL — what clip plays when, and for how long.
- Sets pacing (cuts-per-second by section) and clip trims.
- **Output:** `Shot_List_EDL.md`.

### ✨ Transitions & FX Agent
- Chooses transitions per cut (hard cut, whip pan, zoom, glitch, match cut) and any effects,
  speed ramps, or text animations.
- **Output:** transition map inside the edit blueprint.

### 🔊 Audio Agent
- Picks the music track(s), marks beat-drop sync points, plans SFX, sets ducking under VO,
  and target loudness (−14 LUFS for social).
- **Output:** `Music_and_Audio_Plan.md`.

### ✅ QA Agent
- Verifies every asset is cleared, captions are accurate, pacing holds, audio is balanced,
  and the export preset matches the target platform.
- **Output:** QA checklist sign-off.

```
        ┌─────────────┐
        │  DIRECTOR    │◄──── talks to you (theme, mode, permission)
        └──────┬───────┘
   ┌─────┬─────┼─────┬──────┐
   ▼     ▼     ▼     ▼      ▼
Research Script Editor Transitions Audio
   └─────┴─────┴─────┴──────┘
              ▼
            QA ──► Final CapCut blueprint
```

---

## 4. Folder layout

```
FIFA_2026_Video_Project/
├─ 01_System/        ← this spec
├─ 02_FIFA_2026_Edit/← worked example: 2026 World Cup hype edit
│   ├─ Script_and_VO.md
│   ├─ Shot_List_EDL.md
│   ├─ Music_and_Audio_Plan.md
│   ├─ CapCut_Assembly_Guide.md
│   └─ ASSET_SOURCES.md
└─ 03_Assets/        ← drop downloaded files here
    ├─ Video_Clips/
    ├─ Audio_Music/
    ├─ Voiceover/
    └─ Images_Graphics/
```

## 5. Hard rules
- **Theme first, always.** No work starts before the brief is locked.
- **Permission before download.** Hybrid/Autonomous list assets + licences and wait for yes.
- **Legal-only sourcing.** CC0 / Creative Commons / public domain / licensed stock. No
  broadcast match footage, no ripped clips, no copyrighted music. Logged in a licence ledger.
- **CapCut is the assembly target.** Every plan ends in concrete CapCut steps.
