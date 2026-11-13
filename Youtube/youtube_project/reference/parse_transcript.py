import re
import json

vtt_path = r"E:\AI_Videos\Youtube\youtube_project\reference\reference_subtitles.en.vtt"

with open(vtt_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

blocks = []
current_time = ""
current_text = []

time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})')

seen_lines = set()

for line in lines:
    line_clean = line.strip()
    match = time_pattern.search(line_clean)
    if match:
        if current_time and current_text:
            text_str = " ".join(current_text).strip()
            # clean html tags
            text_str = re.sub(r'<[^>]+>', '', text_str)
            if text_str and text_str not in seen_lines:
                seen_lines.add(text_str)
                blocks.append({"time": current_time, "text": text_str})
            current_text = []
        current_time = match.group(1)
    elif line_clean and not line_clean.startswith("WEBVTT") and not line_clean.startswith("Kind:") and not line_clean.startswith("Language:"):
        # filter formatting artifacts
        cleaned = re.sub(r'<[^>]+>', '', line_clean).strip()
        if cleaned:
            current_text.append(cleaned)

if current_time and current_text:
    text_str = " ".join(current_text).strip()
    text_str = re.sub(r'<[^>]+>', '', text_str)
    if text_str:
        blocks.append({"time": current_time, "text": text_str})

# Print first 20 blocks and total blocks
print(f"Total parsed caption events: {len(blocks)}")
sample = blocks[:15]
for b in sample:
    print(f"[{b['time']}] {b['text']}")

# Also save condensed timeline to a text file for deep narrative analysis
with open(r"E:\AI_Videos\Youtube\youtube_project\reference\reference_transcript_clean.txt", "w", encoding="utf-8") as out:
    for b in blocks:
        out.write(f"[{b['time']}] {b['text']}\n")

