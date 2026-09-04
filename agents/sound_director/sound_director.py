"""
Sound Director Agent (TASK 16)
Orchestrates scene-based multi-track audio design: music states (M01-M08),
foley clicks, ambient room tone, sub-bass impacts, and deliberate strategic silence.
Synthesizes broadcast 48kHz stereo WAV cue assets procedurally.
"""

import json
import math
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np
import scipy.io.wavfile as wavfile

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

class SoundDirector:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or (ROOT_DIR / "production" / "audio")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.sample_rate = 48000

    def generate_90s_benchmark_audio_plan(self, shots: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synthesizes the complete 8-layer audio architecture for the 90-second documentary.
        """
        layers = [
            {"layer_name": "VOICE", "base_volume_db": 0.0, "ducking_db": 0.0},
            {"layer_name": "ROOM_TONE", "base_volume_db": -24.0, "ducking_db": 0.0},
            {"layer_name": "MUSIC", "base_volume_db": -16.0, "ducking_db": -12.0},
            {"layer_name": "FOLEY_KEYBOARD", "base_volume_db": -18.0, "ducking_db": -4.0},
            {"layer_name": "UI_SFX", "base_volume_db": -15.0, "ducking_db": -2.0},
            {"layer_name": "SUB_BASS", "base_volume_db": -8.0, "ducking_db": 0.0},
            {"layer_name": "IMPACT", "base_volume_db": -10.0, "ducking_db": -6.0},
            {"layer_name": "STRATEGIC_SILENCE", "base_volume_db": -99.0, "ducking_db": 0.0}
        ]

        cues = []
        # Continuous Room Tone
        cues.append({
            "cue_id": "CUE-ROOM-01",
            "timestamp_seconds": 0.0,
            "type": "ROOM_TONE",
            "asset": "room_tone_quiet_hvac.wav",
            "duration_seconds": 90.0,
            "volume_db": -24.0
        })

        # Scene-based music transitions
        # M03: Tension Drone (0:00 - 0:15)
        cues.append({
            "cue_id": "CUE-MUS-01",
            "timestamp_seconds": 0.0,
            "type": "MUSIC_THEME",
            "theme": "M03_TENSION_DRONE",
            "asset": "music_m03_tension.wav",
            "duration_seconds": 15.0,
            "volume_db": -18.0
        })
        # M02: Active Investigation Pulse (0:15 - 0:31)
        cues.append({
            "cue_id": "CUE-MUS-02",
            "timestamp_seconds": 15.0,
            "type": "MUSIC_THEME",
            "theme": "M02_INVESTIGATION_PULSE",
            "asset": "music_m02_investigation.wav",
            "duration_seconds": 16.0,
            "volume_db": -16.0
        })
        # M00: TOTAL SILENCE ON BLACKOUT (0:31 - 0:40)
        cues.append({
            "cue_id": "CUE-SILENCE-01",
            "timestamp_seconds": 31.0,
            "type": "SILENCE",
            "asset": "none",
            "duration_seconds": 9.0,
            "volume_db": -99.0
        })
        # Sub-bass hit at cut to black
        cues.append({
            "cue_id": "CUE-SUB-01",
            "timestamp_seconds": 31.0,
            "type": "IMPACT",
            "asset": "sub_bass_drop_60hz.wav",
            "duration_seconds": 2.5,
            "volume_db": -6.0
        })
        # M04: Discovery & Evidence (0:40 - 0:55)
        cues.append({
            "cue_id": "CUE-MUS-03",
            "timestamp_seconds": 40.0,
            "type": "MUSIC_THEME",
            "theme": "M04_DISCOVERY_BELLS",
            "asset": "music_m04_discovery.wav",
            "duration_seconds": 15.0,
            "volume_db": -17.0
        })
        # M05: Escalating Problem Solving (0:55 - 0:70)
        cues.append({
            "cue_id": "CUE-MUS-04",
            "timestamp_seconds": 55.0,
            "type": "MUSIC_THEME",
            "theme": "M05_ESCALATION_ARPEGGIO",
            "asset": "music_m05_escalation.wav",
            "duration_seconds": 15.0,
            "volume_db": -16.0
        })
        # Error SFX at 55.4s
        cues.append({
            "cue_id": "CUE-SFX-ERR",
            "timestamp_seconds": 55.4,
            "type": "SFX",
            "asset": "terminal_error_bell.wav",
            "duration_seconds": 1.0,
            "volume_db": -12.0
        })
        # Success chime harmonic at 65.2s
        cues.append({
            "cue_id": "CUE-SFX-PASS",
            "timestamp_seconds": 65.2,
            "type": "SFX",
            "asset": "pytest_success_chime.wav",
            "duration_seconds": 2.0,
            "volume_db": -14.0
        })
        # M06: Frontier Danger & Cybersecurity (0:70 - 0:82)
        cues.append({
            "cue_id": "CUE-MUS-05",
            "timestamp_seconds": 70.0,
            "type": "MUSIC_THEME",
            "theme": "M06_DANGER_OVERSIGHT",
            "asset": "music_m06_danger.wav",
            "duration_seconds": 12.0,
            "volume_db": -15.0
        })
        # M08: Concluding Cliffhanger & Final Sub Drop (0:82 - 0:90)
        cues.append({
            "cue_id": "CUE-MUS-06",
            "timestamp_seconds": 82.0,
            "type": "MUSIC_THEME",
            "theme": "M08_ENDING_MYSTERY",
            "asset": "music_m08_ending.wav",
            "duration_seconds": 8.0,
            "volume_db": -18.0
        })
        cues.append({
            "cue_id": "CUE-SUB-FINAL",
            "timestamp_seconds": 86.5,
            "type": "IMPACT",
            "asset": "sub_bass_drop_fade.wav",
            "duration_seconds": 3.5,
            "volume_db": -8.0
        })

        audio_plan = {
            "project_id": "astra_benchmark_90s",
            "total_duration_seconds": 90.0,
            "layers": layers,
            "cues": cues
        }

        with open(self.output_dir / "audio-plan.json", "w", encoding="utf-8") as f:
            json.dump(audio_plan, f, indent=2)

        # Synthesize real broadcast WAV assets
        self.synthesize_all_audio_cues(cues)

        return audio_plan

    def _write_wav(self, filename: str, samples: np.ndarray):
        path = self.output_dir / filename
        # Ensure stereo float32 converted to int16
        if samples.ndim == 1:
            samples = np.column_stack([samples, samples])
        # Soft limiter
        samples = np.clip(samples, -0.98, 0.98)
        int_data = (samples * 32767).astype(np.int16)
        wavfile.write(str(path), self.sample_rate, int_data)
        return path

    def synthesize_all_audio_cues(self, cues: List[Dict[str, Any]]):
        """
        Synthesizes authentic documentary sound assets:
        - Low HVAC room tone
        - Analog synth tension drones
        - Subtle rhythmic investigative tick
        - Sub-bass cinematic drops
        - Terminal alert buzzers and clean success chimes
        """
        sr = self.sample_rate

        # 1. room_tone_quiet_hvac.wav (90s)
        n_samples = int(90.0 * sr)
        # Pink noise filtered with 60Hz + 120Hz electrical hum
        t = np.linspace(0, 90.0, n_samples, endpoint=False)
        white = np.random.normal(0, 0.02, n_samples)
        # Simple IIR low pass filter approximation
        b_hum = 0.015 * np.sin(2 * np.pi * 60 * t) + 0.008 * np.sin(2 * np.pi * 120 * t)
        room_tone = np.convolve(white, np.ones(64)/64, mode='same') + b_hum
        self._write_wav("room_tone_quiet_hvac.wav", room_tone * 0.4)

        # 2. music_m03_tension.wav (15s)
        t15 = np.linspace(0, 15.0, int(15.0 * sr), endpoint=False)
        # Dual detuned low saw/sine at 55Hz and 55.4Hz
        drone1 = np.sin(2 * np.pi * 55.0 * t15)
        drone2 = 0.6 * np.sin(2 * np.pi * 110.0 * t15)
        drone3 = 0.4 * np.sin(2 * np.pi * 55.5 * t15)
        env = np.minimum(t15 / 1.5, 1.0) * np.minimum((15.0 - t15) / 2.0, 1.0)
        m03 = (drone1 + drone2 + drone3) * 0.22 * env
        self._write_wav("music_m03_tension.wav", m03)

        # 3. music_m02_investigation.wav (16s)
        t16 = np.linspace(0, 16.0, int(16.0 * sr), endpoint=False)
        pulse_bpm = 120.0
        beat_interval = 60.0 / pulse_bpm # 0.5s
        tick = np.zeros_like(t16)
        for b in np.arange(0, 16.0, beat_interval):
            idx = int(b * sr)
            if idx < len(t16):
                dt = np.linspace(0, 0.05, int(0.05 * sr), endpoint=False)
                burst = np.sin(2 * np.pi * 880 * dt) * np.exp(-dt * 60)
                end_idx = min(idx + len(burst), len(t16))
                tick[idx:end_idx] += burst[:end_idx - idx] * 0.15
        drone_sub = 0.18 * np.sin(2 * np.pi * 65.4 * t16)
        env16 = np.minimum(t16 / 1.0, 1.0) * np.minimum((16.0 - t16) / 1.5, 1.0)
        m02 = (drone_sub + tick) * env16
        self._write_wav("music_m02_investigation.wav", m02)

        # 4. sub_bass_drop_60hz.wav (2.5s)
        t25 = np.linspace(0, 2.5, int(2.5 * sr), endpoint=False)
        # Pitch drops exponentially from 85Hz to 28Hz
        freq_env = 85.0 * np.exp(-t25 * 1.8) + 28.0
        phase = 2 * np.pi * np.cumsum(freq_env) / sr
        amp_env = np.exp(-t25 * 1.2)
        sub_drop = 0.65 * np.sin(phase) * amp_env
        self._write_wav("sub_bass_drop_60hz.wav", sub_drop)

        # 5. music_m04_discovery.wav (15s)
        t_disc = np.linspace(0, 15.0, int(15.0 * sr), endpoint=False)
        chord1 = np.sin(2 * np.pi * 130.81 * t_disc) # C3
        chord2 = np.sin(2 * np.pi * 196.00 * t_disc) # G3
        chord3 = 0.5 * np.sin(2 * np.pi * 261.63 * t_disc) # C4
        chord4 = 0.3 * np.sin(2 * np.pi * 329.63 * t_disc) # E4
        env_disc = np.minimum(t_disc / 2.0, 1.0) * np.minimum((15.0 - t_disc) / 2.0, 1.0)
        m04 = (chord1 + chord2 + chord3 + chord4) * 0.15 * env_disc
        self._write_wav("music_m04_discovery.wav", m04)

        # 6. music_m05_escalation.wav (15s)
        t_esc = np.linspace(0, 15.0, int(15.0 * sr), endpoint=False)
        # Rising arpeggiator motif
        arpeg = np.sin(2 * np.pi * (80.0 + 5.0 * t_esc) * t_esc) * 0.2
        # Accelerating rhythmic pulse
        pulse = 0.1 * np.sin(2 * np.pi * 4.0 * t_esc) * np.sin(2 * np.pi * 440 * t_esc)
        env_esc = np.minimum(t_esc / 1.0, 1.0) * np.minimum((15.0 - t_esc) / 1.5, 1.0)
        m05 = (arpeg + pulse) * env_esc
        self._write_wav("music_m05_escalation.wav", m05)

        # 7. terminal_error_bell.wav (1.0s)
        t_err = np.linspace(0, 1.0, int(1.0 * sr), endpoint=False)
        # Dissonant minor second buzz
        buzz = (np.sin(2 * np.pi * 440 * t_err) + np.sin(2 * np.pi * 466.16 * t_err)) * 0.25
        err_env = np.exp(-t_err * 4.0)
        self._write_wav("terminal_error_bell.wav", buzz * err_env)

        # 8. pytest_success_chime.wav (2.0s)
        t_chime = np.linspace(0, 2.0, int(2.0 * sr), endpoint=False)
        chime1 = np.sin(2 * np.pi * 523.25 * t_chime) # C5
        chime2 = np.sin(2 * np.pi * 659.25 * t_chime) # E5
        chime3 = np.sin(2 * np.pi * 783.99 * t_chime) # G5
        chime_env = np.exp(-t_chime * 2.5)
        pytest_chime = (chime1 + chime2 + chime3) * 0.2 * chime_env
        self._write_wav("pytest_success_chime.wav", pytest_chime)

        # 9. music_m06_danger.wav (12s)
        t_dang = np.linspace(0, 12.0, int(12.0 * sr), endpoint=False)
        # Low menacing sawtooth with pulse
        f_base = 43.65 # F1
        dang_drone = np.sin(2 * np.pi * f_base * t_dang) + 0.5 * np.sin(2 * np.pi * (f_base * 2) * t_dang)
        dang_pulse = 0.3 * np.sin(2 * np.pi * 3.0 * t_dang)
        env_dang = np.minimum(t_dang / 1.0, 1.0) * np.minimum((12.0 - t_dang) / 1.5, 1.0)
        m06 = (dang_drone * (1.0 + dang_pulse)) * 0.22 * env_dang
        self._write_wav("music_m06_danger.wav", m06)

        # 10. music_m08_ending.wav (8s)
        t_end = np.linspace(0, 8.0, int(8.0 * sr), endpoint=False)
        end_pad = (np.sin(2 * np.pi * 98.0 * t_end) + np.sin(2 * np.pi * 146.83 * t_end) + np.sin(2 * np.pi * 220.0 * t_end)) * 0.16
        env_end = np.minimum(t_end / 1.5, 1.0) * ((8.0 - t_end) / 8.0)
        m08 = end_pad * env_end
        self._write_wav("music_m08_ending.wav", m08)

        # 11. sub_bass_drop_fade.wav (3.5s)
        t_fade = np.linspace(0, 3.5, int(3.5 * sr), endpoint=False)
        freq_fade = 70.0 * np.exp(-t_fade * 1.0) + 24.0
        phase_fade = 2 * np.pi * np.cumsum(freq_fade) / sr
        sub_fade = 0.55 * np.sin(phase_fade) * np.exp(-t_fade * 0.9)
        self._write_wav("sub_bass_drop_fade.wav", sub_fade)

if __name__ == "__main__":
    from agents.shot_director.shot_director import ShotDirector
    sd = ShotDirector()
    plan = sd.generate_90s_benchmark_shot_plan()
    snd = SoundDirector()
    res = snd.generate_90s_benchmark_audio_plan(plan["shots"])
    print(f"Sound Director generated audio plan and synthesized {len(res['cues'])} discrete cues across {len(res['layers'])} layers.")
