"""
Master Visual Director (Phase 1)
Orchestrates the visual creation of each documentary shot.
Implements Section 6 specifications:
Input:
- narration
- scene
- claim
- visual bible
- previous shots
- available assets

Output:
- visual_type
- shot_duration
- camera
- composition
- subject
- action
- environment
- generation_method
- prompt
- continuity
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from .visual_selector import VisualSelector
    from .prompt_builder import PromptBuilder
    from .continuity import VisualContinuityManager
    from .shot_planner import ShotPlanner
except ImportError:
    from visual_selector import VisualSelector
    from prompt_builder import PromptBuilder
    from continuity import VisualContinuityManager
    from shot_planner import ShotPlanner

class VisualDirector:
    def __init__(
        self,
        visual_bible: Optional[Dict[str, Any]] = None,
        visual_rules: Optional[Dict[str, Any]] = None,
        entities: Optional[List[Dict[str, Any]]] = None
    ):
        base_dir = Path(__file__).parent
        if visual_rules is None:
            rules_path = base_dir / "visual_rules.json"
            if rules_path.exists():
                with open(rules_path, "r", encoding="utf-8") as f:
                    visual_rules = json.load(f)
            else:
                visual_rules = {}

        self.visual_bible = visual_bible or {}
        self.visual_rules = visual_rules or {}
        self.entities = entities or []

        self.selector = VisualSelector(self.visual_rules)
        self.prompt_builder = PromptBuilder(self.visual_bible)
        self.continuity_mgr = VisualContinuityManager(self.visual_bible, self.entities)
        self.planner = ShotPlanner(self.visual_rules)

    def direct_shot(
        self,
        shot_id: str,
        scene: Dict[str, Any],
        narration: Dict[str, Any],
        claim: Optional[Dict[str, Any]],
        previous_shots: List[Dict[str, Any]],
        available_assets: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Synthesizes all inputs into an exhaustive, camera-ready shot specification."""
        scene_id = scene.get("scene_id", "SCN-001")
        seg_id = narration.get("segment_id", "N001")
        narration_text = narration.get("text", "")
        visual_req = narration.get("visual_requirement", "")
        claim_ids = narration.get("claim_ids", [])
        if claim and claim.get("claim_id") and claim["claim_id"] not in claim_ids:
            claim_ids.append(claim["claim_id"])

        # History of visual types
        prev_types = [s.get("visual_type") for s in previous_shots if s.get("visual_type")]

        # 1. Select optimal visual medium (avoiding streaks > 2)
        visual_type = self.selector.select_medium(
            narration_text=narration_text,
            visual_requirement=visual_req,
            claim_evidence=claim.get("visual_evidence") if isinstance(claim, dict) and "visual_evidence" in claim else None,
            previous_visual_types=prev_types
        )

        # 2. Timing & Pacing calculation
        shot_start = previous_shots[-1]["end"] if previous_shots else scene.get("start", narration.get("start", 0.0))
        # Default duration allocation
        dur = 4.5
        if visual_type in ["DOCUMENT", "CODE_VISUALIZATION"]:
            dur = 5.5
        elif visual_type in ["BLENDER_3D"]:
            dur = 6.0
        elif visual_type in ["AI_VIDEO"]:
            dur = 4.0
        elif visual_type in ["AI_IMAGE"]:
            dur = 3.5

        # 3. Subject and Action determination
        subject = narration.get("subject", visual_req or "Autonomous computing infrastructure")
        action = narration.get("action", "Operating under nocturnal telemetry")
        environment = narration.get("environment", "Atlas Subterranean Hyperscale Facility")

        # 4. Camera & Composition specifications dynamically derived from context
        text_full = (narration_text + " " + visual_req + " " + subject + " " + environment).lower()
        if any(w in text_full for w in ["workstation", "engineer", "desk", "terminal", "screen", "keyboard", "human"]):
            arch_desc = "Minimalist concrete engineering observation pod with acoustic wall treatment and triple 4K workstation displays"
            comp_desc = "Low desktop three-quarter perspective framing keyboard and glowing terminal cursor with reflections"
            lit_desc = "High contrast chiaroscuro; phosphor monitor glow (6500K) with warm tungsten task lamp (3200K) edge accent"
            mat_desc = "Matte anodized dark aluminum, titanium wire-rim glasses, PBT keycaps, tempered reflection glass"
            atm_desc = "Solitary quiet late-night tension, interior HVAC controlled atmosphere"
            cam_lens = "50mm Zeiss Cinema Prime"
            cam_pos = "Low desktop three-quarter angle"
        elif any(w in text_full for w in ["switch", "air-gap", "containment", "kill", "isolation", "cut"]):
            arch_desc = "Heavy industrial air-gap containment room, reinforced vault bulkhead, high-voltage conduit raceways"
            comp_desc = "Tight macro framing on mechanical disconnect switch and security interlock status panel"
            lit_desc = "Emergency amber warning accents (590nm) contrasting against cold 5000K industrial concrete shadows"
            mat_desc = "Heavy cast steel, industrial enamel safety lever, brass terminals, warning hazard stripes"
            atm_desc = "High-voltage electrostatic charge, urgent industrial silence, clean dry air"
            cam_lens = "85mm Macro Prime"
            cam_pos = "Close-up eye-level inspection"
        else:
            arch_desc = "Subterranean reinforced concrete datacenter hall with endless server racks and yellow overhead cable raceways"
            comp_desc = "Symmetrical central perspective with leading cable trays toward vanishing point"
            lit_desc = "Cold 4500K fluorescent overhead strips with cyan 480nm status LED reflections"
            mat_desc = "Matte concrete pillars, perforated steel floor tiles, brushed dark metal server racks"
            atm_desc = "Cleanroom sterile atmosphere with faint floor mist reflections and deep volumetric depth"
            cam_lens = "24mm Zeiss Ultra-Wide Cinema Prime" if visual_type in ["BLENDER_3D", "AI_IMAGE"] else "35mm Prime"
            cam_pos = "Low eye-level tracking perspective (1.6m above floor)"

        camera = {
            "type": "ARRI Alexa Mini LF Cinema 4K",
            "lens": cam_lens,
            "position": cam_pos,
            "height": "1.6m",
            "movement": "Slow forward dolly push" if visual_type in ["BLENDER_3D", "AI_IMAGE"] else "Static with macro focus drift"
        }
        architecture = narration.get("architecture", arch_desc)
        composition = comp_desc
        lighting = lit_desc
        materials = mat_desc
        atmosphere = atm_desc
        motion = camera["movement"]

        # 5. Generation Method & Prompt Building
        generation_method = "REMOTION_REACT"
        if visual_type in ["AI_IMAGE"]:
            generation_method = "GEMINI_IMAGEN"
            prompt = self.prompt_builder.build_structured_image_prompt(
                subject=subject,
                architecture=architecture,
                camera=camera,
                composition=composition,
                lighting=lighting,
                materials=materials,
                atmosphere=atmosphere
            )
        elif visual_type in ["BLENDER_3D"]:
            generation_method = "BLENDER_CYCLES_PY"
            b_spec = self.prompt_builder.build_blender_spec(
                environment=environment,
                objects=["ServerRackMatrix", "OverheadCableTray", "PerforatedFloor"],
                materials=["MatteConcrete", "BrushedMetal", "CyanLED"],
                camera_pos=[0.0, -14.0, 1.7],
                camera_target=[0.0, 0.0, 1.5],
                lens_mm=24.0
            )
            prompt = json.dumps(b_spec)
        elif visual_type in ["AI_VIDEO"]:
            generation_method = "RUNWAY_GEN3"
            prompt = (
                f"INITIAL FRAME: Cinematic establishing shot of {subject}. "
                f"SUBJECT MOTION: Subtle operational micro-movements. "
                f"CAMERA MOTION: {camera['movement']}. "
                f"ENVIRONMENT MOTION: Ambient cooling airflow. "
                f"LIGHTING MOTION: Subtle pulsing status LEDs. "
                f"FOREGROUND MOTION: Faint floor mist drift. "
                f"BACKGROUND MOTION: Distant rack indicator blinking. "
                f"ENDING FRAME: Closer framed perspective. DURATION: {dur}s."
            )
        else:
            generation_method = "REMOTION_MOTION_GRAPHIC"
            prompt = f"Remotion visual component for {visual_type}: {visual_req or narration_text[:60]}"

        # 6. Shot Planning
        source_ids = claim.get("source_ids", []) if claim else ["SRC-01"]
        evidence_struct = None
        if claim_ids:
            cid = claim_ids[0]
            sid = source_ids[0] if source_ids else "SRC-01"
            evidence_struct = {
                "claim_id": cid,
                "visual_type": visual_type,
                "source_id": sid,
                "display_method": "documentary_evidence_callout"
            }

        shot = self.planner.plan_shot(
            shot_id=shot_id,
            scene_id=scene_id,
            narration_segment_id=seg_id,
            start_time=shot_start,
            duration=dur,
            visual_type=visual_type,
            visual_purpose=narration.get("purpose", "story communication"),
            subject=subject,
            action=action,
            environment=environment,
            camera=camera,
            composition=composition,
            lighting=lighting,
            atmosphere=atmosphere,
            motion=motion,
            generation_method=generation_method,
            generation_prompt=prompt,
            claim_ids=claim_ids,
            source_ids=source_ids,
            evidence=evidence_struct
        )

        # 7. Enrich with Continuity & Visual Bible
        shot = self.continuity_mgr.enrich_shot_with_continuity(shot)
        return shot

if __name__ == "__main__":
    director = VisualDirector()
    sample_scene = {"scene_id": "SCN-001", "start": 0.0}
    sample_narr = {
        "segment_id": "N001",
        "text": "At 2:13 AM, the autonomous infrastructure agent began executing tools without human intervention.",
        "visual_requirement": "Show underground datacenter scale",
        "claim_ids": ["CLM-01"]
    }
    shot = director.direct_shot("SHT-001", sample_scene, sample_narr, None, [])
    print("Directed Shot Output:\n", json.dumps(shot, indent=2))
