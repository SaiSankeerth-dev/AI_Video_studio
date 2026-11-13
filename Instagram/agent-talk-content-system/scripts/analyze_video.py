"""
Agent Talk — Video Analysis & Inspection Engine
Utilizes ffprobe, PySceneDetect, and faster-whisper to inspect raw & final videos.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from scenedetect import detect, ContentDetector

def get_ffprobe_metadata(video_path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:stream=codec_type,codec_name,width,height,r_frame_rate,bit_rate,sample_rate,channels",
        "-of", "json",
        str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    probe = json.loads(result.stdout)
    
    video_stream = next((s for s in probe.get("streams", []) if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in probe.get("streams", []) if s.get("codec_type") == "audio"), {})
    fmt = probe.get("format", {})
    
    # parse frame rate
    r_fps = video_stream.get("r_frame_rate", "30/1")
    if "/" in r_fps:
        num, den = r_fps.split("/")
        fps = round(float(num) / float(den), 2)
    else:
        fps = float(r_fps)
        
    duration = float(fmt.get("duration", video_stream.get("duration", 0)))
    
    return {
        "file_size_bytes": int(fmt.get("size", 0)),
        "file_size_mb": round(int(fmt.get("size", 0)) / (1024 * 1024), 2),
        "duration_sec": round(duration, 2),
        "video": {
            "codec": video_stream.get("codec_name"),
            "width": int(video_stream.get("width", 0)),
            "height": int(video_stream.get("height", 0)),
            "aspect_ratio": f"{video_stream.get('width')}:{video_stream.get('height')}",
            "fps": fps,
            "bitrate_kbps": round(int(video_stream.get("bit_rate", 0)) / 1000, 1) if video_stream.get("bit_rate") else None
        },
        "audio": {
            "codec": audio_stream.get("codec_name"),
            "sample_rate_hz": int(audio_stream.get("sample_rate", 0)) if audio_stream.get("sample_rate") else None,
            "channels": int(audio_stream.get("channels", 0)) if audio_stream.get("channels") else None,
            "bitrate_kbps": round(int(audio_stream.get("bit_rate", 0)) / 1000, 1) if audio_stream.get("bit_rate") else None
        }
    }

def detect_scenes(video_path: str, threshold: float = 27.0) -> list:
    scene_list = detect(str(video_path), ContentDetector(threshold=threshold))
    scenes = []
    for i, scene in enumerate(scene_list):
        start = round(scene[0].get_seconds(), 2)
        end = round(scene[1].get_seconds(), 2)
        scenes.append({
            "scene_index": i + 1,
            "start_sec": start,
            "end_sec": end,
            "duration_sec": round(end - start, 2)
        })
    return scenes

def extract_representative_frames(video_path: str, scenes: list, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    frame_indices = [
        ("01_opening_hook", 1.0),
        ("02_tension_build", min(15.0, scenes[-1]["end_sec"] * 0.25)),
        ("03_midpoint_reveal", scenes[-1]["end_sec"] * 0.5),
        ("04_climax", scenes[-1]["end_sec"] * 0.85),
        ("05_ending_punchline", scenes[-1]["end_sec"] - 1.5)
    ]
    extracted = []
    for label, timestamp in frame_indices:
        target_file = out_dir / f"{label}.jpg"
        cmd = [
            "ffmpeg", "-y", "-ss", str(timestamp),
            "-i", str(video_path),
            "-vframes", "1", "-q:v", "2",
            str(target_file)
        ]
        subprocess.run(cmd, capture_output=True, check=False)
        if target_file.exists():
            extracted.append({"label": label, "timestamp": timestamp, "path": str(target_file)})
    return extracted

def transcribe_or_load_script(video_path: str, srt_path: Path = None) -> list:
    if srt_path and srt_path.exists():
        entries = []
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
        import re
        blocks = re.split(r'\n\s*\n', content.strip())
        for b in blocks:
            lines = b.strip().split("\n")
            if len(lines) >= 3:
                idx = lines[0]
                timing = lines[1]
                text = " ".join(lines[2:])
                entries.append({"index": idx, "timing": timing, "text": text})
        return entries
    
    # fallback to faster_whisper
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(video_path), beam_size=5)
    entries = []
    for i, seg in enumerate(segments):
        entries.append({
            "index": i + 1,
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip()
        })
    return entries

def main():
    parser = argparse.ArgumentParser(description="Agent Talk Video Analysis Engine")
    parser.add_argument("--video", required=True, help="Path to target MP4 video")
    parser.add_argument("--slug", required=True, help="Slug/Name for output report")
    parser.add_argument("--srt", default=None, help="Optional path to existing subtitles SRT")
    parser.add_argument("--output-base", default="E:/AI_Videos/Instagram/agent-talk-content-system", help="Base directory")
    args = parser.parse_args()

    video_path = Path(args.video).resolve()
    base_dir = Path(args.output_base).resolve()
    slug = args.slug

    print(f"[*] Analyzing video: {video_path}")
    meta = get_ffprobe_metadata(str(video_path))
    print(f"  - Duration: {meta['duration_sec']}s | Resolution: {meta['video']['width']}x{meta['video']['height']} | FPS: {meta['video']['fps']}")

    print("[*] Running Scene Detection with PySceneDetect...")
    scenes = detect_scenes(str(video_path))
    scene_count = len(scenes)
    avg_duration = round(meta['duration_sec'] / scene_count, 2) if scene_count > 0 else 0
    cpm = round((scene_count / meta['duration_sec']) * 60, 1) if meta['duration_sec'] > 0 else 0
    print(f"  - Detected {scene_count} scenes. Average shot: {avg_duration}s. Cuts Per Minute (CPM): {cpm}")

    frames_dir = base_dir / "analysis" / "video-analysis" / f"{slug}_frames"
    print(f"[*] Extracting keyframes to {frames_dir}...")
    frames = extract_representative_frames(str(video_path), scenes, frames_dir)

    srt_file = Path(args.srt) if args.srt else None
    print("[*] Extracting audio transcript...")
    transcript = transcribe_or_load_script(str(video_path), srt_file)
    print(f"  - Extracted {len(transcript)} dialogue / caption cues.")

    # Save JSON metadata
    analysis_data = {
        "slug": slug,
        "video_path": str(video_path),
        "metadata": meta,
        "editing": {
            "total_shots": scene_count,
            "average_shot_duration_sec": avg_duration,
            "cuts_per_minute": cpm,
            "scenes": scenes
        },
        "frames": frames,
        "transcript": transcript
    }

    json_path = base_dir / "analysis" / "video-analysis" / f"{slug}-metadata.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(analysis_data, f, indent=2)
    print(f"[✓] Metadata JSON exported to: {json_path}")

    # Build Markdown Report
    md_path = base_dir / "analysis" / "video-analysis" / f"{slug}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Video Analysis Report — {slug}\n\n")
        f.write("## 1. Technical Video Inspection\n\n")
        f.write(f"- **Video Path:** `{video_path}`\n")
        f.write(f"- **Resolution:** {meta['video']['width']} × {meta['video']['height']} ({'9:16 Vertical Reel' if meta['video']['width'] < meta['video']['height'] else 'Landscape'})\n")
        f.write(f"- **Duration:** {meta['duration_sec']} seconds ({int(meta['duration_sec'] // 60)}m {int(meta['duration_sec'] % 60)}s)\n")
        f.write(f"- **Frame Rate:** {meta['video']['fps']} fps\n")
        f.write(f"- **Video Codec:** {meta['video']['codec']} ({meta['video']['bitrate_kbps']} kbps)\n")
        f.write(f"- **Audio Codec:** {meta['audio']['codec']} ({meta['audio']['channels']} ch, {meta['audio']['sample_rate_hz']} Hz, {meta['audio']['bitrate_kbps']} kbps)\n")
        f.write(f"- **File Size:** {meta['file_size_mb']} MB\n\n")

        f.write("## 2. Editing & Cinematography Breakdown\n\n")
        f.write(f"- **Total Shot Count:** {scene_count} cuts\n")
        f.write(f"- **Average Shot Duration:** {avg_duration} seconds\n")
        f.write(f"- **Cuts Per Minute (CPM):** {cpm} CPM (High engagement short-form tempo)\n")
        f.write("- **Visual Dynamic:** Multi-shot dialogue between human developer (Tariq Vance) and AI mascot (Claude) with tight close-ups, wide establishing shots, and phone UI zoom-ins.\n\n")

        f.write("### Scene Cut Sequence\n\n")
        f.write("| Scene # | Time Range (s) | Duration (s) |\n|:---:|:---:|:---:|\n")
        for s in scenes:
            f.write(f"| {s['scene_index']} | {s['start_sec']}s – {s['end_sec']}s | {s['duration_sec']}s |\n")

        f.write("\n## 3. Audio & Spoken Dialogue Transcript\n\n")
        f.write("| Index | Timing / Range | Spoken Line |\n|:---:|:---:|:---|\n")
        for t in transcript:
            timing = t.get("timing") or f"{t.get('start', 0)}s – {t.get('end', 0)}s"
            f.write(f"| {t['index']} | `{timing}` | {t['text']} |\n")

        f.write("\n## 4. Keyframe Snapshots\n\n")
        for fr in frames:
            f.write(f"- **{fr['label']}** ({fr['timestamp']}s): `{fr['path']}`\n")

    print(f"[✓] Analysis Markdown exported to: {md_path}")

if __name__ == "__main__":
    main()
