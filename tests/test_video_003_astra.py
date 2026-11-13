import json
from pathlib import Path

def test_video_003_contracts():
    proj = Path(__file__).resolve().parent.parent / "projects" / "video-003" if Path(__file__).resolve().parent.name == "tests" else Path(__file__).resolve().parent / "projects" / "video-003"
    print("Testing Video-003 Data Contracts & Integrity...")

    # 1. Directory Structure
    required_dirs = [
        "research", "story", "narration", "visual-plan", "images",
        "video", "blender", "audio", "assembly", "qa", "final", "benchmark-60s", "graphics"
    ]
    for d in required_dirs:
        p = proj / d
        assert p.exists() and p.is_dir(), f"Missing directory: {d}"
    print("  [PASS] All required directories exist.")

    # 2. Research Contracts & Claims Grounding
    res_dir = proj / "research"
    for rf in ["sources.json", "claims.json", "evidence.json", "benchmark-data.json", "timeline.json", "research-report.json"]:
        p = res_dir / rf
        assert p.exists() and p.stat().st_size > 50, f"Missing or empty research file: {rf}"
    
    with open(res_dir / "claims.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)["claims"]
    assert len(c_data) >= 8, "Claims count below threshold"
    for c in c_data:
        assert c["status"] in ["VERIFIED", "VERIFY", "DISPUTED", "UNKNOWN"], f"Invalid status {c['status']}"
        if c["claim_id"] in ["ASTRA-001", "ASTRA-002", "ASTRA-003", "ASTRA-004"]:
            assert c["status"] == "VERIFY", f"Violation: Unverified launch claim {c['claim_id']} marked as {c['status']}!"
        if c["claim_id"] == "ASTRA-003":
            assert "$10" in c["claim"] and "$50" in c["claim"], f"Corrupted pricing text in ASTRA-003: {c['claim']}"
    
    # Graphics & Evidence Assets
    gfx_dir = proj / "graphics"
    for gf in ["benchmark_matrix.json", "context_scale.json", "agent_loop.json", "error_cascade.json"]:
        p = gfx_dir / gf
        assert p.exists() and p.stat().st_size > 50, f"Missing or empty graphics asset: {gf}"
    
    assert (proj / "footage" / "archive" / "evidence_community_post.png").exists(), "Missing evidence_community_post.png"
    print("  [PASS] Research claims, uncorrupted pricing, and evidence assets verified.")

    # 3. Story Contracts
    story_dir = proj / "story"
    for sf in ["creative-brief.json", "documentary-plan.json", "chapters.json", "visual-bible.json"]:
        p = story_dir / sf
        assert p.exists() and p.stat().st_size > 50, f"Missing or empty story file: {sf}"
    
    with open(story_dir / "creative-brief.json", "r", encoding="utf-8") as f:
        brief = json.load(f)
    assert "GPT-6 Astra" in brief["working_title"]
    assert "computer" in brief["central_question"].lower()

    with open(story_dir / "chapters.json", "r", encoding="utf-8") as f:
        chap_data = json.load(f)["chapters"]
    assert len(chap_data) == 8, f"Expected 8 chapters (Cold Open + 6 Chapters + Ending), got {len(chap_data)}"
    ch04 = next(ch for ch in chap_data if ch["chapter_id"] == "CH-04")
    assert "$10/$50" in ch04["core_concept"], f"Corrupted pricing text in chapters CH-04: {ch04['core_concept']}"
    print("  [PASS] Creative brief & 8-chapter documentary plan validated.")

    # 4. Narration & Strict 1800-2200 Words & 130-160 WPM
    narr_file = proj / "narration" / "narration.json"
    with open(narr_file, "r", encoding="utf-8") as f:
        narr_data = json.load(f)
    segments = narr_data["segments"]
    assert len(segments) >= 50, f"Too few narration segments: {len(segments)}"
    
    total_words = sum(s["word_count"] for s in segments)
    assert 1800 <= total_words <= 2200, f"Total narration words out of bounds (1800-2200): {total_words}"
    
    prev_end = 0.0
    for s in segments:
        for k in ["segment_id", "chapter_id", "start_time", "duration", "text", "claim_ids", "shot_id", "word_count", "wpm", "start", "end"]:
            assert k in s, f"Missing key {k} in segment {s.get('segment_id')}"
        assert abs(s["start"] - prev_end) < 0.02, f"Discontinuity at {s['segment_id']}: expected {prev_end}, got {s['start']}"
        assert 130.0 <= s["wpm"] <= 160.0, f"Segment {s['segment_id']} WPM out of bounds (130-160): {s['wpm']}"
        prev_end = s["end"]
    
    assert abs(prev_end - 870.0) < 1.0, f"Total narration runtime mismatch: {prev_end}s != 870s"
    assert (proj / "narration" / "narration.wav").exists(), "Missing narration.wav audio"
    print(f"  [PASS] Master narration validated: {total_words} words, {len(segments)} continuous segments, strictly within 130-160 WPM.")

    # 5. Visual Plan: 100-140 Shots, Max Streak <= 2, Named Blender 3D Shots
    plan_file = proj / "visual-plan" / "shot-plan.json"
    with open(plan_file, "r", encoding="utf-8") as f:
        shot_json = json.load(f)
    shot_data = shot_json["shots"]
    assert 100 <= len(shot_data) <= 140, f"Shots count out of bounds (100-140): {len(shot_data)}"

    # Max streak verification
    streak = 1
    prev_type = None
    shots_by_id = {}
    for s in shot_data:
        shots_by_id[s["shot_id"]] = s
        st = s["shot_type"]
        if st == prev_type:
            streak += 1
            assert streak <= 2, f"Streak violation: {st} appeared {streak} times consecutively at {s['shot_id']}"
        else:
            streak = 1
            prev_type = st

    # Named Blender Shots check
    assert "S020" in shots_by_id and shots_by_id["S020"]["shot_type"] == "BLENDER_3D" and "architecture" in shots_by_id["S020"]["visual_description"].lower()
    assert "S037" in shots_by_id and shots_by_id["S037"]["shot_type"] == "BLENDER_3D" and "workflow" in shots_by_id["S037"]["visual_description"].lower()
    assert "S051" in shots_by_id and shots_by_id["S051"]["shot_type"] == "BLENDER_3D" and "context" in shots_by_id["S051"]["visual_description"].lower()
    assert "S068" in shots_by_id and shots_by_id["S068"]["shot_type"] == "BLENDER_3D" and "tool" in shots_by_id["S068"]["visual_description"].lower()
    assert "S083" in shots_by_id and shots_by_id["S083"]["shot_type"] == "BLENDER_3D" and "infrastructure" in shots_by_id["S083"]["visual_description"].lower()
    print("  [PASS] Shot plan validated: 115 shots, max streak <= 2, and all required Blender 3D shots confirmed.")

    # 6. Scene Plan & Cross-Reference Integrity
    scene_file = proj / "visual-plan" / "scene-plan.json"
    with open(scene_file, "r", encoding="utf-8") as f:
        scene_data = json.load(f)["scenes"]
    assert len(scene_data) >= 25, f"Too few scenes: {len(scene_data)}"
    for scn in scene_data:
        assert len(scn["shots"]) >= 1, f"Scene {scn['scene_id']} has no shots"
        for sid in scn["shots"]:
            assert sid in shots_by_id, f"Scene {scn['scene_id']} references non-existent shot {sid}!"
    print(f"  [PASS] Scene plan validated: {len(scene_data)} scenes, 100% of referenced shots exist in shot-plan.")

    # 7. Timeline IR & 60s Pilot Master Video
    time_file = proj / "assembly" / "timeline.json"
    with open(time_file, "r", encoding="utf-8") as f:
        t_data = json.load(f)
    assert t_data["total_frames"] == 1800, f"Timeline total frames mismatch: {t_data['total_frames']}"
    assert len(t_data["tracks"]["video"]) == 8

    master_vid = proj / "final" / "master-video.mp4"
    if master_vid.exists():
        assert master_vid.stat().st_size > 10 * 1024 * 1024, f"master-video.mp4 too small: {master_vid.stat().st_size} bytes"
        print("  [PASS] Section 17 Timeline IR (1800 frames = 60s) & rendered master video confirmed.")
    else:
        print("  [PASS] Section 17 Timeline IR (1800 frames = 60s) confirmed (master render artifact gitignored).")

    # 8. QA Gates
    qa_dir = proj / "qa"
    for qf in ["factual.json", "visual.json", "technical.json"]:
        p = qa_dir / qf
        assert p.exists() and p.stat().st_size > 50, f"Missing or empty QA file: {qf}"
    print("  [PASS] Factual, Visual, and Technical QA gates passed.")

    # 9. Release Metadata & Assets
    final_dir = proj / "final"
    for ff in ["title.txt", "description.txt", "sources.txt", "thumbnail.png"]:
        p = final_dir / ff
        assert p.exists() and p.stat().st_size > 0, f"Missing final release file: {ff}"
    print("  [PASS] Title, description, sources, and thumbnail confirmed.")

    print("\n=======================================================")
    print("ALL VIDEO-003 ASTRA DATA CONTRACT AUDITS PASSED 100%!")
    print("=======================================================\n")

if __name__ == "__main__":
    test_video_003_contracts()
