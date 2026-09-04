import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class GeminiDirectorClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not found. Please add your Google AI Studio API key to D:\\gitM\\01_ContentFactory\\.env"
            )
        self.client = genai.Client(api_key=self.api_key)

    def generate_shot_plan(self, narration_text: str, visual_context: str):
        prompt = f"""You are the ContentFactory Cinematic Visual Director v1.0.
Convert this narration into a strict documentary shot specification:

Narration: "{narration_text}"
Context: "{visual_context}"

Return JSON matching Section 28 of the Cinematic Prompt Director v1.0 Specification.
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    def evaluate_image(self, image_bytes, narration_text: str, shot_spec: dict):
        """Image Critic evaluating across the 10-factor quality rubric."""
        prompt = f"""You are the ContentFactory 10-Factor Image Critic.
Evaluate this image against the narration: "{narration_text}".
Return strict JSON with scores (1-10) for photorealism, cinematography, composition, lighting, materials, architecture, human_realism, depth, color_grading, and overall.
Decision must be APPROVE, REFINE, or REGENERATE.
"""
        # Multi-modal evaluation call
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt]
        )
        return response.text
