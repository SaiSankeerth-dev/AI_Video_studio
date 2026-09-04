"""
Visual Selector (Phase 1 Visual Director)
Dynamically selects visual medium without hardcoding fixed percentages.
Balancing:
- Real Material: Archival footage, authentic photos, forensic documents, screen captures.
- Generated Material: AI images, AI video, Blender 3D architectural reconstructions.
- Motion Graphics: Remotion diagrams, maps, timelines, charts, code visualizers.
Enforces the rule: Never exceed 2 consecutive shots of the same visual archetype.
"""

from typing import Dict, List, Any, Optional

MACRO_CATEGORIES = {
    "REAL_MATERIAL": [
        "ARCHIVAL_FOOTAGE", "REAL_FOOTAGE", "PHOTOGRAPH", "DOCUMENT",
        "SCREEN_CAPTURE", "NEWS_CLIP", "INTERVIEW", "TEXTURE_BROLL"
    ],
    "GENERATED_MATERIAL": [
        "AI_IMAGE", "AI_VIDEO", "BLENDER_3D", "UI_RECONSTRUCTION"
    ],
    "GRAPHICS": [
        "MAP", "SATELLITE_MAP", "QUOTE_CARD", "DATA_GRAPHIC",
        "TIMELINE", "DIAGRAM", "CODE_VISUALIZATION", "NETWORK_GRAPH",
        "MOTION_GRAPHIC", "ABSTRACT_TRANSITION"
    ]
}

class VisualSelector:
    def __init__(self, rules: Optional[Dict[str, Any]] = None):
        self.rules = rules or {}
        self.max_streak = self.rules.get("max_consecutive_same_visual_type", 2)
        self.macro_categories = MACRO_CATEGORIES

    def get_macro_category(self, visual_type: str) -> str:
        """Returns the Section 7 macro archetype (REAL_MATERIAL, GENERATED_MATERIAL, GRAPHICS)."""
        vt = visual_type.upper()
        for cat, types in self.macro_categories.items():
            if vt in types:
                return cat
        return "GENERATED_MATERIAL"

    def calculate_distribution(self, shots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates dynamic documentary visual distribution across types and Section 7 macro categories."""
        if not shots:
            return {"total_shots": 0, "macro_distribution": {}, "type_distribution": {}}

        total = len(shots)
        type_counts: Dict[str, int] = {}
        macro_counts: Dict[str, int] = {"REAL_MATERIAL": 0, "GENERATED_MATERIAL": 0, "GRAPHICS": 0}

        for s in shots:
            vt = s.get("visual_type", "UNKNOWN").upper()
            type_counts[vt] = type_counts.get(vt, 0) + 1
            macro = self.get_macro_category(vt)
            macro_counts[macro] = macro_counts.get(macro, 0) + 1

        macro_dist = {
            cat: {
                "count": count,
                "percentage": round((count / total) * 100.0, 1)
            }
            for cat, count in macro_counts.items()
        }

        type_dist = {
            t: {
                "count": count,
                "percentage": round((count / total) * 100.0, 1)
            }
            for t, count in type_counts.items()
        }

        # Check balance: all three pillars represented, no AI image monopoly (>60%)
        is_balanced = (
            macro_counts["REAL_MATERIAL"] > 0 and
            macro_counts["GENERATED_MATERIAL"] > 0 and
            macro_counts["GRAPHICS"] > 0 and
            (type_counts.get("AI_IMAGE", 0) / total) < 0.60
        )

        return {
            "total_shots": total,
            "is_balanced": is_balanced,
            "macro_distribution": macro_dist,
            "type_distribution": type_dist
        }

    def select_medium(
        self,
        narration_text: str,
        visual_requirement: str,
        claim_evidence: Optional[Dict[str, Any]],
        previous_visual_types: List[str]
    ) -> str:
        """Selects optimal visual medium based on communicative effectiveness and streak avoidance."""
        text_lower = narration_text.lower() + " " + visual_requirement.lower()

        # 1. Determine natural candidates based on communicative logic
        candidates = []
        if claim_evidence:
            ev_type = claim_evidence.get("visual_type", "").upper()
            if ev_type in ["DOCUMENT", "SCREEN_CAPTURE", "DATA_GRAPHIC", "TIMELINE", "DIAGRAM", "CODE_VISUALIZATION", "NETWORK_GRAPH"]:
                candidates.append(ev_type)

        if any(w in text_lower for w in ["document", "paper", "memo", "specification", "contract", "filing"]):
            candidates.append("DOCUMENT")
        if any(w in text_lower for w in ["code", "terminal", "diff", "repository", "script", "syntax", "git"]):
            candidates.append("CODE_VISUALIZATION")
        if any(w in text_lower for w in ["map", "datacenter location", "geographical", "continents", "subsea"]):
            candidates.append("MAP")
        if any(w in text_lower for w in ["timeline", "history", "chronology", "months", "years"]):
            candidates.append("TIMELINE")
        if any(w in text_lower for w in ["architecture", "subterranean", "facility", "scale", "fly-through", "infinite server"]):
            candidates.append("BLENDER_3D")
        if any(w in text_lower for w in ["network", "swarm", "communication", "handshake", "agents talking"]):
            candidates.append("NETWORK_GRAPH")
        if any(w in text_lower for w in ["percent", "statistics", "growth", "adoption", "ratio", "benchmark"]):
            candidates.append("DATA_GRAPHIC")
        if any(w in text_lower for w in ["motion", "running", "moving", "typing", "walking"]):
            candidates.append("AI_VIDEO")
        if any(w in text_lower for w in ["close-up", "face", "portrait", "still", "operator", "quiet"]):
            candidates.append("AI_IMAGE")
        if any(w in text_lower for w in ["archival", "early days", "2023", "2022", "historical capture"]):
            candidates.append("ARCHIVAL_FOOTAGE")

        if not candidates:
            candidates = ["AI_IMAGE", "BLENDER_3D", "DIAGRAM", "SCREEN_CAPTURE"]

        # 2. Filter out candidates that violate archetype streak rules
        last_type = previous_visual_types[-1] if previous_visual_types else None
        streak = 0
        if last_type:
            for vt in reversed(previous_visual_types):
                if vt == last_type:
                    streak += 1
                else:
                    break

        for cand in candidates:
            if cand == last_type and streak >= self.max_streak:
                continue
            return cand

        # Fallback to an alternate archetype not matching last_type
        fallbacks = ["DIAGRAM", "DOCUMENT", "BLENDER_3D", "AI_IMAGE", "DATA_GRAPHIC", "SCREEN_CAPTURE"]
        for fb in fallbacks:
            if fb != last_type:
                return fb

        return "AI_IMAGE"

if __name__ == "__main__":
    selector = VisualSelector()
    history = ["AI_IMAGE", "AI_IMAGE"]
    chosen = selector.select_medium("The document revealed three connected facilities.", "show document", None, history)
    print("Selected Medium after 2 AI_IMAGE shots:", chosen)
    assert chosen != "AI_IMAGE", "Streak violation not prevented!"
