"""
Prompt Director Agent (TASK 11)
Transforms Shot Director specifications into structured cinematic prompts for Gemini.
Adheres to the 9-block Visual Bible structure and enforces anti-AI-slop rules.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class PromptDirector:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(r"D:\gitM\01_ContentFactory\production\shots")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def compile_cinematic_prompt(self, shot: Dict[str, Any]) -> str:
        """
        Compiles structured prompt containing:
        SUBJECT, ARCHITECTURE, CAMERA, COMPOSITION, LIGHTING,
        MATERIAL, ATMOSPHERE, REALISM, and DO NOT blocks.
        """
        subject = shot.get("subject", "workstation")
        actions = ", ".join(shot.get("action", []))
        camera_mov = shot.get("camera", {}).get("movement", "slow_push")
        framing = shot.get("camera", {}).get("framing", "MEDIUM_SUBJECT")

        prompt = (
            f"[DOCUMENTARY CINEMATOGRAPHY SPECIFICATION]\n"
            f"SUBJECT: {subject}. Physical occurrence: {actions}.\n"
            f"ARCHITECTURE: Authentic high-tech research facility or engineer desk environment, clean cable management, functional design, no sci-fi tropes.\n"
            f"CAMERA: {framing}, Arri Alexa 65 aesthetic, Zeiss Master Prime lens, subtle {camera_mov}, f/2.8 shallow depth of field.\n"
            f"COMPOSITION: Cinematic rule of thirds, intentional negative space on right third for documentary graphics, strong foreground-background separation.\n"
            f"LIGHTING: Low-key naturalistic illumination, 2:13 AM practical desk lamp (3200K) contrasting against cold clinical monitor screen glow (6500K), deep rich shadows.\n"
            f"MATERIAL: Matte black anodized aluminum monitor chassis, PBT mechanical keycaps, micro-dust on dark desk glass, authentic screen subpixel texture.\n"
            f"ATMOSPHERE: Quiet investigative tension, late-night exhaustion, tangible reality, subtle atmospheric haze, natural 35mm film grain.\n"
            f"REALISM: Photorealistic documentary frame, authentic unedited shutter timing (1/48s motion blur), zero artificial smoothing.\n"
            f"DO NOT: floating neon blue holograms, glowing cyber spheres, abstract robot hands, generic stock photo smiles, deformed fingers, low-res artifacts, plastic AI skin."
        )
        return prompt

    def generate_all_prompts(self, shots: List[Dict[str, Any]]) -> Dict[str, str]:
        prompts = {}
        for s in shots:
            sid = s["shot_id"]
            prompts[sid] = self.compile_cinematic_prompt(s)
        return prompts

if __name__ == "__main__":
    from agents.shot_director.shot_director import ShotDirector
    sd = ShotDirector()
    plan = sd.generate_90s_benchmark_shot_plan()
    pd = PromptDirector()
    prompts = pd.generate_all_prompts(plan["shots"])
    print(f"Generated {len(prompts)} 9-block documentary prompts. First sample:\n\n{prompts['SH-01']}")
