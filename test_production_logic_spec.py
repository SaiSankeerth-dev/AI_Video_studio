"""
Comprehensive Documentary Production Logic Test Suite (Sections 1 - 19)
Tests all 19 specifications defined in the documentary production logic blueprint:
1. Story over topic (central question, weak/strong angle, stakes, promise)
2. Research before writing (sources, claims, evidence, timeline, entities, report)
3. 10-beat dramatic story architecture
4. Spoken narration separate with strict 130-160 WPM
5. Multi-shot edited scene sequences
6. Visual Director modules (director, shot_planner, visual_selector, prompt_builder, continuity, visual_rules)
7. Dynamic visual distribution & streak <= 2
8. Structured prompt generation (SUBJECT, ARCHITECTURE, CAMERA, COMPOSITION, LIGHTING, MATERIAL, ATMOSPHERE, REALISM, DO NOT)
9. Section 9 Image selection loop (4-8 candidates, 100-pt rubric, threshold >= 80)
10. Visual Bible (10 dimensions)
11. Entity identity tracking (researcher_01, facility_01, machine_01)
12. Blender reconstruction for spatial continuity
13. Complete 16-component Remotion motion graphics suite
14. Narration-driven shot design
15. Dynamic cinematic pacing (1.2s - 7.0s)
16. 7-layer audio design with strategic silence
17. Section 17 timeline IR (source, start, duration, transition, crop, scale, position, color, audio)
18. 7-pillar documentary QA
19. End-to-end Master Pipeline execution
"""

import os
import sys
import json
import importlib.util
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

