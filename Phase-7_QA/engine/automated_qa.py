import json
import sys
from pathlib import Path

def run_automated_qa(timeline_path):
    with open(timeline_path, "r", encoding="utf-8") as f:
        timeline = json.load(f)

    report = {
        "episode_id": timeline.get("episode_id"),
        "total_frames": timeline.get("total_frames"),
        "duration_seconds": timeline.get("total_seconds"),
        "checks": {},
        "visual_repetition": {},
        "verdict": "PASS"
    }

    # 1. Technical Checks
    report["checks"]["resolution_1080p"] = timeline["resolution"]["width"] == 1920 and timeline["resolution"]["height"] == 1080
    report["checks"]["fps_30"] = timeline["fps"] == 30
    report["checks"]["has_voiceover"] = len(timeline["tracks"]["voiceover"]) > 0
    report["checks"]["has_music"] = len(timeline["tracks"]["music"]) > 0
    report["checks"]["has_captions"] = len(timeline["tracks"]["captions"]) > 0

    # 2. Visual Repetition Audit (Max 2 consecutive same visual archetype allowed)
    v_clips = timeline["tracks"]["video"]
    consecutive_counts = {}
    last_arch = None
    streak = 0
    violations = []

    for c in v_clips:
        arch = c.get("visual_archetype", "UNKNOWN")
        if arch == last_arch:
            streak += 1
            if streak > 2:
                violations.append(f"Excessive visual repetition: {arch} repeated {streak} times consecutively at frame {c['start_frame']}")
        else:
            streak = 1
            last_arch = arch
        consecutive_counts[arch] = consecutive_counts.get(arch, 0) + 1

    report["visual_repetition"]["archetype_distribution"] = consecutive_counts
    report["visual_repetition"]["violations"] = violations
    report["visual_repetition"]["score"] = "EXCELLENT" if len(violations) == 0 else "WARNING"

    if len(violations) > 0:
        report["verdict"] = "FLAGGED"

    print("=== AUTOMATED QA REPORT ===")
    print(f"Episode: {report['episode_id']} | Duration: {report['duration_seconds']:.2f}s ({report['total_frames']} frames)")
    print(f"Technical Checks: {report['checks']}")
    print(f"Visual Archetype Distribution: {report['visual_repetition']['archetype_distribution']}")
    print(f"Visual Repetition Violations: {len(violations)}")
    print(f"Overall QA Verdict: {report['verdict']}")

    return report

if __name__ == "__main__":
    t_file = sys.argv[1] if len(sys.argv) > 1 else r"D:\gitM\01_ContentFactory\projects\video-001\assembly\timeline.json"
    run_automated_qa(t_file)
