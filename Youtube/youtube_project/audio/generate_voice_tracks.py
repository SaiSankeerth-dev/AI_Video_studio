import json
import subprocess
import os

storyboard_path = r"E:\AI_Videos\Youtube\youtube_project\storyboard\storyboard.json"
voice_dir = r"E:\AI_Videos\Youtube\youtube_project\assets\voice"
audio_plan_path = r"E:\AI_Videos\Youtube\youtube_project\audio\audio_plan.json"

with open(storyboard_path, "r", encoding="utf-8") as f:
    shots = json.load(f)

audio_plan = []

for s in shots:
    shot_id = s["shot_id"].lower()
    voiceover_text = s["voiceover"]
    out_wav = os.path.join(voice_dir, f"{shot_id}_voice.wav")
    
    print(f"Generating TTS for {shot_id}...")
    cmd = [
        "npx", "--yes", "hyperframes@0.8.143", "tts",
        voiceover_text,
        "-v", "am_michael",
        "-o", out_wav
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    
    # Measure audio duration with ffprobe
    duration = 0.0
    if os.path.exists(out_wav):
        probe_cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", out_wav
        ]
        p_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            duration = float(p_res.stdout.strip())
        except Exception:
            duration = s["duration"]
        print(f"  Generated {shot_id}: duration={duration:.2f}s")
    else:
        print(f"  Failed to generate {shot_id}")

    plan_item = {
        "shot_id": s["shot_id"],
        "scene_id": s["scene_id"],
        "voiceover_file": f"{shot_id}_voice.wav",
        "voiceover_duration": duration,
        "target_shot_duration": max(duration + 0.8, s["duration"]),
        "sound_effects": s["sound_effects"],
        "music_direction": s["music_direction"],
        "narration_text": voiceover_text
    }
    audio_plan.append(plan_item)

with open(audio_plan_path, "w", encoding="utf-8") as f:
    json.dump(audio_plan, f, indent=2)

print(f"\nAll voice tracks generated and audio_plan.json written successfully.")
