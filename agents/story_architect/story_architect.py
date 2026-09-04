"""
Story Architect Agent (TASK 04)
Designs the narrative trajectory, mystery progression, emotional escalation,
and 10-beat dramatic structure for investigative documentaries.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class StoryArchitect:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(r"D:\gitM\01_ContentFactory\production\scripts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_story_architecture(
        self,
        topic: str = "GPT-6 Astra: The AI That Can Take Over Your Computer",
        central_question: str = "What changes when AI stops merely generating answers and starts operating the digital world itself?",
        runtime_mode: str = "benchmark_90s" # or "full_documentary"
    ) -> Dict[str, Any]:
        """
        Synthesizes the Fern-style documentary dramatic structure:
        WOW -> HOW? -> PROOF -> SCALE -> DANGER -> CONSEQUENCE
        """
        if runtime_mode == "benchmark_90s":
            beats = [
                {
                    "beat_id": "BEAT-01",
                    "beat_name": "THE COLD HOOK",
                    "dramatic_purpose": "Disorient the viewer with an uncanny event: an autonomous cursor moving at 2:13 AM with hands off the keyboard.",
                    "target_seconds": 15.0,
                    "emotional_state": "TENSE",
                    "revealed_mystery": "Computers have waited for humans for decades. Now the computer is listening to an AI instead."
                },
                {
                    "beat_id": "BEAT-02",
                    "beat_name": "ACTIVE DESKTOP TAKEOVER",
                    "dramatic_purpose": "Demonstrate the capability physically on screen: browser opening, navigation, terminal, multi-app montage.",
                    "target_seconds": 16.0,
                    "emotional_state": "INTRIGUED",
                    "revealed_mystery": "Astra doesn't just generate text; it navigates the digital environment directly."
                },
                {
                    "beat_id": "BEAT-03",
                    "beat_name": "THE PARADIGM BLACKOUT",
                    "dramatic_purpose": "Hard cut to black with thesis typography: THE COMPUTER IS NO LONGER THE TOOL. IT'S THE ENVIRONMENT.",
                    "target_seconds": 9.0,
                    "emotional_state": "REFLECTIVE",
                    "revealed_mystery": "Software shifts from being an instrument for human hands to an ecosystem for autonomous agents."
                },
                {
                    "beat_id": "BEAT-04",
                    "beat_name": "HARD EMPIRICAL EVIDENCE",
                    "dramatic_purpose": "Zoom into official documentation and OSWorld 2.0 benchmark results (72.6% vs 65.7%).",
                    "target_seconds": 15.0,
                    "emotional_state": "CURIOUS",
                    "revealed_mystery": "Verified numbers confirm a 6.9% leap over previous state-of-the-art across live operating systems."
                },
                {
                    "beat_id": "BEAT-05",
                    "beat_name": "THE MINI-STORY FAILURE & RECOVERY",
                    "dramatic_purpose": "Show real developer workflow: command execution, test failure, error inspection, patch adaptation, success.",
                    "target_seconds": 15.0,
                    "emotional_state": "TENSE",
                    "revealed_mystery": "The breakthrough is not flawless execution—it is closed-loop self-correction."
                },
                {
                    "beat_id": "BEAT-06",
                    "beat_name": "THE CYBERSECURITY ESCALATION",
                    "dramatic_purpose": "Expose OpenAI's Safety Overview marking Astra as reaching the Critical Cybersecurity threshold.",
                    "target_seconds": 12.0,
                    "emotional_state": "CONCERNED",
                    "revealed_mystery": "The same agentic agency that debugs software can autonomously exploit systems."
                },
                {
                    "beat_id": "BEAT-07",
                    "beat_name": "THE UNCOMFORTABLE QUESTION",
                    "dramatic_purpose": "Final blackout beat: When the machine can operate the machine, who is actually in control?",
                    "target_seconds": 8.0,
                    "emotional_state": "URGENT",
                    "revealed_mystery": "The boundary between human labor and autonomous infrastructure has permanently shifted."
                }
            ]
            target_runtime = 90.0
        else:
            # Full 10-beat dramatic structure
            beats = [
                {"beat_id": "BEAT-01", "beat_name": "HOOK", "dramatic_purpose": "The autonomous cursor moves at 2:13 AM without human touch.", "target_seconds": 45.0, "emotional_state": "TENSE", "revealed_mystery": "The computer acts on its own."},
                {"beat_id": "BEAT-02", "beat_name": "THE OLD AI", "dramatic_purpose": "Contrast chat prompts with execution.", "target_seconds": 80.0, "emotional_state": "CURIOUS", "revealed_mystery": "Chatbots were passive advisors."},
                {"beat_id": "BEAT-03", "beat_name": "THE COMPUTER", "dramatic_purpose": "Software interfaces as human environments.", "target_seconds": 100.0, "emotional_state": "INTRIGUED", "revealed_mystery": "Operating systems were designed for human perception."},
                {"beat_id": "BEAT-04", "beat_name": "ASTRA TAKES CONTROL", "dramatic_purpose": "Detailed screen reconstruction of agent action.", "target_seconds": 120.0, "emotional_state": "EXCITED", "revealed_mystery": "Pixels and keystrokes replace APIs."},
                {"beat_id": "BEAT-05", "beat_name": "WHAT IT CAN ACTUALLY DO", "dramatic_purpose": "Multi-app cross-application workflow.", "target_seconds": 140.0, "emotional_state": "IMPRESSED", "revealed_mystery": "Jira, Docker, IDE, terminal synthesis."},
                {"beat_id": "BEAT-06", "beat_name": "HOW MUCH BETTER IS IT?", "dramatic_purpose": "OSWorld 2.0 & AutomationBench hard evidence.", "target_seconds": 120.0, "emotional_state": "SKEPTICAL", "revealed_mystery": "72.6% vs 65.7% confirmed metrics."},
                {"beat_id": "BEAT-07", "beat_name": "WHERE IT FAILS", "dramatic_purpose": "Cascading loops, modal dialog freeze, unhandled exceptions.", "target_seconds": 110.0, "emotional_state": "CONCERNED", "revealed_mystery": "Reliability collapses in chaotic edge cases."},
                {"beat_id": "BEAT-08", "beat_name": "CYBERSECURITY", "dramatic_purpose": "OpenAI Safety Overview Critical Threshold.", "target_seconds": 95.0, "emotional_state": "TENSE", "revealed_mystery": "Autonomous exploit synthesis and defense triage."},
                {"beat_id": "BEAT-09", "beat_name": "WHAT HAPPENS WHEN IT IS TOO CAPABLE?", "dramatic_purpose": "The economics of labor and supervision.", "target_seconds": 75.0, "emotional_state": "REFLECTIVE", "revealed_mystery": "If humans must audit every click, the dividend vanishes."},
                {"beat_id": "BEAT-10", "beat_name": "THE FUTURE OF COMPUTER WORK", "dramatic_purpose": "Closing philosophical resolution and question.", "target_seconds": 75.0, "emotional_state": "URGENT", "revealed_mystery": "The interface is no longer between human and software—it is between software and software."}
            ]
            target_runtime = sum(b["target_seconds"] for b in beats)

        story_manifest = {
            "topic": topic,
            "weak_angle": "How GPT-6 Astra's new features work.",
            "strong_angle": "The moment AI stopped waiting for humans to click the buttons and started operating the computer itself.",
            "central_question": central_question,
            "stakes": "If models can reliably navigate live software environments, the foundation of knowledge work and cybersecurity fundamentally changes.",
            "promise": "By the end of this documentary, the viewer will see exactly what Astra can do, where it breaks, and what its autonomous agency means for the future.",
            "runtime_mode": runtime_mode,
            "target_runtime_seconds": target_runtime,
            "narrative_arc": ["WOW", "HOW?", "PROOF", "SCALE", "DANGER", "CONSEQUENCE"],
            "beats": beats
        }

        with open(self.output_dir / "story.json", "w", encoding="utf-8") as f:
            json.dump(story_manifest, f, indent=2)

        return story_manifest

if __name__ == "__main__":
    sa = StoryArchitect()
    story = sa.build_story_architecture()
    print(f"Story created: {len(story['beats'])} beats, {story['target_runtime_seconds']}s target runtime.")
