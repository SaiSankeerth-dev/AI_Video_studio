import json
from pathlib import Path

class PromptCompilerV1:
    """Compiles structured documentary shots into rich, photorealistic Gemini prompts."""

    def compile(self, shot_data):
        v = shot_data["visual"]
        c = shot_data["camera"]
        
        # 1. Gemini Image Generation Prompt
        image_prompt = (
            f"Photorealistic investigative documentary reenactment. "
            f"IMAGE PURPOSE: {shot_data.get('purpose', 'Visual evidence communication')}. "
            f"SUBJECT: {v['subject']}. "
            f"ACTION: {v['action']}. "
            f"ENVIRONMENT: {v['environment']} at {v['time']}. Context: {v['context']}. "
            f"COMPOSITION & SPATIAL HIERARCHY: {v['composition']}. Foreground: {v['foreground']}. Midground: {v['midground']}. Background: {v['background']}. "
            f"CAMERA: {c['shot_size']}, {c['camera_position']} at {c['camera_height']} height, {c['angle']} angle, shot on a {c['lens']} with {c['depth_of_field']}, {c['movement']} perspective. "
            f"LIGHTING: {v['lighting']}. "
            f"PHYSICAL MATERIALS: {v['materials']}. "
            f"ATMOSPHERE & COLOR: {v['atmosphere']}. Color Palette: {v['color_palette']}. "
            f"DOCUMENTARY AUTHENTICITY: Physically believable architectural scale, natural human proportions, realistic surface textures, no fantasy/cyberpunk elements. 16:9 cinematic aspect ratio, 8k resolution."
        )

        # 2. Strict Negative / Avoidance Prompt
        negative_prompt = (
            "text artifacts, illegible UI, distorted faces, extra fingers, duplicated people, malformed hands, "
            "warped architecture, impossible perspective, floating objects, excessive neon, fantasy elements, "
            "cartoon, anime, plastic CGI appearance, oversaturation, excessive bloom, artificial lens flare, "
            "random holograms, meaningless futuristic interfaces, watermark, logo, duplicate equipment, impossible reflections"
        )

        # 3. Image-To-Video Motion Prompt
        motion_prompt = (
            f"CAMERA MOVEMENT: {c['movement']}. "
            f"SUBJECT MOVEMENT: Subtle natural breathing and micro-movements, no morphing or fast displacement. "
            f"ENVIRONMENTAL MOVEMENT: Faint cooling airflow across cables, soft atmospheric drift in background. "
            f"LIGHT MOVEMENT: Asynchronous pulsing of status indicators, stable key illumination. "
            f"RESTRICTIONS: Preserve character facial structure, wardrobe, architectural geometry, and lighting color balance exactly. No sudden camera shake, no morphing objects, no additional characters entering frame."
        )

        shot_data["gemini_image_prompt"] = image_prompt
        shot_data["negative_prompt"] = negative_prompt
        shot_data["image_to_video_prompt"] = motion_prompt
        return shot_data
