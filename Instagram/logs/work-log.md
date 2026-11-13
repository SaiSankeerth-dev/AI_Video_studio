# AI Videos Work Log

All completed milestones and recorded artifacts are tracked here. New downloads, projects, renders, and logs should be recorded under `E:\AI_Videos`.

## 2026-11-12

1. **Windows Base Environment Preserved**
   - Host `Node.js v24.14.0`, `Python 3.12.10`, `%USERPROFILE%\video-tools`, `%USERPROFILE%\lemo-opuscar`, and global skills (`agent-reach`, `hyperframes`) kept intact while Windows Smart App Control / McAfee remain active.

2. **Ubuntu WSL2 Native Setup (`Agent Reach 1.6.1` + `OpenCLI 2.0.3` + `CloakBrowser 0.6.3`)**
   - Verified native Linux tools: `node v22.23.5`, `npm 10.9.9`, `python3 3.14.4`, `uv 0.13.7`, `opencli 2.0.3`, `agent-reach 1.6.1`.
   - Installed missing Chromium runtime libs (`libnspr4`, `libnss3`, `libasound2t64`, `fonts-liberation`) and pinned `playwright==1.58.0` in `~/.agent-reach/tools/cloakbrowser/venv/`.
   - Authenticated Instagram manually via WSLg headed CloakBrowser (`agent-reach login instagram`), verified persistent profile at `~/.agent-reach/browser/profile` (`opencli_context: 7v6wdpkp`, `extension_version: 1.0.27`).
   - Added user-space OpenCLI Instagram overrides in `~/.opencli/clis/instagram/` (`search.js`, `profile.js`, `user.js`) with a mirror snapshot saved at `E:\AI_Videos\logs\backups\opencli-instagram\`.
   - Verified `agent-reach check instagram --text` (`3/3 actions working`: `search`, `profile`, `posts`) plus `explore`, `saved`, `search`, `profile`, and `user` after a full `agent-reach browser stop` restart.

3. **`yt-dlp` Setup & Instagram Reel Verification (`DfH96xeqX-9`)**
   - Installed `yt-dlp 2026.10.26` (`yt-dlp[default]`) via `uv` at `~/.local/bin/yt-dlp` and linked `~/.local/bin/ffmpeg`.
   - Downloaded `https://www.instagram.com/reel/DfH96xeqX-9/` cleanly into `E:\AI_Videos\downloads\instagram\DfH96xeqX-9.mp4` (`9,604,968` bytes).
   - Inspected video and audio (`00:00`–`01:13`): low-poly 3D animation about an AI opening a 214-file PR (`#482`) for a 1-typo fix, introducing `multica-ai/andrej-karpathy-skills` (`CLAUDE.md` Surgical Changes), fixing `#483` in 1 line, and flagging dead billing code (`payments: 0 since March`).

4. **Workspace Organized Under `E:\AI_Videos`**
   - Created `downloads/`, `projects/`, `assets/`, `exports/`, `scripts/`, `docs/`, and `logs/`.
   - Added `scripts/download-video.ps1` and `scripts/workspace-status.ps1`.

