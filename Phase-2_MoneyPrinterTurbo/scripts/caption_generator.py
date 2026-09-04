"""
Caption & Subtitle Generator (Phase 2 MoneyPrinterTurbo)
Generates:
1. Dynamic word-level highlight timings for Remotion (FernSubtitle & KineticCaption)
2. Industry-standard WebVTT (.vtt) and SubRip (.srt) caption files
3. Frame-accurate timing mapped to target FPS (default: 30fps)
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class CaptionGenerator:
    def __init__(self, fps: int = 30, output_dir: Optional[Path] = None):
        self.fps = fps
        self.output_dir = output_dir or (Path(__file__).parents[1] / "subtitles")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _seconds_to_srt_time(self, seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    def _seconds_to_vtt_time(self, seconds: float) -> str:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{mins:02d}:{secs:02d}.{millis:03d}"

    def generate_subtitles(self, narration_segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        sentences = []
        srt_lines = []
        vtt_lines = ["WEBVTT", ""]

        for i, seg in enumerate(narration_segments):
            start_s = seg.get("start", 0.0)
            end_s = seg.get("end", start_s + seg.get("duration", 5.0))
            dur_s = end_s - start_s
            text = seg.get("text", "")
            sid = seg.get("segment_id", f"s{i+1:02d}")

            start_frame = int(round(start_s * self.fps))
            dur_frames = int(round(dur_s * self.fps))

            # Word-level breakdown
            words = text.split()
            word_count = len(words)
            word_dur = dur_s / word_count if word_count > 0 else 0.5
            word_tokens = []

            for w_idx, w in enumerate(words):
                w_start = start_s + (w_idx * word_dur)
                w_end = w_start + word_dur
                word_tokens.append({
                    "word": w,
                    "start": round(w_start, 2),
                    "end": round(w_end, 2),
                    "startFrame": int(round(w_start * self.fps)),
                    "endFrame": int(round(w_end * self.fps))
                })

            sentences.append({
                "id": sid,
                "text": text,
                "start": start_s,
                "end": end_s,
                "startFrame": start_frame,
                "durationFrames": dur_frames,
                "words": word_tokens,
                "audio_file": f"audio/voiceover/{sid}.wav",
                "sfx": "subtle-hit" if "reveal" in seg.get("purpose", "").lower() else None
            })

            # SRT
            srt_lines.append(str(i + 1))
            srt_lines.append(f"{self._seconds_to_srt_time(start_s)} --> {self._seconds_to_srt_time(end_s)}")
            srt_lines.append(text)
            srt_lines.append("")

            # VTT
            vtt_lines.append(f"{self._seconds_to_vtt_time(start_s)} --> {self._seconds_to_vtt_time(end_s)}")
            vtt_lines.append(text)
            vtt_lines.append("")

        total_frames = sentences[-1]["startFrame"] + sentences[-1]["durationFrames"] if sentences else 0
        total_seconds = sentences[-1]["end"] if sentences else 0.0

        output_data = {
            "fps": self.fps,
            "total_frames": total_frames,
            "total_seconds": total_seconds,
            "sentences": sentences
        }

        # Write files
        json_path = self.output_dir / "synced_captions.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)

        srt_path = self.output_dir / "captions.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))

        vtt_path = self.output_dir / "captions.vtt"
        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(vtt_lines))

        return output_data

if __name__ == "__main__":
    gen = CaptionGenerator(fps=30)
    test_segs = [
        {"segment_id": "s01", "start": 0.0, "end": 4.5, "duration": 4.5, "text": "At two thirteen AM, the server hall was completely silent.", "purpose": "context"},
        {"segment_id": "s02", "start": 4.5, "end": 9.0, "duration": 4.5, "text": "Until one unverified terminal session began executing code.", "purpose": "reveal"}
    ]
    res = gen.generate_subtitles(test_segs)
    print("Captions Generated, total frames:", res["total_frames"])
