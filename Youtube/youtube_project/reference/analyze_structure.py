import re
import json

vtt_path = r"E:\AI_Videos\Youtube\youtube_project\reference\reference_subtitles.en.vtt"

with open(vtt_path, 'r', encoding='utf-8') as f:
    content = f.read()

# YouTube auto-generated VTT often duplicates lines with rolling words.
# Let's extract blocks and aggregate unique text segments with timestamps
lines = content.split('\n')
entries = []
seen = set()

time_re = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})')
curr_time = None
curr_lines = []

for line in lines:
    m = time_re.search(line)
    if m:
        if curr_time and curr_lines:
            txt = " ".join(curr_lines)
            txt = re.sub(r'<[^>]+>', '', txt)
            txt = re.sub(r'&gt;&gt;', '', txt)
            txt = re.sub(r'\[music\]', '', txt, flags=re.I)
            txt = re.sub(r'\s+', ' ', txt).strip()
            if txt and len(txt) > 2:
                entries.append((curr_time, txt))
            curr_lines = []
        curr_time = m.group(1)
    elif line and not line.startswith("WEBVTT") and not line.startswith("Kind:") and not line.startswith("Language:"):
        curr_lines.append(line)

# Group into 30-second windows to see the documentary structure
windows = {}
for t, txt in entries:
    parts = t.split(':')
    seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    win_idx = int(seconds // 60) # 1-minute blocks
    if win_idx not in windows:
        windows[win_idx] = []
    # Avoid adjacent identical fragments
    if not windows[win_idx] or txt not in windows[win_idx][-1]:
        windows[win_idx].append(txt)

print(f"Total minutes covered: {len(windows)}")
# Print outline for first 10 minutes
for m in sorted(windows.keys())[:10]:
    minute_text = " ".join(windows[m])
    # deduplicate repetitive rolling words
    words = minute_text.split()
    dedup = []
    for w in words:
        if not dedup or w != dedup[-1]:
            dedup.append(w)
    clean_sample = " ".join(dedup[:60])
    print(f"\n[Minute {m:02d}:00] {clean_sample}...")

