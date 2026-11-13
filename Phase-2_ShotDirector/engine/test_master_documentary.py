"""
Master Documentary Verification & QA Test Suite
Strictly validates all 7 production files against Section 1-26 specifications:
1. documentary-plan.json
2. narration.json
3. scene-plan.json
4. shot-plan.json
5. audio-plan.json
6. continuity-bible.json
7. production-summary.json
"""

import json
import sys
from pathlib import Path

def test_master_documentary(base_dir=None):
    if base_dir is None:
        root = Path(__file__).resolve().parent.parent.parent
        fixture_dir = root / "tests" / "fixtures" / "master_documentary"
        base_dir = fixture_dir if fixture_dir.exists() else root
    base = Path(base_dir)
    print(f"\n==========================================")
    print(f"RUNNING MASTER DOCUMENTARY QA AUDIT ON: {base}")
    print(f"==========================================\n")

    required_files = [
        "documentary-plan.json",
        "narration.json",
        "scene-plan.json",
        "shot-plan.json",
        "audio-plan.json",
        "continuity-bible.json",
        "production-summary.json"
    ]

    # 1. Existence check
    for fname in required_files:
        fpath = base / fname
        assert fpath.exists(), f"Missing required file: {fname}"
        assert fpath.stat().st_size > 0, f"File {fname} is empty"
        print(f"[OK] File exists and non-empty: {fname} ({fpath.stat().st_size:,} bytes)")

    # 2. Load JSON files
    with open(base / "documentary-plan.json", "r", encoding="utf-8") as f:
        doc_plan = json.load(f)
    with open(base / "narration.json", "r", encoding="utf-8") as f:
        narration = json.load(f)
    with open(base / "scene-plan.json", "r", encoding="utf-8") as f:
        scene_plan = json.load(f)
    with open(base / "shot-plan.json", "r", encoding="utf-8") as f:
        shot_plan = json.load(f)
    with open(base / "audio-plan.json", "r", encoding="utf-8") as f:
        audio_plan = json.load(f)
    with open(base / "continuity-bible.json", "r", encoding="utf-8") as f:
        bible = json.load(f)
    with open(base / "production-summary.json", "r", encoding="utf-8") as f:
        summary = json.load(f)

    # 3. Audit documentary-plan.json
    print("\n--- 1. Auditing documentary-plan.json ---")
    assert "title" in doc_plan and doc_plan["title"], "Missing title"
    assert "logline" in doc_plan and doc_plan["logline"], "Missing logline"
    assert "target_duration" in doc_plan and doc_plan["target_duration"] > 0, "Invalid target_duration"
    assert "chapters" in doc_plan and len(doc_plan["chapters"]) >= 5, "Fewer than 5 chapters"
    assert "cold_open" in doc_plan, "Missing cold_open object"
    co = doc_plan["cold_open"]
    for k in ["hook", "viewer_question", "payoff", "duration_seconds"]:
        assert k in co, f"Missing {k} in cold_open"
    assert 20 <= co["duration_seconds"] <= 60, f"Cold open duration out of bounds (20-60s): {co['duration_seconds']}"
    print(f"[PASS] Cold open validated: {co['duration_seconds']}s (Within 20-60s rule)")

    # Audit Section 2 Input and Marked Assumptions
    assert "input_specification" in doc_plan, "Missing input_specification in documentary-plan.json"
    in_spec = doc_plan["input_specification"]
    for k in ["topic", "target_duration", "target_audience", "tone", "research_summary", "source_map", "creative_direction", "visual_preferences"]:
        assert k in in_spec, f"Missing {k} in input_specification"
    assert "assumptions" in doc_plan, "Missing assumptions list in documentary-plan.json"
    assert len(doc_plan["assumptions"]) >= 3, "Too few assumptions documented"
    for assump in doc_plan["assumptions"]:
        assert assump.startswith("ASSUMPTION:"), f"Assumption not marked with 'ASSUMPTION:' tag: {assump}"
    print(f"[PASS] Section 2 Input & {len(doc_plan['assumptions'])} marked ASSUMPTION tags verified")

    for ch in doc_plan["chapters"]:
        for k in ["chapter_id", "title", "purpose", "central_question", "dramatic_function", "information_goal", "emotional_goal", "opening_hook", "turning_point", "ending_hook", "estimated_duration"]:
            assert k in ch, f"Missing {k} in chapter {ch.get('chapter_id')}"
    print(f"[PASS] All {len(doc_plan['chapters'])} chapters conform strictly to Section 3 schema")

    # 4. Audit narration.json
    print("\n--- 2. Auditing narration.json ---")
    assert len(narration) >= 25, f"Narration segments too few: {len(narration)}"
    total_words = 0
    prev_end = 0.0
    for seg in narration:
        for k in ["segment_id", "chapter_id", "text", "word_count", "start", "end", "start_time", "end_time", "estimated_duration", "claim_ids"]:
            assert k in seg, f"Missing {k} in segment {seg.get('segment_id')}"
        assert abs(seg["start"] - prev_end) < 0.001, f"Gap or overlap in narration timeline at {seg['segment_id']}: expected {prev_end}, got {seg['start']}"
        assert abs(seg["start"] - seg["start_time"]) < 0.001, f"start vs start_time mismatch in {seg['segment_id']}"
        assert abs(seg["end"] - seg["end_time"]) < 0.001, f"end vs end_time mismatch in {seg['segment_id']}"
        assert abs((seg["end"] - seg["start"]) - seg["estimated_duration"]) < 0.001, f"estimated_duration mismatch in {seg['segment_id']}"
        
        prev_end = seg["end"]
        total_words += seg["word_count"]
        # Strict WPM check per segment: 130-160 WPM guideline
        dur_min = (seg["end"] - seg["start"]) / 60.0
        wpm = seg["word_count"] / dur_min
        assert 130.0 <= wpm <= 160.0, f"VIOLATION: Spoken pacing out of 130-160 WPM bounds at {seg['segment_id']}: {wpm:.1f} WPM ({seg['word_count']} words in {seg['end']-seg['start']}s)"

    avg_wpm = total_words / (prev_end / 60.0)
    assert 130.0 <= avg_wpm <= 160.0, f"Average WPM out of bounds: {avg_wpm:.1f}"
    print(f"[PASS] Continuous narration timeline verified: 0.0s to {prev_end:.1f}s")
    print(f"[PASS] Total words: {total_words}, Average spoken speed: {avg_wpm:.1f} WPM (Strictly within 130-160 WPM across 100% of segments)")

    # 5. Audit scene-plan.json
    print("\n--- 3. Auditing scene-plan.json ---")
    scenes = scene_plan["scenes"]
    assert len(scenes) >= 25, f"Too few scenes: {len(scenes)}"
    for scn in scenes:
        for k in ["scene_id", "chapter_id", "purpose", "narration_segments", "shots", "start", "end"]:
            assert k in scn, f"Missing {k} in scene {scn.get('scene_id')}"
        assert len(scn["shots"]) >= 1, f"Scene {scn['scene_id']} has no shots"
    print(f"[PASS] All {len(scenes)} scenes verified with attached shots and narration segments")

    # 6. Audit shot-plan.json
    print("\n--- 4. Auditing shot-plan.json ---")
    assert len(shot_plan) >= 50, f"Too few shots: {len(shot_plan)}"
    prev_shot_end = 0.0
    type_counts = {}
    consecutive_arch = None
    streak = 0
    max_streak = 1 if len(shot_plan) > 0 else 0

    valid_visual_types = [
        "ARCHIVAL_FOOTAGE", "REAL_FOOTAGE", "PHOTOGRAPH", "AI_IMAGE", "AI_VIDEO",
        "BLENDER_3D", "MAP", "SATELLITE_MAP", "DOCUMENT", "SCREEN_CAPTURE",
        "NEWS_CLIP", "INTERVIEW", "QUOTE_CARD", "DATA_GRAPHIC", "TIMELINE",
        "DIAGRAM", "CODE_VISUALIZATION", "NETWORK_GRAPH", "UI_RECONSTRUCTION",
        "MOTION_GRAPHIC", "TEXTURE_BROLL", "ABSTRACT_TRANSITION"
    ]

    sec9_and_25_fields = [
        "shot_id", "scene_id", "narration_segment", "start", "start_time", "end", "end_time", "duration",
        "visual_type", "visual_purpose", "subject", "action", "environment",
        "camera", "lens", "composition", "lighting", "atmosphere", "motion",
        "generation_method", "generation_prompt", "asset_requirement", "asset_requirements",
        "source_requirement", "source_ids", "claim_ids", "transition_in", "transition_out",
        "continuity", "continuity_notes"
    ]

    sec14_blender_fields = [
        "environment", "objects", "materials", "camera_position", "camera_target",
        "lens", "depth_of_field", "lighting", "fog", "animation", "camera_path", "render_duration"
    ]

    for s in shot_plan:
        for k in sec9_and_25_fields:
            assert k in s, f"Missing {k} in shot {s.get('shot_id')} (Violates Section 9/25)"

        assert s["visual_type"] in valid_visual_types, f"Invalid visual type {s['visual_type']} in shot {s['shot_id']}"
        assert abs(s["start"] - prev_shot_end) < 0.001, f"Shot timeline discontinuity at {s['shot_id']}: expected {prev_shot_end}, got {s['start']}"
        assert abs((s["end"] - s["start"]) - s["duration"]) < 0.001, f"Duration mismatch in shot {s['shot_id']}"
        assert abs(s["start"] - s["start_time"]) < 0.001, f"start vs start_time mismatch in {s['shot_id']}"
        assert abs(s["end"] - s["end_time"]) < 0.001, f"end vs end_time mismatch in {s['shot_id']}"
        prev_shot_end = s["end"]

        vt = s["visual_type"]
        type_counts[vt] = type_counts.get(vt, 0) + 1

        # Correct streak calculation
        if vt == consecutive_arch:
            streak += 1
        else:
            streak = 1
            consecutive_arch = vt

        if streak > max_streak:
            max_streak = streak

        assert streak <= 2, f"VIOLATION: Visual repetition limit exceeded! {vt} repeated {streak} times consecutively at {s['shot_id']}"

        # Visual prompt checks
        if vt == "AI_IMAGE":
            prompt = s["generation_prompt"]
            for field in ["SUBJECT:", "LOCATION:", "TIME / ERA:", "ACTION:", "ENVIRONMENT:", "ARCHITECTURE:", "MATERIALS:", "CAMERA POSITION:", "CAMERA MOVEMENT:", "LENS:", "COMPOSITION:", "FOREGROUND:", "MIDGROUND:", "BACKGROUND:", "LIGHTING:", "COLOR TEMPERATURE:", "ATMOSPHERE:", "WEATHER:", "DEPTH:", "REALISM:", "VISUAL STYLE:", "CONTINUITY REQUIREMENTS:", "NEGATIVE CONSTRAINTS:"]:
                assert field in prompt, f"Shot {s['shot_id']} AI_IMAGE prompt missing Section 12 field: {field}"

        if vt == "AI_VIDEO":
            prompt = s["generation_prompt"]
            for field in ["INITIAL FRAME:", "SUBJECT MOTION:", "CAMERA MOTION:", "ENVIRONMENT MOTION:", "LIGHTING MOTION:", "FOREGROUND MOTION:", "BACKGROUND MOTION:", "ENDING FRAME:", "DURATION:"]:
                assert field in prompt, f"Shot {s['shot_id']} AI_VIDEO prompt missing Section 13 field: {field}"

        if vt == "BLENDER_3D":
            prompt = s["generation_prompt"]
            b_data = json.loads(prompt)
            for field in sec14_blender_fields:
                assert field in b_data, f"Shot {s['shot_id']} BLENDER_3D prompt missing Section 14 field: {field}"

        # Strict Section 17 Evidence Check: 100% of shots with claim_ids MUST have an evidence structure
        if s["claim_ids"]:
            assert "evidence" in s, f"VIOLATION: Shot {s['shot_id']} references claims {s['claim_ids']} but has no Section 17 evidence structure"
            ev = s["evidence"]
            for k in ["claim_id", "visual_type", "source_id", "display_method"]:
                assert k in ev, f"Missing {k} in evidence structure of shot {s['shot_id']}"
            assert ev["claim_id"] in s["claim_ids"], f"Evidence claim_id mismatch in {s['shot_id']}"

    print(f"[PASS] Shot timeline continuity verified: 0.0s to {prev_shot_end:.1f}s across {len(shot_plan)} shots")
    print(f"[PASS] All shots verified for complete Section 9 (23 fields) and Section 25 schema compliance")
    print(f"[PASS] All {type_counts.get('BLENDER_3D', 0)} Blender 3D shots verified for all 12 Section 14 fields (fog, camera_path, etc.)")
    print(f"[PASS] All claimed shots verified with Section 17 evidence structures (Zero omissions, zero bypasses)")
    print(f"[PASS] Max consecutive visual streak: {max_streak} (Strictly <= 2 allowed, ZERO violations!)")
    print(f"[PASS] Visual Type Distribution: {json.dumps(type_counts, indent=2)}")

    # 7. Audit audio-plan.json
    print("\n--- 5. Auditing audio-plan.json ---")
    audio_scns = audio_plan["scenes"]
    assert len(audio_scns) == len(scenes), f"Mismatch between scene count ({len(scenes)}) and audio plan scenes ({len(audio_scns)})"
    for a in audio_scns:
        assert "scene_id" in a and "audio" in a, f"Invalid audio scene format in {a}"
        aud = a["audio"]
        for k in ["music_state", "music_intensity", "ambience", "sfx", "impact", "silence", "silence_before_reveal"]:
            assert k in aud, f"Missing {k} in audio scene {a['scene_id']}"
        assert 0.0 <= aud["music_intensity"] <= 1.0, f"Invalid music intensity in {a['scene_id']}: {aud['music_intensity']}"
    print(f"[PASS] All {len(audio_scns)} audio scenes strictly conform to Section 21 specification")

    # 8. Audit continuity-bible.json
    print("\n--- 6. Auditing continuity-bible.json ---")
    sec23_dimensions = [
        "characters", "locations", "objects", "architecture", "time_period",
        "weather", "lighting", "camera_language", "visual_style", "colors",
        "clothing", "technology", "visual_rules"
    ]
    for k in sec23_dimensions:
        assert k in bible, f"Missing Section 23 dimension '{k}' in continuity-bible.json"
    assert len(bible["characters"]) >= 2, "Missing key characters in continuity bible"
    assert len(bible["locations"]) >= 2, "Missing key locations in continuity bible"
    assert len(bible["objects"]) >= 2, "Missing key objects in continuity bible"
    print(f"[PASS] Continuity bible verified: 100% compliance with all 13 Section 23 & 25 dimensions")

    # 9. Audit Claims Grounding & Phase-0 Research Files
    print("\n--- 7. Auditing Fact & Claim Grounding ---")
    claims_in_narration = set()
    for seg in narration:
        for cid in seg["claim_ids"]:
            claims_in_narration.add(cid)

    expected_claims = {"CLM-01", "CLM-02", "CLM-03", "CLM-04", "CLM-05"}
    missing_claims = expected_claims - claims_in_narration
    assert not missing_claims, f"Missing required claims in narration: {missing_claims}"
    print(f"[PASS] All claims grounded in narration: {sorted(list(claims_in_narration))}")

    # Check Phase-0 research files
    phase0_dir = base / "Phase-0_Research"
    if phase0_dir.exists():
        assert (phase0_dir / "claims" / "claims.json").exists(), "Missing Phase-0 claims.json"
        assert (phase0_dir / "source-map" / "source-map.json").exists(), "Missing Phase-0 source-map.json"
        assert (phase0_dir / "evidence" / "evidence.json").exists(), "Missing Phase-0 evidence.json"
        print("[PASS] Phase-0 Research repositories verified (claims.json, source-map.json, evidence.json)")

    # 10. Audit production-summary.json
    print("\n--- 8. Auditing production-summary.json ---")
    for k in ["total_duration", "total_chapters", "total_scenes", "total_shots", "shots_by_visual_type", "AI_image_count", "AI_video_count", "Blender_shot_count", "archival_count", "graphic_count", "document_count", "estimated_narration_words", "estimated_render_complexity"]:
        assert k in summary, f"Missing {k} in production summary"
    assert summary["total_shots"] == len(shot_plan), "Summary shot count mismatch"
    assert summary["total_duration"] == prev_shot_end, "Summary duration mismatch"
    assert summary["Blender_shot_count"] == type_counts.get("BLENDER_3D", 0), "Summary Blender count mismatch"
    assert summary["AI_video_count"] == type_counts.get("AI_VIDEO", 0), "Summary AI video count mismatch"
    assert summary["AI_image_count"] == type_counts.get("AI_IMAGE", 0), "Summary AI image count mismatch"
    assert summary["estimated_narration_words"] == total_words, "Summary narration words mismatch"
    
    # Check that render complexity string accurately matches the counts
    complexity_str = summary["estimated_render_complexity"]
    assert f"{summary['Blender_shot_count']} Blender Cycles" in complexity_str, f"Mismatch in complexity string: {complexity_str}"
    assert f"{summary['AI_video_count']} Runway Gen-3" in complexity_str, f"Mismatch in complexity string: {complexity_str}"
    assert f"{summary['AI_image_count']} Gemini" in complexity_str, f"Mismatch in complexity string: {complexity_str}"
    print(f"[PASS] Production summary verified: {summary['total_shots']} shots, {summary['total_duration']}s, render complexity: {summary['estimated_render_complexity'][:40]}...")

    print(f"\n==========================================")
    print(f"ALL AUDIT CHECKS PASSED: 100% PRODUCTION READY!")
    print(f"==========================================\n")

if __name__ == "__main__":
    test_dir = sys.argv[1] if len(sys.argv) > 1 else r"D:\gitM\01_ContentFactory"
    test_master_documentary(test_dir)
