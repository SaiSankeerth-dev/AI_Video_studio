"""CapCut draft generator.

Instead of driving the CapCut GUI with PyAutoGUI (fragile, breaks on every UI
update), this writes a CapCut *draft project* on disk. You open CapCut and the
project is already there: clips placed on the timeline in the agent's order,
trimmed to the agent's durations, with transitions between cuts.

Schema target: CapCut 8.3.0 / draft version 360000 (read from the user's own
empty drafts, so the skeleton matches their install exactly). The clip and
transition encoding is reconstructed -- if a future CapCut rejects it, the
reliable fix is to template from a known-good draft (see README seam).

Timebase: CapCut stores all times in MICROSECONDS.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
import uuid

US = 1_000_000  # microseconds per second

# CapCut Projects folder on this machine (where the app lists drafts).
DRAFT_ROOT = os.path.expandvars(
    r"%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft"
)

# Best-effort built-in transitions, cycled across cuts. resource_id is what ties
# a transition to an installed effect; these are left blank because this install
# has no cached transition resources. CapCut opens the draft and places the cut;
# if a name does not resolve, applying a transition is one click in the app.
TRANSITIONS = [
    {"name": "Pull in", "duration_us": 466666},
    {"name": "Dissolve", "duration_us": 500000},
    {"name": "Zoom", "duration_us": 466666},
    {"name": "Slide", "duration_us": 500000},
]


def _uid() -> str:
    return str(uuid.uuid4()).upper()


def _now_us() -> int:
    return int(time.time() * US)


def _ffprobe() -> str | None:
    exe = shutil.which("ffprobe")
    if exe:
        return exe
    # derive from the ffmpeg next to it if ffprobe is not on PATH
    ff = shutil.which("ffmpeg")
    if ff:
        cand = os.path.join(os.path.dirname(ff), "ffprobe.exe")
        if os.path.exists(cand):
            return cand
    return None


def _probe(path: str) -> tuple[int, int, int]:
    """Return (width, height, duration_us). Falls back to vertical defaults."""
    exe = _ffprobe()
    if exe:
        try:
            out = subprocess.run(
                [exe, "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height:format=duration",
                 "-of", "json", path],
                capture_output=True, text=True, timeout=30,
            ).stdout
            data = json.loads(out)
            stream = (data.get("streams") or [{}])[0]
            w = int(stream.get("width") or 1080)
            h = int(stream.get("height") or 1920)
            dur = float(data.get("format", {}).get("duration") or 0)
            return w, h, int(dur * US)
        except Exception:
            pass
    return 1080, 1920, 0


def _video_material(asset_path: str, is_image: bool, dur_us: int,
                    w: int, h: int) -> dict:
    """One entry in materials.videos (CapCut treats images as 'photo' videos)."""
    return {
        "id": _uid(),
        "type": "photo" if is_image else "video",
        "path": asset_path.replace("\\", "/"),
        "material_name": os.path.basename(asset_path),
        "duration": dur_us if dur_us > 0 else 5 * US,
        "width": w,
        "height": h,
        "has_audio": not is_image,
        "category_id": "",
        "category_name": "local",
        "check_flag": 62978047,
        "crop": {"lower_left_x": 0.0, "lower_left_y": 1.0, "lower_right_x": 1.0,
                 "lower_right_y": 1.0, "upper_left_x": 0.0, "upper_left_y": 0.0,
                 "upper_right_x": 1.0, "upper_right_y": 0.0},
        "crop_ratio": "free",
        "crop_scale": 1.0,
        "is_ai_generate_content": False,
        "is_unified_beauty_mode": False,
        "local_material_id": _uid(),
        "media_path": "",
        "reverse_intensified_path": "",
        "reverse_path": "",
        "source": 0,
        "source_platform": 0,
        "stable": {"matrix_path": "", "stable_level": 0, "time_range": {"duration": 0, "start": -1}},
        "team_id": "",
        "video_algorithm": {"algorithms": [], "deflicker": None, "motion_blur_config": None,
                            "noise_reduction": None, "path": "", "time_range": None},
    }


def _speed() -> dict:
    return {"id": _uid(), "type": "speed", "mode": 0, "speed": 1.0, "curve_speed": None}


def _canvas() -> dict:
    return {"id": _uid(), "type": "canvas_color", "album_image": "", "blur": 0.0,
            "color": "", "image": "", "image_id": "", "image_name": "",
            "source_platform": 0}


def _sound_mapping() -> dict:
    return {"id": _uid(), "type": "sound_channel_mapping", "audio_channel_mapping": 0,
            "is_config_open": False}


def _vocal_separation() -> dict:
    return {"id": _uid(), "type": "vocal_separation", "choice": 0, "production_path": "",
            "removed_sounds": [], "time_range": None}


def _transition(spec: dict) -> dict:
    return {
        "id": _uid(),
        "type": "transition",
        "name": spec["name"],
        "duration": spec["duration_us"],
        "is_overlap": False,
        "category_id": "",
        "category_name": "",
        "effect_id": "",
        "resource_id": "",
        "path": "",
        "platform": "all",
        "request_id": "",
        "source_platform": 0,
    }


def _segment(material_id: str, start_us: int, dur_us: int,
             refs: list[str]) -> dict:
    return {
        "id": _uid(),
        "material_id": material_id,
        "target_timerange": {"start": start_us, "duration": dur_us},
        "source_timerange": {"start": 0, "duration": dur_us},
        "extra_material_refs": refs,
        "speed": 1.0,
        "volume": 1.0,
        "visible": True,
        "enable_adjust": True,
        "enable_color_curves": True,
        "enable_color_wheels": True,
        "enable_lut": True,
        "enable_video_mask": True,
        "render_index": 0,
        "reverse": False,
        "is_placeholder": False,
        "is_tone_modify": False,
        "is_loop": False,
        "cartoon": False,
        "intensifies_audio": False,
        "last_nonzero_volume": 1.0,
        "track_attribute": 0,
        "track_render_index": 0,
        "clip": {"alpha": 1.0, "flip": {"horizontal": False, "vertical": False},
                 "rotation": 0.0, "scale": {"x": 1.0, "y": 1.0},
                 "transform": {"x": 0.0, "y": 0.0}},
        "hdr_settings": {"intensity": 1.0, "mode": 1, "nits": 1000},
        "uniform_scale": {"on": True, "value": 1.0},
        "common_keyframes": [],
        "keyframe_refs": [],
        "caption_info": None,
        "responsive_layout": {"enable": False, "horizontal_pos_layout": 0,
                              "size_layout": 0, "target_follow": "", "vertical_pos_layout": 0},
    }


def build_capcut_draft(timeline: dict, asset_for_clip, base_name: str,
                       with_transitions: bool = True) -> str:
    """Write a CapCut draft folder and return its path.

    asset_for_clip(i, clip_dict) -> absolute asset path (or None to skip).
    """
    safe = "".join(c if c.isalnum() else "_" for c in base_name).strip("_") or "short"
    draft_name = f"AI_{safe}"[:60]
    draft_dir = os.path.join(DRAFT_ROOT, draft_name)
    os.makedirs(draft_dir, exist_ok=True)

    canvas_w, canvas_h = 1080, 1920  # vertical short

    materials_videos: list[dict] = []
    speeds: list[dict] = []
    canvases: list[dict] = []
    sound_mappings: list[dict] = []
    vocal_seps: list[dict] = []
    transitions: list[dict] = []
    segments: list[dict] = []

    path_to_material: dict[str, str] = {}
    cursor_us = 0
    clips = timeline.get("clips", [])

    for i, clip in enumerate(clips):
        asset = asset_for_clip(i, clip)
        if not asset:
            continue
        is_image = os.path.splitext(asset)[1].lower() in (
            ".jpg", ".jpeg", ".png", ".webp", ".bmp")

        if asset not in path_to_material:
            w, h, probed_us = _probe(asset)
            mat = _video_material(asset, is_image, probed_us, w, h)
            materials_videos.append(mat)
            path_to_material[asset] = mat["id"]
        material_id = path_to_material[asset]

        dur_us = int(round(float(clip.get("duration", 2.0)) * US))

        sp, cv, sm, vs = _speed(), _canvas(), _sound_mapping(), _vocal_separation()
        speeds.append(sp); canvases.append(cv)
        sound_mappings.append(sm); vocal_seps.append(vs)
        refs = [sp["id"], cv["id"], sm["id"], vs["id"]]

        # transition lives on the segment that PRECEDES the cut
        if with_transitions and i < len(clips) - 1:
            tr = _transition(TRANSITIONS[i % len(TRANSITIONS)])
            transitions.append(tr)
            refs.append(tr["id"])

        segments.append(_segment(material_id, cursor_us, dur_us, refs))
        cursor_us += dur_us

    total_us = cursor_us

    # --- assemble draft_content.json from the 8.3.0 skeleton -----------------
    platform = {"app_id": 359289, "app_source": "cc", "app_version": "8.3.0",
                "device_id": "", "hard_disk_id": "", "mac_address": "",
                "os": "windows", "os_version": "10.0.26200"}

    content = {
        "canvas_config": {"background": None, "height": canvas_h,
                          "ratio": "original", "width": canvas_w},
        "color_space": -1,
        "cover": None,
        "create_time": 0,
        "draft_type": "video",
        "duration": total_us,
        "extra_info": None,
        "fps": 30.0,
        "free_render_index_mode_on": False,
        "group_container": None,
        "id": _uid(),
        "is_drop_frame_timecode": False,
        "keyframe_graph_list": [],
        "keyframes": {"adjusts": [], "audios": [], "effects": [], "filters": [],
                      "handwrites": [], "stickers": [], "texts": [], "videos": []},
        "last_modified_platform": platform,
        "lyrics_effects": [],
        "materials": {
            "ai_translates": [], "audio_balances": [], "audio_effects": [],
            "audio_fades": [], "audio_pannings": [], "audio_pitch_shifts": [],
            "audio_track_indexes": [], "audios": [], "beats": [], "canvases": canvases,
            "chromas": [], "color_curves": [], "common_mask": [], "digital_humans": [],
            "drafts": [], "effects": [], "flowers": [], "green_screens": [],
            "handwrites": [], "hsl": [], "images": [], "log_color_wheels": [],
            "loudnesses": [], "manual_beautys": [], "manual_deformations": [],
            "material_animations": [], "material_colors": [], "multi_language_refs": [],
            "placeholder_infos": [], "placeholders": [], "plugin_effects": [],
            "primary_color_wheels": [], "realtime_denoises": [], "shapes": [],
            "smart_crops": [], "smart_relights": [], "sound_channel_mappings": sound_mappings,
            "speeds": speeds, "stickers": [], "tail_leaders": [], "text_templates": [],
            "texts": [], "time_marks": [], "transitions": transitions,
            "video_effects": [], "video_radius": [], "video_shadows": [],
            "video_strokes": [], "video_trackings": [], "videos": materials_videos,
            "vocal_beautifys": [], "vocal_separations": vocal_seps,
        },
        "mutable_config": None,
        "name": "",
        "new_version": "163.0.0",
        "path": "",
        "platform": platform,
        "relationships": [],
        "render_index_track_mode_on": True,
        "retouch_cover": None,
        "source": "default",
        "static_cover_image_path": "",
        "time_marks": None,
        "tracks": [{
            "id": _uid(),
            "type": "video",
            "attribute": 0,
            "flag": 0,
            "is_default_name": True,
            "name": "",
            "segments": segments,
        }],
        "update_time": 0,
        "version": 360000,
    }

    with open(os.path.join(draft_dir, "draft_content.json"), "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False)

    # --- draft_meta_info.json ------------------------------------------------
    now = _now_us()
    meta = {
        "draft_cover": "draft_cover.jpg",
        "draft_fold_path": draft_dir.replace("\\", "/"),
        "draft_id": _uid(),
        "draft_is_ai_shorts": True,
        "draft_materials": [{"type": t, "value": []} for t in (0, 1, 2, 3, 6, 7, 8)],
        "draft_name": draft_name,
        "draft_root_path": DRAFT_ROOT,
        "draft_timeline_materials_size_": 0,
        "tm_draft_create": now,
        "tm_draft_modified": now,
        "tm_duration": total_us,
    }
    with open(os.path.join(draft_dir, "draft_meta_info.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)

    return draft_dir
