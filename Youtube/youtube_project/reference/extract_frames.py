import os
import subprocess
import json

video_path = r"E:\AI_Videos\Youtube\youtube_project\reference\reference_video.mp4"
frames_dir = r"E:\AI_Videos\Youtube\youtube_project\reference\reference_frames"

# Key timestamps to sample across the 48-minute documentary
# timestamps in seconds:
# 10s: Opening hook
# 35s: Narrative setup
# 75s: 1996 retro Nintendo gameboy animation
# 135s: Logan Paul / Pikachu Illustrator $5M card 3D showcase
# 210s: Scott interview intro & motion graphics
# 360s: Takumi Akabane design prototype lore
# 480s: CGC grading slab 3D animation
# 600s: Playtest cards market emergence
# 900s: The forensic microscope inspection
# 1200s: Discord chat & forum investigation
# 1500s: Timeline graphic / motion map
# 1800s: Confrontation / evidence mounting
# 2100s: Forensic printing analysis (halftone dots / ink jet vs offset)
# 2400s: The $10,000,000 collapse / climax
# 2700s: Epilogue / conclusion

key_timestamps = [
    (10, "01_opening_hook"),
    (35, "02_title_intro"),
    (75, "03_retro_gameboy_aesthetic"),
    (135, "04_3d_card_render_slab"),
    (210, "05_talking_head_motion_backdrop"),
    (360, "06_archival_document_inspection"),
    (480, "07_cgc_grading_3d_case"),
    (600, "08_market_hype_kinetic_type"),
    (900, "09_forensic_microscope_zoom"),
    (1200, "10_digital_sleuthing_chat_ui"),
    (1500, "11_infographic_network_map"),
    (1800, "12_evidence_dossier_cutout"),
    (2100, "13_microprint_halftone_analysis"),
    (2400, "14_climax_scam_exposed"),
    (2700, "15_epilogue_moral_reflection")
]

for sec, label in key_timestamps:
    out_file = os.path.join(frames_dir, f"{label}_{sec}s.jpg")
    cmd = [
        "ffmpeg", "-y", "-ss", str(sec), "-i", video_path,
        "-vframes", "1", "-q:v", "2", out_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(out_file):
        print(f"Extracted: {label} ({sec}s)")
    else:
        print(f"Failed to extract {label}")

print("Frame extraction complete.")
