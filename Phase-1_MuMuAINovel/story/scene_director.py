"""
Scene Director Engine (Phase 1)
Decomposes narration segments into multi-shot cinematic visual sequences.
Implements Section 5 & Section 15:
- Avoids 1-to-1 narration-to-single-image mapping.
- Breaks a single idea into an edited progression (e.g. 21A Close-up, 21B Action, 21C Reaction, 21D Pull back, 21E Wide view, 21F Motion graphic).
- Applies cinematic pacing:
  * High information density -> faster cuts (1.2s - 2.5s)
  * Major reveal -> slower reveal (4.0s - 6.0s)
  * Evidence inspection -> enough screen time to read (4.5s - 7.0s)
  * Emotional / tense moment -> longer sustained shot (5.0s - 8.0s)
"""

import json
from typing import Dict, List, Any, Optional

class SceneDirector:
    def __init__(self):
        pass

    def calculate_shot_pacing(self, shot_purpose: str, visual_type: str, total_available_time: float, shot_count: int) -> float:
        """Calculates dynamic shot duration based on visual importance and density."""
        if shot_count <= 1:
            return round(total_available_time, 2)

        # Baseline weighting according to editorial function
        weights = {
            "ACTION_CUT": 1.5,
            "DETAIL_INSERT": 2.0,
            "RAPID_FIRE": 1.2,
            "ESTABLISHING": 4.5,
            "EVIDENCE_READING": 5.5,
            "MAJOR_REVEAL": 6.0,
            "EMOTIONAL_BEAT": 5.0,
            "TRANSITION": 1.8,
            "MOTION_GRAPHIC": 4.0
        }

        weight = weights.get(shot_purpose, 3.0)
        if visual_type in ["DOCUMENT", "CODE_VISUALIZATION"]:
            weight = max(weight, 4.5)  # give enough time to read code or forensic documents

        return weight

    def decompose_narration_into_scene(
        self,
        scene_id: str,
        chapter_id: str,
        narration_segment: Dict[str, Any],
        beats: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Turns one narration idea into an edited multi-shot sequence with proportional timing."""
        narration_duration = narration_segment.get("duration", 8.0)
        seg_id = narration_segment.get("segment_id", "N001")

        # Proportional duration distribution
        total_raw_weight = sum(b.get("weight", 1.0) for b in beats)
        shots = []
        current_time = narration_segment.get("start", 0.0)

        for i, beat in enumerate(beats):
            letter = chr(ord('A') + i)
            shot_id = f"SHT-{scene_id[-3:]}{letter}" if len(scene_id) >= 3 else f"SHT-{seg_id}_{letter}"
            ratio = beat.get("weight", 1.0) / total_raw_weight
            shot_dur = round(narration_duration * ratio, 2)
            shot_end = round(current_time + shot_dur, 2)

            shots.append({
                "shot_id": shot_id,
                "scene_id": scene_id,
                "narration_segment": seg_id,
                "shot_letter": letter,
                "description": beat["description"],
                "shot_type": beat.get("shot_type", "MEDIUM"),
                "visual_type": beat.get("visual_type", "AI_IMAGE"),
                "pacing_category": beat.get("pacing_category", "DETAIL_INSERT"),
                "duration": shot_dur,
                "start": current_time,
                "end": shot_end,
                "claim_ids": narration_segment.get("claim_ids", [])
            })
            current_time = shot_end

        # Adjust minor rounding discrepancies on the last shot
        if shots:
            discrepancy = round(narration_segment.get("end", current_time) - shots[-1]["end"], 2)
            if abs(discrepancy) > 0.001:
                shots[-1]["end"] = round(shots[-1]["end"] + discrepancy, 2)
                shots[-1]["duration"] = round(shots[-1]["duration"] + discrepancy, 2)

        return {
            "scene_id": scene_id,
            "chapter_id": chapter_id,
            "narration_segment": seg_id,
            "purpose": narration_segment.get("purpose", "story beat"),
            "start": narration_segment.get("start", 0.0),
            "end": narration_segment.get("end", current_time),
            "duration": narration_duration,
            "shots": shots
        }

if __name__ == "__main__":
    director = SceneDirector()
    sample_narration = {
        "segment_id": "N021",
        "start": 120.0,
        "end": 138.0,
        "duration": 18.0,
        "purpose": "reveal",
        "claim_ids": ["CLM-02"]
    }
    sample_beats = [
        {"description": "Extreme close-up of developer terminal prompt awaiting input", "shot_type": "ECU", "visual_type": "SCREEN_CAPTURE", "pacing_category": "DETAIL_INSERT", "weight": 2.4},
        {"description": "Autonomous tool execution kicks off; autonomous script selection", "shot_type": "CU", "visual_type": "CODE_VISUALIZATION", "pacing_category": "ACTION_CUT", "weight": 2.8},
        {"description": "Terminal output cascades with green test passes without human typing", "shot_type": "MCU", "visual_type": "SCREEN_CAPTURE", "pacing_category": "DETAIL_INSERT", "weight": 2.2},
        {"description": "Camera tracks back to reveal empty operator desk under cyan glow", "shot_type": "WIDE", "visual_type": "AI_IMAGE", "pacing_category": "MAJOR_REVEAL", "weight": 4.2},
        {"description": "High-angle view of massive automated server infrastructure", "shot_type": "EXTREME_WIDE", "visual_type": "BLENDER_3D", "pacing_category": "ESTABLISHING", "weight": 3.4},
        {"description": "Remotion technical motion graphic diagramming the closed feedback loop", "shot_type": "GRAPHIC", "visual_type": "DIAGRAM", "pacing_category": "MOTION_GRAPHIC", "weight": 3.0}
    ]
    scene = director.decompose_narration_into_scene("SCN-021", "CH-04", sample_narration, sample_beats)
    print("Decomposed Scene:", json.dumps(scene, indent=2))