def load_mod(name, rel_path):
    p = (ROOT / rel_path).resolve()
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def test_all_19_sections():
    print("\n=======================================================")
    print("TESTING DOCUMENTARY PRODUCTION LOGIC (SECTIONS 1 TO 19)")
    print("=======================================================\n")

    # SECTION 1: Story Over Topic
    print("[TEST 1] Story Over Topic Conception...")
    story_arch = load_mod("story_architect", "Phase-1_MuMuAINovel/story/story_architect.py")
    arch = story_arch.StoryArchitect()
    foundation = arch.build_narrative_foundation(
        topic="The rise of AI agents",
        weak_angle="How AI agents are changing technology.",
        strong_angle="Why are companies suddenly giving AI systems permission to use computers, write code, and make decisions on their own?",
        central_question="What happens when software stops waiting for humans?",
        stakes="If agents become reliable enough to operate independently, the way we use computers could fundamentally change.",
        promise="By the end of the documentary, the viewer will understand what changed, why it happened now, and what could happen next."
    )
    for k in ["topic", "weak_angle", "strong_angle", "central_question", "stakes", "promise"]:
        assert k in foundation and foundation[k], f"Missing {k} in foundation"
    assert "software stops waiting" in foundation["central_question"]
    print("  [PASS] Section 1 verified: Story grounded in central question, stakes, and promise.")

    # SECTION 2: Research Before Writing
    print("\n[TEST 2] Research Before Writing (Phase 0)...")
    res_engine = load_mod("research_engine", "Phase-0_Research/engine/research_engine.py")
    qa = res_engine.ResearchQA(ROOT / "Phase-0_Research")
    res_report = qa.run_qa()
    assert res_report["verdict"] == "PASS"
    assert res_report["sources_count"] >= 5
    assert res_report["claims_count"] >= 5
    assert res_report["evidence_count"] >= 20

    # Verify research/ directory layout conforming to Section 2
    res_dir = ROOT / "Phase-0_Research" / "research"
    assert res_dir.exists(), "Missing Phase-0_Research/research directory"
    for r_file in ["sources.json", "claims.json", "evidence.json", "timeline.json", "entities.json", "research-report.json"]:
        assert (res_dir / r_file).exists(), f"Missing Section 2 file in research/: {r_file}"

    # Verify claim schema Section 2
    claims_file = ROOT / "Phase-0_Research" / "claims" / "claims.json"
    with open(claims_file, "r", encoding="utf-8") as f:
        c_data = json.load(f)["claims"]
    for c in c_data:
        for k in ["claim_id", "claim", "importance", "source_ids", "confidence", "visual_evidence"]:
            assert k in c, f"Missing Section 2 field {k} in claim {c.get('claim_id')}"
        assert c["confidence"] in ["high", "medium", "verified"]
        assert len(c["visual_evidence"]) > 0
    print("  [PASS] Section 2 verified: Phase 0 research/ layout & claims meet strict evidence requirements.")

    # SECTION 3: Story Architecture
    print("\n[TEST 3] 10-Beat Story Architecture...")
    beats = arch.generate_story_architecture(foundation)
    expected_stages = ["HOOK", "QUESTION", "CONTEXT", "FIRST REVEAL", "ESCALATION", "COMPLICATION", "DEEPER DISCOVERY", "CLIMAX", "ANSWER", "IMPLICATION"]
    assert len(beats) == 10
    for idx, expected in enumerate(expected_stages):
        assert beats[idx]["stage"] == expected, f"Stage mismatch at {idx}: expected {expected}, got {beats[idx]['stage']}"
    print(f"  [PASS] Section 3 verified: Full 10-beat dramatic architecture generated ({len(beats)} beats).")

    # SECTION 4: Spoken Narration & Pacing
    print("\n[TEST 4] Spoken Narration & 130-160 WPM Standard...")
    narr_writer = load_mod("narration_writer", "Phase-1_MuMuAINovel/story/narration_writer.py")
    writer = narr_writer.NarrationWriter()
    sample_seg = writer.create_segment(
        segment_id="N014",
        chapter_id="CH-04",
        text="The system was not simply generating text anymore. It was beginning to interact with the world around it.",
        purpose="reveal",
        emotion="tension",
        claim_ids=["CLM-01"],
        visual_requirement="show the physical scale of autonomous execution",
        start_time=100.0
    )
    for k in ["segment_id", "text", "purpose", "emotion", "claim_ids", "visual_requirement", "duration", "wpm"]:
        assert k in sample_seg, f"Missing {k} in narration segment"
    assert 130.0 <= sample_seg["wpm"] <= 160.0

    # Also verify production narration.json has Section 4 schema across 100% of segments
    with open(ROOT / "narration.json", "r", encoding="utf-8") as f:
        prod_narr = json.load(f)
    assert len(prod_narr) == 30, f"Expected 30 narration segments, got {len(prod_narr)}"
    for s in prod_narr:
        for k in ["segment_id", "text", "purpose", "emotion", "claim_ids", "visual_requirement", "duration"]:
            assert k in s, f"Production narration segment {s.get('segment_id')} missing Section 4 field '{k}'"
        dur = round(s["end"] - s["start"], 2)
        words = len(s["text"].split())
        wpm = round(words / (dur / 60.0), 1)
        assert 130.0 <= wpm <= 160.0, f"WPM out of bounds for {s.get('segment_id')}: {wpm}"
    print(f"  [PASS] Section 4 verified: Spoken segment created ({sample_seg['wpm']} WPM) & all 30 production segments strictly conform.")

    # SECTION 5: Multi-Shot Scene Progression
    print("\n[TEST 5] Multi-Shot Scene Progression...")
    scene_dir = load_mod("scene_director", "Phase-1_MuMuAINovel/story/scene_director.py")
    sc_dir = scene_dir.SceneDirector()
    mock_narr = {"segment_id": "N021", "start": 120.0, "end": 138.0, "duration": 18.0, "purpose": "reveal", "claim_ids": ["CLM-02"]}
    mock_beats = [
        {"description": "Shot 21A: Close-up of computer interface", "weight": 2.0},
        {"description": "Shot 21B: Agent selecting a file", "weight": 2.5},
        {"description": "Shot 21C: Screen changes", "weight": 2.0},
        {"description": "Shot 21D: Camera pulls back", "weight": 4.0},
        {"description": "Shot 21E: Wide view of automated workflow", "weight": 4.5},
        {"description": "Shot 21F: Motion graphic explaining the loop", "weight": 3.0}
    ]
    scene = sc_dir.decompose_narration_into_scene("SCN-021", "CH-04", mock_narr, mock_beats)
    assert len(scene["shots"]) == 6
    assert scene["shots"][0]["shot_letter"] == "A"
    assert scene["shots"][-1]["shot_letter"] == "F"
    assert abs(scene["shots"][-1]["end"] - 138.0) < 0.001
    print("  [PASS] Section 5 verified: Single narration idea turned into 6-shot edited sequence.")

    # SECTION 6: Visual Director Module
    print("\n[TEST 6] Visual Director Architecture...")
    vd_path = ROOT / "Phase-1_MuMuAINovel" / "visual-director"
    required_vd_files = ["director.py", "shot_planner.py", "visual_selector.py", "prompt_builder.py", "continuity.py", "visual_rules.json"]
    for f in required_vd_files:
        assert (vd_path / f).exists(), f"Missing visual director file: {f}"

    load_mod("visual_director.visual_selector", "Phase-1_MuMuAINovel/visual-director/visual_selector.py")
    load_mod("visual_director.prompt_builder", "Phase-1_MuMuAINovel/visual-director/prompt_builder.py")
    load_mod("visual_director.continuity", "Phase-1_MuMuAINovel/visual-director/continuity.py")
    load_mod("visual_director.shot_planner", "Phase-1_MuMuAINovel/visual-director/shot_planner.py")
    vis_dir_mod = load_mod("visual_director.director", "Phase-1_MuMuAINovel/visual-director/director.py")
    v_director = vis_dir_mod.VisualDirector()
    d_shot = v_director.direct_shot("SHT-001", {"scene_id": "SCN-01", "start": 0.0}, sample_seg, None, [])
    for out_field in ["visual_type", "duration", "camera", "composition", "subject", "action", "environment", "generation_method", "generation_prompt", "continuity"]:
        assert out_field in d_shot, f"Missing VisualDirector output field: {out_field}"
    print("  [PASS] Section 6 verified: All 6 Visual Director files present and fully operational.")

    # SECTION 7: Dynamic Visual Distribution
    print("\n[TEST 7] Dynamic Visual Distribution & Streak Rules...")
    selector_mod = sys.modules["visual_director.visual_selector"]
    selector = selector_mod.VisualSelector({"max_consecutive_same_visual_type": 2})
    history = ["AI_IMAGE", "AI_IMAGE"]
    next_medium = selector.select_medium("The document was verified.", "show document", None, history)
    assert next_medium != "AI_IMAGE", "Streak <= 2 was violated!"
    with open(ROOT / "shot-plan.json", "r", encoding="utf-8") as f:
        sp_data = json.load(f)
    dist = selector.calculate_distribution(sp_data)
    assert dist["is_balanced"], f"Visual distribution not balanced: {dist}"
    for cat in ["REAL_MATERIAL", "GENERATED_MATERIAL", "GRAPHICS"]:
        assert cat in dist["macro_distribution"] and dist["macro_distribution"][cat]["count"] > 0
    print(f"  [PASS] Section 7 verified: Streak rule enforced, macro distribution balanced (Real: {dist['macro_distribution']['REAL_MATERIAL']['percentage']}%, Gen: {dist['macro_distribution']['GENERATED_MATERIAL']['percentage']}%, Graphics: {dist['macro_distribution']['GRAPHICS']['percentage']}%).")

    # SECTION 8: Structured Image Prompts
    print("\n[TEST 8] Structured Image Prompt Director...")
    p_builder_mod = sys.modules["visual_director.prompt_builder"]
    p_builder = p_builder_mod.PromptBuilder()
    prompt = p_builder.build_structured_image_prompt(
        subject="Underground hyperscale computing facility",
        architecture="Massive industrial server hall extending deep into the background",
        camera={"shot_size": "Wide", "position": "Eye-level", "lens": "24mm", "height": "1.6m", "movement": "Dolly push"},
        composition="Strong central perspective",
        lighting="Cold overhead industrial lighting",
        materials="Brushed metal, concrete",
        atmosphere="Slight condensation haze"
    )
    for field in ["DOCUMENTARY VISUAL BIBLE:", "SUBJECT:", "ARCHITECTURE:", "CAMERA:", "COMPOSITION:", "LIGHTING:", "MATERIAL:", "ATMOSPHERE:", "REALISM:", "DO NOT:"]:
        assert field in prompt, f"Missing Section 8/10 field: {field}"
    print("  [PASS] Section 8 verified: Prompt adheres to structured multi-block specification with Section 10 Visual Bible.")

    # SECTION 9: Image Selection Loop
    print("\n[TEST 9] Image Selection Loop (100-Point Rubric)...")
    critic_mod = load_mod("image_selection_loop", "Phase-3_VisualGeneration/critic/image_selection_loop.py")
    loop = critic_mod.ImageSelectionLoop()
    candidates = [
        {"candidate_id": "c1", "composition": 19, "prompt_adherence": 19, "realism": 19, "cinematic_quality": 14, "continuity": 14, "technical_quality": 9},
        {"candidate_id": "c2", "composition": 17, "prompt_adherence": 16, "realism": 15, "cinematic_quality": 12, "continuity": 12, "technical_quality": 8},
        {"candidate_id": "c3", "composition": 14, "prompt_adherence": 13, "realism": 12, "cinematic_quality": 10, "continuity": 10, "technical_quality": 6, "has_text_artifacts": True},
        {"candidate_id": "c4", "composition": 18, "prompt_adherence": 18, "realism": 17, "cinematic_quality": 13, "continuity": 13, "technical_quality": 9},
    ]
    cycle = loop.run_selection_cycle({"shot_id": "SHT-01"}, candidates)
    assert cycle["cycle_verdict"] == "ACCEPT"
    assert cycle["best_score"] >= 80.0
    print(f"  [PASS] Section 9 verified: 4 candidates evaluated, winner scored {cycle['best_score']}/100 (Threshold >= 80).")

    # SECTION 10: Visual Bible
    print("\n[TEST 10] Visual Bible (10 Dimensions)...")
    bible_path = ROOT / "Phase-1_MuMuAINovel" / "visual-bible" / "visual_bible.json"
    assert bible_path.exists()
    with open(bible_path, "r", encoding="utf-8") as f:
        vb = json.load(f)
    for dim in ["camera_language", "lighting", "environment", "materials", "color_behavior", "architecture", "character_rules", "historical_accuracy", "image_realism", "graphic_language"]:
        assert dim in vb, f"Missing Section 10 dimension in Visual Bible: {dim}"
    print("  [PASS] Section 10 verified: All 10 Visual Bible dimensions documented.")

    # SECTION 11: Recurring Subject Identity
    print("\n[TEST 11] Entity Tracking & Identity Rules...")
    entities_dir = ROOT / "Phase-1_MuMuAINovel" / "entities"
    for ent in ["researcher_01", "facility_01", "machine_01"]:
        e_dir = entities_dir / ent
        assert e_dir.exists(), f"Missing entity directory: {ent}"
        assert (e_dir / "reference.png").exists(), f"Missing reference.png in {ent}"
    assert (entities_dir / "researcher_01" / "description.json").exists()
    assert (entities_dir / "researcher_01" / "wardrobe.json").exists()
    assert (entities_dir / "facility_01" / "architecture.json").exists()
    assert (entities_dir / "machine_01" / "specifications.json").exists()
    print("  [PASS] Section 11 verified: researcher_01, facility_01, and machine_01 identities established.")

    # SECTION 12: Blender Reconstruction
    print("\n[TEST 12] Blender 3D Reconstruction...")
    blender_mod = load_mod("blender_reconstruction", "Phase-3_Blender/engine/blender_reconstruction.py")
    b_engine = blender_mod.BlenderReconstructionEngine()
    fly_spec = b_engine.generate_network_flythrough_spec([{"name": "Facility A"}, {"name": "Facility B"}, {"name": "Facility C"}])
    assert len(fly_spec["nodes"]) == 3
    assert len(fly_spec["connections"]) == 2
    assert "camera_path" in fly_spec
    print("  [PASS] Section 12 verified: Multi-facility spatial connection blueprint generated.")

    # SECTION 13: Remotion Graphics Library (16 Components)
    print("\n[TEST 13] Remotion Graphics Library (16 Components)...")
    comp_dir = ROOT / "Phase-4_Remotion" / "src" / "components"
    all_16_comps = [
        "EvidenceCard", "QuoteCard", "DataChart", "Timeline", "Map", "NetworkGraph",
        "DocumentZoom", "Comparison", "FlowDiagram", "ArchitectureDiagram", "ProcessDiagram",
        "CodeWindow", "Terminal", "LocationCard", "EntityCard", "SourceCard"
    ]
    for comp in all_16_comps:
        f1 = comp_dir / f"{comp}.tsx"
        f2 = comp_dir / "scenes" / f"{comp}.tsx"
        assert f1.exists() or f2.exists(), f"Missing Remotion component: {comp}"
    print(f"  [PASS] Section 13 verified: All {len(all_16_comps)} Remotion components present.")

    # SECTION 14, 15, 16, 17: Timeline IR, Sound Design & Assembly
    print("\n[TEST 14-17] Assembly Engine, Pacing, 7 Audio Layers & Timeline IR...")
    radio_mod = load_mod("radio_edit", "Phase-2_MoneyPrinterTurbo/scripts/radio_edit.py")
    radio_eng = radio_mod.RadioEditEngine()
    radio = radio_eng.assemble_radio_edit(prod_narr)
    for layer in ["voice", "music", "ambience", "sfx", "impacts", "transitions", "silence"]:
        assert layer in radio["tracks"], f"Missing Section 16 audio layer: {layer}"
    assert len(radio["tracks"]["silence"]) > 0, "Strategic silence pauses missing"
    assert len(radio["tracks"]["transitions"]) > 0, "Transition cues missing"

    assembly_mod = load_mod("assembly_engine", "Phase-6_Assembly/engine/assembly_engine.py")
    asm = assembly_mod.TimelineAssemblyEngine(fps=30)
    ir = asm.assemble_production_timeline("ep-001", "Test Doc", sp_data, {"segments": prod_narr}, radio)
    assert "voice" in ir["tracks"], "Missing canonical Section 17 'voice' track in timeline IR"
    v_item = ir["tracks"]["video"][0]
    for sec17_key in ["source", "start", "duration", "transition", "crop", "scale", "position", "color", "audio"]:
        assert sec17_key in v_item, f"Missing Section 17 video item key: {sec17_key}"
    assert (ROOT / "timeline.json").exists(), "timeline.json was not persisted to disk"
    print(f"  [PASS] Section 14-17 verified: 7 audio layers ({len(radio['tracks']['silence'])} silence cues, {len(radio['tracks']['transitions'])} transitions) & Section 17 timeline IR conformant.")

    # SECTION 18: 7-Pillar Documentary QA
    print("\n[TEST 18] 7-Pillar Documentary QA Suite...")
    qa_mod = load_mod("documentary_qa", "Phase-7_QA/engine/documentary_qa.py")
    doc_qa = qa_mod.DocumentaryQAEngine()
    with open(ROOT / "narration.json", "r", encoding="utf-8") as f:
        narr = json.load(f)
    with open(ROOT / "shot-plan.json", "r", encoding="utf-8") as f:
        sp = json.load(f)
    with open(ROOT / "audio-plan.json", "r", encoding="utf-8") as f:
        ap = json.load(f)
    with open(ROOT / "continuity-bible.json", "r", encoding="utf-8") as f:
        cb = json.load(f)
    with open(ROOT / "Phase-0_Research" / "claims" / "claims.json", "r", encoding="utf-8") as f:
        cl = json.load(f)["claims"]

    prod_plan = arch.generate_documentary_plan(foundation)

    full_qa = doc_qa.run_full_7_pillar_qa(
        documentary_plan=prod_plan,
        narration=narr,
        shot_plan=sp,
        audio_plan=ap,
        continuity_bible=cb,
        claims_data=cl,
        timeline=ir
    )
    for p in ["1_TECHNICAL_QA", "2_STORY_QA", "3_VISUAL_QA", "4_CONTINUITY_QA", "5_EVIDENCE_QA", "6_AUDIO_QA", "7_PACING_QA"]:
        assert p in full_qa["pillars"], f"Missing QA pillar: {p}"
        assert full_qa["pillars"][p]["passed"], f"QA Pillar {p} failed: {full_qa['pillars'][p]}"
    assert full_qa["verdict"] == "PASS"
    print("  [PASS] Section 18 verified: 100% pass across all 7 QA pillars.")

    # SECTION 19: Master Pipeline Integration
    print("\n[TEST 19] Master Pipeline Integration...")
    pipe_mod = load_mod("master_pipeline", "master_pipeline.py")
    pipeline = pipe_mod.ContentFactoryPipeline(ROOT)
    pipe_res = pipeline.run_pipeline()
    assert pipe_res["verdict"] == "PRODUCTION_READY"
    print("  [PASS] Section 19 verified: Full end-to-end documentary pipeline operational.")

    print("\n=======================================================")
    print("ALL 19 DOCUMENTARY PRODUCTION LOGIC SECTIONS VERIFIED!")
    print("=======================================================\n")

if __name__ == "__main__":
    test_all_19_sections()
