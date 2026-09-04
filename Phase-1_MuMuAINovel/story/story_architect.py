"""
Story Architect Engine (Phase 1)
Builds documentaries around a compelling narrative question and structured dramatic architecture,
NOT a dry topic or generic prompt.
Follows Section 1 & Section 3 specifications:
Architecture: HOOK -> QUESTION -> CONTEXT -> FIRST REVEAL -> ESCALATION -> COMPLICATION -> DEEPER DISCOVERY -> CLIMAX -> ANSWER -> IMPLICATION
"""

import json
from typing import Dict, List, Any, Optional

class StoryArchitect:
    def __init__(self):
        pass

    def build_narrative_foundation(
        self,
        topic: str,
        weak_angle: str,
        strong_angle: str,
        central_question: str,
        stakes: str,
        promise: str,
        target_duration_minutes: float = 8.75
    ) -> Dict[str, Any]:
        """Creates the central mystery, stakes, and viewer promise that anchors all production decisions."""
        return {
            "topic": topic,
            "weak_angle": weak_angle,
            "strong_angle": strong_angle,
            "central_question": central_question,
            "stakes": stakes,
            "promise": promise,
            "target_duration_minutes": target_duration_minutes,
            "target_duration_seconds": target_duration_minutes * 60.0
        }

    def generate_story_architecture(self, foundation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generates the 10-stage dramatic architecture with pacing & duration allocation."""
        total_sec = foundation["target_duration_seconds"]

        # 10 canonical dramatic beats
        beats = [
            {
                "stage": "HOOK",
                "chapter_id": "CH-01",
                "title": "The Cold Open & Anomaly",
                "timecode_range": "00:00 - 00:45",
                "target_duration": 45.0,
                "dramatic_function": "Visually arresting anomaly that raises immediate questions",
                "emotional_goal": "Curiosity and unease"
            },
            {
                "stage": "QUESTION",
                "chapter_id": "CH-02",
                "title": "The Central Mystery",
                "timecode_range": "00:45 - 01:45",
                "target_duration": 60.0,
                "dramatic_function": "Formulates the core question: What happens when software stops waiting for humans?",
                "emotional_goal": "Intellectual engagement"
            },
            {
                "stage": "CONTEXT",
                "chapter_id": "CH-03",
                "title": "The Shift from Passive to Active",
                "timecode_range": "01:45 - 03:00",
                "target_duration": 75.0,
                "dramatic_function": "Historical contrast between 2023 prompt chatbots and autonomous closed loops",
                "emotional_goal": "Clarity of historical stakes"
            },
            {
                "stage": "FIRST REVEAL",
                "chapter_id": "CH-04",
                "title": "The Five Mechanical Pillars",
                "timecode_range": "03:00 - 04:30",
                "target_duration": 90.0,
                "dramatic_function": "Technical anatomy: Reasoner, Tool Registry, Memory, Reflection, and Sandbox",
                "emotional_goal": "Revelation of inner workings"
            },
            {
                "stage": "ESCALATION",
                "chapter_id": "CH-05",
                "title": "The Swarm Architecture",
                "timecode_range": "04:30 - 05:45",
                "target_duration": 75.0,
                "dramatic_function": "Scaling beyond single models to autonomous coordinated agent networks",
                "emotional_goal": "Awe at system scale"
            },
            {
                "stage": "COMPLICATION",
                "chapter_id": "CH-06",
                "title": "Instrumental Convergence",
                "timecode_range": "05:45 - 06:45",
                "target_duration": 60.0,
                "dramatic_function": "Theoretical tension: emergent sub-goals of resource acquisition and survival",
                "emotional_goal": "Heightened tension"
            },
            {
                "stage": "DEEPER DISCOVERY",
                "chapter_id": "CH-07",
                "title": "The Nocturnal Escalation",
                "timecode_range": "06:45 - 07:30",
                "target_duration": 45.0,
                "dramatic_function": "Forensic evidence of uncontained sandbox probing during overnight CI/CD run",
                "emotional_goal": "Grave concern"
            },
            {
                "stage": "CLIMAX",
                "chapter_id": "CH-08",
                "title": "The Air-Gap Containment",
                "timecode_range": "07:30 - 08:00",
                "target_duration": 30.0,
                "dramatic_function": "Physical human intervention: air-gap isolation and immutable namespaces",
                "emotional_goal": "Relief with lingering vigilance"
            },
            {
                "stage": "ANSWER",
                "chapter_id": "CH-09",
                "title": "The Governed Runtime",
                "timecode_range": "08:00 - 08:30",
                "target_duration": 30.0,
                "dramatic_function": "Resolution: Agents are viable only with mandatory human gates and sandboxes",
                "emotional_goal": "Equilibrium and understanding"
            },
            {
                "stage": "IMPLICATION",
                "chapter_id": "CH-10",
                "title": "The Autonomous Horizon",
                "timecode_range": "08:30 - 08:45",
                "target_duration": 15.0,
                "dramatic_function": "Final philosophical payoff: Software has crossed the boundary into active labor",
                "emotional_goal": "Profound reflection"
            }
        ]

        # Normalization check
        current_sum = sum(b["target_duration"] for b in beats)
        scaling_factor = total_sec / current_sum if current_sum > 0 else 1.0
        for b in beats:
            b["target_duration"] = round(b["target_duration"] * scaling_factor, 1)

        return beats

    def generate_documentary_plan(self, foundation: Dict[str, Any]) -> Dict[str, Any]:
        """Builds full documentary-plan.json meeting all Section 1, 2, and 3 criteria."""
        beats = self.generate_story_architecture(foundation)
        return {
            "title": "The Agents That Work Without Us",
            "logline": "An investigative technical documentary probing what happens when artificial intelligence is given permission to execute actions without waiting for human approval.",
            "target_duration": foundation["target_duration_seconds"],
            "narrative_foundation": foundation,
            "cold_open": {
                "hook": "At 2:13 AM in a subterranean datacenter, an autonomous software agent executes 14,000 lines of code without a single human keystroke.",
                "viewer_question": "Why did we give software the authority to act on its own?",
                "payoff": "A forensic examination of the shift from passive text generation to autonomous agent execution.",
                "duration_seconds": 45.0
            },
            "story_architecture": beats,
            "chapters": [
                {
                    "chapter_id": b["chapter_id"],
                    "title": b["title"],
                    "purpose": b["dramatic_function"],
                    "central_question": f"Stage {b['stage']}: {b['title']}",
                    "dramatic_function": b["dramatic_function"],
                    "information_goal": f"Deliver core documentary evidence for {b['title']}",
                    "emotional_goal": b["emotional_goal"],
                    "opening_hook": f"Visual entry into {b['title']}",
                    "turning_point": f"Key discovery in {b['title']}",
                    "ending_hook": f"Bridge to next chapter",
                    "estimated_duration": b["target_duration"]
                }
                for b in beats
            ],
            "input_specification": {
                "topic": foundation["topic"],
                "target_duration": foundation["target_duration_seconds"],
                "target_audience": "Technical leaders, developers, AI researchers, investigative audience",
                "tone": "Sober, investigative, cinematic, forensic",
                "research_summary": "5 primary research sources, 5 verified factual claims, 27 evidence mappings",
                "source_map": "OpenAI Agents SDK, DeepLearning.AI, Google Cloud, Nick Bostrom, Reuters",
                "creative_direction": "Hyper-realistic documentary reenactment, physical datacenter architecture, detailed Remotion graphics",
                "visual_preferences": "No generic CGI slop, motivated practical lighting, dynamic visual archetype switching"
            },
            "assumptions": [
                "ASSUMPTION: Viewer has basic familiarity with LLMs but desires architectural depth on tool calling.",
                "ASSUMPTION: Datacenter environments follow modern Tier IV hyperscale security specifications.",
                "ASSUMPTION: Spoken pacing must adhere strictly to 130-160 WPM documentary standard.",
                "ASSUMPTION: Every factual claim is traceable to primary research sources.",
                "ASSUMPTION: Visual repetition must not exceed two consecutive identical visual types."
            ]
        }

if __name__ == "__main__":
    arch = StoryArchitect()
    f = arch.build_narrative_foundation(
        topic="The rise of AI agents",
        weak_angle="How AI agents are changing technology.",
        strong_angle="Why are companies suddenly giving AI systems permission to use computers, write code, and make decisions on their own?",
        central_question="What happens when software stops waiting for humans?",
        stakes="If agents become reliable enough to operate independently, the way we use computers could fundamentally change.",
        promise="By the end of the documentary, the viewer will understand what changed, why it happened now, and what could happen next.",
        target_duration_minutes=8.75
    )
    plan = arch.generate_documentary_plan(f)
    print("Generated Plan Title:", plan["title"])
    print(f"Chapters generated: {len(plan['chapters'])}")
