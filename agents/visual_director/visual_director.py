"""
Visual Director & Medium Selector Agent (TASK 10)
Chooses the optimal visual medium for each shot based on editorial content rather than
generating AI images for every sentence. Enforces documentary streak rules and macro balance.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

VALID_MEDIUMS = [
    "REAL_FOOTAGE", "ARCHIVAL_FOOTAGE", "AI_CINEMATIC_IMAGE", "AI_VIDEO",
    "SCREEN_RECORDING", "SCREEN_RECONSTRUCTION", "DOCUMENT", "EVIDENCE_CARD",
    "PHOTO", "MAP", "3D_BLENDER", "MOTION_GRAPHICS", "DATA_VISUALIZATION",
    "UI_ANIMATION", "KINETIC_TYPOGRAPHY", "DIAGRAM", "ENVIRONMENT_SHOT",
    "HUMAN_SCENE", "OBJECT_MACRO", "ABSTRACT_TRANSITION"
]

class VisualDirector:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(r"D:\gitM\01_ContentFactory\production\shots")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def select_medium_for_content(self, shot_subject: str, purpose: str, narration: str) -> str:
        """
        Determines the most authentic documentary medium:
        Evidence claims -> DOCUMENT / EVIDENCE_CARD
        Software actions -> SCREEN_RECONSTRUCTION / SCREEN_RECORDING
        Spatial network -> 3D_BLENDER
        Comparative stats -> DATA_VISUALIZATION / MOTION_GRAPHICS
        Thesis statements -> KINETIC_TYPOGRAPHY
        Atmosphere -> AI_CINEMATIC_IMAGE / HUMAN_SCENE
        """
        sub = shot_subject.lower()
        purp = purpose.lower()
        narr = narration.lower()

        if "blackout" in purp or "thesis" in purp or "typography" in sub:
            return "KINETIC_TYPOGRAPHY"
        if "evidence" in purp or "highlight" in purp:
            return "EVIDENCE_CARD"
        if "document" in sub or "report" in sub or "paper" in sub:
            return "DOCUMENT"
        if "chart" in sub or "benchmark" in sub or "comparison" in purp or "%" in narr:
            return "DATA_VISUALIZATION"
        if "blender" in sub or "spatial" in purp or "network" in sub or "lattice" in sub:
            return "3D_BLENDER"
        if "terminal" in sub or "browser" in sub or "code" in sub or "reconstruction" in purp:
            if "typing" in sub or "patch" in purp or "active" in purp:
                return "SCREEN_RECORDING"
            return "SCREEN_RECONSTRUCTION"
        if "hand" in sub or "engineer" in sub or "human" in purp:
            return "HUMAN_SCENE"
        if "macro" in sub or "cursor" in sub:
            return "OBJECT_MACRO"
        
        return "AI_CINEMATIC_IMAGE"

    def audit_shot_distribution(self, shots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ensures streak <= 2 and validates macro distribution of mediums.
        """
        violations = []
        counts = {}
        for i, shot in enumerate(shots):
            m = shot.get("visual_type", "UNKNOWN")
            counts[m] = counts.get(m, 0) + 1
            if i >= 2:
                if shots[i-2].get("visual_type") == shots[i-1].get("visual_type") == m:
                    violations.append(f"Streak violation at shot {shot.get('shot_id')}: '{m}' used 3 times in a row")

        total = len(shots)
        distribution = {k: f"{(v/total)*100:.1f}%" for k, v in counts.items()}

        # Verify no medium single-handedly exceeds 35% of the documentary
        for k, v in counts.items():
            if (v / total) > 0.35 and total > 5:
                violations.append(f"Medium '{k}' dominates {distribution[k]} of the project (Max 35%)")

        return {
            "passed": len(violations) == 0,
            "total_shots": total,
            "distribution": distribution,
            "violations": violations
        }

if __name__ == "__main__":
    from agents.shot_director.shot_director import ShotDirector
    sd = ShotDirector()
    plan = sd.generate_90s_benchmark_shot_plan()
    vd = VisualDirector()
    audit = vd.audit_shot_distribution(plan["shots"])
    print("Visual Director Audit:", audit)
