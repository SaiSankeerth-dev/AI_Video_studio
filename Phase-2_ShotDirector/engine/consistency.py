import json
from pathlib import Path

class VisualConsistencyEngine:
    def __init__(self, visual_bible_path=None):
        if visual_bible_path and Path(visual_bible_path).exists():
            with open(visual_bible_path, "r", encoding="utf-8") as f:
                self.bible = json.load(f)
        else:
            self.bible = self._default_bible()

    def _default_bible(self):
        return {
            "project": {
                "visual_language": "photorealistic investigative documentary",
                "aspect_ratio": "16:9",
                "camera_language": "35mm and 50mm cinema lenses, natural perspective, slow controlled camera dollies",
                "lighting_rules": "motivated practical lighting, high contrast chiaroscuro, cold industrial cyan LEDs with warm tungsten accents, avoid saturated neon sci-fi"
            },
            "characters": {
                "maya": {
                    "full_name": "Dr. Maya Rao",
                    "role": "AI Safety & Systems Architect",
                    "appearance": "34-year-old Indian engineer, sharp focused expression, dark hair tied back in a neat professional ponytail",
                    "wardrobe": "dark charcoal technical zip jacket over a black crewneck, lanyard ID badge"
                },
                "daniel": {
                    "full_name": "Daniel Ross",
                    "role": "Lead Infrastructure & Reliability Engineer",
                    "appearance": "42-year-old systems engineer, tired analytical expression, wire-rim glasses, short graying dark hair",
                    "wardrobe": "navy fleece jacket over an Oxford shirt, smartwatch"
                }
            },
            "locations": {
                "atlas_datacenter": {
                    "name": "Atlas Subterranean Hyperscale Facility",
                    "architecture": "brutalist reinforced concrete pillars, infinite dark server corridors, overhead yellow cable trays, acoustic wall baffling",
                    "materials": "matte concrete, brushed anodized black server racks, perforated raised floor tiles, optical fiber conduits",
                    "lighting": "dim cold fluorescent overhead strips, pulsating cyan server status LEDs, isolated emergency amber indicators"
                },
                "observation_deck": {
                    "name": "Atlas Glass Observation & Monitoring Room",
                    "architecture": "dark subterranean glass control pod overlooking the server hall, wrap-around acoustic glass",
                    "materials": "dark acoustic felt panels, matte black consoles, tempered glass reflections",
                    "lighting": "glow from multiple 4K diagnostic monitors, single warm desktop task lamp"
                }
            }
        }

    def enrich_shot(self, shot):
        # Character lookup
        subj_lower = shot.get("subject", "").lower()
        for char_key, char_data in self.bible.get("characters", {}).items():
            if char_key in subj_lower or char_data["full_name"].lower() in subj_lower:
                shot["subject_details"] = f"{char_data['full_name']}, {char_data['appearance']}, wearing {char_data['wardrobe']}"
                break
        
        # Location lookup
        env_lower = shot.get("environment", "").lower()
        for loc_key, loc_data in self.bible.get("locations", {}).items():
            if loc_key in env_lower or loc_data["name"].lower() in env_lower or "server" in env_lower or "datacenter" in env_lower:
                shot["location_details"] = f"{loc_data['architecture']}, constructed with {loc_data['materials']}. Lighting: {loc_data['lighting']}"
                break

        # Global style constraints
        shot["global_style"] = self.bible["project"]["visual_language"]
        shot["lighting_rules"] = self.bible["project"]["lighting_rules"]
        return shot
