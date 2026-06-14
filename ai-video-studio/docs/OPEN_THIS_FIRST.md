# FIFA 2026 — CapCut draft: status & how to finish it

## What's done
- Ran your **AI Shorts Studio** pipeline (the multi-agent system in `AI_VE`) seeded with a real
  FIFA 2026 hype shot list.
- It generated **14 B-roll clips** + a **CapCut draft project** and the draft was **installed into
  CapCut** and recognised (CapCut re-indexed `root_meta_info.json` on launch).
- Open CapCut → it appears as **AI_FIFA_World_Cup_2026**: vertical 1080×1920, 30 fps, **45 s,
  14 clips, 13 transitions**, in the exact senior-editor order from `Shot_List_EDL.md`.

## The honest limitation (why it isn't "senior-editor pretty" yet)
1. **Visuals are placeholder cards.** With no Pexels key and no clips from you, every shot is a
   generated colour card labelled with its shot description. That was the option you chose.
   The *edit structure* is senior-level; the *footage* is not. Real footage is the only thing
   that makes it look pro — swap each card for a real clip and it's a finished reel.
2. **I could not visually verify inside CapCut.** The desktop security layer masks CapCut's
   window in screenshots, so I confirmed the install by other means (CapCut re-indexed the draft)
   but couldn't watch the timeline render.
3. **I did not hand-author titles/music/color into the draft JSON.** Doing that blind — without a
   way to see it render — risked corrupting a draft that currently opens cleanly. Those four
   finishing touches are 10 minutes in-app and listed below.

## Get to a pro finish (in CapCut, ~15 min)
1. **Footage** — replace each placeholder: click a clip → right-click → *Replace*, drop in a real
   clip. Sources + per-shot search terms are in `02_FIFA_2026_Edit/ASSET_SOURCES.md`.
   (Or give me a free **Pexels API key** and I'll have the pipeline pull real vertical b-roll
   automatically and rebuild the draft.)
2. **Motion** — select all clips → *Animation → Ken Burns / Zoom in*. Alternate zoom-in/out.
3. **Titles** — add the on-screen text from `02_FIFA_2026_Edit/Script_and_VO.md` (e.g.
   "THREE NATIONS", "48 TEAMS · 104 MATCHES", "JUN 11 – JUL 19, 2026"). Bold condensed font,
   *Scale-up* in-animation.
4. **Music** — CapCut → *Audio → Music* → an epic/sport track; line the drop up at **0:39** on the
   final freeze (see `Music_and_Audio_Plan.md`).
5. **Color** — *Filters → Cinematic / Teal-Orange* ~40% across all clips; Adjust: Contrast +10,
   Saturation +8.
6. **Export** — 1080p, 30 fps, high bitrate.

## To rebuild with the script (after you add a Pexels key or your own clips)
```
# real stock b-roll:
set PEXELS_API_KEY=...    &&    python build_fifa_capcut.py
# or hybrid with your clips: drop them in 03_Assets, then rerun
```
Then copy the regenerated `AI_FIFA_World_Cup_2026` folder into:
`C:\Users\V. Sai Sankeerth\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft`

*(Minor cleanup: a stray `AI_FIFA_World_Cup_2026 - Copy` folder is in `capcut_build\drafts` — safe
to delete.)*
