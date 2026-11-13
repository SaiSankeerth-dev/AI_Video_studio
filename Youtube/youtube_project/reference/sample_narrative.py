import json

transcript_path = r"E:\AI_Videos\Youtube\youtube_project\reference\reference_transcript_clean.txt"
with open(transcript_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Sample key minutes from 10 to 48
print("=== NARRATIVE TURNING POINTS ===")
target_minutes = [10, 15, 20, 25, 30, 35, 40, 45, 47]
for target in target_minutes:
    prefix = f"[00:{target:02d}:"
    matching = [l for l in lines if l.startswith(prefix)]
    if matching:
        print(f"\n--- Minute {target} ---")
        for m in matching[:5]:
            print(m.strip())
