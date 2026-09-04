import json
import jsonschema
from pathlib import Path

def validate_shot_plan(shot_plan_path):
    schema_path = Path(__file__).parents[1] / "schemas" / "visual-shot.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with open(shot_plan_path, "r", encoding="utf-8") as f:
        shots = json.load(f)

    if isinstance(shots, dict) and "shots" in shots:
        shots = shots["shots"]

    errors = []
    for s in shots:
        try:
            jsonschema.validate(instance=s, schema=schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Shot {s.get('shot_id', 'UNKNOWN')} Validation Error: {e.message}")

    if len(errors) == 0:
        print(f"PASS: All {len(shots)} shots conform strictly to visual-shot.schema.json (Section 28)!")
        return True
    else:
        print(f"FAIL: {len(errors)} validation errors detected:")
        for err in errors:
            print(f" - {err}")
        return False

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else r"D:\gitM\01_ContentFactory\projects\video-001\visual-director\cinematic_shots_v1.json"
    validate_shot_plan(path)
