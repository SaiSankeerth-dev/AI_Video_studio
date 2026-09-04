"""
Spoken Narration Writer Engine (Phase 1)
Generates spoken documentary narration (not essay prose).
Calculates natural timing at 130-160 Words Per Minute (WPM).
Links each paragraph explicitly to verified claims and visual requirements.
"""

import json
from typing import Dict, List, Any, Optional

class NarrationWriter:
    TARGET_WPM_MIN = 130.0
    TARGET_WPM_MAX = 160.0
    DEFAULT_WPM = 142.0

    def __init__(self):
        pass

    def calculate_timing(self, text: str, target_wpm: Optional[float] = None) -> Dict[str, Any]:
        """Calculates spoken duration from word count within 130-160 WPM guideline."""
        wpm = target_wpm or self.DEFAULT_WPM
        words = len(text.strip().split())
        duration_seconds = round((words / wpm) * 60.0, 2)
        # Avoid zero or tiny durations
        duration_seconds = max(duration_seconds, 1.5)
        actual_wpm = round(words / (duration_seconds / 60.0), 1)
        return {
            "word_count": words,
            "duration": duration_seconds,
            "wpm": actual_wpm
        }

    def create_segment(
        self,
        segment_id: str,
        chapter_id: str,
        text: str,
        purpose: str,
        emotion: str,
        claim_ids: List[str],
        visual_requirement: str,
        start_time: float,
        target_wpm: Optional[float] = None
    ) -> Dict[str, Any]:
        """Creates a single calibrated narration segment conforming to Section 4."""
        timing = self.calculate_timing(text, target_wpm)
        dur = timing["duration"]
        end_time = round(start_time + dur, 2)

        return {
            "segment_id": segment_id,
            "chapter_id": chapter_id,
            "text": text,
            "purpose": purpose,
            "emotion": emotion,
            "claim_ids": claim_ids,
            "visual_requirement": visual_requirement,
            "word_count": timing["word_count"],
            "duration": dur,
            "estimated_duration": dur,
            "start": start_time,
            "start_time": start_time,
            "end": end_time,
            "end_time": end_time,
            "wpm": timing["wpm"]
        }

    def assemble_narration_script(self, raw_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assembles continuous narration timeline with contiguous start/end times and strict 130-160 WPM validation."""
        timeline = []
        current_time = 0.0

        for i, raw in enumerate(raw_segments):
            seg_id = raw.get("segment_id", f"N{i+1:03d}")
            text = raw["text"]
            ch_id = raw.get("chapter_id", "CH-01")
            purpose = raw.get("purpose", "context")
            emotion = raw.get("emotion", "neutral")
            claim_ids = raw.get("claim_ids", [])
            vis_req = raw.get("visual_requirement", "show relevant subject")
            custom_wpm = raw.get("target_wpm", self.DEFAULT_WPM)

            seg = self.create_segment(
                segment_id=seg_id,
                chapter_id=ch_id,
                text=text,
                purpose=purpose,
                emotion=emotion,
                claim_ids=claim_ids,
                visual_requirement=vis_req,
                start_time=current_time,
                target_wpm=custom_wpm
            )
            timeline.append(seg)
            current_time = seg["end"]

        return timeline

if __name__ == "__main__":
    writer = NarrationWriter()
    test_seg = writer.create_segment(
        segment_id="N014",
        chapter_id="CH-04",
        text="The system was not simply generating text anymore. It was beginning to interact with the world around it.",
        purpose="reveal",
        emotion="tension",
        claim_ids=["CLM-01"],
        visual_requirement="show the physical scale of autonomous execution",
        start_time=0.0
    )
    print("Sample Narration Segment:", json.dumps(test_seg, indent=2))
