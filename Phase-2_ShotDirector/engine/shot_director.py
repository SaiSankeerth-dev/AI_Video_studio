import json
from pathlib import Path
from .prompt_compiler import PromptCompilerV1

class CinematicShotDirectorV1:
    def __init__(self):
        self.compiler = PromptCompilerV1()

    def build_shot(self, sid, narration, shot_type, purpose, subject, action, env, time_str, ctx, comp, fg, mg, bg, light, mats, atmos, palette, cam_size, cam_pos, cam_ht, angle, lens, dof, move, chars=[], locs=[], objs=[], refs=[]):
        shot = {
            "shot_id": sid,
            "purpose": purpose,
            "shot_type": shot_type,
            "narration": narration,
            "visual": {
                "subject": subject,
                "action": action,
                "environment": env,
                "time": time_str,
                "context": ctx,
                "composition": comp,
                "foreground": fg,
                "midground": mg,
                "background": bg,
                "lighting": light,
                "materials": mats,
                "atmosphere": atmos,
                "color_palette": palette
            },
            "camera": {
                "shot_size": cam_size,
                "camera_position": cam_pos,
                "camera_height": cam_ht,
                "angle": angle,
                "lens": lens,
                "depth_of_field": dof,
                "movement": move
            },
            "continuity": {
                "characters": chars,
                "locations": locs,
                "objects": objs,
                "reference_images": refs
            },
            "quality_targets": {
                "story_alignment": 9.5,
                "composition": 9.2,
                "photorealism": 9.4,
                "cinematography": 9.3,
                "character_consistency": 9.1,
                "environment_consistency": 9.3,
                "technical_accuracy": 9.5,
                "lighting": 9.2,
                "visual_clarity": 9.4,
                "video_motion_potential": 9.2
            }
        }
        return self.compiler.compile(shot)