5. **AI Video Production: "One Small Fix" (Reference-Based Original Production)**
   - **Reference Video:** `https://www.instagram.com/reel/DfH96xeqX-9/` (`reference/reference_video.mp4`, 29 cuts, 73.97 s).
   - **Phase 1 (Reference Analysis):** Documented complete timestamp breakdown in `reference/reference_analysis.md` and shot list in `reference/reference_storyboard.md` (29 shots, 23.5 cuts/min, pacing curve, curiosity loops, dead silence punchline).
   - **Phase 2 (Character Design & Mascot Update):** Designed human developer **Tariq Vance** (olive skin, gold wire spectacles, ocean teal beanie, navy bomber). Updated AI companion mascot to **Claude** based on the user's uploaded reference image (`.user_uploaded/media_1794503864465_6bde76ff.jpg`): wide rounded terracotta cuboid, dark angled rectangular button eyes (`/ \`), curved antenna stalks with glowing golden bulbs, floating translucent terminal visor with `>_` and dynamic audio spectrum bars, glowing Claude starburst emblem, `"AI"` badge, 4 pillar legs, and side arms. Documented in `character/character_bible.md`.
   - **Phases 3 & 4 (Script & Storyboard):** Authored 24-line dialogue script in `script/final_script.md` and 29-shot storyboard in `storyboard/storyboard.md`.
   - **Phase 5 (Audio & Subtitles):** Synthesized all 24 voice lines at 48 kHz stereo using local Kokoro-82M (`am_michael` for Tariq, `af_nova` for Claude), normalized to `-16 LUFS`. Mixed with CC0 lofi BGM (`vanilla_lofi_cc0.mp3`) trimmed to 76.0 s with a sharp cut to digital zero (`-120 dB`) dead silence across Shots 28–29. Generated 39-cue subtitle file in `subtitles/final_subtitles.srt`.
   - **Phase 6 (3D Scene Engine & UI Cards):** Built procedural Three.js WebGL scene in `project/hyperframes/assets/scene3d.js` featuring Tariq, Claude, laptop with Claude decal, coffee mug with Claude decal, books, and cozy studio lighting. Created 8 dark GitHub UI cards in `project/hyperframes/assets/cards.js` and upper-band mobile-safe HUD in `project/hyperframes/assets/styles.css` (`y = 205 px`).
   - **Phase 7 & 8 (Rendering & QA Iterations):**
     - **Iteration 01:** Rendered `renders/iteration_01.mp4` (`1080 × 1920`, `30.00 fps`, `79.03 s`, `28.6 MB`). Scored **9.37 / 10.00** in `reports/quality_report_iteration_01.md`. Diagnosed desk lamp encroachment in Claude close-ups, thin starburst spokes, flat button eyes, and competing background terminal opacity.
     - **Iteration 02:** Repositioned desk lamp to `x = 0.14` (completely clearing Claude's close-up camera frustum), thickened starburst spokes by 57% with boosted amber core emissivity (`0.72`), added obsidian specular sheen to button eyes, and softened background terminal opacity to `0.35`. Rendered `renders/iteration_02.mp4` (`1080 × 1920`, `30.00 fps`, `79.03 s`, `28.7 MB`). Extracted 16 frames and built `contact_sheet_4x4.jpg`. Evaluated in `reports/quality_report_iteration_02.md` with weighted score **9.71 / 10.00** (exceeding the >= 9.50/10.00 goal).
   - **Final Release & Promotion:**
     - Promoted to `renders/final_video.mp4` and exported to `E:\AI_Videos\exports\01_one_small_fix_final.mp4`.
     - Generated comprehensive reports: `reports/quality_report.md`, `reports/reference_match_report.md`, and `reports/iteration_history.md`.

## 2026-11-13

6. **Workspace Reorganization to `E:\AI_Videos\Instagram`**
   - Per direct user instruction, all assets, documentation, downloads, exports, logs, projects, and scripts were moved into `E:\AI_Videos\Instagram`.
   - `E:\AI_Videos` now exclusively houses the `Instagram` directory.
   - Updated `scripts/download-video.ps1` to target `E:\AI_Videos\Instagram\downloads` and `/mnt/e/AI_Videos/Instagram/downloads/$Platform`.
   - Strict invariant established: all current and future project deliverables, downloads, scripts, assets, and renders will be stored inside `E:\AI_Videos\Instagram` only.

7. **Agent Talk Video Production: "Run Claude Code From Your Phone (T3 Code)"**
   - **Source Post:** `https://www.instagram.com/p/Dfquw4KBL47/` (`downloads\instagram\Dfquw4KBL47.mp4`, 33.7 s).
   - **Topic Analysis:** Ingested source post about **T3 Code** (open-source mobile bridge for Claude Code, Codex, Cursor, Grok, and Antigravity, 52k+ stars, BYOS model). Documented in `projects/03-claude-on-phone/reference/topic_analysis.md`.
   - **Character Design:** Adopted user's uploaded pixel reference (`media_1794581540347_e1ff6bf3.png`): terracotta cuboid body, 4 pillar legs, 2 side arms, dual tilted rectangular button eyes `/ \`, glowing golden antenna bulbs, floating audio spectrum visor, glowing starburst emblem, and AI badge. Documented in `character/character_bible.md`.
   - **Script & Storyboard:** Authored 8-scene script and storyboard in `script/final_script.md` and `storyboard/storyboard.md`.
   - **Audio Production:** Synthesized 8 dialogue lines (`L01`–`L08`) at 48 kHz stereo using Kokoro-82M (`af_nova`), normalized to `-16 LUFS`. Mixed with modern tech lo-fi BGM (`-20 LUFS`) and layered with UI sound effects (notification, pop, whooshes, click, chime). Subtitles written to `subtitles/final_subtitles.srt`.
   - **3D & HyperFrames Composition:** Built procedural Three.js WebGL scene with Claude standing on a sleek OLED smartphone, dark navy studio with warm tungsten lighting and fairy light bokeh, floating dark UI cards, and interactive button state changes.
   - **Render & Quality Assurance:** Rendered `renders/iteration_01.mp4` (`1080 × 1920`, `30.00 fps`, `47.00 s`, `10.3 MB`). Extracted 16 frames and built `contact_sheet_4x4.jpg`. Evaluated across the 8-category rubric with a validated score of **9.75 / 10.00** (exceeding the >= 9.50 requirement).
   - **Final Release & Promotion:**
     - Promoted to `projects/03-claude-on-phone/renders/final_video.mp4`.
     - Exported to `E:\AI_Videos\Instagram\exports\03_claude_on_phone_final.mp4`.
     - Quality report written to `projects/03-claude-on-phone/reports/quality_report.md`.

8. **Agent Talk Remake: Two-Character Conversation (Tariq Vance + Pixel-Accurate Claude Mascot)**
   - **User Directive:**
     1. Adopt the user-uploaded pixel mascot reference (`media_1794583368294_98c1c419.png`) for Claude: clean low-poly terracotta cuboid body (`#D47F53`), two upright square black eyes, two rectangular side arm blocks, and four vertical square block pillar legs (strictly omitting antennas, bulbs, visor, starburst, and AI badge). Maintain this design for all future videos.
     2. Rebuild the video as an authentic **two-character conversation** between the human developer (**Tariq Vance**) and the AI mascot (**Claude**)—matching the dynamic, humor, and relatability of the previous video ("One Small Fix")—while remaining strictly focused on the **T3 Code** topic from `https://www.instagram.com/p/Dfquw4KBL47/`.
     3. Ensure Tariq Vance is clearly visible and prominently framed in the scene.
   - **Script & Audio:** Authored 19-line conversational script spanning 68.5 s. Synthesized lines using local Kokoro-82M (`am_michael` for Tariq, `af_nova` for Claude) and normalized with ffmpeg broadcast loudnorm (`-16 LUFS`). Loop-extended synth music bed and layered tactical SFX (buzz, notification, click, chime, alert drop). Subtitles written to `subtitles/final_subtitles.srt`.
   - **3D Scene Engine & Cinematography:**
     - Restored **Tariq Vance** seated at the desk opposite Claude, with his gold wireframe glasses, ocean-teal beanie, navy bomber jacket, animated brows, and lip-sync.
     - Redesigned **Claude** to match the pure terracotta block mascot.
     - Positioned Tariq at `(-0.78, 0.0, 0.14)` and Claude perched on books at `(0.82, 1.19, 0.18)` with a smartphone on the desk at `(0.08, 1.01, 0.52)` displaying the live diff UI.
     - Configured camera shot modes: `tariq_cu` (tight cross-desk close-up on Tariq's face and glasses), `claude_cu` (close-up on mascot), `phone_cu` (dive-in to mobile diff card), and `wide_desk` (two-shot establishing context).
   - **Rendering & Visual Verification:**
     - Rendered `renders/iteration_03.mp4` (`1080 × 1920`, `30.00 fps`, `68.50 s`, `23.7 MB`).
     - Extracted 16 frames to `renders/_iteration_03_frames/` and generated `contact_sheet_4x4.jpg`. Visually verified Tariq Vance is clearly visible, expressive, and center-stage in all his shots.
     - QA Score: **9.75 / 10.00** (documented in `reports/quality_report.md`).
   - **Final Release & Promotion:**
     - Promoted to [`projects/03-claude-on-phone/renders/final_video.mp4`](file:///E:/AI_Videos/Instagram/projects/03-claude-on-phone/renders/final_video.mp4).
     - Exported to [`E:\AI_Videos\Instagram\exports\03_claude_on_phone_final.mp4`](file:///E:/AI_Videos/Instagram/exports/03_claude_on_phone_final.mp4).


9. **Agent Talk Episode 04: "The GTA 6 AI Clip Farm (OpenShorts)"**
   - **Reference Inspiration:** `https://www.instagram.com/reel/Dfmp-V4hDF1/` (Downloaded to `downloads/ref_Dfmp-V4hDF1.mp4`, analyzed in `projects/04-openshorts-gta6/reference_analysis.md`).
   - **Concept & Narrative:** Can developers and creators actually get rich automatically clipping 8-hour live streams with AI? Tariq Vance and Claude explore the hype, demonstrate the real-world open-source tool **OpenShorts** (`mutonby/openshorts`, 8.0k stars on GitHub, MIT license, Docker, MCP server), and deliver a sharp reality check on YouTube's Reused Content monetization policy and publisher copyright.
   - **Character Continuity:** Pinned Tariq Vance (gold glasses, teal beanie, navy bomber jacket) and Claude (our retro terracotta cuboid mascot `#D47F53`, 4 block legs, 2 block arms, 2 black eyes).
   - **Audio Production:** Synthesized 19 dialogue lines using Kokoro TTS (`am_michael` for Tariq, `af_nova` for Claude), loudness-normalized to `-16 LUFS`, mixed with warm tech synth groove and layered UI SFX (`pop`, `whoosh`, `click`, `chime`, `impact-bass-1`, `error`).
   - **Cinematography & UI:** Implemented dynamic alternating camera presets (`tariq_cu`, `claude_cu`, `two_shot`) with the 3-part tabbed navigation card (`1. What People Say`, `2. How To Do It Free`, `3. Is It Real?`) and animated waveform visualizer.
   - **Rendering & Output:** Rendered `renders/04_openshorts_gta6_final.mp4` (`1080 × 1920`, `30 fps`, `88.23 s`, `30.5 MB`). Extracted 16 frames to `_final_frames/` and generated `contact_sheet_4x4.jpg`. Exported to `E:\AI_Videos\Instagram\exports\04_openshorts_gta6_final.mp4`.
   - **Content SEO & Publishing System:**
     - Video Analysis: `analysis/video-analysis/04-openshorts-gta6.md` & metadata JSON.
     - Keyword Research: `analysis/keyword-research/04-openshorts-gta6-keywords.md`.
     - Instagram Package: `publishing/instagram/04-openshorts-gta6-posting-package.md` (Rubric score: **97.2 / 100**).
     - YouTube Shorts Package: `publishing/youtube/04-openshorts-gta6-posting-package.md`.
     - TikTok Package: `publishing/tiktok/04-openshorts-gta6-posting-package.md`.
