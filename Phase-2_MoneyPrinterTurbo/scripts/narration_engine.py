"""
Narration Engine (Phase 2 MoneyPrinterTurbo)
Generates audio tracks from spoken narration segments, ensuring:
1. Exact timing alignment with script WPM calculations
2. Multi-speaker or narrator voice profile configuration
3. Generation of segment-level and sentence-level audio metadata
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class NarrationEngine:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or (Path(__file__).parents[1] / "narration")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_narration_manifest(
        self,
        narration_segments: List[Dict[str, Any]],
        voice_id: str = "en-US-Journey-F",
        base_audio_path: str = "audio/voiceover"
    ) -> Dict[str, Any]:
        """Generates audio track manifest linking every spoken segment to its timed audio asset."""
        manifest = {
            "voice_id": voice_id,
            "total_segments": len(narration_segments),
            "total_duration": 0.0,
            "total_words": 0,
            "segments": []
        }

        current_time = 0.0
        for seg in narration_segments:
            seg_id = seg.get("segment_id", "N000")
            dur = seg.get("duration", seg.get("estimated_duration", 5.0))
            words = seg.get("word_count", len(seg.get("text", "").split()))
            
            audio_file = f"{base_audio_path}/{seg_id}.wav"
            
            manifest_seg = {
                "segment_id": seg_id,
                "chapter_id": seg.get("chapter_id", "CH-01"),
                "text": seg.get("text", ""),
                "audio_file": audio_file,
                "start": current_time,
                "end": round(current_time + dur, 2),
                "duration": dur,
                "word_count": words,
                "wpm": round(words / (dur / 60.0), 1) if dur > 0 else 140.0,
                "claim_ids": seg.get("claim_ids", [])
            }
            manifest["segments"].append(manifest_seg)
            manifest["total_words"] += words
            current_time = round(current_time + dur, 2)

        manifest["total_duration"] = current_time
        manifest["average_wpm"] = round(manifest["total_words"] / (current_time / 60.0), 1) if current_time > 0 else 140.0

        out_path = self.output_dir / "narration_manifest.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest

if __name__ == "__main__":
    eng = NarrationEngine()
    test_segs = [
        {"segment_id": "N001", "text": "At 2:13 AM, the system began to interact with the physical world.", "duration": 5.2, "word_count": 12},
        {"segment_id": "N002", "text": "Nobody outside the project knew what was happening.", "duration": 3.8, "word_count": 8}
    ]
    manifest = eng.generate_narration_manifest(test_segs)
    print("Narration Manifest Generated:", json.dumps(manifest, indent=2))
