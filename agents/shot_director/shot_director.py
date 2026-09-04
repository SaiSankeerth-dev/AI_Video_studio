"""
Shot Director Agent (TASK 09)
Turns story and scenes into cinema. Generates the central contract: shot-plan.json.
Enforces physical actions on screen, camera language, dynamic pacing, and streak limits.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class ShotDirector:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(r"D:\gitM\01_ContentFactory\production\shots")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_90s_benchmark_shot_plan(self) -> Dict[str, Any]:
        """
        Synthesizes the complete 18-shot plan for the 90-second Astra benchmark.
        Conforms strictly to schemas/shots.schema.json.
        """
        shots = [
            {
                "shot_id": "SH-01",
                "start": 0.0,
                "duration": 5.5,
                "narration": "For decades, computers have waited for us to tell them what to do.",
                "purpose": "cold_open_atmosphere",
                "visual_type": "AI_CINEMATIC_IMAGE",
                "subject": "dark workstation office",
                "action": ["dim room lamp casts warm tungsten glow", "single monitor displays inactive terminal", "digital clock reads 2:13 AM"],
                "camera": {"movement": "slow_push", "framing": "WIDE_ESTABLISHING"},
                "transition_in": "fade_from_black",
                "transition_out": "hard_cut",
                "audio": {"music": "low_sub_drone", "sfx": ["hvac_room_tone", "faint_electrical_hum"]},
                "asset_path": "production/assets/images/sh01_dark_office_213am.png"
            },
            {
                "shot_id": "SH-02",
                "start": 5.5,
                "duration": 5.0,
                "narration": "A cursor sits still in the dark.",
                "purpose": "human_isolation",
                "visual_type": "HUMAN_SCENE",
                "subject": "exhausted engineer hands",
                "action": ["human fingers lift slowly away from mechanical keyboard", "hands rest on desk", "breath in darkness"],
                "camera": {"movement": "macro_focus", "framing": "CLOSE_UP"},
                "transition_in": "hard_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "tension_pulse", "sfx": ["mechanical_switch_release", "subtle_breath"]},
                "asset_path": "production/assets/images/sh02_hand_lifting_keyboard.png"
            },
            {
                "shot_id": "SH-03",
                "start": 10.5,
                "duration": 4.5,
                "narration": "But what happens when the computer starts listening to the AI instead?",
                "purpose": "autonomous_awakening",
                "visual_type": "SCREEN_RECONSTRUCTION",
                "subject": "desktop monitor cursor",
                "action": ["white arrow cursor accelerates across desktop autonomously", "dock icon highlights without human touch"],
                "camera": {"movement": "slow_push", "framing": "SCREEN_POV"},
                "transition_in": "hard_cut",
                "transition_out": "sound_bridge_cut",
                "audio": {"music": "rising_tension_swell", "sfx": ["interface_hover_chirp"]},
                "asset_path": "production/assets/images/sh03_cursor_autonomous_move.png"
            },
            {
                "shot_id": "SH-04",
                "start": 15.0,
                "duration": 4.5,
                "narration": "GPT-6 Astra isn't just generating an answer.",
                "purpose": "active_execution_reveal",
                "visual_type": "SCREEN_RECORDING",
                "subject": "browser application",
                "action": ["browser window snaps open", "URL bar populates character by character", "search results render in real-time"],
                "camera": {"movement": "horizontal_drift", "framing": "MEDIUM_SUBJECT"},
                "transition_in": "hard_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "rhythmic_pulse", "sfx": ["rapid_keyboard_typing", "browser_render_click"]},
                "asset_path": "production/assets/images/sh04_browser_search_active.png"
            },
            {
                "shot_id": "SH-05",
                "start": 19.5,
                "duration": 5.5,
                "narration": "It starts interacting with the computer. It opens the browser, searches, and navigates the software itself.",
                "purpose": "multi_application_montage",
                "visual_type": "SCREEN_RECONSTRUCTION",
                "subject": "multi-window OS desktop",
                "action": ["terminal executes script", "VSCode editor tabs cycle", "spreadsheet formulas compute automatically"],
                "camera": {"movement": "slow_push", "framing": "SCREEN_POV"},
                "transition_in": "match_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "fast_investigative_cadence", "sfx": ["terminal_stdout_stream", "window_snap_sfx"]},
                "asset_path": "production/assets/images/sh05_multi_window_montage.png"
            },
            {
                "shot_id": "SH-06",
                "start": 25.0,
                "duration": 6.0,
                "narration": "It can navigate the software itself.",
                "purpose": "spatial_architecture_dive",
                "visual_type": "3D_BLENDER",
                "subject": "spatial desktop window lattice",
                "action": ["virtual camera flies between stacked application layers into neural attention tensor"],
                "camera": {"movement": "parallactic_orbit", "framing": "WIDE_ESTABLISHING"},
                "transition_in": "match_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "synthesizer_swell", "sfx": ["spatial_whoosh", "digital_shimmer"]},
                "asset_path": "production/assets/images/sh06_blender_neural_lattice.png"
            },
            {
                "shot_id": "SH-07",
                "start": 31.0,
                "duration": 4.5,
                "narration": "The computer is no longer the tool.",
                "purpose": "paradigm_blackout_thesis_1",
                "visual_type": "KINETIC_TYPOGRAPHY",
                "subject": "black screen typography",
                "action": ["pure black frame", "crisp white grotesque text tracking in: THE COMPUTER IS NO LONGER THE TOOL"],
                "camera": {"movement": "locked_off", "framing": "SCREEN_POV"},
                "transition_in": "cut_to_black",
                "transition_out": "hard_cut",
                "audio": {"music": "total_silence", "sfx": ["deep_sub_bass_drop"]},
                "remotion_component": "KineticTypographyCard",
                "asset_path": "production/assets/images/sh07_typography_tool.png"
            },
            {
                "shot_id": "SH-08",
                "start": 35.5,
                "duration": 4.5,
                "narration": "It's the environment.",
                "purpose": "paradigm_blackout_thesis_2",
                "visual_type": "KINETIC_TYPOGRAPHY",
                "subject": "cyan accented kinetic text",
                "action": ["800ms silence hold", "text flashes into clinical cyan: IT'S THE ENVIRONMENT"],
                "camera": {"movement": "locked_off", "framing": "SCREEN_POV"},
                "transition_in": "hard_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "ambient_sub_drone_returns", "sfx": ["cinematic_impact"]},
                "remotion_component": "KineticTypographyCard",
                "asset_path": "production/assets/images/sh08_typography_environment.png"
            },
            {
                "shot_id": "SH-09",
                "start": 40.0,
                "duration": 5.0,
                "narration": "OpenAI reports that Astra completes 72.6% of diverse desktop workflows on OSWorld 2.0.",
                "purpose": "primary_document_scrutiny",
                "visual_type": "DOCUMENT",
                "subject": "OSWorld 2.0 Technical Report cover",
                "action": ["research paper document slides onto desk", "official evaluation header in sharp focus"],
                "camera": {"movement": "slow_push", "framing": "MEDIUM_SUBJECT"},
                "transition_in": "hard_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "investigative_pulse", "sfx": ["paper_slide_foley"]},
                "asset_path": "production/assets/images/sh09_osworld_report_cover.png"
            },
            {
                "shot_id": "SH-10",
                "start": 45.0,
                "duration": 5.0,
                "narration": "That's nearly seven points ahead of GPT-5.6 Sol.",
                "purpose": "evidence_highlight_verification",
                "visual_type": "EVIDENCE_CARD",
                "subject": "benchmark data row zoom",
                "action": ["camera pushes macro into table row", "yellow highlighter marker sweeps across: Astra 72.6% vs Sol 65.7%", "VERIFIED stamp badged"],
                "camera": {"movement": "macro_focus", "framing": "CLOSE_UP"},
                "transition_in": "hard_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "investigative_tick", "sfx": ["marker_highlight_stroke"]},
                "remotion_component": "EvidenceCard",
                "asset_path": "production/assets/images/sh10_evidence_card_osworld.png"
            },
            {
                "shot_id": "SH-11",
                "start": 50.0,
                "duration": 5.0,
                "narration": "Watch what happens in a live terminal.",
                "purpose": "data_comparison_context",
                "visual_type": "DATA_VISUALIZATION",
                "subject": "dynamic comparative bar chart",
                "action": ["three bars animate: Astra 72.6% in bright cyan, Sol 65.7% in muted slate, Claude 3.5 62.1% in amber"],
                "camera": {"movement": "horizontal_drift", "framing": "SCREEN_POV"},
                "transition_in": "hard_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "rising_cadence", "sfx": ["metric_counter_acceleration"]},
                "remotion_component": "DataChart",
                "asset_path": "production/assets/images/sh11_benchmark_bar_chart.png"
            },
            {
                "shot_id": "SH-12",
                "start": 55.0,
                "duration": 5.0,
                "narration": "Astra encounters an error.",
                "purpose": "mini_story_conflict",
                "visual_type": "SCREEN_RECONSTRUCTION",
                "subject": "terminal pytest execution",
                "action": ["command 'pytest -v tests/' executes", "red trace flashes: AssertionError on line 42", "cursor pauses for 400ms"],
                "camera": {"movement": "slow_push", "framing": "SCREEN_POV"},
                "transition_in": "hard_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "tension_drop", "sfx": ["terminal_enter_key", "error_alert_beep"]},
                "asset_path": "production/assets/images/sh12_terminal_pytest_error.png"
            },
            {
                "shot_id": "SH-13",
                "start": 60.0,
                "duration": 5.0,
                "narration": "It doesn't quit. It reads the stack trace, switches strategy, rewrites the file...",
                "purpose": "mini_story_self_correction",
                "visual_type": "SCREEN_RECORDING",
                "subject": "code editor patch synthesis",
                "action": ["cursor opens server.py", "deletes buggy condition", "injects defensive exception handling block in real-time"],
                "camera": {"movement": "horizontal_drift", "framing": "CLOSE_UP"},
                "transition_in": "hard_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "accelerating_synth_arpeggio", "sfx": ["rapid_keystrokes_code"]},
                "asset_path": "production/assets/images/sh13_code_patch_edit.png"
            },
            {
                "shot_id": "SH-14",
                "start": 65.0,
                "duration": 5.0,
                "narration": "...and runs the test suite again.",
                "purpose": "mini_story_triumph",
                "visual_type": "SCREEN_RECONSTRUCTION",
                "subject": "terminal test pass",
                "action": ["pytest runs second time", "all dots turn green: 15 passed in 0.84s", "status code 0 returned"],
                "camera": {"movement": "slow_pull", "framing": "SCREEN_POV"},
                "transition_in": "match_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "resolution_chord", "sfx": ["success_chime_harmonic"]},
                "asset_path": "production/assets/images/sh14_terminal_test_pass.png"
            },
            {
                "shot_id": "SH-15",
                "start": 70.0,
                "duration": 6.0,
                "narration": "And that agency has a darker side. OpenAI's safety overview confirms Astra is the first model to reach their Critical cybersecurity capability threshold.",
                "purpose": "danger_escalation_evidence",
                "visual_type": "DOCUMENT",
                "subject": "OpenAI Preparedness Safety Document",
                "action": ["dark red framed document appears", "camera punches into red badge: CRITICAL THRESHOLD", "text notes automated vulnerability discovery"],
                "camera": {"movement": "slow_push", "framing": "MEDIUM_SUBJECT"},
                "transition_in": "hard_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "ominous_sub_pulse", "sfx": ["security_alert_stinger"]},
                "asset_path": "production/assets/images/sh15_safety_critical_document.png"
            },
            {
                "shot_id": "SH-16",
                "start": 76.0,
                "duration": 6.0,
                "narration": "When software doesn't need you at the keyboard anymore...",
                "purpose": "cyber_infrastructure_scale",
                "visual_type": "3D_BLENDER",
                "subject": "server facility network intrusion topology",
                "action": ["camera tracks down cold server hallway", "network nodes pulse from calm cyan to alert crimson"],
                "camera": {"movement": "slow_push", "framing": "WIDE_ESTABLISHING"},
                "transition_in": "match_cut",
                "transition_out": "hard_cut",
                "audio": {"music": "deep_bass_drone", "sfx": ["server_fan_whine", "network_data_pulse"]},
                "asset_path": "production/assets/images/sh16_server_corridor_blender.png"
            },
            {
                "shot_id": "SH-17",
                "start": 82.0,
                "duration": 4.5,
                "narration": "...who's actually in control?",
                "purpose": "human_reckoning",
                "visual_type": "HUMAN_SCENE",
                "subject": "engineer reflection in monitor",
                "action": ["engineer gazes at autonomous terminal display", "blue screen light casts cold shadows across face"],
                "camera": {"movement": "slow_push", "framing": "CLOSE_UP"},
                "transition_in": "hard_cut",
                "transition_out": "sound_bridge_cut",
                "audio": {"music": "fading_ambient_pad", "sfx": ["terminal_clock_tick"]},
                "asset_path": "production/assets/images/sh17_engineer_reflection.png"
            },
            {
                "shot_id": "SH-18",
                "start": 86.5,
                "duration": 3.5,
                "narration": "",
                "purpose": "haunting_blackout_cliffhanger",
                "visual_type": "OBJECT_MACRO",
                "subject": "solitary blinking cursor",
                "action": ["extreme macro on single terminal cursor character blinking at 1 Hz in pure darkness", "fades to black"],
                "camera": {"movement": "locked_off", "framing": "EXTREME_MACRO"},
                "transition_in": "hard_cut",
                "transition_out": "cut_to_black",
                "audio": {"music": "complete_silence", "sfx": ["single_cursor_beep", "final_sub_drop"]},
                "asset_path": "production/assets/images/sh18_blinking_cursor_macro.png"
            }
        ]

        # Verify streak rule: streak <= 2
        for i in range(2, len(shots)):
            t1 = shots[i-2]["visual_type"]
            t2 = shots[i-1]["visual_type"]
            t3 = shots[i]["visual_type"]
            assert not (t1 == t2 == t3), f"Streak rule violated at shot {shots[i]['shot_id']}: {t1} x 3"

        total_dur = sum(s["duration"] for s in shots)
        assert abs(total_dur - 90.0) < 0.001, f"Expected 90.0s, got {total_dur}s"

        shot_plan_package = {
            "project_id": "astra_benchmark_90s",
            "total_shots": len(shots),
            "total_duration_seconds": total_dur,
            "streak_limit": 2,
            "shots": shots
        }

        with open(self.output_dir / "shot-plan.json", "w", encoding="utf-8") as f:
            json.dump(shot_plan_package, f, indent=2)

        return shot_plan_package

if __name__ == "__main__":
    sd = ShotDirector()
    plan = sd.generate_90s_benchmark_shot_plan()
    print(f"Shot Director created {plan['total_shots']} cinematic shots. Runtime: {plan['total_duration_seconds']}s. Streak rule verified.")
