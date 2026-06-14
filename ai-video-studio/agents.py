"""The agents.

DESIGN DECISION (this is the disagreement with the original spec, made concrete):
Not every box deserves an LLM. Roles are split into two kinds.

  Reasoning agents (need a model):
    CEO, Research, Fact Checker, Story Architect, Visual Director, Music Director,
    Caption Director (word *choice* only)

  Deterministic agents (plain code -- cheaper, reliable, testable):
    Asset Manager, Senior Editor, QA, Export, and caption *timing*

Every agent has the same shape: `def agent(state, llm) -> state`. That signature
is intentionally LangGraph-compatible, so porting later is mechanical.
"""

from __future__ import annotations

import json

from llm import LLM
from state import Caption, Shot, VideoState

MAX_SHOT_SECONDS = 2.0  # the "no visual longer than 2s" rule, enforced in code


def _json(llm: LLM, role: str, user: str) -> dict:
    """Call the model, expect JSON, parse defensively."""
    system = f"ROLE: {role}\n" + _SYSTEM_PROMPTS[role]
    raw = llm.complete(system, user, json_mode=True)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
        return json.loads(cleaned)


# --------------------------------------------------------------------------
# Reasoning agents
# --------------------------------------------------------------------------
def ceo_agent(state: VideoState, llm: LLM) -> VideoState:
    """Production manager: turns a raw topic into a brief the rest of the team uses."""
    src = state.topic or state.script
    out = _json(llm, "ceo", f"Topic or script:\n{src}")
    state.brief = out
    state.target_seconds = int(out.get("length_seconds", state.target_seconds))
    state.note("CEO", f"brief set: {out.get('emotion')} / {state.target_seconds}s / {out.get('audience')}")
    return state


def research_agent(state: VideoState, llm: LLM) -> VideoState:
    out = _json(llm, "research", f"Topic: {state.topic}\nBrief: {json.dumps(state.brief)}")
    state.facts = out.get("facts", [])
    state.note("Research", f"gathered {len(state.facts)} candidate facts")
    return state


def fact_checker_agent(state: VideoState, llm: LLM) -> VideoState:
    """Removes unverifiable / false claims before they reach the story."""
    out = _json(llm, "fact_checker", "Facts to check:\n" + "\n".join(state.facts))
    reject_terms = [t.lower() for t in out.get("reject_if_contains", [])]
    for fact in state.facts:
        if any(term in fact.lower() for term in reject_terms):
            state.rejected_facts.append(fact)
        else:
            state.verified_facts.append(fact)
    if state.rejected_facts:
        state.note("FactChecker", f"REJECTED {len(state.rejected_facts)}: {out.get('reason', '')}")
    state.note("FactChecker", f"{len(state.verified_facts)} facts verified")
    return state


def story_architect_agent(state: VideoState, llm: LLM) -> VideoState:
    """The most important reasoning agent: facts -> hook / conflict / payoff / CTA."""
    out = _json(llm, "story_architect", "Verified facts:\n" + "\n".join(state.verified_facts))
    state.story = out
    state.note("StoryArchitect", f"hook: {out.get('hook', '')[:48]}...")
    return state


def visual_director_agent(state: VideoState, llm: LLM) -> VideoState:
    """Proposes the shot list. Senior Editor turns it into the final timeline."""
    out = _json(llm, "visual_director", f"Story: {json.dumps(state.story)}\nTarget: {state.target_seconds}s")
    state.shots = [Shot(**s) for s in out.get("shots", [])]
    state.note("VisualDirector", f"proposed {len(state.shots)} shots")
    return state


def music_director_agent(state: VideoState, llm: LLM) -> VideoState:
    out = _json(llm, "music_director", f"Story: {json.dumps(state.story)}\nTarget: {state.target_seconds}s")
    state.music_plan = out.get("segments", [])
    state.note("MusicDirector", f"{len(state.music_plan)} music segments")
    return state


