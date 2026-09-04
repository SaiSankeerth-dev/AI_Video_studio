"""
Shot Planner (Phase 1 Visual Director)
Coordinates the structural composition of each shot:
- Duration and pacing
- Camera position, lens, and movement
- Asset and source requirements
- Section 17 Evidence structures for claimed shots
"""

import json
from typing import Dict, List, Any, Optional

class ShotPlanner:
    def __init__(self, visual_rules: Optional[Dict[str, Any]] = None):
        self.rules = visual_rules or {}

    def plan_shot(
        self,
        shot_id: str,
        scene_id: str,
        narration_segment_id: str,
        start_time: float,
        duration: float,
        visual_type: str,
        visual_purpose: str,
        subject: str,
        action: str,
        environment: str,
        camera: Dict[str, Any],
        composition: str,
        lighting: str,
        atmosphere: str,
        motion: str,
        generation_method: str,
        generation_prompt: str,
        claim_ids: List[str],
        source_ids: List[str],
        evidence: Optional[Dict[str, Any]] = None,
        transition_in: str = "CUT",
        transition_out: str = "CUT"
    ) -> Dict[str, Any]:
        """Creates a fully specified shot record conforming to Section 9 & 25 schema."""
        end_time = round(start_time + duration, 2)
        start_time = round(start_time, 2)
        duration = round(duration, 2)

        shot = {
            "shot_id": shot_id,
            "scene_id": scene_id,
            "narration_segment": narration_segment_id,
            "start": start_time,
            "start_time": start_time,
            "end": end_time,
            "end_time": end_time,
            "duration": duration,
            "visual_type": visual_type,
            "visual_purpose": visual_purpose,
            "subject": subject,
            "action": action,
            "environment": environment,
            "camera": camera.get("type", "35mm cinema camera"),
            "lens": camera.get("lens", "35mm f/2.0"),
            "composition": composition,
            "lighting": lighting,
            "atmosphere": atmosphere,
            "motion": motion,
            "generation_method": generation_method,
            "generation_prompt": generation_prompt,
            "asset_requirement": f"Render or asset for {visual_type} at 1080p 30fps",
            "asset_requirements": [f"{visual_type.lower()}_primary_layer"],
            "source_requirement": "Vetted primary source" if claim_ids else "None",
            "source_ids": source_ids,
            "claim_ids": claim_ids,
            "transition_in": transition_in,
            "transition_out": transition_out,
            "continuity": {},
            "continuity_notes": ""
        }

        # If shot references claims, attach Section 17 evidence structure
        if claim_ids:
            if evidence:
                shot["evidence"] = evidence
            else:
                cid = claim_ids[0]
                sid = source_ids[0] if source_ids else "SRC-01"
                shot["evidence"] = {
                    "claim_id": cid,
                    "visual_type": visual_type,
                    "source_id": sid,
                    "display_method": "documentary_evidence_callout"
                }

        return shot

if __name__ == "__main__":
    planner = ShotPlanner()
    s = planner.plan_shot(
        shot_id="SHT-021A",
        scene_id="SCN-021",
        narration_segment_id="N021",
        start_time=120.0,
        duration=3.5,
        visual_type="AI_IMAGE",
        visual_purpose="Detail inspection of agent execution",
        subject="Operator terminal",
        action="Displaying autonomous tool invocation",
        environment="Atlas Datacenter",
        camera={"type": "Cinema 4K", "lens": "50mm prime"},
        composition="Tight medium-close foreground framing",
        lighting="Subtle blue CRT bounce",
        atmosphere="Clean industrial air",
        motion="Static with terminal text scroll",
        generation_method="GEMINI_IMAGEN",
        generation_prompt="SUBJECT: Terminal... ARCHITECTURE: Concrete...",
        claim_ids=["CLM-02"],
        source_ids=["SRC-01"]
    )
    print("Planned Shot:", json.dumps(s, indent=2))
