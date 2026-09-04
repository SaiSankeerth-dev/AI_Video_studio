"""
Prompt Builder (Phase 1 Visual Director)
Generates rich, photorealistic, structurally grounded prompts combining:
1. Documentary Visual Bible rules
2. Entity identity specifics (characters, facilities, hardware)
3. Structured prompt blocks:
   SUBJECT, ARCHITECTURE, CAMERA, COMPOSITION, LIGHTING, MATERIAL, ATMOSPHERE, REALISM, DO NOT
Avoids vague one-line prompts (e.g. 'a cinematic server room').
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class PromptBuilder:
    def __init__(self, visual_bible: Optional[Dict[str, Any]] = None):
        if visual_bible:
            self.visual_bible = visual_bible
        else:
            bible_file = Path(__file__).parents[1] / "visual-bible" / "visual_bible.json"
            if bible_file.exists():
                with open(bible_file, "r", encoding="utf-8") as f:
                    self.visual_bible = json.load(f)
            else:
                self.visual_bible = {}

    def build_structured_image_prompt(
        self,
        subject: str,
        architecture: str,
        camera: Dict[str, Any],
        composition: str,
        lighting: str,
        materials: str,
        atmosphere: str,
        continuity_context: Optional[str] = None,
        entity_context: Optional[str] = None
    ) -> str:
        """Constructs a production-grade prompt combining Section 10 Visual Bible and Section 8 Structured Blocks."""
        cam_desc = (
            f"{camera.get('shot_size', 'Medium shot')}, {camera.get('position', 'eye-level')}, "
            f"{camera.get('lens', '35mm cinema lens')}, camera height {camera.get('height', '1.6m')}, "
            f"{camera.get('movement', 'static observation')}"
        )

        blocks = []

        # SECTION 10: Injected Master Documentary Visual Bible
        if self.visual_bible:
            cam_bible = self.visual_bible.get("camera_language", {})
            lit_bible = self.visual_bible.get("lighting", {})
            col_bible = self.visual_bible.get("color_behavior", {})
            arch_bible = self.visual_bible.get("architecture", {})
            real_bible = self.visual_bible.get("image_realism", {})
            hist_bible = self.visual_bible.get("historical_accuracy", {})

            bible_summary = (
                f"DOCUMENTARY VISUAL BIBLE:\n"
                f"- Sensor & Aspect: {cam_bible.get('primary_sensor', 'ARRI Alexa Mini LF')}, {cam_bible.get('aspect_ratio', '16:9')}\n"
                f"- Lighting Standard: {lit_bible.get('primary_key', 'Cold 4500K-5000K industrial')} with {lit_bible.get('accent_practical', 'cyan telemetry LEDs')}\n"
                f"- Color Grading: {col_bible.get('palette_name', 'Forensic Industrial Noir')} ({col_bible.get('color_grading_lut', 'cool shadows with warm accents')})\n"
                f"- Architectural Canon: {arch_bible.get('style', 'Subterranean Brutalist Infrastructure')}\n"
                f"- Realism Standard: {real_bible.get('fidelity_standard', 'Photorealistic cinematic production still')}, {real_bible.get('surface_wear', 'authentic micro-scratches and surface wear')}\n"
                f"- Era Fidelity: {hist_bible.get('era', '2024-2026 Agentic Transition')}, {hist_bible.get('no_fantasy_elements', 'no sci-fi holograms')}"
            )
            blocks.append(bible_summary)

        # SECTION 11: Recurring Entity Identity Invariants
        if entity_context:
            blocks.append(f"ENTITY IDENTITY:\n{entity_context}")
        elif continuity_context:
            blocks.append(f"CONTINUITY CONTEXT:\n{continuity_context}")

        # SECTION 8: Explicit Structured Prompt Blocks
        blocks.extend([
            f"SUBJECT:\n{subject}",
            f"ARCHITECTURE:\n{architecture}",
            f"CAMERA:\n{cam_desc}",
            f"COMPOSITION:\n{composition}",
            f"LIGHTING:\n{lighting}",
            f"MATERIAL:\n{materials}",
            f"ATMOSPHERE:\n{atmosphere}",
            f"REALISM:\nPhotorealistic documentary production still, 35mm optical capture, physically plausible architecture, realistic human anatomy and surface textures, accurate depth of field.",
            (
                "DO NOT:\n"
                "text artifacts, logos, watermarks, fantasy architecture, floating objects, "
                "duplicated equipment, warped geometry, extra limbs or fingers, plastic skin, "
                "excessive neon, oversaturated lighting, cartoon, anime, 3d render look."
            )
        ])

        return "\n\n".join(blocks)

    def build_blender_spec(
        self,
        environment: str,
        objects: List[str],
        materials: List[str],
        camera_pos: List[float],
        camera_target: List[float],
        lens_mm: float = 24.0,
        dof_target: str = "CentralServerRack",
        lighting_setup: str = "OverheadIndustrialCyan",
        fog_density: float = 0.02,
        camera_path: str = "linear_dolly_push",
        render_duration_frames: int = 150
    ) -> Dict[str, Any]:
        """Constructs Section 14 Blender 3D specification."""
        return {
            "environment": environment,
            "objects": objects,
            "materials": materials,
            "camera_position": camera_pos,
            "camera_target": camera_target,
            "lens": f"{lens_mm}mm",
            "depth_of_field": {"enabled": True, "focus_target": dof_target, "f_stop": 2.8},
            "lighting": lighting_setup,
            "fog": {"density": fog_density, "color": [0.05, 0.08, 0.12]},
            "animation": {"type": "camera_dolly", "axis": "Y", "speed": 0.08},
            "camera_path": camera_path,
            "render_duration": render_duration_frames
        }

if __name__ == "__main__":
    builder = PromptBuilder()
    prompt = builder.build_structured_image_prompt(
        subject="Underground hyperscale computing facility",
        architecture="Massive industrial server hall extending deep into the background, repeated server racks, exposed cable trays, reinforced structural columns",
        camera={"shot_size": "Wide establishing shot", "position": "Low eye-level cinematic perspective", "lens": "24mm wide-angle lens", "height": "1.6m above floor", "movement": "Slow forward tracking"},
        composition="Strong central perspective, foreground server racks framing the image, large negative space toward the vanishing point",
        lighting="Cold overhead industrial lighting, subtle practical cyan LEDs, soft volumetric haze",
        materials="Brushed metal, dark polymer, concrete, fiber-optic cables",
        atmosphere="Slight condensation haze, deep environmental depth, realistic dust particles"
    )
    print("Sample Structured Prompt:\n" + prompt)
