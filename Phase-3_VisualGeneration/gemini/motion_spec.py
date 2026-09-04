import json

class MotionSpecCompiler:
    def compile_motion_spec(self, shot_spec):
        archetype = shot_spec.get("archetype", "ESTABLISHING")
        cam = shot_spec.get("camera", {})

        if archetype == "ESTABLISHING":
            motion_desc = (
                "Continuous slow 35mm forward dolly push-in (speed factor: 0.0006 per frame). "
                "Server status LEDs pulse asynchronously. Subtle atmospheric floor fog moves slowly from right to left. "
                "Keep camera horizontal axis perfectly level. Zero camera shake. Zero object warping."
            )
        elif archetype == "CHARACTER" or archetype == "REENACTMENT":
            motion_desc = (
                "Slow 50mm push-in toward the subject (speed factor: 0.0008 per frame). "
                "Subject remains seated with subtle micro-movements of hands typing and head tracking the monitor. "
                "Screen diagnostic text softly scrolls in the reflection. Zero morphing of face or wardrobe."
            )
        elif archetype == "MACRO":
            motion_desc = (
                "Slow lateral camera slide along the silicon chip plane (speed factor: 0.0007 per frame). "
                "Gold micro-circuit traces shimmer under moving light angle. Extreme shallow depth of field maintained throughout."
            )
        elif archetype == "SCALE":
            motion_desc = (
                "Slow orbit pan across the global data network map. "
                "Light pulses propagate along subsea fiber paths between major continents. "
                "Topographical map features remain crisp and static."
            )
        else:
            motion_desc = "Subtle 2.5D parallax drift with slight scale increase from 1.0 to 1.05."

        return {
            "shot_id": shot_spec.get("shot_id"),
            "motion_type": cam.get("movement", "slow dolly"),
            "motion_prompt": motion_desc,
            "target_fps": 30,
            "duration_seconds": 6.0
        }
