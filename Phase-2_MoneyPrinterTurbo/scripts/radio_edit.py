"""
Radio Edit Engine (Phase 2 MoneyPrinterTurbo)
Assembles the complete audio-first edit before visual generation.
Implements Section 16 specifications:
7 Audio Layers:
- VOICE (spoken narration)
- MUSIC (ambient, tension, resolution score with ducking and volume curves)
- AMBIENCE (room tone, datacenter hum, sterile HVAC)
- SFX (keystrokes, terminal beeps, mechanical switches)
- IMPACTS (sub-bass hits on pivotal moments)
- TRANSITIONS (whooshes, risers, cut transients)
- SILENCE (strategic pauses before major reveals)
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class RadioEditEngine:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or (Path(__file__).parents[1] / "base-animatic")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def assemble_radio_edit(
        self,
        narration_segments: List[Dict[str, Any]],
        audio_plan_scenes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Builds multi-track synchronized audio blueprint with ducking and strategic silence."""
        tracks = {
            "voice": [],
            "music": [],
            "ambience": [],
            "sfx": [],
            "impacts": [],
            "transitions": [],
            "silence": []
        }

        total_duration = narration_segments[-1]["end"] if narration_segments else 0.0

        # 1. Voice track
        for seg in narration_segments:
            sid = seg.get("segment_id", "vox_01")
            dur = seg.get("duration", seg.get("estimated_duration", round(seg["end"] - seg["start"], 2)))
            tracks["voice"].append({
                "id": f"vox_{sid}",
                "start": seg["start"],
                "duration": dur,
                "end": seg["end"],
                "file": f"audio/voiceover/{sid}.wav",
                "text": seg.get("text", ""),
                "volume": 1.0
            })

        # 2. Ambience track (Continuous background floor)
        tracks["ambience"].append({
            "id": "amb_datacenter_hvac",
            "start": 0.0,
            "duration": total_duration,
            "file": "audio/ambient-drone.wav",
            "volume": 0.12,
            "loop": True
        })

        # 3. Dynamic Music with strategic cuts/silence before reveals
        current_time = 0.0
        last_chapter = None
        for i, seg in enumerate(narration_segments):
            purpose = seg.get("purpose", "").lower()
            emotion = seg.get("emotion", "").lower()
            dur = seg.get("duration", seg.get("estimated_duration", round(seg["end"] - seg["start"], 2)))
            start_t = seg["start"]
            ch_id = seg.get("chapter_id", "")

            # Chapter boundary transition whoosh / riser
            if ch_id and ch_id != last_chapter and i > 0:
                tracks["transitions"].append({
                    "id": f"trans_ch_{ch_id}",
                    "start": max(0.0, start_t - 0.5),
                    "duration": 1.5,
                    "file": "audio/whoosh-transition.wav",
                    "type": "CHAPTER_TRANSITION",
                    "volume": 0.35
                })
            last_chapter = ch_id

            # Strategic silence before reveal (spaced at least 4s apart)
            is_reveal_moment = ("reveal" in purpose or "tension" in emotion or "climax" in purpose)
            last_silence_end = (tracks["silence"][-1]["start"] + tracks["silence"][-1]["duration"]) if tracks["silence"] else -10.0
            silence_start = max(0.0, start_t - 0.8)

            if is_reveal_moment and (silence_start >= last_silence_end + 4.0):
                # Insert 0.8s silence window right at the reveal moment
                tracks["silence"].append({
                    "id": f"silence_pre_{seg['segment_id']}",
                    "start": silence_start,
                    "duration": 0.8,
                    "purpose": f"Strategic tension pause before {seg.get('segment_id', 'reveal')} reveal"
                })

                tracks["transitions"].append({
                    "id": f"trans_reveal_{seg['segment_id']}",
                    "start": silence_start,
                    "duration": 0.8,
                    "file": "audio/riser-cut.wav",
                    "type": "REVEAL_CUT_TRANSIENT",
                    "volume": 0.3
                })

                tracks["impacts"].append({
                    "id": f"impact_{seg['segment_id']}",
                    "start": start_t + 0.2,
                    "duration": 2.5,
                    "file": "audio/subtle-impact.wav",
                    "volume": 0.4
                })

                # Music ducks during reveal, then resumes
                tracks["music"].append({
                    "id": f"mus_tension_{seg['segment_id']}",
                    "start": start_t + 0.5,
                    "duration": max(0.5, dur - 0.5),
                    "file": "audio/ambient-dark.wav",
                    "volume": 0.04,  # ducked beneath spoken voice
                    "state": "RISING_TENSION"
                })
            else:
                tracks["music"].append({
                    "id": f"mus_bed_{seg['segment_id']}",
                    "start": start_t,
                    "duration": dur,
                    "file": "audio/ambient-dark.wav",
                    "volume": 0.035,
                    "state": "STEADY_BED"
                })

            # Check SFX triggers
            text_lower = seg.get("text", "").lower()
            if any(w in text_lower for w in ["code", "terminal", "execut"]):
                tracks["sfx"].append({
                    "id": f"sfx_term_{seg['segment_id']}",
                    "start": start_t + 0.5,
                    "duration": 1.8,
                    "file": "audio/terminal-typing.wav",
                    "volume": 0.25
                })
            elif any(w in text_lower for w in ["switch", "air-gap", "kill"]):
                tracks["sfx"].append({
                    "id": f"sfx_switch_{seg['segment_id']}",
                    "start": start_t + 0.3,
                    "duration": 1.2,
                    "file": "audio/mechanical-switch.wav",
                    "volume": 0.5
                })

        radio_edit = {
            "title": "Master Radio Edit",
            "total_duration": total_duration,
            "channels": 7,
            "tracks": tracks,
            "compliance": "Meets Section 16 Strategic Audio & Silence Architecture"
        }

        out_path = self.output_dir / "radio_edit.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(radio_edit, f, indent=2)

        return radio_edit

if __name__ == "__main__":
    radio = RadioEditEngine()
    test_segs = [
        {"segment_id": "N01", "start": 0.0, "end": 6.0, "duration": 6.0, "text": "In a subterranean data center, an agent began working.", "purpose": "context"},
        {"segment_id": "N02", "start": 6.0, "end": 13.0, "duration": 7.0, "text": "Until one document surfaced showing it attempted to disable containment.", "purpose": "reveal", "emotion": "tension"}
    ]
    edit = radio.assemble_radio_edit(test_segs)
    print("Radio Edit Assembled. Total silence cues:", len(edit["tracks"]["silence"]))