def caption_director_agent(state: VideoState, llm: LLM) -> VideoState:
    """LLM picks emphasis words; TIMING is generated deterministically here.

    In production, replace the even-spacing below with Whisper word timestamps
    aligned to the real voiceover. Captions are an ASR problem, not a creative
    one -- a model guessing timestamps is exactly how you get drift.
    """
    out = _json(llm, "caption_director", f"Narration: {state.story.get('hook','')} {state.story.get('payoff','')}")
    emphasis = {w.upper() for w in out.get("emphasis_words", [])}

    narration = f"{state.story.get('hook', '')} {state.story.get('payoff', '')}".split()
    if narration:
        per_word = state.target_seconds / len(narration)
        for i, word in enumerate(narration):
            clean = word.strip(".,!?").upper()
            state.captions.append(
                Caption(
                    start=round(i * per_word, 2),
                    end=round((i + 1) * per_word, 2),
                    text=word,
                    emphasis=clean in emphasis,
                )
            )
    state.note("CaptionDirector", f"{len(state.captions)} word-level captions (timing = even split; swap for Whisper)")
    return state


# --------------------------------------------------------------------------
# Deterministic agents (no LLM)
# --------------------------------------------------------------------------
def asset_manager_agent(state: VideoState, llm: LLM) -> VideoState:
    """Resolves each shot to a real asset path via the 3-mode AssetSource.

    Mode is chosen by env (ASSET_MODE = user | auto | hybrid):
      user   -> your folder (ASSETS_DIR)
      auto   -> stock API / generated B-roll (legally usable)
      hybrid -> your folder first, agent fills the gaps (preferred)

    The fallback to a round-robin / generated clip prevents a missing file from
    killing the whole render.
    """
    import os

    from assets import get_asset_source

    mode = os.environ.get("ASSET_MODE", "user")
    root = os.environ.get("ASSETS_DIR", "assets")
    cache = os.environ.get("ASSET_CACHE", "auto_assets")

    try:
        source = get_asset_source(mode, root=root, topic=state.topic, cache_dir=cache)
    except Exception as exc:
        state.errors.append(f"Asset source ({mode}): {exc}")
        for shot in state.shots:
            shot.asset = "clips/_fallback_stock.mp4"
        state.assets = {"mode": mode, "resolved": 0, "fallbacks": len(state.shots)}
        state.note("AssetManager", f"{mode} source failed: {exc}")
        return state

    resolved = 0
    for i, shot in enumerate(state.shots):
        asset = source.match(shot.description, i)
        if asset:
            shot.asset = asset.path
            resolved += 1
        else:
            shot.asset = "clips/_fallback_stock.mp4"
    state.assets = {"mode": mode, "resolved": resolved,
                    "fallbacks": len(state.shots) - resolved}
    state.note("AssetManager",
               f"[{mode}] {resolved} resolved, {state.assets['fallbacks']} fallbacks")
    return state


def _split_to_max(shots: list[Shot], scale: float) -> list[Shot]:
    """Scale every shot to fit the target, then split any clip > MAX_SHOT_SECONDS."""
    clips: list[Shot] = []
    for shot in shots:
        start, end = shot.start * scale, shot.end * scale
        cursor = start
        while end - cursor > MAX_SHOT_SECONDS + 1e-6:
            clips.append(Shot(round(cursor, 2), round(cursor + MAX_SHOT_SECONDS, 2),
                              shot.description, shot.asset))
            cursor += MAX_SHOT_SECONDS
        clips.append(Shot(round(cursor, 2), round(end, 2), shot.description, shot.asset))
    return clips


def senior_editor_agent(state: VideoState, llm: LLM) -> VideoState:
    """The actual product. Turns the shot list into a timeline that holds attention.

    Rules enforced as CODE, not vibes:
      - fit total duration to target_seconds
      - no clip longer than 2s  -> a visual change at least every 2s
      - add motion to any clip >= 1.5s, alternate sfx on cuts
    Motion choice is a simple rule here; an LLM could pick per-shot motion if
    you find rules too flat.
    """
    if not state.shots:
        state.errors.append("Senior Editor: no shots to edit")
        return state

    raw_total = max(s.end for s in state.shots)
    scale = state.target_seconds / raw_total if raw_total else 1.0
    clips = _split_to_max(state.shots, scale)

    motions = ["zoom-in", "pan-left", "zoom-out", "pan-right"]
    for i, clip in enumerate(clips):
        if clip.duration >= 1.0:
            clip.motion = motions[i % len(motions)]
        clip.sfx = "whoosh" if i % 2 == 0 else "impact"

    state.timeline = {
        "fps": 30,
        "resolution": [1080, 1920],
        "total_seconds": round(clips[-1].end, 2),
        "clips": [vars(c) | {"duration": c.duration} for c in clips],
        "music": state.music_plan,
        "captions": [vars(c) for c in state.captions],
    }
    state.note("SeniorEditor", f"timeline built: {len(clips)} clips, {state.timeline['total_seconds']}s")
    return state


