"""Build a FIFA World Cup 2026 hype CapCut draft using the repo's own machinery.

Uses assets.AutoAssetSource (the multi-agent asset layer) to generate legally-safe
B-roll cards, and capcut.build_capcut_draft to write an editable CapCut project.
Then rewrites asset/draft paths from the Linux sandbox form to the Windows form so
CapCut on Windows can resolve everything once the folder is moved into its Projects dir.
"""
from __future__ import annotations
import json, os
import assets, capcut

# --- path mapping: Linux sandbox  <->  Windows host -------------------------
LINUX_AI_VE = "/sessions/keen-dazzling-hypatia/mnt/AI_VE"
WIN_AI_VE   = "C:/Users/V. Sai Sankeerth/AI_VE"
WIN_CAPCUT_PROJECTS = ("C:/Users/V. Sai Sankeerth/AppData/Local/CapCut/"
                       "User Data/Projects/com.lveditor.draft")

BUILD = os.path.join(LINUX_AI_VE, "capcut_build")
ASSET_CACHE = os.path.join(BUILD, "auto_assets")
DRAFT_OUT   = os.path.join(BUILD, "drafts")
os.makedirs(ASSET_CACHE, exist_ok=True)
os.makedirs(DRAFT_OUT, exist_ok=True)

# --- the real FIFA 2026 hype shot list (description, seconds) ---------------
SHOTS = [
    ("Stadium aerial at dusk, floodlights on, packed crowd", 3.0),
    ("Crowd erupting, fans waving flags",                     2.0),
    ("National flags of many countries waving",               2.0),
    ("Football strike on goal, slow motion",                  3.0),
    ("Ball hitting the net, goal celebration",                2.0),
    ("Mexico City skyline and Estadio Azteca",                3.0),
    ("Mexican fans celebrating in the street",                2.0),
    ("North American host city skylines montage",             4.0),
    ("Diverse fans cheering with face paint",                 3.0),
    ("Players tunnel, boots walking out",                     3.0),
    ("USA, Canada and Mexico flags together",                 3.0),
    ("Sweeping aerial over a host city at sunset",            3.0),
    ("Fast hype montage: goals, saves, celebrations",         6.0),
    ("Epic wide stadium shot with fireworks",                 6.0),
]

def main() -> None:
    src = assets.AutoAssetSource(topic="FIFA World Cup 2026", cache_dir=ASSET_CACHE)
    clips = []
    for i, (desc, dur) in enumerate(SHOTS):
        a = src.match(desc, i)          # generates a labelled B-roll card (ffmpeg)
        asset_path = a.path if a else ""
        clips.append({"asset": asset_path, "duration": dur, "description": desc,
                      "motion": ["zoom-in", "pan-left", "zoom-out", "pan-right"][i % 4]})
        print(f"  shot {i:02d}: {dur:>4}s  {desc[:38]:38}  -> {os.path.basename(asset_path)}")

    timeline = {"fps": 30, "resolution": [1080, 1920],
                "total_seconds": sum(d for _, d in SHOTS), "clips": clips,
                "music": [], "captions": []}

    # write the draft into our build dir (not %LOCALAPPDATA%, which is Windows-only)
    capcut.DRAFT_ROOT = DRAFT_OUT
    draft_dir = capcut.build_capcut_draft(
        timeline, asset_for_clip=lambda i, c: c["asset"],
        base_name="FIFA World Cup 2026", with_transitions=True)
    print("draft built at:", draft_dir)

    # --- rewrite paths Linux -> Windows so CapCut resolves them -------------
    draft_name = os.path.basename(draft_dir)
    win_fold = f"{WIN_CAPCUT_PROJECTS}/{draft_name}"

    content_p = os.path.join(draft_dir, "draft_content.json")
    meta_p    = os.path.join(draft_dir, "draft_meta_info.json")

    def fix(s: str) -> str:
        return s.replace(LINUX_AI_VE, WIN_AI_VE)

    with open(content_p, encoding="utf-8") as f:
        content = json.load(f)
    for v in content["materials"]["videos"]:
        v["path"] = fix(v["path"])
    with open(content_p, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False)

    with open(meta_p, encoding="utf-8") as f:
        meta = json.load(f)
    meta["draft_fold_path"] = win_fold
    meta["draft_root_path"] = WIN_CAPCUT_PROJECTS
    with open(meta_p, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)

    print("\nDONE.")
    print("Draft folder (Linux):", draft_dir)
    print("Move this folder into:", WIN_CAPCUT_PROJECTS)
    print("Asset cache (Windows):", ASSET_CACHE.replace(LINUX_AI_VE, WIN_AI_VE))

if __name__ == "__main__":
    main()
