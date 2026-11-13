import json
import os
import subprocess

base_dir = r"E:\AI_Videos\Youtube\youtube_project"
images_dir = os.path.join(base_dir, "assets", "images")
voice_dir = os.path.join(base_dir, "assets", "voice")
sfx_dir = os.path.join(base_dir, "assets", "sfx")
music_file = os.path.join(base_dir, "assets", "music", "soundtrack_bed.wav")
videos_dir = os.path.join(base_dir, "assets", "videos")
editing_dir = os.path.join(base_dir, "editing")
exports_dir = os.path.join(base_dir, "exports")

os.makedirs(videos_dir, exist_ok=True)
os.makedirs(exports_dir, exist_ok=True)

# Load audio plan
with open(os.path.join(base_dir, "audio", "audio_plan.json"), "r", encoding="utf-8") as f:
    audio_plan = json.load(f)

# SFX mapping per shot
sfx_map = {
    "SHOT-01": "sfx_sub_boom.wav",
    "SHOT-03": "sfx_shutter_click.wav",
    "SHOT-04": "sfx_scanner_chirp.wav",
    "SHOT-05": "sfx_scanner_chirp.wav",
    "SHOT-06": "sfx_paper_slide.wav",
    "SHOT-07": "sfx_cash_chime.wav",
    "SHOT-09": "sfx_cash_chime.wav",
    "SHOT-10": "sfx_knife_slice.wav",
    "SHOT-11": "sfx_scanner_chirp.wav",
    "SHOT-12": "sfx_scanner_chirp.wav",
    "SHOT-14": "sfx_knife_slice.wav",
    "SHOT-15": "sfx_paper_slide.wav",
    "SHOT-16": "sfx_sub_boom.wav",
    "SHOT-17": "sfx_sub_boom.wav",
    "SHOT-18": "sfx_scanner_chirp.wav",
    "SHOT-20": "sfx_sub_boom.wav"
}

# Camera movement configs per shot (zoompan parameters)
# z: zoom expression, x: x-offset, y: y-offset
motion_configs = {
    # Shot 01: Slow forward push-in into center (1.0 -> 1.12)
    "SHOT-01": "zoompan=z='min(zoom+0.0003,1.12)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 02: Slow pan down-right
    "SHOT-02": "zoompan=z='1.05':d=TOTAL_FRAMES:x='if(lte(on,1),(iw-iw/zoom)/2,x+0.5)':y='if(lte(on,1),(ih-ih/zoom)/2,y+0.3)':s=1920x1080:fps=30",
    # Shot 03: Rapid push-in (1.0 -> 1.15)
    "SHOT-03": "zoompan=z='min(zoom+0.0005,1.15)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 04: Slow pan left-to-right
    "SHOT-04": "zoompan=z='1.08':d=TOTAL_FRAMES:x='min(x+0.6,iw-iw/zoom)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 05: Push-in on seller info box (1.0 -> 1.14)
    "SHOT-05": "zoompan=z='min(zoom+0.0003,1.14)':d=TOTAL_FRAMES:x='(iw/2-(iw/zoom/2))+120':y='(ih/2-(ih/zoom/2))+50':s=1920x1080:fps=30",
    # Shot 06: Slow lateral pan across split documents
    "SHOT-06": "zoompan=z='1.06':d=TOTAL_FRAMES:x='min(x+0.5,iw-iw/zoom)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 07: Tilt up graph (moving y from bottom to top)
    "SHOT-07": "zoompan=z='1.08':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='max(0,ih-ih/zoom-on*0.6)':s=1920x1080:fps=30",
    # Shot 08: Pull back (1.12 -> 1.0)
    "SHOT-08": "zoompan=z='max(1.12-on*0.0003,1.0)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 09: Ascending diagonal track
    "SHOT-09": "zoompan=z='1.08':d=TOTAL_FRAMES:x='min(x+0.7,iw-iw/zoom)':y='max(0,y-0.4)':s=1920x1080:fps=30",
    # Shot 10: Macro crawl toward blade tip
    "SHOT-10": "zoompan=z='min(zoom+0.0004,1.16)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 11: Vertical microscope scan (top to bottom)
    "SHOT-11": "zoompan=z='1.08':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='min(ih-ih/zoom,y+0.5)':s=1920x1080:fps=30",
    # Shot 12: Horizontal loupe pan
    "SHOT-12": "zoompan=z='1.06':d=TOTAL_FRAMES:x='min(x+0.6,iw-iw/zoom)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 13: Aerial forward push over Chicago
    "SHOT-13": "zoompan=z='min(zoom+0.0004,1.12)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 14: Macro push-in on blade cutting tape
    "SHOT-14": "zoompan=z='min(zoom+0.0005,1.15)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 15: Macro zoom into puffy curved lid
    "SHOT-15": "zoompan=z='min(zoom+0.0004,1.14)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='(ih/2-(ih/zoom/2))-60':s=1920x1080:fps=30",
    # Shot 16: Top-down rapid dive into open box
    "SHOT-16": "zoompan=z='min(zoom+0.0006,1.18)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 17: Slow orbit push around G.I. Joe pack
    "SHOT-17": "zoompan=z='min(zoom+0.0003,1.10)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 18: Slow push-in on scale readout
    "SHOT-18": "zoompan=z='min(zoom+0.0004,1.12)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='(ih/2-(ih/zoom/2))+100':s=1920x1080:fps=30",
    # Shot 19: Backward drift
    "SHOT-19": "zoompan=z='max(1.10-on*0.0003,1.0)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30",
    # Shot 20: Stardust cosmic pull-back (1.15 -> 1.0)
    "SHOT-20": "zoompan=z='max(1.15-on*0.00025,1.0)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
}

