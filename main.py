"""Run the AI Shorts Studio.

    python main.py                      # offline mock run (no keys, no deps)
    python main.py "Your topic here"    # offline mock run on a custom topic
    python main.py "Topic" --real       # live: OpenAI + (optionally) real render
    python main.py "Topic" --gemini     # live: Google Gemini + GEMINI_API_KEY
    python main.py "Topic" --ollama     # live: local Ollama, no keys, no quota

Asset + export flags (combine with any LLM mode above):
    --assets DIR        folder of your clips/images/audio   (sets ASSETS_DIR)
    --asset-mode MODE   user | auto | hybrid                (sets ASSET_MODE)
    --capcut            write an editable CapCut draft       (sets EXPORT_TARGET)

  e.g.  python main.py "Sunset facts" --ollama --asset-mode hybrid --assets ./my_clips --capcut

For --real you need:  pip install openai  and  export OPENAI_API_KEY=...
For --gemini:         pip install google-genai  and  export GEMINI_API_KEY=...
For --ollama:         pip install ollama  and  `ollama pull qwen3:8b` (server running)
                      override model with  OLLAMA_MODEL=qwen3:14b
For auto/hybrid stock: export PEXELS_API_KEY=...  (no key -> offline B-roll)
For real MP4s also:   pip install moviepy ffmpeg  and  export USE_REAL_RENDER=1
"""

from __future__ import annotations

import os
import sys

from llm import GeminiLLM, MockLLM, OllamaLLM, OpenAILLM
from orchestrator import build_studio
from state import VideoState


def _flag_value(name: str, default: str | None = None) -> str | None:
    """Read `--name VALUE` from argv."""
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
            return sys.argv[i + 1]
    return default


def main() -> None:
    # positional args = anything that is not a flag and not a flag's value
    flag_values = {"--assets", "--asset-mode"}
    args: list[str] = []
    skip = False
    for j, tok in enumerate(sys.argv[1:]):
        if skip:
            skip = False
            continue
        if tok in flag_values:
            skip = True
            continue
        if not tok.startswith("--"):
            args.append(tok)
    real = "--real" in sys.argv
    gemini = "--gemini" in sys.argv
    ollama = "--ollama" in sys.argv

    # asset + export config -> env (read by asset_manager_agent / export_agent)
    if "--asset-mode" in sys.argv:
        os.environ["ASSET_MODE"] = _flag_value("--asset-mode", "user")
    if "--assets" in sys.argv:
        os.environ["ASSETS_DIR"] = _flag_value("--assets", "assets")
    if "--capcut" in sys.argv:
        os.environ["EXPORT_TARGET"] = "capcut"

    topic = args[0] if args else "Messi's greatest World Cup moment"
    if ollama:
        model = os.environ.get("OLLAMA_MODEL", "qwen3:8b")
        llm, mode = OllamaLLM(model=model), f"OLLAMA:{model}"
    elif gemini:
        llm, mode = GeminiLLM(), "GEMINI"
    elif real:
        llm, mode = OpenAILLM(), "REAL"
    else:
        llm, mode = MockLLM(), "MOCK"

    print(f"\n=== AI Shorts Studio  |  mode: {mode}  |  topic: {topic} ===\n")

    studio = build_studio(llm)
    state = studio.run(VideoState(topic=topic))

    print("\n--- RESULT ---")
    print(f"Story hook    : {state.story.get('hook', '')}")
    print(f"Rejected facts: {state.rejected_facts}")
    print(f"Timeline      : {state.timeline.get('total_seconds')}s, "
          f"{len(state.timeline.get('clips', []))} clips")
    print(f"QA passed     : {state.qa_passed}  {state.qa_report.get('checks', {})}")
    print(f"Exports       : {list(state.exports.values())}")
    if state.errors:
        print(f"Errors        : {state.errors}")

    with open("last_run_state.json", "w") as f:
        f.write(state.to_json())
    print("\nFull state written to last_run_state.json")


if __name__ == "__main__":
    main()
