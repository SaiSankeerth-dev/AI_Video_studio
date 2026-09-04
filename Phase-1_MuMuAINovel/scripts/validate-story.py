import json
import sys
from pathlib import Path

def validate(story_file):
    with open(story_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Validated {story_file}: {len(data.get('scenes', []))} scenes found.")

if __name__ == '__main__':
    story_path = sys.argv[1] if len(sys.argv) > 1 else 'story.json'
    validate(story_path)
