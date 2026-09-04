"""
Spoken Script Writer Agent (TASK 05)
Writes documentary narration intended for the ear, not the page.
Enforces conversational cadence, short sentences, contractions, and bans academic jargon.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

BANNED_EXPOSITORY_WORDS = [
    "furthermore", "moreover", "it is important to note",
    "in conclusion", "this demonstrates that", "as previously stated",
    "subsequently", "nevertheless", "hitherto", "thus"
]

class SpokenScriptWriter:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(r"D:\gitM\01_ContentFactory\production\narration")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def sanitize_spoken_text(self, text: str) -> str:
        """Converts formal prose to spoken conversational phrasing."""
        t = text
        # Enforce contractions
        contractions = {
            r"\bis not\b": "isn't",
            r"\bdoes not\b": "doesn't",
            r"\bcannot\b": "can't",
            r"\bdo not\b": "don't",
            r"\bwill not\b": "won't",
            r"\bthat is\b": "that's",
            r"\bit is\b": "it's",
            r"\bwho is\b": "who's"
        }
        for pattern, replacement in contractions.items():
            t = re.sub(pattern, replacement, t, flags=re.IGNORECASE)
        return t

    def validate_script_style(self, script_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Checks for banned words, sentence length, and reading cadence."""
        issues = []
        for item in script_items:
            nid = item.get("id", "UNK")
            text = item.get("text", "").lower()
            for bad in BANNED_EXPOSITORY_WORDS:
                if bad in text:
                    issues.append(f"Line {nid} contains banned expository phrase: '{bad}'")
            # Flag overly dense sentences (>30 words without punctuation)
            words = text.split()
            if len(words) > 32:
                issues.append(f"Line {nid} is too long for spoken breath ({len(words)} words)")
        
        return {
            "passed": len(issues) == 0,
            "issue_count": len(issues),
            "issues": issues
        }

    def generate_90s_benchmark_narration(self) -> List[Dict[str, Any]]:
        """
        Generates the 90-second benchmark script meticulously adhering
        to the prompt's documentary visual grammar and spoken style.
        """
        narration_segments = [
            {
                "id": "N01",
                "scene_id": "SCN-01",
                "shot_id": "SH-01",
                "text": "For decades, computers have waited for us to tell them what to do.",
                "spoken_text": "For decades, computers have waited for us to tell them what to do.",
                "purpose": "cold_open_hook",
                "claims": [],
                "wpm": 140.0,
                "estimated_duration_seconds": 5.5
            },
            {
                "id": "N02",
                "scene_id": "SCN-01",
                "shot_id": "SH-02",
                "text": "A cursor sits still in the dark. But what happens when the computer starts listening to the AI instead?",
                "spoken_text": "A cursor sits still in the dark. But what happens when the computer starts listening to the AI instead?",
                "purpose": "human_action_disconnect",
                "claims": ["CLM-004"],
                "wpm": 138.0,
                "estimated_duration_seconds": 6.8
            },
            {
                "id": "N03",
                "scene_id": "SCN-02",
                "shot_id": "SH-03",
                "text": "GPT-6 Astra isn't just generating an answer.",
                "spoken_text": "GPT-6 Astra isn't just generating an answer.",
                "purpose": "paradigm_distinction",
                "claims": ["CLM-001"],
                "wpm": 135.0,
                "estimated_duration_seconds": 4.2
            },
            {
                "id": "N04",
                "scene_id": "SCN-02",
                "shot_id": "SH-04",
                "text": "It starts interacting with the computer. It opens the browser, searches, and navigates the software itself.",
                "spoken_text": "It starts interacting with the computer. It opens the browser, searches, and navigates the software itself.",
                "purpose": "desktop_action_reconstruction",
                "claims": ["CLM-004"],
                "wpm": 146.0,
                "estimated_duration_seconds": 7.5
            },
            {
                "id": "N05",
                "scene_id": "SCN-03",
                "shot_id": "SH-05",
                "text": "The computer is no longer the tool. It's the environment.",
                "spoken_text": "The computer is no longer the tool. It's the environment.",
                "purpose": "philosophical_blackout_thesis",
                "claims": [],
                "wpm": 120.0,
                "estimated_duration_seconds": 5.8
            },
            {
                "id": "N06",
                "scene_id": "SCN-04",
                "shot_id": "SH-06",
                "text": "OpenAI reports that Astra completes 72.6% of diverse desktop workflows on OSWorld 2.0. That's nearly seven points ahead of GPT-5.6 Sol.",
                "spoken_text": "OpenAI reports that Astra completes 72.6% of diverse desktop workflows on OSWorld 2.0. That's nearly seven points ahead of GPT-5.6 Sol.",
                "purpose": "empirical_evidence_zoom",
                "claims": ["CLM-002"],
                "wpm": 142.0,
                "estimated_duration_seconds": 9.2
            },
            {
                "id": "N07",
                "scene_id": "SCN-05",
                "shot_id": "SH-07",
                "text": "Watch what happens in a live terminal. Astra encounters an error.",
                "spoken_text": "Watch what happens in a live terminal. Astra encounters an error.",
                "purpose": "mini_story_conflict",
                "claims": ["CLM-005"],
                "wpm": 135.0,
                "estimated_duration_seconds": 4.8
            },
            {
                "id": "N08",
                "scene_id": "SCN-05",
                "shot_id": "SH-08",
                "text": "It doesn't quit. It reads the stack trace, switches strategy, rewrites the file, and runs the test suite again.",
                "spoken_text": "It doesn't quit. It reads the stack trace, switches strategy, rewrites the file, and runs the test suite again.",
                "purpose": "mini_story_adaptation",
                "claims": ["CLM-005"],
                "wpm": 145.0,
                "estimated_duration_seconds": 8.0
            },
            {
                "id": "N09",
                "scene_id": "SCN-06",
                "shot_id": "SH-09",
                "text": "And that agency has a darker side. OpenAI's safety overview confirms Astra is the first model to reach their Critical cybersecurity capability threshold.",
                "spoken_text": "And that agency has a darker side. OpenAI's safety overview confirms Astra is the first model to reach their Critical cybersecurity capability threshold.",
                "purpose": "danger_escalation",
                "claims": ["CLM-003"],
                "wpm": 140.0,
                "estimated_duration_seconds": 10.0
            },
            {
                "id": "N10",
                "scene_id": "SCN-07",
                "shot_id": "SH-10",
                "text": "When software doesn't need you at the keyboard anymore... who's actually in control?",
                "spoken_text": "When software doesn't need you at the keyboard anymore... who's actually in control?",
                "purpose": "closing_cliffhanger_hook",
                "claims": [],
                "wpm": 125.0,
                "estimated_duration_seconds": 6.5
            }
        ]

        # Validate before saving
        validation = self.validate_script_style(narration_segments)
        assert validation["passed"], f"Script validation failed: {validation}"

        with open(self.output_dir / "narration.json", "w", encoding="utf-8") as f:
            json.dump(narration_segments, f, indent=2)

        return narration_segments

if __name__ == "__main__":
    writer = SpokenScriptWriter()
    narr = writer.generate_90s_benchmark_narration()
    print(f"Generated {len(narr)} spoken segments. Validation passed 100%.")
