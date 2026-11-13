import json

image_prompts = []
video_prompts = []

# Load shots
with open(r"E:\AI_Videos\Youtube\youtube_project\storyboard\storyboard.json", "r", encoding="utf-8") as f:
    shots = json.load(f)

for s in shots:
    img_entry = {
        "shot_id": s["shot_id"],
        "scene_id": s["scene_id"],
        "target_filename": f"{s['shot_id'].lower()}.png",
        "main_subject": s["visual_description"].split(".")[0],
        "environment": s["environment"],
        "composition": s["composition"],
        "camera_angle": s["camera_angle"],
        "lens": s["lens"],
        "lighting": s["lighting"],
        "colour_palette": "Deep void charcoal (#0F1115), aged parchment off-white (#F5EFEB), warning amber (#FF9F1C), and forensic cyan (#00E5FF)",
        "mood": "Investigative, tense, forensic, cinematic",
        "style": "Photorealistic documentary cinema, high skeuomorphic paper and physical texture",
        "aspect_ratio": "16:9",
        "quality_requirements": "Ultra-sharp 8k UHD render, physically based rendering (PBR) textures, fine cardboard fibers, realistic light scatter, cinematic depth of field",
        "negative_prompt": "cartoon, 3d render plastic sheen, deformed hands, illegible blurry text, low resolution, blown-out highlights, oversaturated colors",
        "full_prompt": s["image_prompt"]
    }
    image_prompts.append(img_entry)

    vid_entry = {
        "shot_id": s["shot_id"],
        "scene_id": s["scene_id"],
        "target_video_filename": f"{s['shot_id'].lower()}_clip.mp4",
        "starting_frame": f"{s['shot_id'].lower()}.png",
        "ending_frame": f"{s['shot_id'].lower()}_end.png",
        "subject_movement": s["subject_movement"],
        "camera_movement": s["camera_movement"],
        "environmental_movement": "Subtle drifting volumetric dust particles and slow atmospheric light shift",
        "lighting_changes": "Gentle specular reflection sweep across primary surfaces matching camera orbit",
        "animation_style": "Smooth cinematic motion with optical motion blur and natural physics easing",
        "motion_intensity": "Subtle to moderate (3/10) to preserve documentary elegance and legibility",
        "duration_seconds": s["duration"],
        "frame_rate": 30,
        "aspect_ratio": "16:9",
        "continuity_instructions": f"Match color grading and lighting direction of previous shot in {s['scene_id']}",
        "full_prompt": s["video_prompt"]
    }
    video_prompts.append(vid_entry)

with open(r"E:\AI_Videos\Youtube\youtube_project\prompts\image_prompts.json", "w", encoding="utf-8") as f:
    json.dump(image_prompts, f, indent=2)

with open(r"E:\AI_Videos\Youtube\youtube_project\prompts\video_prompts.json", "w", encoding="utf-8") as f:
    json.dump(video_prompts, f, indent=2)

print("Generated image_prompts.json and video_prompts.json successfully.")
