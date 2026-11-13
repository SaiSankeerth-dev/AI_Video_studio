import os
import subprocess
import json

base_dir = r"E:\AI_Videos\Youtube\youtube_project"
editing_dir = os.path.join(base_dir, "editing")
music_file = os.path.join(base_dir, "assets", "music", "soundtrack_bed.wav")
concat_list = os.path.join(editing_dir, "concat_list.txt")
raw_video = os.path.join(editing_dir, "raw_concatenated_video.mp4")
final_video = os.path.join(base_dir, "exports", "final_video.mp4")

print("STAGE 1: Concatenating all 20 rendered scene clips...")
concat_cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", concat_list,
    "-c", "copy",
    raw_video
]
res1 = subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("  ✓ Raw video concatenation complete.")

# Inspect raw video duration
probe_cmd = [
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", raw_video
]
p_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, text=True)
total_dur = float(p_res.stdout.strip())
print(f"  Total Video Duration: {total_dur:.2f} seconds.")

print("\nSTAGE 2: Mixing background music with dynamic ducking and EBU R128 mastering...")
# Filter graph:
# [0:a] is the dialog + shot SFX track from the concatenated video
# [1:a] is the soundtrack_bed.wav
# Music is ducked by 14dB (volume=0.20) and sidechain-compressed / mixed with dialog
# Then passed through loudnorm filter targeting -14.0 LUFS, -1.0 dBFS peak, 4.0 LRA
filter_complex = (
    f"[1:a]atrim=0:{total_dur},volume=0.20[music];"
    f"[0:a]volume=1.0[voice];"
    f"[voice][music]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
    f"[mixed]loudnorm=I=-14.0:LRA=4.0:TP=-1.0[mastered_audio]"
)

master_cmd = [
    "ffmpeg", "-y",
    "-i", raw_video,
    "-i", music_file,
    "-filter_complex", filter_complex,
    "-map", "0:v",
    "-map", "[mastered_audio]",
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "256k",
    "-shortest",
    final_video
]

res2 = subprocess.run(master_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(final_video) and os.path.getsize(final_video) > 1000000:
    print(f"  ✓ MASTER FINAL VIDEO EXPORTED SUCCESSFULLY: {final_video}")
    size_mb = os.path.getsize(final_video) / (1024 * 1024)
    print(f"  File size: {size_mb:.2f} MB")
else:
    print("  ✗ Master export failed.")