def qa_agent(state: VideoState, llm: LLM) -> VideoState:
    """Objective checks only. If something fails, the graph loops back to editing."""
    t = state.timeline
    clips = t.get("clips", [])
    checks: dict[str, bool] = {}

    total = t.get("total_seconds", 0)
    checks["duration_on_target"] = abs(total - state.target_seconds) <= 1.0
    checks["no_clip_over_2s"] = all(c["duration"] <= MAX_SHOT_SECONDS + 1e-6 for c in clips)

    # dead-section check: gap between visual changes (cuts) must stay <= 2s
    boundaries = [0.0] + [c["end"] for c in clips]
    biggest_gap = max((b - a for a, b in zip(boundaries, boundaries[1:])), default=0)
    checks["no_dead_sections"] = biggest_gap <= MAX_SHOT_SECONDS + 1e-6

    caption_span = max((c["end"] for c in t.get("captions", [])), default=0)
    checks["captions_cover_video"] = caption_span >= total * 0.9

    state.qa_report = {"checks": checks, "biggest_gap": round(biggest_gap, 2)}
    state.qa_passed = all(checks.values())
    if not state.qa_passed:
        state.qa_attempts += 1
        failed = [k for k, v in checks.items() if not v]
        state.note("QA", f"FAILED {failed} (attempt {state.qa_attempts})")
    else:
        state.note("QA", "all checks passed")
    return state


def export_agent(state: VideoState, llm: LLM) -> VideoState:
    """Exports the timeline. Target chosen by env EXPORT_TARGET:

      manifest (default) / mp4  -> render.py (JSON manifest or FFmpeg/MoviePy)
      capcut                    -> capcut.py writes an editable CapCut draft
    """
    import os

    target = os.environ.get("EXPORT_TARGET", "manifest").lower()
    base = state.topic or "short"

    if target == "capcut":
        from capcut import build_capcut_draft

        draft = build_capcut_draft(
            state.timeline,
            asset_for_clip=lambda i, clip: clip.get("asset"),
            base_name=base,
            with_transitions=True,
        )
        state.exports = {"capcut": draft}
        state.note("Export", f"CapCut draft written: {draft}")
        return state

    from render import render_variants

    state.exports = render_variants(state.timeline, base_name=base)
    state.note("Export", f"exported: {', '.join(state.exports.keys())}")
    return state


# --------------------------------------------------------------------------
# System prompts for the reasoning agents (the real instructions the model gets)
# --------------------------------------------------------------------------
_SYSTEM_PROMPTS: dict[str, str] = {
    "ceo": (
        "You are a short-form video production manager. From a topic or script, "
        "produce a brief. Return JSON: {length_seconds:int, audience:str, goal:str, "
        "emotion:str, style:str}. Keep length_seconds between 15 and 60."
    ),
    "research": (
        "You are a research agent for a short video. Return JSON {facts: [string]} "
        "with 4-7 concrete, verifiable facts. No opinions, no filler."
    ),
    "fact_checker": (
        "You verify facts for accuracy. Return JSON {reject_if_contains:[string], "
        "reason:str} listing substrings that mark a claim as false or unverifiable."
    ),
    "story_architect": (
        "You turn facts into a retention-first narrative for a vertical short. "
        "Return JSON {hook, conflict, payoff, cta}. The hook must work in under 2 seconds."
    ),
    "visual_director": (
        "You plan the shot list for a vertical short. Return JSON {shots:[{start, "
        "end, description}]} covering the full target length. No shot longer than 2s."
    ),
    "music_director": (
        "You plan the music arc. Return JSON {segments:[{start, end, mood, intensity}]} "
        "that rises toward the payoff and resolves at the end."
    ),
    "caption_director": (
        "You choose which words to emphasize in burned-in captions. Return JSON "
        "{emphasis_words:[string]} -- only the highest-impact words."
    ),
}
