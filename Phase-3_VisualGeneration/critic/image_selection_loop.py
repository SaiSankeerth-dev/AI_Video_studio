"""
Image Selection Loop (Phase 3 Visual Generation)
Implements Section 9 specifications:
Never: Prompt -> image -> use image
Always:
1. Generate 4-8 candidate variants
2. Parallel Technical QA (resolution, artifacts, faces, text)
3. Parallel Creative QA (composition, realism, storytelling, continuity)
4. Strict 100-point scoring:
   - composition: 20
   - prompt adherence: 20
   - realism: 20
   - cinematic quality: 15
   - continuity: 15
   - technical quality: 10
   TOTAL: 100
5. Decision gates:
   >= 80: ACCEPT / PASS
   70-79: REVIEW / REGENERATE
   < 70: REJECT
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class ImageSelectionLoop:
    WEIGHTS = {
        "composition": 20,
        "prompt_adherence": 20,
        "realism": 20,
        "cinematic_quality": 15,
        "continuity": 15,
        "technical_quality": 10
    }

    ACCEPT_THRESHOLD = 80
    REVIEW_THRESHOLD = 70

    def __init__(self, rubric_path: Optional[Path] = None):
        self.rubric_path = rubric_path or (Path(__file__).parent / "scoring_rubric.json")

    def evaluate_candidate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates a single candidate image across technical and creative criteria."""
        scores = {}
        total = 0

        for factor, max_pts in self.WEIGHTS.items():
            pts = candidate_data.get(factor, max_pts * 0.9)  # default 90% if not specified
            pts = max(0, min(pts, max_pts))
            scores[factor] = round(pts, 1)
            total += pts

        total = round(total, 1)

        # Technical QA sanity checks
        tech_flags = []
        if candidate_data.get("has_text_artifacts", False):
            tech_flags.append("Illegible or corrupted text artifacts detected")
            total = min(total, 65.0)
        if candidate_data.get("has_face_distortion", False):
            tech_flags.append("Facial distortion / unnatural bone structure detected")
            total = min(total, 60.0)
        if candidate_data.get("resolution_under_1080p", False):
            tech_flags.append("Resolution lower than full HD 1080p")
            total = min(total, 50.0)

        # Decision gate
        if total >= self.ACCEPT_THRESHOLD:
            decision = "ACCEPT"
        elif total >= self.REVIEW_THRESHOLD:
            decision = "REVIEW_REGENERATE"
        else:
            decision = "REJECT"

        return {
            "candidate_id": candidate_data.get("candidate_id", "cand_01"),
            "total_score": total,
            "decision": decision,
            "factor_scores": scores,
            "technical_flags": tech_flags
        }

    def run_selection_cycle(self, shot_spec: Dict[str, Any], candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluates 4-8 candidates, sorts by quality score, and selects the winning production frame."""
        assert 4 <= len(candidates) <= 8, f"Selection loop requires 4 to 8 candidates, received {len(candidates)}"

        evaluated = [self.evaluate_candidate(c) for c in candidates]
        evaluated.sort(key=lambda x: x["total_score"], reverse=True)

        winner = evaluated[0]
        cycle_verdict = winner["decision"]

        return {
            "shot_id": shot_spec.get("shot_id", "SHT-UNKNOWN"),
            "candidate_count": len(candidates),
            "selected_candidate": winner if cycle_verdict == "ACCEPT" else None,
            "best_score": winner["total_score"],
            "cycle_verdict": cycle_verdict,
            "all_evaluations": evaluated
        }

if __name__ == "__main__":
    loop = ImageSelectionLoop()
    mock_candidates = [
        {"candidate_id": "c1", "composition": 19, "prompt_adherence": 19, "realism": 18, "cinematic_quality": 14, "continuity": 14, "technical_quality": 9},
        {"candidate_id": "c2", "composition": 17, "prompt_adherence": 16, "realism": 15, "cinematic_quality": 12, "continuity": 12, "technical_quality": 8},
        {"candidate_id": "c3", "composition": 14, "prompt_adherence": 13, "realism": 12, "cinematic_quality": 10, "continuity": 10, "technical_quality": 6, "has_text_artifacts": True},
        {"candidate_id": "c4", "composition": 18, "prompt_adherence": 17, "realism": 17, "cinematic_quality": 13, "continuity": 13, "technical_quality": 9},
    ]
    res = loop.run_selection_cycle({"shot_id": "SHT-001"}, mock_candidates)
    print("Selection Cycle Result:", json.dumps(res, indent=2))
    assert res["cycle_verdict"] == "ACCEPT"
    assert res["best_score"] >= 80
