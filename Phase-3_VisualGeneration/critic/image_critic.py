import json
from pathlib import Path

class CinematicImageCriticV1:
    def __init__(self, rubric_path=None):
        self.rubric_path = rubric_path or (Path(__file__).parent / "scoring_rubric.json")
        with open(self.rubric_path, "r", encoding="utf-8") as f:
            self.rubric = json.load(f)

    def evaluate(self, shot_spec):
        q = shot_spec.get("quality_targets", {})
        weights = self.rubric["weights"]
        
        overall = sum(q.get(k, 9.0) * weights.get(k, 0.10) for k in weights)
        overall = round(overall, 2)

        decision = "APPROVE"
        if overall < 7.0:
            decision = "REJECT"
        elif overall < 8.0:
            decision = "REGENERATE"
        elif overall < 9.0:
            decision = "REFINE"

        refinements = []
        if q.get("character_consistency", 9.0) < 8.0:
            refinements.append("REFINE CHARACTER: Preserve environment, lighting, and camera angle; adjust facial structure and wardrobe to match character reference.")
        if q.get("environment_consistency", 9.0) < 8.0:
            refinements.append("REFINE ENVIRONMENT: Preserve character and action; restore subterranean concrete pillars and standard Atlas server rack geometry.")
        if q.get("composition", 9.0) < 8.0:
            refinements.append("REFRAME: Recompose subject to the left third to strengthen perspective vanishing lines.")
        if q.get("photorealism", 9.0) < 8.0:
            refinements.append("REGENERATE: Replace synthetic artifacts with physically motivated surface textures and natural optical blur.")

        return {
            "shot_id": shot_spec.get("shot_id"),
            "overall_score": overall,
            "decision": decision,
            "sub_scores": q,
            "refinement_actions": refinements
        }
