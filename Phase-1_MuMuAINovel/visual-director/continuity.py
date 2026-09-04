"""
Continuity Engine (Phase 1 Visual Director)
Maintains narrative and visual identity across the entire documentary timeline.
Enforces:
1. Recurring Entity identities (characters, facilities, hardware)
2. Documentary Visual Bible rules (lighting, architectural motifs, lens choices, color behavior)
3. Historical accuracy and timeline coherence
"""

from typing import Dict, List, Any, Optional

class VisualContinuityManager:
    def __init__(self, bible: Optional[Dict[str, Any]] = None, entities: Optional[List[Dict[str, Any]]] = None):
        self.bible = bible or {}
        self.entities = entities or []

    def get_character_identity(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        for char in self.bible.get("characters", []):
            if char.get("character_id") == name_or_id or char.get("name", "").lower() in name_or_id.lower():
                return char
        return None

    def get_location_identity(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        for loc in self.bible.get("locations", []):
            if loc.get("location_id") == name_or_id or loc.get("name", "").lower() in name_or_id.lower():
                return loc
        return None

    def enrich_shot_with_continuity(self, shot: Dict[str, Any]) -> Dict[str, Any]:
        """Applies character wardrobe, facial invariants, location architecture, and lighting rules to a shot."""
        subj = shot.get("subject", "")
        env = shot.get("environment", "")

        continuity_notes = []

        # Check characters
        char_match = self.get_character_identity(subj)
        if char_match:
            continuity_notes.append(
                f"Subject Invariant: {char_match['name']}, {char_match.get('appearance', '')}. "
                f"Wardrobe: {char_match.get('wardrobe', '')}. Rule: {char_match.get('identity_rules', '')}"
            )

        # Check locations
        loc_match = self.get_location_identity(env)
        if loc_match:
            continuity_notes.append(
                f"Location Invariant: {loc_match['name']}. Architecture: {loc_match.get('architecture', '')}. "
                f"Lighting: {loc_match.get('lighting', '')}. Rule: {loc_match.get('continuity_rules', '')}"
            )

        # Global Bible rules
        color_rules = self.bible.get("color_behavior", {})
        if color_rules:
            continuity_notes.append(f"Color Grading: {color_rules.get('palette_description', 'Cool industrial shadows with amber/cyan practical accents')}")

        shot["continuity"] = {
            "entity_ids": [char_match["character_id"]] if char_match else [],
            "location_id": loc_match["location_id"] if loc_match else None,
            "continuity_notes": " | ".join(continuity_notes) if continuity_notes else "Adheres to master documentary visual bible style."
        }
        shot["continuity_notes"] = shot["continuity"]["continuity_notes"]
        return shot

if __name__ == "__main__":
    bible_sample = {
        "characters": [
            {
                "character_id": "CHAR-01",
                "name": "Dr. Maya Rao",
                "appearance": "Sharp focused analytical expression, dark hair tied in ponytail",
                "wardrobe": "Dark charcoal technical zip jacket with biometric ID badge",
                "identity_rules": "Consistent facial structure, dark technical jacket"
            }
        ],
        "locations": [
            {
                "location_id": "LOC-01",
                "name": "Atlas Datacenter",
                "architecture": "Brutalist reinforced concrete pillars, overhead yellow cable trays",
                "lighting": "Cold overhead fluorescent with cyan server status LEDs",
                "continuity_rules": "Yellow overhead cable trays always present"
            }
        ]
    }
    mgr = VisualContinuityManager(bible=bible_sample)
    test_shot = {"subject": "Dr. Maya Rao reviewing security trace", "environment": "Atlas Datacenter"}
    enriched = mgr.enrich_shot_with_continuity(test_shot)
    print("Enriched Continuity:", json.dumps(enriched["continuity"], indent=2))
