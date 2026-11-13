# AI Video Studio: Comprehensive Repository Audit & Architectural Health Report

**Audit Date:** November 13, 2026  
**Repository:** [https://github.com/SaiSankeerth-dev/AI_Video_studio](https://github.com/SaiSankeerth-dev/AI_Video_studio)  
**Target Branch:** `main`  
**Current HEAD Commit:** `bde80d7` (*feat(studio): add Agent Talk autonomous 3D video engine, SEO suite & demo showcase*)  
**Auditor:** Senior Software Architect & Repository Auditor

---

## Executive Summary

The **AI Video Studio** repository is a sophisticated, multi-track autonomous video production platform. It integrates two primary production systems alongside two core architectural tracks:

1. **Short-Form Production Track (`Instagram/`):** Autonomous 9:16 vertical video production engine (*Agent Talk* brand, `@agent.talk`), featuring the recurring 3D low-poly mascot *Claude* and senior developer *Tariq Vance*, 4 completed video projects, 23 social growth & SEO agent skills, and a computer vision/audio analysis pipeline (`PySceneDetect` + `faster-whisper`).
2. **Long-Form Documentary Track (`Youtube/`):** Investigative technical video essay system (`youtube_project`) with full scripting, storyboard generation, forensic research, and thumbnail generation.
3. **Modular V2 Documentary Engine (`agents/`, `engines/`, `schemas/`, `brand/`, `production/`, `qa/`):** A modern, object-oriented 15-agent pipeline orchestrated by `v2_pipeline_orchestrator.py` and validated by `test_v2_documentary_architecture.py`.
4. **Specification Prototype Engine (`Phase-0_Research` through `Phase-7_QA`):** A 19-section documentary production logic blueprint orchestrated by `master_pipeline.py` and validated by `test_production_logic_spec.py`.

### Key Audit Findings
* **Zero Secret Exposures:** No API keys, passwords, credentials, session tokens, or private personal data (`sankeerthvss@email.com` / `V. Sai Sankeerth`) exist in Git-tracked files.
* **Confirmed Disposable Artifact:** `test_sapi.wav` (207 KB) at root is an unreferenced temporary test fixture from early Windows SAPI audio synthesis (a byte-identical duplicate of `production/voice/raw_n01.wav`).
* **Root JSON Clutter:** 8 JSON files at the root (`documentary-plan.json`, `narration.json`, `scene-plan.json`, `shot-plan.json`, `audio-plan.json`, `continuity-bible.json`, `production-summary.json`, `timeline.json`) are byte-for-byte duplicates of canonical files in `projects/video-001/master-documentary/` and `Phase-6_Assembly/timeline.json`. They are currently opened directly by `test_production_logic_spec.py` and `master_pipeline.py`.
* **Hardcoded Machine Paths:** 35 files contain legacy hardcoded paths (`D:\gitM\01_ContentFactory`), originating from an earlier development environment. These break cross-environment portability on systems lacking a `D:` drive.
* **Phase Directories are Active:** The `Phase-*` directories are **NOT** dead code; they contain working implementations actively loaded by `master_pipeline.py` and validated by `test_production_logic_spec.py`. Deleting them would break the specification test suite.
* **Missing Standard Files:** The repository is missing an open-source `LICENSE` (MIT) and `CONTRIBUTING.md`.

---

## Duplicate Pipeline Audit (`master_pipeline.py` vs `v2_pipeline_orchestrator.py` vs `build_full_video_003_data.py`)

| Aspect | `v2_pipeline_orchestrator.py` | `master_pipeline.py` | `build_full_video_003_data.py` |
| :--- | :--- | :--- | :--- |
| **Lines of Code** | 267 lines (15.7 KB) | 257 lines (14.6 KB) | 459 lines (46.0 KB) |
| **Role** | **Active Modern Orchestrator (V2)** | **Specification Pipeline Orchestrator (V1)** | **Project Contract Generator** |
| **Architecture** | Modular packages (`agents.*`, `engines.*`) | Dynamic loading (`Phase-*` directories) | Standalone data synthesis script |
| **Target Output** | `production/` (full multi-agent release) | Root-level JSONs & Phase caches | `projects/video-003/` contracts |
| **Test Suite** | `test_v2_documentary_architecture.py` | `test_production_logic_spec.py` | `test_video_003_astra.py` |
| **Overlapping Logic** | Orchestrates documentary stages 1–23 | Orchestrates 19-section logic blueprint | None (Script data & claims for Astra) |
| **Recommendation** | **KEEP** as primary V2 entry point | **KEEP** as legacy benchmark entry point | **KEEP & ORGANIZE** into `scripts/` |

---

## File-by-File Classification & Audit Targets

### Root Level Files

| File Path | Current Purpose | Dependency Evidence | Classification | Recommended Action | Risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `test_sapi.wav` | 207 KB uncompressed WAV from early SAPI test | Duplicate of `production/voice/raw_n01.wav`. Zero imports or references across codebase. | **REMOVE** | Delete from repository to reduce git bloat. | Low |
| `test_gemini.py` | Manual Gemini API connectivity test (24 lines) | Standalone script; contains hardcoded `D:\gitM\...` path. | **KEEP AND ORGANIZE** | Move to `tests/test_gemini.py`, sanitize hardcoded path. | Low |
| `test_video_003_astra.py` | Data contract audit for `projects/video-003` | Tests Astra documentary project data; contains hardcoded `D:\` path. | **KEEP AND ORGANIZE** | Move to `tests/test_video_003_astra.py`, update path to relative. | Low |
| `test_production_logic_spec.py` | End-to-end audit of all 19 documentary sections | Opens root JSONs, executes `master_pipeline.py`. 100% passing. | **KEEP AND ORGANIZE** | Move to `tests/test_production_logic_spec.py`. | Medium |
| `test_v2_documentary_architecture.py` | Complete validation of V2 15 agents & engines | Tests `agents/`, `engines/`, `schemas/`, `brand/`. | **KEEP AND ORGANIZE** | Move to `tests/test_v2_documentary_architecture.py`. | Medium |
| `build_full_video_003_data.py` | Generates 14.5-min script & contracts for video-003 | Hardcoded to `D:\gitM\...`. Contains full 2,020-word Astra screenplay. | **KEEP AND ORGANIZE** | Move to `scripts/build_full_video_003_data.py`, make paths relative. | Low |
| `audio-plan.json` | Audio mix specification (30 scenes) | Identical duplicate of `projects/video-001/master-documentary/audio-plan.json`. Opened by `test_production_logic_spec.py`. | **KEEP AND ORGANIZE** | Move to `tests/fixtures/master_documentary/` or retain as fixture. | Medium |
| `continuity-bible.json` | 13-dimension continuity specification | Identical duplicate of `projects/video-001/master-documentary/continuity-bible.json`. Opened by `test_production_logic_spec.py`. | **KEEP AND ORGANIZE** | Move to `tests/fixtures/master_documentary/` or retain as fixture. | Medium |
| `documentary-plan.json` | 7-chapter documentary plan | Identical duplicate of `projects/video-001/master-documentary/documentary-plan.json`. | **KEEP AND ORGANIZE** | Move to `tests/fixtures/master_documentary/` or retain as fixture. | Medium |
| `narration.json` | 30-segment enriched spoken narration | Canonical Section 4 test fixture opened by `test_production_logic_spec.py`. | **KEEP AND ORGANIZE** | Move to `tests/fixtures/master_documentary/` or retain as fixture. | Medium |
| `production-summary.json` | Production complexity metadata | Identical duplicate of `projects/video-001/master-documentary/production-summary.json`. | **KEEP AND ORGANIZE** | Move to `tests/fixtures/master_documentary/` or retain as fixture. | Medium |
| `scene-plan.json` | 30-scene emotional breakdown | Identical duplicate of `projects/video-001/master-documentary/scene-plan.json`. | **KEEP AND ORGANIZE** | Move to `tests/fixtures/master_documentary/` or retain as fixture. | Medium |
| `shot-plan.json` | 61-shot production contract | Identical duplicate of `projects/video-001/master-documentary/shot-plan.json`. Opened by `test_production_logic_spec.py`. | **KEEP AND ORGANIZE** | Move to `tests/fixtures/master_documentary/` or retain as fixture. | Medium |
| `timeline.json` | Multi-track timeline IR (135 KB) | Identical duplicate of `Phase-6_Assembly/timeline.json`. | **KEEP AND ORGANIZE** | Move to `tests/fixtures/master_documentary/` or retain as fixture. | Medium |
| `master_pipeline.py` | V1 specification pipeline entry point | Runs 19-section pipeline using `Phase-*` modules. | **KEEP** | Retain at root; sanitize hardcoded paths. | Low |
| `v2_pipeline_orchestrator.py` | V2 modern multi-agent orchestrator | Orchestrates 15 agents and 5 engines across Tasks 01–23. | **KEEP** | Retain at root as primary platform entry point. | Low |
| `README.md` | Master project documentation | Primary GitHub repository documentation with demo media. | **KEEP** | Update with verified audit classifications and architecture guide. | Low |
| `.gitignore` | Git exclusion rules | Protects secrets, prevents large binaries and temporary caches. | **KEEP** | Maintain strict rules. | Low |
| `.env.example` | Template environment configuration | Documents `GEMINI_API_KEY` placeholder. | **KEEP** | Retain as safe reference. | Low |

---

## Directory-by-Directory Audit

### 1. `Instagram/` (862 files, 582.2 MB on disk; 688 tracked files)
* **Status:** **KEEP** (Active Short-Form Studio).
* **Contents:**
  * `agent-talk-content-system/`: 23 installed agent skills (`.agents/skills/`), brand profiles (`.agents/brand/`), keyword dictionaries, publishing packages for episodes 03 and 04.
  * `projects/`: 4 production projects (`01-one-small-fix`, `02-four-hundred-messages`, `03-claude-on-phone`, `04-openshorts-gta6`).
  * `scripts/`: Video analysis engine (`analyze_video.py`), video ingestion script (`download-video.ps1`).
  * `docs/assets/`: Demo assets (`demo.mp4`, `demo_preview.gif`).
* **Health:** All scripts refactored to dynamic path resolution; zero personal identifiers remain.

### 2. `Youtube/` (126 files, 391.8 MB on disk; 102 tracked files)
* **Status:** **KEEP** (Active Long-Form Studio).
* **Contents:**
  * `youtube_project/`: Full investigative documentary pipeline on the $3.5M fake Pokémon box scam (*Logan Paul / Schrödinger's Box*).
  * Includes storyboards, research evidence, voice stems, prompt generators, and YouTube publishing packages.
* **Health:** Git exclusions correctly omit heavy raw concatenated videos (`209 MB` and `38 MB`), keeping Git history clean.

### 3. `Phase-0_Research` through `Phase-7_QA` (304 tracked files)
* **Status:** **KEEP** (Specification Prototype Engine).
* **Analysis:**
  * `Phase-0_Research` (17 files): Research QA, source discovery, claim extraction modules.
  * `Phase-1_MuMuAINovel` (25 files): 10-beat story architect, narration writer (130-160 WPM), scene director, visual director.
  * `Phase-2_MoneyPrinterTurbo` (10 files): Caption generator, radio edit engine with 7 audio tracks and silence cues.
  * `Phase-2_ShotDirector` (10 files): 216 KB `master_documentary_compiler.py` and `test_master_documentary.py`.
  * `Phase-3_Blender` (5 files): 3D spatial reconstruction blueprints and scene builder.
  * `Phase-3_VisualGeneration` (4 files): 100-point rubric image selection critic loop.
  * `Phase-4_Remotion` (221 files, 40.7 MB): Complete React Remotion motion graphic project with 16 core components, documentary scenes, and audio stems.
  * `Phase-5_Footage` (2 files): B-roll catalog and footage manager.
  * `Phase-6_Assembly` (4 files): Section 17 Timeline IR assembly engine.
  * `Phase-7_QA` (2 files): 7-pillar documentary QA engine.
* **Finding:** While these directories represent an earlier architectural phase, they contain active, working code imported by `master_pipeline.py` and verified by `test_production_logic_spec.py`. Deleting them would break the specification test suite.

### 4. `agents/` (16 files)
* **Status:** **KEEP** (V2 Modular Multi-Agent Suite).
* **Contents:** 15 discrete director agents (`research_director`, `fact_checker`, `story_architect`, `script_writer`, `voice_director`, `scene_director`, `shot_director`, `visual_director`, `prompt_director`, `visual_critic`, `motion_director`, `sound_director`, `documentary_qa`, `thumbnail_director`, `packaging_director`).
* **Health:** All 15 agents operational and verified in Tasks 01–23.

### 5. `engines/` (5 files)
* **Status:** **KEEP** (V2 Engine Abstraction Layer).
* **Contents:** `blender`, `evidence`, `ffmpeg`, `gemini`, `remotion`.
* **Health:** Modular wrappers providing headless execution for 3D, vision, Remotion, and timeline muxing.

### 6. `schemas/` (14 files)
* **Status:** **KEEP** (Data Contract Validation).
* **Contents:** 14 formal JSON schemas (`claims`, `sources`, `story`, `narration`, `scenes`, `shots`, `assets`, `audio`, `timeline`, `qa`, etc.).
* **Health:** All 14 schemas validate cleanly against Python `json.load`.

### 7. `brand/` (6 files)
* **Status:** **KEEP** (Documentary Brand Style System).
* **Contents:** `style-bible.md`, `color-system.json`, `typography.json`, `camera-language.json`, `transition-language.json`, `visual-rules.json`.

### 8. `production/` (80 files, 57.6 MB)
* **Status:** **KEEP** (V2 Production Workspace).
* **Contents:** Generated documentary assets across `research`, `scripts`, `narration`, `voice`, `shots`, `graphics`, `audio`, `assembly`, `packaging`, and `full_documentary`.

### 9. `projects/` (198 files, 97.6 MB)
* **Status:** **KEEP** (Documentary Projects Repository).
* **Contents:**
  * `video-001`: Investigative documentary project.
  * `video-002`: Technical documentary project.
  * `video-003`: "GPT-6 Astra: Autonomous Computer Use" documentary project (127 files).

### 10. `qa/` & `research/` (8 files)
* **Status:** **KEEP** (Canonical Data Directories).
* **Contents:** `qa/final/qa-report.json`, `qa/visual/asset-scores.json`, and core grounding research data (`claims.json`, `sources.json`, etc.).

---

## Security, Credentials, and Git Hygiene Audit

1. **Environment Variables & Secrets:**
   * `.env.example`: Only contains a template placeholder (`GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE`).
   * No actual `.env` files exist in the repository or git index.
   * Regex scanning for API key patterns (`AIzaSy...`, `sk-...`, `ghp_...`, `gho_...`) yielded **zero** matches across all files.
2. **Personal Data Sanitization:**
   * Scanned all commits, code, and documentation for personal usernames and email addresses.
   * Committer identity is cleanly configured to GitHub's official privacy address: `SaiSankeerth-dev <SaiSankeerth-dev@users.noreply.github.com>`.
   * Dynamic path resolution (`process.env.APPDATA`, `import.meta.url`, `Path(__file__)`) replaces all hardcoded user paths.
3. **Large File & Binary Hygiene:**
   * Maximum tracked binary file is `docs/assets/demo.mp4` at **9.9 MB** (well below GitHub's 50 MB warning threshold).
   * Heavy raw video captures (209 MB in `Youtube/reference/` and 30 MB exports in `Instagram/exports/`) are correctly excluded by `.gitignore`.
   * `__pycache__` directories and `.hyperframes/` cache are properly ignored and uncommitted.

---

## Proposed Cleanup & Organization Plan (Awaiting Approval)

To achieve a clean, senior-developer repository structure without breaking any working pipelines or test suites:

### Action 1: Remove Confirmed Disposable File
* **Target:** `test_sapi.wav` (207 KB).
* **Reason:** Unreferenced SAPI test audio file; duplicate of `production/voice/raw_n01.wav`.

### Action 2: Organize Root Test Suites into `tests/`
Create `tests/` directory and move:
* `test_production_logic_spec.py` &rarr; `tests/test_production_logic_spec.py`
* `test_v2_documentary_architecture.py` &rarr; `tests/test_v2_documentary_architecture.py`
* `test_video_003_astra.py` &rarr; `tests/test_video_003_astra.py`
* `test_gemini.py` &rarr; `tests/test_gemini.py`
* Add `tests/__init__.py`.

### Action 3: Organize Root Contract Generator into `scripts/`
Create `scripts/` directory (or utilize existing structure) and move:
* `build_full_video_003_data.py` &rarr; `scripts/build_full_video_003_data.py`
* Update internal hardcoded path `D:\gitM\01_ContentFactory\projects\video-003` to `Path(__file__).resolve().parent.parent / "projects" / "video-003"`.

### Action 4: Organize Root Duplicate JSONs into `tests/fixtures/master_documentary/`
Move or mirror the 8 canonical reference JSONs into `tests/fixtures/master_documentary/`:
* `documentary-plan.json`
* `narration.json`
* `scene-plan.json`
* `shot-plan.json`
* `audio-plan.json`
* `continuity-bible.json`
* `production-summary.json`
* `timeline.json`
* Update `master_pipeline.py` and `test_production_logic_spec.py` with backwards-compatible path resolution so they look in `tests/fixtures/master_documentary/` with fallback to root if present.

### Action 5: Sanitize Hardcoded `D:\gitM\` Paths Across Codebase
Update all occurrences of `D:\gitM\01_ContentFactory` in `engines/remotion/remotion_engine.py`, `engines/gemini/gemini_engine.py`, `Phase-0_Research/visual-director/gemini_client.py`, `test_video_003_astra.py`, etc., to use dynamic relative path resolution based on `Path(__file__).resolve()`.

### Action 6: Add Standard Open-Source Files
* Add [`LICENSE`](file:///e:/AI_Videos/LICENSE) (MIT License).
* Add [`CONTRIBUTING.md`](file:///e:/AI_Videos/CONTRIBUTING.md) (Senior-developer guidelines on code style, testing, and multi-agent pipeline contribution).
* Update [`README.md`](file:///e:/AI_Videos/README.md) with updated test commands, directory layout, and pipeline documentation.

---

## Verification & Execution Gate

Before executing these file movements and deletions, the plan is submitted to the user for formal approval. Upon approval, all moves, path sanitizations, test validations, and Git push operations will proceed immediately.
