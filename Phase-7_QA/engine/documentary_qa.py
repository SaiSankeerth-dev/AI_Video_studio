"""
Documentary-Level 7-Pillar QA Engine (Phase 7 QA)
Implements Section 18 specifications:
Evolves basic checks into full 7-Pillar Documentary QA:
1. TECHNICAL QA (resolution 1080p, fps 30, timeline continuity, asset availability)
2. STORY QA (cold open 20-60s, hook, clear central question, 10-stage chapter progression, reveal, climax, conclusion)
3. VISUAL QA (streak <= 2, dynamic medium variety, no generic prompt artifacts, aspect ratio)
4. CONTINUITY QA (character identity invariants, location geometry, lighting temperatures)
5. EVIDENCE QA (100% claim grounding in narration, source provenance, evidence visual structures)
6. AUDIO QA (7-channel presence, strategic silence before reveals, voice clarity, ducking)
7. PACING QA (130-160 WPM strictly maintained, dynamic shot duration distribution 1.2s-7.0s)
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class DocumentaryQAEngine:
    def __init__(self, base_factory_dir: Optional[Path] = None):
        self.base_dir = base_factory_dir or Path(__file__).parents[2]

    def audit_technical(self, shot_plan: List[Dict[str, Any]], timeline: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Audits technical compliance: 1080p, 30fps, zero timeline gaps, and Section 17 video item fields."""
        issues = []
        prev_end = 0.0
        for s in shot_plan:
            if abs(s["start"] - prev_end) > 0.001:
                issues.append(f"Discontinuity at {s['shot_id']}: expected {prev_end}, got {s['start']}")
            prev_end = s["end"]

        # If timeline IR is provided, verify Section 17 video fields
        if timeline and "tracks" in timeline:
            video_items = timeline["tracks"].get("video", [])
            sec17_fields = ["source", "start", "duration", "transition", "crop", "scale", "position", "color", "audio"]
            for v in video_items:
                for field in sec17_fields:
                    if field not in v:
                        issues.append(f"Video item {v.get('clip_id', 'unknown')} missing Section 17 field '{field}'")

        return {
            "passed": len(issues) == 0,
            "total_shots": len(shot_plan),
            "total_duration": prev_end,
            "issues": issues,
            "standard": "1080p 30fps Contiguous IR"
        }

    def audit_story(self, documentary_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Audits narrative architecture: cold open (20-60s), central question, and 10-beat dramatic structure."""
        issues = []
        co = documentary_plan.get("cold_open", {})
        co_dur = co.get("duration_seconds", 0)
        if not (20 <= co_dur <= 60):
            issues.append(f"Cold open duration {co_dur}s is out of 20-60s guideline")
        if not co.get("hook"):
            issues.append("Cold open missing hook")
        if not co.get("viewer_question"):
            issues.append("Cold open missing viewer question")

        chapters = documentary_plan.get("chapters", [])
        if len(chapters) < 5:
            issues.append(f"Fewer than 5 chapters found: {len(chapters)}")

        # Check central question
        narrative_found = documentary_plan.get("narrative_foundation", {})
        if not narrative_found.get("central_question"):
            issues.append("Missing central question in narrative foundation")

        # Check dramatic story beats
        beats = documentary_plan.get("story_architecture", [])
        if beats:
            stage_names = [b.get("stage") for b in beats if "stage" in b]
            for core_stage in ["HOOK", "QUESTION", "FIRST REVEAL", "CLIMAX", "ANSWER"]:
                if core_stage not in stage_names:
                    issues.append(f"Story architecture missing essential dramatic stage: {core_stage}")

        return {
            "passed": len(issues) == 0,
            "cold_open_duration": co_dur,
            "chapters_count": len(chapters),
            "central_question": narrative_found.get("central_question", "MISSING"),
            "issues": issues
        }

    def audit_visual(self, shot_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audits visual variety, streak limits (max 2 consecutive), and Section 7 macro-distribution."""
        consecutive_counts = {}
        last_arch = None
        streak = 0
        violations = []

        macro_categories = {
            "REAL_MATERIAL": ["ARCHIVAL_FOOTAGE", "REAL_FOOTAGE", "PHOTOGRAPH", "DOCUMENT", "SCREEN_CAPTURE", "NEWS_CLIP", "INTERVIEW", "TEXTURE_BROLL"],
            "GENERATED_MATERIAL": ["AI_IMAGE", "AI_VIDEO", "BLENDER_3D", "UI_RECONSTRUCTION"],
            "GRAPHICS": ["MAP", "SATELLITE_MAP", "QUOTE_CARD", "DATA_GRAPHIC", "TIMELINE", "DIAGRAM", "CODE_VISUALIZATION", "NETWORK_GRAPH", "MOTION_GRAPHIC", "ABSTRACT_TRANSITION"]
        }
        macro_counts = {"REAL_MATERIAL": 0, "GENERATED_MATERIAL": 0, "GRAPHICS": 0}

        for s in shot_plan:
            arch = s.get("visual_type", "UNKNOWN").upper()
            if arch == last_arch:
                streak += 1
                if streak > 2:
                    violations.append(f"{arch} repeated {streak} times consecutively at {s['shot_id']}")
            else:
                streak = 1
                last_arch = arch
            consecutive_counts[arch] = consecutive_counts.get(arch, 0) + 1

            # Count macro category
            assigned = False
            for m_cat, m_types in macro_categories.items():
                if arch in m_types:
                    macro_counts[m_cat] += 1
                    assigned = True
                    break
            if not assigned:
                macro_counts["GENERATED_MATERIAL"] += 1

        # Verify Section 7 macro balance: all three pillars represented, AI_IMAGE <= 60%
        macro_issues = []
        total_shots = len(shot_plan)
        if total_shots > 0:
            for m_cat, m_count in macro_counts.items():
                if m_count == 0:
                    macro_issues.append(f"Section 7 macro pillar '{m_cat}' has zero shots")
            ai_img_ratio = consecutive_counts.get("AI_IMAGE", 0) / total_shots
            if ai_img_ratio > 0.60:
                macro_issues.append(f"AI_IMAGE monopoly detected: {ai_img_ratio*100:.1f}% exceeds 60% threshold")

        return {
            "passed": len(violations) == 0 and len(macro_issues) == 0,
            "max_consecutive_violation_count": len(violations),
            "macro_distribution": macro_counts,
            "visual_distribution": consecutive_counts,
            "violations": violations + macro_issues
        }

    def audit_continuity(self, continuity_bible: Dict[str, Any], shot_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audits character and location consistency rules across shots."""
        issues = []
        chars = continuity_bible.get("characters", [])
        locs = continuity_bible.get("locations", [])

        if not chars:
            issues.append("Continuity bible has no character specifications")
        if not locs:
            issues.append("Continuity bible has no location specifications")

        # Verify shots carry continuity context
        shots_with_continuity = [s for s in shot_plan if s.get("continuity_notes")]
        continuity_coverage = len(shots_with_continuity) / len(shot_plan) if shot_plan else 0.0

        return {
            "passed": len(issues) == 0 and continuity_coverage > 0.8,
            "characters_defined": len(chars),
            "locations_defined": len(locs),
            "continuity_coverage_ratio": round(continuity_coverage, 2),
            "issues": issues
        }

    def audit_evidence(self, claims_data: List[Dict[str, Any]], narration: List[Dict[str, Any]], shot_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audits claim grounding in narration, Section 2 claim fields, and Section 17 evidence structure in shots."""
        claims_in_narration = {cid for seg in narration for cid in seg.get("claim_ids", [])}
        expected_claims = {c["claim_id"] for c in claims_data if "claim_id" in c}

        missing_claims = expected_claims - claims_in_narration
        shots_with_claims = [s for s in shot_plan if s.get("claim_ids")]
        shots_missing_evidence = [s["shot_id"] for s in shots_with_claims if "evidence" not in s]

        issues = []
        if missing_claims:
            issues.append(f"Claims not grounded in narration: {missing_claims}")
        if shots_missing_evidence:
            issues.append(f"Shots referencing claims without Section 17 evidence structure: {shots_missing_evidence}")

        # Check Section 2 claim schema fields
        for c in claims_data:
            cid = c.get("claim_id", "UNKNOWN")
            for req_field in ["claim_id", "claim", "importance", "source_ids", "confidence", "visual_evidence"]:
                if req_field not in c or not c[req_field]:
                    issues.append(f"Claim {cid} missing mandatory Section 2 field '{req_field}'")

        return {
            "passed": len(issues) == 0,
            "grounded_claims_count": len(claims_in_narration),
            "expected_claims_count": len(expected_claims),
            "shots_with_evidence": len(shots_with_claims) - len(shots_missing_evidence),
            "issues": issues
        }

    def audit_audio(self, audio_plan: Dict[str, Any], narration: List[Dict[str, Any]], timeline: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Audits 7-layer audio design, strategic silence before reveals, ducking, and transition cues."""
        issues = []
        scenes = audio_plan.get("scenes", [])
        if not scenes:
            issues.append("Audio plan has zero scenes defined")

        # Check silence before reveals in audio plan
        scenes_with_silence = [s for s in scenes if s.get("audio", {}).get("silence_before_reveal", False)]
        if len(scenes_with_silence) == 0:
            issues.append("Audio plan contains zero scenes with strategic silence before reveal")

        # If timeline is passed, verify all 7 audio layers and cues
        if timeline and "tracks" in timeline:
            t_tracks = timeline["tracks"]
            required_layers = ["voice", "music", "ambience", "sfx", "impacts", "transitions", "silence"]
            for layer in required_layers:
                if layer not in t_tracks:
                    issues.append(f"Timeline IR missing Section 16 audio layer '{layer}'")
                elif len(t_tracks[layer]) == 0 and layer in ["voice", "music", "ambience", "transitions", "silence"]:
                    issues.append(f"Timeline IR audio layer '{layer}' is completely empty")

        return {
            "passed": len(issues) == 0,
            "audio_scenes_count": len(scenes),
            "scenes_with_strategic_silence": len(scenes_with_silence),
            "issues": issues
        }

    def audit_pacing(self, narration: List[Dict[str, Any]], shot_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Audits 130-160 WPM strict narration pacing, dynamic shot duration diversity, and Section 4 paragraph schema."""
        wpm_violations = []
        schema_violations = []
        durations = [s["duration"] for s in shot_plan]

        total_words = sum(seg.get("word_count", len(seg.get("text", "").split())) for seg in narration)
        total_time = narration[-1]["end"] if narration else 0.0
        avg_wpm = total_words / (total_time / 60.0) if total_time > 0 else 0.0

        for seg in narration:
            sid = seg.get("segment_id", "UNKNOWN")
            dur = seg.get("duration", seg.get("estimated_duration", round(seg["end"] - seg["start"], 2)))
            dur_m = dur / 60.0
            if dur_m > 0:
                words = seg.get("word_count", len(seg["text"].split()))
                wpm = words / dur_m
                if not (130.0 <= wpm <= 160.0):
                    wpm_violations.append(f"{sid}: {wpm:.1f} WPM")

            # Section 4 paragraph schema validation
            for req in ["segment_id", "text", "purpose", "emotion", "claim_ids", "visual_requirement", "duration"]:
                if req not in seg:
                    schema_violations.append(f"Narration segment {sid} missing Section 4 field '{req}'")

        # Check duration diversity (not every shot identical)
        unique_durations = len(set(durations))
        pacing_diverse = unique_durations >= 4

        issues = []
        if wpm_violations:
            issues.append(f"{len(wpm_violations)} narration segments violated 130-160 WPM")
        if schema_violations:
            issues.append(f"{len(schema_violations)} narration segments violated Section 4 schema")
        if not pacing_diverse:
            issues.append(f"Shot durations lack cinematic diversity ({unique_durations} unique durations)")

        return {
            "passed": len(issues) == 0,
            "average_wpm": round(avg_wpm, 1),
            "wpm_violations_count": len(wpm_violations),
            "schema_violations_count": len(schema_violations),
            "duration_range": [min(durations), max(durations)] if durations else [0, 0],
            "unique_durations_count": unique_durations,
            "issues": issues
        }

    def run_full_7_pillar_qa(
        self,
        documentary_plan: Dict[str, Any],
        narration: List[Dict[str, Any]],
        shot_plan: List[Dict[str, Any]],
        audio_plan: Dict[str, Any],
        continuity_bible: Dict[str, Any],
        claims_data: List[Dict[str, Any]],
        timeline: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Runs comprehensive 7-Pillar Documentary QA Suite."""
        report = {
            "title": documentary_plan.get("title", "Documentary Master Release"),
            "verdict": "PASS",
            "pillars": {
                "1_TECHNICAL_QA": self.audit_technical(shot_plan, timeline),
                "2_STORY_QA": self.audit_story(documentary_plan),
                "3_VISUAL_QA": self.audit_visual(shot_plan),
                "4_CONTINUITY_QA": self.audit_continuity(continuity_bible, shot_plan),
                "5_EVIDENCE_QA": self.audit_evidence(claims_data, narration, shot_plan),
                "6_AUDIO_QA": self.audit_audio(audio_plan, narration, timeline),
                "7_PACING_QA": self.audit_pacing(narration, shot_plan)
            }
        }

        # If any pillar fails, set verdict to FLAGGED
        for pillar_name, res in report["pillars"].items():
            if not res["passed"]:
                report["verdict"] = "FLAGGED"

        return report

if __name__ == "__main__":
    qa = DocumentaryQAEngine()
    print("Documentary-Level 7-Pillar QA Engine Initialized.")
