# FIFA 2026 Hype — CapCut Assembly Guide (step by step)

Everything below assembles the timeline defined in `Shot_List_EDL.md`. Works in CapCut
desktop or mobile. Target: 45s, 9:16, 30fps.

## 0. Setup
1. Open CapCut → **New project**.
2. Top-right → aspect ratio → **9:16** (vertical). (Use 16:9 for the YouTube variant.)
3. Settings → frame rate **30fps**, resolution **1080p**.

## 1. Import assets
1. Download clips into `03_Assets/Video_Clips/` using the slots in `ASSET_SOURCES.md`.
2. In CapCut → **Import** → select the whole `Video_Clips` folder.
3. Import your music into `Audio_Music` and SFX too.

## 2. Lay the rough cut (follow the EDL table)
1. Drag clips onto the timeline in order **01 → 14**.
2. Trim each to the duration in the Shot List (tap clip → drag edge, watch the duration readout).
3. For the 0:33–0:39 fast montage (shot 13): drop 12 clips, set each to **0.5s** (select all → uniform duration).

## 3. Speed & freeze
- Shot 4: select → **Speed → Curve → "Bullet"** for the ramp.
- Shot 10: **Speed → Normal → 0.5x** (slow-mo).
- Shot 14: play to last frame → **Freeze** → extend the frozen frame to fill 0:43.5–0:45.

## 4. Transitions
Tap the seam between two clips → **Transitions**, then apply per the cheat-sheet in the Shot List
(whip = "Swirl"/"Whip", zoom = "Zoom in", dissolve = "Dissolve", flash = "Flash white"). Keep most
at hard cut; transitions only where the EDL marks them.

## 5. Music + audio
1. Add your chosen track on the audio track from 0:00.
2. Trim so the **drop lands at 0:39** (line up with shot 14's freeze). Move the track left/right until the waveform's loudest hit sits at 0:39.
3. Add SFX (whoosh, boom, net, crowd) at the times in the Audio Plan.
4. Select music → **Auto-duck ON** so it dips under the VO.

## 6. Voiceover
- Your own VO: drop the file in, align lines to the timecodes in `Script_and_VO.md`.
- Synthetic: add each line as a **Text** layer → select → **Text-to-audio** → pick a deep voice (Cosmo) → it generates the VO clip; align to timecodes.

## 7. On-screen text
Add the **On-screen text** column from the script as Text layers:
- Font: bold condensed (CapCut "Aa" → e.g. *Anton* / *Oswald* style).
- Animation: **In = "Punch"/"Scale up"**, Out = "Fade". ~0.3s each.
- Big stat text ("48 TEAMS · 104 MATCHES") center-screen; location tags lower-third.
- Final "WORLD CUP 2026" at 0:39 with **Scale up + glow**.

## 8. Color & polish
- Add a global **Filter** → "Cinematic"/"Teal-Orange" at ~40% across all clips for cohesion.
- Adjust → slight **Contrast +10, Saturation +8** for punch.
- Optional: subtle **vignette**.

## 9. Captions (accessibility + reach)
- Auto-captions → **Captions → Auto** (reads the VO). Position above the on-screen text. Restyle bold.

## 10. Export
- **Export → 1080p, 30fps, high bitrate.**
- For Reels/TikTok/Shorts: 9:16, under 60s ✓.
- Re-export a **16:9** version for YouTube (change project ratio, re-center text).

---
### QA before you post (sign-off)
- [ ] Every clip is from a legal/free source (check `ASSET_SOURCES.md` ledger).
- [ ] Music drop lands on the 0:39 freeze.
- [ ] VO is audible over music (auto-duck working).
- [ ] All dates/stats on screen are correct (Jun 11–Jul 19, 48 teams, 104 matches, 16 cities).
- [ ] No clipping; master around −14 LUFS.
- [ ] Captions accurate and readable.
