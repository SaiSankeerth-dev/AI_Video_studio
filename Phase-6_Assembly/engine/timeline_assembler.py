import json
import sys
from pathlib import Path

def assemble_timeline(project_dir=r"D:\gitM\01_ContentFactory\projects\video-001"):
    p_dir = Path(project_dir)
    cf_dir = p_dir.parents[1]
    synced_file = cf_dir / "Phase-4_Remotion" / "public" / "data" / "synced_sentences.json"
    
    with open(synced_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    video_clips = []
    voice_clips = []
    music_clips = [
        {
            "clip_id": "mus_01",
            "file": "audio/ambient-dark.wav",
            "start_frame": 0,
            "duration_frames": data["total_frames"],
            "volume": 0.045,
            "loop": True
        }
    ]
    sfx_clips = []
    graphics_clips = []
    captions_clips = []

    # Map each sentence to a visually diverse archetype
    archetype_map = {
        "s01": ("broll_motion", "video/fern_datacenter.mp4", "DATA_CENTER"),
        "s02": ("broll_motion", "video/fern_engineer.mp4", "HUMAN_OPERATOR"),
        "s03": ("motion_graphics", "components/ChatbotFriction", "INTERACTION_DIAGRAM"),
        "s04": ("broll_motion", "video/fern_silicon.mp4", "SILICON_HARDWARE"),
        "s05": ("motion_graphics", "components/TitleCard", "TITLE_TYPOGRAPHY"),
        "s06": ("broll_motion", "video/fern_silicon.mp4", "SILICON_HARDWARE"),
        "s07": ("motion_graphics", "components/ArchitectureDiagram", "BENTO_INFOGRAPHIC"),
        "s08": ("broll_motion", "video/fern_datacenter.mp4", "DATA_CENTER"),
        "s09": ("broll_motion", "video/fern_network.mp4", "GLOBAL_NETWORK"),
        "s10": ("motion_graphics", "components/AgentLoop", "STATE_MACHINE"),
        "s11": ("motion_graphics", "components/ToolExecution", "CODE_SANDBOX"),
        "s12": ("broll_motion", "video/fern_engineer.mp4", "HUMAN_OPERATOR"),
        "s13": ("motion_graphics", "components/CodeDiff", "CODE_DIFF"),
        "s14": ("motion_graphics", "components/ToolExecution", "ERROR_HEAL"),
        "s15": ("broll_motion", "video/fern_monolith.mp4", "DATA_CENTER"),
        "s16": ("motion_graphics", "components/CompanyMap", "SWARM_TREE"),
        "s17": ("broll_motion", "video/fern_network.mp4", "GLOBAL_NETWORK"),
        "s18": ("motion_graphics", "components/CompanyMap", "SWARM_DISPATCH"),
        "s19": ("motion_graphics", "components/SourceCard", "SECURITY_GATE"),
        "s20": ("broll_motion", "video/fern_monolith.mp4", "DATA_CENTER"),
        "s21": ("motion_graphics", "components/SourceCard", "SECURITY_GATE"),
        "s22": ("broll_motion", "video/fern_datacenter.mp4", "DATA_CENTER"),
        "s23": ("motion_graphics", "components/QuoteCard", "EPILOGUE_QUOTE_A"),
        "s24": ("motion_graphics", "components/QuoteCard", "EPILOGUE_QUOTE_B"),
    }

    for sent in data["sentences"]:
        sf = sent["startFrame"]
        df = sent["durationFrames"]
        sid = sent["id"]

        vtype, src_file, archetype = archetype_map.get(sid, ("broll_motion", "video/fern_datacenter.mp4", "DATA_CENTER"))

        video_clips.append({
            "clip_id": f"vid_{sid}",
            "type": vtype,
            "source_file": src_file,
            "start_frame": sf,
            "duration_frames": df,
            "visual_archetype": archetype
        })

        voice_clips.append({
            "clip_id": f"vox_{sid}",
            "file": sent["audio_file"],
            "start_frame": sf,
            "duration_frames": df,
            "text": sent["text"],
            "speaker": "Narrator (Andrew)"
        })

        if sent.get("sfx"):
            sfx_clips.append({
                "clip_id": f"sfx_{sid}",
                "file": f"audio/{sent['sfx']}.wav",
                "start_frame": sf,
                "duration_frames": 45,
                "volume": 0.35
            })

        captions_clips.append({
            "clip_id": f"cap_{sid}",
            "start_frame": sf,
            "duration_frames": df,
            "text": sent["text"],
            "style": "FernSubtitle"
        })

    timeline_ir = {
        "episode_id": "video-001",
        "title": "The AI Agents That Are Starting to Work Without Us",
        "fps": 30,
        "resolution": {"width": 1920, "height": 1080},
        "total_frames": data["total_frames"],
        "total_seconds": data["total_seconds"],
        "tracks": {
            "video": video_clips,
            "voiceover": voice_clips,
            "music": music_clips,
            "sfx": sfx_clips,
            "graphics": graphics_clips,
            "captions": captions_clips
        }
    }

    out_file = p_dir / "assembly" / "timeline.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(timeline_ir, f, indent=2)
    print(f"Montara Timeline IR re-assembled with 100% visual variety: {out_file}")
    return timeline_ir

if __name__ == "__main__":
    proj = sys.argv[1] if len(sys.argv) > 1 else r"D:\gitM\01_ContentFactory\projects\video-001"
    assemble_timeline(proj)