rendered_clips = []
timeline = []
current_time = 0.0

for item in audio_plan:
    shot_id = item["shot_id"]
    sid_lower = shot_id.lower()
    voice_file = os.path.join(voice_dir, item["voiceover_file"])
    image_file = os.path.join(images_dir, f"{sid_lower}.png")
    out_clip = os.path.join(videos_dir, f"{sid_lower}.mp4")
    
    duration = item["voiceover_duration"]
    total_frames = int(duration * 30) + 15 # add 0.5s breathing room
    clip_dur = total_frames / 30.0
    
    # Motion filter string
    motion_expr = motion_configs.get(shot_id, "zoompan=z='min(zoom+0.0003,1.10)':d=TOTAL_FRAMES:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30")
    motion_filter = motion_expr.replace("TOTAL_FRAMES", str(total_frames))
    
    # Check if we have an SFX for this shot
    sfx_name = sfx_map.get(shot_id)
    sfx_file = os.path.join(sfx_dir, sfx_name) if sfx_name else None
    
    print(f"Rendering {shot_id} ({clip_dur:.2f}s)...")
    
    # Build FFmpeg command with complex audio mixing (voice + optional SFX)
    if sfx_file and os.path.exists(sfx_file):
        filter_complex = (
            f"[0:v]scale=1920:1080,{motion_filter},format=yuv420p[v];"
            f"[1:a]volume=1.0[voice];"
            f"[2:a]volume=0.35[sfx];"
            f"[voice][sfx]amix=inputs=2:duration=first:dropout_transition=2[aout]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", image_file,
            "-i", voice_file,
            "-i", sfx_file,
            "-filter_complex", filter_complex,
            "-map", "[v]", "-map", "[aout]",
            "-t", str(clip_dur),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k",
            out_clip
        ]
    else:
        filter_complex = f"[0:v]scale=1920:1080,{motion_filter},format=yuv420p[v]"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", image_file,
            "-i", voice_file,
            "-filter_complex", filter_complex,
            "-map", "[v]", "-map", "1:a",
            "-t", str(clip_dur),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k",
            out_clip
        ]
        
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(out_clip):
        print(f"  ✓ Rendered {shot_id}")
        rendered_clips.append(out_clip)
        timeline.append({
            "shot_id": shot_id,
            "scene_id": item["scene_id"],
            "start_time": current_time,
            "end_time": current_time + clip_dur,
            "duration": clip_dur,
            "clip_file": f"{sid_lower}.mp4",
            "sfx": sfx_name,
            "voice_file": item["voiceover_file"]
        })
        current_time += clip_dur
    else:
        print(f"  ✗ Failed to render {shot_id}")

# Write timeline.json
with open(os.path.join(editing_dir, "timeline.json"), "w", encoding="utf-8") as f:
    json.dump({
        "project": "The $3,500,000 Cardboard Box",
        "total_duration": current_time,
        "clip_count": len(rendered_clips),
        "timeline": timeline
    }, f, indent=2)

print(f"\nAll {len(rendered_clips)} clips rendered. Total documentary runtime: {current_time:.2f} seconds.")

# Create concat list for FFmpeg
concat_list_path = os.path.join(editing_dir, "concat_list.txt")
with open(concat_list_path, "w", encoding="utf-8") as f:
    for clip in rendered_clips:
        # Use forward slashes
        clean_path = clip.replace("\\", "/")
        f.write(f"file '{clean_path}'\n")

print(f"Wrote concat list to {concat_list_path}")
