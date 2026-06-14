"""Rendering seam -- this replaces the CapCut + PyAutoGUI layer.

Why no CapCut: driving a GUI by clicking pixels breaks on every UI update and
inherits screen-resolution and timing bugs you cannot reproduce. FFmpeg/MoviePy
render cuts, motion, captions, audio mix, and platform presets directly and
deterministically. Same output, none of the fragility.

`render_variants` runs in MOCK mode by default: it writes a JSON manifest
describing exactly what WOULD be rendered, so the pipeline completes with no
video dependencies. Set USE_REAL_RENDER=1 (and `pip install moviepy`) to render
actual MP4s.
"""

from __future__ import annotations

import json
import os

PLATFORM_SPECS = {
    "youtube": {"w": 1080, "h": 1920, "fps": 30},
    "instagram": {"w": 1080, "h": 1920, "fps": 30},
    "tiktok": {"w": 1080, "h": 1920, "fps": 30},
}


def render_variants(timeline: dict, base_name: str) -> dict[str, str]:
    safe = "".join(c if c.isalnum() else "_" for c in base_name).strip("_") or "short"
    if os.environ.get("USE_REAL_RENDER") == "1":
        return _render_real(timeline, safe)
    return _render_mock(timeline, safe)


def _render_mock(timeline: dict, safe: str) -> dict[str, str]:
    """Write a manifest per platform instead of pixels. Lets the graph finish offline."""
    os.makedirs("exports", exist_ok=True)
    out: dict[str, str] = {}
    for platform, spec in PLATFORM_SPECS.items():
        path = f"exports/{safe}_{platform}.manifest.json"
        with open(path, "w") as f:
            json.dump({"platform": platform, "spec": spec, "timeline": timeline}, f, indent=2)
        out[platform] = path
    return out


def _render_real(timeline: dict, safe: str) -> dict[str, str]:
    """Real render sketch. Fill the clip loop with your asset paths and effects."""
    from moviepy.editor import (  # type: ignore
        AudioFileClip,
        CompositeVideoClip,
        TextClip,
        VideoFileClip,
        concatenate_videoclips,
    )

    os.makedirs("exports", exist_ok=True)
    clips = []
    for c in timeline["clips"]:
        clip = VideoFileClip(c["asset"]).subclip(0, c["duration"])
        # apply motion (c["motion"]) and overlay captions here
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")

    out: dict[str, str] = {}
    for platform, spec in PLATFORM_SPECS.items():
        path = f"exports/{safe}_{platform}.mp4"
        video.resize((spec["w"], spec["h"])).write_videofile(
            path, fps=spec["fps"], codec="libx264", audio_codec="aac"
        )
        out[platform] = path
    return out
