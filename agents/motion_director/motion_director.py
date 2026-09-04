"""
Motion Director Agent (TASK 15)
Directs editorial motion design: subtle camera drifts (100% to 105%), Ken Burns moves,
document highlights, kinetic typography pacing, and data chart interpolations.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class MotionDirector:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(r"D:\gitM\01_ContentFactory\production\graphics")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_motion_spec(self, shot: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates exact frame-by-frame transformation parameters for Remotion or FFmpeg filters.
        Enforces documentary camera movement: never static.
        """
        sid = shot["shot_id"]
        mov = shot.get("camera", {}).get("movement", "slow_push")
        duration = shot.get("duration", 4.0)
        fps = 30
        total_frames = int(round(duration * fps))

        if mov == "slow_push":
            # Scale 1.0 -> 1.06, subtle centered push
            transform = {
                "type": "ZOOM_IN",
                "scale_start": 1.0,
                "scale_end": 1.06,
                "pan_x_start": 0.0,
                "pan_x_end": 0.0,
                "easing": "cubic-bezier(0.25, 1, 0.5, 1)"
            }
        elif mov == "slow_pull":
            transform = {
                "type": "ZOOM_OUT",
                "scale_start": 1.06,
                "scale_end": 1.0,
                "pan_x_start": 0.0,
                "pan_x_end": 0.0,
                "easing": "cubic-bezier(0.25, 1, 0.5, 1)"
            }
        elif mov == "horizontal_drift":
            transform = {
                "type": "PAN_RIGHT",
                "scale_start": 1.03,
                "scale_end": 1.03,
                "pan_x_start": -20.0,
                "pan_x_end": 20.0,
                "easing": "linear"
            }
        elif mov == "macro_focus":
            transform = {
                "type": "MACRO_DRIFT",
                "scale_start": 1.02,
                "scale_end": 1.08,
                "pan_x_start": -10.0,
                "pan_x_end": 10.0,
                "easing": "ease-out"
            }
        else: # locked_off or default
            transform = {
                "type": "MICRO_DRIFT",
                "scale_start": 1.0,
                "scale_end": 1.015,
                "pan_x_start": 0.0,
                "pan_x_end": 0.0,
                "easing": "linear"
            }

        return {
            "shot_id": sid,
            "duration_seconds": duration,
            "total_frames": total_frames,
            "transform": transform,
            "grain_intensity": 0.04,
            "vignette": 0.25
        }

    def generate_graphics_manifest(self, shots: List[Dict[str, Any]]) -> Dict[str, Any]:
        manifest = {}
        for s in shots:
            sid = s["shot_id"]
            manifest[sid] = self.create_motion_spec(s)
        
        with open(self.output_dir / "motion-specs.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest

if __name__ == "__main__":
    from agents.shot_director.shot_director import ShotDirector
    sd = ShotDirector()
    plan = sd.generate_90s_benchmark_shot_plan()
    md = MotionDirector()
    specs = md.generate_graphics_manifest(plan["shots"])
    print(f"Motion Director generated {len(specs)} camera drift specifications.")
